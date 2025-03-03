import random
import effect
from rune import Runes
from color import Fore, Back, Style
from die import Die
from artifact import Artifacts
from entity import Enemy, Rat, Toad, Boss

class Room:
    @staticmethod
    def create(room_type, difficulty):
        if room_type == 'enemy':
            return CombatRoom(difficulty)
        elif room_type == 'chest':
            return ChestRoom()
        elif room_type == 'shop':
            return ShopRoom()
        elif room_type == 'event':
            return EventRoom(difficulty)
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
            print("5. Продать кость")
            print("6. Продать руну")
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
                return
            elif choice == '6':
                self.del_rune()
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
            print(f"улучшено до d{die.sides}+{die.upgrades}!")
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
        
        if die.sides in mutation_map.keys() and self.player.gold >= cost:
            self.player.gold -= cost
            new_sides = mutation_map[die.sides]
            die.mutate(new_sides)
            print(f"Преобразовано в d{new_sides}!")
        else:
            print("Нельзя преобразовать!")
    
    def del_dice(self, die):
        for i in range(len(self.player.dice)):
            if self.player.dice[i] == die:
                die_runes = die.runes
                gold_reward: int = die.sides
                for r in die_runes:
                    gold_reward += r.cost
                gold_reward *= 0.5
                self.player.gold += int(gold_reward)
                print(f"Получено {int(gold_reward)} золота")
                del self.player.dice[i]
                
    def del_rune(self):
        print("\nДоступные руны:")
        for i, rune in enumerate(self.player.runes):
            print(f"{i+1}. {rune.symbol}")
        rune_id = int(input("\n Введите номер руны: "))
        try:
            gold_reward = int(self.player.runes[rune_id-1].cost * 0.5)
            self.player.gold += gold_reward
            print(f"Получено {gold_reward} золота")
            del self.player.runes[rune_id-1]
        except:
            print("Неправильный выбор!")
            
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
        for name, entity in [('Игрок', self.player), (self.enemy.name, self.enemy)]:
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
        print(f"{self.enemy.name}: {self.enemy.health}/{self.enemy.max_health} HP | {self.enemy.shield} щит")
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
            die_id = 0
            try:
                die_id = int(input(f"Переброс (1-{len(self.player.dice)}): ")) - 1
                die = self.player.dice[die_id]
            except:
                print("Неправильный выбор!")
                break
            value, rune = die.roll()
            print(f"Новый бросок: {value} {rune.symbol}")
            self.player.roll_results[die_id] = [value, rune]
            self.player.rerolls -= 1
            
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
        print(f"{self.enemy.name}: {self.enemy.health}/{self.enemy.max_health} HP | {self.enemy.shield} щит")
        
        # Tick status durations
        self.player.tick()
        self.enemy.tick()
        
        input("Enter чтобы продолжить...")

class CombatRoom(Room):
    def __init__(self, difficulty):
        self.difficulty = random.randint(1, 2) + difficulty

    @property
    def description(self):
        return f"Логово врага (уровень {self.difficulty})"

    def enter(self, player):
        enemy = random.choice([Rat(self.difficulty), Toad(self.difficulty)])
        battle = BattleSystem(player, enemy)
        
        print(f"\n=== Логово врага! ===")
        print(f"\nКости врага {enemy.name}:")
        for i, die in enumerate(enemy.dice):
                print(f"{i+1}. {die} | Стороны: {', '.join([rune.symbol for rune in die.runes])}")
        while player.is_alive() and enemy.is_alive():
            battle.battle_round()
        
        if player.is_alive():
            reward_gold = enemy.gold
            player.gold += reward_gold
            print(f"\nПолучено {reward_gold} золота")
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

# Event rooms
class HealRoom(Room):
    @staticmethod
    def enter(player):
        player.health = player.max_health
        print(f"\n{Fore(228)}Лечебные источники востановили все здоровье!{Style.RESET_ALL}")

class GoldRoom(Room):
    @staticmethod
    def enter(player):
        gold = random.randint(20, 40)
        player.gold += gold
        print(f"\n{Fore(228)}Найдено {gold} золота в забытой вагонетке!{Style.RESET_ALL}")

class TrapRoom(Room):
    @staticmethod
    def enter(player):
        damage = random.randint(5, 10)
        player.take_damage(damage)
        print(f"\n{Fore(228)}Ловушка! получено {damage} урона!{Style.RESET_ALL}")

class StrangerRoom(Room):
    @staticmethod
    def enter(player):
        print(f"\n{Fore(153)}Таинственный незнакомец предлагает благословение...{Style.RESET_ALL}")
        print("1. +2 к всем броскам в следующей битве")
        print("2. Восстановить 10 здоровья")
        choice = input("Выберите дар (1-2): ")
        if choice == '1':
            player.add_effect(effect.Blessing(2))
            print(f"{Fore(153)}Вы чувствуете прилив магической энергии!{Style.RESET_ALL}")
        elif choice == '2':
            player.take_heal(10)
            print(f"{Fore(153)}Вас наполняет целительная сила!{Style.RESET_ALL}")

