from enum import Enum
try:
    from bluepy.btle import Peripheral, Scanner
except ModuleNotFoundError:
    print("No bluetooth")
from threading import Lock
from time import sleep,time
import os
from tree.utils.Logger import Logger

class Bluetooth:
    """
    Backend bluetooth
    """
    mutex_connect = Lock()
    mutex_disconnect = Lock()
    mutex_send = Lock()
    mutex_reset = Lock()
    nb_connection = 0
    reset = 0

    @classmethod
    def connect(self, addresse):
        """
        return the new peripheric
        """
        try:
            periph = Peripheral(addresse)
        except:
            return None
        self.mutex_connect.acquire()
        self.nb_connection += 1
        self.mutex_connect.release()
        return periph

    @classmethod
    def connect_by_scan(self, addresse):
        # another way to connect 
        # unused now
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
        """
        Restart the bluetooth of the rpi 
        NEEDED FOR LONG TIME RUNNING RPI
        """
        self.mutex_reset.acquire()
        if not(self.reset):
            Logger.info("Want to reset the bluetooth")
            self.reset = True
            self.mutex_reset.release()
            # just wait until all devices are disconnected
            debut = time()
            while self.nb_connection > 0 and time()-debut < 30:
                sleep(1)

            # on restart le bluetooth
            self.mutex_disconnect.acquire()
            os.system("sudo systemctl restart bluetooth")
            Logger.info("Bluetooth restart")
            sleep(20)
            self.mutex_disconnect.release()
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
            Logger.error("Connection error in the bluetooth sending")
            self.mutex_send.release()
            return 1
        self.mutex_send.release()
        return 0

    @classmethod
    def disconnect(self, periph):
        if periph != None:
            try:
                self.mutex_disconnect.acquire()
                periph.disconnect()
                periph = None
                self.mutex_disconnect.release()
            except BrokenPipeError as e:
                Logger.error("Bluetooth disconnection error : "+str(e))
                self.restart()
            self.mutex_connect.acquire()
            self.nb_connection -= 1
            self.mutex_connect.release()





