class BaseArtifact:
    def __init__(self, player, name, description):
        self.player = player
        self.name = name
        self.description = description
    
    def __str__(self):
        return f"{self.name} - {self.description}"