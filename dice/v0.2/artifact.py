import enum
from effect import EffectType

class BaseArtifact:
    def __init__(self, name, description, rarity):
        self.name = name
        self.description = description
        self.rarity = rarity

class MagicCharm(BaseArtifact):
    def __init__(self):
        super().__init__("Магическая сфера", "Дает +1 рерол", 4)
    
    def apply(self, player):
        player.max_rerolls += 1

class ThornShield(BaseArtifact):
    def __init__(self):
        super().__init__("Осколочный щит", "Наносит 1 урон за каждые 3 сломаных щита", 2)
    
    @staticmethod
    def effect(*args):
        source = args[0]
        shield = source.shield
        damage = shield//3
        if damage:
            source.target.take_damage(damage)
    
    def apply(self, player):
        player.signal_shield_broke.add(self.effect)

class MasochistsWhip(BaseArtifact):
    def __init__(self):
        super().__init__("Пояс терпимости", "Самоурон теперь наносит чистый урон и дает X щита", 1)
    
    @staticmethod
    def effect(*args):
        source = args[0]
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