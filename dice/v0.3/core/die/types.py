from core.die import Die
from core import Rarity

class Simple(Die):
    rarity = Rarity.ordinary
    def __init__(self, sides, runes=None, upgrades=None):
        super().__init__("simple", sides, runes, upgrades)

SHOP_POOL_DICE = [Simple]
CHEST_POOL_DICE = SHOP_POOL_DICE