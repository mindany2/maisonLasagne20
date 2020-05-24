from tree.utils.Liste_radios import Liste_radios
from tree.utils.Dico import Dico

class Preset:
    """
    Il y a une preset par mode
    """
    def __init__(self, nom):
        self.nom = nom
        self.liste_scénario = Liste_radios()
        self.liste_boutons_html = []
        self.etat = False
        self.lien_inter_bouton = Dico()

    def add_lien_inter(self, nom_inter, bouton):
        self.lien_inter_bouton.add(nom_inter, bouton)

    def press_inter(self, nom_inter):
        bt = self.lien_inter_bouton.get(nom_inter)
        if bt != None:
            scenar = bt.press()
            print("iiiiiiiiiiiiiiciiiiiiiiiiiiiii")
            print(scenar.nom)
            self.change_select(scenar)

    def change(self):
        self.etat = not(self.etat)

    def add_boutons_html(self, bt):
        self.liste_boutons_html.append(bt)

    def is_present(self, index_str):
        return int(index_str) < len(self.liste_boutons_html)

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

    def change_scenario_prec(self, scenar):
        self.liste_scénario.change_precedent(scenar)

    def get_scenario_prec(self):
        return self.liste_scénario.precedent()

    def change_select(self, scenar):
        self.liste_scénario.change_select(scenar)

    def get_marqueur(self):
        return self.liste_scénario.selected().get_marqueur()

    def get_marqueur_precedent(self):
        return self.liste_scénario.precedent().get_marqueur()


    def do(self):
        self.liste_scénario.selected().do()
    
    def show(self):
        print("Preset "+self.nom)
        self.liste_scénario.show()
