import json


def save_file(filename):
    """
    This function saves the file as a json file inside the folder that we are working on
    :param filename: Filename to create
    :return: json file
    """
    with open('result.json', 'w') as fp:
        json.dump(filename, fp)
        fp.close()
