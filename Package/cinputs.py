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

def input_directory(dir_name, default_dir=None, is_created=False):
    '''
    Input a directory path.
    '''

    # get the directory
    dir = ''
    while dir == '':
        if default_dir is None:
            dir = input('Enter {0} directory: '.format(dir_name))
        else:
            dir = input('Enter {0} directory [{1}]: '.format(dir_name, default_dir))
            if dir == '':
                dir = default_dir
        if is_created and not xlib.is_valid_path(dir):
            print('***ERROR: The directory {0} is not valid.'.format(dir))
            dir = ''
        elif dir != '' and dir[0] != '/':
            print('***ERROR: The directory {0} is not an absolute path.'.format(dir))
            dir = ''

    # result the directory
    return dir

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
            print('All candidate databases: {0} ...'.format(str(candidate_database_list).strip('[]').replace('\'','')))
            print('(if {0} is selected, it has to be the last)'.format(last_database))
            database = input('Enter the database {0}: '.format(order_number))
        else:
            print('Remaining candidate databases: {0} ...'.format(str(candidate_database_list).strip('[]').replace('\'','')))
            print('(if {0} is selected, it has to be the last)'.format(last_database))
            database = input('Enter the database {0} or END to finish: '.format(order_number))
        if database != '' and database.upper() != 'END':
            if database in candidate_database_list:
                selected_database_list.append(database)
                candidate_database_list.remove(database)
                order_number += 1
                if database == last_database:
                    database = 'END'
            else:
                print('*** ERROR: {0} is not in candidate database list.'.format(database))
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
        print('Experiment/process ids existing: {0} ...'.format(str(experiment_id_list).strip('[]').replace('\'','')))
    else:
        OK = False

    # input and check the experiment/process identification
    if OK:
        while experiment_id == '':
            experiment_id = input('... Enter the experiment/process id: ')
            if experiment_id not in experiment_id_list:
                print('*** ERROR: {0} does not exist.'.format(experiment_id))
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
    experiment_dir = '{0}/{1}'.format(toa_config_dict['RESULT_DIR'], experiment_id)
    subdir_list = [subdir for subdir in os.listdir(experiment_dir) if os.path.isdir(os.path.join(experiment_dir, subdir))]
    for subdir in subdir_list:
        for app in app_list:
            if app == xlib.get_all_applications_selected_code() or subdir.startswith(app):
                result_dataset_id_list.append(subdir)
                break

    # print the result dataset identifications in the clusters
    if result_dataset_id_list != []:
        print('dataset ids existing in {0}: {1} ...'.format(experiment_id, str(result_dataset_id_list).strip('[]').replace('\'','')))
    else:
        OK = False

    # input and check the result dataset identification
    if OK:
        while result_dataset_id == '':
            result_dataset_id = input('... Enter the dataset id: ')
            if result_dataset_id not in result_dataset_id_list:
                print('*** ERROR: {0} does not exist.'.format(result_dataset_id))
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
        print('Submission log files: {0} ...'.format(str(submission_log_file_list).strip('[]').replace('\'','')))
    else:
        OK = False

    # input and check the submission log file
    if OK:
        while submission_log_file == '':
            submission_log_file = input('... Enter the submission log file: ')
            if submission_log_file not in submission_log_file_list:
                print('*** ERROR: {0} does not exist.'.format(submission_log_file))
                submission_log_file = ''

    # return the submission log file
    return submission_log_file

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print('This file contains the general functions to data inputs in mode console.')
    sys.exit(0)

#-------------------------------------------------------------------------------
