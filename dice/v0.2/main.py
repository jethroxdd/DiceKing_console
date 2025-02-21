import random
import enum
from rune import Runes
import effect
from color import *

class Die:
    def __init__(self, sides, runes, upgrades=0, enchantment=None):
        self.base_sides = sides
        self.runes = runes
        self.upgrades = upgrades
        self.enchantment = enchantment
        self.current_value = 1
        self.current_rune = runes[0]
    
    @property
    def sides(self):
        return self.base_sides + self.upgrades
    
    def roll(self):
        self.current_value = random.randint(1, self.base_sides)
        self.current_rune = self.runes[self.current_value - 1]
        return self.current_value + self.upgrades, self.current_rune
    
    def upgrade(self):
        self.upgrades += 1
        
    def mutate(self, new_sides):
        self.base_sides = new_sides
        # Fill new faces with default attack runes
        while len(self.runes) < new_sides:
            self.runes.append(Runes.empty.value)
            
    def enchant(self, enchantment):
        self.enchantment = enchantment
        
    def replace_rune(self, face_id, new_rune):
        if 0 <= face_id < len(self.runes):
            old_rune = self.runes[face_id]
            self.runes[face_id] = new_rune
            return old_rune
    
    def remove_rune(self, face_id):
        if 0 <= face_id < len(self.runes):
            rune = self.runes[face_id]
            self.runes[face_id] = Runes.empty.value
            return rune

    def __repr__(self):
        return f"d{self.base_sides}{f"+{self.upgrades}" if self.upgrades else ""}"

