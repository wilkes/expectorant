import re
def camelcase_to_underscore(str):
    return re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', str).lower().strip('_')

def humanize(str):
    return camelcase_to_underscore(str).replace('_', ' ')

SETUP_METHODS = ('set_up', 'setUp', 'setup')
TEAR_DOWN_METHODS = ('tear_down', 'tearDown', 'teardown')

class TextClinic:
    def run_trials(self, a_class):
        self.results = []
        for trial_method in self.__trials_for(a_class):
            try:
                self.run_trial(a_class(), trial_method)
                self.results.append((trial_method, 'pass'))
            except AssertionError:
                self.results.append((trial_method, 'failure'))
            except:
                self.results.append((trial_method, 'error'))
    
    def get_passes(self):
        return [p for p in self.results if p[1] == 'pass']
    passes = property(get_passes)

    def get_errors(self):
        return [p for p in self.results if p[1] == 'error']
    errors = property(get_errors)
    
    def get_failures(self):
        return [p for p in self.results if p[1] == 'failure']
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
