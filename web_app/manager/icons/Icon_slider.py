from web_app.manager.icons.Icon import Icon, TYPE_ICON
from web_app.manager.utils.Style import Style
from In_out.network.messages.interrupt.Press_inter import Press_inter

class Icon_slider(Icon):
    """
    A slider with a image at its background
    """
    def __init__(self, name, env, mini, maxi, image=None, background_color=None, lenght = None, index = None):
        Icon.__init__(self, name, env = env, index = index, lenght = lenght)
        self.mini, self.maxi = mini, maxi
        self.image = image
        self.background_color = background_color

    def pack(self, i, j):
        self.style = Style(grid = True, position=(i,j), size=(1,self.lenght), width=100,
                background_color = self.background_color)

    def get_min(self):
        return self.mini

    def get_max(self):
        return self.maxi

    def get_value(self):
        return self.value

    def move(self, client, prefix, value):
        self.value = value
        print(self.value)
        client.send(Press_inter(self.env, prefix+self.name, self.value))

    def get_image(self):
        return self.image

    def get_type(self):
        return TYPE_ICON.slider

