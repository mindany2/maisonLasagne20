from In_out.interrupts.Interrupts_manager import Interrupts_manager
from data_manager.read_interrupt.configure_boards import configure_boards
from data_manager.read_interrupt.configure_interrupt import config_interrupt
from threading import Event


manager = Interrupts_manager()

configure_boards(manager)
config_interrupt(manager)

manager.start()

Event().wait()
