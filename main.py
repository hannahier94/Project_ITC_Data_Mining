import constants
import PARSER
import save_file


def main():
    saved = PARSER.html_data(constants.URLS, constants.KEYS)
    save_file.save_file(saved)


if __name__ == '__main__':
    main()
