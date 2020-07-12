import sys
from htmls import Htmls
from user_args import parse_args, UserInputs
from logsetup import get_module_logger
import savefile as savefile
from dbuild import DbBuild
sys.path.append('../')


def main():
    """
    Directs script to correct function based on inputs
    """

    input_args = parse_args()
    user_input = UserInputs(input_args)
    logger = get_module_logger(console=user_input.console)
    topics = user_input.apply_func()
    posts = Htmls(topics, user_input.sleep)
    res = posts.get_html_data(logger)
    savefile.save_file(res)
    DbBuild(res, logger)


if __name__ == '__main__':
    main()
