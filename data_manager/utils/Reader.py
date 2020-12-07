from data_manager.utils.get import get_relay, get_addr, get_triak

class Reader:
    """
    Allow to manage the exception of the reading
    """
    def __init__(self, start, path_file, line = 0, add_line = 1):
        self.start = start
        self.path_file = path_file
        try:
            self.line = self.start.lc.line
        except AttributeError:
            self.line = line
        self.add_line = add_line

    def __iter__(self):
        return [Reader(arg, self.path_file, self.line+i*self.add_line, add_line = self.add_line) for i,arg in enumerate(self.start)].__iter__()

    def __str__(self):
        return str(self.start)

    def __int__(self):
        try:
            return int(self.start)
        except ValueError:
            self.raise_error("{} is not an interger".format(str(self.start)))

    def get(self, arg, method = None, args=[], mandatory = False):
        # run the method at the end
        try:
            new = self.start[arg]
            new_line = self.line + (list(self.start.keys()).index(arg)+1)*self.add_line
            if new in (None, "") and mandatory:
                self.raise_error("The argument {} cannot be empty".format(arg), new_line)
            new_dict = Reader(new, self.path_file, new_line, self.add_line)
        except KeyError:
            if mandatory:
                self.raise_error("The argument {} is not define".format(arg))
            return None

        if method:
            if args:
                method(new_dict, args)
            else:
                method(new_dict)
        return new_dict

    def get_int(self, arg, mandatory = False):
        # allow to return directly an integer
        value = self.get(arg, mandatory = mandatory)
        try:
            return int(value)
        except ValueError:
            self.raise_error("The argument {} need to be an interger".format(arg))

    def get_str(self, arg, mandatory = False):
        return str(self.get(arg, mandatory = mandatory))

    def get_path(self):
        return self.path_file

    def split(self, separator, number = None):
        # allow to split like a string
        splited = str(self.start).split(separator)
        if number and len(splited) != number:
            self.raise_error("The value {} need to have exactly {} arguments".format(str(self.start), number))
        return Reader(splited, self.path_file, self.line, self.add_line)

    def get_addr(self, arg, mandatory = False):
        addr = self.get(arg, mandatory = mandatory)
        if addr:
            pin, board = get_addr(str(addr))
            return Reader({"index":pin, "board":board}, self.path_file, self.line, add_line = 0)
        else:
            return Reader({}, self.path_file, self.line, add_line = 0)

    def get_triak(self):
        # allow to get a triak and raise exception
        if not(self.start):
            self.raise_error("The triak need to be define")
        index = self.get("index", mandatory = True)
        board = self.get("board", mandatory = True)
        try:
            return get_triak(index, board)
        except ValueError:
            self.raise_error("The triak addr {}({}) of need to be interger".format(index, board))
        except (IndexError, NameError) as e:
            self.raise_error("{} in the arg {}({})".format(str(e), index, board))

    def get_relay(self):
        # allow to get a relay and raise exception
        if not(self.start):
            self.raise_error("The relay need to be define")
        index = self.get("index", mandatory = True)
        board = self.get("board", mandatory = True)
        try:
            return get_relay(str(index), str(board))
        except ValueError:
            self.raise_error("The relay addr {}({}) of need to be interger".format(index, board))
        except (IndexError, NameError) as e:
            self.raise_error("{} in the arg {}({})".format(str(e), index, board))


    def get_line(self):
        return self.line

    def raise_error(self, message, line=None):
        if not(line):
            line = self.get_line()
        raise(ValueError("{} at line {} in {}.".format(message, line, self.path_file)))


