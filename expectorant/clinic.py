import sys
SETUP_METHODS = ('set_up', 'setUp', 'setup')
TEAR_DOWN_METHODS = ('tear_down', 'tearDown', 'teardown')

class Clinic(object):
    def __init__(self):
        self.__listeners = []

    def add_listener(self, listener):
        self.__listeners.append(listener)

    def run_trials(self, trial_class):
        for t in trial_class.__dict__:
             if self.__is_test_name(t):
                 self.run_trial(trial_class, t)
    
    def run_trial(self, trial_class, method_name):
        trial = trial_class()
        try:
            self.__notify_listeners('on_start', trial_class, method_name)
            self.__run_matching(trial, SETUP_METHODS, 'on_setup')
            self.__run_matching(trial, [method_name])
            self.__run_matching(trial, TEAR_DOWN_METHODS, 'on_teardown')
        except:
            pass
        finally:
            self.__notify_listeners('on_completion', trial_class, method_name, sys.exc_info())

    def __run_matching(self, trial, matching, callback=None):
        matching = [m for m in trial.__class__.__dict__ if m in matching]
        for m in matching:
            getattr(trial, m)()
            if callback: 
                self.__notify_listeners(callback, trial.__class__, m)

    def __notify_listeners(self, calback, *args): 
        [getattr(l, calback)(*args) for l in self.__listeners if hasattr(l, calback)]
    
    def __is_test_name(self, funcname):
        return not (funcname.startswith('_') or
                    funcname in SETUP_METHODS or
                    funcname in TEAR_DOWN_METHODS)
