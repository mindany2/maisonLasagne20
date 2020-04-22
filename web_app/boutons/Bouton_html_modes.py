from web_app.boutons.Bouton_html import Bouton_html
from web_app.boutons.Style import Style
from tree.utils.boutons.Bouton_changement_mode import Bouton_changement_mode

class Bouton_html_modes(Bouton_html):
    """
    Ceci est le bouton mode
    """
    def __init__(self):
        Bouton_html.__init__(self, Bouton_changement_mode(), None, None)

    def reload(self):
        # on override reload
        self.bouton.reload_name()
        if self.bouton.nom == "normal":
            self.style = Style((10,50), relative=False, couleur="yellow", taille = 50, couleur_texte="black")
        else:
            self.style = Style((10,50), relative=False, couleur="black", taille = 50, couleur_texte= "white")

    def get_id(self):
        return "mode"



        
