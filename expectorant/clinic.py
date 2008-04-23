import sys
SETUP_METHODS = ('set_up', 'setUp', 'setup')
TEAR_DOWN_METHODS = ('tear_down', 'tearDown', 'teardown')

class TextClinic:
    def run_trials(self, a_class):
        self.results = []
        for trial_method in self.__trials_for(a_class):
            try:
                self.run_trial(a_class(), trial_method)
            except AssertionError, e:
                self.results.append((trial_method, 'failure', sys.exc_info()))
            except:
                self.results.append((trial_method, 'error', sys.exc_info()))
            else:
                self.results.append((trial_method, 'pass', sys.exc_info()))
    
    def get_ran(self):
        return [p[0] for p in self.results]
    ran = property(get_ran)
        
    def get_passes(self):
        return [p[0] for p in self.results if p[1] == 'pass']
    passes = property(get_passes)

    def get_errors(self):
        return [p[0] for p in self.results if p[1] == 'error']
    errors = property(get_errors)
    
    def get_failures(self):
        return [p[0] for p in self.results if p[1] == 'failure']
    failures = property(get_failures)
    
    def run_trial(self, trial, method_name):
        self.__run_matching(trial, SETUP_METHODS)
        self.__run_matching(trial, [method_name])
        self.__run_matching(trial, TEAR_DOWN_METHODS)
    
    def __run_matching(self, trial, matching):
        for m in trial.__class__.__dict__:
            if m in matching:
                getattr(trial, m)()
    
    def __trials_for(self, a_class):
        return [t for t in a_class.__dict__ if self.__is_test_name(t)]
    
    def __is_test_name(self, funcname):
        return not (funcname.startswith('_') or
                    funcname in SETUP_METHODS or
                    funcname in TEAR_DOWN_METHODS)
