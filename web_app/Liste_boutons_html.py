from tree.Dico import Dico

class Liste_boutons_html:

    liste_boutons = Dico()

    @classmethod
    def add_boutons(self,nom,  bouton):
        self.liste_boutons.add(nom, bouton)

    @classmethod
    def __iter__(self):
        return self.liste_boutons.__iter__()

    @classmethod
    def get_bouton(self, nom):
        return self.liste_boutons.get(nom)

    @classmethod
    def show(self):
        print("---- Liste boutons html ----")
        self.liste_boutons.show()
