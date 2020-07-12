import mysql.connector
from utils import utils
from datetime import datetime


class DbBuild:

    def __init__(self, res, logger):
        """Initialize the DB information"""
        self.__localhost = utils['HOST']
        self.__username = utils['USER']
        self.__password = utils['PASS']
        self.__database_name = utils['DB']
        self.__res = res
        self.__logger = logger
        self.create_db()
        self.create_connection()
        self.cursor = self.__db.cursor()
        self.create_tables()
        self.update_tables()
        self.__db.commit()
        self.close_db()

    def create_db(self):
        """Delete existing DB / Create DB if not Exist"""
        my_connection = mysql.connector.connect(
            host=self.__localhost,
            user=self.__username,
            passwd=self.__password
        )
        self.__conn = my_connection.cursor()
        self.__conn.execute("DROP DATABASE IF EXISTS %s" % self.__database_name)
        self.__conn.execute("CREATE DATABASE IF NOT EXISTS %s" % self.__database_name)
        self.__logger.info("\n*** Database was created successfully. ***\n")

    def create_connection(self):
        """Create connection"""
        self.__db = mysql.connector.connect(
            host=self.__localhost,
            user=self.__username,
            passwd=self.__password,
            database=self.__database_name
        )
        self.__logger.info("\n*** Connection was created successfully. ***\n")

    def create_tables(self):
        for statement in utils['CREATE_TABLE_STATEMENTS']:
            self.cursor.execute(statement)
        self.__db.commit()
        self.__logger.info("\n*** Created tables successfully ***\n")

    def update_tables(self):
        try:
            for tag in range(len(self.__res)):
                for post in range(len(next(iter(self.__res[tag].values())))):
                    self.cursor.execute("""INSERT IGNORE INTO posts (post_id, tag, domain_tag, title, awards, author, 
                    author_info, comments, scorelikes, scoredislikes, dates, thread, spoilers, promoted, crossposts, 
                    postype, titlescore) VALUES ('{}', '{}', '{}', '{}', {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', 
                    '{}', {}, {}, '{}', {});""".format(self.__res[tag]['postid'][post],
                                                       self.__res[tag]['tag'][post],
                                                       self.__res[tag]['domain_tag'][post],
                                                       self.__res[tag]['title'][post],
                                                       int(self.__res[tag]['awards'][post]),
                                                       self.__res[tag]['author'][post],
                                                       self.__res[tag]['author_info'][post],
                                                       self.__res[tag]['comments'][post],
                                                       self.__res[tag]['scorelikes'][post],
                                                       self.__res[tag]['scoredislikes'][post],
                                                       self.__res[tag]['dates'][post],
                                                       self.__res[tag]['thread'][post],
                                                       self.__res[tag]['spoilers'][post],
                                                       int(self.__res[tag]['promoted'][post]),
                                                       int(self.__res[tag]['crossposts'][post]),
                                                       self.__res[tag]['postype'][post],
                                                       int(self.__res[tag]['titlescore'][post])))
                    self.__db.commit()

                self.cursor.execute("""INSERT IGNORE INTO search (search_id, tag, date) 
                                    VALUES ({}, '{}', '{}');"""
                                    .format(tag, self.__res[tag]['tag'][utils['MAGIC_ZERO']],
                                            datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                self.__db.commit()

        except (KeyError, IndexError, TypeError) as err:
            self.__logger.info("There was an error during the post insertion. The error: {}".format(err))

    def close_db(self):
        try:
            self.cursor.close()
            self.__db.close()
            self.__logger.info("\n*** MySQL connection is closed. ***\n")
        except Exception as err:
            self.__logger.info("\n*** Connection to MySQL did not succeed {}. ***\n".format(err))
            pass
