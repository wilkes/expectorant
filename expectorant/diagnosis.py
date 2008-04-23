def confirm(bool, msg):
    assert bool, msg

def deny(bool, msg):
    assert not bool, msg

def surely(target, func, *expected):
    if not func(target, *expected):
        if hasattr(func, 'surely_message'):
            msg = func.surely_message(target, *expected)
        else:
            msg = "%s failed with %s, %s" % (repr(func), repr(target), repr(expected))
        raise AssertionError, msg

def surely_not(target, func, *expected):
    if func(target, *expected):
        if hasattr(func, 'surely_not_message'):
            msg = func.surely_not_message(target, *expected)
        else:
            msg = "%s failed with %s, %s" % (repr(func), repr(target), repr(expected))
        raise AssertionError, msg

def same_as(a,b): return a is b
same_as.surely_message = lambda a,b: "%s is not the same as %s" % (repr(a), repr(b))
same_as.surely_not_message = lambda a,b: "%s is the same as %s" % (repr(a), repr(b))
is_same_as = same_as
is_the_same_as = same_as

def equals(a,b): return a == b
equals.surely_message = lambda a,b: "%s does not equal %s" % (repr(a), repr(b))
equals.surely_not_message = lambda a,b: "%s equals %s" % (repr(a), repr(b))


def raises(func, exception_class, message=None):
    try:
        func()
        return False
    except exception_class, e:
        if message:
            if not str(e) == message:
                raise AssertionError, "<%s> does not equal <%s>" % (str(e), message)
        return True
raises.surely_message = lambda *args: "%s was not raised" % args[2]
raises.surely_not_message = lambda *args: "%s was raised" % args[2]
