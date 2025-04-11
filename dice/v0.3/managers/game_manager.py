from managers import RoomManager


# Start the game
# Display 2-3 room choices
# Player selects the room
# Enter the room, if it is enemy encounter, start the battle
# Display next room choices
# On 10th room Boss
# After the Boss modification room
# Next stage

class GameManager:
    def __init__(self, player):
        self.player = player
        self.room = 1
        self.stage = 1
        self.room_manager = RoomManager(player)
    
    @property
    def difficulty(self):
        return (self.stage-1)*5 + (self.room-1)//2
    
    def _game_flow(self):
        
        pass