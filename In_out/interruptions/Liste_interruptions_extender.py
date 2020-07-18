from In_out.utils.Port_extender import Port_extender
from tree.utils.Dico import Dico
import RPi.GPIO as GPIO

class Liste_interruptions_extender:
    """
    Contient la liste des intérupteurs d'un pin d'intéruption
    """
    def __init__(self, port_interrupt, port_bus, registre): # le registre vaut 0 si A, 1 si B (extender)
        self.port_bus = port_bus
        self.port_interrupt = port_interrupt
        self.liste_inter = Dico()
        self.bus = Port_extender()
        self.add_registre = registre

        # GPINTEN = mettre les intérruptions
        self.bus.write(self.port_bus, 0x04 + self.add_registre, 0xff)

        # INTCON = pour avoir les 2 interruptions
        self.bus.write(self.port_bus, 0x08 + self.add_registre, 0x00)

        # GPPU = resitance
        self.bus.write(self.port_bus, 0x0c + self.add_registre, 0x00)

        # IODIR = sortie / entrée
        self.bus.write(self.port_bus, 0x00 + self.add_registre, 0xff)

        # IOCON =
        self.bus.write(self.port_bus, 0x0a + self.add_registre, 0x02)

        self.bus.read(self.port_bus,0x12 + self.add_registre)

        GPIO.setup(self.port_interrupt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.port_interrupt, GPIO.RISING, callback = self.detect_interrupt)

    def add(self, inter, index):
        print("new inter")
        self.liste_inter.add(index,inter)

    def get_inter(self, nom):
        print(self.liste_inter)
        for inter in self.liste_inter:
            if inter.nom == nom:
                return inter
        return None

    def detect_interrupt(self, event):
        print("interruption {} !!!".format(self.add_registre))
        for i,pin in enumerate(self.bus.read(self.port_bus,0x12 + self.add_registre)):
            # on verifie si le pin est haut
            #TODO il va falloir le modifier pour les radars ect..
            if int(pin) == 1:
                print("le pin {} est on".format(i))
                inter = self.liste_inter.get(i)
                if inter != None:
                    inter.press()

    def show(self):
        print("--- Liste_interruptions ---")
        print(" port_interrupt = {} \n port_bus = {}".format(self.port_interrupt, self.port_bus))
        print("--- Interrupteurs ---")
        self.liste_inter.show()

        


    

    
