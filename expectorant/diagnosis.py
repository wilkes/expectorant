def surely(target, func, *expected):
    func(target, *expected)

def same_as(a,b):
    assert a is b, "Failed: %r is %r" % (a,b)

def equals(a,b):
    assert a == b, "Failed: %r == %r" % (a,b)

def is_true(a):
    assert a, "Failed: %r is truth" % a

def has_length_of(l, length):
    assert len(l) == length, "Expected length of %d, but was %d" % (length, len(l))

def is_in(item, list):
    assert item in list, "%r not in %r" % (item, list)

def raises(func, exception_class, message=None):
    try:
        func()
    except exception_class, e:
        if message:
            assert str(e) == message, "<%s> does not equal <%s>" % (e, message)
    else:
        raise AssertionError, "%r was not raised" % exception_class
        