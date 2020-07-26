"""
Arg parse and clean results
"""

import argparse
from utils import utils


class UserInputs:
    """Constructs a class from user inputs"""
    def __init__(self, input_args):
        """Takes in user/default inputs as attributes"""
        self.command = input_args.command[utils['MAGIC_ZERO']]
        self.sleep = input_args.sleep
        if input_args.topics:
            self.topics = [x.lower() for x in input_args.topics]
        else:
            self.topics = []

        self.console = input_args.console

        # Set console level
        if input_args.console == 'False':
            self.console = False
        else:
            self.console = input_args.console

        self.default_topics = [z.lower() for z in utils['URLS']]

    def __repr__(self):
        """__repr__"""
        return self

    def __str__(self):
        """__str__"""
        return str(self)

    def add(self):
        """This function combines the default search and the additional topics into
        a uniform format without duplicates"""
        return list(set(self.default_topics + self.topics))

    def get_default(self):
        """This function returns a uniform format for the default topics"""
        return self.default_topics

    def customize(self):
        """This function returns a uniform format for the custom input topics"""
        return self.topics

    def apply_func(self):
        """Directs command to function"""
        function_map = {'default': self.get_default(),
                        'add': self.add(),
                        'custom': self.customize()}

        return function_map[self.command]


def parse_args():

    """ Takes in inputs from argparse and returns inputs from argparse """

    parser = argparse.ArgumentParser(f"""Welcome to the Reddit Web Scraper!
                                    \n The default list to scrape is: \n {utils['URLS']}\n Enter -h for help.""")

    parser.add_argument('command', choices=['default', 'custom', 'add'],
                        type=str, nargs=utils['MAGIC_ONE'], help='''Any two word topics  should be a single word 
                        (ex: to search 'data science' and 'ML', input : --topics=datascience --topics=ML).
                        Options include 
                        default, add, custom .\n
                        default : search only default topics, \n
                        add: keep default topics and add your own, \n
                        custom: provide your own topics to search.''')

    parser.add_argument("-s", "--sleep", type=int, choices=[utils['MAGIC_ZERO'], utils['MAGIC_ONE'],
                                                            utils['MAGIC_TWO']], default=utils['MAGIC_ONE'],
                        help="Choose seconds to sleep, default = {} (recommended)".format(utils['MAGIC_ONE']))

    parser.add_argument("-c", "--console", default='False', choices=['False', 'DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        action='store',
                        help="Set logging level for console logs, default is set to 'False'. "
                             "\nChoices = ['False', 'DEBUG','INFO','WARNING','ERROR'] ")

    parser.add_argument('--topics', action='append',
                        help="Please specify each topic individually with --topics=xxx \n Any topics specified"
                        "with default function will be ignored.")

    input_args = parser.parse_args()

    return input_args
