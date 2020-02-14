from scenario.Liste_instructions import Liste_instructions
from threading import Thread

class Bouton:
    """
    La base d'un bouton, juste un état
    """

    def __init__(this, nom):
        this.etat = False
        this.nom = nom
        this.liste_inst = Liste_instructions()

    def add_inst(this, inst):
        this.liste_inst.add(inst)
        

    def change(this):
        this.etat = not(this.etat)

    def do(this):

        process = Thread(target = this.liste_inst.do)
        process.start()

    def show(this):
        print(this.nom)
        for inst in this.liste_inst:
            inst.show()
