import re

class Reader:
    """
    Allow to manage the exception of the reading
    """
    def __init__(self, getter, start, path_file, line = 0, add_line = 1):
        self.start = start
        self.getter = getter
        self.path_file = path_file
        try:
            self.line = self.start.lc.line
        except AttributeError:
            self.line = line
        self.add_line = add_line

    def get_getter(self):
        return self.getter

    def __iter__(self):
        return [Reader(self.getter, arg, self.path_file, self.line+i, add_line = self.add_line) for i,arg in enumerate(self.start)].__iter__()

    def __str__(self):
        return str(self.start)

    def __int__(self):
        if self.start == None:
            return None
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
            new_dict = Reader(self.getter, new, self.path_file, new_line, self.add_line)
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
        except (ValueError, TypeError):
            if mandatory:
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
        return Reader(self.getter, splited, self.path_file, self.line, self.add_line)

    def get_addr(self, arg, mandatory = False):
        addr = self.get(arg, mandatory = mandatory)
        if addr:
            pin, board = self.getter.get_addr(str(addr))
            return Reader(self.getter, {"index":pin, "board":board}, self.path_file, self.line, add_line = 0)
        else:
            return Reader(self.getter, {}, self.path_file, self.line, add_line = 0)

    def get_triak(self):
        # allow to get a triak and raise exception
        if not(self.start):
            self.raise_error("The triak need to be define")
        index = self.get("index", mandatory = True)
        board = self.get("board", mandatory = True)
        try:
            return self.getter.get_triak(index, board)
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
            return self.getter.get_relay(str(index), str(board))
        except ValueError:
            self.raise_error("The relay addr {}({}) of need to be interger".format(index, board))
        except (IndexError, NameError) as e:
            self.raise_error("{} in the arg {}({})".format(str(e), index, board))

    def get_object(self, env, type_obj):
        # allow to get an environnement object
        try:
            obj = self.getter.get_object(env, str(self.start))
            assert(isinstance(obj, type_obj))
            return obj
        except NameError as e:
            self.raise_error(str(e))
        except AssertionError:
            self.raise_error("The type {} is not available to perform this task, try: {}"
                    .format(type(obj).__name__,[type.__name__ for type in type_obj]))

    def get_scenarios(self, get_all=False):
        # Cut the name like 
        # env1.env2.preset.scenar1, scenar2
        match = re.match(r'(?P<env>([\w\.]*))\.(?P<preset>([^\.]*))\.(?P<scenar1>([^\,]*))', str(self.start))
        if match:
            name_env, name_preset, name_scenars = match.group("env"), match.group("preset"), [match.group("scenar1")]
        else:
            self.raise_error("Could not found a scenario like : env1.env2.preset1.scenar1, scenar2")
        match = re.match(r'[^\,]*\,[ ]*(?P<scenar2>([\w\.]*))', str(self.start))
        if match:
            name_scenars.append(match.group("scenar2"))

        try:
            env = self.getter.get_env(name_env)
            preset = self.getter.get_preset(env, name_preset)
            scenars = self.getter.get_scenario(preset, name_scenars)
        except (KeyError, NameError) as e:
            self.raise_error("{} on the research of the scenario {}".format(str(e), str(self.start)))
        if get_all:
            return env, preset, scenars
        return scenars[0]

    def get_wait_for_beat(self):
        match = re.match(r'bpm_(?P<number>([0-9]*))[ ]*\+[ ]*(?P<delay>(.)*)', str(self.start))
        wait_for_beat = 0
        if match:
            # bpm delay
            try:
                wait_for_beat, self.start = int(match.group("number")), Reader(self.getter, match.group("delay"), self.path_file)
            except ValueError:
                self.raise_error("The bpm number need to be interger like this : \"bpm_(int) + delay\"")
        return wait_for_beat

    def get_line(self):
        return self.line

    def raise_error(self, message, line=None):
        if not(line):
            line = self.get_line()
        raise(ValueError("{} at line {} in {}.".format(message, line, self.path_file)))


