import numpy as np

def rgb_to_hexa(r, g, b):
    return "0x"+hex(r)[2:4].zfill(2)+hex(g)[2:4].zfill(2)+hex(b)[2:4].zfill(2)

class Color:
    """
    RGB color
    """
    def __init__(self, value):
        try:
            self.value = value
            self.int_to_rgb()
        except TypeError:
            self.value = "0x"+(8-len(hex(int(value))))*"0"+hex(int(value))[2:]
        self.int_to_rgb()

    def dim(self, dimmer):
        r = int(self.r* float(dimmer)/100)
        g = int(self.g* float(dimmer)/100)
        b = int(self.b* float(dimmer)/100)
        return Color(rgb_to_hexa(r,g,b))

    def set(self, color):
        self.value = color.value

    def int_to_rgb(self):
        self.value = '0x{0:0{1}X}'.format(int(self.value,16),6)
        self.r = int("0x"+self.value[2:4].zfill(2),16)
        self.g = int("0x"+self.value[4:6].zfill(2),16)
        self.b = int("0x"+self.value[6:8].zfill(2),16)
        return [self.r, self.g, self.b]

    def _get_list(self, variable_init, variable_self, nb_dots):
        if variable_init != variable_self:
            return np.arange(variable_init, variable_self+1, float((variable_self - variable_init))/nb_dots) # arange did not keep the last arg
        return [variable_init]*(nb_dots+1)

    def __str__(self):
        return str(self.value)

    def get_with_hash(self):
        return "#"+str(self.value)[2::]

    def __eq__(self, other):
        if isinstance(other, Color):
            return int(self.value,16) == int(other.value,16)
        return False

    def generate_array(self, color_init, nb_dots):
        self.int_to_rgb()
        color_init.int_to_rgb()
        list_red = self._get_list(color_init.r, self.r, nb_dots)
        list_green = self._get_list(color_init.g, self.g, nb_dots)
        list_blue = self._get_list(color_init.b, self.b, nb_dots)
        return [rgb_to_hexa(int(r),int(g),int(b)) for r,g,b in zip(list_red, list_green, list_blue)]

    def is_black(self):
        return int(self.value,16) == 0
    



