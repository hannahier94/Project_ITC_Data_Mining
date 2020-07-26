"""
This code collects variables from variables 
sent by Htmls class method
and returns parsed
information
"""

import re
import nltk
from utils import utils
import string
import uuid
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
nltk.download('vader_lexicon')
sia = SIA()


class Variables:

    POL_LIM = 0.2

    def __init__(self, post, url, info):
        self.post = post
        self.info = info
        self.url = url
        self.MARKER = utils['MARKER']

    def __get_siteid(self):
        res = re.findall(f'\W*(data-fullname="\w+\")', self.post.prettify())[utils['MAGIC_ZERO']]
        return res.replace(f'data-fullname="', "").replace('"', "")

    def __get_title(self):
        title = self.post.find('div', class_='entry unvoted').div.p.text.split('(')[utils['MAGIC_ZERO']] \
                    .replace("'", "")[utils['MAGIC_ZERO']:utils['MAGIC_TITLE']]
        printable = set(string.printable)
        return ''.join(filter(lambda x: x in printable, title))

    def __get_titlescore(self):
        title_score = self.post.find('div', class_='entry unvoted').div.p.text.split('(')[utils['MAGIC_ZERO']]
        pol_score = sia.polarity_scores(title_score)['compound']
        pol_score = utils['MAGIC_ONE'] if pol_score > self.POL_LIM else -utils['MAGIC_ONE'] if pol_score < -self.POL_LIM else utils['MAGIC_ZERO']
        return pol_score

    def __get_author(self):
        return self.post.find('a', class_='author').text.replace("'", "")

    def __get_comments(self):
        return int(self.post.find('a', class_='comments').text.split()[utils['MAGIC_ZERO']].replace("'", ""))

    def __get_likes(self):
        return self.post.find('div', attrs={'class': 'score likes'}).text.replace("'", "")

    def __get_dislikes(self):
        return self.post.find('div', attrs={'class': 'score dislikes'}).text.replace("'", "")

    def __get_date(self):
        return re.findall(r'\d+-\d+-\w+:\d+:\d+\+\d+',
                          self.post.find('p', attrs={'class': 'tagline'}).time.prettify())[utils['MAGIC_ZERO']]

    def __get_awards(self):
        awards_i = self.post.find('span', class_='awardings-bar').prettify()
        award_count_list = [i.replace('data-count=', "").strip('"') for i in
                            re.findall(r'data-count="\d+\"', awards_i)]
        return sum([int(i) for i in award_count_list])

    def __get_thread(self):
        return self.post.find('div', class_='entry unvoted').div.p.text.split('(')[utils['MAGIC_ONE']]\
            .replace(')', "").replace("'", "")

    def __get_extra_bool(self, kind):
        try:
            res = re.findall(f'\W*({kind}="\w+\")', self.post.prettify())[utils['MAGIC_ZERO']]
            return res.replace(f'{kind}="', "").replace('"', "").capitalize() == 'True'
        except:
            return False

    def __get_extra_num(self, kind):
        try:
            res = re.findall(f'\W*({kind}="\w+\")',
                             self.post.prettify())[utils['MAGIC_ZERO']].replace(f'{kind}="', "").replace('"', "")
            return int(res)
        except:
            return utils['MAGIC_ZERO']

    def __get_postype(self):
        try:
            post_type = re.findall('\W*(collapsed hide-when-pinned \S+\")', self.post.prettify())[utils['MAGIC_ZERO']].\
                replace('collapsed hide-when-pinned ', '').replace('"', '')
            return post_type
        except:
            post_type = 'Unknown'
            return post_type

    def __get_author_info(self):
        return self.post.find('span', class_='flair flair-seniorflair').text.replace("'", "")

    def __get_url(self):
        return re.search('r/(.*)/top', self.url).group(utils['MAGIC_ONE'])

    def __get_internal_id(self):
        title = self.__get_siteid()
        internal_uuid = str(uuid.uuid4())[:utils['UUID_LEN']]
        return internal_uuid + title.split(self.MARKER)[utils['MAGIC_ONE']]

    def __str__(self):
        return str(self)

    def __set_dtypes(self):

        self.ZERO_DICT = {'titlescore': self.__get_titlescore,
                          'comments': self.__get_comments,
                          'scorelikes': self.__get_likes,
                          'scoredislikes': self.__get_dislikes,
                          'awards': self.__get_awards}

        self.UNKNOWN_DICT = {'site_id': self.__get_siteid,
                             'internal_id': self.__get_internal_id,
                             'tag': self.__get_url,
                             'title': self.__get_title,
                             'author': self.__get_author,
                             'dates': self.__get_date,
                             'thread': self.__get_thread,
                             'postype': self.__get_postype}

        self.BOOL_DICT = {'spoilers': self.__get_extra_bool(kind='data-spoiler'),
                          'promoted': self.__get_extra_bool(kind='data-promoted'),
                          'crossposts': self.__get_extra_num(kind='data-num-crossposts')}

    def parse_info(self, logger):

        """ Function to parse all datatype variables with relevant try/except clause"""
        self.__set_dtypes()

        for key, func in self.UNKNOWN_DICT.items():
            try:
                self.info[key].append(str(func()))
            except Exception as err:
                logger.info("{}\nCould not find {}. Appending Unknown.".format(err, key))
                self.info[key].append('Unknown')

        for key, func in self.BOOL_DICT.items():
            try:
                self.info[key].append(func)
            except Exception as err:
                logger.info("{}\nCould not find {}. Appending False.".format(err, key))
                self.info[key].append(False)

        for key, func in self.ZERO_DICT.items():
            try:
                self.info[key].append(func())
            except Exception as err:
                logger.info("{} \nCould not find {}. Appending {}.".format(err, key, utils['MAGIC_ZERO']))
                self.info[key].append(utils['MAGIC_ZERO'])

        return self.info
