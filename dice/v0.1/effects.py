from effect import DecreaseEffect, StaticEffect, IncreaseEffect, InstantEffect
# Effect functions
def Pass(side, entity):
    pass

class Bleed(DecreaseEffect):
    '''
    Deal damage that decreases every turn until it ends
    '''
    def __init__(self, value):
        '''
        :param value: amount of stacks.
        '''
        super().__init__("bleed", value, None, value, False)
    
    def apply(self, entity):
        entity.takeDirectDamage(self.value)

class Harm(InstantEffect):
    def __init__(self, value):
        super().__init__("harm", value, None, 1, False)
    
    def apply(self, entity):
        entity.Damage(self.value)

class Heal(InstantEffect):
    def __init__(self, value):
        super().__init__("heal", value, None, 1, True)
    
    def apply(self, entity):
        entity.takeHeal(self.value)
        for effect in entity.effects:
            if effect.name == "bleed":
                entity.effects.remove(effect)

class Regen(DecreaseEffect):
    def __init__(self, value):
        super().__init__("regen", value, None, value, True)
    
    def apply(self, entity):
        entity.takeHeal(self.value)
        for effect in entity.effects:
            if effect.name == "bleed":
                entity.effects.remove(effect)

class Slowness(StaticEffect):
    def __init__(self, value, duration):
        super().__init__("slowness", value, None, duration, False)
    
    def apply(self, entity):
        for i in entity.dicesChosen:
            entity.dices[i].cooldown += self.value
            
class Poison(StaticEffect):
    '''
    Deal flat damage for 3 turns
    '''
    def __init__(self, value):
        super().__init__("poison", value, None, 3, False)
    
    def apply(self, entity):
        entity.takeDamage(self.value)   
    
    def add(self, effect):
        self.value = max(self.value, effect.value)
        self.duration = max(self.duration, effect.duration)        

class Stun(StaticEffect):
    def __init__(self, duration):
        super().__init__("stun", 1, None, duration, False)
    
    def apply(self, entity):
        for dice in entity.dices:
            dice.cooldown += 1
        
class Burn(StaticEffect):
    def __init__(self, duration):
        super().__init__("burn", 1, None, duration, False)
    
    def apply(self, entity):
        entity.takeDamage(self.value)
    
    def add(self, effect):
        self.duration += effect.duration