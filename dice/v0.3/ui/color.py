def Fore(color):
    return f"\033[38;5;{color}m"

def Back(color):
    return f"\033[48;5;{color}m"

def Paint(text, fore=7, back=0):
    return f"{Fore(fore)}{Back(back)}{text}{Style.RESET_ALL}"

class Color:
    '''
    Text colors
    '''
    # Basic colors
    BLACK = 0     
    RED = 1       
    GREEN = 2      
    YELLOW = 3     
    BLUE = 4      
    MAGENTA = 5    
    CYAN = 6      
    WHITE = 7
    
    # Display colors
    UI = 7
    ERROR = 88
    INPUT = 220
    SUCCESS = 28
    WARNING = 202
    HEADER = 80
    
    # Rune colors
    EMPTY = 240
    ATTACK = 124
    SHIELD = 26
    FIRE = 166
    CRIT = 214
    
class Style:
    RESET_ALL = '\033[0m'        # Reset to default color