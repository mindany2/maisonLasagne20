from tree.utils.Liste import Liste_radios

class Gestionnaire_scenario:
    """
    Permet de stocker l'ordre des scénarios
    """
    def __init__(self):
        self.scenario_select = None
        self.pile = Liste_radios

