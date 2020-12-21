from In_out.utils.Secrets import Secrets, encrypt, PATH, VARIABLE, create_key
import os
import sys

def create_secret(source):
    """
    Allow to add new secret in the secret file
    """
    key = os.environ.get(VARIABLE)
    if not(key):
        create_key()
        return

    with open(PATH, "a") as file_pass:
        file_pass.write(encrypt(key, source).decode("utf-8"))







if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise(IOError("Need to specified a file secret to add"))
    path_file = sys.argv[1]
    if path_file.split(".")[-1] != "yaml":
        verif = input("Are you sure the file is a yaml file (Y,n)?")
        if verif not in ["y","Y",""]:
            sys.exit()
    with open(sys.argv[1], "rb") as file:
        create_secret(file.read())
