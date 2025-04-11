from core.room import Room
from managers import CombatManager
from core.rune.types import Attack, Shield
from core.die.types import SimpleDie
from ui.color import Paint, Color
from random import randint
import core.entity.enemy as EnemyTypes

# Room pools:
# 1. Standart - shows name of the room
# 2. Event - random room from this pool. Doesn't sho name of room? onlr "Event room"
# 3. Chest - rooms with some revard. Shows as "Chest room"

# Shop room (standart)
# Heal room (event) - regen 10 HP
# Chest room (chest) - add random rune, empty die, artifact or die with random runes
# Elit Battle (standart)(event) - battle with stronger enemy for artifact
# Gold room (event) - gain some gold
# Trap room (event) - Recive some damage
# Stranger (event) - Recive buff for next battle
# Casino (event) - gamble gold
# Encient forge (event) - upgrade die with small chance to brake die
# Altar (event) - buy artifacts for blood (recive damage)
# Mimic (chest) - small chance to appear instead of chest. Battle with strong mimic for chest loot.
# Russian roulette (event) - option to play russian roulette (1/6 chance to win): win - recive legendary item, lose - death (end of run).
# Cursed chest (chest) - better rarity items, but -5 max HP
# Museum (event) - option to steal the die (1/6), failure - battle with guard.
# The Fortune Teller (event) - pay to choose next room (5 options).
# Hospital - pay for heal or encrease max HP.
# Sacrifice altar - sacrifice die to encrease max HP (more sides, more max HP)

class Battle(Room):
    def __init__(self,player, difficulty):
        super().__init__("Battle encounter", "The battle starts", player, difficulty)
    
    def enter(self):
        enemy = EnemyTypes.Rat(1)
        cm = CombatManager(self.player, enemy)
        cm.battle()
        if self.player.is_dead:
            print(Paint("You died!", Color.RED))
            return
        reward = int(randint(10, 20)*(self.difficulty**(0.7)))
        print(Paint("You won!", Color.GREEN))
        self.player.gold += reward
        print(Paint(f"\nYou gained {reward} gold", Color.YELLOW))
