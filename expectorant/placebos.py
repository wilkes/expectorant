from expectorant.diagnosis import confirm

class Dispenser(object):
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.placebos = {}
    
    def __call__(self, name=None):
        return Placebo(name)
    
    def __getattr__(self, name):
        return self.placebos.setdefault(name, Placebo(name))
    
    def __enter__(self):
        return self
    
    def __exit__( self, type, value, tb):
        self.verify()
    
    def verify(self):
        for m in self.placebos.itervalues():
            m.verify()
dispenser = Dispenser()

# Stolen from http://www.voidspace.org.uk/python/mock.html, Sentinel pattern
class Placebo(object):
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
    
    def once(self):
        return self.called(1)
    
    def twice(self):
        return self.called(2)
    
    def returns(self, ret):
        self.return_value = ret
        return self
    
    def verify(self):
        if self.expected_times_called:
            confirm(self.times_called == self.expected_times_called,
                    "%s expected to be called %s times, but was called %s times" %
                        (repr(self), self.expected_times_called, self.times_called))
    
    def __verify_args(self, *args, **kwargs):
        if self.expects_args:
            self.__verify_positional_args(args)
            self.__verify_keywords_args(kwargs)
    
    def __verify_positional_args(self, args):
        confirm(len(self.args) == len(args),
            "%s expected %s positional arguments, but received %s\n\t%s" %
                (repr(self), len(self.args), len(args), repr(args)))
        for (i, (expected, received)) in enumerate(zip(self.args, args)):
            confirm(expected is received,
                        "%s at position %d: expected: %s received: %s" %
                            (repr(self), i, repr(expected), repr(received)))
    
    def __verify_keywords_args(self, kwargs):
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
