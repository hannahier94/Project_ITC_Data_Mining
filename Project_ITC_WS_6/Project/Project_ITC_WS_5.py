import json
import CONSTANTS
import PARSER


def save_file(filename):
    """
    This function saves the file as a json file inside the folder that we are working on
    :param filename: Filename to create
    :return: json file
    """
    with open('result_full.json', 'w') as fp:
        json.dump(filename, fp)
        fp.close()


def main():
    saved = PARSER.html_data(CONSTANTS.URLS, CONSTANTS.USER_AGENT_LIST, CONSTANTS.PAGES, CONSTANTS.KEYS)
    save_file(saved)


if __name__ == '__main__':
    main()
