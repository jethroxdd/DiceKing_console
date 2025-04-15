from core.entity import Entity
from core.die.types import Simple
from core.rune.types import Attack, Shield
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
                Simple(4, [Shield()]*3 + [Attack()]*1), 
                Simple(4, [Shield()]*3 + [Attack()]*1)
                ]
            )

class Slime(Enemy):
    def __init__(self, level=1):
        super().__init__(
            "Slime", 
            10 + 4*level, 
            [
                Simple(4, [Attack()]*3 + [Shield()]*1),
                Simple(4, [Attack()]*3 + [Shield()]*1)
                ]
            )

class Boss(Enemy):
    def __init__(self, level=1):
        super().__init__(
            "BOSS",
            20 + 10*level, 
            [
                Simple(4, [Shield()]*3 + [Attack()]*1), 
                Simple(4, [Shield()]*3 + [Attack()]*1)
                ]
            )

STAGE_1_POOL = [Rat, Slime]
STAGE_2_POOL = [Rat, Slime]
STAGE_3_POOL = [Rat, Slime]
STAGE_4_POOL = [Rat, Slime]
STAGE_5_POOL = [Rat, Slime]

ENEMY_POOL = [
    STAGE_1_POOL,
    STAGE_2_POOL,
    STAGE_3_POOL,
    STAGE_4_POOL,
    STAGE_5_POOL
]