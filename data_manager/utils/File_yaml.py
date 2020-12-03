import yaml

class File_yaml:
    """
    Read a yaml file
    """
    def __init__(self, path):
        self.config_file = open(path)
        self.dict = Dict(yaml.load(self.config_file, Loader=yaml.FullLoader))
        self.config_file.close()

    def get(self, arg, method = None):
        return self.dict.get(arg, method)

class Dict:
    """
    Allow to manage the exception of the reading
    """
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        return self.start.__iter__()

    def __int__(self):
        return int(self.start)

    def get(self, arg, method = None):
        # run the method at the end
        try:
            new_dict = Dict(self.start[arg])
        except:
            return None

        if method:
            method(new_dict)
        return new_dict


