"""
Class created to obtain API additional information from Reddit
"""
import praw
import pandas as pd
from utils import utils
from savefile import save_file


class Apiget:
    def __init__(self, logger, topics=utils['URLS']):
        """ Initialize apiget class """
        self.__clientid = utils['REDDIT_CLIENT']
        self.__clientsecret = utils['REDDIT_SECRET']
        self.__clientuser = utils['REDDIT_USER']
        self.topics = topics
        self.logger = logger
        self.create_praw()
        self.get_apinfo()

    def create_praw(self):
        """Create praw instance for reddit API"""
        self.reddit = praw.Reddit(client_id=self.__clientid, client_secret=self.__clientsecret,
                                  user_agent=self.__clientuser)
        self.logger.info("\n*** Reddit API connection was created successfully. ***\n")

    def get_apinfo(self):
        """Get API information for selected topics"""

        apinfo = []

        for topic in self.topics:
            ml_sub_reddit = self.reddit.subreddit(topic)
            posts = []
            try:
                for post in ml_sub_reddit.hot(limit=utils['MAGIC_NUMBER_API']):
                    posts.append([post.name, topic, post.link_flair_text, post.is_original_content,
                                  str(pd.to_datetime(post.edited * utils['MAGIC_DATE_CONVERTER'])), post.locked,
                                  post.over_18, post.distinguished, post.spoiler, post.stickied,
                                  str(pd.to_datetime(post.created_utc * utils['MAGIC_DATE_CONVERTER']))])
                posts = pd.DataFrame(posts, columns=utils['API_KEYS'])
                posts.reset_index(drop=True, inplace=True)
                apinfo.append(posts.to_dict('list'))
                self.logger.info('API {} loaded sucessfully'.format(topic))
            except Exception as err:
                self.logger.warning('API {} could not be loaded.'.format(topic))

        return apinfo

    def get_out(self):
        """Save file in api_results.json"""
        data = self.get_apinfo()
        save_file(data, filename=utils["API_FILE"])
