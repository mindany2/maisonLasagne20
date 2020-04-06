from tree.Liste_radios import Liste_radios
from tree.Liste import Liste

class Tree:
    liste_envi = Liste()
    liste_modes = Liste_radios()

    @classmethod
    def show(self):
        print("modes : ")
        self.liste_modes.show()
        print("Environnements : ")
        self.liste_envi.show()

    @classmethod
    def get_mode(self, mode):
        return self.liste_modes.get(mode)

    @classmethod
    def get_current_mode(self):
        return self.liste_modes.element_select

    @classmethod
    def get_env(self, env):
        return self.liste_envi.get(env)

    @classmethod
    def get_bouton(self, nom_env, nom_bouton):
        return self.get_env(nom_env).get_bouton(nom_bouton)
