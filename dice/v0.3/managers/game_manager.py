class GameManager:
    def __init__(self, player):
        self.player = player
        self.room = 1
        self.stage = 1
    
    @property
    def difficulty(self):
        return (self.stage-1)*5 + (self.room-1)//2