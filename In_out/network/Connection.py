from In_out.network.Client import Client
from In_out.network.messages.interrupt.Network_interrupt import Network_interrupt
from In_out.network.messages.get.Get_network_interrupt import Get_network_interrupt
from tree.utils.Locker import Locker
from tree.utils.Logger import Logger
from tree.utils.Dico import Dico
from threading import Thread
from time import sleep,time

TIME_OUT = 1 #s

class Connection(Locker):
    """
    Store connection informations for a network device
    """
    def __init__(self, name, addr, me):
        Locker.__init__(self)
        self.name = name
        self.addr = addr
        self.me = me
        self.client = Client(self.addr)
        self.timeout = 0
        # list of all interrupt press TO the remote device
        self.output_interrupts = []
        # list of all interrupts inputs FROM the remote device
        self.input_interrrupts = Dico()

    def add_input_interrupt(self, name, env_path):
        self.input_interrrupts.add(name, env_path)

    def add_output_interrupt(self, name):
        self.output_interrupts.append(name)

    def send_interrupt(self, name, state):
        if name in self.output_interrupts:
            Logger.info("send {}:{} to {}".format(name, state, self.name))
            self.send(Network_interrupt(self.me, name, state))

    def press_inter(self,getter, name, state):
        if name in self.input_interrrupts.keys():
            getter.get_tree().press_inter(self.input_interrrupts.get(name), name, state)

    def get_input_interrupts(self):
        return list(self.input_interrrupts.keys())

    def initialize(self):
        return
        if self.output_interrupts:
            # check if the interrupts exist remotely
            all_inter = self.send(Get_network_interrupt(self.me))
            if all_inter:
                if isinstance(all_inter, list):
                    for inter in self.output_interrupts:
                        if inter not in all_inter:
                            Logger.error("No link to the interrupt {} for {}".format(inter, self.name))
                else:
                    Logger.error("Exception during interrupt initialization on {} : {}".format(self.name, all_inter))
            else:
                Logger.error("No connection or interrupt to {} at {}".format(self.name, self.addr))

    def send(self, message):
        self.timeout = time()
        if not(self.client.state()):
            if self.client.connect():
                Logger.info("Connect from {}".format(self.name))
                Thread(target=self.check_for_disconnection).start()
            else:
                Logger.error("Could not connect to {} at {}".format(self.name, self.addr))
                return
        data = self.client.send(message)
        return data

    def check_for_disconnection(self):
        """
        check if the connection exceed the TIME_OUT since the last send
        """
        while (time() - self.timeout) < TIME_OUT:
            sleep(0.1)
        Logger.info("Disconnect from {}".format(self.name))
        self.disconnect()

    def disconnect(self):
        self.client.disconnect()


