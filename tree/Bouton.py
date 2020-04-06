from tree.scenario.Liste_scenarios import Liste_scenarios

class Bouton:
    """
    La base d'un bouton, juste un état
    """

    def __init__(self, nom, liste_scenar = []):
        self.etat = False
        self.nom = nom
        self.liste_scénario = Liste_scenarios()
        for scénar in liste_scenar:
            self.add_scenar(scénar)

    def add_scenar(self, scénar, attente = False):
        self.liste_scénario.add(scénar, attente)

    def change(self):
        self.etat = not(self.etat)

    def change_liste_scenario(self, nom, liste_scenar = []):
        self.nom = nom
        self.liste_scénario = Liste_scenarios()
        for scénar in liste_scenar:
            self.add_scenar(scénar)


    def do(self):
        self.liste_scénario.do()

    def show(self):
        for scénar in self.liste_scénario:
            scénar.show()
