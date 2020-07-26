""" Parse config.json """

import json


def read_json():
    """ Parse config.json as a dictionary """
    with open("config.json", "r") as infile:
        return json.load(infile)


utils = read_json()
