class Entity:
    """
    Represents an entity in the game, such as a player or enemy.
    Manages health, dice, effects, and actions.
    """
    def __init__(self, name: str, health: int, dices: list):
        """
        Initializes the entity with health and a set of dice.
        
        :param health: Initial health of the entity.
        :param dices: List of dice available to the entity.
        """
        self.name = name
        self.health = health
        self.maxHealth = health
        self.isDead = False
        self.dices = list(dices)
        self.dicesChosen = []
        self.effects = []
        self.tempEffects = []
        self.maxDice = 3
        self.gold = 0
        
        self.stun = False
        self.coin = ""
        self.damage = 0
        self.defense = 0
        self.shield = 0
        self.isCrit = False
        self.critMult = 2.0
    
    def setTarget(self, target):
        self.target = target
    
    def shift(self):
        '''
        Changes of stats after round
        Shield decreasing every round
        '''
        self.shield -= 1
        self.shield = max(self.shield, 0)
        self.damage = 0
        self.defense = 0
        self.isCrit = False
        self.dicesChosen = []
        self.coin = ""
        for effect in self.effects:
            effect.shift()
            if effect.isEnded:
                self.effects.remove(effect)
                
    def dealDamage(self):
        if self.coin == "heads":
            self.damage *= 2
        return self.damage
    
    def takeDamage(self, damage: int):
        if self.coin == "tails":
            damage *= 2
        takenDamage = max(damage - self.shield, 0)
        self.shield = max(self.shield - damage, 0)
        self.health -= takenDamage
        self.isDead = self.health <= 0
        return 0
    

    def takeDirectDamage(self, damage: int):
        if self.coin == "tails":
            damage *= 2
        self.health -= damage
        self.isDead = self.health <= 0
    
    def takeHeal(self, value: int):
        self.health += value
        self.health = min(self.health, self.maxHealth)

    def printDicesList(self):
        # Print currently availible dices
        for i in range(len(self.dices)):
            dice = self.dices[i]
            if(dice.cooldown == 0):
                print(f"{i}) {dice.name}")
            else:
                print(f"{i}) {'*'*dice.cooldown}")
    
    def availibleDices(self):
        return [i for i in range(len(self.dices)) if (self.dices[i].cooldown == 0)]
            
    def diceCooldown(self):
        for dice in self.dices:
            if dice.cooldown > 0:
                dice.cooldown -= 1
    
    def rollDices(self):
        # Roll all chosen dices
        for dice_index in self.dicesChosen:
            # try:
            dice = self.dices[dice_index]
            if dice.cooldown != 0:
                continue
            else:
                self.rollDice(dice)
                dice.cooldown = dice.baseCooldown
            # except Exception:
            #     print(Exception)
        
        self.diceCooldown()
        self.apply()

    def rollDice(self, dice):
        dice.roll(self)

    def apply(self):
        # count all dices
        self.damage += self.damage*self.isCrit
        self.defense += self.defense*self.isCrit
        self.shield += self.defense
        for effect in self.tempEffects:
            if self.isCrit:
                effect.value *= 2
            self.addEffect(effect)
        self.tempEffects = []
    
    def addTempEffect(self, newEffect):
        for effect in self.tempEffects:
            if effect.name == newEffect.name:
                effect.add(newEffect)
                break
        else:
            self.tempEffects.append(newEffect)
    
    def addEffect(self, newEffect):
        for effect in self.effects:
            if effect.name == newEffect.name:
                effect.add(newEffect)
                break
        else:
            self.effects.append(newEffect)
        
    def applyGoodEffects(self):
        for effect in self.effects:
            if effect.isGood:
                effect.apply(self)
    
    def applyBadEffects(self):
        for effect in self.effects:
            if not effect.isGood:
                effect.apply(self)
    
    def isEffected(self, effectName: str):
        for effect in self.effects:
            if effect.name == effectName:
                return True
        else:
            return False