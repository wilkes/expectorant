from __future__ import with_statement
from expectorant.placebos import dispenser, Dispenser, Expectation
from expectorant.diagnosis import surely, raises, same_as, equals
from expectorant.clinic import TextClinic
import sys

class SampleTrial(object):
    def setUp(self):
        self.log = 'setUp '

    def set_up(self):    pass
    def setup(self):     pass

    def tear_down(self):
        self.log += 'tear_down'

    def tearDown(self):  pass
    def teardown(self):  pass
    def _ignored(self):  pass
    
    def this_is_trial1(self):
        self.log += 'this_is_trial1 '

    def this_is_another_trial(self):
        """expected output"""
        pass
    
    def this_test_fails(self):
        assert False
    
    def this_errors_out(self):
        raise Exception, 'boom!'

def has_length_of(l, length):
    return len(l) == length
    
class TestClinicTextRunner(object):
    def setUp(self):
        self.clinic = TextClinic()
        
    def test_call_order(self):
        trial = SampleTrial()
        self.clinic.run_trial(trial, 'this_is_trial1')
        surely(trial.log, equals, 'setUp this_is_trial1 tear_down')
        
    def test_calls_all_trials(self):
        self.clinic.run_trials(SampleTrial)
        surely(self.clinic.results, has_length_of, 4)
        surely(self.clinic.failures, has_length_of, 1)
        surely(self.clinic.passes, has_length_of, 2)
        surely(self.clinic.errors, has_length_of, 1)
