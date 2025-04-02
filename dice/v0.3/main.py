import UI
from classes.die.types import SimpleDie
from classes.rune.types import Attack, Shield, Fire
from classes.entity import Player, Enemy
from managers import CombatManager, ModManager
from classes.room.types import Battle

player = Player(100, [SimpleDie(4, [Fire()]*4), SimpleDie(4, [Shield()]*4)])

room = Battle(player, 1)
room.enter()