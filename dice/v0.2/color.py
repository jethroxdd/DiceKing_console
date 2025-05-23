
def Fore(color):
    return f"\033[38;5;{color}m"

def Back(color):
    return f"\033[48;5;{color}m"

class Color:
    '''
    Text color
    '''
    BLACK = 0     
    RED = 1       
    GREEN = 2      
    YELLOW = 3     
    BLUE = 4      
    MAGENTA = 5    
    CYAN = 6      
    WHITE = 7

class Style:
    RESET_ALL = '\033[0m'        # Reset to default color