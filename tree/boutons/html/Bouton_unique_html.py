from tree.Tree import Tree
from tree.boutons.html.style.Style import Style
from tree.boutons.Bouton_unique import Bouton_unique



class Bouton_unique_html(Bouton_unique):
    """
    le bouton de l'application web pour les global
    """

    def __init__(self, nom, env, scenar_on, scenar_off):
        Bouton_unique.__init__(self, nom, env, scenar_on, scenar_off)
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




