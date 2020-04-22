from tree.utils.Liste_radios import Liste_radios
from tree.utils.Liste import Liste

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
    def get_mode(self, nom_mode):
        return self.liste_modes.get(nom_mode)

    @classmethod
    def change_mode_select(self, mode):
        self.liste_modes.change_select(mode)
        for env in self.liste_envi:
            env.change_mode()

    @classmethod
    def add_mode(self, mode):
        self.liste_modes.add(mode)

    @classmethod
    def get_current_mode(self):
        return self.liste_modes.selected()

    @classmethod
    def get_env(self, env):
        return self.liste_envi.get(env)

    @classmethod
    def get_scenar(self, nom_env, nom_scenar):
        return self.get_env(nom_env).get_scenar(nom_scenar)
