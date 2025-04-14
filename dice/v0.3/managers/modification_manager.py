from enum import Enum
from ui import display
from ui import select_from_list, get_valid_input

class ModificationType(Enum):
    ATTACH = 1
    REMOVE = 2
    UPGRADE_DIE = 3
    EXIT = 0

class ModificationResult(Enum):
    SUCCESS = 1
    FAILURE = 2
    EXIT = 3

class ModificationManager:
    BASE_UPGRADE_COST = 25

    def __init__(self, player):
        self.player = player
        self.current_session = None

    class ModificationSession:
        def __init__(self, die=None):
            self.die = die

    def start_session(self, die=None):
        self.current_session = self.ModificationSession(die)
        return self._main_menu()

    def _main_menu(self):
        options = [
            "Attach Rune",
            "Remove Rune",
            "Upgrade Die",
        ]
        
        while True:
            print()
            display.message(f"Player gold: {self.player.gold}")
            display.message(self.current_session.die.str_all())
            choice = select_from_list(options, "Modification Menu ('Enter' to exit): ", default=ModificationType.EXIT)
            choice = ModificationType(choice)
            match choice:
                case ModificationType.ATTACH:
                    self._attach_rune_flow()
                case ModificationType.REMOVE:
                    self._remove_rune_flow()
                case ModificationType.UPGRADE_DIE:
                    self._upgrade_die_flow()
                case ModificationResult.EXIT:
                    return ModificationResult.EXIT

    def _attach_rune_flow(self):
        print()
        rune_id = self._select_rune(self.player.runes)
        if rune_id == False:
            return ModificationResult.EXIT
        
        face = self._select_face(self.current_session.die)
        if face == False:
            return ModificationResult.EXIT

        rune = self.player.runes[rune_id-1]
        return self.attach_rune(self.current_session.die, rune, face-1)

    def attach_rune(self, die, rune, face_id: int):
        _rune = die.attach_rune(rune, face_id)
        if _rune.name == "empty":
            display.success(f"Attached {rune} rune to the {face_id+1} side")
        else:
            display.success(f"Replaced {_rune} with {rune} at {face_id+1} side")
            self.player.add_rune(_rune)
        return ModificationResult.SUCCESS
    
    def _remove_rune_flow(self):
        print()
        face = self._select_face(self.current_session.die)
        if face == False:
            return ModificationResult.EXIT
        
        return self.remove_rune(self.current_session.die, face-1)

    def remove_rune(self, die, face_id: int):
        _rune = die.remove_rune(face_id)
        if _rune.name == "empty":
            display.error("Cant remove rune frome empty side!")
            return ModificationResult.FAILURE
        self.player.add_rune(_rune)
        display.success(f"Removed {_rune} from {face_id+1} side.")
        return ModificationResult.SUCCESS
    
    def _upgrade_die_flow(self):
        die = self.current_session.die
        cost = (die.upgrades+1)*self.BASE_UPGRADE_COST
        display.message(f"{die} has {die.upgrades} upgrades. Next upgrade will cost {cost}.")
        if self.player.gold < cost:
            display.warning("Not enough money")
            return ModificationResult.FAILURE
        choice = get_valid_input(
            input_text="Upgrade die? (y/n): ",
            validation=lambda x: x in ['y', 'n']
        )
        if choice == 'y':
            self.player.gold -= cost
            die.upgrade()
            display.message("Succesfully upgraded die")
            return ModificationResult.SUCCESS

        return ModificationResult.EXIT

    def _select_rune(self, runes):
        options = [str(r) for r in runes]
        return select_from_list(options, "Availible runes: ", "Choose rune ('Enter' to exit): ", default=False)

    def _select_face(self, die):
        options = [str(r) for r in die.runes]
        return select_from_list(options, f"{die} faces:", "Choose face ('Enter' to exit): ", default=False)