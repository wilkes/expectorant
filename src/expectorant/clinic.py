import sys
SETUP_METHODS = ('setUp', 'setup', 'set_up',)
TEAR_DOWN_METHODS = ('tearDown', 'teardown', 'tear_down',)

class Clinic(object):
    def __init__(self):
        self.__listeners = []

    def add_listener(self, listener):
        self.__listeners.append(listener)

    def run_trials(self, trial_class):
        for t in trial_class.__dict__:
             if self.__is_test_name(t):
                 self.run_trial(trial_class(), t)
    
    def run_trial(self, trial, method_name):
        trial_class = trial.__class__
        try:
            self.__notify_listeners('on_start', trial_class, method_name)
            context = self.__run_first_matching(trial, SETUP_METHODS, 'on_setup')
            self.__run_test(trial, method_name, context)
            self.__run_first_matching(trial, TEAR_DOWN_METHODS, 'on_teardown')
        except:
            pass
        finally:
            self.__notify_listeners('on_completion', trial_class, method_name, sys.exc_info())

    def __run_test(self, trial, method_name, context):
        func = getattr(trial, method_name)
        if self.__can_run_with_context(func, context):
            self.__run_with_context(func, context)
        else:
            func()
            
    def __can_run_with_context(self, func, context):
        return context and func.func_code.co_argcount == 2
        
    def __run_with_context(self, func, context):
        context.__enter__()
        try:
            func(context)
        finally:
            context.__exit__(sys.exc_info())
        
            
    def __run_first_matching(self, trial, matching, callback=None):
        for m in matching:
            if hasattr(trial, m):
                result = getattr(trial, m)()
                if callback: 
                    self.__notify_listeners(callback, trial.__class__, m)
                return result

    def __notify_listeners(self, callback, *args): 
        for l in self.__listeners:
            if hasattr(l, callback): 
                getattr(l, callback)(*args)
    
    def __is_test_name(self, funcname):
        return not (funcname.startswith('_') or
                    funcname in SETUP_METHODS or
                    funcname in TEAR_DOWN_METHODS)
