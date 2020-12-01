from In_out.external_boards.Triak import Triak
from In_out.external_boards.Board import Board

class Board_triak(Board):
    """
    A triak board : 
    https://tinyurl.com/8triakboard
    """
    def __init__(self, number, stnucleo, nb_ports = 8):
        Board.__init__(self, number, nb_ports)
        self.liste_triak = [ Triak(number, i, stnucleo) for i in range(1,nb_ports+1)]


    def get_triak(self, indice_triak):
        return self.liste_triak[indice_triak-1]
