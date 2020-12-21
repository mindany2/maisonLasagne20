from tree.connected_objects.Trap import STATE
from tree.scenario.instructions.Instruction import Instruction
from enum import Enum
from time import time, sleep

class TYPE_INST_TRAP(Enum):
    up = 1
    down = 2

class Instruction_trap(Instruction):
    """
    Up or down the trap
    """
    def __init__(self,calculator, trap, action, duration, delay, synchro):
        Instruction.__init__(self, calculator, duration, delay, synchro)
        self.action = action
        self.trap = trap

    def run(self, barrier):
        """
        Setup a try/finally to allow kill from another instruction
        """
        try:
            self.trap.lock()
            if self.action == TYPE_INST_TRAP.down and self.trap.get_state() != STATE.down:
                # descend the trap
                self.trap.set_magnet(False)
                if self.trap.get_state() == STATE.up:
                    self.trap.change(STATE.in_process)
                    super().run()

                if self.trap.test():
                    # this inst was kill, just finish
                    raise SystemExit("kill inst")
                self.trap.go_down()
                time_up = time()
                while(time()-time_up < self.eval(self.duration)):
                    sleep(0.1) # wait resolution
                    if self.trap.test():
                        raise SystemExit("kill inst")
                self.trap.change(STATE.down)

            elif self.action == TYPE_INST_TRAP.up and self.trap.get_state() != STATE.up:
                # rise the trap
                if self.trap.get_state() == STATE.down:
                    self.trap.change(STATE.in_process)
                    super().run()

                if self.trap.test():
                    # this inst was kill, just finish
                    raise SystemExit("kill inst")
                self.trap.go_up()
                self.trap.set_magnet(True)
                time_up = time()
                while(time()-time_up < self.eval(self.duration)):
                    sleep(0.1)
                    if self.trap.test():
                        raise SystemExit("kill inst")
                self.trap.change(STATE.up)

        finally:
            print("the trap is {}".format(self.trap.state))
            self.trap.unlock()

    def finish(self):
        self.trap.kill()

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : trap\n")
        string += "".join("- Action : {}\n".format(self.action))
        return string
