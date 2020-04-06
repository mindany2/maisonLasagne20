from tree.Liste_radios import Liste_radios
from tree.Tree import Tree
from time import sleep

class Interrupteur:
    """
    Ceci est un interrupteur dans la maison
    """
    # mode pousoir par défaut

    def __init__(self, nom, pin, liste_noms_bouton):
        self.nom = nom
        self.pin = pin
        self.liste = Liste_radios()
        for bt in liste_noms_bouton:
            env_nom = bt.split(".")[0]
            nom = bt.split(".")[1]
            bouton = Tree().get_bouton(env_nom, nom)
            self.liste.add(bouton, change = False)
        # permet de pas prendre en compte les interférences
        self.stop = False

    def press(self):
        if not(self.stop):
            print(self.nom)
            self.stop = True
            print(self.liste.element_select.nom)
            print(self.liste.element_select.etat)
            print("ok")
            if self.liste.element_select.etat:
                self.liste.next()
            print(self.liste.element_select.nom)
            print("ok")
            self.liste.element_select.do()
            self.liste.next()
            print(self.liste.element_select.nom)
            sleep(2)
            self.stop = False

    def show(self):
        print(self.nom + " : " + str(self.pin) + " : ")
        self.liste.show()

