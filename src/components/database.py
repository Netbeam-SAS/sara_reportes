#!/usr/bin/env python
# coding: utf-8
# Copyright 2021 Netbeam SAS
# Created by: Camilo Jimenez
""" Database class """

from mysql.connector import connect
from commans.utils import CommonsUtils

# Init config Log
logging = CommonsUtils.setup_logging()

class Database:
    """ Database class"""
    def __init__(self):
        """ Main Function"""
        settings = CommonsUtils.load_settings()['DATABASE']
        
        self.__host     = settings['HOST']
        self.__user     = settings['USER']
        self.__password = settings['PASSWORD']
        self.__database = settings['DB_NAME']

    def __open(self):
        """ Open Connection with database function"""
        try:
            connector = connect(
                host=self.__host,
                user=self.__user,
                password=self.__password,
                database=self.__database)

            self.__connection = connector
            self.__session    = connector.cursor()
        except Exception as error:
            logging.error('Error in connection a DB')
            logging.error(f'Error {error}')
            raise error

    def __close(self):
        """ Close Connection with database function"""
        self.__session.close()
        self.__connection.close()

    def select_query(self, query):
        """Execute query Function
        
        :param str query: String query
        """
        self.__open()
        self.__session.execute(query)
        result = self.__session.fetchall()
        self.__close()

        return result

    def insert_query(self, query):
        """Insert values query Function
        
        :param str query: String query
        """

        self.__open()
        self.__session.execute(query)
        self.__connection.commit()
        self.__close()