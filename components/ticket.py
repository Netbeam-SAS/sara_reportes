#!/usr/bin/env python
# coding: utf-8
# Copyright 2021 Netbeam SAS
# Created by: Camilo Jimenez
""" Ticket class """
import json

from itertools import groupby
from operator import itemgetter

from components.utils import CommonsUtils

logging = CommonsUtils.setup_logging()

class Ticket:
    def __init__(self, ticket, all_staff):
        self.reset()
        self.__all_staff = all_staff
        self.__ticket = self.convert_tuple_dict(ticket, self.TICKET_HEADERS)
        try:
            self.time_life_ticket = self.__ticket['closed'] - self.__ticket['created']
            self.sla = self.__ticket['est_duedate'] - self.__ticket['created']
        except Exception as error:
            logging.error('Error en fechas del ticket')
            raise
    
    def reset(self):
        self.time_life_ticket = ''
        self.__ticket = {}
        self.__thread_ticket = []
        self.__info_ticket = []
        self.TIMES_BY_DEPT = {}
        self.TIMES_BY_STAFF = {}
    
    TICKET_HEADERS = ('ticket_id', 'number', 'dept', 'created', 'est_duedate', 'closed' , 'thread_id')

    THREAD_TICKET_HEADERS = (
        'timestamp',
        'username',
        'staff_id',
        'event',
        'dept',
        'pdept')

    INFO_TICKET_HEADERS = ('field_id', 'value')

    LIST_DEPT = [
        'Operaciones',
        'Pre-Venta',
        'Comercial'
    ]

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

    def set_info_ticket(self, info_ticket):
        try:
            self.__info_ticket = [self.convert_tuple_dict(value, self.INFO_TICKET_HEADERS)\
                for value in info_ticket]         
        except Exception as error:
            logging.error(f"Error en hilo de historia del ticket: {self.__ticket['number']}")
            logging.error(f'Error: {error}')

    def get_thread_ticket(self):
        return self.__thread_ticket
    
    def __get_diference_times_by_group(self, column):
        times_by_group = {}
        for key, value in groupby(self.__thread_ticket, key=itemgetter(column)):            
            thread_by_group = list(value)
            times_by_group[key] = thread_by_group[-1]['timestamp'] - \
                thread_by_group[0]['timestamp']
        return times_by_group
    
    def execute_times_by_dept(self):
        self.TIMES_BY_DEPT = self.__get_diference_times_by_group('pdept')

    def execute_times_by_staff(self):
        self.TIMES_BY_STAFF = self.__get_diference_times_by_group('username')
    
    def get_info_detail_ticket(self):
        for info in self.__info_ticket:
            if info['field_id'] == 62:
                dict_value = json.loads(info['value'])
                key_dic_value = list(dict_value.keys())[0]
                self.__ticket['fact_type'] = dict_value[key_dic_value]
            elif info['field_id'] == 64:
                self.__ticket['points_quantity'] = int(info['value'])

    
    @staticmethod
    def conver_date_to_minutes(date):
        try:
            return round(date.total_seconds() / 60.0, 2)
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
        row_info = [
            self.__ticket['number'],
            self.__ticket['dept'],
            self.__ticket['fact_type'],
            self.__ticket['points_quantity'],
            self.__ticket['created'],
            self.__ticket['est_duedate'],
            self.__ticket['closed'],
            self.conver_date_to_minutes(self.sla),
            self.conver_date_to_minutes(self.time_life_ticket)
        ]

        for dept in self.LIST_DEPT:
            if dept in self.TIMES_BY_DEPT:
                time_minutes = self.conver_date_to_minutes(self.TIMES_BY_DEPT[dept])
                if time_minutes > 0:
                    row_info.append(time_minutes)
                else:
                    row_info.append(None)
            else:
                row_info.append(None)
        
        for staff in self.__all_staff:
            if staff in self.TIMES_BY_STAFF:
                time_minutes = self.conver_date_to_minutes(self.TIMES_BY_STAFF[staff])
                if time_minutes > 0:
                    row_info.append(time_minutes)
                else:
                    row_info.append(None)
            else:
                row_info.append(None)
            
        
        return row_info




            
        

