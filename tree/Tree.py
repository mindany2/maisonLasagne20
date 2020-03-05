from tree.Liste_environnements import Liste_environnements

class Tree:
    liste_envi = Liste_environnements()

    @classmethod
    def show(self):
        self.liste_envi.show()

    @classmethod
    def __iter__(self):
        return self.liste_envi.__iter__()

    @classmethod
    def get_env(self, env):
        return self.liste_envi.get_env(env)

    @classmethod
    def get_bouton(self, nom_env, nom_bouton):
        return self.get_env(nom_env).get_bouton(nom_bouton)
