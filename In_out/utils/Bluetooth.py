from enum import Enum
from bluepy.btle import Peripheral, Scanner
from threading import Lock

class Bluetooth:
    """
    Gère le bluetooth
    """
    mutex = Lock()

    @classmethod
    def connect(self, addresse):
        """
        Retourne le périphérique
        """
        self.mutex.acquire()
        try:
            periph = Peripheral(addresse)
        except:
            self.mutex.release()
            return None
        self.mutex.release()
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
    def get_char(self, periph, uuid, indice):
        service = periph.getServiceByUUID(uuid)
        return service.getCharacteristics(indice)

    @classmethod
    def send(self, char, valeur):
        self.mutex.acquire()
        char[0].write(valeur)
        self.mutex.release()

    @classmethod
    def deconnect(self, periph):
        self.mutex.acquire()
        if periph != None:
            periph.disconnect()
        self.mutex.release()





