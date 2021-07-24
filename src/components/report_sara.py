#!/usr/bin/env python
# coding: utf-8
# Copyright 2021 Netbeam SAS
# Created by: Camilo Jimenez
""" Commons Utils class """
from email import message
import os
from pathlib import Path

from components.utils import CommonsUtils
from components.database import Database
from components.ticket import Ticket
from components.excel_file import ExcelFile
from components.email import Email

# Init config Log
logging = CommonsUtils.setup_logging()


PATH_FILES = 'files/'


class ReportSara:
    """ Class Payload Functions"""

    HEADERS_FILE = [
        'Ticket',
        'Departamento',
        'Tipo de Factibilidad',
        'Cantidad de puntos',
        'Fecha Creado',
        'Fecha Vencimiento',
        'Fecha Cierre',
        'SLA',
        'Tiempo de vida',
        'Operaciones',
        'Pre-Venta',
        'Comercial']

    @staticmethod
    def get_html_content_from_file(query_name):
        """
        Method that retrieves the string from html file

        :param query_name: The query filename to read
        :return: The query string from file, throws FileNotFoundException if the file does not exist
        """
        base_path = os.path.dirname(os.path.realpath(__file__))
        query_string = ''
        with open(f'{base_path}/html_files/{query_name}.html', 'r', encoding='utf8') as f:
            query_string = f.read()
        return query_string.strip()

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
        """Method that execute query get info thread ticket
        """
        
        try:
            query = ReportSara.get_query_from_file('info_thread_by_ticket')\
                .format(ticket['thread_id'])     
            database = Database()
            rows = database.select_query(query)
            return rows            
        except Exception as e:
            logging.error(f"Error to execute query info thread ticket: {ticket['number']}")
            logging.error("Error: %s", e)

    @staticmethod
    def execute_query_info_ticket(ticket):        
        """Method that execute query get info ticket
        """
        
        try:
            query = ReportSara.get_query_from_file('info_by_ticket')\
                .format(ticket['ticket_id'])     
            database = Database()
            rows = database.select_query(query)
            return rows            
        except Exception as e:
            logging.error(f"Error to execute query info thread ticket: {ticket['number']}")
            logging.error("Error: %s", e)

    @staticmethod
    def execute_query_all_staff():        
        """Method that execute query get all staff
        """
        
        try:
            query = ReportSara.get_query_from_file('all_staff')    
            database = Database()
            return [row[0] for row in database.select_query(query)]
        except Exception as e:
            logging.error(f"Error to execute query all staff")
            logging.error("Error: %s", e)
    
    @staticmethod
    def execute_report_times(settings):
        """ Function execute report Times

            Esta funcion se encarga de guardar en un archivo de excel la informacion de los tickets
            y una estadisticas de tiempos.
        """
        tickets = ReportSara.execute_query_tickets_closed()
        all_staff = ReportSara.execute_query_all_staff()

        path_file_excel = Path(PATH_FILES, 'reporte_sara_tiempos.xlsx')
        excel_file = ExcelFile(path_file_excel)

        excel_file.set_sheet("Reporte Tiempos") 

        # columns names
        ReportSara.HEADERS_FILE = ReportSara.HEADERS_FILE + all_staff
        excel_file.write_row(ReportSara.HEADERS_FILE)
        
        for ticket in tickets:
            try:
                ticket_class = Ticket(ticket, all_staff)     

                # Obtener la informacion del hilo de historia del ticket
                ticket_class.set_thread_ticket(ReportSara.execute_query_info_thread(ticket_class.get_ticket()))

                # Obtener los tiempos por cada departamento
                ticket_class.execute_times_by_dept()

                # Obtener los tiempos por cada Staff
                ticket_class.execute_times_by_staff()

                # Obtener la informacion del ticket
                ticket_class.set_info_ticket(ReportSara.execute_query_info_ticket(ticket_class.get_ticket()))

                ticket_class.get_info_detail_ticket()
                
                excel_file.write_row(ticket_class.get_info_ticket())            
            except Exception as error:
                logging.error(f'Error con ticket {ticket_class.get_ticket()["number"]}')
                logging.error(f'Error: {error}')
                

        excel_file.save_excel(len(tickets))

        # Enviar correo electronico
        subject = "[SARA] Reporte de tiempos de tickets cerrados hasta hoy"
        body = ReportSara.get_html_content_from_file('body_content_sara_tiempos')

        email = Email(subject, body, [excel_file.src], settings['EMAIL'])
        email.send_email()


        

        