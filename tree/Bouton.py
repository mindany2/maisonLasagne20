from scenario.Liste_instructions import Liste_instructions

class Bouton:
    """
    La base d'un bouton, juste un état
    """

    def __init__(this, nom):
        this.etat = False
        this.nom = nom
        this.liste_inst = Liste_instructions()

    def add_inst(this, inst):
        this.liste_inst.add(isnt)
        

    def change(this):
        this.etat = not(this.etat)

    def do(this):
        this.liste_inst.do()
