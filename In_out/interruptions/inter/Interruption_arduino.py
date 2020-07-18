from time import time, sleep
from In_out.interruptions.inter.Interruption import Interruption
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
        sleep(0.1)
        print("la arduino nous demande de la lire")
        data = Arduino.send_for_request(MESSAGE_SLAVE.rien)
        try:
            print("on a reçu ",MESSAGE_SLAVE(data).name)
        except:
            data = Arduino.send_for_request(MESSAGE_SLAVE.rien)
            try:
                print("on a reçu ",MESSAGE_SLAVE(data).name)
            except:
                #raise(Exception("erreur de lecture, on a reçu {}".format(data)))
                pass
        if data != 0:
            sleep(0.1)
            self.client.send_request("press_inter",["arduino_"+MESSAGE_SLAVE(data).name])

    def show(self):
        print(self.nom + " : " + str(self.pin) + " : ")

