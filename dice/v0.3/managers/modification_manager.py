import UI
from UI import Paint, msg
from enum import Enum

class ModManager:
    '''
    Insert runes in die
    Take off runes from die
    Replace rune in die
    Upgrade die
    Upgrade rune
    Sell rune
    Sell die
    Craft rune
    Transmure runes (3 runes -> 1 rune better rarity)
    '''
    def __init__(self, player):
        self.player = player
    
    def attach_rune(self, die):
        while True:
            try:
                UI.print_availible_runes(self.player)
                print(die.print_all())
                rune_id = int(input(Paint("Which rune? ", 220))) - 1
                face_id = int(input(Paint(f"Which side (1-{die.sides})? ", 220))) - 1
                
                if 0 <= face_id < die.sides and 0 <= rune_id < len(self.player.runes):
                    new_rune = self.player.runes[rune_id]
                    old_rune = die.attach_rune(self.player.runes[rune_id], face_id)
                    del self.player.runes[rune_id]
                    if old_rune.name != "empty":
                        self.player.runes.append(old_rune)
                        print(f"Replaced {old_rune} to {new_rune} on {face_id+1} side!")
                        return
                    else:
                        print(f"Attached {new_rune} to {face_id+1} side!")
                        return
                else:
                    raise Exception()
            except:
                print(Paint("Incorrect input!", 88))
                
    def remove_rune(self, die):
        while True:
            try:
                print(die.print_all())
                face_id = int(input(Paint(f"Which side (1-{die.sides})? ", 220))) - 1
                if 0 <= face_id <= die.sides:
                    print("#0")
                    rune = die.remove_rune(face_id)
                    print("#01")
                    if rune.name != "empty":
                        print("#1")
                        print(f"Removed {rune} from {face_id+1} side")
                        self.player.runes.append(rune)
                        return
                    else:
                        print("#2")
                        print(f"Can't remove from empty side")
                        return
            except:
                print(Paint("Incorrect input!", 88))
    