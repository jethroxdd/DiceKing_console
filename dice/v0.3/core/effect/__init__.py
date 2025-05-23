from enum import IntEnum
from ui.color import Paint

class EffectPriority(IntEnum):
    GOOD = 0
    BAD = 1

class BaseEffect:
    name = "base effect"
    value = 0
    duration = 0
    priority = EffectPriority.GOOD
    color = 0
    
    
    def __str__(self):
        return f"{Paint("burn", 214)}[{self.value}|{self.duration}]"