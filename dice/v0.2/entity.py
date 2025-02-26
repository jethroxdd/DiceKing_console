from signal import EntitySignal
from die import Die
from rune import Runes

class Entity:
    def __init__(self, health):
        self.target = None
        self.max_health = health
        self.health = health
        self.shield = 0
        self.effects = []
        self.roll_results = []
        self.dice = []
        
        self.signal_shield_broke = EntitySignal(self)
        self.signal_self_damage = EntitySignal(self)
    
    def set_target(self, entity):
        self.target = entity
    
    def add_effect(self, effect):
        for e in self.effects:
            if e.name == effect.name:
                e.add(effect)
                break
        else:
            self.effects.append(effect)
        
    def tick(self):
        decayed_effect_ids = []
        for i in range(len(self.effects)):
            self.effects[i].tick()
            if self.effects[i].is_ended:
                decayed_effect_ids.append(i)
        for i in decayed_effect_ids[::-1]:
            del self.effects[i]
        self.shield = max(self.shield - 1, 0)
        self.crit = False
        self.roll_results = []
            
    def is_alive(self):
        return self.health > 0
    
    def apply_effects(self, is_good):
        for order in range(5):
            for effect in self.effects:
                if is_good == effect.is_good and order == effect.order:
                    effect.apply(self)
    
    def take_damage(self, damage):
        actual = max(damage - self.shield, 0)
        if damage != 0 and self.shield != 0:
            self.signal_shield_broke.emit()
        self.shield = max(self.shield - damage, 0)
        self.health -= actual
        return actual

    def take_true_damage(self, damage):
        self.health -= damage
        return damage

    def take_heal(self, amount):
        self.health = min(self.health + amount, self.max_health)

class Player(Entity):
    def __init__(self):
        super().__init__(30)
        self.dice = [
            Die(4, [Runes.attack.value]*4),
            Die(4, [Runes.shield.value]*4)
        ]
        self.runes = []
        self.artifacts = []
        self.gold = 0
        self.max_dice = 8
        self.max_runes = 5
        self.max_rerolls = 1
        self.rerolls = self.max_rerolls

    def add_die(self, die):
        if len(self.dice) < self.max_dice:
            self.dice.append(die)
            return True
        return False

    def add_rune(self, rune):
        if len(self.runes) < self.max_runes:
            self.runes.append(rune)
            return True
        return False

    def add_artifact(self, artifact):
        if not self.has_artifact(artifact):
            self.artifacts.append(artifact)
            artifact.apply(self)
            return
        else:
            print(f"Can't hold another {artifact.name} artifact")
    
    def has_artifact(self, artifact):
        for a in self.artifacts:
            if a.name == artifact.name:
                return True
        return False

class Enemy(Entity):
    def __init__(self, difficulty, name="Enemy", base_health=8, mult_health=4):
        super().__init__(base_health + difficulty * mult_health)
        self.name = name


class Rat(Enemy):
    def __init__(self, difficulty):
        super().__init__(difficulty, "Rat")
        self.dice = [
            Die(4, [Runes.poison.value]*1 + [Runes.attack.value]*3)
        ]

def get_random_rune():
    pass

def get_random_rune_list_max_cost(cost):
    pass
    