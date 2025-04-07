from enum import Enum
from ui import Paint, display_error
from ui import select_from_list, get_valid_int_input

class ModificationType(Enum):
    ATTACH = 1
    REMOVE = 2
    UPGRADE_DIE = 3
    EXIT = 0

class ModificationResult(Enum):
    SUCCESS = 1
    FAILURE = 2
    CANCELLED = 3

class ModificationManager:
    BASE_UPGRADE_COST = 50
    TRANSMUTE_COST = 3
    SELL_MULTIPLIER = 0.6

    def __init__(self, player):
        self.player = player
        self.current_session = None

    class ModificationSession:
        def __init__(self, die=None):
            self.die = die
            self.original_state = die.copy() if die else None
            self.modification_type = None

    def start_session(self, die=None):
        self.current_session = self.ModificationSession(die)
        return self._main_menu()

    def _main_menu(self):
        options = {
            ModificationType.ATTACH: "Attach Rune",
            ModificationType.REMOVE: "Remove Rune",
            ModificationType.UPGRADE_DIE: "Upgrade Die",
            ModificationType.EXIT: "Exit"
        }
        
        while True:
            choice = select_from_list(options, "Modification Menu:")
            if not choice:
                return ModificationResult.CANCELLED
            
            match choice:
                case ModificationType.ATTACH:
                    result = self._attach_rune_flow()
                case ModificationType.REMOVE:
                    result = self._remove_rune_flow()
                # case ModificationType.UPGRADE_DIE:
                #     result = self._upgrade_die_flow()
                # case ModificationType.TRANSMUTE:
                #     result = self._transmute_runes_flow()
                # case ModificationType.SELL:
                #     result = self._sell_items_flow()
                case _:
                    return ModificationResult.CANCELLED
            
            if result != ModificationResult.SUCCESS:
                return result

    def _attach_rune_flow(self):
            
        die = self.current_session.die
        rune_index = self._select_rune()
        if rune_index is None:
            return ModificationResult.CANCELLED
        
        face = self._select_face(die)
        if face is None:
            return ModificationResult.CANCELLED
        
        return self.attach_rune(die, self.player.runes[rune_index], face)

    def attach_rune(self, die, rune, face: int) -> ModificationResult:
        if not self._validate_attachment(die, rune, face):
            display_error("Invalid attachment!")
            return ModificationResult.FAILURE
        
        old_rune = die.get_rune(face)
        if old_rune and not old_rune.is_empty():
            if not self._confirm_replace(old_rune):
                return ModificationResult.CANCELLED
            self.player.add_rune(old_rune)
        
        if die.attach_rune(rune, face):
            self.player.remove_rune(rune)
            display_success(f"Attached {rune.name} to face {face+1}!")
            return ModificationResult.SUCCESS
        return ModificationResult.FAILURE

    def _remove_rune_flow(self):
        if not self._validate_die_selection():
            return ModificationResult.FAILURE
            
        die = self.current_session.die
        face = self._select_face(die, "Select face to remove from:")
        if face is None:
            return ModificationResult.CANCELLED
        
        return self.remove_rune(die, face)

    def remove_rune(self, die, face: int) -> ModificationResult:
        if not self._validate_removal(die, face):
            display_error("Invalid removal attempt!")
            return ModificationResult.FAILURE
        
        removed_rune = die.remove_rune(face)
        if removed_rune and not removed_rune.is_empty():
            if self.player.add_rune(removed_rune):
                display_success(f"Removed {removed_rune.name} from face {face+1}")
                return ModificationResult.SUCCESS
            else:
                die.attach_rune(removed_rune, face)  # Revert if inventory full
                display_error("Inventory full! Cannot remove rune.")
                return ModificationResult.FAILURE
        return ModificationResult.FAILURE

    def _validate_attachment(self, die, rune, face):
        return (
            0 <= face < die.sides and
            rune in self.player.runes and
            die.can_accept_rune(rune, face)
        )

    def _validate_removal(self, die, face):
        return (
            0 <= face < die.sides and
            not die.get_rune(face).is_empty()
        )

    def _select_rune(self, raw):
        return get_valid_input(
            items=self.player.runes,
            prompt=prompt,
            formatter=lambda r: f"{r.name} ({r.type})"
        )

    def _select_face(self, die, raw):
        return get_valid_input(
            raw=raw,
            validation=lambda x: 1 <= x <= die.sides,
            transform=lambda x: int(x)-1
        )

    # Additional methods for upgrade/transmute/sell would follow similar patterns
    # ...

    def cancel_session(self):
        if self.current_session and self.current_session.die:
            self.current_session.die.restore(self.current_session.original_state)
        self.current_session = None
        display_warning("Modification session cancelled")

    def commit_session(self):
        self.current_session = None
        display_success("Modifications committed")