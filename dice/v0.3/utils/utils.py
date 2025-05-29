from random import choice, choices
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

def random_items_from_pool(pool, waighted=False, k=1):
    if waighted:
        return choices(pool, weights=[i.rarity.value for i in pool], k=k)[0:k-1]
    else:
        return choice(pool)

class Signal:
    def __init__(self):
        self._callbacks = []

    def connect(self, callback):
        self._callbacks.append(callback)

    def emit(self, *args, **kwargs):
        for callback in self._callbacks:
            callback(*args, **kwargs)