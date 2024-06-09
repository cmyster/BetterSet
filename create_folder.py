from os import mkdir, path
from shutil import rmtree

def create_folder(name, index):
    """
    param: Generates a folder based on name and index number.
    type: str, int
    return: str
    """
    folder = name + str(index)
    if path.exists(folder):
        rmtree(folder)
    mkdir(folder)
    return folder