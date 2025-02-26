import random
import enum
from rune import Runes
import effect
from color import Fore, Back, Style
from signal import Signal
from artifact import Artifacts
from entity import Player, Enemy
from game import Game

# Usage
player = Player()
game = Game(player)
game.play()