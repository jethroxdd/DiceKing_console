from classes.rune import types as RuneTypes
from classes.entity import Entity
        
class Player(Entity):
    def __init__(self, health, dice):
        super().__init__("Player", health, dice)
        self.runes = []
        self.max_active_dice_amount = 5