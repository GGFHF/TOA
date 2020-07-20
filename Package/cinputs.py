#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------

'''
This software has been developed by:

    GI Sistemas Naturales e Historia Forestal (formerly known as GI Genetica, Fisiologia e Historia Forestal)
    Dpto. Sistemas y Recursos Naturales
    ETSI Montes, Forestal y del Medio Natural
    Universidad Politecnica de Madrid
    https://github.com/ggfhf/

Licence: GNU General Public Licence Version 3.
'''

#-------------------------------------------------------------------------------

'''
This file contains the general functions to data inputs in mode console.
'''

#-------------------------------------------------------------------------------

import os
import sys

import xlib
import xtoa

#-------------------------------------------------------------------------------

def input_code(text, code_list, default_code):
    '''
    Input a code selected from a code list.
    '''

    # initialize the code
    code = ''

    # get the code list text
    code_list_text = str(code_list).strip('[]').replace('\'','').replace(',', ' or')

    # input and check the code
    while code == '':
        if default_code is None:
            code = input(f'{text} ({code_list_text}): ').lower()
        else:
            code = input(f'{text} ({code_list_text}) [{default_code}]: ').lower()
            if code == '': code = default_code
        found = False
        for i in range(len(code_list)):
            if code.lower() == code_list[i].lower():
                code = code_list[i]
                found = True
                break
        if not found:
            print(f'*** ERROR: {code} is not in {code_list_text}.')
            code = ''

    # return the code
    return code

#-------------------------------------------------------------------------------

def input_int(text, default=None, minimum=(-sys.maxsize - 1), maximum=sys.maxsize):
    '''
    Input a integer number.
    '''

    # initialize the number
    literal = None

    # input and check the integer number
    while literal is None:
        if default is None:
            literal = input(f'{text}: ')
        else:
            literal = input(f'{text} [{default}]: ')
            if literal == '': literal = default
        if not xlib.check_int(literal, minimum, maximum):
            print(f'*** ERROR: {literal} is not a valid value.')
            literal = None

    # return the integer value
    return int(literal)

#-------------------------------------------------------------------------------

def input_float(text, default=None, minimum=float(-sys.maxsize - 1), maximum=float(sys.maxsize), mne=0.0, mxe=0.0):
    '''
    Input a float number.
    '''

    # initialize the number
    literal = None

    # input and check the float number
    while literal is None:
        if default is None:
            literal = input(f'{text}: ')
        else:
            literal = input(f'{text} [{default}]: ')
            if literal == '': literal = default
        if not xlib.check_float(literal, minimum, maximum, mne, mxe):
            print(f'*** ERROR: {literal} is not a valid value.')
            literal = None

    # return the float value
    return float(literal)

#-------------------------------------------------------------------------------

def input_directory(directory_name, default_directory=None, is_created=False):
    '''
    Input a directory path.
    '''

    # get the directory
    directory = ''
    while directory == '':
        if default_directory is None:
            directory = input(f'Enter {directory_name} directory: ')
        else:
            directory = input(f'Enter {directory_name} directory [{default_directory}]: ')
            if directory == '':
                directory = default_directory
        if is_created and not xlib.is_valid_path(directory):
            print(f'***ERROR: The directory {directory} is not valid.')
            directory = ''
        elif directory != '' and directory[0] != '/':
            print(f'***ERROR: The directory {directory} is not an absolute path.')
            directory = ''

    # result the directory
    return directory

#-------------------------------------------------------------------------------

def input_database_list(candidate_database_list, last_database):
    '''
    Input an ordered list of databases to annotate.
    '''

    # set the candidate database number 
    candidate_database_num = len(candidate_database_list)

    # initialize the list of selected databases 
    selected_database_list = []

    # initialize the order number
    order_number = 1

    # input database identifications and check them
    database = ''
    while database.upper() != 'END' and order_number <= candidate_database_num:

        # input a candidate database
        if order_number == 1:
            candidate_database_list_text = str(candidate_database_list).strip('[]').replace('\'','')
            print(f'All candidate databases: {candidate_database_list_text} ...')
            print(f'(if {last_database} is selected, it has to be the last)')
            database = input(f'Enter the database {order_number}: ')
        else:
            candidate_database_list_text = str(candidate_database_list).strip('[]').replace('\'','')
            print(f'Remaining candidate databases: {candidate_database_list_text} ...')
            print(f'(if {last_database} is selected, it has to be the last)')
            database = input(f'Enter the database {order_number} or END to finish: ')
        if database != '' and database.upper() != 'END':
            if database in candidate_database_list:
                selected_database_list.append(database)
                candidate_database_list.remove(database)
                order_number += 1
                if database == last_database:
                    database = 'END'
            else:
                print(f'*** ERROR: {database} is not in candidate database list.')
        elif database.upper() == 'END' and order_number == 1:
            database = ''
            print('*** ERROR: You have to input at least one database.')

    # return the selected database list
    return selected_database_list

