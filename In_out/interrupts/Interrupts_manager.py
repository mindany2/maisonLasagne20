from In_out.network.Client import Client
try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils
    fake_rpigpio.utils.install()

class Interrupts_manager:
    """
    class to list all the interrupt in the process
    """
    def __init__(self):
        self.list_extender_interrupts = []
        self.list_others_interrupts = []
        self.client = Client() # connect to the tree process
        self.zigbee = None
        GPIO.setmode(GPIO.BCM)

    def get_client(self):
        return self.client

    def start(self):
        # start the client
        self.client.start()
        for inter in self.list_others_interrupts:
            inter.start()

    def add_interrupt_extender(self, inter):
        self.list_extender_interrupts[((inter.pin-1)//8)].add(inter, (inter.pin-1) % 8)

    def add_interrupt(self, inter):
        self.list_others_interrupts.append(inter)

    def add_zigbee_device(self, device):
        self.zigbee.add_device(device)

    def configure_list_extender(self, list_interrupt_extender):
        self.list_extender_interrupts.append(list_interrupt_extender)

    def get_zigbee(self):
        return self.zigbee

    def add_zigbee(self, zigbee):
        self.zigbee = zigbee

    def __str__(self):
        string = "-"*10 + "Interrupts manager"+"-"*10 + "\n"
        string += "-List_interrupts_extender\n"
        string += "".join(["|  {}\n".format(str(string)) for string in self.list_extender_interrupts])
        string += "-Other insterrupts\n"
        string += "".join(["|  {}\n".format(str(string)) for string in self.list_others_interrupts])
        return string
        









