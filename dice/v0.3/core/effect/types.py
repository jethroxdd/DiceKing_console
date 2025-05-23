from ui.color import Paint, Color
from core.effect import BaseEffect, EffectPriority

class Burn(BaseEffect):
    name = "burn"
    value = 0
    duration = 0
    priority = EffectPriority.BAD
    color = Color.FIRE
    
    @property
    def is_ended(self):
        return self.duration <= 0
    
    def apply(self, source):
        return source.take_true_damage(self.value)
        
    def stack(self, effect):
        self.duration += effect.duration
        return self.duration
    
    def tick(self):
        self.duration = max(0, self.duration - 1)
        return self.is_ended

