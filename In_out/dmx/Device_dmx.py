class Device_dmx:
    """
    Cette class permet de stocker l'addresse
    d'une lumiere dmx
    """

    def __init__(self, dmx, addr):
        self.dmx = dmx
        self.addr = addr

    def set(self, option, valeur):
        # option = channel de l'option en enum
        self.dmx.set_channel(self.addr.value + option - 1, valeur)
