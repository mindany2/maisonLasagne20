from scenario.Instruction import Instruction

class Liste_instructions:
    """
    Contient une succession d'instructions
    """
    def __init__(this):
        this.liste = []

    def add(this, inst):
        this.liste.append(inst)

    def __iter__(this):
        return this.liste.__iter__()

    def do(this):
        #on fait toute les instructions
        print("coucou je fait des trucs")
        for inst in this.liste:
            # chaque instruction est un thread
            # on le demarre
            inst.start()
            if (inst.attente):
                # on doit attendre que l'instruction se termine
                inst.join()

        #on attend qu'ils aient tous terminé
        for inst in this.liste:
            inst.join()


