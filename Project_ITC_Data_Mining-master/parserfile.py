"""
Sets up the
web scraper to parse
"""

from bs4 import BeautifulSoup
import requests
import random
from agents import get_user_agent
from utils import utils
import uuid
import datetime
MAGIC_ONE = utils['MAGIC_ONE']


class Parser:
    
    FRONT = 'https://old.reddit.com/r/' 
    BACK = '/top/?sort=top&t=all'
    
    def __init__(self, urls, keys=utils['POST_KEYS'],
                 postlim=None, totallim=None, sleeptime=utils['MAGIC_ONE']):

        """ Initialize parser class """

        self.topics = urls
        self.urls = [self.FRONT + url + self.BACK for url in urls]
        self.keys = keys
        self.postlim = postlim
        self.totallim = totallim
        self.sleeptime = sleeptime
        self.search = {k: [] for k in utils['TABLES']['SEARCH']}
        self.search_info = self.__search_params()

    def get_info(self, url, logger, posts=True):
        """ Set up for beautiful soup """
        self.logger = logger
        proxy = random.choice(self.proxies_pool())
        user_agent = get_user_agent(logger)
        headers = {'User-Agent': user_agent}
        proxies = {'proxies': proxy}
        attrs = {'class': 'thing'}
        html = requests.get(url, headers=headers, proxies=proxies)

        # calling the url with beautiful soup
        soup = BeautifulSoup(html.text, 'html.parser')
        if posts:
            posts = soup.find_all('div', attrs=attrs)
            return soup, posts
        else:
            return soup

    def proxies_pool(self):
        """ Create proxies for search """
        
        PROXY_URL = 'https://www.sslproxies.org/'

        # Retrieve the site's page. The 'with'(Python closure) is
        # used here in order to automatically close the session
        # when done
        with requests.Session() as res:
            proxies_page = res.get(PROXY_URL)

        # Create a BeutifulSoup object and find the table element
        # which consists of all proxies
        soup = BeautifulSoup(proxies_page.content, 'html.parser')
        proxies_table = soup.find(id='proxylisttable')

        # Go through all rows in the proxies table and store them
        # in the right format (IP:port) in our proxies list
        proxies = []
        for row in proxies_table.tbody.find_all('tr'):
            proxies.append('{}:{}'.format(row.find_all('td')
                                          [utils['MAGIC_ZERO']].string,
                                          row.find_all('td')[MAGIC_ONE]
                                          .string))
        return proxies

    def next_url(self, url, soup, unfinished, logger):
        """ Get next url from url's next button """
        try:
            # keeping the next url for the next loop
            next_button = soup.find('span', class_='next-button')
            url = next_button.find('a').attrs['href']
            unfinished = True
        except Exception:
            logger.error("\n*** Finished to load the url {} ***\n".format(url))
            unfinished = False

        return url, unfinished

    def __search_params(self):
        for topic in self.topics:
            self.current_searchid = str(uuid.uuid4())[:utils['UUID_LEN']]

            yield (self.current_searchid, topic, str(datetime.datetime.now()
                                                     .time()))

    def update_search_dict(self, current_url):

        identifier, topic, time = next(self.search_info)

        self.search['id'].append(identifier)
        self.search['tag_id'].append(topic)
        self.search['date'].append(time)
