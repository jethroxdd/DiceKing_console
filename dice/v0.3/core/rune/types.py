from core.rune import RunePriority, BaseRune
import core.effect.types as EffectTypes
from ui.color import Paint, Color
from core import RarityType, PoolType

class Empty(BaseRune):
    name = "-"
    priority = RunePriority.UTILITY
    cost = 0
    rarity = 0
    color = Color.EMPTY
    
    def apply(self, *args):
        pass

class Attack(BaseRune):
    name = "attack"
    priority = RunePriority.DAMAGE
    cost = 10
    rarity = RarityType.COMMON
    color = Color.ATTACK

    def apply(self, value, source, target, roll_results, index):
        target.take_damage(value)

class Shield(BaseRune):
    name = "shield"
    priority = RunePriority.SHIELD
    cost = 10
    rarity = RarityType.COMMON
    color = Color.SHIELD

    def apply(self, value, source, target, roll_results, index):
        source.add_shield(value)

class Fire(BaseRune):
    name = "fire"
    priority = RunePriority.DAMAGE
    cost = 40
    rarity = RarityType.EPIC
    color = Color.FIRE
    
    def apply(self, value, source, target, roll_results, index):
        target.take_damage(value//2)
        target.add_effect(EffectTypes.Burn(value))

class Crit(BaseRune):
    name = "crit"
    priority = RunePriority.UTILITY
    cost = 50
    rarity = RarityType.LEGENDARY
    color = Color.CRIT
    
    def apply(self, value, source, target, roll_results, index):
        for result in roll_results[index:]:
            result.value.add_mult(2)

class Heal(BaseRune):
    name = "heal"
    priority = RunePriority.EFFECT
    cost = 50
    rarity = RarityType.EPIC
    color = Color.HEAL
    
    def apply(self, value, source, target, roll_results, index):
        source.take_heal(value)

class Rage(BaseRune):
    name = "rage"
    priority = RunePriority.UTILITY
    cost = 40
    rarity = RarityType.EPIC
    color = Color.RAGE
    power = 2
    
    def apply(self, value, source, target, roll_results, index):
        roll_results[index].value.add_base(self.power)
        target.take_damage(value+self.power)
        source.take_self_damage(self.power)

class Mirror(BaseRune):
    name = "mirror"
    priority = RunePriority.UTILITY
    cost = 40
    rarity = RarityType.LEGENDARY
    color = Color.MIRROR
    
    def apply(self, value, source, target, roll_results, index):
        if index == 0:
            return
        roll_results[index].rune = roll_results[index-1].rune
        roll_results[index].apply(roll_results, index)
    
# Rune pool configuration
RUNE_POOLS = {
    PoolType.ALL: [Attack, Shield, Crit, Fire, Heal, Mirror, Rage],
    PoolType.CHEST: [Attack, Shield, Crit, Fire, Heal, Mirror, Rage],
    PoolType.SHOP: [Attack, Shield, Heal, Rage]
}