from tree.scenario.Liste_scenarios import Liste_scenarios

class Bouton:
    """
    La base d'un bouton, juste un état
    """

    def __init__(self, nom, mode, liste_scenar = []):
        self.etat = False
        self.nom = nom+"."+mode.nom
        self.mode = mode
        self.liste_scénario = Liste_scenarios()
        for scénar in liste_scenar:
            self.add_scenar(scénar)

    def add_scenar(self, scénar, attente = False):
        self.liste_scénario.add(scénar, attente)

    def change(self):
        self.etat = not(self.etat)

    def do(self):
        self.liste_scénario.do()

    def show(self):
        print("mode = " + str(self.mode) + " nom = " +self.nom + " === " + str(self.etat))
        for scénar in self.liste_scénario:
            scénar.show()
