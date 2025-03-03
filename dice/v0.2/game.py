import random
from room import Room, BossRoom, CombatRoom
from color import Back, Style

class Game:
    def __init__(self, player):
        self.player = player
        self.completed_rooms = 0
    
    @property
    def difficulty(self):
        return self.completed_rooms // 5

    def set_player_defaults(self):
        self.player.shield = 0
        self.player.effects = []

    def generate_room_options(self):
        if self.completed_rooms >= 50:
            return [BossRoom(int(self.difficulty*1.5))]
        
        room_types = []
        weights = [4, 1, 3, 5, 1]  # Enemy, Chest, Shop, Event, Workshop
        for _ in range(2):
            rt = random.choices(['enemy', 'chest', 'shop', 'event', 'workshop'], weights, k=1)[0]
            room_types.append(rt)
        return [Room.create(rt, self.difficulty) for rt in room_types]

    def play(self):
        while self.player.is_alive():
            options = self.generate_room_options()
            while True:
                try:
                    print(f"\n=== Прогресс: {self.completed_rooms}/50 комнат ===")
                    
                    print("\nКомнаты:")
                    for i, room in enumerate(options):
                        print(f"{i+1}. {room.description}")
            
            
                    choice = int(input("Введите выбор: ")) - 1
                    if choice < 0:
                        choice = ""
                    selected_room = options[choice]
                    break
                except:
                    print("Неправильный выбор!")
            success = selected_room.enter(self.player)
            
            if self.completed_rooms >= 50:
                if self.player.is_alive():
                    print(f"\n{Back(22)}=== ПОЗДРАВЛЯЕМ! Вы победили последнего босса! ==={Style.RESET_ALL}")
                break
            
            if not success:
                print(f"\n{Back(52)}=== ПОРАЖЕНИЕ ==={Style.RESET_ALL}")
                return
            
            self.completed_rooms += 1
            self.set_player_defaults()
