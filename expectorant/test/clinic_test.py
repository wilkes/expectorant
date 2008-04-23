from expectorant.diagnosis import surely, is_true, equals, is_in, has_length_of
from expectorant.clinic import TextClinic

log = ''
def note(s):
    global log
    log += s + ' '

class SampleTrial(object):
    def setUp(self):
        note('setUp')

    def set_up(self):    pass
    def setup(self):     pass

    def tear_down(self):
        note('tear_down')

    def tearDown(self):  pass
    def teardown(self):  pass
    def _ignored(self):  pass
    
    def this_is_trial1(self):
        note('this_is_trial1')

    def this_is_another_trial(self):
        """expected output"""
        note('this_is_another_trial')
    
    def this_test_fails(self):
        note('this_test_fails')
        assert False
    
    def this_errors_out(self):
        note('this_errors_out')
        raise Exception, 'boom!'
    
class TestClinicTextRunner(object):
    def setUp(self):
        global log
        log = ''
        self.clinic = TextClinic()
        
    def test_call_order(self):
        trial = SampleTrial()
        self.clinic.run_trial(trial, 'this_is_trial1')
        surely(log, equals, 'setUp this_is_trial1 tear_down ')
        
    def test_collecting_results(self):
        self.clinic.run_trials(SampleTrial)
        surely(self.clinic.results, has_length_of, 4)
        surely('this_is_trial1', is_in, self.clinic.ran)
        surely('this_is_another_trial', is_in, self.clinic.ran)
        surely('this_test_fails', is_in, self.clinic.ran)
        surely('this_errors_out', is_in, self.clinic.ran)
    
    def test_collecting_failures(self):
        self.clinic.run_trials(SampleTrial)
        surely(self.clinic.failures, has_length_of, 1)
        surely('this_test_fails', is_in, self.clinic.failures)
        
    def test_collecting_passes(self):
        self.clinic.run_trials(SampleTrial)
        surely(self.clinic.passes, has_length_of, 2)
        surely('this_is_trial1', is_in, self.clinic.passes)
        surely('this_is_another_trial', is_in, self.clinic.passes)

    def test_collecting_errors(self):
        self.clinic.run_trials(SampleTrial)
        surely(self.clinic.errors, has_length_of, 1)
        surely(self.clinic.errors[0], equals, 'this_errors_out')
