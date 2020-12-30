from web_app.manager.icons.Icon_slider import Icon_slider

class Icon_slider_with_value(Icon_slider):
    """
    Allow to display the value of the slider in the icon 
    """
    def __init__(self, name, position, variable, text, value=0, lenght = 1, height = 1):
        Icon_slider.__init__(self, name, position, variable, value, lenght, height)
        self.text = text
