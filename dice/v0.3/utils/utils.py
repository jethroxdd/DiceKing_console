from random import choices
import re

def len_without_color(text):
    length = len(text)
    color_patern = r"\033\[38;5;[0-9]{1,3}m"
    reset_patern = r"\033\[0m"
    color_founds = re.findall(color_patern, text)
    reset_founds = re.findall(reset_patern, text)
    for f in color_founds:
        length -= len(f) + 6
    for f in reset_founds:
        length -= len(f) + 3
    return length

def random_items_from_pool(pool, k=1):
    return choices(pool, weights=[i.rarity for i in pool], k=k)[0]

class Signal:
    def __init__(self, player):
        self.player = player
        self.functions = []
    
    def add(self, func):
        self.functions += [func]
    
    def emit(self, *args, **kwargs):
        for fun in self.functions:
            fun(*args, **kwargs)