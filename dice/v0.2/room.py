import random
from rune import Runes
from color import Fore, Back, Style
from die import Die
from artifact import Artifacts
from entity import Enemy

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

class Workshop:
    def __init__(self, player):
        self.player = player
    
    def modify_dice(self):
        while True:
            print("\n=== Мастерская ===")
            print(f"Золото: {self.player.gold}")
            print("\nДоступные руны:")
            for i, rune in enumerate(self.player.runes):
                print(f"{i+1}. {rune.symbol}")
            print("\nДоступные кости:")
            for i, die in enumerate(self.player.dice):
                print(f"{i+1}. {die} | Стороны: {', '.join([rune.symbol for rune in die.runes])}")
                
            choice = input("\nВыбери кость (1-8) или выход(q): ")
            if choice.lower() == 'q':
                break
                
            try:
                die_idx = int(choice) - 1
                selected_die = self.player.dice[die_idx]
                self.show_mod_options(selected_die)
            except (ValueError, IndexError):
                print("Неправильный выбор!")
                
    def show_mod_options(self, die):
        while True:
            print(f"\nВыбрано: {die}")
            print("1. Прикрепить руну к стороне")
            print("2. Снять руну со стороны")
            print("3. Улучшить(+1 ко всем сторонам)")
            print("4. Преобразовать(увеличить количество сторон)")
            print("5. Удалить кость")
            print("6. Удалить руну")
            # print("4. Apply Enchantment")
            print("q. Назад")
            
            choice = input("Выберите: ")
            
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
                print("Неправильный выбор!")
                
    def attach_rune(self, die):
        print("\nДоступные руны:")
        for i, rune in enumerate(self.player.runes):
            print(f"{i+1}. {rune.symbol}")
        print(f"{die} | Стороны: {', '.join([rune.symbol for rune in die.runes])}")
        rune_id = int(input("Какую руну? ")) - 1
        face_id = int(input(f"Какую сторону (1-{die.sides})? ")) - 1
        
        if 0 <= face_id < die.sides and 0 <= rune_id < len(self.player.runes):
            new_rune = self.player.runes[rune_id]
            old_rune = die.replace_rune(face_id, self.player.runes[rune_id])
            del self.player.runes[rune_id]
            if old_rune.name != Runes.empty.value.name:
                self.player.runes.append(old_rune)
                print(f"Замена {old_rune.symbol} на {new_rune.symbol} на стороне {face_id+1}!")
            else:
                print(f"Прикреплено {new_rune.symbol} к стороне {face_id+1}!")
        else:
            print("Неправильный выбор!")
        
    def remove_rune(self, die):
        print(f"{die} | Стороны: {', '.join([rune.symbol for rune in die.runes])}")
        face_id = int(input(f"С какой стороны (1-{die.sides})? ")) - 1
        if 0 <= face_id <= die.sides:
            rune = die.remove_rune(face_id)
            if rune.name != Runes.empty.value.name:
                print(f"Убрано {rune.symbol} со стороны {face_id+1}")
                self.player.runes.append(rune)
            else:
                print(f"Нельзя снять руну с пустой стороны")
        
    
    def upgrade_die(self, die):
        cost = 25 * (die.upgrades + 1)
        if self.player.gold >= cost:
            self.player.gold -= cost
            die.upgrade()
            print(f"улучшено до d{die.base_sides}+{die.upgrades}!")
        else:
            print(f"Нужно {cost} золота для следующего улучшения!")
            
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
            print(f"Преобразовано в d{new_sides}!")
        else:
            print("нельзя преобразовать!")
    
    def del_dice(self, die):
        for i in range(len(self.player.dice)):
            if self.player.dice[i] == die:
                del self.player.dice[i]
                
    def del_rune(self, die):
        print("\nДоступные руны:")
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

