from core.die import Die
from core import RarityType, PoolType

class Simple(Die):
    rarity = RarityType.COMMON
    _name = "simple"
    def __init__(self, sides, runes=None, upgrades=None):
        super().__init__(sides, runes, upgrades)


DICE_POOLS = {
    PoolType.SHOP: [Simple],
    PoolType.CHEST: [Simple]
}