from enum import Enum
from core.rune.types import Empty
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
            display.message(self.current_session.die)
            choice = select_from_list(options, "Modification Menu: ", input_text="Choose option ('Enter' to exit): ", default=ModificationType.EXIT, framed=True)
            choice = ModificationType(choice)
            match choice:
                case ModificationType.ATTACH:
                    self._attach_rune_flow()
                case ModificationType.REMOVE:
                    self._remove_rune_flow()
                case ModificationType.UPGRADE_DIE:
                    self._upgrade_die_flow()
                case ModificationType.EXIT:
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
        if isinstance(_rune, Empty):
            display.success(f"Attached {rune} rune to the {face_id+1} side")
        else:
            display.success(f"Replaced {_rune} with {rune} at {face_id+1} side")
            self.player.add_rune(_rune)
        self.player.remove_rune(rune)
        return ModificationResult.SUCCESS
    
    def _remove_rune_flow(self):
        print()
        faces = self._select_faces(self.current_session.die)
        if faces == False:
            return ModificationResult.EXIT
        
        return self.remove_rune(self.current_session.die, faces)

    def remove_rune(self, die, face_ids: int):
        for face_id in face_ids: 
            _rune = die.remove_rune(face_id-1)
            if isinstance(_rune, Empty):
                continue
            self.player.add_rune(_rune)
    
    def _upgrade_die_flow(self):
        die = self.current_session.die
        cost = (die.upgrades+1)*self.BASE_UPGRADE_COST
        if self.player.gold < cost:
            display.warning("Not enough money")
            return ModificationResult.FAILURE
        self.player.gold -= cost
        die.upgrade()
        display.message("Succesfully upgraded die")
        return ModificationResult.SUCCESS

    def _select_rune(self, runes):
        options = [str(r) for r in runes]
        return select_from_list(options, "Availible runes: ", "Choose rune ('Enter' to exit): ", default=False)

    def _select_face(self, die):
        options = [str(r) for r in die.runes]
        return select_from_list(options, f"{die.name} faces:", "Choose face ('Enter' to exit): ", default=False)
    
    
    def _select_faces(self, die):
        options = [str(r) for r in die.runes]
        display.options(options)
        selected = get_valid_input(
            input_text="Select runes ('Enter' to exit): ",
            validation=lambda x: self._validate_runes_selection(x),
            transform=lambda x: list(map(int, x.split())),
            default = False
        )
        return selected
    
    def _validate_runes_selection(self, selections):
        die = self.current_session.die
        return (
            len(selections) > 0 and
            len(selections) <= die.sides and
            all(1 <= s <= die.sides for s in selections)
        )