import random
from rune import Runes


class Die:
    def __init__(self, sides, runes, upgrades=0, enchantment=None):
        self.base_sides = sides
        self.runes = runes
        self.upgrades = upgrades
        self.enchantment = enchantment
        self.current_value = 1
        self.current_rune = runes[0]
    
    @property
    def sides(self):
        return self.base_sides + self.upgrades
    
    def roll(self):
        self.current_value = random.randint(1, self.base_sides)
        self.current_rune = self.runes[self.current_value - 1]
        return self.current_value + self.upgrades, self.current_rune
    
    def upgrade(self):
        self.upgrades += 1
        
    def mutate(self, new_sides):
        self.base_sides = new_sides
        # Fill new faces with default attack runes
        while len(self.runes) < new_sides:
            self.runes.append(Runes.empty.value)
            
    def enchant(self, enchantment):
        self.enchantment = enchantment
        
    def replace_rune(self, face_id, new_rune):
        if 0 <= face_id < len(self.runes):
            old_rune = self.runes[face_id]
            self.runes[face_id] = new_rune
            return old_rune
    
    def remove_rune(self, face_id):
        if 0 <= face_id < len(self.runes):
            rune = self.runes[face_id]
            self.runes[face_id] = Runes.empty.value
            return rune

    def __repr__(self):
        return f"d{self.base_sides}{f"+{self.upgrades}" if self.upgrades else ""}"
