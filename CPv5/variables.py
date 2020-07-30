"""
This code collects variables from variables 
sent by Htmls class method
and returns parsed
information
"""

import re
import nltk
from utils import MAGIC_ZERO, MAGIC_ONE, MAGIC_TWO
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

sia = SIA()


class Variables:

    POL_LIM = 0.2

    def __init__(self, post, info):
        self.post = post
        self.info = info
        
    def __get_postid(self):
        res = re.findall(f'\W*(data-fullname="\w+\")', self.post.prettify())[MAGIC_ZERO]
        return res.replace(f'data-fullname="', "").replace('"', "")
    
    def __get_title(self):
        return self.post.find('div', class_='entry unvoted').div.p.text.split('(')[MAGIC_ZERO]
    
    def __get_titlescore(self):
        #title_score = self.get_title()
        title_score = self.post.find('div', class_='entry unvoted').div.p.text.split('(')[MAGIC_ZERO]
        pol_score = sia.polarity_scores(title_score)['compound']
        return MAGIC_ONE if pol_score > self.POL_LIM else -MAGIC_ONE if pol_score < self.POL_LIM else MAGIC_ZERO
        
    def __get_author(self):
        return self.post.find('a', class_='author').text
    
    def __get_comments(self):
        return self.post.find('a', class_='comments').text.split()[MAGIC_ZERO]

    def __get_likes(self):
        return self.post.find('div', attrs={'class': 'score likes'}).text
        
    def __get_dislikes(self):
        return self.post.find('div', attrs={'class': 'score dislikes'}).text
        
    def __get_date(self):
        return re.findall(r'\d+-\d+-\w+:\d+:\d+\+\d+', self.post.find('p', attrs={'class': 'tagline'}).time.prettify())[MAGIC_ZERO]
    
    def __get_awards(self):
        awards_i = self.post.find('span', class_='awardings-bar').prettify()
        award_count_list = [i.replace('data-count=', "").strip('"') for i in
                            re.findall(r'data-count="\d+\"', awards_i)]
        return sum([int(i) for i in award_count_list])

    def __get_domain_tag(self):
        titles = self.post.find('p', class_='title')
        if '(' not in titles.span.text:
            return titles.span.text
        else:
            return None

    def __get_thread(self):
        return self.post.find('div', class_='entry unvoted').div.p.text.split('(')[MAGIC_ONE].replace(')', "")


    def __get_extra_bool(self,key, kind):
        try:
            res = re.findall(f'\W*({kind}="\w+\")', self.post.prettify())[MAGIC_ZERO]
            return res.replace(f'{kind}="', "").replace('"', "").capitalize() == 'True'
        except:
            return False
            
    def __get_extra_num(self,key, kind):
        try:
            res = re.findall(f'\W*({kind}="\w+\")', self.post.prettify())[MAGIC_ZERO].replace(f'{kind}="', "").replace('"', "")
            return int(res)
        except:
            return MAGIC_ZERO
    
    
    def __get_postype(self):
        return re.findall('\W*(collapsed hide-when-pinned \S+\")', self.post.prettify())[MAGIC_ZERO].replace('collapsed hide-when-pinned ', '').replace('"', '')

    
    def __str__(self):
        return str(self)
    
    
    def __set_dtypes(self):
                                     
        self.ZERO_DICT = {
            'titlescore' : self.__get_titlescore,
            'comments': self.__get_comments,
            'scorelikes': self.__get_likes,
            'scoredislikes': self.__get_dislikes,
            'awards': self.__get_awards,   
        }  
    
        self.UNKNOWN_DICT = {'postid': self.__get_postid,
                    'title' : self.__get_title,
                    'author': self.__get_author,
                    'dates': self.__get_date,
                    'domain_tag': self.__get_domain_tag,
                    'thread': self.__get_thread,
                    'postype': self.__get_postype
                   }
    
        self.BOOL_DICT = {
            'spoilers': self.__get_extra_bool(key ='spoilers', kind='data-spoiler'),
            'promoted': self.__get_extra_bool(key='promoted',kind='data-promoted'),
            'crossposts': self.__get_extra_num(key='crossposts', kind='data-num-crossposts')
        }
        
    
    def parse_info(self,logger):

        """ Function to parse all datatype variables with relevant try/except clause"""
        self.__set_dtypes()
        
        for key, func in self.UNKNOWN_DICT.items():
            try:
                self.info[key].append(str(func()))                
            except Exception as err:
                logger.info("{}\nCould not find {}. Appending Unknown.".format(err,key))
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
                logger.info("{} \nCould not find {}. Appending {}.".format(err, key, MAGIC_ZERO))
                self.info[key].append(MAGIC_ZERO)
    
        return self.info

