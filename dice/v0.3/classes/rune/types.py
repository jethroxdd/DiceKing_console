from classes.rune import BaseRune
import classes.effect.types as EffectTypes
from UI.color import Paint
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
        return Paint("empty", 240)

class Attack(BaseRune):
    def __init__(self):
        super().__init__("attack", 4)
    
    def apply(self, value, source, target, roll_results):
        target.take_damage(value)
    
    def __str__(self):
        return Paint("attack", 124)

class Shield(BaseRune):
    def __init__(self):
        super().__init__("shield", 1)
    
    def apply(self, value, source, target, roll_results):
        source.take_shield(value)
        
    def __str__(self):
        return Paint("shield", 26)

class Fire(BaseRune):
    def __init__(self):
        super().__init__("fire", 1)
    
    def apply(self, value, source, target, roll_results):
        target.take_damage(value)
        target.add_effect(EffectTypes.Burn(value))
        
    def __str__(self):
        return Paint("fire", 202)