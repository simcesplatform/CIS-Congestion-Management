# -*- coding: utf-8 -*-
# Copyright 2021 Tampere University.
# This software was developed as a part of the ProCemPlus project: https://www.interrface.eu
# This source code is licensed under the MIT license. See LICENSE in the repository root directory.
# Author(s): Mehdi Attar <mehdi.attar@tuni.fi>


'''
Contains classes related to reading the NIS data from a JSON file.
'''

from dataclasses import dataclass
from tools.tools import FullLogger


# import csv
import json

LOGGER = FullLogger(__name__)

#@dataclass
#class ResourceState():
#    '''
#    Represents required attributes read from the json file.
#    '''
#
#    ResourceId: list
#    CustomerId: list
#    BusName: list


class JsonFileError(Exception):
    '''
    CsvFileResourceStateSource was unable to read the given csv file or the file was missing a required column.
    '''

class JsonFileCIS():
    '''
    Class for getting the network information data from a JSON file.
    '''
    REQUIRED_KEYS = {
        'ResourceId',
        'CustomerId',
        'BusName'
    }

    def __init__(self, file_name: str):
        '''
        Create object which uses the given json file that uses the given delimiter.
        Raises JsonFileError if file cannot be read e.g. file not found, or it is missing required attributes.
        '''
        LOGGER.warning("beginning of the file opener")
        self._file = None  # required if there is no file and the __del__ method is executed
        try:
            self._file = open(file_name, newline="", encoding="utf-8")

        except Exception as e:
            raise JsonFileError(f'Unable to read json file {file_name}: {str( e )}.')

        LOGGER.warning("after openning the json file")
        try:
            self._pythonComponent = json.load(self._file)
        except Exception as e:
            LOGGER.error(f"error of the json loading{e} - {file_name}")

        # check that self._json.keys has required attributes
        fields = set(self._pythonComponent.keys())           # .keys are attributes of the json file
        # missing contains fields that do not exist or is empty if all fields exist.
        missing = JsonFileCIS.REQUIRED_KEYS.difference(fields)
        if len(missing) > 0:
            raise JsonFileError(f'Resource state source json file missing required attribute: {",".join( missing )}.')

    def get_data(self):
        '''Return the data parsed from the JSON file.'''
        return self._pythonComponent

    def __del__(self):
        '''
        Close the json file when this object is destroyed.
        '''
        if self._file is not None:
            self._file.close()
