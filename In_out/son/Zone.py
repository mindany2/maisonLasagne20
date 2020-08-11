from In_out.utils.DAX66 import ACTION

class Zone:
    """
    Contient tous les paramètres d'une zone sur l'ampli
    """
    def __init__(self, numero, dax66):
        self.numero = numero
        self.output = dax66

        values = self.output.get_all_infos(self.numero)

        pa, self.power,self.mute, self.distrub, self.volume, self.treble, self.bass, self.balance, self.source, ls = values

    def set_volume(self, volume):
        self.output.send(self.numero, ACTION.volume, volume)

    def set_power(self, valeur):
        self.output.send(self.numero, ACTION.power, valeur)

    def reload(self):
        self.output.send(self.numero, ACTION.volume, self.volume)
        self.output.send(self.numero, ACTION.power, self.power)
        self.output.send(self.numero, ACTION.source, self.source)


