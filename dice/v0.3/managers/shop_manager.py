from enum import Enum
from random import choice, choices, random
from utils import random_items_from_pool
from core import PoolType
from core.die.types import DICE_POOLS
from core.rune.types import RUNE_POOLS, Empty
from core.artifact.types import ARTIFACT_POOLS
from ui import display, input

class ItemType(Enum):
    DIE = "die"
    RUNE = "rune"
    ARTIFACT = "artifact"

class ShopItem:
    def __init__(self, item, item_type: ItemType):
        self.item = item
        self.cost = item.cost
        self.type = item_type
        self.purchased = False
    
    def __str__(self):
        return "---" if self.purchased else str(self.item)
    
    @property
    def is_purchased(self):
        return self.purchased

class ShopPool:
    @classmethod
    def get_die(cls):
        return random_items_from_pool(cls.dice)
    
    @classmethod
    def get_rune(cls):
        return random_items_from_pool(cls.runes)
    
    @classmethod
    def get_artifact(cls):
        return random_items_from_pool(cls.artifacts)
    
    dice = DICE_POOLS[PoolType.CHEST]
    runes = RUNE_POOLS[PoolType.CHEST]
    artifacts = ARTIFACT_POOLS[PoolType.CHEST]

class ShopManager:
    def __init__(self, player):
        self.player = player

    def enter(self):
        items = [
            ShopItem(self._create_die_item(), ItemType.DIE),
            *[ShopItem(self._create_rune_item(), ItemType.RUNE) for _ in range(2)],
            ShopItem(self._create_artifact_item(), ItemType.ARTIFACT)
        ]
        self._shop_loop(items)

    def _shop_loop(self, items):
        while True:
            display.message(f"Player Gold: {self.player.gold}")
            available_items = [item for item in items]
            
            options = [
                f"{item.cost}G{' '*(4 - len(str(item.cost)))} {item}"
                for item in available_items
            ]
            options.append("Sell Item")
            
            selection = input.select_from_list(
                options=options,
                title="Shop",
                input_text="Choose option ('Enter' to exit): ",
                framed=True,
                default=False
            )
            
            if selection is False:
                break
            
            if selection == len(options):
                self._handle_sell_menu()
            else:
                selected_item = available_items[selection - 1]
                self._process_purchase(selected_item)

    def _process_purchase(self, item):
        if item.is_purchased:
            display.error("Item already purchased!")
            return
        if self.player.gold < item.cost:
            display.error("Not enough gold!")
            return
        
        self.player.gold -= item.cost
        {
            ItemType.DIE: self.player.add_die,
            ItemType.RUNE: self.player.add_rune,
            ItemType.ARTIFACT: self.player.add_artifact
        }[item.type](item.item)
        
        item.purchased = True
        display.success("Purchase successful!")

    def _handle_sell_menu(self):
        options = ["Runes", "Dice"]
        selection = input.select_from_list(
            options=options,
            title="Sell Items",
            input_text="Choose category ('Enter' to exit): ",
            framed=True,
            default=False
        )
        
        if not selection:
            return
        
        item_type = ItemType.RUNE if selection == 1 else ItemType.DIE
        self._sell_item_type(item_type)

    def _sell_item_type(self, item_type):
        items, name = (self.player.runes, "Runes") if item_type == ItemType.RUNE else (self.player.dice, "Dice")
        
        if not items:
            display.error(f"No {name.lower()} to sell!")
            return
        
        options = [str(item) for item in items]
        selection = input.select_from_list(
            options=options,
            title=f"Sell {name}",
            input_text=f"Choose {name[:-1].lower()} ('Enter' to exit): ",
            default=False,
            framed=True,
            multiple=True
        )
        
        if selection:
            print(selection)
            for s in sorted(selection)[::-1]:
                self._finalize_sale(item_type, s - 1)

    def _finalize_sale(self, item_type, index):
        if item_type == ItemType.RUNE:
            rune = self.player.runes[index]
            self.player.gold += int(rune.cost * 0.9)
            self.player.remove_rune_at(index)
        else:
            die = self.player.dice[index]
            self.player.gold += int(die.cost * 0.9)
            for rune in die.runes:
                self.player.gold += int(rune.cost * 0.9)
            self.player.remove_die_at(index)
        display.success("Item sold!")

    def _create_die_item(self):
        die_cls = ShopPool.get_die()
        sides = choices([4, 6, 8, 10, 12], weights=[5, 4, 3, 2, 1], k=1)[0]
        runes = [self._create_rune_component() for _ in range(sides)]
        return die_cls(sides, runes)

    def _create_rune_component(self):
        return Empty() if random() > 0.5 else ShopPool.get_rune()()

    def _create_rune_item(self):
        return ShopPool.get_rune()()

    def _create_artifact_item(self):
        return ShopPool.get_artifact()(self.player)