class Workshop:
    def __init__(self, player):
        self.player = player
    
    def modify_dice(self):
        while True:
            print("\n=== Dice Workshop ===")
            print(f"Gold: {self.player.gold}")
            print("\nAvailable Runes:")
            for i, rune in enumerate(self.player.runes):
                print(f"{i+1}. {rune.symbol}")
            print("\nSelect a die to modify:")
            for i, die in enumerate(self.player.dice):
                print(f"{i+1}. {die} | Faces: {', '.join([rune.symbol for rune in die.runes])}")
                
            choice = input("\nChoose die (1-8) or (q)uit: ")
            if choice.lower() == 'q':
                break
                
            try:
                die_idx = int(choice) - 1
                selected_die = self.player.dice[die_idx]
                self.show_mod_options(selected_die)
            except (ValueError, IndexError):
                print("Invalid selection!")
                
    def show_mod_options(self, die):
        while True:
            print(f"\nSelected: {die}")
            print("1. Attach Rune to Face")
            print("2. Take off Rune from Face")
            print("3. Upgrade Die (+1 to all faces)")
            print("4. Mutate Die (increase die type)")
            print("5. Delete dice")
            print("6. Delete rune")
            # print("4. Apply Enchantment")
            print("q. Back")
            
            choice = input("Choose modification: ")
            
            if choice == '1':
                self.attach_rune(die)
            elif choice == '2':
                self.remove_rune(die)
            elif choice == '3':
                self.upgrade_die(die)
            elif choice == '4':
                self.mutate_die(die)
            elif choice == '5':
                self.del_dice(die)
            elif choice == '6':
                self.del_dice(die)
            # elif choice == '4':
                # self.apply_enchantment(die)
            elif choice == 'q':
                break
            else:
                print("Invalid choice!")
                
    def attach_rune(self, die):
        print("\nAvailable Runes:")
        for i, rune in enumerate(self.player.runes):
            print(f"{i+1}. {rune.symbol}")
        print(f"{die} | Faces: {', '.join([rune.symbol for rune in die.runes])}")
        face_id = int(input(f"Which face (1-{die.sides})? ")) - 1
        rune_id = int(input("Which rune? ")) - 1
        
        if 0 <= face_id < die.sides and 0 <= rune_id < len(self.player.runes):
            new_rune = self.player.runes[rune_id]
            old_rune = die.replace_rune(face_id, self.player.runes[rune_id])
            del self.player.runes[rune_id]
            if old_rune.name != Runes.empty.value.name:
                self.player.runes.append(old_rune)
                print(f"Replaced {old_rune.symbol} with {new_rune.symbol} on face {face_id+1}!")
            else:
                print(f"Attached {new_rune.symbol} to face {face_id+1}!")
        else:
            print("Invalid selection!")
        
    def remove_rune(self, die):
        print(f"{die} | Faces: {', '.join([rune.symbol for rune in die.runes])}")
        face_id = int(input(f"Which face (1-{die.sides})? ")) - 1
        if 0 <= face_id <= die.sides:
            rune = die.remove_rune(face_id)
            if rune.name != Runes.empty.value.name:
                print(f"Removed {rune.symbol} from face {face_id+1}")
                self.player.runes.append(rune)
            else:
                print(f"Cant remove rune from empty side")
        
    
    def upgrade_die(self, die):
        cost = 25 * (die.upgrades + 1)
        if self.player.gold >= cost:
            self.player.gold -= cost
            die.upgrade()
            print(f"Upgraded to d{die.base_sides}+{die.upgrades}!")
        else:
            print(f"Need {cost} gold for next upgrade!")
            
    def mutate_die(self, die):
        mutation_map = {
            4: 6,
            6: 8,
            8: 10,
            10: 12
        }
        cost = 100
        
        if die.base_sides in mutation_map.keys() and self.player.gold >= cost:
            self.player.gold -= cost
            new_sides = mutation_map[die.base_sides]
            die.mutate(new_sides)
            print(f"Mutated to d{new_sides}!")
        else:
            print("Can't mutate or insufficient funds!")
    
    def del_dice(self, die):
        for i in range(len(self.player.dice)):
            if self.player.dice[i] == die:
                del self.player.dice[i]
                
    def del_rune(self, die):
        print("\nAvailable Runes:")
        for i, rune in enumerate(self.player.runes):
            print(f"{i+1}. {rune.symbol}")
            
    # def apply_enchantment(self, die):
    #     enchantments = {
    #         'Burn': {'cost': 75, 'effect': 'burn'},
    #         'Freeze': {'cost': 75, 'effect': 'freeze'},
    #         'Spray': {'cost': 100, 'effect': 'aoe'}
    #     }
        
    #     print("Available Enchantments:")
    #     for i, (name, info) in enumerate(enchantments.items()):
    #         print(f"{i+1}. {name} ({info['cost']}g)")
            
    #     choice = input("Choose enchantment: ")
    #     try:
    #         idx = int(choice) - 1
    #         name = list(enchantments.keys())[idx]
    #         info = enchantments[name]
            
    #         if self.player.gold >= info['cost']:
    #             self.player.gold -= info['cost']
    #             die.enchant(info['effect'])
    #             print(f"Applied {name} enchantment!")
    #         else:
    #             print("Not enough gold!")
    #     except:
    #         print("Invalid selection!")

class Entity:
    def __init__(self, health):
        self.target = None
        self.max_health = health
        self.health = health
        self.shield = 0
        self.effects = []
        self.roll_results = []
    
    def set_target(self, entity):
        self.target = entity
    
    def add_effect(self, effect):
        for e in self.effects:
            if e.name == effect.name:
                e.add(effect)
                break
        else:
            self.effects.append(effect)
        
    def tick(self):
        decayed_effect_ids = []
        for i in range(len(self.effects)):
            self.effects[i].tick()
            if self.effects[i].is_ended:
                decayed_effect_ids.append(i)
        for i in decayed_effect_ids:
            del self.effects[i]
        self.shield = max(self.shield - 1, 0)
        self.crit = False
        self.roll_results = []
            
    def is_alive(self):
        return self.health > 0
    
    def apply_effects(self, is_good):
        for order in range(5):
            for effect in self.effects:
                if is_good == effect.is_good and order == effect.order:
                    effect.apply(self)
    
    def take_damage(self, damage):
        actual = max(damage - self.shield, 0)
        self.shield = max(self.shield - damage, 0)
        self.health -= actual
        return actual

    def take_heal(self, amount):
        self.health = min(self.health + amount, self.max_health)

