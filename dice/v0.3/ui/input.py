from ui import display
from ui.color import Paint, Color

def get_valid_input(input_text, validation, transform=lambda x: x, default=None):
        """Generic input validation handler"""
        while True:
            raw = input(Paint(input_text, Color.INPUT))
            if raw == "" and default != None:
                return default
            try:
                transformed = transform(raw)
                if validation(transformed):
                    return transformed
                raise ValueError
            except (ValueError, IndexError):
                display.error("Invalid input!")

def select_from_list(options, title, input_text="Choose option: ", default=None):
    print(title)
    for i, text in enumerate(options):
        print(f"{i+1}. {text}")
    
    selection = get_valid_input(
        input_text = input_text,
        validation = lambda x: 1 <= x <= len(options),
        transform = lambda x: int(x),
        default = default
    )
    
    return selection