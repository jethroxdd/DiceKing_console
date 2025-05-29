from enum import Enum, auto

class RarityType(Enum):
    COMMON = 5
    RARE = 3
    EPIC = 2
    LEGENDARY = 1

class PoolType(Enum):
    ALL = auto()
    STANDARD = auto()
    BATTLE = auto()
    EVENT = auto()
    CHEST = auto()
    SHOP = auto()
    BOSS = auto()

class ItemType(Enum):
    ARTIFACT = auto()
    RUNE = auto()
    DIE = auto()