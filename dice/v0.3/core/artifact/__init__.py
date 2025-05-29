from core import RarityType

class BaseArtifact:
    rarity = RarityType.COMMON
    cost = 0
    name = "Base Artifact"
    description = "Base Artifact"
    
    def __init__(self, player):
        self.player = player
    
    def apply(self):
        pass
    
    def stack(self):
        pass
    
    def __str__(self):
        return f"{self.name} - {self.description}"