class WorkshopRoom(Room):
    @property
    def description(self):
        return "Мастерская"
    
    def enter(self, player):
        workshop = Workshop(player)
        workshop.modify_dice()
        return True

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
        for name, entity in [('Игрок', self.player), ('Враг', self.enemy)]:
            if entity.effects:
                effect_str = ""
                for effect in entity.effects:
                    if effect.symbol != "hidden":
                        effect_str += f"{effect.symbol}({effect.value}|{effect.duration}); "
                print(f"{name} Эффекты: {effect_str}")
    
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
        print(f"\n=== Начало раунда ===")
        print(f"\nИгрок: {self.player.health}/{self.player.max_health} HP | {self.player.shield} щит")
        print(f"Враг: {self.enemy.health}/{self.enemy.max_health} HP | {self.enemy.shield} щит")
        # Status damage
        self.show_effects()
        
        # Player's turn
        print("\nБроски игрока:")
        for die in self.player.dice:
            value, rune = die.roll()
            self.player.roll_results.append([value, rune])
            print(f"{die}\t: {value} {rune.symbol}")
            
        # Reroll logic
        while self.player.rerolls > 0:
            if input("\nПереброс? (y/n): ").lower() == 'y':
                die_id = 0
                try:
                    die_id = int(input(f"Какую (1-{len(self.player.dice)}): ")) - 1
                    die = self.player.dice[die_id]
                except:
                    print("Неправильный выбор!")
                    break
                value, rune = die.roll()
                print(f"Новый бросок: {value} {rune.symbol}")
                self.player.roll_results[die_id] = [value, rune]
                self.player.rerolls -= 1
            else:
                break
            
        self.player.rerolls = self.player.max_rerolls
        
        # Enemy turn
        print("\nБроски врага:")
        for die in self.enemy.dice:
            value, rune = die.roll()
            self.enemy.roll_results.append([value, rune])
            print(f"{die}\t: {value} {rune.symbol}")
        
            
        # Resolve rolls results
        self.resolve_rolls(self.player, self.enemy)
        
        print(f"\nИгрок: {self.player.health}/{self.player.max_health} HP | {self.player.shield} щит")
        print(f"Враг: {self.enemy.health}/{self.enemy.max_health} HP | {self.enemy.shield} щит")
        
        # Tick status durations
        self.player.tick()
        self.enemy.tick()

class CombatRoom(Room):
    def __init__(self, difficulty_mod=0):
        self.difficulty = random.randint(1, 2) + difficulty_mod

    @property
    def description(self):
        return f"Логово врага (уровень {self.difficulty})"

    def enter(self, player):
        enemy = Enemy(self.difficulty)
        battle = BattleSystem(player, enemy)
        
        print(f"\n=== Логово врага! ===")
        while player.is_alive() and enemy.is_alive():
            battle.battle_round()
        
        if player.is_alive():
            player.gold += int(random.randint(5, 10)*self.difficulty**(0.5))
            player.shield = 0
            return True
        return False

class ChestRoom(Room):
    @property
    def description(self):
        return "Сундук сокровищ"

    def enter(self, player):
        print(f"\n{Fore(228)}Вы нашли блестящий сундук!{Style.RESET_ALL}")
        reward = random.choices(['die', 'rune', 'artifact'], weights=(1, 3, 1), k=1)[0]
        
        match(reward):
            case'die':
                sides = random.choices([4, 6, 8, 10, 12, 20], weights=(6, 5, 4, 3, 2, 1), k=1)[0]
                new_die = Die(sides, [Runes.empty.value]*sides)
                if player.add_die(new_die):
                    print(f"Найдена пустая кость d{sides}!")
                else:
                    print(f"Нет места. {sides*2} золота вместо этого.")
                    player.gold += 10
            
            case 'rune':
                rune = random.choices([r.value for r in Runes][1:], [r.value.rarity for r in Runes][1:], k=1)[0]
                if player.add_rune(rune):
                    print(f"Найдена руна {rune.symbol}!")
                else:
                    print(f"Нет места. {rune.cost} золота вместо этого.")
                    player.gold += rune.cost
            
            case 'artifact':
                artifact = random.choices([a.value for a in Artifacts], [a.value.rarity for a in Artifacts], k=1)[0]
                print(f"Найдено {artifact.name}!\n{artifact.description}.")
                if input("Взять? (y/n)") == "y":
                    if player.add_artifact(artifact):
                        print(f"You now have {artifact.name}!")
                    else:
                        print(f"Нет места. 30 золота вместо этого.")
                        player.gold += 30
        return True