class Player(Entity):
    def __init__(self):
        super().__init__(30)
        self.dice = [
            Die(4, [Runes.attack.value]*4),
            Die(4, [Runes.shield.value]*4)
        ]
        self.runes = []
        self.artifacts = []
        self.gold = 0
        self.max_dice = 8
        self.max_runes = 5
        self.max_rerolls = 1
        self.rerolls = self.max_rerolls

    def add_die(self, die):
        if len(self.dice) < self.max_dice:
            self.dice.append(die)
            return True
        return False

    def add_rune(self, rune):
        if len(self.runes) < self.max_runes:
            self.runes.append(rune)
            return True
        return False

    def add_artifact(self, artifact):
        self.artifacts.append(artifact)
        artifact.apply(self)

class Enemy(Entity):
    def __init__(self, difficulty):
        super().__init__(8 + difficulty * 4)
        self.dice = [
            Die(4, [Runes.attack.value]*2 + [Runes.shield.value]*2),
            Die(4, [Runes.attack.value]*3 + [Runes.crit.value])
        ]

class BattleSystem:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.set_targets()
    
    def set_targets(self):
        self.player.set_target(self.enemy)
        self.enemy.set_target(self.player)
    
    def find_die_with_value(self, value):
        for die in self.player.dice:
            if die.current_value == value:
                return die
        return None
                
    def show_effects(self):
        for name, entity in [('Player', self.player), ('Enemy', self.enemy)]:
            if entity.effects:
                effect_str = ""
                for effect in entity.effects:
                    if effect.name != "hidden":
                        effect_str += f"{effect.symbol}({effect.value}|{effect.duration}); "
                print(f"{name} statuses: {effect_str}")
    
    def resolve_rolls(self, player, enemy):
        for order in range(6):
            # applying rune effects
            for value, rune in player.roll_results:
                if rune.order == order:
                    rune.apply(value, player)
            for value, rune in enemy.roll_results:
                if rune.order == order:
                    rune.apply(value, enemy)
            
            # applying status effects
            for effect in player.effects:
                if effect.order == order:
                    effect.apply(player)
            for effect in enemy.effects:
                if effect.order == order:
                    effect.apply(enemy)
    
    def battle_round(self):
        print(f"\n=== Round Start ===")
        print(f"\nPlayer: {self.player.health}/{self.player.max_health} HP | {self.player.shield} shield")
        print(f"Enemy: {self.enemy.health}/{self.enemy.max_health} HP | {self.enemy.shield} shield")
        # Status damage
        self.show_effects()
        
        # Player's turn
        print("\nPlayer's roll:")
        for die in self.player.dice:
            value, rune = die.roll()
            self.player.roll_results.append([value, rune])
            print(f"{die}\t: {value} {rune.symbol}")
            
        # Reroll logic
        while self.player.rerolls > 0:
            if input("\nReroll? (y/n): ").lower() == 'y':
                die_id = 0
                try:
                    die_id = int(input(f"Which die (1-{len(self.player.dice)}): ")) - 1
                    die = self.player.dice[die_id]
                except:
                    print("Invalid selection!")
                    break
                value, rune = die.roll()
                print(f"New roll: {value} {rune.symbol}")
                self.player.roll_results[die_id] = [value, rune]
                self.player.rerolls -= 1
            else:
                break
            
        self.player.rerolls = self.player.max_rerolls
        
        # Enemy turn
        print("\nEnemy's roll:")
        for die in self.enemy.dice:
            value, rune = die.roll()
            self.enemy.roll_results.append([value, rune])
            print(f"{die}\t: {value} {rune.symbol}")
        
            
        # Resolve rolls results
        self.resolve_rolls(self.player, self.enemy)
        
        print(f"\nPlayer: {self.player.health}/{self.player.max_health} HP | {self.player.shield} shield")
        print(f"Enemy: {self.enemy.health}/{self.enemy.max_health} HP | {self.enemy.shield} shield")
        
        # Tick status durations
        self.player.tick()
        self.enemy.tick()

