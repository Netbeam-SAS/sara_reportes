#!/usr/bin/env python
# coding: utf-8
# Copyright 2021 Netbeam SAS
# Created by: Camilo Jimenez
""" Commons Utils class """
import argparse

from collections import ChainMap

import yaml

class CommonsUtils:
    """ Class that owns common methods / functionality """
    @staticmethod
    def setup_logging():
        """ Method that initialize Logging """
        import logging

        # Get level logging from environment values
        settings_logging = CommonsUtils.load_settings()['LOGGING']       
        
        # Setup level logging
        logging.basicConfig(level=settings_logging['LEVEL'], format='%(levelname)s | %(message)s')

        return logging

        
    @staticmethod
    def load_yaml(yaml_filepath):
        """ Method that loads YAML files

        :param str yaml_filepath: the YAML filepath
        :return: the YAML file content
        """
        with open(yaml_filepath) as file:
            yaml_content = yaml.full_load(file)
        return yaml_content

    @staticmethod
    def load_settings():
        """Method that load the settings.yaml file

        :return: :dict: a dict with the SETTINGS values
        """
        settings_content = CommonsUtils.load_yaml("config/settings.yaml")['SETTINGS']
        settings = dict(ChainMap(*settings_content))
        # Normalize settings
        for k, v in settings.items():
            if isinstance(v, list) and (len(v) and isinstance(v[0], dict)):
                settings[k] = dict(ChainMap(*v))
        return settings
    
    @staticmethod
    def arguement_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument('-tr', '--typereport', required=True, \
            help="Tipo de reporte que se quiere ejecutar")

        return parser.parse_args()