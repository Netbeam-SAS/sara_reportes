#!/usr/bin/env python
# coding: utf-8
# Copyright 2021 Netbeam SAS
# Created by: Camilo Jimenez
""" Commons Utils class """
import os
from pathlib import Path

from components.utils import CommonsUtils
from components.database import Database
from components.ticket import Ticket
from components.excel_file import ExcelFile

# Init config Log
logging = CommonsUtils.setup_logging()


PATH_FILES = 'files/'


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
    def execute_query_tickets_closed():        
        """Method tha execute query select all tickets closed
        """
        
        try:
            query = ReportSara.get_query_from_file('all_tickets_closed')            
            database = Database()
            rows = database.select_query(query)
            return rows            
        except Exception as e:
            logging.error("Error to execute query select all ticket closed")
            logging.error("Error: %s", e)

    @staticmethod
    def execute_query_info_thread(ticket):        
        """Method tha execute query select all tickets closed
        """
        
        try:
            query = ReportSara.get_query_from_file('info_thread_by_ticket')\
                .format(ticket['thread_id'])        
            # query = ReportSara.get_query_from_file('info_thread_by_ticket')\
            #     .format(3622)        
            database = Database()
            rows = database.select_query(query)
            return rows            
        except Exception as e:
            logging.error(f"Error to execute query info thread ticket: {ticket['number']}")
            logging.error("Error: %s", e)
    
    @staticmethod
    def execute_report_times():
        """ Function execute report Times

            Esta funcion se encarga de guardar en un archivo de excel la informacion de los tickets
            y una estadisticas de tiempos.
        """
        tickets = ReportSara.execute_query_tickets_closed()

        path_file_excel = Path(PATH_FILES, 'reporte_sara_tiempos.xlsx')
        excel_file = ExcelFile(path_file_excel)

        excel_file.set_sheet("Reporte Tiempos") 

        # columns names
        excel_file.write_row([
            'Ticket',
            'Departamento',
            'Fecha Creado',
            'Fecha Overdue',
            'Fecha Cierre',
            'SLA',
            'Tiempo de vida',
            'Operaciones',
            'Pre-Venta',
            'Comercial'])
        
        for ticket in tickets:
            try:
                ticket_class = Ticket(ticket)     

                # Obtener la informacion del hilo de historia del ticket
                ticket_class.set_thread_ticket(ReportSara.execute_query_info_thread(ticket_class.get_ticket()))

                # Obtener los tiempos por cada departamento
                ticket_class.execute_process_times()
                
                excel_file.write_row(ticket_class.get_info_ticket())            
            except Exception as error:
                logging.error(f'Error con ticket {ticket_class.get_ticket()["number"]}')
                logging.error(f'Error: {error}')
                

        excel_file.save_excel()



        

        