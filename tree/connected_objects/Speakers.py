from tree.connected_objects.Connected_object import Connected_object

class Speakers(Connected_object):
    """
    A pair of speakers, link to a zone and an amp
    """

    def __init__(self, name, amp, zone):
        Connected_object.__init__(self, name)
        self.amp = amp
        self.zone = zone
        self.connected = False

    def volume(self):
        return self.zone.volume

    def connect(self):
        if not(self.connected) and self.volume() == 0:
            self.amp.power_on()
            self.connected = True

    def disconnect(self):
        if self.connected and self.volume() == 0:
            self.amp.power_off()
            self.connected = False

    def change_volume(self, value):
        if value == 0:
            self.zone.set_power(0)
        elif value != 0 and self.zone.power == 0:
            self.zone.set_power(1)
        self.zone.set_volume(value)

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : speakers\n")
        string += "".join("- Zone : {}\n".format(self.zone))
        string += "".join("- Amp : {}\n".format(self.amp))
        return string


