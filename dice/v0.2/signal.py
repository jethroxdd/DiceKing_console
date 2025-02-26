class Signal:
    def __init__(self, signals = []):
        self.signals = signals
    
    def add(self, func):
        self.signals.append(func)
        
    def emit(self, args=[]):
        for signal in self.signals:
            signal(args)

class EntitySignal(Signal):
    def __init__(self, entity, signals = []):
        super().__init__(signals)
        self.entity = entity
    
    def emit(self):
        for signal in self.signals:
            signal(self.entity)