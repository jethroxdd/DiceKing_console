from classes.die import Die
from random import randint
class SimpleDie(Die):
    def __init__(self, sides, runes=None, upgrades=None):
        super().__init__("simple", sides, runes, upgrades)
    
    def roll(self):
        value = randint(0, self.sides-1)
        rune = self.runes[value]
        return rune, value + 1 + self.upgrades