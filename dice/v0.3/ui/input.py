from ui import display
from ui.color import Paint, Color

def get_valid_input(input_text, validation, transform=lambda x: x, default=None):
        """Generic input validation handler"""
        while True:
            raw = input(Paint(input_text, Color.INPUT))
            if raw == "" and not default is None:
                return default
            try:
                transformed = transform(raw)
                if validation(transformed):
                    return transformed
                raise ValueError
            except (ValueError, IndexError):
                display.error("Invalid input!")

def get_single_int(options, input_text="Choose option: ", default=None):
    return get_valid_input(
        input_text = input_text,
        validation = lambda x: 1 <= x <= len(options),
        transform = lambda x: int(x),
        default = default
    )

def get_multiple_int(options, input_text="Choose option: ", default=None):
    return get_valid_input(
        input_text="Select runes ('Enter' to exit): ",
        validation=lambda x: all(1 <= s <= len(options) for s in x),
        transform=lambda x: list(map(int, x.split())),
        default = default
    )
    
def select_from_list(options, title, input_text="Choose option: ", default=None, framed=False, multiple=False):
    if not framed and not multiple:
        return _select_single_from_list(options, title, input_text, default)
    if not framed and multiple:
        return _select_multiple_from_list(options, title, input_text, default)
    if framed and not multiple:
        return _select_single_from_list_framed(options, title, input_text, default)
    if framed and multiple:
        return _select_multiple_from_list_framed(options, title, input_text, default)

def _select_single_from_list(options, title, input_text="Choose option: ", default=None):
    print(title)
    for i, text in enumerate(options):
        print(f"{i+1}. {text}")
    
    selection = get_single_int(options, input_text, default)
    return selection

def _select_single_from_list_framed(options, title, input_text="Choose option: ", default=None):
    text = []
    for i, _text in enumerate(options):
        text += [f"{i+1}. {_text}"]
    display.frame_text(text=text, title=title)
        
    selection = get_single_int(options, input_text, default)
    return selection

def _select_multiple_from_list(options, title, input_text="Choose option: ", default=None):
    print(title)
    for i, text in enumerate(options):
        print(f"{i+1}. {text}")
    
    selection = get_multiple_int(options, input_text, default)
    return selection

def _select_multiple_from_list_framed(options, title, input_text="Choose option: ", default=None):
    text = []
    for i, _text in enumerate(options):
        text += [f"{i+1}. {_text}"]
    display.frame_text(text=text, title=title)
        
    selection = get_multiple_int(options, input_text, default)
    return selection