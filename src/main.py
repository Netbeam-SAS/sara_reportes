#!/usr/bin/env python
# coding: utf-8
# Copyright 2021 Netbeam SAS
# Created by: Camilo Jimenez
""" Main Function """

from components.utils import CommonsUtils
from components.report_sara import ReportSara

logging = CommonsUtils.setup_logging()
arg = CommonsUtils.arguement_parser()


def main():
    settings = CommonsUtils.load_settings()

    if arg.typereport == "tiempos":
        logging.info('Inicio reporte de tiempos')
        ReportSara.execute_report_times()
        logging.info('Fin reporte de tiempos')
        
    else:
        logging.error('Ingrese correctamente el reporte que desea ejecutar.')


if __name__ == "__main__":    
    main()