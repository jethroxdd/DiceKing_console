import enum
from effect import EffectType

class BaseArtifact:
    def __init__(self, name, description, rarity):
        self.name = name
        self.description = description
        self.rarity = rarity

class MagicCharm(BaseArtifact):
    def __init__(self):
        super().__init__("Magic Charm", "Gain +1 max reroll", 4)
    
    def apply(self, player):
        player.max_rerolls += 1

class ThornShield(BaseArtifact):
    def __init__(self):
        super().__init__("Glass Shield", "Deal 1 damage to enemy for each 3 broken shield", 2)
    
    @staticmethod
    def effect(source):
        shield = source.shield
        damage = shield//3
        if damage:
            source.target.take_damage(damage)
    
    def apply(self, player):
        player.signal_shield_broke.add(self.effect)

class MasochistsWhip(BaseArtifact):
    def __init__(self):
        super().__init__("Masochist's whip", "Self damage now deal true damage and gives X shield", 1)
    
    @staticmethod
    def effect(source):
        effect = None
        for e in source.effects:
            if e.name == EffectType.self_damage.name:
                effect = e
                break
        if effect == None:
            return
        source.take_true_damage(effect.value)
        source.shield += effect.value
        del source.effects[source.effects.index(effect)]
    
    def apply(self, player):
        player.signal_self_damage.add(self.effect)

class Artifacts(enum.Enum):
    magic_charm = MagicCharm()
    thorn_shield = ThornShield()
    masochists_whip = MasochistsWhip()