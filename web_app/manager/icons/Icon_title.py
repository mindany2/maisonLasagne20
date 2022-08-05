from web_app.manager.icons.Icon import Icon, TYPE_ICON
from web_app.manager.utils.Style import Style

class Icon_title(Icon):
    """
    Title
    """
    def __init__(self, name, text, index = -1, lenght = 1, color="black"):
        Icon.__init__(self, name, index=index, lenght=lenght, text=text)
        self.color = color

    def pack(self, i, j):
        self.style = Style(grid = True, position=(i,j), justify_self="center", size=(0,self.lenght),
                font_size=15, font_color=self.color)

    def get_type(self):
        return TYPE_ICON.text
