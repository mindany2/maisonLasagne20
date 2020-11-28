from tree.utils.Liste import Liste
from tree.scenario.Scenario import MARQUEUR

class Gestionnaire_scenario:
    """
    Permet de stocker l'ordre des scénarios
    """
    def __init__(self, scenar_init):
        # le scenario selecter :
        #   ce scenario représente la choix sur l'environnement, il ne peut y en avoir qu'un
        #   s'il est OFF, alors nimporte quel autre environnement peut mettre le scenario qu'il veut
        #   sinon c'est le scenario actif car était le prioritaire 
        self.scenario_select = scenar_init
        # stocke dans l'ordre reçu les scenarios secondaire (appels d'autres environnement)
        self.pile = Liste()
        # scenario en cours
        self.scenar = scenar_init
        # on fait le scenario init
        self.do(scenar_init)

    def do(self, scenar):
        # lance le scenario
        self.scenar.set_etat(False)
        self.scenar = scenar
        self.scenar.set_etat(True)
        self.scenar.do()

    def do_scenar_principal(self, scenar):
        """
        cette fonction doit être appeller pour modifier directement l'etat de l'environnement
        (ON, OFF)
        """
        if scenar.get_marqueur() != MARQUEUR.OFF:
            # si on met ON
            self.do(scenar)
        elif self.scenario_select.get_marqueur() == MARQUEUR.OFF:
            # si on était déjà OFF, on impose donc de tout éteindre
            self.do(scenar)
            self.pile = Liste() # on vide la liste
        else: # on fait le premier de la pile s'il existe
            if not(self.pile.est_vide()):
                self.do(self.pile.top())
        # on met le scenario comme principal
        self.scenario_select = scenar

    def do_scenar_secondaire(self, scenar):
        self.pile.push(scenar)
        if self.scenario_select.get_marqueur() == MARQUEUR.OFF:
            self.do(scenar)

    def get_scenar_select(self):
        return self.scenario_select

    def get_scenar_en_cours(self):
        return self.scenar

    def push(self, scenar):
        self.pile.add(scenar)

    def remove(self, scenar):
        self.pile.remove(scenar)
        if self.scenar == scenar: # c'est le scenario en cours
            # on met le scenario adequat
            if self.pile.est_vide() or self.scenario_select.get_marqueur() != MARQUEUR.OFF:
                self.do(self.scenario_select)
            else:
                self.do(self.pile.top())


    def top(self):
        return self.pile.last()

    def get_marker(self):
        # retourne le marqueur du  scenario selecter
        return self.scenario_select.get_marqueur()


