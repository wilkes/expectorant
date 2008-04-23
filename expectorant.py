# Stolen from http://www.voidspace.org.uk/python/mock.html
class SentinelObject(object):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '<SentinelObject "%s">' % self.name

class Sentinel(object):
    def __init__(self):
        self._sentinels = {}
        
    def __getattr__(self, name):
        return self._sentinels.setdefault(name, SentinelObject(name))

sentinel = Sentinel()


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
        return "<Mock %s>" % self.name

class Expectation(object):
    def __init__(self, mock, name):
        self.mock = mock
        self.method_name = name
        self.called_times = 0
        self.return_value = None
        self.args = []
        self.kwargs = None
        self.expects_args = False
    
    def __call__(self, *args, **kwargs):
        self.__verify_args(*args, **kwargs)
        self.called_times += 1
        return self.return_value
    
    def with_args(self, *args, **kwargs):
        self.expects_args = True
        self.args.extend(args)
        self.kwargs = kwargs
    
    def called(self, num):
        self.expected_number_of_calls = num
        return self
    
    def returns(self, ret):
        self.return_value = ret
        return self
        
    def verify(self):
        confirm(self.called_times == self.expected_number_of_calls, 
                "Expected '%s' to be called %s times, but was called %s times" % (self.method_name, self.expected_number_of_calls, self.called_times))
    
    def __verify_args(self, *args, **kwargs):
        if not self.expects_args: return
        confirm(len(self.args) == len(args), 
            "Expected %s positional arguments, but received %s\n\t%s" % (len(self.args), len(args), repr(args)))
        i = 0
        for expected, received in zip(self.args, args):
            confirm(expected is received, 
                        "position %d: expected: %s received: %s" % (i, repr(expected), repr(received)))
            i += 1
            
        confirm(len(self.kwargs) == len(kwargs), 
            "Expected %s positional arguments, but received %s" % (len(self.kwargs), len(kwargs)))
        for k in self.kwargs:
            confirm(k in kwargs, "missing keyword %s" % k)
            expected = self.kwargs[k]
            received = kwargs[k]
            confirm(expected is received, 
                        "keyword %s: expected: %s received: %s" % (k, repr(expected), repr(received)))
            

def confirm(bool, msg):
    if bool: return
    raise VerificationFailure, msg

class VerificationFailure(Exception):
    pass