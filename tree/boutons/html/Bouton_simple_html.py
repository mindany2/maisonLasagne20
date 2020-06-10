from tree.Tree import Tree
from tree.boutons.html.style.Style import Style
from tree.boutons.Bouton_simple import Bouton_simple



class Bouton_simple_html(Bouton_simple):
    """
    le bouton de l'application web
    """

    def __init__(self, nom, scenar):
        Bouton_simple.__init__(self, nom, scenar)
        # tous les style sont initialisé après avec preset.set_styles
        self.style_on = None
        self.style_off = None
        self.style = None

    def reload(self):
        self.style = (self.style_off, self.style_on)[self.etat()]

    def get_infos(self):
        return (self.get_name(), self.style)

    def show(self):
        print(self.get_name() + " = " + str(self.etat()))




