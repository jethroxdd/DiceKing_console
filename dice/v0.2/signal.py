class _Signal:
    def __init__(self, functions):
        self.functions = functions
    
    def add(self, func):
        self.functions.append(func)
        
    def emit(self, *args):
        for function in self.functions:
            function(*args)