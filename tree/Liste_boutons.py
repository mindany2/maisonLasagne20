from tree.Bouton import Bouton


class Liste_boutons:
    """
    Contient la liste des boutons d'une page
    soit en html , soit en console MIDI
    """
    def __init__(this, liste_info):
        this.liste_boutons = []
        this.liste_info = liste_info


    def __iter__(this):
        return iter(this.liste_boutons)

    def add(this, bouton):
        this.liste_boutons.append(bouton)

    def show(this):
        for btn in this.liste_boutons:
            btn.show()
