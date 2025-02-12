from side import Side
from dice import BaseDice, BasicDice, LoopDice
import effects
import sides    

tamplateDice = BaseDice(
    name="Tamplate name", 
    description = "Tamplate description",
    sides=[
        Side("template", None, sides.Pass), 
        Side("template", None, sides.Pass)], 
    baseCooldown=2)

attack_d4 = BasicDice(
    name="Light attack (d4)",
    description = "Deals small amount of damage",
    Type="attack", 
    number=4,
    roll=sides.Attack,
    baseCooldown=1)

attack_d8 = BasicDice(
    name="Heavy attack (d8)", 
    description = "Deals some amount of damage",
    Type="attack", 
    number=8,
    roll=sides.Attack,
    baseCooldown=2)

defense_d4 = BasicDice(
    name="Light defense (d4)", 
    description = "Gives small amount of shield",
    Type="deffense", 
    number=4,
    roll=sides.Defense,
    baseCooldown=1)

defense_d8 = BasicDice(
    name="Heavy defense (d8)", 
    description = "Gives some amount of shield",
    Type="deffense", 
    number=8,
    roll=sides.Defense,
    baseCooldown=2)

coin_d2 = BaseDice(
    name="Lucky coin", 
    description = "Doubles dealing damage if heads, or incoming damage if tails",
    sides=[
        sides.Coin("heads"), 
        sides.Coin("tails")], 
    baseCooldown=2)

heal_d4 = BaseDice(
    name="Small heal (d4)", 
    description = "Instant heal",
    sides=[
        sides.Effect(effects.Heal(1), True), 
        sides.Effect(effects.Heal(2), True),
        sides.Effect(effects.Heal(3), True),
        sides.Effect(effects.Heal(4), True)], 
    baseCooldown=2)

regen_d4 = BaseDice(
    name="Regen dice (d4)", 
    description = "Receive regeneration, heal for each stack, evere round decrease",
    sides=[
        sides.Effect(effects.Regen(1), True), 
        sides.Effect(effects.Regen(2), True), 
        sides.Effect(effects.Regen(3), True), 
        sides.Effect(effects.Regen(4), True)], 
    baseCooldown=3)

crit_d4 = BaseDice(
    name="Crit dice (d4)", 
    description = "Doubles numbers of other dices",
    sides=[
        sides.Pass(),
        sides.Pass(),
        sides.Pass(),
        sides.Crit()], 
    baseCooldown=2)

attackLoop_d4 = LoopDice(
    name="Loop attack (d4)", 
    description = "Stack damage until stop roll",
    sides=[
        sides.Attack(1),
        sides.Attack(2),
        sides.Attack(3),
        sides.Stop()],
    baseCooldown=2)

defenceLoop_d4 = LoopDice(
    name="Loop defense (d4)",
    description = "Stack deffense until stop roll",
    sides=[
        sides.Defense(1), 
        sides.Defense(2), 
        sides.Defense(3), 
        sides.Stop()], 
    baseCooldown=2)

dagger_d4 = BaseDice(
    name="Bleed dagger (d4)", 
    description = "Applies bleed on enemie",
    sides=[
        sides.Effect(effects.Bleed(1), False), 
        sides.Effect(effects.Bleed(2), False), 
        sides.Effect(effects.Bleed(3), False), 
        sides.Effect(effects.Bleed(4), False), ], 
    baseCooldown=2)

skull_d8 = BaseDice(
    name="Skull dice (d8)", 
    description = "Every side deal 5 damage, one side receive 10 damage",
    sides=[
        sides.Attack(5), 
        sides.Attack(5), 
        sides.Attack(5), 
        sides.Attack(5), 
        sides.Attack(5), 
        sides.Attack(5), 
        sides.Attack(5), 
        sides.Effect(effects.Harm(10), True)], 
    baseCooldown=1)

DIce_d6 = BaseDice(
    name="D-ice (d4)",
    description="Deal damage and slowness(1) to the enemy",
    sides=[
        sides.ColdAttack(1),
        sides.ColdAttack(2),
        sides.ColdAttack(3),
        sides.ColdAttack(4),
        sides.ColdAttack(5),
        sides.ColdAttack(6),],
    baseCooldown = 2)

