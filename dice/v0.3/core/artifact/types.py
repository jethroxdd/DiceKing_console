from core.artifact import BaseArtifact
from core import Rarity

class MagicSphere(BaseArtifact):
    rarity = Rarity.rare
    cost = 30
    def __init__(self, player):
        super().__init__(player=player, name="Magic Sphere", description="Adds 1 reroll")
    
    def apply(self):
        self.player.max_rerolls += 1
    
    def add(self):
        self.apply()

class FragShield(BaseArtifact):
    rarity = Rarity.rare
    cost = 40
    def __init__(self, player):
        super().__init__(player=player, name="Fragmentation Shield", description="Deal 3 damage when 5 shield broke")
        self.damage = 3
        self.broken_shield_count = 0
    
    def apply(self):
        self.player._on_shield_broke.add(self.func)
    
    def add(self):
        self.damage += 1

    def func(self, *args, **kwargs):
        value = args[0]
        self.broken_shield_count += value
        while self.broken_shield_count//5 > 0:
            self.player.target.take_damage(self.damage)
            self.broken_shield_count -= 5

SHOP_POOL_ARTIFACTS = [MagicSphere, FragShield]
CHEST_POOL_ARTIFACTS = SHOP_POOL_ARTIFACTS