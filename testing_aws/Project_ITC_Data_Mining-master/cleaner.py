"""
Cleans the information into Seperate tables and queries the existing DB to find existing IDs before creating new Ids
"""

from multiprocessing.dummy import Pool as ThreadPool
from utils import utils
from dbuild import DbBuild


class CleanDicts:

    ID = 'id'
    POSTID = 'internal_id'
    TITLE = 'title'

    def __init__(self, logger):
        # Dictionary of values to insert into
        self.TABLE_ID_MAP = utils['TABLE_ID_MAP']
        self.POSTS_MAP = utils['POSTS_MAP']
        self.__sql_posts = {key: list() for key in self.POSTS_MAP.values()}

        self.__sql_titles = list()
        self.__logger = logger

        self.MARKER = utils['MARKER']

        # create a list of ID tables
        self.ids = " ".join([v for v in self.TABLE_ID_MAP.values()]).split()
        self.cols = {x.rsplit(utils['SEPERATOR'])[utils['MAGIC_ZERO']]:
                    list() for x in self.ids}  # create a dict to store cache
        self.__update_sql_ids()

    def __update_sql_ids(self):
        """ Query the db to find existing ids """
        self.id_dicts = DbBuild(self.__logger).check_tables()
        self.__sql_id_dict = {k: {} for k in self.id_dicts.keys()}

        for key, value in self.id_dicts.items():
            if len(value) > 0:
                for column in self.cols.keys():
                    self.cols[column].extend([x[1] for x in value
                                              if column.upper() in key])
                for a, b in value:
                    self.__sql_id_dict[key].setdefault(a, b)

    def __update_id_cache(self, col_details):
        """ Update IDs based on values in the cache """
        col_name, col_cache = col_details[utils['MAGIC_ZERO']], \
                              col_details[utils['MAGIC_ONE']]  # divide column names
        # and column cache
        self.__logger.info('Sorting IDs')
        for user_info in self.mess:
            self.__update_posts(user_info)  # update post info

            col_cache.extend([p for p in user_info[col_name]
                              if p not in col_cache])

        for k, v in self.__sql_id_dict.items():
            upper_col = col_name.upper()
            if upper_col in k:
                for c in col_cache:
                    c_lower = c.lower()
                    v.setdefault(c_lower, len(v) + utils['MAGIC_ONE'])

    def __update_posts(self, user_info):
        """ Update posts """
        self.__logger.info('Cleaning posts')

        for k, v in user_info.items():
            if k in self.POSTS_MAP.values():
                try:
                    self.__sql_posts[k].extend(v)
                except Exception as err:
                    self.__logger.warning('{}\nCould not update posts'
                                          .format(err))

        self.__sql_titles.extend(list(zip(self.__sql_posts[self.POSTID],
                                          user_info[self.TITLE])))
        return self.__sql_posts

    def organize_info(self, mess):
        """Function to organize information"""
        self.mess = mess  # create a cache
        col_details = [(col_name, col_cache) for col_name, col_cache
                       in self.cols.items()]
        self.__logger.info('starting cleanse')
        pool = ThreadPool(len(col_details))
        pool.map(self.__update_id_cache, col_details)
        pool.close()
        pool.join()

        # Convert sql ids to a dict containing lists of tuples (id, info)
        self.__sql_finalids = {table: [(v, k) for k, v
                                       in self.__sql_id_dict[table].items()]
                               for table in self.__sql_id_dict.keys()}

        self.__sql_finalids[self.TITLE.upper()] = self.__sql_titles

        return self.__sql_finalids, self.__sql_posts
