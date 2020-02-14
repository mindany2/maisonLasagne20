from tree.Environnement import Environnement

class Liste_environnements:
    """
    Contient tous les environnements
    cad lieu 
    """
    def __init__(self):
       self.liste_env = []
       self.liste_info = []

    def add(self, env):
        self.liste_env.append(env)

    def __iter__(self):
        return self.liste_env.iter()

