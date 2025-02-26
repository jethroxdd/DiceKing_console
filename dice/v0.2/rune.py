import enum
import effect
from color import Fore, Back, Style, Color

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

@enum.unique
class RuneType(enum.Enum):
    empty = f"-"
    attack = f"{Fore(160)}attack{Style.RESET_ALL}"
    shield = f"{Fore(23)}shield{Style.RESET_ALL}"
    heal = f"{Fore(40)}heal{Style.RESET_ALL}"
    crit = f"{Fore(220)}crit{Style.RESET_ALL}"
    burn = f"{Fore(202)}burn{Style.RESET_ALL}"
    leach = f"{Fore(63)}leach{Style.RESET_ALL}"
    poison = f"{Fore(92)}poison{Style.RESET_ALL}"
    golden = f"{Fore(220)}golden{Style.RESET_ALL}"

class BaseRune:
    def __init__(self, _type: RuneType, order, cost, rarity):
        self.name = _type.name
        self.symbol = _type.value
        self.order = order
        self.cost = cost
        self.rarity = rarity

class Empty(BaseRune):
    def __init__(self):
        super().__init__(RuneType.empty, -1, 0, 10)
        
    def apply(self, value, source):
        pass

class Attack(BaseRune):
    def __init__(self):
        super().__init__(RuneType.attack, 2, 10, 4)
        
    def apply(self, value, source):
        source.target.add_effect(effect.Damage(value))

class Shield(BaseRune):
    def __init__(self):
        super().__init__(RuneType.shield, 1, 10, 4)
        
    def apply(self, value, source):
        source.shield += value

class Heal(BaseRune):
    def __init__(self):
        super().__init__(RuneType.heal, 2, 15, 3)
        
    def apply(self, value, source):
        source.take_heal(value)

class Crit(BaseRune):
    def __init__(self):
        super().__init__(RuneType.crit, 0, 2, 2)
        
    def apply(self, value, source):
        for i in range(len(source.roll_results)):
            source.roll_results[i][0] *= 2

class Burn(BaseRune):
    def __init__(self):
        super().__init__(RuneType.burn, 2, 20, 2)
        
    def apply(self, value, source):
        source.target.add_effect(effect.Damage(value))
        source.target.add_effect(effect.Burn(value))

class Leach(BaseRune):
    def __init__(self):
        super().__init__(RuneType.leach, 2, 30, 1)
        
    def apply(self, value, source):
        source.target.add_effect(effect.Damage(value))
        source.take_heal(value//2)

class Poison(BaseRune):
    def __init__(self):
        super().__init__(RuneType.poison, 2, 20, 1)
        
    def apply(self, value, source):
        source.target.add_effect(effect.Poison(value))

class Golden(BaseRune):
    def __init__(self):
        super().__init__(RuneType.golden, 2, 20, 2)
        
    def apply(self, value, source):
        source.gold += value

@enum.unique
class Runes(enum.Enum):
    empty = Empty()
    attack = Attack()
    shield = Shield()
    heal = Heal()
    crit = Crit()
    burn = Burn()
    leach = Leach()
    poison = Poison()
    golden = Golden()