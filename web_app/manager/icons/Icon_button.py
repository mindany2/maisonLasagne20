from web_app.manager.icons.Icon import Icon, TYPE_ICON
from web_app.manager.utils.Style import Style

class Icon_button(Icon):
    """
    Image button, used png to change bg color
    """
    def __init__(self, name, image, color_on, color_off, messsage, index = 100, lenght = 1):
        Icon.__init__(self, name, index = index, lenght = lenght)
        self.image = image
        self.color_on = color_on
        self.color_off = color_off
        self.pressed = False

    def pack(self, i, j):
        print(i,j,self.lenght)
        self.style = Style(grid = True, position=(i,j), size=(1,self.lenght), width=100,
                background_color = [self.color_off, self.color_on][self.pressed])

    def press(self):
        print("do action")
        self.pressed = not(self.pressed)

    def get_image(self):
        return self.image

    def get_type(self):
        return TYPE_ICON.button
