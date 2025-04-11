from ui.color import Paint, Color

def display_error(text):
        print(Paint(text, Color.ERROR))

def display_success(text):
        print(Paint(text, Color.SUCCESS))
        
def display_warning(text):
        print(Paint(text, Color.WARNING))

def display_available_dice(source):
        print(Paint("Availible dice:", Color.UI))
        for i, die in enumerate(source.dice):
                print(f"{i+1}. {die.str_all()}")

def display_availible_runes(source):
        print(Paint("Availible runes:", Color.UI))
        for i, rune in enumerate(source.runes):
                print(f"{i+1}. {rune}")

def display_roll_results(roll_results, source_name):
        print(Paint(f"{source_name}'s roll results:", Color.UI))
        for i, result in enumerate(roll_results):
                print(f"{i+1}. {result}")

def display_stats(player, enemy):
        for entity in [player, enemy]:
                print(f"{Paint(entity.name, Color.UI)} {Paint(entity.health, 196)}{Paint("|", Color.UI)}{Paint(entity.shield, 26)}")
                print(f"{Paint("Effects", Color.UI)} {", ".join([str(e) for e in entity.effects])}")

def display_header(round_number):
        print(Paint(f"\n=== Round {round_number} ===", Color.HEADER))
        

def display_post_round_summary(statistic):
        pass