class Game:
    def __init__(self, player):
        self.player = player
        self.room_count = 0
        self.completed_rooms = 0
        self.difficulty = 0

    def generate_room_options(self):
        if self.completed_rooms >= 50:
            return [BossRoom(int(self.difficulty*1.5))]
        
        room_types = []
        weights = [4, 3, 3, 2, 2]  # Enemy, Chest, Shop, Event
        for _ in range(2):
            rt = random.choices(['enemy', 'chest', 'shop', 'event', 'workshop'], weights, k=1)[0]
            room_types.append(rt)
        return [Room.create(rt, self.difficulty) for rt in room_types]

    def play(self):
        while self.player.is_alive():
            options = self.generate_room_options()
            while True:
                try:
                    print(f"\n=== Progress: {self.completed_rooms}/50 rooms ===")
                    
                    print("\nChoose your next room:")
                    for i, room in enumerate(options):
                        print(f"{i+1}. {room.description}")
            
            
                    choice = int(input("Enter choice: ")) - 1
                    if choice < 0:
                        choice = ""
                    selected_room = options[choice]
                    break
                except:
                    print("Invalid selection!")
            success = selected_room.enter(self.player)
            
            if self.completed_rooms >= 50:
                if self.player.is_alive():
                    print("\n=== CONGRATULATIONS! You defeated the Final Boss! ===")
                break
            
            if not success:
                print("\n=== GAME OVER ===")
                return
            
            if isinstance(selected_room, CombatRoom):
                self.player.gold += random.randint(int(10*(self.difficulty**(0.5))), int(20*(self.difficulty)**(0.5)))
                print(f"\nYou gained {self.player.gold} gold!") 
                self.difficulty += 1
            
            self.completed_rooms += 1
            self.player.health = min(self.player.health + 2, self.player.max_health)

# Rooms
class Room:
    @staticmethod
    def create(room_type, difficulty=0):
        if room_type == 'enemy':
            return CombatRoom(difficulty)
        elif room_type == 'chest':
            return ChestRoom()
        elif room_type == 'shop':
            return ShopRoom()
        elif room_type == 'event':
            return EventRoom()
        elif room_type == 'workshop':
            return WorkshopRoom()
        return Room()

    @property
    def description(self):
        return "Unknown Room"

class WorkshopRoom(Room):
    @property
    def description(self):
        return "Modification Workshop"
    
    def enter(self, player):
        workshop = Workshop(player)
        workshop.modify_dice()
        return True

class CombatRoom(Room):
    def __init__(self, difficulty_mod=0):
        self.difficulty = random.randint(1, 2) + difficulty_mod

    @property
    def description(self):
        return f"Enemy Encounter (Level {self.difficulty})"

    def enter(self, player):
        enemy = Enemy(self.difficulty)
        battle = BattleSystem(player, enemy)
        
        print(f"\n=== Enemy Encounter! ===")
        while player.is_alive() and enemy.is_alive():
            battle.battle_round()
        
        if player.is_alive():
            player.gold += int(random.randint(20, 40)*self.difficulty**(0.5))
            return True
        return False

class ChestRoom(Room):
    @property
    def description(self):
        return "Treasure Chest"

    def enter(self, player):
        print("\nYou found a glowing chest!")
        reward = random.choices(['die', 'rune', 'artifact'], weights=(1, 3, 1), k=1)[0]
        
        if reward == 'die':
            sides = random.choices([4, 6, 8, 10, 12, 20], weights=(6, 5, 4, 3, 2, 1), k=1)[0]
            new_die = Die(sides, [Runes.empty.value]*sides)
            if player.add_die(new_die):
                print(f"Found an empty d{sides} die!")
            else:
                print("Couldn't carry die. Received 30 gold instead.")
                player.gold += 10
        
        elif reward == 'rune':
            rune_type = random.choice(['attack', 'shield', 'heal', 'crit', 'poison', 'burn'])
            rune = Runes[rune_type].value
            if player.add_rune(rune):
                print(f"Found a {rune.symbol} rune!")
            else:
                print("Couldn't carry rune. Received 10 gold instead.")
                player.gold += 10
        
        elif reward == 'artifact':
            artifact = Artifact("Magic Charm", "rerolls")
            player.add_artifact(artifact)
            print("Found Magic Charm! +1 Reroll per round")
        
        return True

