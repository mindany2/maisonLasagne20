from tree.scenario.Instruction_enceinte import Instruction_enceinte
from threading import Thread, Lock
from tree.scenario.Scenario import MARQUEUR

class Enceintes:
    """
    Gère une paire d'enceinte
    ( lier a une zone )
    """

    def __init__(self, nom, ampli, zone, nom_env):
        self.nom = nom
        self.ampli = ampli
        self.zone = zone
        self.mutex = Lock()
        self.nom_env = nom_env

        self.volume = self.zone.volume
        self.power = self.zone.power

    def change_volume(self, valeur, save_valeurs):
        if self.ampli.etat():
            if valeur == 0:
                self.zone.set_power(0)
            elif valeur != 0 and self.zone.power == 0:
                self.zone.set_power(1)

            # si l'ampli est allumer
            self.zone.set_volume(valeur)
        if save_valeurs:
            self.volume = valeur
            self.power = (valeur != 0)

    def reload(self, etat):
        # on met l'ampli dans le bon etat
        print("Reload enceinte")

        self.mutex.acquire()

        if etat:
            self.ampli.allumer()

            # met le son dans la zone
            inst = Instruction_enceinte(self, self.volume, 5, 0, False)
            self.volume = self.zone.volume

            proc = Thread(target=inst.run, args = [None])
            proc.start()

        else:
            # enleve le son dans la zone
            inst = Instruction_enceinte(self, 0, 5, 0, False)
            proc = Thread(target=inst.run, args = [None, False])
            proc.start()
        self.mutex.release()

    def show(self):
        print("Enceinte " + str(self.zone.numero))

    def lock(self):
        self.mutex.acquire()

    def unlock(self):
        self.mutex.release()
