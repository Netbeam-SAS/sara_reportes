#!/usr/bin/env python
# coding: utf-8
# Copyright 2021 Netbeam SAS
# Created by: Camilo Jimenez
""" Ticket class """

from itertools import groupby
from operator import itemgetter

from components.utils import CommonsUtils

logging = CommonsUtils.setup_logging()

class Ticket:
    def __init__(self, ticket):
        self.reset()
        self.__ticket = self.convert_tuple_dict(ticket, self.TICKET_HEADERS)
        try:
            self.time_life_ticket = self.__ticket['closed'] - self.__ticket['created']
            self.sla = self.__ticket['est_duedate'] - self.__ticket['created']
        except Exception as error:
            logging.error('Error en fechas del ticket')
            raise
    
    def reset(self):
        self.time_life_ticket = ''
        self.__thread_ticket = []
        self.TIMES_BY_DEPT = {
            'Operaciones': '',
            'Pre-Venta': '',
            'Comercial': ''
        }
    
    TICKET_HEADERS = ('ticket_id', 'number', 'dept', 'created', 'est_duedate', 'closed' , 'thread_id')

    THREAD_TICKET_HEADERS = (
        'timestamp',
        'username',
        'staff_id',
        'event',
        'dept',
        'pdept')

    def get_ticket(self):
        return self.__ticket

    def convert_tuple_dict(self, info_tuple, headers):
        try:
            return dict(zip(headers, info_tuple))
        except Exception as error:
            logging.error('Error al convertir a diccionario')
            logging.error(f'Error: {error}')

    def set_thread_ticket(self, thread_ticket):
        try:
            self.__thread_ticket = [self.convert_tuple_dict(value, self.THREAD_TICKET_HEADERS)\
                for value in thread_ticket]            
        except Exception as error:
            logging.error(f"Error en hilo de historia del ticket: {self.__ticket['number']}")
            logging.error(f'Error: {error}')

    def get_thread_ticket(self):
        return self.__thread_ticket
    
    def execute_process_times(self):
        for key, value in groupby(self.__thread_ticket, key=itemgetter('pdept')):            
            thread_by_dept = list(value)
            self.TIMES_BY_DEPT[key] = thread_by_dept[-1]['timestamp'] - \
                thread_by_dept[0]['timestamp']
    
    @staticmethod
    def conver_date_to_minutes(value):
        try:
            return value.total_seconds() / 60.0
        except Exception as error:
            pass
        return 0

    @staticmethod
    def convert_hours_to_minutes(hours):
        try:
            return hours * 60
        except Exception as error:
            pass
        return 0
    
    def get_info_ticket(self):
        return [
            self.__ticket['number'],
            self.__ticket['dept'],
            self.__ticket['created'],
            self.__ticket['est_duedate'],
            self.__ticket['closed'],
            self.conver_date_to_minutes(self.sla),
            self.conver_date_to_minutes(self.time_life_ticket),
            self.conver_date_to_minutes(self.TIMES_BY_DEPT['Operaciones']),
            self.conver_date_to_minutes(self.TIMES_BY_DEPT['Pre-Venta']),
            self.conver_date_to_minutes(self.TIMES_BY_DEPT['Comercial'])
        ]




            
        
