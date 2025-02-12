import dices
from entity import Entity
import copy

rat = Entity(
    name="Rat",
    health=20,
    dices=[
        dices.attack_d4,
        dices.defense_d4,
        dices.ratsClaw_d6])

goblin = Entity(
    name="Goblin",
    health=20,
    dices=[
        dices.attack_d4
    ]
)

beeHive = Entity(
    name="Bee Hive",
    health=20,
    dices=[
        dices.attack_d4,
        dices.defense_d4,
        dices.beeSting_d4])

boss = Entity(
    name="The Final Boss",
    health = 100,
    dices=copy.deepcopy(dices.ALL))

dragon = Entity("Dragon", 150, [
    copy.deepcopy(dices.fireDice_d10),
    copy.deepcopy(dices.lightningDice_d10)
])