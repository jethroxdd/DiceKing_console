from helpers import RollResult, RollResults
from itertools import zip_longest
from random import shuffle
from UI.color import Paint
import UI

'''
Battle starts
    Choose dice
    Raund starts
        Dice roll
        Rerolls
        Select rolls order
        Apply rolls
    Round ends
If someone dies battle ends
'''
class CombatManager:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        
        self.chosen_dice = []
        
        self.player.set_target(self.enemy)
        self.enemy.set_target(self.player)
    
    def battle(self):
        self.select_player_dice()
        while not self.player.is_dead and not self.enemy.is_dead:
            self.round()
    
    def round(self):
        UI.print_stats(self.player, self.enemy)
        
        # Roll dice
        roll_results = self.roll_dice()
        
        # Rerolls
        pass 
    
        # Select order
        self.select_order(roll_results)
        shuffle(roll_results.enemy)
        
        UI.print_roll_results(roll_results, "player")
        UI.print_roll_results(roll_results, "enemy")
        
        # Apply rolls
        roll_results.apply()
        
        # Apply effects
        self.player.apply_effects()
        self.enemy.apply_effects()
        
        # Tick
        self.player.tick()
        self.enemy.tick()
        
        input(Paint("End of the round. Press Enter...", 220))

    def select_player_dice(self):
        # Select dice to roll from player's inventory
        selected_dice = []
        UI.print_availible_dice(self.player)
        while True:
            input_line = input(Paint("Select up to 5 dice (separate with spaces): ", 220))
            try:
                selected_dice = list(map(int, input_line.split()))
                if 0 < len(selected_dice) <= self.player.max_active_dice_amount:
                    for i in  selected_dice:
                        self.chosen_dice.append(self.player.dice[i-1])
                    return
                else:
                    raise Exception()
            except:
                print(Paint("Incorrect input!", 88))
    
    def roll_dice(self):
        roll_results = RollResults()
        # Roll player's dice
        for die in self.chosen_dice:
            rune, value = die.roll()
            roll_results.player.append(RollResult(rune, value, self.player, self.player.target))
        
        # Roll enemy's dice
        for die in self.enemy.dice:
            rune, value = die.roll()
            roll_results.enemy.append(RollResult(rune, value, self.enemy, self.enemy.target))
        
        return roll_results
    
    def select_order(self, roll_results):
        UI.print_roll_results(roll_results, "player")
        while True:
            temp = list(range(1, len(self.chosen_dice) + 1))
            input_line = input(Paint("Select order(separate with spaces): ", 220))
            try:
                selected_order = temp if input_line == "" else list(map(int, input_line.split()))
                if len(set(selected_order)) == len(self.chosen_dice):
                    for i in selected_order:
                        if not i in temp:
                            raise Exception()
                    else:
                        temp_arr = []
                        for i in selected_order:
                            temp_arr.append(roll_results.player[i-1])
                        roll_results.player = temp_arr
                        return
                else:
                    raise Exception()
            except:
                print(Paint("Incorrect input!", 88))
        