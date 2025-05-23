import random
from room import Room, BossRoom, CombatRoom

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
                    print("\n=== ПОЗДРАВЛЯЕМ! Вы победили последнего босса! ===")
                break
            
            if not success:
                print("\n=== ПОРАЖЕНИЕ ===")
                return
            
            if isinstance(selected_room, CombatRoom):
                self.player.gold += random.randint(int(10*(self.difficulty**(0.5))), int(20*(self.difficulty)**(0.5)))
                print(f"\nВы заработали {self.player.gold} золота всего!") 
                self.difficulty += 1
            
            self.completed_rooms += 1
            self.player.health = min(self.player.health + 2, self.player.max_health)