class ShopRoom(Room):
    @property
    def description(self):
        return "Магазин"

    def enter(self, player):
        die_sides = random.choice([4, 6, 8])
        die_runes = []
        for _ in range(die_sides):
            rune = random.choices([r.value for r in Runes], weights = (r.value.rarity for r in Runes), k=1)[0]
            die_runes.append(rune)
        die = Die(die_sides, die_runes)
        die_cost = int(sum([r.cost for r in die.runes])*0.9 + die_sides*2)
        rune1 = random.choices([r.value for r in Runes][1:], [r.value.rarity for r in Runes][1:], k=1)[0]
        rune2 = random.choices([r.value for r in Runes][1:], [r.value.rarity for r in Runes][1:], k=1)[0]
        print(f"\nДобро пожаловать в магазин!")
        print(f"Золото: {player.gold}g")
        print(f"1. Купить кость d{die_sides} за ({die_cost}g) ({", ".join([rune.symbol for rune in die.runes])})")
        print(f"2. Купить руну {rune1.symbol} за ({rune1.cost}g)")
        print(f"3. Купить руну {rune2.symbol} за ({rune2.cost}g)")
        print(f"4. Leave")
        
        choice = input("Выбор: ")
        if choice == '1' and player.gold >= die_cost:
            if player.add_die(die):
                player.gold -= die_cost
                print(f"Куплена кость d{die_sides}!")
            else:
                print("Нет места.")
        elif choice == '2' and player.gold >= rune1.cost:
            if player.add_rune(rune1):
                player.gold -= rune1.cost
                print(f"Куплена руна {rune1.symbol}!")
            else:
                print("Нет места.")
        
        elif choice == '3' and player.gold >= rune2.cost:
            if player.add_rune(rune2):
                player.gold -= rune2.cost
                print(f"Куплена руна {rune2.symbol}!")
            else:
                print("Нет места.")
        
        return True

class EventRoom(Room):
    @property
    def description(self):
        return "Таинственное событие"

    def enter(self, player):
        event = random.choice(['heal', 'gold', 'trap'])
        match(event):
            case 'heal':
                player.health = player.max_health
                print(f"\n{Fore(228)}Лечебные источники востановили все здоровье!{Style.RESET_ALL}")
            case 'gold':
                gold = random.randint(20, 40)
                player.gold += gold
                print(f"\n{Fore(228)}Найдено {gold} золота в забытой вагонетке!{Style.RESET_ALL}")
            case 'trap':
                damage = random.randint(5, 10)
                player.take_damage(damage)
                print(f"\n{Fore(228)}Ловушка! получено {damage} урона!{Style.RESET_ALL}")
        return True

class BossRoom(CombatRoom):
    def __init__(self, difficulty_mod=5):
        super().__init__(difficulty_mod)

    @property
    def description(self):
        return "Логово Босса"

    def enter(self, player):
        print(f"\n{Back(52)}=== ПОСЛЕДНИЙ БОСС ==={Style.RESET_ALL}")
        boss = Enemy(15, "Босс")
        boss.dice.append(Die(10, [Runes.poison.value]*8 + [Runes.crit.value]*3))
        battle = BattleSystem(player, boss)
        
        while player.is_alive() and boss.is_alive():
            battle.battle_round()
        
        return player.is_alive()
