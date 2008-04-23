from expectorant.diagnosis import surely, is_true, equals, is_in, has_length_of
from expectorant.clinic import Clinic
import sys

class SampleTrial(object):
    def setUp(self):  pass
    def set_up(self): pass
    def setup(self):  pass

    def tear_down(self): pass
    def tearDown(self):  pass
    def teardown(self):  pass

    def _ignored(self):  pass
    
    def this_is_trial1(self):           pass
    def this_is_another_trial(self):    pass
    def this_test_fails(self):          assert False
    def this_errors_out(self):          raise Exception, 'boom!'

class ClinicListener(object):
    def __init__(self):
        self.ran      = []
        self.passes   = []
        self.failures = []
        self.errors   = []

    def on_completion(self, trial_class, method_name, exc_info):
        self.ran.append(method_name)
        exc_type = exc_info[0]
        if exc_type:
            if exc_type is AssertionError:
                self.failures.append(method_name)
            else:
                self.errors.append(method_name)
        else:
            self.passes.append(method_name)
    

class SimpleLogger(object):
    def __init__(self):
        self.log = ''
    
    def on_setup(self, trial_class, method_name):
        self.note(method_name)

    def on_teardown(self, trial_class, method_name):
        self.note(method_name)

    def on_start(self, trial_class, method_name):
        self.note(method_name)

    def on_completion(self, trial_class, method_name, exc_info):
        self.note('completed')
    
    def note(self, s):
        self.log += s + ' '

    
class TestClinic(object):
    def setUp(self):
        self.clinic = Clinic()
        self.listener = ClinicListener()
        self.clinic.add_listener(self.listener)
    
    def test_call_order(self):
        logger = SimpleLogger()
        self.clinic.add_listener(logger)
        self.clinic.run_trial(SampleTrial, 'this_is_trial1')
        expected = 'this_is_trial1 setup set_up setUp tearDown teardown tear_down completed '
        surely(logger.log, equals, expected)

    def test_collecting_results(self):
        self.clinic.run_trials(SampleTrial)
        surely(self.listener.ran, has_length_of, 4)
        surely('this_is_trial1', is_in, self.listener.ran)
        surely('this_is_another_trial', is_in, self.listener.ran)
        surely('this_test_fails', is_in, self.listener.ran)
        surely('this_errors_out', is_in, self.listener.ran)
    
    def test_collecting_failures(self):
        self.clinic.run_trials(SampleTrial)
        surely(self.listener.failures, has_length_of, 1)
        surely('this_test_fails', is_in, self.listener.failures)
        
    def test_collecting_passes(self):
        self.clinic.run_trials(SampleTrial)
        surely(self.listener.passes, has_length_of, 2)
        surely('this_is_trial1', is_in, self.listener.passes)
        surely('this_is_another_trial', is_in, self.listener.passes)

    def test_collecting_errors(self):
        self.clinic.run_trials(SampleTrial)
        surely(self.listener.errors, has_length_of, 1)
        surely('this_errors_out', is_in, self.listener.errors)
    