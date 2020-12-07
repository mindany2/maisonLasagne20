from tree.utils.Locker import Locker

class Connected_object(Locker):
    """
    Parent class of all connected objects
    """
    def __init__(self, name):
        Locker.__init__(self)
        self.name = name
   
    def repair(self):
        return False


    def __str__(self):
        return self.name + "\n"
