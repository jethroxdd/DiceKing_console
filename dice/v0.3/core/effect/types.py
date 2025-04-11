from ui.color import Paint
from core.effect import BaseEffect

'''
Order:
0 - good
1 - bad
'''

class Burn(BaseEffect):
    def __init__(self, duration):
        super().__init__("burn", 1, duration, 1)
    
    @property
    def is_ended(self):
        return self.duration <= 0
    
    def apply(self, source):
        source.take_true_damage(self.value)
    
    def add(self, effect):
        self.duration += effect.duration
    
    def tick(self):
        self.duration = max(0, self.duration - 1)

    def __str__(self):
        return f"{Paint("burn", 214)}[{self.value}|{self.duration}]"
