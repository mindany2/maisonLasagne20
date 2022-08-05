
class Dico:
    """
    Redeffinition of dict with usefull methods
    """
    def __init__(self):
        self.list = {}

    def add(self, key, element):
        assert key != None, "The key is None"
        self.list[key] = element

    def get(self, key):
        return self.list[key]

    def next(self, element):
        find = False
        for el in self.list.values():
            if find:
                return el
            if el == element:
                find = True
        assert(find), f"{element} is not in the dict"
        return list(self.list.values())[0]

    def last(self):
        return list(self.list.values())[-1]

    def get_key(self, element):
        for key in self.list.keys():
            if self.list[key] == element:
                return key
        return None

    def __iter__(self):
        return self.list.values().__iter__()

    def keys(self):
        return self.list.keys().__iter__()

    def is_empty(self):
        return self.list == {}

    def zip(self):
        return zip(self.keys(), self.__iter__())

    def clear(self):
        self.list = {}

    def __str__(self):
        return "".join([str(value) + "\n" for value in self.list.values()])

    def __eq__(self, other):
        if isinstance(other, Dico):
            shared_item = [key for key in self.list.keys() if key in other.list and self.list[key] == other.list[key]]
            return len(shared_item) == len(self.list) == len(other.list)

        return False

    def get_index(self, key):
        return list(self.list.keys()).index(key)

    def __len__(self):
        return len(self.list)

    def remove(self, key):
        del self.list[key]

