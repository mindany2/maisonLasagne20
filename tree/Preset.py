from tree.utils.Pile_radio import Pile_radio
from tree.utils.Dico import Dico
from tree.scenario.Scenario import MARQUEUR
from tree.boutons.Bouton_principal import Bouton_principal

class Preset:
    """
    Il y a une preset par mode
    """
    def __init__(self, nom):
        self.nom = nom
        self.liste_scénario = Pile_radio()
        self.liste_boutons_html = []
        self.etat = False
        self.lien_inter_bouton = Dico()

    def add_lien_inter(self, nom_inter, bouton):
        self.lien_inter_bouton.add(nom_inter, bouton)

    def get_bouton(self, nom_inter):
        return self.lien_inter_bouton.get(nom_inter)

    def principal(self, nom_inter):
        # permet de savoir si le bouton est principal pour l'environnement
        return isinstance(self.get_bouton(nom_inter), Bouton_principal)

    def press_inter(self, nom_inter, etat):
        bt = self.get_bouton(nom_inter)
        if bt != None:
            scenar = bt.press(etat)
            self.change_select(scenar)

    def change_select(self, scenar):
        self.liste_scénario.change_select(scenar)

    def change(self):
        self.etat = not(self.etat)

    def add_boutons_html(self, bt):
        self.liste_boutons_html.append(bt)

    def get_nb_boutons_html(self):
        return len(self.liste_boutons_html)

    def press_bouton_html(self, index):
        bt = self.liste_boutons_html[index]
        self.liste_scénario.change_select(bt.press())

    def get_bouton_html(self, index):
        return self.liste_boutons_html[index]

    def reload_html(self):
        for bt in self.liste_boutons_html:
            bt.reload()

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
    
    def show(self):
        print("Preset "+self.nom)
        self.liste_scénario.show()
