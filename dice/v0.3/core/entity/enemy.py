from core import PoolType
from core.entity import Entity
from core.die.types import Simple
import core.rune.types as RuneTypes
from random import shuffle
class Enemy(Entity):
    def __init__(self, name="Enemy", health=None, dice=None):
        super().__init__(name, health, dice)
        self.gold = 10
    
    def ai_select_dice(self):
        # Basic implementation - choose random dice
        shuffle(self.dice)
        return self.dice

    def ai_choose_order(self, results):
        # Basic implementation - random order
        shuffle(results)
        return results

class Rat(Enemy):
    def __init__(self, level=1):
        super().__init__(
            "Rat",
            10 + 4*level, 
            [
                Simple(4, [RuneTypes.Shield()]*2 + [RuneTypes.Attack()]*1 + [RuneTypes.Empty()]), 
                Simple(4, [RuneTypes.Shield()]*2 + [RuneTypes.Attack()]*1 + [RuneTypes.Empty()])
                ]
            )

class Slime(Enemy):
    def __init__(self, level=1):
        super().__init__(
            "Slime", 
            10 + 4*level, 
            [
                Simple(4, [RuneTypes.Attack()]*2 + [RuneTypes.Shield()]*1 + [RuneTypes.Empty()]),
                Simple(4, [RuneTypes.Attack()]*2 + [RuneTypes.Shield()]*1 + [RuneTypes.Empty()])
                ]
            )

class Boss(Enemy):
    def __init__(self, level=1):
        super().__init__(
            "BOSS",
            20 + 10*level, 
            [
                Simple(6, [RuneTypes.Crit()]*1 + [RuneTypes.Shield()]*1 + [RuneTypes.Shield()]*2 + [RuneTypes.Empty()]*1), 
                Simple(6, [RuneTypes.Crit()]*1 + [RuneTypes.Attack()]*1 + [RuneTypes.Attack()]*2 + [RuneTypes.Empty()]*1)
                ]
            )

STAGE_1_POOL = [Rat, Slime]
STAGE_2_POOL = [Rat, Slime]
STAGE_3_POOL = [Rat, Slime]
STAGE_4_POOL = [Rat, Slime]
STAGE_5_POOL = [Rat, Slime]

ENEMY_POOL = {
    PoolType.ALL: [Rat, Slime],
    0: [Rat, Slime],
    2: [Rat, Slime],
    3: [Rat, Slime],
    4: [Rat, Slime],
    5: [Rat, Slime]
}