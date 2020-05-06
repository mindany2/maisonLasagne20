from In_out.Interrupteur import Interrupteur
from In_out.utils.Port_extender import Port_extender
from tree.utils.Dico import Dico
import RPi.GPIO as GPIO
from time import sleep


class Liste_interrupteur:
    """
    Contient la liste des intérupteurs d'un pin d'intéruption
    """
    port_bus = 0x20
    port_interrupt = 12
    liste_inter = Dico()
    # GPINTEN = mettre les intérruptions
    bus = Port_extender()
    bus.write(port_bus, 0x05, 0xff)
    bus.write(port_bus, 0x04, 0xff)

    # INTCON = pour avoir les 2 interruptions
    bus.write(port_bus, 0x09, 0x00)
    bus.write(port_bus, 0x08, 0x00)

    # DEFVAL  
    bus.write(port_bus, 0x09, 0x00)
    bus.write(port_bus, 0x08, 0x00)

    # GPPU = resitance
    bus.write(port_bus, 0x0d, 0xff)
    bus.write(port_bus, 0x0c, 0xff)

    # IODIR = sortie / entrée
    bus.write(port_bus, 0x01, 0xff)
    bus.write(port_bus, 0x00, 0xff)

    # IOCON =
    bus.write(port_bus, 0x0a, 0x02)
    bus.write(port_bus, 0x0b, 0x02)

    bus.read(port_bus,0x12)
    bus.read(port_bus,0x13)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(port_interrupt, GPIO.IN)

    @classmethod
    def init(self):
        self.bus.read(self.port_bus,0x12)
        self.bus.read(self.port_bus,0x13)
        GPIO.add_event_detect(self.port_interrupt, GPIO.RISING, callback = self.interrupt)
        while(1):
            pass

    @classmethod
    def add(self, inter):
        self.liste_inter.add(inter.pin,inter)
        #self.bus.write_pin(self.port_bus, 0x05, inter.pin, 1)

    @classmethod
    def get_inter(self, nom):
        for inter in self.liste_inter:
            if inter.nom == nom:
                return inter
        return None


    @classmethod
    def interrupt(self, event):
        for i,pin in enumerate(self.bus.read(self.port_bus,0x13)):
            if int(pin) == 1:
                print("sur le premier")
                inter = self.liste_inter.get(i+1)
                if inter != None:
                    inter.press()

        for i,pin in enumerate(self.bus.read(self.port_bus,0x12)):
            if int(pin) == 1:
                print("sur le 2eme")
                inter = self.liste_inter.get(i+9)
                if inter != None:
                    inter.press()




    @classmethod
    def show(self):
        print("--- Interrupteurs ---")
        self.liste_inter.show()

if __name__ == "__main__":
    Liste_interrupteur().init()
    while(1):
        sleep(0.25)

        


    

    
