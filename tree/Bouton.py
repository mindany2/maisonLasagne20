from scenario.Liste_instructions import Liste_instructions

class Bouton:
    """
    La base d'un bouton, juste un état
    """

    def __init__(self, nom):
        self.etat = False
        self.nom = nom
        self.liste_inst = Liste_instructions()

    def add_inst(self, inst):
        self.liste_inst.add(inst)
        

    def change(self):
        self.etat = not(self.etat)

    def do(self):
        self.liste_inst.do()

    def show(self):
        print(self.nom)
        for inst in self.liste_inst:
            inst.show()
