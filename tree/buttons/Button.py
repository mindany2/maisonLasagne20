class Button:
    """
    Simple button
    """

    def __init__(self, name, manager=None):
        self.name = name
        self.manager = manager

    def state(self):
        return False

    def press(self):
        pass

    def __eq__(self, other):
        if isinstance(other, Button):
            return self.name == other.name
        return False

    def __str__(self):
        return self.name + "\n"

