from tree.utils.Liste_radios import Liste_radios

class Preset:
    """
    Il y a une preset par mode
    """
    def __init__(self, nom):
        self.nom = nom
        self.liste_scénario = Liste_radios()
        self.etat = False

    def change(self):
        self.etat = not(self.etat)

    def add_scenar(self, scenar):
        self.liste_scénario.add(scenar)

    def get_scenar(self, nom):
        return self.liste_scénario.get(nom)

    def change_select(self, scenar):
        self.liste_scénario.change_select(scenar)

    def get_marqueur(self):
        return self.liste_scénario.selected().get_marqueur()

    def do(self):
        self.liste_scénario.selected().do()
    
    def show(self):
        print("Preset "+self.nom)
        self.liste_scénario.show()
