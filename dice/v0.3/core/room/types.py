from random import randint, choice
from core import PoolType, ItemType
from core.room import Room
from core.entity import Enemy
from core.entity.enemy import ENEMY_POOL, Boss
from core.die.types import DICE_POOLS, Simple
from core.rune.types import RUNE_POOLS
from core.artifact.types import ARTIFACT_POOLS
from utils import random_items_from_pool
from ui import display, input
import managers
import core.rune.types as RuneTypes

class CombatRoom(Room):
    """Base class for rooms containing combat encounters."""
    def __init__(self, name: str, description: str, player, difficulty: int, enemy: Enemy):
        super().__init__(name, description, player, difficulty)
        self.enemy = enemy

    def _handle_victory(self, reward: int) -> None:
        """Handle player victory sequence."""
        if not self.player.is_alive:
            display.error("You died!")
            return

        display.success("You won!")
        self.player.gold += reward
        display.warning(f"\nYou gained {reward} gold")

class EventRoom(Room):
    """Base class for event-type rooms with common display patterns."""
    def __init__(self, name: str, description: str, player, difficulty: int):
        super().__init__(name, description, player, difficulty)
    
    def enter(self, custom_title: str = None) -> None:
        """Standard enter method for event rooms with optional custom title."""
        display.H2(custom_title or "Event Room")

class LootRoom(Room):
    """Base class for rooms containing loot interactions."""
    def __init__(self, name: str, description: str, player, difficulty: int):
        super().__init__(name, description, player, difficulty)
        self._item_handlers = {
            ItemType.ARTIFACT: self._handle_artifact,
            ItemType.RUNE: self._handle_rune,
            ItemType.DIE: self._handle_die
        }

    def _get_item_pool(self, item_type: ItemType):
        """Retrieve appropriate item pool for loot type."""
        pools = {
            ItemType.ARTIFACT: ARTIFACT_POOLS[PoolType.CHEST],
            ItemType.RUNE: RUNE_POOLS[PoolType.CHEST],
            ItemType.DIE: DICE_POOLS[PoolType.CHEST]
        }
        return pools[item_type]

    def _handle_artifact(self, item):
        self.player.add_artifact(item)

    def _handle_rune(self, item):
        self.player.add_rune(item)

    def _handle_die(self, item):
        self.player.add_die(item)

class Battle(CombatRoom):
    def __init__(self, player, difficulty: int, enemy=None):
        enemy = enemy or self._create_enemy(difficulty)
        super().__init__("Battle", "Fight the enemy", player, difficulty, enemy)

    def enter(self, title: str = "Battle Encounter") -> None:
        display.H2(title)
        cm = managers.CombatManager(self.player, self.enemy)
        cm.battle()
        self._handle_victory(reward=int(randint(10, 20)*(self.difficulty**0.7) + 10))
    
    def _create_enemy(self, difficulty):
        return random_items_from_pool(ENEMY_POOL[PoolType.ALL])(difficulty)

class Shop(EventRoom):
    def __init__(self, player, difficulty: int):
        super().__init__("Shop", "Buy upgrades", player, difficulty)

    def enter(self) -> None:
        super().enter("Shop")
        managers.ShopManager(self.player).enter()

class ModificationRoom(Room):
    def __init__(self, player, difficulty: int):
        super().__init__("Mod Room", "Modify your dice", player, difficulty)
        self.mod_manager = managers.ModificationManager(player)

    def enter(self) -> None:
        super().enter()
        while (die_index := self._select_die()):
            die = self.player.dice[die_index-1]
            self.mod_manager.start_session(die)

    def _select_die(self):
        display.available_runes(self.player, framed=True)
        display.available_dice(self.player, framed=True)
        
        return input.get_valid_input(
            input_text="Choose dice ('Enter' to exit): ",
            validation=lambda x: 1 <= x <= len(self.player.dice) ,
            transform=int,
            default=False
        )
         

class HealingSprings(EventRoom):
    def __init__(self, player, difficulty: int):
        super().__init__("Healing Springs", "Restore full health", player, difficulty)

    def enter(self) -> None:
        super().enter()
        display.success("Your health has been fully restored.")
        self.player.health = self.player.max_health

class Trap(EventRoom):
    def __init__(self, player, difficulty: int):
        super().__init__("Trap", "Recive some damage.", player, difficulty)

    def enter(self) -> None:
        super().enter()
        damage = randint(1, 10)**self.difficulty
        display.error(f"You fell in the trap and recived {damage} damage.")
        self.player.take_true_damage(damage)

class GoldMinecart(EventRoom):
    def __init__(self, player, difficulty: int):
        super().__init__("Minecart with gold", "Abandoned gold", player, difficulty)

    def enter(self) -> None:
        super().enter()
        gold = randint(1, 10)**self.difficulty
        display.success(f"You found {gold} gold in minecart.")
        self.player.gold += gold

class Chest(LootRoom):
    def __init__(self, player, difficulty: int):
        super().__init__("Chest", "Receive random item", player, difficulty)

    def enter(self) -> None:
        display.H2("Chest Room")
        if self._handle_loot():
            display.message("You acquired a new item!")

    def _handle_loot(self) -> bool:
        """Handle full loot acquisition flow."""
        item_type = choice(list(ItemType))
        item = self._create_item(item_type)
        
        if not self._confirm_acquisition(item):
            return False

        self._add_item(item_type, item)
        return True

    def _create_item(self, item_type: ItemType):
        pool = self._get_item_pool(item_type)
        if item_type == ItemType.DIE:
            return random_items_from_pool(pool)(sides=choice([4, 6, 8, 10]))
        return random_items_from_pool(pool)(self.player if item_type == ItemType.ARTIFACT else None)

    def _confirm_acquisition(self, item) -> bool:
        display.message(f"You found {item}")
        return input.get_valid_input(
            input_text="Take it? (y/n): ",
            validation=lambda x: x.lower() == 'y',
            default=False
        )

    def _add_item(self, item_type: ItemType, item) -> None:
        self._item_handlers[item_type](item)

class BossBattle(Battle):
    def __init__(self, player, difficulty: int):
        enemy = Boss(level=difficulty)
        super().__init__(player, difficulty, enemy)

    def enter(self) -> None:
        super().enter("Boss Battle")

    @staticmethod
    def _create_boss_enemy(difficulty: int) -> Enemy:
        return Enemy(
            name="Boss",
            health=30 + 10 * difficulty,
            dice=[
                Simple(4, [RuneTypes.Crit()] + [RuneTypes.Shield()]*3),
                Simple(4, [RuneTypes.Crit()] + [RuneTypes.Attack()]*3),
                Simple(6, [RuneTypes.Shield()]*3 + [RuneTypes.Attack()]*3)
            ]
        )

# Room pool configuration
ROOM_POOLS = {
    PoolType.STANDARD: [Shop, ModificationRoom],
    PoolType.BATTLE: [Battle],
    PoolType.EVENT: [HealingSprings, Trap, GoldMinecart],
    PoolType.CHEST: [Chest],
    PoolType.BOSS: [Boss]
}