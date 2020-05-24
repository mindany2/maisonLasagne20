from In_out.utils.Port_extender import Port_extender
from In_out.cartes.Carte import Carte
from In_out.cartes.Relais import Relais

class Carte_relais(Carte):
    """
    Une carte de relais
    """
    def __init__(self, numero, port_bus, nb_ports = 16):
        Carte.__init__(self, numero, port_bus, nb_ports)
        self.liste_relais = [ Relais(port_bus, 0x13*(i<8)+0x12*(i>7), i%9+1) for i in range(0,nb_ports)]
        """
        for i,pin in enumerate(Port_extender().read(port_bus, registre)):
            self.liste_relais[i].etat = pin
        """
        bus = Port_extender()
        bus.write(port_bus, 0x12, 0xff)
        bus.write(port_bus, 0x13, 0xff)
        bus.write(port_bus, 0x01, 0x0)
        bus.write(port_bus, 0x00, 0x0)

    def get_relais(self, indice_relais):
        return self.liste_relais[indice_relais-1]
        


