from In_out.interrupts.Interrupts_manager import Interrupts_manager
from utils.Data_change.Create_inputs import get_interruptions
from utils.Data_change.Create_config import get_config_inter

get_config_inter()
get_interruptions()

from threading import Event

Event().wait()
