import random
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
        self.current_value = random.randint(1, self.base_sides) + self.upgrades
        self.current_rune = self.runes[self.current_value - 1 - self.upgrades]
        return self.current_value, self.current_rune
    
    def upgrade(self):
        self.upgrades += 1
        
    def mutate(self, new_sides):
        self.base_sides = new_sides
        # Fill new faces with default attack runes
        while len(self.runes) < new_sides:
            self.runes.append('empty')
            
    def enchant(self, effect):
        self.enchantment = effect
        
    def replace_rune(self, face_idx, new_rune):
        if 0 <= face_idx < len(self.runes):
            old_rune = self.runes[face_idx]
            self.runes[face_idx] = new_rune
            return old_rune

    def __repr__(self):
        return f"d{self.base_sides}{f"+{self.upgrades}" if self.upgrades else ""}"

class Rune:
    TYPES = {
        'empty': {'symbol': f'{WHITE}empty{RESET}', 'scaling': False},
        'attack': {'symbol': f'{RED}attack{RESET}', 'scaling': True},
        'shield': {'symbol': f'{BLUE}shield{RESET}', 'scaling': True},
        'heal': {'symbol': f'{GREEN}heal{RESET}', 'scaling': True},
        'crit': {'symbol': f'{YELLOW}crit{RESET}', 'scaling': False},
        'burn': {'symbol': f'{RED}burn{RESET}', 'scaling': True},
        'poison': {'symbol': f'{MAGENTA}poison{RESET}', 'scaling': True}
    }

class Workshop:
    def __init__(self, player):
        self.player = player
        
    def modify_dice(self):
        while True:
            print("\n=== Dice Workshop ===")
            print(f"Gold: {self.player.gold}")
            print("Select a die to modify:")
            for i, die in enumerate(self.player.dice):
                print(f"{i+1}. {die} | Faces: {', '.join(die.runes)}")
                
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
            print("2. Upgrade Die (+1 to all faces)")
            print("3. Mutate Die (increase die type)")
            print("4. Apply Enchantment")
            print("5. Back")
            
            choice = input("Choose modification: ")
            
            if choice == '1':
                self.attach_rune(die)
            elif choice == '2':
                self.upgrade_die(die)
            elif choice == '3':
                self.mutate_die(die)
            elif choice == '4':
                self.apply_enchantment(die)
            elif choice == '5':
                break
            else:
                print("Invalid choice!")
                
    def attach_rune(self, die):
        print("\nAvailable Runes:")
        for i, rune in enumerate(self.player.runes):
            print(f"{i+1}. {rune}")
            
        face_idx = int(input("Which face (1-{die.sides})? ")) - 1
        rune_idx = int(input("Which rune? ")) - 1
        
        if 0 <= face_idx < die.sides and 0 <= rune_idx < len(self.player.runes):
            new_rune = self.player.runes[rune_idx]
            old_rune = die.replace_rune(face_idx, self.player.runes[rune_idx])
            del self.player.runes[rune_idx]
            if old_rune != "empty":
                self.player.runes.append(old_rune)
                print(f"Replaced {old_rune} with {new_rune} on face {face_idx+1}!")
            else:
                print(f"Attached {new_rune} to face {face_idx+1}!")
        else:
            print("Invalid selection!")
            
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
        
        if die.base_sides in mutation_map and self.player.gold >= cost:
            self.player.gold -= cost
            new_sides = mutation_map[die.base_sides]
            die.mutate(new_sides)
            print(f"Mutated to d{new_sides}!")
        else:
            print("Can't mutate or insufficient funds!")
            
    def apply_enchantment(self, die):
        enchantments = {
            'Burn': {'cost': 75, 'effect': 'burn'},
            'Freeze': {'cost': 75, 'effect': 'freeze'},
            'Spray': {'cost': 100, 'effect': 'aoe'}
        }
        
        print("Available Enchantments:")
        for i, (name, info) in enumerate(enchantments.items()):
            print(f"{i+1}. {name} ({info['cost']}g)")
            
        choice = input("Choose enchantment: ")
        try:
            idx = int(choice) - 1
            name = list(enchantments.keys())[idx]
            info = enchantments[name]
            
            if self.player.gold >= info['cost']:
                self.player.gold -= info['cost']
                die.enchant(info['effect'])
                print(f"Applied {name} enchantment!")
            else:
                print("Not enough gold!")
        except:
            print("Invalid selection!")

