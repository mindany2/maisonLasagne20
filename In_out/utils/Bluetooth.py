from enum import Enum
from bluepy.btle import Peripheral, Scanner
from threading import Lock
from time import sleep,time
import os

class Bluetooth:
    """
    Gère le bluetooth
    """
    mutex_connect = Lock()
    mutex_deconnect = Lock()
    mutex_send = Lock()
    mutex_reset = Lock()
    nb_connection = 0
    reset = 0

    @classmethod
    def connect(self, addresse):
        """
        Retourne le périphérique
        """
        try:
            print("on tente de se connecte")
            periph = Peripheral(addresse)
            print("on y est arrive")
        except:
            print("erreur de connection")
            return None
        self.mutex_connect.acquire()
        self.nb_connection += 1
        print("nb connection = {}".format(self.nb_connection))
        self.mutex_connect.release()
        return periph

    @classmethod
    def connect_by_scan(self, addresse):
        try:
            scan = Scanner()
        except:
            return None
        devices = scan.scan(1, passive = True)
        for dev in devices:
            if (dev.addr == addresse):
                try:
                    return Peripheral(dev)
                except:
                    return None
    @classmethod
    def restart(self):
        self.mutex_reset.acquire()
        if not(self.reset):
            print("on reset le bluetooth")
            self.reset = True
            self.mutex_reset.release()
            # pas besoin de mutex on ne fait que lire
            # on attend qu'il n'y ai plus rien de co
            debut = time()
            while self.nb_connection > 0 and time()-debut < 30:
                print("on est bloquer, nombre de connection = {}".format(self.nb_connection))
                sleep(1)

            # on restart le bluetooth
            os.system("sudo systemctl restart bluetooth")
            print("on a reset")
            sleep(20)
            self.mutex_reset.acquire()
            self.reset = False
        self.mutex_reset.release()

    @classmethod
    def get_char(self, periph, uuid, indice):
        try:
            service = periph.getServiceByUUID(uuid)
            return service.getCharacteristics(indice)
        except:
            return None

    @classmethod
    def send(self, char, valeur):
        self.mutex_send.acquire()
        try:
            char[0].write(valeur)
        except:
            print("erreur de connection durant l'envoi")
            self.mutex_send.release()
            return 1
        self.mutex_send.release()
        return 0

    @classmethod
    def deconnect(self, periph):
        if periph != None:
            try:
                self.mutex_deconnect.acquire()
                periph.disconnect()
                self.mutex_deconnect.release()
            except:
                print("erreur de deconnection")
                pass
            self.mutex_connect.acquire()
            self.nb_connection -= 1
            self.mutex_connect.release()





