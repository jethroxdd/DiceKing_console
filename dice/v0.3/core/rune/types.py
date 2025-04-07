from core.rune import BaseRune
import core.effect.types as EffectTypes
from ui.color import Paint, Color
'''
Order:
0 - utility
1 - shield
2 - effect
3 - self damage
4 - damage
'''

class Empty(BaseRune):
    def __init__(self):
        super().__init__("empty", 0)
    
    def apply(self, value, source, target, roll_results):
        pass
    
    def __str__(self):
        return Paint("empty", Color.EMPTY)

class Attack(BaseRune):
    def __init__(self):
        super().__init__("attack", 4)
    
    def apply(self, value, source, target, roll_results):
        target.take_damage(value)
    
    def __str__(self):
        return Paint("attack", Color.ATTACK)

class Shield(BaseRune):
    def __init__(self):
        super().__init__("shield", 1)
    
    def apply(self, value, source, target, roll_results):
        source.take_shield(value)
        
    def __str__(self):
        return Paint("shield", Color.SHIELD)

class Fire(BaseRune):
    def __init__(self):
        super().__init__("fire", 1)
    
    def apply(self, value, source, target, roll_results):
        target.take_damage(value)
        target.add_effect(EffectTypes.Burn(value))
        
    def __str__(self):
        return Paint("fire", Color.FIRE)

class Crit(BaseRune):
    def __init__(self):
        super().__init__("crit", 0)
    
    def apply(self, value, source, target, roll_results):
        for result in roll_results:
            result.value_mult_mods += [2]
        
    def __str__(self):
        return Paint("crit", Color.CRIT)