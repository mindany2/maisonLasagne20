
class Style:
    """
    Contient toutes les informations de style
    des boutons html
    """
    def __init__(self, couleur = "red"):
        self.image = ""
        self.bg = couleur
    
    def __str__(self):
        retour = ""
        retour +=  "background-color : "+self.bg + ";"
        return retour
