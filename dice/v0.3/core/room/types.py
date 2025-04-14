from core.room import Room
import managers
from ui import display
from random import randint

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
    def __init__(self, player, difficulty, *args, **kwargs):
        super().__init__("Battle encounter", "The battle starts", player, difficulty)
        self.enemy = kwargs["enemy"]
    
    def enter(self):
        enemy = self.enemy
        cm = managers.CombatManager(self.player, enemy)
        cm.battle()
        if self.player.is_dead:
            display.error("You died!")
            return
        reward = int(randint(10, 20)*(self.difficulty**(0.7))) + 10
        display.success("You won!")
        self.player.gold += reward
        display.warning(f"\nYou gained {reward} gold")

class Shop(Room):
    def __init__(self, player, difficulty, *args, **kwargs):
        super().__init__("Shop", "Buy upgrades", player, difficulty)
    
    def enter(self):
        shop_manager = managers.ShopManager(self.player)
        shop_manager.enter()