ratsClaw_d6 = BaseDice(
    name="Rats claw",
    description="Clow from defeated rat, applies poison",
    sides=[
        sides.Attack(1),
        sides.Attack(2),
        sides.Attack(3),
        sides.Attack(4),
        sides.Effect(effects.Bleed(3), False),
        sides.Effect(effects.Bleed(3), False)],
    baseCooldown = 1)

beeSting_d4 = BaseDice(
    name = "Bee sting",
    description = "Deals poison and attack damage",
    sides=[
        sides.Effect(effects.Poison(1), False),
        sides.Effect(effects.Poison(2), False),
        sides.Effect(effects.Poison(3), False),
        sides.Effect(effects.Poison(4), False),],
    baseCooldown = 2)

fireDice_d10 = BaseDice(
    name = "Fire Dice",
    description = "Deals damage and applies burn",
    sides=[
        sides.FireAttack(1, 4),
        sides.FireAttack(2, 4),
        sides.FireAttack(3, 4),
        sides.FireAttack(4, 4),
        sides.FireAttack(5, 4),
        sides.FireAttack(6, 4),
        sides.FireAttack(7, 4),
        sides.FireAttack(8, 4),
        sides.FireAttack(9, 4),
        sides.FireAttack(10, 4)],
    baseCooldown = 1)

lightningDice_d10 = BaseDice(
    name = "Lightning Dice",
    description = "Deals damage and stuns enemie",
    sides=[
        sides.LightningAttack(1),
        sides.LightningAttack(2),
        sides.LightningAttack(3),
        sides.LightningAttack(4),
        sides.LightningAttack(5),
        sides.LightningAttack(6),
        sides.LightningAttack(7),
        sides.LightningAttack(8),
        sides.LightningAttack(9),
        sides.LightningAttack(10),],
    baseCooldown = 3)

sword_d6 = BaseDice(
    name="Sword Dice",
    description="Steel sword",
    sides=[
        Side("attack", 2, sides.Attack),
        Side("attack", 2, sides.Attack),
        Side("attack", 3, sides.Attack),
        Side("attack", 4, sides.Attack),
        Side("attack", 5, sides.Attack),
        Side("attack", 5, sides.Attack),],
    baseCooldown = 1)

vampireDice_d8 = BaseDice(
    name="Vampire dice", 
    description = "Heals for 50% of damage dealt",
    sides=[
        Side("vampire-attack", 1, sides.VampireAttack),
        Side("vampire-attack", 2, sides.VampireAttack),
        Side("vampire-attack", 3, sides.VampireAttack),
        Side("vampire-attack", 4, sides.VampireAttack),
        Side("vampire-attack", 5, sides.VampireAttack),
        Side("vampire-attack", 6, sides.VampireAttack),
        Side("vampire-attack", 7, sides.VampireAttack),
        Side("vampire-attack", 8, sides.VampireAttack),], 
    baseCooldown=3)

poisonFlaskDice_d8 = BaseDice(
    name="Poison flask dice", 
    description = "Applies poison effect",
    sides=[
        sides.Effect(effects.Poison(1), False), 
        sides.Effect(effects.Poison(2), False), 
        sides.Effect(effects.Poison(3), False), 
        sides.Effect(effects.Poison(4), False), 
        sides.Effect(effects.Poison(5), False), 
        sides.Effect(effects.Poison(6), False), 
        sides.Effect(effects.Poison(7), False), 
        sides.Effect(effects.Poison(8), False), ], 
    baseCooldown=2)

goldStealler_d6 = BaseDice(
    name="Gold stealler", 
    description = "Steals gold based on side",
    sides=[
        sides.GoldStealler(1)
        sides.GoldStealler(2)
        sides.GoldStealler(3)
        sides.GoldStealler(4)
        sides.GoldStealler(5)
        sides.GoldStealler(6)], 
    baseCooldown=2)

base = (attack_d4, attack_d8, defense_d4, defense_d8)
ALL = (attack_d4, attack_d8, defense_d4, defense_d8, crit_d4, heal_d4, coin_d2, regen_d4, attackLoop_d4, defenceLoop_d4, dagger_d4, skull_d8, DIce_d6, fireDice_d10, sword_d6)
special = (ratsClaw_d6, beeSting_d4)