class Entity:
    def __init__(self, health):
        self.max_health = health
        self.health = health
        self.shield = 0
        self.statuses = {}
        
    def add_status(self, name, duration, potency):
        self.statuses[name] = {'duration': duration, 'potency': potency}
        
    def tick_statuses(self):
        expired = []
        for status, info in self.statuses.items():
            info['duration'] -= 1
            if info['duration'] <= 0:
                expired.append(status)
        for status in expired:
            del self.statuses[status]
        self.shield = max(self.shield - 1, 0)
            
    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, damage):
        actual = max(damage - self.shield, 0)
        self.shield = max(self.shield - damage, 0)
        self.health -= actual
        return actual

# Modified Player class
class Player(Entity):
    def __init__(self):
        super().__init__(30)
        self.dice = [
            Die(4, ['attack']*4),
            Die(4, ['shield']*4)
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

    def add_rune(self, rune_type):
        if len(self.runes) < self.max_runes:
            self.runes.append(rune_type)
            return True
        return False

    def add_artifact(self, artifact):
        self.artifacts.append(artifact)
        artifact.apply(self)

class Enemy(Entity):
    def __init__(self, difficulty):
        super().__init__(8 + difficulty * 4)
        self.dice = [
            Die(4, ['attack']*2 + ['shield']*2),
            Die(4, ['attack']*3 + ['crit'])
        ]

class BattleSystem:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        
    def process_roll(self, source, target, value, rune_type):
        effect = {}
        rune = Rune.TYPES[rune_type]
        
        potency = value
        
        # Handle enchantments
        if source == self.player:
            die = self.find_die_with_value(value)
            if die and die.enchantment:
                potency = self.apply_enchantment_effect(die.enchantment, value)
        
        if rune_type == 'attack':
            effect['damage'] = value if rune['scaling'] else 1
        elif rune_type == 'shield':
            source.shield += value if rune['scaling'] else 3
            effect['shield'] = value
        elif rune_type == 'heal':
            source.health = min(source.health + (value if rune['scaling'] else 2), source.max_health)
            effect['heal'] = value
        elif rune_type == 'crit':
            effect['crit'] = 1
        elif rune_type == 'burn':
            target.add_status('burn', 2, value)
            effect['burn'] = value
        elif rune_type == 'poison':
            target.add_status('poison', 3, value//2)
            
        return effect
    
    def find_die_with_value(self, value):
        for die in self.player.dice:
            if die.current_value == value:
                return die
        return None
        
    def apply_enchantment_effect(self, enchantment, value):
        if enchantment == 'burn':
            return 1  # Fixed potency
        elif enchantment == 'aoe':
            return value // 2  # Split damage
        # Add other enchantment effects
        return value
    
    def apply_status_damage(self):
        for entity in [self.player, self.enemy]:
            damage = 0
            if 'burn' in entity.statuses:
                dmg = entity.statuses['burn']['potency']
                damage += dmg
                print(f"{'Enemy' if entity==self.enemy else 'Player'} burns for {dmg}!")
            if 'poison' in entity.statuses:
                dmg = entity.statuses['poison']['potency']
                damage += dmg
                print(f"{'Enemy' if entity==self.enemy else 'Player'} poisoned for {dmg}!")
            
            if damage > 0:
                entity.health -= damage
                
    def show_statuses(self):
        for name, entity in [('Player', self.player), ('Enemy', self.enemy)]:
            if entity.statuses:
                status_str = ", ".join([f"{k}({v['duration']})" for k,v in entity.statuses.items()])
                print(f"{name} statuses: {status_str}")
    
    def battle_round(self):
        print(f"\n=== Round Start ===")
        # Status damage
        self.apply_status_damage()
        self.show_statuses()
        
        # Player turn
        print("\nPlayer's roll:")
        player_effects = {'damage':0, 'crit':0}
        for i, die in enumerate(self.player.dice):
            val, rune = die.roll()
            print(f"Die {i+1}: {val} {Rune.TYPES[rune]['symbol']}")
            effects = self.process_roll(self.player, self.enemy, val, rune)
            player_effects['damage'] += effects.get('damage',0)
            player_effects['crit'] += effects.get('crit',0)
            
        # Reroll logic
        while self.player.rerolls > 0:
            if input("\nReroll? (y/n): ").lower() == 'y':
                die_idx = int(input(f"Which die (1-{len(self.player.dice)}): ")) - 1
                die = self.player.dice[die_idx]
                val, rune = die.roll()
                print(f"New roll: {val} {Rune.TYPES[rune]['symbol']}")
                self.player.rerolls -= 1
            else:
                break
        self.player.rerolls = self.player.max_rerolls
        
        # Enemy turn
        print("\nEnemy's roll:")
        enemy_effects = {'damage':0, 'crit':0}
        for die in self.enemy.dice:
            val, rune = die.roll()
            print(f"Enemy die: {val} {Rune.TYPES[rune]['symbol']}")
            effects = self.process_roll(self.enemy, self.player, val, rune)
            enemy_effects['damage'] += effects.get('damage',0)
            enemy_effects['crit'] += effects.get('crit',0)
            
        # Resolve combat
        player_dmg = player_effects['damage']
        if random.random() < player_effects['crit'] * 0.25:
            player_dmg *= 2
            print("\nCritical hit!")
            
        enemy_dmg = enemy_effects['damage']
        if random.random() < enemy_effects['crit'] * 0.25:
            enemy_dmg *= 2
            print("Enemy critical hit!")
            
        self.enemy.take_damage(player_dmg)
        self.player.take_damage(enemy_dmg)
        
        print(f"\nPlayer: {self.player.health}/{self.player.max_health} HP | {self.player.shield} shield")
        print(f"Enemy: {self.enemy.health}/{self.enemy.max_health} HP | {self.enemy.shield} shield")
        
        # Tick status durations
        self.player.tick_statuses()
        self.enemy.tick_statuses()

import random

class Game:
    def __init__(self, player):
        self.player = player
        self.room_count = 0
        self.completed_rooms = 0

    def generate_room_options(self):
        if self.completed_rooms >= 10:
            return [BossRoom()]
        
        room_types = []
        weights = [4, 3, 3, 2, 2]  # Enemy, Chest, Shop, Event
        for _ in range(2):
            rt = random.choices(['enemy', 'chest', 'shop', 'event', 'workshop'], weights, k=1)[0]
            room_types.append(rt)
        return [Room.create(rt) for rt in room_types]

    def play(self):
        while self.player.is_alive():
            if self.completed_rooms >= 10:
                final_boss = BossRoom()
                final_boss.enter(self.player)
                if self.player.is_alive():
                    print("\n=== CONGRATULATIONS! You defeated the Final Boss! ===")
                break
            
            print(f"\n=== Progress: {self.completed_rooms}/10 rooms ===")
            options = self.generate_room_options()
            
            print("\nChoose your next room:")
            for i, room in enumerate(options):
                print(f"{i+1}. {room.description}")
            
            choice = int(input("Enter choice: ")) - 1
            selected_room = options[choice]
            success = selected_room.enter(self.player)
            
            if not success:
                print("\n=== GAME OVER ===")
                return
            
            if isinstance(selected_room, CombatRoom):
                self.player.gold += random.randint(10, 20)
                print(f"\nYou gained {self.player.gold} gold!")
            
            self.completed_rooms += 1    
            self.player.health = min(self.player.health + 2, self.player.max_health)

class Room:
    @staticmethod
    def create(room_type):
        if room_type == 'enemy':
            return CombatRoom()
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
            sides = random.choice([4, 6, 6, 8])
            new_die = Die(sides, ['empty']*sides)
            if player.add_die(new_die):
                print(f"Found an empty d{sides} die!")
        
        elif reward == 'rune':
            rune_type = random.choice(['shield', 'heal', 'crit', 'poison'])
            if player.add_rune(rune_type):
                print(f"Found a {rune_type} rune!")
        
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
        print("\nWelcome to the Shop!")
        print(f"Your gold: {player.gold}")
        print("1. Buy d4 Attack Die (50g)")
        print("2. Buy Poison Rune (10g)")
        print("3. Buy Crit Rune (10g)")
        print("4. Leave")
        
        choice = input("Choose: ")
        if choice == '1' and player.gold >= 50:
            player.gold -= 50
            new_die = Die(4, ['attack']*4)
            if player.add_die(new_die):
                print("Purchased d4 attack die!")
        
        elif choice == '2' and player.gold >= 10:
            player.gold -= 10
            if player.add_rune('poison'):
                print("Purchased poison rune!")
        
        elif choice == '3' and player.gold >= 10:
            player.gold -= 10
            if player.add_rune('crit'):
                print("Purchased crit rune!")
        
        return True

class EventRoom(Room):
    @property
    def description(self):
        return "Mysterious Event"

    def enter(self, player):
        event = random.choice(['heal', 'gold', 'trap'])
        if event == 'heal':
            player.health = player.max_health
            print("\nA healing spring restores you to full health!")
        elif event == 'gold':
            gold = random.randint(20, 40)
            player.gold += gold
            print(f"\nFound {gold} gold in an abandoned cart!")
        elif event == 'trap':
            damage = random.randint(5, 10)
            player.take_damage(damage)
            print(f"\nTriggered a trap! Took {damage} damage!")
        return True

class BossRoom(CombatRoom):
    def __init__(self):
        super().__init__(difficulty_mod=5)

    @property
    def description(self):
        return "Final Boss Lair"

    def enter(self, player):
        print("\n=== FINAL BOSS APPEARS ===")
        boss = Enemy(10)
        boss.health = 100
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