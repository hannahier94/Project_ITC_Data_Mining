"""
This function, given an old.reddit.com thread, a list of users to randomly access, the number of pages and the
fields to get, extracts the information required.
:param urls: list of urls to consider
:param user_agent_list: list of user agents to randomly rotate
:param keys: list of keys to extract
:return: dictionary with lists containing the information of each key
"""

from parserfile import Parser
from utils import utils
from variables import Variables
import time


class Htmls(Parser):
    
    def __init__(self, urls, sleeptime=1, unfinished=True):
        Parser.__init__(self, urls, sleeptime)
        self.keys = utils['POST_KEYS']
        self.unfinished = unfinished

    def __repr__(self):
        return self
    
    def __str__(self):
        return str(self)

    def __scrape_post(self, post, url):
        """ Sets up dictionaries and calls relevant scraping functions """

        var = Variables(post, url, self.info)
        self.info = var.parse_info(logger=self.log)

    def __update_dicts(self):
        """ Updates topic level dictionaries """
        try:
            for key in self.keys:  # updating the posts dictionary
                self.post_dict[key] += self.info[key]
        except:
            self.log.warning('Cannot append post_info for this topic')

    def __reset_info(self):
        """ A function to reset the variables for each iteration of urls"""
        self.post_dict = {word: [] for word in utils['POST_KEYS']}
        self.unfinished = True  # variable to track if next buttons were found

    def get_html_data(self, log):
        """ Iterate over URLS and posts to compile information """

        self.log = log
        self.forums = []

        for url in self.urls:

            self.__reset_info()

            while self.unfinished:

                soup, posts = self.get_info(url, self.log)

                if len(posts) < 1:
                    self.log.warning('No posts found for {}, please try a new topic '.format(url))
                    self.unfinished = False  # update loops accordingly

                self.info = {key: [] for key in self.keys}

                for post in posts:  # looping inside the information extracted in each page
                    self.__scrape_post(post, url)

                self.__update_dicts()

                url, self.unfinished = self.next_url(url, soup, self.unfinished, logger=self.log)
                time.sleep(self.sleeptime)

            self.forums.append(self.post_dict)

        return self.forums
