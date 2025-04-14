import core.rune.types as RuneTypes
import core.die.types as DieTypes
from utils import random_items_from_pool
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
    die_types = [DieTypes.Simple]
    runes = [RuneTypes.Attack, RuneTypes.Shield, RuneTypes.Crit, RuneTypes.Fire]
    artifacts = []

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
            for i, k in enumerate(items):
                options += [f"{i+1}. {k.cost}G{" "*(4-len(str(k.cost)))} {k}"]
            
            # Display shop items
            display.frame_text(options, title="Shop")
            
            # Player select item
            selection = input.get_valid_input(
                input_text="Chose shop item ('Enter' to exit): ",
                validation=lambda x: 1<=x<=len(options) and not items[x-1].purchased,
                transform=lambda x: int(x),
                default=False
            )
            if selection == False:
                break
            # Handle player selection
            item = items[selection-1]
            
            self._buy_item(item)
    
    def _buy_item(self, item):
        if self.player.gold < item.cost:
            display.error("Not enough gold!")
            return 0
        self.player.gold -= item.cost
        match item.type_:
            case "die":
                self.player.dice += [item.item]
            case "rune":
                self.player.runes += [item.item]
            case "artifact":
                self.player.artifacts += [item.item]
        item.purchased = True
        display.success("Successfully purchased an item")
        
        
    
    def _create_die_item(self):
        die_type = random_items_from_pool(ShopPool.die_types)
        die_sides = choices([4, 6, 8, 10, 12], weights=[5, 4, 3, 2, 1], k=1)[0]
        runes = []
        for _ in range(die_sides):
            if random() <= 0.5:
                runes.append(RuneTypes.Empty())
            else:
                rune = random_items_from_pool(ShopPool.runes)()
                runes.append(rune)
        die = die_type(die_sides, runes)
        return die
    
    def _create_rune_item(self):
        return random_items_from_pool(ShopPool.runes)()
    
    def _create_artifact_item(self):
        return random_items_from_pool(ShopPool.artifacts)()