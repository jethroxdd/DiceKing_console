from itertools import zip_longest
from classes.entity import Player, Enemy

class RollResult:
    def __init__(self, rune, value, source, target):
        self.rune = rune
        self.value = value
        self.source = source
        self.target = target
    
    def apply(self, roll_results):
        self.rune.apply(self.value, self.source, self.target, roll_results)
    
    def __str__(self):
        return f"{self.value} {self.rune}"

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