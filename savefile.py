import json
from utils import utils


def save_file(data, filename='result'):
    """
    This function saves the file as a json file inside the folder that we are working on
    :param filename: Filename to create
    :return: json file
    """
    filename = filename + utils['EXTENSION']

    with open(filename, 'w') as fp:
        json.dump(data, fp)
        fp.close()
