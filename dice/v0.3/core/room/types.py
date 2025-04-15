from core.room import Room
from core.entity import Enemy
from core.die.types import CHEST_POOL_DICE, Simple
from core.rune.types import CHEST_POOL_RUNES, Attack, Shield, Crit
from core.artifact.types import CHEST_POOL_ARTIFACTS
from utils import random_items_from_pool
import managers
from ui import display
from ui import input
from random import randint, choice

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
    
    def enter(self, title="Battle encounter"):
        display.H2(title)
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
        display.H2("Shop")
        shop_manager = managers.ShopManager(self.player)
        shop_manager.enter()

class ModificationRoom(Room):
    def __init__(self, player, difficulty, *args, **kwargs):
        super().__init__("Modification room", "Modificate your stuff", player, difficulty)
        self.mod_manager = managers.ModificationManager(self.player)
    
    def enter(self):
        display.H2("Modification room")
        while True:
            die = self._select_die()
            if not die:
                return
            self.mod_manager.start_session(die)
        
    def _select_die(self):
        # Displayer availible dice
        display.available_runes(self.player, framed=True)
        display.available_dice(self.player, framed=True)
        selection = input.get_valid_input(
            input_text="Choose dice ('Enter' to exit): ",
            validation=lambda x: 1<=x<=len(self.player.dice) if self.player.dice else False,
            transform=lambda x: int(x),
            default=False
        )
        if selection == False:
            return None
        die = self.player.dice[selection-1]
        return die

class HealingSprings(Room):
    def __init__(self, player, difficulty, *args, **kwargs):
        super().__init__("Healing Springs", "Restore full health", player, difficulty)
    
    
    def enter(self):
        display.H2("Chest")
        display.success("Your health is full.")
        self.player.health = self.player.max_health

class Chest(Room):
    
    def __init__(self, player, difficulty, *args, **kwargs):
        super().__init__("Chest", "Recive random item", player, difficulty)
    
    
    def enter(self):
        display.H2("Chest")
        item = None
        item_type = choice(["artifact", "rune", "die"])
        match item_type:
            case "artifact":
                item = random_items_from_pool(CHEST_POOL_ARTIFACTS)(self.player)
            case "rune":
                item = random_items_from_pool(CHEST_POOL_RUNES)()
            case "die":
                item = random_items_from_pool(CHEST_POOL_DICE)(sides=choice([4, 6, 8, 10]))
        
        display.message(f"You recived {item}")
        option = input.get_valid_input(
            input_text="Take it (y/n): ",
            validation=lambda x: x in ['y', 'n'],
            default='n'
        )
        if option == 'n':
            return

        match item_type:
            case "artifact":
                self.player.add_artifact(item)
            case "rune":
                self.player.add_rune(item)
            case "die":
                self.player.add_die(item)
        

class Boss(Battle):
    def __init__(self, player, difficulty):
        dice = [
            Simple(4, [Crit()]+[Shield()]*3),
            Simple(4, [Crit()]+[Attack()]*3),
            Simple(6, [Shield()]*3+[Attack()]*3)
        ]
        enemy = Enemy(name="Boss", health=30+10*difficulty, dice=dice)
        super().__init__(player, difficulty, enemy=enemy)
    
    def enter(self):
        super().enter(title="Boss Battle")
        

STANDARD_POOL = [Battle, Shop, ]
EVENT_POOL = [HealingSprings]
CHEST_POOL = [Chest]