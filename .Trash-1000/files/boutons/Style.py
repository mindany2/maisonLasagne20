
def init_position(position, relative):
    if relative:
        top = position[0]*20+5
        left = position[1]*19+5
    else:
        top = position[0]
        left = position[1]
    return str(top), str(left)

class Style:
    """
    Contient toutes les informations de style
    des boutons html
    """
    def __init__(self, position, relative = True, couleur = "red", taille = 10, couleur_texte = "black"):
        self.image = ""
        self.bg = couleur
        self.size = taille
        self.font_color = couleur_texte
        self.top, self.left = init_position(position, relative)

    
    def __str__(self):
        retour = ""
        retour +=  "background-color : "+self.bg + ";"
        retour += "font-size : "+str(self.size)+"px;"
        retour += "font-color : "+str(self.font_color)+"px;"
        return retour
