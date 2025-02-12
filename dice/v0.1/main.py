import random
import dices
from entity import Entity
from systems import RoundSystem
import copy
import enemies

dices = copy.deepcopy(random.sample(dices.ALL, 6))

player = Entity("Player", 100, copy.deepcopy(dices))
# enemy = Entity("Enemy", 20, copy.deepcopy(dices))
enemy = copy.deepcopy(enemies.rat)
player.setTarget(enemy)
enemy.setTarget(player)

game = RoundSystem(player, enemy)
game.start()