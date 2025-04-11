from enum import Enum
from ui import display_error, display_warning, display_success
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
    BASE_UPGRADE_COST = 50

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
        options = {
            "Attach Rune",
            "Remove Rune",
            "Upgrade Die",
        }
        
        while True:
            print(self.current_session.die.str_all())
            choice = select_from_list(options, "Modification Menu ('Enter' to exit): ", default=ModificationResult.EXIT)
            choice = ModificationType(choice)
            result = ModificationResult.SUCCESS
            match choice:
                case ModificationType.ATTACH:
                    result = self._attach_rune_flow()
                case ModificationType.REMOVE:
                    result = self._remove_rune_flow()
                case ModificationResult.EXIT:
                    return ModificationResult.EXIT
                # case ModificationType.UPGRADE_DIE:
                #     result = self._upgrade_die_flow()
                
            if result == ModificationResult.FAILURE:
                display_error("Something went wrong!")
                

    def _attach_rune_flow(self):
        rune_id = self._select_rune(self.player.runes)
        print(rune_id)
        if rune_id == None:
            return ModificationResult.EXIT
        
        face = self._select_face(self.current_session.die)
        if face == None:
            return ModificationResult.EXIT

        rune = self.player.runes[rune_id]
        return self.attach_rune(self.current_session.die, rune, face)

    def attach_rune(self, die, rune, face_id: int):
        _rune = die.attach_rune(rune, face_id)
        if _rune.name == "empty":
            display_success(f"Attached {rune} rune to the {face_id+1} side")
        else:
            display_success(f"Replaced {_rune} with {rune} at {face_id+1} side")
            self.player.add_rune(_rune)
        return ModificationResult.SUCCESS
    
    def _remove_rune_flow(self):
        face = self._select_face(self.current_session.die)
        if not face:
            return ModificationResult.EXIT
        
        return self.remove_rune(self.current_session.die, face)

    def remove_rune(self, die, face_id: int):
        _rune = die.remove_rune(face_id)
        if _rune.name == "empty":
            display_error("Cant remove rune frome empty side!")
            return ModificationResult.FAILURE
        self.player.add_rune(_rune)
        display_success(f"Removed {_rune} from {face_id+1} side.")
        return ModificationResult.SUCCESS

    def _select_rune(self, runes):
        options = [str(r) for r in runes]
        return select_from_list(options, "Availible runes: ", "Choose rune ('Enter' to exit): ")-1

    def _select_face(self, die):
        options = [str(r) for r in die.runes]
        return select_from_list(options, f"{die} faces:", "Choose face ('Enter' to exit): ")-1