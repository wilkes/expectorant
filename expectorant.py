class Mockery(object):
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.mocks = {}

    def __call__(self, name=None):
        return Mock(name)

    def __getattr__(self, name):
        return self.mocks.setdefault(name, Mock(name))
    
    def __enter__(self):
        return self

    def __exit__( self, type, value, tb ):
        self.verify()
    
    def verify(self):
        for m in self.mocks.itervalues():
            m.verify()
mock = Mockery()

# Stolen from http://www.voidspace.org.uk/python/mock.html, Sentinel pattern
class Mock(object):
    def __init__(self, name='Mock'):
        self.name = name
        self.expectations = []

    def receives(self, method_name):
        exp = Expectation(self, method_name)
        self.__dict__[method_name] = exp
        self.expectations.append(exp)
        return exp            

    def verify(self):
        for each in self.expectations:
            each.verify()
            
    def __repr__(self):
        return "<Mock '%s'>" % self.name

    def __str__(self):
        return repr(self)

class Expectation(object):
    def __init__(self, mock, name):
        self.mock = mock
        self.method_name = name
        self.times_called = 0
        self.return_value = None
        self.args = []
        self.kwargs = None
        self.expects_args = False
        self.expected_times_called = 0
    
    def __call__(self, *args, **kwargs):
        self.__verify_args(*args, **kwargs)
        self.times_called += 1
        return self.return_value
    
    def with_args(self, *args, **kwargs):
        self.expects_args = True
        self.args.extend(args)
        self.kwargs = kwargs
        return self
    
    def called(self, num):
        self.expected_times_called = num
        return self
    
    def returns(self, ret):
        self.return_value = ret
        return self
        
    def verify(self):
        if self.expected_times_called:
            confirm(self.times_called == self.expected_times_called, 
                    "%s expected to be called %s times, but was called %s times" % 
                        (repr(self), self.expected_times_called, self.times_called))
    
    def __verify_args(self, *args, **kwargs):
        if not self.expects_args: return
        confirm(len(self.args) == len(args), 
            "%s expected %s positional arguments, but received %s\n\t%s" % 
                (repr(self), len(self.args), len(args), repr(args)))
        for (i, (expected, received)) in enumerate(zip(self.args, args)):
            confirm(expected is received, 
                        "%s at position %d: expected: %s received: %s" % 
                            (repr(self), i, repr(expected), repr(received)))
            
        confirm(len(self.kwargs) == len(kwargs), 
            "%s expected %s positional arguments, but received %s" % 
                (repr(self), len(self.kwargs), len(kwargs)))
        for k in self.kwargs:
            confirm(k in kwargs, "%s missing keyword %s" % (repr(self), k))
            confirm(self.kwargs[k] is kwargs[k], 
                        "%s keyword %s: expected: %s received: %s" % 
                            (repr(self), k, repr(self.kwargs[k]), repr(kwargs[k])))

    def __repr__(self):
        return "<%s '%s.%s'>" % (self.__class__.__name__, self.mock.name, self.method_name)
            

def confirm(bool, msg):
    if not bool: raise VerificationFailure, msg

def surely(target, func, *expected):
    if not func(target, *expected):
        if hasattr(func, 'surely_message'):
            msg = func.surely_message(target, *expected)
        else:
            msg = "%s failed with %s, %s" % (repr(func), repr(target), repr(expected))
        raise VerificationFailure, msg

def surely_not(target, func, *expected):
    if func(target, *expected):
        if hasattr(func, 'surely_not_message'):
            msg = func.surely_not_message(target, *expected)
        else:
            msg = "%s failed with %s, %s" % (repr(func), repr(target), repr(expected))
        raise VerificationFailure, msg

def same_as(a,b):
    return a is b
same_as.surely_message = lambda a,b: "%s is not the same as %s" % (repr(a), repr(b))
same_as.surely_not_message = lambda a,b: "%s is the same as %s" % (repr(a), repr(b))
is_same_as = same_as
is_the_same_as = same_as

def raises(func, exception_class, message=None):
    try:
        func()
        return False
    except exception_class, e:
        if message: return str(e) == message
        return True
raises.surely_message = lambda *args: "%s was not raised" % args[2]
raises.surely_not_message = lambda *args: "%s was raised" % args[2]

class VerificationFailure(Exception): pass