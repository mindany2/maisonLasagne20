from tree.utils.Dico import Dico
from web_app.boutons.Bouton_html_env import Bouton_html_env
from tree.Tree import Tree

class Liste_boutons_env_html:

    """ 
    Contient la liste des listes d'envrionnements avec les boutons html
    """
    def __init__(self, index):
        self.liste_boutons = Dico()
        self.index = index
        self.position = 0


    def add_boutons(self, bouton, preset):
        if self.liste_boutons.get(preset) == None:
            self.liste_boutons.add(preset, Dico())
        self.liste_boutons.get(preset).add(bouton.nom,Bouton_html_env(bouton, (self.index, self.position)))
        self.position += 1

    def change_select(self, bt):
        preset = bt.env.get_preset_select()
        self.liste_boutons.get(preset).change_select(bt)

    def __iter__(self):
        for liste in self.liste_boutons:
            for bt in liste:
                yield bt

    def get_bouton(self, preset, nom_bouton):
        return self.liste_boutons.get(preset).get(nom_bouton)

    def show(self):
        print("---- Liste boutons html ----")
        self.liste_boutons.show()
