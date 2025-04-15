from itertools import zip_longest
from ui import get_valid_input, display

class RollResult:
    def __init__(self, rune, _value, raw, source, target):
        self.rune = rune
        self._value = _value
        self.raw = raw
        self.source = source
        self.target = target
        self.value_mult_mods = []
        self.value_flat_mods = []
    
    @property
    def value(self):
        value = self._value
        for mod in self.value_mult_mods:
            value *= mod
        for mod in self.value_flat_mods:
            value += mod
        return int(value)
    
    
    def apply(self, roll_results):
        self.rune.apply(self.value, self.source, self.target, roll_results)
    
    def __str__(self):
        value = self.value
        if self.rune.name in ["crit", "empty"]:
            value = "-"
        return f"({self.raw}) {value} {self.rune}"

class RollResults:
    def __init__(self):
        self.player = []
        self.enemy = []
    
    def apply(self):
        for player_result, enemy_result in zip_longest(self.player, self.enemy):
            if player_result and enemy_result:
                if player_result.rune.order < enemy_result.rune.order:
                    player_result.apply(self.player)
                    enemy_result.apply(self.enemy)
                else:
                    enemy_result.apply(self.enemy)
                    player_result.apply(self.player)
            elif player_result:
                player_result.apply(self.player)
            elif enemy_result:
                enemy_result.apply(self.enemy)

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
            default = False
        )
        if selected == False:
            selected = [i+1 for i, die in enumerate(self.player.dice)]
        return [self.player.dice[i-1] for i in selected]

    def _select_enemy_dice(self):
        """AI selects enemy dice (basic implementation)"""
        return self.enemy.ai_select_dice()

    def _roll_dice(self):
        """Execute dice rolls for both sides"""
        results = RollResults()
        
        # Player rolls
        for die in self.player_dice:
            rune, value, raw = die.roll()
            results.player.append(RollResult(rune, value, raw, self.player, self.enemy))
        
        # Enemy rolls
        for die in self.enemy_dice:
            rune, value, raw = die.roll()
            results.enemy.append(RollResult(rune, value, raw, self.enemy, self.player))
        
        display.roll_results(results.player, "Player")
        
        return results

    def _handle_rerolls(self, results):
        """Manage reroll mechanics"""
        remaining_rerolls = self.player.get_available_rerolls()
        
        while remaining_rerolls > 0:            
            selection = get_valid_input(
                input_text=f"Rerolls left: {remaining_rerolls}. Choose die to reroll ('Enter' to skip): ",
                validation=lambda x: 0 <= x <= len(results.player),
                transform=lambda x: int(x),
                default = False
            )
            
            if selection == False:
                break
                
            die_index = selection - 1
            die = self.player_dice[die_index]
            rune, value, raw = die.roll()
            result = RollResult(rune, value, raw, self.player, self.enemy)
            results.player[die_index] = result
            remaining_rerolls -= 1
            print(result)

    def _resolve_activation_order(self, results):
        """Determine effect activation order"""
        # Player chooses order
        display.roll_results(results.player, "Player")     
                
        order = get_valid_input(
            input_text="Choose activation order ('Enter' to skip): ",
            validation=lambda x: self._validate_activation_order(x, len(results.player)),
            transform=lambda x: list(map(int, x.split())),
            default = False
        )
        if order == False:
            order = set(range(1, len(results.player)+1))
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
        self.player.process_effects()
        self.enemy.process_effects()

    def _post_round_cleanup(self):
        """End-of-round maintenance"""
        self.player.end_round_cleanup()
        self.enemy.end_round_cleanup()

    # Helper methods
    def _combat_continues(self):
        return not self.player.is_dead and not self.enemy.is_dead

    def _validate_dice_selection(self, selections):
        return (
            len(selections) > 0 and
            len(selections) <= len(self.player.dice) and
            all(1 <= s <= len(self.player.dice) for s in selections)
        )

    def _validate_activation_order(self, order, max_length):
        return (
            len(order) == max_length and
            set(order) == set(range(1, max_length+1))
        )