from In_out.utils.Port_extender import Port_extender
from tree.utils.Dico import Dico
from time import sleep
from tree.utils.Logger import Logger
try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils
    fake_rpigpio.utils.install()

class List_interrupts_extender:
    """
    The extender have a register by interrupt pin list (8 pins)
    this allow to configurate this register to take interrupt and 
    read it after the interrupt pin of the extender raise
    """
    def __init__(self, extender, port_interrupt, port_bus, register):
        """
        Port_bus = i2c serial port
        port_interrupt = GPIO port link to the interrupt pin on the extender
        register = 0 or 1 for A or B board
        """
        self.port_bus = port_bus
        self.port_interrupt = port_interrupt
        self.list_inter = Dico()
        self.bus = extender
        self.add_register = register

        # GPINTEN = setup interrupt
        self.bus.write(self.port_bus, 0x04 + self.add_register, 0xff)

        # INTCON = to have rising and falling interrupt
        self.bus.write(self.port_bus, 0x08 + self.add_register, 0x00)

        # GPPU = resistors
        self.bus.write(self.port_bus, 0x0c + self.add_register, 0x00)

        # IODIR = setup like input
        self.bus.write(self.port_bus, 0x00 + self.add_register, 0x00)

        # IOCON =
        self.bus.write(self.port_bus, 0x0a + self.add_register, 0x02)

        self.bus.read(self.port_bus,0x12 + self.add_register)

        GPIO.setup(self.port_interrupt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.port_interrupt, GPIO.RISING, callback = self.detect_interrupt)

    def add(self, inter, index):
        self.list_inter.add(index, inter)
        self.bus.write_pin(self.port_bus, 0x00 + self.add_register, index+1, 0)

    def get_inter(self, name):
        return self.list_inter.get(name)

    def detect_interrupt(self, event):
        data = self.bus.read(self.port_bus,0x12 + self.add_register)
        if data == ['0']*8 or data == ['1']*8 or data == None:
            return
        Logger.info("interrupt {} : {}:{} data={}".format(self.port_interrupt, self.port_bus, self.add_register, data))
        for i,pin in enumerate(data):
            # check if the pin is up
            #TODO need to change for the radar..
            if int(pin) == 1:
                Logger.info("pin {} is on".format(i))
                try:
                    self.list_inter.get(i).press()
                    sleep(1)
                    return
                except KeyError:
                    Logger.info("This pin haven't any interrupt on board :\n {}".format(str(self)))

    def __str__(self):
        string = "port : {} | register : {} | gpio : {}\n".format(self.port_bus, self.add_register, self.port_interrupt)
        string += "".join(" - {}\n".format(inter) for inter in self.list_inter)
        return string

    
