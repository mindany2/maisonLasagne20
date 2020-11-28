from tree.boutons.html.Bouton_html_modes import Bouton_html_modes
from tree.Tree import Tree
from tree.utils.Dico import Dico

class Mode:
    """
    Ceci est un mode qui permet de changer rapidement
    de preset
    """
    def __init__(self, nom, css_file, couleur, scenar_init):
        self.nom = nom
        self.etat = False
        self.bouton_change_html = Bouton_html_modes(self.nom)
        self.scenar_init = scenar_init

    def press_bouton_mode(self):
        self.bouton_change_html.press()
        Tree().reload_modes()

    def show(self):
        print(self.nom)

    def __str__(self):
        return self.nom

    def change(self):
        self.etat = not(self.etat)
        if self.etat and self.scenar_init:
            env, preset, nom = self.scenar_init.split(".")
            scenar = Tree().get_scenar(env, nom, preset = preset)
            if scenar:
                scenar.do()
