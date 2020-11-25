from tree.utils.Liste import Liste
from tree.utils.Dico import Dico
from tree.scenario.Scenario import MARQUEUR
from tree.boutons.Bouton_principal import Bouton_principal

class Preset:
    """
    Stocke une liste de scenario
    et d'interruptions
    """
    def __init__(self, nom):
        self.nom = nom
        self.liste_scénario = Liste()
        self.
        self.etat = False
        self.lien_inter_bouton = Dico()

    def add_lien_inter(self, nom_inter, bouton):
        self.lien_inter_bouton.add(nom_inter, bouton)

    def get_bouton(self, nom_inter):
        return self.lien_inter_bouton.get(nom_inter)

    def press_inter(self, nom_inter, etat):
        bt = self.get_bouton(nom_inter)
        if bt != None:
            bt.press(etat)
            return True
        return False

    def change_select(self, scenar):
        if scenar != None:
            self.liste_scénario.change_select(scenar)

    def change_etat(self, etat):
        self.etat = etat

    def add_scenar(self, scenar):
        self.liste_scénario.add(scenar)

    def get_scenar(self, nom):
        return self.liste_scénario.get(nom)

    def get_pile(self):
        return self.liste_scénario

    def get_marqueur(self):
        return self.liste_scénario.selected().get_marqueur()

    def do(self):
        self.liste_scénario.selected().do()
    
    def reset(self):
        for scenar in self.liste_scénario:
            scenar.reset()
