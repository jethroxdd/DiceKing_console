class Entity:
    def __init__(self, name, health, dice):
        self.name = name
        self.max_health = health
        self.health = health
        self.dice = dice
        
        self.gold = 0
        self.max_shield = 10
        self.shield = 0
        self.target = None
        self.effects = []
    
    @property
    def is_dead(self):
        return self.health <= 0
    
    def take_damage(self, damage):
        actual = max(0, damage - self.shield)
        self.shield = max(0, self.shield - damage)
        self.health = max(0, self.health - actual)
        
    def take_true_damage(self, damage):
        self.health = max(0, self.health - damage)
    
    def take_heal(self, heal):
        self.health = min(self.max_health, self.health + heal)
    
    def take_shield(self, shield):
        self.shield = min(self.max_shield, self.shield + shield)

    def set_target(self, target):
        self.target = target
    
    def end_round_cleanup(self):
        # Tick shield
        self.shield = max(0, self.shield - 1)
        
    def process_effects(self):
        # Tick effects and remove ended effects
        for e in self.effects:
            e.tick()
            if e.is_ended:
                self.effects.remove(e)
    
    def add_effect(self, effect):
        for e in self.effects:
            if e.name == effect.name:
                e.add(effect)
                return
        self.effects.append(effect)
    
    def apply_effects(self):
        for i in [0, 1]:
            for e in self.effects:
                if e.order == i:
                    e.apply(self)
    
    def __str__(self):
        return f"{self.name} {self.health}|{self.shield}\nEffects: {", ".join([e for e in self.effects])}\nAvailible dice:\n{"\n".join([f"{str(die)}:{', '.join([str(r) for r in die.runes])}" for die in self.dice])}"