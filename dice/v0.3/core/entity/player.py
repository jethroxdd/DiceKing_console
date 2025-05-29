from core.rune import types as RuneTypes
from core.entity import Entity
from utils import Signal

class Player(Entity):
    def __init__(self, health, dice):
        super().__init__("Player", health, dice)
        self.artifacts = []
        self._artifacts_lookup = {}
        self.runes = []
        self.max_active_dice_amount = 5
        self._max_rerolls = 1
        self.used_rerolls = 0
        self._init_signals()

    def _init_signals(self):
        """Initialize event signals with more descriptive names"""
        self.on_shield_broke = Signal()
        self.on_self_damage = Signal()

    @property
    def max_rerolls(self):
        return self._max_rerolls
    
    @max_rerolls.setter
    def max_rerolls(self, max_rerolls):
        if max_rerolls <= 0:
            raise ValueError("max_rerolls must by positive")
        self._max_rerolls = max_rerolls
    
    @property
    def remaining_rerolls(self):
        """Clearer name for remaining resource"""
        return self._max_rerolls - self.used_rerolls
    
    @remaining_rerolls.setter
    def remaining_rerolls(self, remaining_rerolls):
        """Clearer name for remaining resource"""
        if remaining_rerolls > self._max_rerolls:
            raise ValueError(f"Remaining rerolls can't be more than max rerolls: remaining_rerols={remaining_rerolls}, max_rerolls={self._max_rerolls}")
        self.used_rerolls = self._max_rerolls - remaining_rerolls

    def take_damage(self, damage):
        """Centralized damage handling with event signaling"""
        shield_broken = self.shield - max(0, self.shield - damage)
        if shield_broken:
            self.on_shield_broke.emit(shield_broken)
        
        super().take_damage(damage)

    def take_self_damage(self, damage):
        """Explicit self-damage handling with event"""
        self.on_self_damage.emit(self_damage=damage)
        super().take_self_damage(damage)

    def add_artifact(self, artifact):
        """Optimized artifact management with O(1) lookups"""
        existing = self._artifacts_lookup.get(artifact.name)
        if existing:
            existing.stack()
            return

        self.artifacts.append(artifact)
        self._artifacts_lookup[artifact.name] = artifact
        artifact.apply()

    def add_rune(self, rune):
        """Type hinting would be beneficial here in real implementation"""
        self.runes.append(rune)

    def remove_rune_at(self, index):
        """Clearer method name for index-based removal"""
        del self.runes[index]

    def remove_rune(self, rune):
        """More intuitive value-based removal method"""
        self.runes.remove(rune)
    
    def add_die(self, die):
        """Consistent method naming convention"""
        self.dice.append(die)
    
    def remove_die_at(self, index):
        """Index-based removal"""
        del self.dice[index]
    
    def remove_die(self, die):
        """Index-based removal"""
        self.dice.remove(die)

    def end_round_cleanup(self):
        """Fixed typo and explicit cleanup sequence"""
        super().end_round_cleanup()
        self.used_rerolls = 0

    def heal(self, value):
        """Clamped healing implementation"""
        self.health = min(self.max_health, self.health + value)
    