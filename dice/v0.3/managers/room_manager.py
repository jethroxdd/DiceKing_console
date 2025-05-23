from random import choice
from core.room.types import STANDARD_POOL, EVENT_POOL, CHEST_POOL, Battle, ModificationRoom, Boss
from core.entity.enemy import ENEMY_POOL
import enum

# Generate rooms to choose from
# Enter room

class RoomPools:
    types = ["standard", "event", "chest"]
    standard = STANDARD_POOL
    event = EVENT_POOL
    chest = CHEST_POOL

class EnemyPools:
    stage = ENEMY_POOL

class RoomManager:
    def __init__(self, player):
        self.player = player
    
    def get_room_options(self, current_stage, current_room, difficulty):
        options = []
        for _ in range(3):
            enemy = choice(EnemyPools.stage[current_stage-1])(difficulty)
            room_type = choice(RoomPools.types)
            room = choice(getattr(RoomPools, room_type))(self.player, difficulty, enemy=enemy)
            options += [[room, room_type]]
        return options
    
    def boss_battle(self, current_stage, difficulty):
        room = Boss(self.player, difficulty)
        room.enter()
    
    def modification_menu(self):
        mod_room = ModificationRoom(self.player, 1)
        mod_room.enter()