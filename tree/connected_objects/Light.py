from tree.utils.Locker import Locker

class Light(Locker):
    """
    Parent class of all lights
    """
    def __init__(self, name):
        Locker.__init__(self)
        self.name = name
   
    def repair(self):
        return False
        
