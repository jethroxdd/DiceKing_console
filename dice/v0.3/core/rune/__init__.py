from enum import IntEnum
from ui.color import Color
from ui.display import Paint
from core import Rarity

class RunePriority(IntEnum):
    UTILITY = 0
    SHIELD = 1
    EFFECT = 2
    SELF_DAMAGE = 3
    DAMAGE = 4

class BaseRune:
    name = "base_rune"
    priority = RunePriority.UTILITY
    cost = 0
    rarity = Rarity.COMMON
    color = Color.WHITE
    
    def apply(self, value: int, source, target, roll_results: list, index: int):
        raise NotImplementedError
        
    def __str__(self):
        return Paint(self.name, self.color)