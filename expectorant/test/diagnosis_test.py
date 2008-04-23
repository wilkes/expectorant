from __future__ import with_statement
from expectorant.diagnosis import surely, surely_not, raises, same_as

class TestDiagnosis(object):
    def test_surely_operator_is(self):
        is_the_same_as = is_same_as = same_as
        surely(1, same_as, 1)
        surely(1, is_same_as, 1)
        surely(1, is_the_same_as, 1)
    
    def test_surely_not_operator_is(self):
        surely_not(2, same_as, 1)
    
    def test_same_as_message(self):
        surely(lambda: surely(1, same_as, 2), raises,  AssertionError, '1 is not the same as 2')
    
    def test_same_as_not_message(self):
        surely(lambda: surely_not(1, same_as, 1), raises, AssertionError, '1 is the same as 1')
    
    def test_custom_error(self):
        def barfs(x): assert False, 'Barf!'
        surely(lambda: surely(1, barfs), raises, AssertionError, 'Barf!')
    
    def test_unary(self):
        is_the_truth = lambda x: x is True
        is_the_truth.surely_message = lambda x: "%s is not True" % x
        is_the_truth.surely_not_message = lambda x: "%s is True" % x
        
        surely(True, is_the_truth)
        surely(lambda: surely(False, is_the_truth), raises, AssertionError, "False is not True")
        surely_not(False, is_the_truth)
        surely(lambda: surely_not(True, is_the_truth), raises, AssertionError, "True is True")