from In_out.utils.Port_extender import Port_extender
from In_out.cartes.relais.Carte_relais import Carte_relais
from In_out.cartes.relais.Relais_port_extender import Relais_port_extender

class Carte_relais_extender(Carte_relais):
    """
    Une carte de relais
    """
    def __init__(self, extender, numero, port_bus, nb_ports = 16):
        Carte_relais.__init__(self, numero, port_bus, nb_ports)
        self.liste_relais = [ Relais_port_extender(extender, port_bus, 0x13*(i<8)+0x12*(i>7), i%8+1) for i in range(0,nb_ports)]
        """
        for i,pin in enumerate(Port_extender().read(port_bus, registre)):
            self.liste_relais[i].etat = pin
        """
        self.bus = extender
        self.bus.write(port_bus, 0x12, 0xff)
        self.bus.write(port_bus, 0x13, 0xff)
        self.bus.write(port_bus, 0x01, 0x0)
        self.bus.write(port_bus, 0x00, 0x0)

        # on met des resistances
        self.bus.write(port_bus, 0x0d, 0xff)
        self.bus.write(port_bus, 0x0c, 0xff)



