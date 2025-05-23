from managers import GameManager
from core.artifact.types import BloodTome
from core.entity import Player
from core.die.types import Simple
from core.rune.types import Attack, Fire, Shield, Empty, Crit, Mirror, Heal, Rage
from utils import Value

player = Player(
    50, 
    [
        Simple(6, [Attack()]*6), 
        Simple(6, [Shield()]*6)
        ]
    )
gm = GameManager(player)
gm.start_game()
