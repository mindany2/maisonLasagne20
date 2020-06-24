from time import time, sleep
from In_out.interruptions.utils.Interruption import Interruption
from In_out.utils.Arduino import Arduino, MESSAGE_SLAVE

class Interruption_arduino(Interruption):
    """
    Ceci est un interrupteur dans la maison
    """
    # mode pousoir par défaut

    def __init__(self, nom, pin, client):
        Interruption.__init__(self, nom, pin, client)
        self.temps = time()

    def press(self):
        if ((time() - self.temps) > 1):     # permet de prendre que la premiere interruption
            sleep(0.5)# on attend 1s
            print("la arduino nous demande de la lire")
            #data = Arduino.send_for_request(MESSAGE_SLAVE.rien)
            print("on a reçu ",MESSAGE_SLAVE(data).name)
            self.temps = time() 

    def show(self):
        print(self.nom + " : " + str(self.pin) + " : ")

