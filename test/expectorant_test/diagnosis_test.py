from expectorant.diagnosis import surely, raises, same_as, isa

class TestDiagnosis(object):
    def test_surely_operator_is(self):
        is_the_same_as = is_same_as = same_as
        surely(1, same_as, 1)
        surely(1, is_same_as, 1)
        surely(1, is_the_same_as, 1)
        
    def test_same_as_message(self):
        surely(lambda: surely(1, same_as, 2), raises,  AssertionError, 'Failed: 1 is 2')
        
    def test_custom_error(self):
        def barfs(x): assert False, 'Barf!'
        surely(lambda: surely(1, barfs), raises, AssertionError, 'Barf!')
    
    def test_unary(self):
        def is_the_truth(x): assert x is True, "%s is not True" % x
        surely(True, is_the_truth)
        surely(lambda: surely(False, is_the_truth), raises, AssertionError, "False is not True")
    
    def test_isa(self):
        surely(1, isa, type(1))

    def test_isa_fails(self):
        surely(lambda: surely("a", isa, type(1)), 
            raises, AssertionError, "Expected %s to be of type %s" % (repr("a"), type(1)))