class BaseEffect:
    def __init__(self, name, value, duration, order):
        self.name = name
        self.value = value
        self.duration = duration
        self.order = order