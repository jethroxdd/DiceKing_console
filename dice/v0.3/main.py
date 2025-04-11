import ui
from core.die.types import SimpleDie
from core.rune.types import Attack, Shield, Fire, Empty, Crit
from core.entity import Player, Enemy
from managers import CombatManager, ModificationManager
from core.room.types import Battle

player = Player(
    100, 
    [
        SimpleDie(4, [Attack()]*3 + [Fire()]), 
        SimpleDie(4, [Shield()]*4), 
        SimpleDie(4, [Empty()]*3 + [Crit()])
        ]
    )
player.runes = [Attack()]*3 + [Shield()]*3 + [Fire()]
mm = ModificationManager(player)
mm.start_session(player.dice[0])
# room = Battle(player, 1)
# room.enter()