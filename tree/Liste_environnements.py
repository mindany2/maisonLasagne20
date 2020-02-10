from tree.Environnement import Environnement

class Liste_environnements:
    """
    Contient tous les environnements
    cad lieu 
    """
    def __init__(this):
       this.liste_env = []
       this.liste_info = []

    def add(this, env):
        this.liste_env.append(env)

    def __iter__(this):
        return this.liste_env.iter()

