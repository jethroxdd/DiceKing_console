from random import choice
import core.room.types as RoomTypes
import core.entity.enemy as EnemyTypes
import enum

# Generate rooms to choose from
# Enter room

class RoomPools:
    types = ["standard", "event", "chest"]
    standard = [RoomTypes.Battle, RoomTypes.Shop]
    event = []
    chest = []

class EnemyPools:
    stage = [
        [EnemyTypes.Rat, EnemyTypes.Slime],
        [EnemyTypes.Rat, EnemyTypes.Slime],
        [EnemyTypes.Rat],
        [EnemyTypes.Rat],
        [EnemyTypes.Rat]
    ]

class RoomManager:
    def __init__(self, player):
        self.player = player
    
    def get_room_options(self, current_stage, current_room, difficulty):
        options = []
        for _ in range(3):
            enemy = choice(EnemyPools.stage[current_stage-1])(difficulty)
            # room_type = choice(RoomPools.types)
            room_type = "standard"
            room = choice(getattr(RoomPools, room_type))(self.player, difficulty, enemy=enemy)
            options += [room]
        return options
    
    def boss_battle(self, current_stage):
        room = RoomTypes.Battle(self.player, current_stage+5, enemy=EnemyTypes.Rat(current_stage+5))
        room.enter
    
    def modification_menu(self):
        pass