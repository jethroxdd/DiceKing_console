import random
from enum import Enum
from typing import List, NamedTuple
from core.room.types import ROOM_POOLS, ModificationRoom, BossBattle
from core.entity.enemy import ENEMY_POOL
from core import PoolType

class RoomType(Enum):
    """Enum representing valid room types."""
    STANDARD = PoolType.STANDARD
    BATTLE = PoolType.BATTLE
    EVENT = PoolType.EVENT
    CHEST = PoolType.CHEST

class RoomOption(NamedTuple):
    """Data structure representing a room choice with metadata."""
    room: object
    type: str  # Using string value for backward compatibility

class RoomManager:
    """Manages room generation and special room interactions."""
    # Weighted room type configuration (Standard: 6, Event: 3, Chest: 1)
    ROOM_TYPE_CHOICES = [RoomType.STANDARD, RoomType.BATTLE, RoomType.EVENT, RoomType.CHEST]
    ROOM_TYPE_WEIGHTS = [2, 10, 3, 1]
    
    def __init__(self, player):
        self.player = player
    
    def get_room_options(self, current_stage: int, difficulty: int, n=3) -> List[RoomOption]:
        """Generate three weighted random room options for player selection."""
        # Select three room types using weighted probabilities
        chosen_types = random.choices(
            self.ROOM_TYPE_CHOICES, 
            weights=self.ROOM_TYPE_WEIGHTS, 
            k=n
        )
        
        options = []
        for room_type_enum in chosen_types:            
            room_type_value = room_type_enum.value
            room = self._create_room(room_type_value, difficulty)
            options.append(RoomOption(room, room_type_value))
        
        return options
    
    def boss_battle(self, current_stage: int, difficulty: int) -> None:
        """Initiate a boss battle room."""
        BossBattle(self.player, difficulty).enter()
    
    def modification_menu(self) -> None:
        """Open the modification menu room."""
        ModificationRoom(self.player, 1).enter()
    
    def _create_room(self, room_type: RoomType, difficulty: int) -> object:
        """Instantiate a room of specified type with generated enemy."""
        room_class = random.choice(ROOM_POOLS[room_type])
        return room_class(self.player, difficulty)