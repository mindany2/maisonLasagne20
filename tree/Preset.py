from tree.utils.Liste import Liste
from tree.utils.Dico import Dico
from tree.scenario.Scenario import MARQUEUR
from tree.scenario.Gestionnaire_scenario import Gestionnaire_scenario
from tree.boutons.Bouton_principal import Bouton_principal

class Preset:
    """
    Stocke une liste de scenario
    et d'interruptions
    """
    def __init__(self, nom):
        self.nom = nom
        self.liste_scénario = Liste()
        self.gestion_scenar = None
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

    def change_etat(self, etat):
        self.etat = etat

    def add_scenar(self, scenar):
        self.liste_scénario.add(scenar)
        # on initialise le gestionnaire de scenario
        # avec le premier scenario OFF trouvé
        if not(self.gestion_scenar) and scenar.get_marqueur() == MARQUEUR.OFF:
            self.gestion_scenar = Gestionnaire_scenario(scenar)

    def get_scenar(self, nom):
        return self.liste_scénario.get(nom)

    def get_gestionnaire(self):
        return self.gestion_scenar

    def get_marqueur(self):
        return self.gestion_scenar.get_marqueur()

    def reset(self):
        for scenar in self.liste_scénario:
            scenar.set_etat(False)
