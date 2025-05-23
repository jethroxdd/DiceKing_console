from utils import random_items_from_pool
from core.die.types import SHOP_POOL_DICE
from core.rune.types import SHOP_POOL_RUNES, Empty
from core.artifact.types import SHOP_POOL_ARTIFACTS
from ui import display
from ui import input
from random import choice, choices, random

class ShopItem:
    def __init__(self, item, type_):
        self.item = item
        self.cost = item.cost
        self.type_ = type_
        self.purchased = False
    
    def __str__(self):
        if self.purchased:
            return "---"
        return str(self.item)

class ShopPool:
    dice = SHOP_POOL_DICE
    runes = SHOP_POOL_RUNES
    artifacts = SHOP_POOL_ARTIFACTS
    

class ShopManager:
    # Shop items:
    # 1. Die with random sides(4, 6, 8, 10, 12) and random runes (some of them empty)
    # 2. Random rune
    # 3. Random rune
    # 4. Random artifact
    # Each item can be bought once
    def __init__(self, player):
        self.player = player

    def enter(self):
        
        # Create shop items
        items = []
        die_item = [ShopItem(self._create_die_item(), "die")]
        rune_items = [ShopItem(self._create_rune_item(), "rune") for _ in range(2)]
        artifact_item = []
        items = die_item + rune_items + artifact_item
        
        self._shop_loop(items)
        
    
    def _shop_loop(self, items):
        while True:
            # Display player gold
            display.message(f"player gold: {self.player.gold}")
            
            # Combine display info
            options = []
            for k in items:
                options += [f"{k.cost}G{" "*(4-len(str(k.cost)))} {k}"]
            else:
                options += ["Sell item"]
                
            # Player select item
            selection = input.select_from_list(options=options, title="Shop", input_text="Choose option ('Enter' to exit): ", framed=True, default=False)
            
            if selection == False:
                break
            # Handle player selection
            if selection == len(options):
                self._sell_flow()
            else:
                item = items[selection-1]
                self._buy_item(item)
    
    def _buy_item(self, item):
        if self.player.gold < item.cost:
            display.error("Not enough gold!")
            return 0
        self.player.gold -= item.cost
        match item.type_:
            case "die":
                self.player.add_die(item.item)
            case "rune":
                self.player.add_rune(item.item)
            case "artifact":
                self.player.add_artifact(item.item)
        item.purchased = True
        display.success("Successfully purchased an item")
        
    def _sell_flow(self):
        # Display shop items
        options = ["Runes", "Dice"]
        selection = input.select_from_list(options=options, title="Selling menu", input_text="Choose item type ('Enter' to exit): ", framed=True, default=False)
        if selection == False:
            return
        item_type = ["rune", "die"][selection-1]
        item_id = self._choose_item(item_type)
        if item_id == False:
            return
        self._sell_item(item_type, item_id-1)

    def _choose_item(self, item_type):
        item_id = 0
        match item_type:
            case 'rune':
                options = [str(r) for r in self.player.runes]
                item_id = input.select_from_list(options=options, title="Selling menu", input_text="Choose rune ('Enter' to exit): ", framed=True, default=False)
            case 'die':
                options = [str(d) for d in self.player.dice]
                item_id = input.select_from_list(options=options, title="Selling menu", input_text="Choose die ('Enter' to exit): ", framed=True, default=False)
        return item_id
        
    def _sell_item(self, item_type, item_id):
        if item_type == "rune":
            self.player.gold += int(0.9*self.player.runes[item_id].cost)
            del self.player.runes[item_id]
            return
        for i, _ in enumerate(self.player.dice[item_id].runes):
            self.player.gold += int(0.9*self.player.dice[item_id].runes[i].cost)
        self.player.gold += int(0.9*self.player.dice[item_id].cost)
        del self.player.dice[item_id]
            
    
    def _create_die_item(self):
        die_type = random_items_from_pool(ShopPool.dice)
        die_sides = choices([4, 6, 8, 10, 12], weights=[5, 4, 3, 2, 1], k=1)[0]
        runes = []
        for _ in range(die_sides):
            if random() <= 0.5:
                runes.append(Empty())
            else:
                rune = random_items_from_pool(ShopPool.runes)()
                runes.append(rune)
        die = die_type(die_sides, runes)
        return die
    
    def _create_rune_item(self):
        return random_items_from_pool(ShopPool.runes)()
    
    def _create_artifact_item(self):
        return random_items_from_pool(ShopPool.artifacts)()