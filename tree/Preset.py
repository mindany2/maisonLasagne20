from tree.Liste import Liste

class Preset:
    """
    Il y a une preset par mode
    """
    def __init__(self, nom):
        self.nom = nom
        self.liste_scénario = Liste()

    def add_scenar(self, scenar):
        self.liste_scénario.add(scenar)

    def get_scenar(self, nom):
        self.liste_scénario.get(nom)
    
    def show(self):
        print("Preset "+self.nom)
        self.liste_scénario.show()
