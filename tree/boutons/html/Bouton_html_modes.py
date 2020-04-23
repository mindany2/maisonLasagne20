from tree.boutons.html.Style import Style
from tree.boutons.Bouton_changement_mode import Bouton_changement_mode

class Bouton_html_modes(Bouton_changement_mode):
    """
    Ceci est le bouton mode
    """
    def __init__(self, nom_mode):
        Bouton_changement_mode.__init__(self, nom_mode)
        if nom_mode == "normal":
            self.style = Style((0,0), relative=False, couleur="white", couleur_texte="black")
        else:
            self.style = Style((0,0), relative=False, couleur="black", couleur_texte="white")

    def reload(self):
        pass




        
