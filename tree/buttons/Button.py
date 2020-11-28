class Button:
    """
    Simple button
    """

    def __init__(self, name, manager):
        self.name = name
        self.manager = manager

    def etat(self):
        return False

    def press(self):
        """
        Lance le bon scénario et gère la pile
        """
        pass

    def __eq__(self, other):
        if isinstance(other, Button):
            return self.name == other.name
        return False

    def __str__(self):
        return self.name

