import enum
from color import Fore, Back, Style

'''
Order:
-1 - empty
 0 - crit
 1 - shield
 2 - runes
 3 - good_effect
 4 - damage
 5 - bad_effect
'''  


class EffectType(enum.Enum):
    damage = "hidden"
    self_damage = "hidden"
    burn = f"{Fore(202)}горение{Style.RESET_ALL}"
    poison = f"{Fore(92)}яд{Style.RESET_ALL}"

class BaseEffect:
    def __init__(self, _type, value , duration, order, is_good: bool):
        '''
        apply = apply(Effect, Entity)
        '''
        self.name = _type.name
        self.symbol = _type.value
        self.value = value
        self.duration = duration
        self.order = order
        self.is_good = is_good
        self.is_ended = False
    
    def tick(self):
        self.duration -= 1
        if self.duration <= 0:
            self.duration = 0
            self.is_ended = True 

class Burn(BaseEffect):
    def __init__(self, duration):
        super().__init__(EffectType.burn, value=duration//2, duration=duration, order=5, is_good=False)
    
    def tick(self):
        super().tick()
        self.value = self.duration//2
    
    def add(self, effect):
        self.duration += effect.duration
        
    def apply(self, entity):
        entity.take_damage(self.value)

class Poison(BaseEffect):
    def __init__(self, value):
        super().__init__(EffectType.poison, value=value, duration=3, order=5, is_good=False)
    
    def add(self, effect):
        self.duration = 3
        self.value = max(self.value, effect.value)
        
    def apply(self, entity):
        entity.take_damage(self.value)

class Damage(BaseEffect):
    def __init__(self, value):
        super().__init__(EffectType.damage, value=value, duration=0, order=4, is_good=False)
    
    def add(self, effect):
        self.value += effect.value
        
    def apply(self, entity):
        entity.take_damage(self.value)

class SelfDamage(BaseEffect):
    def __init__(self, value):
        super().__init__(EffectType.self_damage, value=value, duration=0, order=4, is_good=False)
    
    def add(self, effect):
        self.value += effect.value
        
    def apply(self, entity):
        entity.take_damage(self.value)