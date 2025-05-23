from core.rune import types as RuneTypes
from core.entity import Entity
from utils import Signal
        
class Player(Entity):
    def __init__(self, health, dice):
        super().__init__("Player", health, dice)
        self.artifacts = []
        self.runes = []
        self.max_active_dice_amount = 5
        self.max_rerolls = 1
        self.used_rerolls = 0
        self.init_signals()
    
    def init_signals(self):
        self._on_shield_broke = Signal(self)
        self._on_self_damage = Signal(self)
    
    @property
    def is_alive(self):
        return self.health > 0
    
    @property
    def rerolls(self):
        return self.max_rerolls - self.used_rerolls
    
    def take_damage(self, damage):
        shield_broke = self.shield - max(0, self.shield-damage)
        if shield_broke:
            self._on_shield_broke.emit(shield_broke)
        
        super().take_damage(damage)
    
    def take_self_damage(self, damage):
        self._on_self_damage.emit(damage)
        super().take_self_damage(damage)
    
    def add_artifact(self, artifact):
        for a in self.artifacts:
            if a.name == artifact.name:
                a.add()
                return
        self.artifacts.append(artifact)
        artifact.apply()
    
    def add_rune(self, rune):
        self.runes.append(rune)
    
    def add_die(self, die):
        self.dice.append(die)
    
    def remove_rune(self, rune_id):
        del self.runes[rune_id]
    
    def end_round_cleanup(self):
        super().end_round_cleanup()
        self.used_rerols = 0
    
    def remove_rune_by_id(self, id):
        del self.runes[id]
    
    def remove_rune_by_value(self, value):
        id = self.runes.index(value)
        del self.runes[id]
    
    def heal(self, value):
        self.health = min(self.max_health, self.health+value)