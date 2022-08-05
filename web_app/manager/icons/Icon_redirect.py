from web_app.manager.icons.Icon import Icon, TYPE_ICON
from web_app.manager.utils.Style import Style
from In_out.network.messages.interrupt.Press_inter import Press_inter

class Icon_redirect(Icon):
    """
    Image button, used png to change bg color
    """
    def __init__(self, name, image, link, background_color = None, index = None, lenght = None):
        Icon.__init__(self, name, index = index, lenght = lenght)
        self.image = image
        self.background_color = background_color
        self.link = link

    def pack(self, i, j):
        self.style = Style(grid = True, position=(i,j), size=(1,self.lenght), width=100,
                background_color = self.background_color)

    def get_link(self):
        return self.link

    def get_state(self):
        return True

    def press(self, client):
        print("go to "+self.link)

    def get_image(self):
        return self.image

    def get_type(self):
        return TYPE_ICON.link
