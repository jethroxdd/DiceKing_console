from core.artifact import BaseArtifact
from core import RarityType, PoolType

class MagicSphere(BaseArtifact):
    rarity = RarityType.RARE
    cost = 30
    name = "Magic Sphere"
    description = "Adds 1 reroll"
    
    def apply(self):
        self.player.max_rerolls += 1
    
    def stack(self):
        self.apply()

class FragShield(BaseArtifact):
    rarity = RarityType.RARE
    cost = 40
    name = "Fragmentation Shield"
    description = "Deal 3 damage when 5 shield broke"
    damage = 3
    broken_shield_count = 0
    
    def apply(self):
        self.player.on_shield_broke.connect(self.func)
    
    def stack(self):
        self.damage += 1

    def func(self, *args, **kwargs):
        value = args[0]
        self.broken_shield_count += value
        while self.broken_shield_count//5 > 0:
            self.player.target.take_damage(self.damage)
            self.broken_shield_count -= 5

class BloodTome(BaseArtifact):
    rarity = RarityType.RARE 
    cost = 40
    name = "Blood Tome"
    description = "Self damage deal the same amount of damage to the enemy."
    
    def apply(self):
        self.player.on_self_damage.connect(self.func)

    def func(self, *args, **kwargs):
        damage = args[0]
        self.player.target.take_damage(damage)


ARTIFACT_POOLS = {
    PoolType.SHOP: [MagicSphere, FragShield],
    PoolType.CHEST: [MagicSphere, FragShield]
}