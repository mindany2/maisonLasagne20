
class Style:
    """
    Contient toutes les informations de style
    des boutons html
    """
    def __init__(self, padding = (0,0),position = (0,0), size = (50,50),relative = True, background_color = "red",
            font_size = 15, couleur_texte = "white", borders_etat = (False, False), borders_radius_etat = (False, False), 
            background_image = None, box_shadow = False, font_weight = "None"):
        self.image = ""
        self.bg_color = background_color
        self.font_size = font_size
        self.font_color = couleur_texte
        self.top, self.left = position[0], position[1]
        self.padding = padding
        self.width, self.height = size[0], size[1]
        self.border_left = ("None", "solid")[borders_etat[0]]
        self.border_right = ("None", "solid")[borders_etat[1]]
        self.border_radius = ("0 ", "40px ")[borders_radius_etat[0]]+("0 0 ","40px 40px ")[borders_radius_etat[1]]+("0 ", "40px ")[borders_radius_etat[0]]
        self.bg_image = background_image
        self.box_shadow = ("None", "box-shadow: inset 0 10px 50px rgba(255, 255, 255, 100)")[box_shadow]
        self.font_weight = font_weight


    
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
        if self.bg_image: # != None
            retour += "background-image : {};".format(self.bg_image)

        return retour
