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
        self.dmx.set(self.addr + option.value - 1, valeur)
