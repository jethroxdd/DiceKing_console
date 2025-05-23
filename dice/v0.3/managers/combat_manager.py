from itertools import zip_longest
from utils import Value
from ui import get_valid_input, display

class RollResult:
    SPECIAL_RUNE_NAMES = {"crit", "empty"}
    
    def __init__(self, rune, value, raw, source, target):
        self.rune = rune
        self.value = Value(value)
        self.raw = raw
        self.source = source
        self.target = target
    
    def apply(self, roll_results, i):
        self.rune.apply(self.value, self.source, self.target, roll_results, i)
    
    def __str__(self):
        """Formats roll result for display"""
        display_value = "-" if self.rune.name in self.SPECIAL_RUNE_NAMES else int(self.value)
        return f"({self.raw}) {display_value} {self.rune}"

class RollResults:
    def __init__(self):
        self.player = []
        self.enemy = []
    
    def apply(self):
        """Process all results in priority order"""
        for i, (player_res, enemy_res) in enumerate(zip_longest(self.player, self.enemy, fillvalue=None)):
            self._process_result_pair(player_res, enemy_res, i)
    
    def _process_result_pair(self, player_res, enemy_res, index: int):
        """Handles a pair of player/enemy results with priority comparison"""
        if player_res and enemy_res:
            self._handle_priority_results(player_res, enemy_res, index)
        else:
            self._apply_result(player_res, self.player, index)
            self._apply_result(enemy_res, self.enemy, index)
    
    def _handle_priority_results(self, player_res: RollResult, enemy_res: RollResult, index: int):
        """Applies results based on rune priority"""
        if player_res.rune.priority < enemy_res.rune.priority:
            self._apply_result(player_res, self.player, index)
            self._apply_result(enemy_res, self.enemy, index)
        else:
            self._apply_result(enemy_res, self.enemy, index)
            self._apply_result(player_res, self.player, index)
    
    def _apply_result(self, result, results_list, index: int):
        """Applies a single result if it exists"""
        if result:
            result.apply(results_list, index)

class CombatManager:

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.current_round = 0
        
        # Initialize targeting
        self.player.set_target(self.enemy)
        self.enemy.set_target(self.player)

    def battle(self):
        """Main battle loop"""
        
        while self._combat_continues():
            self.current_round += 1
            print()
            display.H2(f"Round {self.current_round}")
            self._handle_round()
    
    def _handle_round(self):
        """Process a single combat round"""
        display.stats(self.player, self.enemy)
        
        # Phase 1: Dice Selection
        print()
        self.player_dice = self._select_player_dice()
        self.enemy_dice = self._select_enemy_dice()
        
        # Phase 2: Rolling and Rerolls
        print()
        roll_results = self._roll_dice()
        self._handle_rerolls(roll_results)
        
        # Phase 3: Order Resolution
        print()
        self._resolve_activation_order(roll_results)
        
        # Phase 4: Effect Application
        print()
        self._apply_roll_results(roll_results)
        self._process_status_effects()
        
        # Phase 5: Cleanup
        self._post_round_cleanup()

    def _select_player_dice(self):
        """Player selects dice for this round"""
        display.available_dice(self.player)
        
        selected = get_valid_input(
            input_text="Select dice ('Enter' to select all dice): ",
            validation=lambda x: self._validate_dice_selection(x),
            transform=lambda x: list(map(int, x.split())),
            default = [i+1 for i, die in enumerate(self.player.dice)]
        )   
        return [self.player.dice[i-1] for i in selected]

    def _select_enemy_dice(self):
        """AI selects enemy dice (basic implementation)"""
        return self.enemy.ai_select_dice()

    def _roll_dice(self) -> RollResults:
        """Execute dice rolls for both sides"""
        results = RollResults()
        self._roll_combatant_dice(self.player, self.player_dice, results.player)
        self._roll_combatant_dice(self.enemy, self.enemy_dice, results.enemy)
        display.roll_results(results.player, "Player")
        return results
    
    def _roll_combatant_dice(self, combatant, dice_list, results_container):
        """Roll dice for a combatant and store results"""
        for die in dice_list:
            rune, value, raw = die.roll()
            results_container.append(RollResult(rune, value, raw, combatant, combatant.target))

    def _handle_rerolls(self, results: RollResults):
        """Manage reroll mechanics"""
        remaining_rerolls = self.player.rerolls
        
        while remaining_rerolls > 0:
            selection = get_valid_input(
                input_text=f"Rerolls left: {remaining_rerolls}. Choose die to reroll ('Enter' to skip): ",
                validation=lambda x: 0 <= x <= len(results.player),
                transform=int,
                default=False
            )
            
            if not selection:
                break
                
            self._perform_reroll(results, selection - 1)
            remaining_rerolls -= 1
    
    def _perform_reroll(self, results: RollResults, index: int):
        """Execute a single reroll operation"""
        die = self.player_dice[index]
        rune, value, raw = die.roll()
        results.player[index] = RollResult(rune, value, raw, self.player, self.enemy)
        print(results.player[index])

    def _resolve_activation_order(self, results):
        """Determine effect activation order"""
        # Player chooses order
        display.roll_results(results.player, "Player")     
                
        order = get_valid_input(
            input_text="Choose activation order ('Enter' to skip): ",
            validation=lambda x: self._validate_activation_order(x, len(results.player)),
            transform=lambda x: list(map(int, x.split())),
            default = set(range(1, len(results.player)+1))
        )
        results.player = [results.player[i-1] for i in order]
        
        # Enemy uses AI-determined order
        results.enemy = self.enemy.ai_choose_order(results.enemy)

    def _apply_roll_results(self, results):
        """Apply all combat results"""
        results.apply()        
        display.roll_results(results.player, "Player")
        display.roll_results(results.enemy, "Enemy")
        

    def _process_status_effects(self):
        """Handle status effect ticks"""
        for combatant in [self.player, self.enemy]:
            combatant.process_effects()

    def _post_round_cleanup(self):
        """End-of-round maintenance"""
        for combatant in [self.player, self.enemy]:
            combatant.end_round_cleanup()

    # Helper methods
    def _combat_continues(self):
        return not self.player.is_dead and not self.enemy.is_dead

    def _validate_dice_selection(self, selections):
        num_dice = len(self.player.dice)
        return (
            len(selections) > 0 and
            len(selections) <= num_dice and
            all(1 <= s <= num_dice for s in selections)
        )

    def _validate_activation_order(self, order, max_length):
        return (
            len(order) == max_length and
            set(order) == set(range(1, max_length+1))
        )