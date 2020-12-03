from In_out.network.Client import Client
import RPi.GPIO as GPIO


class Interrupts_manager:
    """
    Static class to list all the interrupt in the process
    """
    list_extender_interrupts = []
    list_others_interrupts = []

    @classmethod
    def init(self):
        # start the client
        GPIO.setmode(GPIO.BCM)
        self.client = Client() # connect to the tree process

    @classmethod
    def add_interrupt_extender(self, inter):
        self.list_extender_interrupts[((inter.pin-1)//8)].add(inter, (inter.pin-1) % 8)

    @classmethod
    def add_interrupt(self, inter):
        self.list_others_interrupts.append(inter)

    @classmethod
    def configure_list_extender(self, list_interrupt_extender):
        self.list_extender_interrupts.append(list_interrupt_extender)









