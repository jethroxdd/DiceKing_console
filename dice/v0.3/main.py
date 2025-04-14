from managers import GameManager
from core.entity import Player
from core.die.types import Simple
from core.rune.types import Attack, Fire, Shield, Empty,Crit

player = Player(
    50, 
    [
        Simple(6, [Attack()]*6), 
        Simple(6, [Shield()]*6)
        ]
    )
player.gold = 1000
gm = GameManager(player)
gm.start_game()
