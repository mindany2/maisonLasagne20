from tree.Tree import Tree
from utils.communication.Message import Message

class Press_inter(Message):

    def __init__(self, nom, etat):
        self.nom= nom
        self.etat = etat

    def do(self):
        Tree().press_inter(self.nom, self.etat)
