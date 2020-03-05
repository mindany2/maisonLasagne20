from tree.Environnement import Environnement

class Liste_environnements:
    """
    Contient tous les environnements
    cad lieu 
    """
    def __init__(self):
       self.liste_env = {}

    def add(self, env):
        self.liste_env[env.nom] = env

    def get_env(self, nom):
        env = self.liste_env[nom]
        return env

    def __iter__(self):
        return self.liste_env.values().__iter__()

    def show(self):
        for env in self.liste_env.values():
            env.show()


