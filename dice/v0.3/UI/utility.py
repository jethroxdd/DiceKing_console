from UI.color import Paint

def print_availible_dice(source):
    print(Paint("Availible dice:", 240))
    for i, die in enumerate(source.dice):
        print(f"{i+1}){die.print_all()}")

def print_availible_runes(source):
    print(Paint("Доступные руны:", 240))
    for i, rune in enumerate(source.runes):
        print(f"{i+1}. {rune}")

def print_roll_results(roll_results, source_str):
    print(Paint(f"{source_str}'s roll results:", 240))
    for i in range(len(getattr(roll_results, source_str))):
        result = getattr(roll_results, source_str)[i]
        print(f"{i+1}) {str(result)}")

def print_stats(player, enemy):
    print(f"{Paint("Player", 250)} {Paint(player.health, 196)}{Paint("|", 250)}{Paint(player.shield, 26)}")
    print(f"{Paint("Effects", 248)} {", ".join([str(e) for e in player.effects])}")
    print(f"{Paint("Enemy", 250)} {Paint(enemy.health, 196)}{Paint("|", 250)}{Paint(enemy.shield, 26)}")
    print(f"{Paint("Effects", 248)} {", ".join([str(e) for e in enemy.effects])}")