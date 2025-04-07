from ui import display_error
from ui.color import Paint, Color

def get_valid_input(input_text, validation, transform=lambda x: x, default=None):
        """Generic input validation handler"""
        while True:
            raw = input(Paint(input_text, Color.INPUT))
            if raw == "":
                return default
            try:
                transformed = transform(raw)
                if validation(transformed):
                    return transformed
                raise ValueError
            except (ValueError, IndexError):
                display_error()

def select_from_list(options, title):
    print(title)
    for i, text in options:
        print(f"{i}. {text}")
    
    selection = get_valid_input(
        input_text = "Choose option:",
        validation = lambda x: 0 <= len(options),
        transform = lambda x: int(x)
    )
    
    return selection