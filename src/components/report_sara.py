#!/usr/bin/env python
# coding: utf-8
# Copyright 2021 Netbeam SAS
# Created by: Camilo Jimenez
""" Commons Utils class """

import requests
import json
import os
from datetime import datetime, timedelta, date

from commans.utils import CommonsUtils
from commans.database import Database

# Init config Log
logging = CommonsUtils.setup_logging()

FORMAT_DATE = "%Y-%m-%d-%H-%M-%S"
TODAY = date.today() 

class ReportSara:
    """ Class Payload Functions"""

    @staticmethod
    def get_query_from_file(query_name):
        """
        Method that retrieves the query string from sql file

        :param query_name: The query filename to read
        :return: The query string from file, throws FileNotFoundException if the file does not exist
        """
        base_path = os.path.dirname(os.path.realpath(__file__))
        query_string = ''
        with open(f'{base_path}/queries/{query_name}.sql', 'r') as f:
            query_string = f.read()
        return query_string.strip()
        
    @staticmethod
    def execute_query_get_services(type_payload):        
        """Method tha execute query select services
        
        :param str type_payload: The type services
        """
        
        try:
            query = ReportSara.get_query_from_file('select_services')\
                    .format(type_payload)
            
            database = Database()
            rows = database.execute_query(query)
            return [dict(id= id_site, sensor= sensor_id_site) for id_site, sensor_id_site in rows]            
        except Exception as e:
            logging.error("Error to execute query select services")
            logging.error("Error: %s", e)

    @staticmethod
    def get_data_payload_uk(url, params, type_payload="UK"):

        # Definimos el inicio y fin de los datos que queremos consultar
        start_date = datetime.strptime(f'{TODAY}-00-00-00', FORMAT_DATE) - timedelta(hours=24)
        end_date = datetime.strptime(f'{TODAY}-00-00-00', FORMAT_DATE)

        # Agregamos nuevos parametros
        params['avg'] = '60'
        params['sdate'] = start_date
        params['edate'] = end_date
         
        sites = ReportSara.execute_query_get_services(type_payload)

        for site in sites:
            data = ReportSara.get_data_historical_api(url, params, id_object=site['sensor'])
            if data:
                max_value = ReportSara.__maximun_value_payload(data)
                try:
                    ReportSara.execute_query_insert_values(site=site, payload=max_value, date=start_date)
                except Exception as error:
                    logging.error('Error insert data values')
                    logging.error(f'Error: {error}')


        

            # Debemos insertar los datos en DB

    @staticmethod
    def execute_get_data_payload(url, params, type_payload="UK"):
        """ Function execute get data payload

            Esta funcion se encarga de verificar que tipo de consulta vamos a realizar
            al servidor del PRTG

            :param str [url]: Url del servidor PRTG
            :param dic [params]: Parametros por defecto para request
            :param str [type]: Tipo de consulta que se desea hacer
        """

        if type_payload == "UK":
            ReportSara.get_data_payload_uk(url, params, type_payload)
        