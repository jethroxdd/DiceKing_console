from core.rune import types as RuneTypes
from core.entity import Entity
        
class Player(Entity):
    def __init__(self, health, dice):
        super().__init__("Player", health, dice)
        self.runes = []
        self.max_active_dice_amount = 5
        self.max_rerols = 1
        self.used_rerols = 0
    
    @property
    def is_alive(self):
        return self.health > 0
    
    def add_rune(self, rune):
        self.runes.append(rune)
    
    def remove_rune(self, rune_id):
        del self.runes[rune_id]
    
    def get_available_rerolls(self):
        return self.max_rerols - self.used_rerols
    
    def end_round_cleanup(self):
        super().end_round_cleanup()
        self.used_rerols = 0