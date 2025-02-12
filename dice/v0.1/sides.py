from effect import StaticEffect
from side import Side
import effects


# Side functions

class MultiSide:
    def __init__(self, sides):
        self.sides = sides
    
    def roll(self, entity):
        for side in self.sides:
            side.roll(entity)

class ColdAttack(MultiSide):
    def __init__(self, attackValue, slownessValue=1):
        self.sides = [Attack(attackValue), Effect(effects.Slowness(slownessValue, 1), False)]

class FireAttack(MultiSide):
    def __init__(self, attackValue, burnValue=1):
        self.sides = [Attack(attackValue), Effect(effects.Burn(burnValue), False)]

class VampireAttack(MultiSide):
    def __init__(self, value):
        self.sides = [Attack(value), Effect(effects.Heal(value//2), False)]

class LightningAttack(MultiSide):
    def __init__(self, value):
        self.sides = [Attack(value), Effect(effects.Stun(1), False)]


class Empty(Side):
    def __init__(self):
        super().__init__("empty", None, None)
    
    def roll(self, entity):
        pass

class Attack(Side):
    def __init__(self, value):
        super().__init__("attack", value, None)
    
    def roll(self, entity):
        entity.damage += self.value

class Defense(Side):
    def __init__(self, value):
        super().__init__("defense", value, None)
    
    def roll(self, entity):
        entity.defense += self.value

class Coin(Side):
    def __init__(self, value):
        super().__init__("coin", value, None)
    
    def roll(self, entity):
        entity.coin = self.value

class Crit(Side):
    def __init__(self):
        super().__init__("crit", True, None)
    
    def roll(self, entity):
        entity.isCrit = True

class Effect(Side):
    def __init__(self, value, is_self):
        super().__init__(f"{'self' if is_self else "other"}-effect", value, None)
        self.is_self = is_self
    
    def roll(self, entity):
        if self.is_self:
            entity.addTempEffect(self.value)
        else:
            entity.target.addTempEffect(self.value)

class Stop(Side):
    def __init__(self):
        super().__init__("stop", "stop", None)
    
    def roll(self, entity):
        pass

class Pass(Side):
    def __init__(self):
        super().__init__("empty", None, None)

    def roll(self):
        pass

class GoldStealler(Side):
    def __init__(self, value):
        super().__init__("gold-stealler", value, None)
    
    def roll(self, entity):
        entity.gold -= self.value