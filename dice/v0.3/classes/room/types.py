from classes.room import Room
from managers import CombatManager
from classes.entity import Enemy
from classes.rune.types import Attack, Shield
from classes.die.types import SimpleDie
from UI import Paint, Color
from random import randint

class Battle(Room):
    def __init__(self,player, difficulty):
        super().__init__("Battle encounter", "The battle starts", player, difficulty)
    
    def enter(self):
        enemy = Enemy(10 + 5*self.difficulty, [SimpleDie(4, [Shield()]*2 + [Attack()]*2)])
        cm = CombatManager(self.player, enemy)
        cm.battle()
        if self.player.is_dead:
            print(Paint("You died!", Color.RED))
            return
        reward = int(randint(10, 20)*(self.difficulty**(0.7)))
        print(Paint("You won!", Color.GREEN))
        self.player.gold += reward
        print(Paint(f"\nYou gained {reward} gold", Color.YELLOW))
        