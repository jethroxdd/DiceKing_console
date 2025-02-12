import random
from color import *
from entity import Entity
import itertools
import re


class RoundSystem():
    def __init__(self, player: Entity, enemy: Entity):
        self.player = player
        self.enemy = enemy
    
    def start(self):
        while(not self.player.isDead and not self.enemy.isDead):
            self.gameLoop()
        if self.player.isDead:
            if self.enemy.isDead:
                print(f"{YELLOW}It's a tie!{RESET}")
            else:
                print(f"{RED}Player has been defeated!{RESET}")
        else:
            print(f"{GREEN}Enemy has been defeated!{RESET}")
        

    def gameLoop(self):
        # Player's turn
        self.printStats()
        self.processTurn(self.player, is_player=True)

        # Enemy's turn
        self.processTurn(self.enemy, is_player=False)

        # Resolve and apply effects
        self.resolveCombatPhase()

        # Prepare for next round
        input("\nPress Enter to continue to the next round...\n")
        self.player.shift()
        self.enemy.shift()

    def processTurn(self, entity, is_player):
        """Handle turn processing for any entity"""
        print(f"\n{'Player' if is_player else 'Enemy'}'s turn:{YELLOW}")
        entity.printDicesList()
        
        if is_player:
            player_input = input(f"{RESET}Choose dice up to 3 (separated by spaces): ")
            chosen = self.strToIntList(player_input)[:entity.maxDice]
        else:
            available = entity.availibleDices()
            chosen = random.sample(available, min(random.randint(0, len(available)), entity.maxDice))
            print(f"{RESET}Enemy chose dice: {chosen}")
        
        entity.dicesChosen = chosen
        entity.rollDices()

    def resolveCombatPhase(self):
        """Handle damage calculation and effect application"""
        # Print combat stats
        self.printCombatStats()
        
        # Apply effects and damage
        self.applyEffectsToBoth('good')
        
        player_damage = self.player.dealDamage()
        enemy_damage = self.enemy.dealDamage()
        
        self.enemy.takeDamage(player_damage)
        self.player.takeDamage(enemy_damage)
        
        self.printStats()
        self.applyEffectsToBoth('bad')

    def applyEffectsToBoth(self, effect_type):
        """Apply effects to both entities"""
        for entity in [self.player, self.enemy]:
            if effect_type == 'good':
                entity.applyGoodEffects()
            else:
                entity.applyBadEffects()

    def printCombatStats(self):
        """Print combat statistics for both entities"""
        p = self.player
        e = self.enemy
        damage = lambda x: f"\n\tdamage {RED}{x.damage}{RESET}"
        defense = lambda x: f"\n\tdefense {CYAN}{x.defense}{RESET}"
        crit = lambda x: f"\n\tcrit {YELLOW}{x.isCrit}{RESET}"
        coin_info = lambda x: f"\n\tcoin {YELLOW}{x.coin}{RESET}" if x.coin else ""
        
        stats = [
            f"{p.name}{damage(p)}{defense(p)}{crit(p)}{coin_info(p)}",
            
            f"{e.name}{damage(e)}{defense(e)}{crit(e)}{coin_info(e)}",
        ]
        
        print("\n" + "\n".join(stats))

    def formatStat(self, label, health, shield, color_label, color_health, color_shield):
        return f"{color_label}{label} {color_health}{health} {color_shield}{shield}{RESET}"

    def formatEffect(self, effect, color_label=WHITE, color_value=MAGENTA):
        return f"{color_label}{effect.name} {color_value}{effect.value}{RESET}"

    def printStats(self):
        """Print formatted statistics with proper column alignment considering color codes"""
        max_line_length = 40
        column_width = 20  # Each column is half of max line length

        # Helper to calculate visible length (excluding ANSI codes)
        def visible_length(s):
            return len(re.sub(r'\x1b\[[0-9;]*m', '', s))

        # Print health/shield status
        p_stats = self.formatStat(self.player.name, self.player.health, self.player.shield, GREEN, RED, CYAN)
        e_stats = self.formatStat(self.enemy.name, self.enemy.health, self.enemy.shield, GREEN, RED, CYAN)
        
        # Calculate padding between stats
        total_visible = visible_length(p_stats) + visible_length(e_stats)
        padding = " " * (max_line_length - total_visible)
        print(f"{p_stats}{padding}{e_stats}")

        # Prepare effect lists with color formatting
        p_effects = [self.formatEffect(e) for e in self.player.effects]
        e_effects = [self.formatEffect(e) for e in self.enemy.effects]

        # Print effects in aligned columns
        for p_eff, e_eff in itertools.zip_longest(p_effects, e_effects, fillvalue=""):
            # Calculate padding for player column
            p_pad = max(column_width - visible_length(p_eff), 0)
            # Calculate padding for enemy column
            e_pad = max(column_width - visible_length(e_eff), 0)
            
            # Construct line with proper padding
            line = f"{p_eff}{' ' * p_pad}{' ' * e_pad}{e_eff}"
            print(line)

    def strToIntList(self, input_string: str):
        """Convert input string to list of unique integers"""
        seen = set()
        result = []
        
        for item in input_string.split():
            try:
                num = int(item)
                if num not in seen:
                    seen.add(num)
                    result.append(num)
            except ValueError:
                print(f"Warning: '{item}' is not a valid integer, skipped.")
        
        return result