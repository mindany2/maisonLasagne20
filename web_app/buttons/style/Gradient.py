from tree.utils.Color import Color

class Gradient:
    """
    un dégrader linéaire 
    """
    def __init__(self, color_left, color_right, direction = "left"):
        self.color_left = Color(color_left)
        self.color_right = Color(color_right)
        self.direction = direction

    def __str__(self):
        return "linear-gradient(to {}, {}, {})".format(self.direction, self.color_right.get_with_hash(), self.color_left.get_with_hash()) 

