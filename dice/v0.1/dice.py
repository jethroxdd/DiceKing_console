import random
from side import Side
class BaseDice:
    # Base class for all dices
    def __init__(self, name: str, description: str, sides: list, baseCooldown: int):
        self.name = name
        self.description = description
        self.number = len(sides) + 1
        self.sides = sides
        self.cooldown = 0
        self.baseCooldown = baseCooldown
    
    def roll(self, entity):
        random.choice(self.sides).roll(entity)

class BasicDice(BaseDice):
    Type: str
    def __init__(self, name: str, description: str, Type: str, number: int, roll, baseCooldown: int):
        super().__init__(name, description, [], baseCooldown)
        self.number = number
        self.generateSides(Type, number, roll)
    
    def generateSides(self, Type: str, number: int, roll):
        for i in range(number):
            self.sides.append(Side(Type, i+1, roll))

class LoopDice(BaseDice):
    def __init__(self, name: str, description: str, sides: list, baseCooldown: int, stopValue="stop"):
        super().__init__(name, description, sides, baseCooldown)
        self.stopValue = stopValue
    
    def roll(self, entity):
        result = random.choice(self.sides).roll(entity)
        while result != self.stopValue:
            result = random.choice(self.sides).roll(entity)