from core.entity import Entity
from core.die.types import SimpleDie
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
    def __init__(self, level):
        super().__init__("Rat", 10 + 4*level, [SimpleDie(4, [Shield()]*3 + [Attack()]*1)])

class Slime(Enemy):
    def __init__(self, level):
        super().__init__("Slime", 10 + 4*level, [SimpleDie(4, [Attack()]*2 + [Shield()]*1)])