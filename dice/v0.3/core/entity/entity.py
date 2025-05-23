class Entity:
    def __init__(self, name, health, dice, max_shield=10, gold=0):
        self.name = name
        self.max_health = health
        self.health = health
        self.dice = dice
        
        self.gold = gold
        self.max_shield = max_shield
        self.shield = 0
        self.target = None
        self.effects = []
    
    @property
    def is_dead(self):
        """Returns True if the entity's health is 0 or below"""
        return self.health <= 0
    
    def take_damage(self, damage):
        """Apply damage through shields, returns actual damage taken"""
        actual = max(0, damage - self.shield)
        self.shield = max(0, self.shield - damage)
        self.health = max(0, self.health - actual)
        return actual
        
    def take_true_damage(self, damage):
        """Apply damage bypassing shields"""
        self.health = max(0, self.health - damage)
        return damage
    
    def take_self_damage(self, damage):
        """Apply damage through shields, returns actual damage taken"""
        actual = max(0, damage - self.shield)
        self.shield = max(0, self.shield - damage)
        self.health = max(0, self.health - actual)
        return actual
    
    def take_true_self_damage(self, damage):
        """Apply damage bypassing shields"""
        self.health = max(0, self.health - damage)
        return damage
    
    def take_heal(self, amount):
        """Restore health up to max health, returns actual healing done"""
        healed = min(amount, self.max_health - self.health)
        self.health += healed
        return healed
    
    def add_shield(self, amount):
        """Add shield up to max shield, returns actual shield added"""
        shield_added = min(amount, self.max_shield - self.shield)
        self.shield += shield_added
        return shield_added

    def set_target(self, target):
        """Set combat target"""
        self.target = target
    
    def end_round_cleanup(self):
        """Round-end maintenance"""
        # Tick shield
        self.shield = max(0, self.shield - 1)
        
    def process_effects(self):
        """Process effect durations and remove expired effects"""
        for e in self.effects:
            e.tick()
            if e.is_ended:
                self.effects.remove(e)
    
    def add_effect(self, effect):
        """Add new effect or stack with existing effect of same type"""
        for e in self.effects:
            if e.name == effect.name:
                e.stack(effect)
                return
        self.effects.append(effect)
    
    def apply_effects(self):
        """Apply effects in priority order"""
        for effect in sorted(self.effects, key=lambda e: e.order):
            effect.apply(self)
    
    def __str__(self):
        effects_list = ', '.join(str(e) for e in self.effects)
        dice_info = '\n'.join(
            f"{die}: {', '.join(str(r) for r in die.runes)}"
            for die in self.dice
        )
        return (
            f"{self.name} {self.health}|{self.shield}\n"
            f"Effects: {effects_list}\n"
            f"Available dice:\n{dice_info}"
        )