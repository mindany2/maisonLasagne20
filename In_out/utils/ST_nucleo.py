from In_out.utils.I2C import I2C


class ST_nucleo:
    """
    Carte pour les triacs
    """

    i2c = I2C()
    ip = 0x10

    @classmethod
    def set(self, carte, triac, valeur):
        v1 = valeur // 255
        v2 = valeur  % 255
        self.i2c.write_data(self.ip, [carte, triac, v1, v2])