class GambleRoom(Room):
    @staticmethod
    def enter(player):
        print(f"\n{Fore(136)}Вы нашли подпольное казино!{Style.RESET_ALL}")
        if player.gold >= 20:
            try:
                bet = int(input("Введите ставку: "))
                if 0 > bet > player.gold:
                    player.gold -= bet
                    if random.randint(0, 1):
                        player.gold += bet*2
                        print(f"{Fore(220)}Вы выиграли {bet*2} золота!{Style.RESET_ALL}")
                    else:
                        print(f"{Fore(124)}Вы проиграли...{Style.RESET_ALL}")
                else:
                    print("Неправильная ставка!")
            except:
                print("Вас выгнали из казино!")
        else:
            print("У вас недостаточно денег, чтобы войти.")

class ForgeRoom(Room):
    @staticmethod
    def enter(player):
        print(f"\n{Fore(94)}Вы нашли древнюю кузницу!{Style.RESET_ALL}")
        print(f"{Fore(94)}Используйте на свой страх и риск!{Style.RESET_ALL}")
        if input("\nИспользовать (улучшить случайную кость с шансом разрушить ее)? (y/n) ") == 'y':
            if player.dice:
                die = random.choice(player.dice)
                if random.random() < 0.8:
                    die.upgrade()
                    print(f"{Fore(226)}Кость {die} ({', '.join([rune.symbol for rune in die.runes])}{Fore(226)}) была улучшена (+1)!{Style.RESET_ALL}")
                else:
                    player.dice.remove(die)
                    print(f"{Fore(124)}Кость {die} ({', '.join([rune.symbol for rune in die.runes])}{Fore(124)}) треснула и рассыпалась!{Style.RESET_ALL}")
            else:
                print("У вас нет костей???")

class AltarRoom(Room):
    @staticmethod
    def enter(player):
        print(f"\n{Fore(125)}Вы нашли кровавый алтарь...{Style.RESET_ALL}")
        print(f"{Fore(125)}Вы можете ожертвовать 10 здоровья для случайного артефакта{Style.RESET_ALL}")
        choice = input("Согласитться? (y/n): ")
        if choice == 'y' and player.health > 10:
            player.take_true_damage(10)
            artifact = random.choice(list(Artifacts)).value
            print(f"{Fore(125)}Вы получаете {artifact.name}!{Style.RESET_ALL}")
            player.add_artifact(artifact)

class MimicRoom(Room):
    @staticmethod
    def enter(player, difficulty):
        print(f"\n{Fore(130)}Сундук оживает и атакует!{Style.RESET_ALL}")
        mimic = Enemy(difficulty, "Мимик", flat_health=15)
        mimic.dice = [
            Die(6, [Runes.attack.value]*3 + [Runes.golden.value]*3),
            Die(4, [Runes.shield.value]*4)
        ]
        battle = BattleSystem(player, mimic)
        while player.is_alive() and mimic.is_alive():
            battle.battle_round()
        if player.is_alive():
            artifact = random.choice(list(Artifacts)).value
            print(f"{Fore(125)}Из мимика выпало {artifact.name}!{Style.RESET_ALL}")
            player.add_artifact(artifact)

class WindfallRoom(Room):
    @staticmethod
    def enter(player):
        print(f"\n{Fore(228)}Вы нашли сокровищницу!{Style.RESET_ALL}")
        player.gold += 20
        player.take_heal(15)
        print("Получено 20 золота и восстановлено 15 здоровья!")

class EventRoom(Room):
    def __init__(self, difficulty):
        self.difficulty = difficulty
    
    @property
    def description(self):
        return "Таинственное событие"

    def enter(self, player):
        event = random.choice(['heal', 'gold', 'trap', 'stranger', 'gamble', 'forge', 'altar', 'mimic', 'windfall'])
        match(event):
            case 'heal':
                HealRoom.enter(player)
            case 'gold':
                GoldRoom.enter(player)
            case 'trap':
                TrapRoom.enter(player)
            case 'stranger':
                StrangerRoom.enter(player)
            case 'gamble':
                GambleRoom.enter(player)
            case 'forge':
                ForgeRoom.enter(player)
            case 'altar':
                AltarRoom.enter(player)
            case 'mimic':
                MimicRoom.enter(player, self.difficulty)
            case 'windfall':
                WindfallRoom.enter(player)
        return True


class BossRoom(CombatRoom):
    def __init__(self, room):
        super().__init__(room)

    @property
    def description(self):
        return "Логово Босса"

    def enter(self, player):
        print(f"\n{Back(52)}=== ПОСЛЕДНИЙ БОСС ==={Style.RESET_ALL}")
        boss = Boss(self.difficulty)
        battle = BattleSystem(player, boss)
        
        while player.is_alive() and boss.is_alive():
            battle.battle_round()
        
        return player.is_alive()
