
def get_int(arg, exception = TypeError()):
    try:
        return int(arg)
    except ValueError:
        raise(exception)

