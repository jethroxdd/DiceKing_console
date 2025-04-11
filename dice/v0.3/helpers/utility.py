from itertools import zip_longest
from core.entity import Player, Enemy
from ui.color import Paint, Color

class RollResult:
    def __init__(self, rune, _value, source, target):
        self.rune = rune
        self._value = _value
        self.source = source
        self.target = target
        self.value_mult_mods = []
        self.value_flat_mods = []
    
    @property
    def value(self):
        value = self._value
        for mod in self.value_mult_mods:
            value *= mod
        for mod in self.value_flat_mods:
            value += mod
        return int(value)
    
    def apply(self, roll_results):
        self.rune.apply(self.value, self.source, self.target, roll_results)
    
    def __str__(self):
        value = self.value
        if self.rune.name in ["crit", "empty"]:
            value = "-"
        return f"{value} {self.rune}"

class RollResults:
    def __init__(self):
        self.player = []
        self.enemy = []
    
    def apply(self):
        for player_result, enemy_result in zip_longest(self.player, self.enemy):
            if player_result and enemy_result:
                if player_result.rune.order < enemy_result.rune.order:
                    player_result.apply(self.player)
                    enemy_result.apply(self.enemy)
                else:
                    enemy_result.apply(self.enemy)
                    player_result.apply(self.player)
            elif player_result:
                player_result.apply(self.player)
            elif enemy_result:
                enemy_result.apply(self.enemy)

class EntityRoundStatistics:
    def __init__(self):
        self.dealt_damage = 0
        self.recived_damage = 0
        self.taken_damage = 0
        self.blocked_damage = 0

class RoundStatistics:
    def __init__(self):
        pass
