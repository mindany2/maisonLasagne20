from tree.utils.Dico import Dico
from web_app.boutons.Bouton_html_modes import Bouton_html_modes
from web_app.boutons.Bouton_html import Bouton_html
from web_app.boutons.Liste_boutons_env_html import Liste_boutons_env_html
from web_app.boutons.Style import Style
from tree.Tree import Tree

class Liste_boutons_html:

    liste_boutons_env = Dico()
    liste_boutons_tree = Dico()
    bouton_mode = Bouton_html_modes()
    
    """ 
    Contient la liste des listes d'envrionnements avec les boutons html
    """
    index = 0

    @classmethod
    def add_boutons_env(self, bouton, preset):
        env = bouton.env
        if self.liste_boutons_env.get(env) == None:
            self.liste_boutons_env.add(env, Liste_boutons_env_html(self.index))
            self.index += 1
        self.liste_boutons_env.get(env).add_boutons(bouton, preset)

    @classmethod
    def add_boutons_global(self, bouton):
        #TODO
        pass

    @classmethod
    def change_select(self, bt):
        self.liste_boutons_env.get(bt.env).change_select(bt)

    @classmethod
    def __iter__(self):
        yield self.bouton_mode
        for liste in self.liste_boutons_env:
            for bt in liste:
                yield bt
        for bt in self.liste_boutons_tree:
            yield bt

    @classmethod
    def get_bouton(self, bouton_id):
        if bouton_id.count(".") != 0:
            nom_env = bouton_id.split(".")[0]
            nom_preset = bouton_id.split(".")[1]
            nom_bouton = bouton_id.split(".")[2]
            env = Tree().get_env(nom_env)
            preset = env.get_preset(nom_preset)
            return self.liste_boutons_env.get(env).get_bouton(preset, nom_bouton)
        else:
            if bouton_id == "mode":
                return self.bouton_mode

    @classmethod
    def show(self):
        print("---- Liste boutons html ----")
        self.liste_boutons_env.show()
