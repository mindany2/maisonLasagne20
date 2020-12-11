
class Dico:
    """
    Redeffinition of dict with usefull methods
    """
    def __init__(self):
        self.list = {}

    def add(self, key, element):
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
        assert(find)
        return list(self.list.values())[0]

    def last(self):
        return self.list.values()[-1]

    def sort(self):
        # return a sorted list of the elements
        return sorted(list(self.list.values()))


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

    def clear(self):
        self.list = {}

    def __str__(self):
        return "".join([str(value) + "\n" for value in self.list.values()])

    def __len__(self):
        return len(self.list)

    def remove(self, key):
        del self.list[key]

