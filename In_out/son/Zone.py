from In_out.utils.DAX66 import ACTION

class Zone:
    """
    Contient tous les paramètres d'une zone sur l'ampli
    """
    def __init__(self, numero, dax66):
        self.numero = numero
        self.output = dax66

        values = self.output.get_all_infos(self.numero)

        if values:

            pa, self.power,bpower, self.mute, self.distrub, self.volume, self.treble, self.bass, self.balance, self.source, ls = values

            if int(self.source) != 2:
                self.output.send(self.numero, ACTION.source, 2)
                self.source = 2

            print("fin init zone " + str(numero) + " source = "+ str(self.source))
        else:
            self.power = 0
            self.volume = 0

    def set_volume(self, volume):
        self.output.send(self.numero, ACTION.volume, volume)
        self.volume = volume


    def set_power(self, valeur):
        self.output.send(self.numero, ACTION.power, valeur)
        self.power = valeur


