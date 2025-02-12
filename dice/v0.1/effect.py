class BaseEffect:
    def __init__(self, name: str, value, _apply, duration: int, isGood: bool, visible=True):
        '''
        apply = apply(Effect, Entity)
        '''
        self.name = name
        self.value = value
        self._apply = _apply
        self.duration = duration
        self.isGood = isGood
        self.isEnded = False
        self.visible = visible

    def add(self, effect):
        self.value += effect.value
        self.duration = max(self.duration, effect.duration)

    def shift(self):
        pass
    
    def decreaseDuration(self):
        self.duration -= 1
        if self.duration <= 0:
            self.duration = 0
            self.isEnded = True
    
    def apply(self, entity):
        self._apply(self, entity)
        return self.value

class DecreaseEffect(BaseEffect):
    def shift(self):
        self.value -= 1
        if self.value <= 0:
            self.value = 0
            self.isEnded = True
        self.duration = self.value

class IncreaseEffect(BaseEffect):
    def shift(self):
        self.value += 1
        self.decreaseDuration()

class InstantEffect(BaseEffect):
    def shift(self):
        self.value = 0
        self.isEnded = True

class StaticEffect(BaseEffect):
    def shift(self):
        self.decreaseDuration()
        
    def add(self, effect):
        self.duration += effect.duration