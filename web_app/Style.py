
def init_position(position):
    top = position[0]*20+5
    left = position[1]*19+5
    return str(top), str(left)

class Style:
    """
    Contient toutes les informations de style
    des boutons html
    """
    def __init__(self, position, couleur = "red"):
        self.image = ""
        self.bg = couleur
        self.size = 10
        self.top, self.left = init_position(position)

    
    def __str__(self):
        retour = ""
        retour +=  "background-color : "+self.bg + ";"
        retour += "font-size : "+str(self.size)+"px;"
        return retour
