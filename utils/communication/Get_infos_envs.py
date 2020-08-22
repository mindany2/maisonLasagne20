from tree.Tree import Tree
from utils.communication.Message import Message

class Get_infos_envs(Message):

    def __init__(self):
        pass

    def do(self):
        return Tree().get_infos_envi()

