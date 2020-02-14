from tree.Bouton import Bouton


class Liste_boutons:
    """
    Contient la liste des boutons d'une page
    soit en html , soit en console MIDI
    """
    def __init__(self, liste_info):
        self.liste_boutons = []
        self.liste_info = liste_info


    def __iter__(self):
        return iter(self.liste_boutons)

    def add(self, bouton):
        self.liste_boutons.append(bouton)

    def show(self):
        for btn in self.liste_boutons:
            btn.show()
