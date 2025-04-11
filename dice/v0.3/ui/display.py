from ui.color import Paint, Color
from helpers import len_without_color

def display_error(text):
        print(Paint(text, Color.ERROR))

def display_success(text):
        print(Paint(text, Color.SUCCESS))
        
def display_warning(text):
        print(Paint(text, Color.WARNING))

def display_message(text):
        print(Paint(text, Color.UI))

def display_title_H1(text: str):
        width = len_without_color(text)
        display_message(f"┌─{"─"*(width)}─┐")
        print(Paint("│ ", Color.UI) + text + Paint(" │", Color.UI))
        display_message(f"└─{"─"*(width)}─┘")

def display_title_H2(text):
        display_message(f"=== {text} ===")

def display_frame_text(text: list, min_width=0):
        width = 0
        for line in text:
                width = max(width, len_without_color(line))
        width = max(width, min_width)
        display_message(f"┌─{"─"*(width)}─┐")
        for line in text:
                padding = " "*(width-len_without_color(line))
                print(Paint("│ ", Color.UI) + line + Paint(f"{padding} │", Color.UI))
        display_message(f"└─{"─"*(width)}─┘")

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
        text = []
        for entity in [player, enemy]:
                text += [f"{Paint(entity.name, Color.UI)} {Paint(entity.health, 196)}{Paint("|", Color.UI)}{Paint(entity.shield, 26)}"]
                text += [f"{Paint("Effects", Color.UI)} {", ".join([str(e) for e in entity.effects])}"]
        display_frame_text(text)

def display_header(round_number):
        print(Paint(f"\n=== Round {round_number} ===", Color.HEADER))
        

def display_post_round_summary(statistic):
        pass