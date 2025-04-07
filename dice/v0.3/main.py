import ui
from core.die.types import SimpleDie
from core.rune.types import Attack, Shield, Fire, Empty, Crit
from core.entity import Player, Enemy
from managers import CombatManager, ModManager
from core.room.types import Battle

player = Player(
    100, 
    [
        SimpleDie(4, [Attack()]*3 + [Fire()]), 
        SimpleDie(4, [Shield()]*4), 
        SimpleDie(4, [Empty()]*3 + [Crit()])
        ]
    )

room = Battle(player, 1)
room.enter()