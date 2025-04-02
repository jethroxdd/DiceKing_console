from classes.entity import Entity
class Enemy(Entity):
    def __init__(self, health, dice):
        super().__init__("Enemy", health, dice)
        self.gold = 10