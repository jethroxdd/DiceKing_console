from managers import GameManager
from core.artifact.types import BloodTome
from core.entity import Player
from core.die.types import Simple
import core.rune.types as RuneTypes
from utils import Value

player = Player(
    50, 
    [
        Simple(6, [RuneTypes.Attack()]*4 + [RuneTypes.Empty()]*2), 
        Simple(6, [RuneTypes.Shield()]*4 + [RuneTypes.Empty()]*2),
        ]
    )
gm = GameManager(player)
gm.start_game()
