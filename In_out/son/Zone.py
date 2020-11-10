from In_out.utils.DAX66 import ACTION

class Zone:
    """
    Contient tous les paramètres d'une zone sur l'ampli
    """
    def __init__(self, numero, dax66):
        self.numero = numero
        self.output = dax66
        self.power = 0
        self.volume = 0
        self.mute = 0
        self.distrub = 0
        self.treble = 0
        self.bass = 0
        self.balance = 0
        self.source = 0
        self.get_infos()

    def get_infos(self):
        values = self.output.get_all_infos(self.numero)

        if values:
            pa, self.power,bpower, self.mute, self.distrub, self.volume, self.treble, self.bass, self.balance, self.source, ls = values

        if int(self.source) != 2:
            self.output.send(self.numero, ACTION.source, 2)
            self.source = self.output.get_info(self.numero, ACTION.source)

        if int(self.volume) != 0:
            self.output.send(self.numero, ACTION.volume, 0)
            self.volume = 0

        self.show()


    def set_volume(self, volume):
        if self.volume != volume:
            self.output.send(self.numero, ACTION.volume, volume)
            self.volume = volume


    def set_power(self, valeur):
        if self.power != valeur:
            self.output.send(self.numero, ACTION.power, valeur)
            self.power = valeur

    def show(self):
        print("Zone {}: volume={}, source={}, power={}".format(self.numero,self.volume, self.source, self.power))

