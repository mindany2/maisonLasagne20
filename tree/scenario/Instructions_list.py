from threading import Thread, Barrier
from numpy import cumsum
from time import time, sleep

class Instructions_list:
    """
    Manage a list of instructions
    with an id_list to compare scenario
    """
    def __init__(self, loop, calculator):
        self.list = []
        self.list_barrier = [0]
        self.loop = loop
        self.state = False
        self.calculator = calculator

    def set_state(self, state):
        if not(state):
            # finish all the instruction in process
            self.finish()
        self.state = state

    def finish(self):
        for inst in self.list:
            process = Thread(target=inst.finish)
            process.name = "Finish {}".format(inst)
            process.start()

    def add(self, inst):
        self.list.append(inst)
        self.list_barrier[-1] += 1
        if not(inst.synchro):
            # need a new barrier
            self.list_barrier.append(0)
    """
    # TODO 
    def __eq__(self, other):
        if isinstance(other, Instructions_list):
            if len(self.list) == 0 or len(other.list) == 0:
                return False

            for inst1 in self.list:
                for inst2 in other.list:
                    if not(inst1 == inst2):
                        return False
            return True
        return False
    """

    def __iter__(self):
        return self.list.__iter__()

    def do(self, finish=False):
        while True:
            #do all the instructions
            list_thread = []
            list_barriers = [Barrier(i) for i in self.list_barrier]
            cummulative_sum = cumsum(self.list_barrier)
            # start all the thread
            for i,inst in enumerate(self.list):
                n = sum([int(i+1 > j) for j in cummulative_sum])
                bar = list_barriers[n]
                if inst.wait_precedent():
                    for proc in list_thread:
                        proc.join()
                    list_thread = []
                process = Thread(target=inst.run, args=[bar])
                process.name = str(inst)
                list_thread.append(process)
                process.start()

            # waiting for all thread to finish
            for proc in list_thread:
                proc.join()
            if not(self.loop and self.state):
                break
        if finish:
            self.finish()

    def get_state(self):
        return self.state

    def initialize(self):
        for inst in self.list:
            inst.initialize()

    def __str__(self):
        string = ""
        if self.loop:
            string += "- Loop\n"
        for inst in self.list:
            string += "\n"
            string += "".join(["   |{}\n".format(string) for string in str(inst).split("\n")])
        return string


