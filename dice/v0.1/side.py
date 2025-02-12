class Side:
    def __init__(self, Type: str, value, apply, runes = []):
        '''
        roll - function that activates when side rolls
        roll = roll(Side, Entity)
        '''
        self.Type = Type
        self.value = value
        self.apply = apply
        self.runes = runes
    
    def roll(self, entity):
        self.apply(self, entity)
        return self.value