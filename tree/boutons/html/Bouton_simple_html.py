from tree.Tree import Tree
from tree.boutons.html.Style import Style
from tree.boutons.Bouton_simple import Bouton_simple



class Bouton_simple_html(Bouton_simple):
    """
    le bouton de l'application web
    """

    def __init__(self, nom, scenar, position):
        Bouton_simple.__init__(self, nom, scenar)
        self.style_on = Style(position, couleur = "green")
        self.style_off = Style(position)
        self.style = (self.style_off, self.style_on)[self.etat()]

    def reload(self):
        self.style = (self.style_off, self.style_on)[self.etat()]

    def show(self):
        print(self.get_name() + " = " + str(self.etat()))




