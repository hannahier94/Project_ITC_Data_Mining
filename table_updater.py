
from dbuild import DbBuild
from utils import utils
import json


class TableUpdater(DbBuild):

    def __init__(self, res, logger):
        DbBuild.__init__(self, logger)

        if not isinstance(res, dict):  # Confirm object is a dict
            res = eval(res.replace(str(False).lower(), str(False)).replace(str(True).lower(), str(True)))

        self.res = res
        self.__create_inserts()
        self.alter_tables()
        self.__get_apiinfo()
        self.__update_cat()

        self.__update_others()
        self.__update_ids()
        self.__commit_db()
        self.close_db()

        self.posts_cache = list()

    def __commit_db(self):
        """ Commits to DB or writes the error to the logger """

        try:
            self.db.commit()
            self.logger.debug("Commited to DB")
        except Exception as err:
            self.logger.warning("{} . Could not commit to DB.".format(err))

    def __format_insert(self, table_name, cols):
        """ Creates an insert statement for the tables given their columns
         params: table_nam: " the name of the SQL table
         params: cols : the columns to insert into """

        length = len(cols) - utils['MAGIC_ONE']

        seperator = utils['INSERT_PLACEHOLDER'] + utils["INSERT_SEPERATOR"]

        params = (seperator * length)
        params += utils['INSERT_PLACEHOLDER']

        cols = ', '.join(list(cols))

        statement = utils['INSERT_FORMATTER'].format(table_name.lower(), cols, params)
        self.logger.debug("Created statement {}".format(statement))

        return statement

    def __create_inserts(self):
        """ Creates a dictionary of table : insert statement"""

        self.__insert_dict = dict()

        for sqlid in self.res['IDS'].keys():
            self.__insert_dict[sqlid] = self.__format_insert(sqlid, utils['TABLES'][sqlid])

        for table in [k for k in self.res.keys() if k != 'IDS']:
            self.__insert_dict[table] = self.__format_insert(table, self.res[table].keys())

    def __update_cat(self):
        """ Update catalogue to replace names with IDs """

        CAT_IDS = {
            'THREADS': "thread_id",
            'POSTYPE': "postype_id",
            'AUTHORS': "author_id",
            'TITLE': "id"
        }

        three_zero = utils['MAGIC_ZERO'] * utils['MAGIC_THREE']

        final_ids = {}
        tag_list = []

        for table in self.res['IDS'].keys():
            final_ids[table] = {val[utils['MAGIC_ZERO']]: val[utils['MAGIC_ONE']]
                                for val in self.res['IDS'][table]}
        print(final_ids)
        for table, col in CAT_IDS.items():
            col_list = []
            for lst in self.res['CAT'][col]:
                try:
                    col_list.append(final_ids[table][lst.lower()])
                except Exception as err:
                    self.logger.info('{}. Appending 000'.format(err))
                    col_list.append(three_zero)
            self.res['CAT'][col] = col_list

        for item in self.res['SEARCH']['tag_id']:
            try:
                tag_list.append(final_ids['TAGS'][item.lower()])
            except Exception as err:
                self.logger.info('{}. Appending 000'.format(err))
                tag_list.append(three_zero)

        self.res['SEARCH']['tag_id'] = tag_list
        self.logger.info('Catalogue updated')

    def __update_ids(self):

        for table in self.res['IDS'].keys():
            self.logger.info('Working on table {}'.format(table))
            i = utils['MAGIC_ZERO']
            while i < len(self.res['IDS'][table]):

                statement = self.__insert_dict[table]
                try:
                    self.cursor.execute(statement, self.res['IDS'][table][i])
                except Exception as err:
                    self.logger.debug('{} : Could not update id for {}'.format(err, self.res['IDS'][table][i]))
                i += utils['MAGIC_ONE']

                if i % utils['COMMIT_NUM'] == utils['MAGIC_ZERO']:
                    self.__commit_db()

            self.__commit_db()

    def __update_others(self):

        NON_ID_TABLES = {
            "POSTS": "internal_id",
            "CAT": "id",
            "SEARCH": "id"
        }

        REDDIT_NULL = '•'

        for table, id_column in NON_ID_TABLES.items():
            self.logger.info('Working on table {}'.format(table))
            i = utils['MAGIC_ZERO']
            while i < len(self.res[table][id_column]):

                statement = self.__insert_dict[table]

                vals = [self.res[table][col][i]
                        if self.res[table][col][i] != REDDIT_NULL else utils['MAGIC_ZERO']
                        for col in self.res[table].keys()]
                try:
                    self.cursor.execute(statement, vals)
                except Exception as err:
                    self.logger.info(err)

                i += utils['MAGIC_ONE']

                if i % utils['COMMIT_NUM'] == utils['MAGIC_ZERO']:
                    self.__commit_db()

            self.__commit_db()

    def __get_apiinfo(self):
        filename = utils['API_FILE'] + utils["EXTENSION"]
        with open(filename, 'r') as file:
            data = json.load(file)
            self.__update_apitable(data)

    def __update_apitable(self, list_data):

        self.API_TABLE = utils['API']
        id_col = utils['API_KEYS'][utils['MAGIC_ZERO']]
        self.logger.info('Working on table {}'.format(self.API_TABLE))

        # Combine all dictionaries into a big dict of lists for easy iteration
        for n in range(1, len(list_data)):
            for col in list_data[utils['MAGIC_ZERO']].keys():
                list_data[utils['MAGIC_ZERO']][col].extend(list_data[n][col])

        data = list_data[utils['MAGIC_ZERO']]

        i = utils['MAGIC_ZERO']

        statement = self.__format_insert(self.API_TABLE, data.keys())

        while i < len(data[id_col]):

            vals = [data[col][i]
                    if data[col][i] else None 
                    for col in data.keys()]

            try:
                self.cursor.execute(statement, vals)

            except Exception as err:
                self.logger.info('{} : Could not update api for {}'.format(err, data[id_col][i]))
            i += utils['MAGIC_ONE']

            if i % utils['COMMIT_NUM'] == utils['MAGIC_ZERO']:
                self.__commit_db()
                break

            self.__commit_db()
