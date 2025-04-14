from managers import RoomManager
from ui import display
from ui import input


# Start the game
# Display 2-3 room choices
# Player selects the room
# Enter the room (room.enter())
# Display next room choices
# On 10th room Boss
# After the Boss is modification room
# Next stage

class GameManager:
    def __init__(self, player):
        self.player = player
        self.room = 1
        self.stage = 1
        self.total_rooms = 1
        self.room_manager = RoomManager(player)
    
    @property
    def difficulty(self):
        return (self.stage)*5 + (self.room)//2
    
    def start_game(self):
        while self.player.is_alive:
            self._game_flow()

    def _game_flow(self):
         # Main game loop
        while self.room <= 10 and self.player.is_alive:
            # Получение вариантов комнат
            room_options = self.room_manager.get_room_options(
                current_stage=self.stage,
                current_room=self.room,
                difficulty=self.difficulty
            )
            
            # Отображение выбора комнат
            chosen_room = self._choose_room(room_options)
            
            # Обработка выбранной комнаты
            chosen_room.enter()
            
            # Проверка на босса
            if self.room == 10:
                self._handle_boss_room()
                self._handle_modification_room()
                self._next_stage()
            else:
                self.room += 1
                self.total_rooms += 1
    
    def _choose_room(self, room_options: list):
        options = []
        for i, k in enumerate(room_options):
            options.append(f"{i+1}. {k.name}")
        display.frame_text(text=options, title="Room options:", min_width=25)
        selection = input.get_valid_input(
            input_text="Choose room: ",
            validation=lambda x: 1 <= x <= len(options),
            transform=lambda x: int(x)
        )
        return room_options[selection-1]
    
    def _handle_boss_room(self):
        self.room_manager.boss_battle(self.stage)
    
    def _handle_modification_room(self):
        self.room_manager.modification_menu()
    
    def _next_stage(self):
        self.stage += 1
        self.room = 1
        print(f"\n=== STAGE {self.stage} START ===")
        self._apply_stage_modifiers()
    
    def _apply_stage_modifiers(self):
        # Увеличение сложности для нового этапа
        self.player.max_health += 5 * self.stage
        self.player.heal(20)
        print(f"Max health increased to {self.player.max_health}")