#-------------------------------------------------------------------------------

def input_experiment_id():
    '''
    Input an experiment/process identification.
    '''

    # initialize the control variable
    OK = True

    # initialize the experiment/process identification
    experiment_id = ''

    # initialize the experiment/process identification list
    experiment_id_list = []

    # get the dictionary of TOA configuration.
    toa_config_dict = xtoa.get_toa_config_dict()

    # get the experiment/process identifications
    subdir_list = [subdir for subdir in os.listdir(toa_config_dict['RESULT_DIR']) if os.path.isdir(os.path.join(toa_config_dict['RESULT_DIR'], subdir))]
    for subdir in subdir_list:
        experiment_id_list.append(subdir)

    # print the experiment/process identifications in the clusters
    if experiment_id_list != []:
        experiment_id_list_text = str(experiment_id_list).strip('[]').replace('\'','')
        print(f'Experiment/process ids existing: {experiment_id_list_text} ...')
    else:
        OK = False

    # input and check the experiment/process identification
    if OK:
        while experiment_id == '':
            experiment_id = input('... Enter the experiment/process id: ')
            if experiment_id not in experiment_id_list:
                print(f'*** ERROR: {experiment_id} does not exist.')
                experiment_id = ''

    # return the experiment/process identification
    return experiment_id

#-------------------------------------------------------------------------------

def input_result_dataset_id(experiment_id, app_list):
    '''
    Input a result dataset identification.
    '''

    # initialize the control variable
    OK = True

    # get the dictionary of TOA configuration.
    toa_config_dict = xtoa.get_toa_config_dict()

    # initialize the result dataset identification
    result_dataset_id = ''

    # initialize the result dataset list
    result_dataset_id_list = []

    # get the result dataset identifications of the experiment
    experiment_dir = f'''{toa_config_dict['RESULT_DIR']}/{experiment_id}'''
    subdir_list = sorted([subdir for subdir in os.listdir(experiment_dir) if os.path.isdir(os.path.join(experiment_dir, subdir))])
    for subdir in subdir_list:
        for app in app_list:
            if app == xlib.get_all_applications_selected_code() or subdir.startswith(app):
                result_dataset_id_list.append(subdir)
                break

    # print the result dataset identifications in the clusters
    if result_dataset_id_list != []:
        result_dataset_id_list_text = str(result_dataset_id_list).strip('[]').replace('\'','')
        print(f'dataset ids existing in {experiment_id}: {result_dataset_id_list_text} ...')
    else:
        OK = False

    # input and check the result dataset identification
    if OK:
        while result_dataset_id == '':
            result_dataset_id = input('... Enter the dataset id: ')
            if result_dataset_id not in result_dataset_id_list:
                print(f'*** ERROR: {result_dataset_id} does not exist.')
                result_dataset_id = ''

    # return the result dataset identification
    return result_dataset_id

#-------------------------------------------------------------------------------

def input_submission_log_file():
    '''
    Input a submission process log.
    '''

    # initialize the control variable
    OK = True

    # initialize the submission log file
    submission_log_file = ''

    # get the submission log file list
    submission_log_file_list = [file for file in os.listdir(xlib.get_log_dir()) if os.path.isfile(os.path.join(xlib.get_log_dir(), file))]

    # print the submission log file list
    if submission_log_file_list != []:
        submission_log_file_list_text = str(submission_log_file_list).strip('[]').replace('\'','')
        print(f'Submission log files: {submission_log_file_list_text} ...')
    else:
        OK = False

    # input and check the submission log file
    if OK:
        while submission_log_file == '':
            submission_log_file = input('... Enter the submission log file: ')
            if submission_log_file not in submission_log_file_list:
                print(f'*** ERROR: {submission_log_file} does not exist.')
                submission_log_file = ''

    # return the submission log file
    return submission_log_file

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print('This file contains the general functions to data inputs in mode console.')
    sys.exit(0)

#-------------------------------------------------------------------------------