class ShopRoom(Room):
    @property
    def description(self):
        return "Merchant Shop"

    def enter(self, player):
        die_sides = random.choice([4, 6, 8])
        die_runes = []
        for _ in range(die_sides):
            rune = random.choices([rune.value for rune in Runes], weights = (rune.value.rarity for rune in Runes), k=1)[0]
            die_runes.append(rune)
        die = Die(die_sides, die_runes)
        print(die.runes)
        die_cost = int(sum([rune.cost for rune in die.runes])*0.9 + 20)
        rune1 = None
        while rune1 == Runes.empty.value or rune1 == None:
            rune1 = random.choice([rune.value for rune in Runes])
        rune2 = None
        while rune2 == Runes.empty.value or rune2 == None:
            rune2 = random.choice([rune.value for rune in Runes])
        print(f"\nWelcome to the Shop!")
        print(f"Your gold: {player.gold}")
        print(f"1. Buy d{die_sides} Die ({die_cost}g) ({", ".join([rune.symbol for rune in die.runes])})")
        print(f"2. Buy {rune1.symbol} Rune ({rune1.cost}g)")
        print(f"3. Buy {rune2.symbol} Rune ({rune2.cost}g)")
        print(f"4. Leave")
        
        choice = input("Choose: ")
        if choice == '1' and player.gold >= die_cost:
            if player.add_die(die):
                player.gold -= die_cost
                print(f"Purchased d{die_sides} Die!")
            else:
                print("Cannot carry more dice! Refunding gold.")
        elif choice == '2' and player.gold >= rune1.cost:
            if player.add_rune(rune1):
                player.gold -= rune1.cost
                print(f"Purchased {rune1.symbol} rune!")
            else:
                print("Cannot carry more runes! Refunding gold.")
        
        elif choice == '3' and player.gold >= rune2.cost:
            if player.add_rune(rune2):
                player.gold -= rune2.cost
                print(f"Purchased {rune2.symbol} rune!")
            else:
                print("Cannot carry more runes! Refunding gold.")
        
        return True

class EventRoom(Room):
    @property
    def description(self):
        return "Mysterious Event"

    def enter(self, player):
        event = random.choice(['heal', 'gold', 'trap'])
        match(event):
            case 'heal':
                player.health = player.max_health
                print("\nA healing spring restores you to full health!")
            case 'gold':
                gold = random.randint(20, 40)
                player.gold += gold
                print(f"\nFound {gold} gold in an abandoned cart!")
            case 'trap':
                damage = random.randint(5, 10)
                player.take_damage(damage)
                print(f"\nTriggered a trap! Took {damage} damage!")
        return True

class BossRoom(CombatRoom):
    def __init__(self, difficulty_mod=5):
        super().__init__(difficulty_mod)

    @property
    def description(self):
        return "Final Boss Lair"

    def enter(self, player):
        print("\n=== FINAL BOSS APPEARS ===")
        boss = Enemy(15)
        boss.dice.append(Die(10, ['poison']*5 + ['crit']*5))
        battle = BattleSystem(player, boss)
        
        while player.is_alive() and boss.is_alive():
            battle.battle_round()
        
        return player.is_alive()


class Artifact:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

    def apply(self, player):
        if self.effect == "rerolls":
            player.max_rerolls += 1
            player.rerolls = player.max_rerolls

# Usage
player = Player()
game = Game(player)
game.play()