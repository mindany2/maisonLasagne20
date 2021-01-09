from web_app.manager.icons.Icon import Icon

class Icon_slider(Icon):
    """
    A slider with a image at its background
    """
    def __init__(self, name, position, variable, value = 0, lenght = 1, height = 1):
        Icon.__init__(self, name, position, lenght, height)
        self.variable = variable
        self.value = value

