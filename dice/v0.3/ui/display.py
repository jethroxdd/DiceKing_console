from ui.color import Paint, Color
from utils import len_without_color

def error(text):
        print(Paint(text, Color.ERROR))

def success(text):
        print(Paint(text, Color.SUCCESS))
        
def warning(text):
        print(Paint(text, Color.WARNING))

def message(text, color=Color.UI):
        print(Paint(text, color))

def H1(text: str):
        width = len_without_color(text)
        message(f"┌─{"─"*(width)}─┐")
        print(Paint("│ ", Color.UI) + text + Paint(" │", Color.UI))
        message(f"└─{"─"*(width)}─┘")
        print()

def H2(text):
        message(f"=== {text} ===\n")

def frame_text(text: list, title="", min_width=0):
        width = len_without_color(title)
        for line in text:
                width = max(width, len_without_color(line))
        width = max(width, min_width)
        message(f"┌{title}{"─"*(width-len_without_color(title))}──┐")
        for line in text:
                padding = " "*(width-len_without_color(line))
                print(Paint("│ ", Color.UI) + line + Paint(f"{padding} │", Color.UI))
        message(f"└─{"─"*(width)}─┘")

def available_dice(source, framed=False):
        if framed:
                _available_dice_framed(source)
                return
        print(Paint("Availible dice:", Color.UI))
        for i, die in enumerate(source.dice):
                print(f"{i+1}. {die}")

def _available_dice_framed(source):
        options = []
        for i, die in enumerate(source.dice):
                options += [f"{i+1}. {die}"]
        frame_text(text=options, title="Availible dice")

def available_runes(source, framed=False):
        if framed:
                _available_runes_framed(source)
                return
        print(Paint("Availible runes:", Color.UI))
        for i, rune in enumerate(source.runes):
                print(f"{i+1}. {rune}")

def _available_runes_framed(source):
        text = []
        for i, rune in enumerate(source.runes):
                text += [f"{i+1}. {rune}"]
        frame_text(text=text, title="Availible runes")

def roll_results(roll_results, source_name):
        print(Paint(f"{source_name}'s roll results:", Color.UI))
        for i, result in enumerate(roll_results):
                print(f"{i+1}. {result}")

def stats(player, enemy):
        text = []
        for entity in [player, enemy]:
                text += [f"{Paint(entity.name, Color.UI)} {Paint(entity.health, 196)}{Paint("|", Color.UI)}{Paint(entity.shield, 26)}"]
                text += [f"{Paint("Effects", Color.UI)} {", ".join([str(e) for e in entity.effects])}"]
        frame_text(text=text, title="Stats", min_width=15)

def header(round_number):
        print(Paint(f"\n=== Round {round_number} ===", Color.HEADER))

def room_choose(rooms):
        pass

def options(options: list):
        for i, text in enumerate(options):
                print(f"{i+1}. {text}")

def game_title():
        print("")
        print(" ████████▄   ▄█   ▄████████    ▄████████         ▄█   ▄█▄  ▄█  ███▄▄▄▄      ▄██████▄  ")
        print(" ███   ▀███ ███  ███    ███   ███    ███        ███ ▄███▀ ███  ███▀▀▀██▄   ███    ███ ")
        print(" ███    ███ ███▌ ███    █▀    ███    █▀         ███▐██▀   ███▌ ███   ███   ███    █▀  ")
        print(" ███    ███ ███▌ ███         ▄███▄▄▄           ▄█████▀    ███▌ ███   ███  ▄███        ")
        print(" ███    ███ ███▌ ███        ▀▀███▀▀▀          ▀▀█████▄    ███▌ ███   ███ ▀▀███ ████▄  ")
        print(" ███    ███ ███  ███    █▄    ███    █▄         ███▐██▄   ███  ███   ███   ███    ███ ")
        print(" ███   ▄███ ███  ███    ███   ███    ███        ██  ▀███▄ ███  ███   ███   ███    ███ ")
        print(" ████████▀  █▀   ████████▀    ██████████        █▀    ▀█▀ █▀    ▀█   █▀    ████████▀  ")
        print("")
