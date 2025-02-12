import random
import dices
from color import *
from entity import Entity
from effect import StaticEffect
import copy

class Room:
    @property
    def description(self):
        return "A mysterious room"

class NewDiceRoom(Room):
    def __init__(self):
        self.choices = random.sample(dices.ALL, 3)
    
    @property
    def description(self):
        return "Acquire a powerful new dice"
    
    def enter(self, player):
        print("\nChoose a dice to add:")
        for i, dice in enumerate(self.choices):
            print(f"{i+1}) {dice.name}: {dice.description}")
        
        while True:
            choice = input("Select (1-3): ")
            if choice in ["1", "2", "3"]:
                player.dices.append(copy.deepcopy(self.choices[int(choice)-1]))
                print(f"Added {self.choices[int(choice)-1].name}!")
                break

class EventRoom(Room):
    @property
    def description(self):
        return "Random event occurrence"
    
    def enter(self, player):
        event = random.choice([
            self._heal_event,
            self._damage_event,
            self._coin_buff
        ])
        event(player)
    
    def _heal_event(self, player):
        heal = random.randint(10, 20)
        player.takeHeal(heal)
        print(f"Healing springs restore {heal} HP!")

    def _damage_event(self, player):
        damage = random.randint(5, 15)
        player.takeDirectDamage(damage)
        print(f"Poisonous gas deals {damage} damage!")

    def _coin_buff(self, player):
        player.coin = random.choice(["heads", "tails"])
        print(f"Magical coin activated! Next combat: {player.coin}")

class StoreRoom(Room):
    def __init__(self):
        self.items = [
            {
                "name": "Healing Potion",
                "cost": 15,
                "effect": lambda e: e.takeHeal(30),
                "desc": "Restore 30 HP"
            },
            {
                "name": "Shield Booster",
                "cost": 20,
                "effect": lambda e: setattr(e, 'shield', e.shield + 20),
                "desc": "+20 Shield"
            },
            {
                "name": "Damage Boost",
                "cost": 25,
                "effect": lambda e: e.addEffect(StaticEffect(
                    "Power Boost", 5, lambda eff, ent: None, 3, True
                )),
                "desc": "+5 Damage for 3 turns"
            }
        ]

    @property
    def description(self):
        return f"{YELLOW}Store{RESET} - Spend your gold"

    def enter(self, player):
        print(f"\n{YELLOW}Welcome to the Store!{RESET}")
        print(f"Your gold: {YELLOW}{player.gold}{RESET}\n")
        
        while True:
            print("Items available:")
            for i, item in enumerate(self.items):
                print(f"{i+1}) {item['name']} - {item['desc']} ({YELLOW}{item['cost']}g{RESET})")
            print(f"{len(self.items)+1}) Leave store")
            
            choice = input("Select item: ")
            if choice == str(len(self.items)+1):
                return
            elif choice.isdigit() and 1 <= int(choice) <= len(self.items):
                item = self.items[int(choice)-1]
                if player.gold >= item['cost']:
                    player.gold -= item['cost']
                    item['effect'](player)
                    print(f"{GREEN}Purchased {item['name']}!{RESET}")
                else:
                    print(f"{RED}Not enough gold!{RESET}")
            else:
                print(f"{RED}Invalid choice!{RESET}")