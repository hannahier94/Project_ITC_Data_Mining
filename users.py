"""

This class is used to
parse the user information.
Uses a decorator to ensure
no user page is parsed twice.

Param post: post being scraped,
Param user_info: the dictionary to update

"""

import re
from parserfile import Parser
from utils import USER_KEYS, MAGIC_ZERO, MAGIC_ONE, MAGIC_TWO
from functools import lru_cache


class Users(Parser):

    def __init__(self, post, user_info):
        self.post = post
        self.user_info = user_info
        self.__cache = []

    def get_user_info(self, log):
        try:
            self.logger = log
            self.__user_page = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+',
                                          str(self.post.find('a', class_='author')))[MAGIC_ZERO]
            Parser.__init__(self, [self.__user_page], keys=USER_KEYS)

            self.__usoup = self.get_info(self.__user_page, logger=self.logger, posts=False)
            if self.__user_page not in self.__cache:
                self.__cache.append(self.__user_page)
                return self.__parse_user_info()
        except Exception as err:
            self.logger.error('{}, cannot parse user information for this post'.format(err))
            return None

    def __get_username(self):
        username = self.__user_page.split('/')[-MAGIC_ONE]
        return username

    def __get_total_posts(self):
        return self.__usoup.find('span', class_="karma").text

    def __get_total_comments(self):
        return self.__usoup.find('span', class_="karma comment-karma").text

    def __get_user_since(self):
        user_age = self.__usoup.find('div', class_="titlebox").find('div', class_="bottom").find('span', class_="age")
        return re.findall(r'\d+-\d+-\w+:\d+:\d+\+\d+', str(user_age))[MAGIC_ZERO]

    def __get_trophies(self):
        return len(self.__usoup.find('div', class_="side").find_all('div', class_='spacer')[MAGIC_TWO].ul.li.tr)

    def __set_dtypes(self):
        self.__NUM_DICT = {'total_posts': self.__get_total_posts,
                           'total_comments': self.__get_total_comments}
        self.__VAR_DICT = {'username': self.__get_username,
                           'user_since': self.__get_user_since}

    @lru_cache()
    def __parse_user_info(self):

        self.__set_dtypes()

        for k, func in self.__VAR_DICT.items():
            try:
                self.user_info[k].append(func())

            except:
                self.logger.info("Could not find {}. Appending Unknown.".format(k))
                self.user_info[k].append('Unknown')

        for k, func in self.__NUM_DICT.items():
            try:

                self.user_info[k].append(func())
            except:
                self.logger.info("Could not find {}. Appending {}.".format(k, MAGIC_ZERO))
                self.user_info[k].append(MAGIC_ZERO)

        return self.user_info
