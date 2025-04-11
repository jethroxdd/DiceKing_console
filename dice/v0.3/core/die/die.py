from core.rune.types import Empty

class Die:
    def __init__(self, name, sides: int, runes=None, upgrades=None):
        self.name = name
        self.sides = sides
        self.runes = [Empty()]*sides
        self.init_runes(runes)
        self.upgrades = upgrades or 0    
    
    def init_runes(self, runes):
        runes = runes or []
        for i, rune in enumerate(runes):
            self.runes[i] = rune

    def attach_rune(self, rune, face_id):
        old_rune = self.runes[face_id]
        self.runes[face_id] = rune
        return old_rune

    def remove_rune(self, face_id):
        old_rune = self.runes[face_id]
        self.runes[face_id] = Empty()
        return old_rune
    
    def upgrade(self):
        self.upgrades += 1
    
    def str_all(self):
        '''<type> <sides><upgrades>: <runes>'''
        return f"{self.name} d{self.sides}{"+" if self.upgrades > 0 else ""}{self.upgrades if self.upgrades != 0 else ""}: {', '.join([str(r) for r in self.runes])}"
    
    def __str__(self):
        '''<type> <sides><upgrades>'''
        return f"{self.name} d{self.sides}{"+" if self.upgrades > 0 else ""}{self.upgrades if self.upgrades != 0 else ""}"