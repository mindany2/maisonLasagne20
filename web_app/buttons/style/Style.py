
class Style:
    """
    Contient toutes les informations de style
    des boutons html
    """
    def __init__(self, padding = (0,0),position = (0,0), size = (50,50),relative = True, background_color = "",
            font_size = 15, font_color = "white", borders_state = (False, False), borders_radius_state = (False, False), 
            background_image = None, box_shadow = False, font_weight = "None", margin = [0,0], type_position = "relative"):
        self.image = ""
        self.bg_color = background_color
        self.font_size = font_size
        self.font_color = font_color
        self.padding = padding
        self.bg_image = background_image
        self.font_weight = font_weight
        self.margin = margin
        self.type_position = type_position

        self.set_position(position)
        self.set_size(size)
        self.set_border(borders_state, borders_radius_state)
        self.set_shadow(box_shadow)

    def set_position(self, position):
        self.top, self.left = position[0], position[1]

    def set_size(self, size):
        self.width, self.height = size[0], size[1]

    def set_border(self, borders_state, borders_radius_state):
        self.border_left = ("None", "solid")[borders_state[0]]
        self.border_right = ("None", "solid")[borders_state[1]]
        self.border_radius = ("0 ", "40px ")[borders_radius_state[0]]+("0 0 ","40px 40px ")[borders_radius_state[1]]+("0 ", "40px ")[borders_radius_state[0]]


    def set_shadow(self, box_shadow):
        self.box_shadow = ("None", "box-shadow: inset 0 10px 50px rgba(255, 255, 255, 100)")[box_shadow]

    
    def __str__(self):
        retour = ""
        retour +=  "background-color : {};".format(self.bg_color)
        retour += "font-size : {}px;".format(self.font_size)
        retour += "color : {};".format(self.font_color)
        retour += "top : {}px;".format(self.top)
        retour += "left : {}px;".format(self.left)
        retour += "width : {}px;".format(self.width)
        retour += "height : {}px;".format(self.height)
        retour += "padding : {}% {}%;".format(self.padding[0], self.padding[1])
        retour += "border-left : {};".format(self.border_left)
        retour += "border-right : {};".format(self.border_right)
        retour += "border-radius : {};".format(self.border_radius)
        retour += "box-shadow : {};".format(self.box_shadow)
        retour += "font-weight : {};".format(self.font_weight)
        retour += "margin-left : {}px;".format(self.margin[0])
        retour += "margin-right : {}px;".format(self.margin[1])
        retour += "margin-right : {}px;".format(self.margin[1])
        retour += "position : {};".format(self.type_position)
        if self.bg_image: # != None
            retour += "background-image : {};".format(self.bg_image)
        return retour
