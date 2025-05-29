from managers import RoomManager
from core import PoolType
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
        return (self.stage-1)*5 + (self.room)//2
    
    def start_game(self):
        display.game_title()
        display.H2(f"STAGE {self.stage} START")
        while self.player.is_alive:
            self._game_flow()

    def _game_flow(self):
        # Main game loop
        # Получение вариантов комнат
        room_options = self.room_manager.get_room_options(
            current_stage=self.stage,
            difficulty=self.difficulty
        )
        
        # Отображение выбора комнат
        chosen_room = self._choose_room(room_options)
        
        # Обработка выбранной комнаты
        chosen_room.enter()
        
        # Проверка на босса
        if self.room == 10:
            self._handle_boss_room()
            if not self.player.is_alive:
                return
            self._handle_modification_room()
            self._next_stage()
        else:
            self.room += 1
            self.total_rooms += 1
    
    def _choose_room(self, room_options: list):
        options = []
        for room_option in room_options:
            room = room_option.room
            room_type = room_option.type
            if room_type is PoolType.EVENT:
                options += ["Event"]
            elif room_type is PoolType.CHEST:
                options += ["Chest"]
            else:
                options += [str(room.name)]
        print()
        selection = input.select_from_list(options=options, title=f"Room {self.room} options:", input_text="Select room: ", framed=True)
        return room_options[selection-1][0]
    
    def _handle_boss_room(self):
        self.room_manager.boss_battle(self.stage, self.difficulty)
    
    def _handle_modification_room(self):
        self.room_manager.modification_menu()
    
    def _next_stage(self):
        self.stage += 1
        self.room = 1
        display.H2(f"STAGE {self.stage} START")
        self._apply_stage_modifiers()
    
    def _apply_stage_modifiers(self):
        # Увеличение сложности для нового этапа
        self.player.max_health += 5 * self.stage
        self.player.heal(20)
        print(f"Max health increased to {self.player.max_health}")