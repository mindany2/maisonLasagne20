from eclairage.Lumiere import Lumiere

class Liste_lumieres:
    """
    Contient le dictionnaire qui lie les
    lumières et leur nom
    """
    def __init__(this):
        this.dictionnaire = dict()

    def add(this, lumière):
        this.dictionnaire[lumière.nom] = lumière

    def get(this, nom):
        return this.dictionnaire[nom]


