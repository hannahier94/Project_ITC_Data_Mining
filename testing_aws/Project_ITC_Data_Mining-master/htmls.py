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
from cleaner import CleanDicts
from variables import Variables
import time
import json
import uuid


class Htmls(Parser):
    
    def __init__(self, urls, sleeptime=1, unfinished=True):
        Parser.__init__(self, urls, sleeptime)
        self.keys = utils['POST_KEYS']
        self.MAP_IDS = utils['MAP_IDS']
        self.unfinished = unfinished
        self.catalogue = {k: [] for k in utils['TABLES']['CAT']}

    def __repr__(self):
        return self

    def __str__(self):
        return str(self)

    def __scrape_post(self, post, url):
        """ Sets up dictionaries and calls relevant scraping functions """

        var = Variables(post, url, self.info)
        self.info = var.parse_info(logger=self.log)

        self.catalogue['id'].append(str(uuid.uuid4())[:utils['UUID_LEN']])
        self.catalogue['search_id'].append(self.current_searchid)

    def __update_dicts(self):
        """ Updates topic level dictionaries """
        try:
            for key in self.keys:  # updating the posts dictionary
                self.post_dict[key] += self.info[key]
        except:
            self.log.warning('Cannot append post_info for this topic')

        self.__update_cat()

    def __reset_info(self, url):
        """ A function to reset the variables for each iteration of urls"""
        self.update_search_dict(url)
        self.post_dict = {word: [] for word in utils['POST_KEYS']}
        self.unfinished = True  # variable to track if next buttons were found

    def __update_cat(self):
        for key, val in self.MAP_IDS.items():
            updated_info = self.info[val]
            self.catalogue[key] += [v for v in updated_info]

    def __scrape_url(self, url):
        """ Scrapes posts of each post
        params: url : current url """
        while self.unfinished:

            soup, posts = self.get_info(url, self.log)

            if len(posts) < 1:
                self.log.warning('No posts found for {}, please try '
                                 'a new topic '.format(url))

                self.unfinished = False  # update loops accordingly

            self.info = {key: [] for key in self.keys}

            # looping inside the information extracted in each page
            for post in posts:
                self.__scrape_post(post, url)

            self.__update_dicts()

            url, self.unfinished = self.next_url(url, soup,
                                                 self.unfinished,
                                                 logger=self.log)
            time.sleep(self.sleeptime)

    def __format_return(self):
        """ Returns a cleaned dictionary of sql info """
        self.result_dict = {"CAT": self.catalogue,
                            "IDS": self.sql_ids,
                            "POSTS": self.sql_posts,
                            "SEARCH": self.search}

    def get_html_data(self, log):
        """ Iterate over URLS and posts to compile information
        param: log is a logger received from main
        returns: a json of the scraper results dictionary"""

        self.log = log
        self.forums = []

        for url in self.urls:

            self.__reset_info(url)

            self.__scrape_url(url)

            self.forums.append(self.post_dict)

        clean = CleanDicts(self.logger)
        self.sql_ids, self.sql_posts = clean.organize_info(self.forums)
        self.__format_return()

        return json.dumps(self.result_dict)
