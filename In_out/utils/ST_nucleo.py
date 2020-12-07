from enum import Enum
from time import sleep
from threading import Lock, Thread
from serial import Serial
from tree.utils.Logger import Logger

class STATE_TRIAK(Enum):
    """
    Manage the triak to be always ON or OFF
    or dimmable
    """
    dimmer = 3
    on = 1
    off = 2


class ST_nucleo:
    """
    Talk to a ST_nucleo card with the triak program on it:
    https://tinyurl.com/stnucleo
    dev_file/st_nucleo/Maison.bin
    """

    def __init__(self, name, addr):
        try:
            self.port = Serial(addr, baudrate=9600)
        except:
            Logger.error("The st_nucleo {} could not open it's port {}".format(name, addr))
            self.port = None

        self.name = name
        self.mutex = Lock()
        self.addr = addr
        self.list_boards_triak = {}

    def add_board_triak(self, board):
        self.list_boards_triak[board.number] = board

    def nb_boards(self):
        return len(self.list_boards_triak)

    def get_board_triak(self, index):
        try:
            return self.list_boards_triak[index]
        except:
            return None

    def set_triak(self, index_board, triak, valeur, state):
        self.mutex.acquire()
        carte = self.list_boards_triak[index_board]
        v1 = valeur // 255 +1 
        v2 = valeur  % 255 +1
        if v1 > 255:
            v1 = 255
        if chr(v2) == "\n":
            v2 += 1
        if self.port:
            self.port.write([carte, triak, v1, v2, state.value])
        sleep(0.02) # time needed to make sure all data succeed
        self.mutex.release()

    def __str__(self):
        string = self.name + "\n"
        string += "".join("- Addr : {}\n".format(self.addr))
        string += "".join("- Boards :\n")
        string += "".join(["|-{}\n".format(string) for string in self.list_boards_triak.values()])
        return string

