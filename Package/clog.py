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
This file contains the functions related to forms corresponding to dataset
menu items in mode console.
'''

#-------------------------------------------------------------------------------

import os
import re
import sys

import cinputs
import clib
import xlib
import xtoa

#-------------------------------------------------------------------------------

def form_list_submission_logs():
    '''
    List the submission logs.
    '''

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment('Logs - List submission logs')

    # get the submission process dictionary
    submission_process_dict = xlib.get_submission_process_dict()

    # build the log dictionary
    log_dict = {}
    log_file_list = [file for file in os.listdir(xlib.get_log_dir()) if os.path.isfile(os.path.join(xlib.get_log_dir(), file))]
    for log_file in log_file_list:
        try:
            pattern = r'^(.+)\-(.+)\-(.+).txt$'
            mo = re.search(pattern, log_file)
            submission_process_id = mo.group(1).strip()
            yymmdd = mo.group(2)
            hhmmss = mo.group(3)
            submission_process_text = submission_process_dict[submission_process_id]['text']
            date = f'20{yymmdd[:2]}-{yymmdd[2:4]}-{yymmdd[4:]}'
            time = f'{hhmmss[:2]}:{hhmmss[2:4]}:{hhmmss[4:]}'
        except:
            submission_process_text = 'unknown process'
            date = '0000-00-00'
            time = '00:00:00'
        key = f'{submission_process_text}-{log_file}'
        log_dict[key] = {'submission_process_text': submission_process_text, 'log_file': log_file, 'date': date, 'time': time}

    # print the submission log list
    print(xlib.get_separator())
    if log_dict == {}:
        print('*** WARNING: There is not any submission log.')
    else:
        # set data width
        submission_process_text_width = 55
        log_file_width = 45
        date_width = 10
        time_width = 8
        # set line template
        line_template = '{0:' + str(submission_process_text_width) + '}   {1:' + str(log_file_width) + '}   {2:' + str(date_width) + '}   {3:' + str(time_width) + '}'
        # print header
        print(line_template.format('Process', 'Log file', 'Date', 'Time'))
        print(line_template.format('=' * submission_process_text_width, '=' * log_file_width, '=' * date_width, '=' * time_width))
        # print detail lines
        for key in sorted(log_dict.keys()):
            print(line_template.format(log_dict[key]['submission_process_text'], log_dict[key]['log_file'], log_dict[key]['date'], log_dict[key]['time']))

    # show continuation message 
    print(xlib.get_separator())
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

def form_view_submission_log():
    '''
    View the log of a submission.
    '''

    # initialize the control variable
    OK = True

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment('Logs - View a submission log')

    # get the submission log
    submission_log_file = cinputs.input_submission_log_file()
    if submission_log_file == '':
        print('WARNING: There is not any submission log.')
        OK = False
    
    # view the log file
    if OK:
        text = 'Logs - View a submission log'
        OK = clib.view_file(os.path.join(xlib.get_log_dir(), submission_log_file), text)

    # show continuation message 
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

def form_list_results_logs():
    '''
    List the processes of an experiment in the cluster.
    '''

    # initialize the control variable
    OK = True

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment('Logs - List result logs')

    # get experiment identification
    experiment_id = cinputs.input_experiment_id()
    if experiment_id == '':
        print('WARNING: There is not any experiment/process run.')
        OK = False

    # get the dictionary of TOA configuration.
    if OK:
        toa_config_dict = xtoa.get_toa_config_dict()

    # get the result dataset list of the experiment
    if OK:
        experiment_dir = f'{toa_config_dict["RESULT_DIR"]}/{experiment_id}'
        subdir_list = [subdir for subdir in os.listdir(experiment_dir) if os.path.isdir(os.path.join(experiment_dir, subdir))]
        result_dataset_id_list = []
        for subdir in subdir_list:
            result_dataset_id_list.append(subdir)

    # print the result dataset identification list of the experiment
    if OK:
        print(xlib.get_separator())
        if result_dataset_id_list == []:
            print(f'*** WARNING: There is not any result dataset of the experiment/process {experiment_id}.')
        else:
            result_dataset_id_list.sort()
            # set data width
            result_dataset_width = 25
            bioinfo_app_width = 25
            # set line template
            line_template = '{0:' + str(result_dataset_width) + '}   {1:' + str(bioinfo_app_width) + '}'
            # print header
            print(line_template.format('Result dataset', 'Bioinfo app / Utility'))
            print(line_template.format('=' * result_dataset_width, '=' * bioinfo_app_width))
            # print detail lines
            for result_dataset_id in result_dataset_id_list:

                if result_dataset_id.startswith(xlib.get_blastplus_code()+'-'):
                    bioinfo_app_name = xlib.get_blastplus_name()

                elif result_dataset_id.startswith(xlib.get_diamond_code()+'-'):
                    bioinfo_app_name = xlib.get_diamond_name()

                elif result_dataset_id.startswith(xlib.get_entrez_direct_code()+'-'):
                    bioinfo_app_name = xlib.get_entrez_direct_name()

                elif result_dataset_id.startswith(xlib.get_miniconda3_code()+'-'):
                    bioinfo_app_name = xlib.get_miniconda3_name()

                elif result_dataset_id.startswith(xlib.get_r_code()+'-'):
                    bioinfo_app_name = xlib.get_r_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_download_basic_data_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_download_basic_data_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_download_dicots_04_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_download_dicots_04_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_download_gene_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_download_gene_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_download_go_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_download_go_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_download_gymno_01_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_download_gymno_01_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_download_interpro_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_download_interpro_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_download_monocots_04_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_download_monocots_04_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_download_taxonomy_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_download_taxonomy_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_gilist_viridiplantae_nucleotide_gi_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_gilist_viridiplantae_nucleotide_gi_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_gilist_viridiplantae_protein_gi_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_gilist_viridiplantae_protein_gi_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_load_basic_data_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_load_basic_data_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_load_dicots_04_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_load_dicots_04_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_load_gene_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_load_gene_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_load_go_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_load_go_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_load_gymno_01_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_load_gymno_01_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_load_interpro_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_load_interpro_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_load_monocots_04_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_load_monocots_04_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_merge_annotations_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_merge_annotations_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_nr_blastplus_db_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_nr_blastplus_db_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_nr_diamond_db_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_nr_diamond_db_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_nt_blastplus_db_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_nt_blastplus_db_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_pipeline_aminoacid_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_pipeline_aminoacid_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_pipeline_nucleotide_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_pipeline_nucleotide_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_proteome_dicots_04_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_proteome_dicots_04_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_proteome_gymno_01_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_proteome_gymno_01_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_proteome_monocots_04_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_proteome_monocots_04_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_proteome_refseq_plant_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_proteome_refseq_plant_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_rebuild_toa_database_code()+'-'):
                    bioinfo_app_name = xlib.get_get_toa_process_rebuild_toa_database_name()

                elif result_dataset_id.startswith(xlib.get_toa_process_recreate_toa_database_code()+'-'):
                    bioinfo_app_name = xlib.get_get_toa_process_recreate_toa_database_name()

                elif result_dataset_id.startswith(xlib.get_transdecoder_code()+'-'):
                    bioinfo_app_name = xlib.get_transdecoder_name()

                else:
                    bioinfo_app_name = 'xxx'

                print(line_template.format(result_dataset_id, bioinfo_app_name))

    # show continuation message 
    print(xlib.get_separator())
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

def form_view_result_log():
    '''
    View the log of an experiment/process result.
    '''

    # initialize the control variable
    OK = True

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment('Logs - View an experiment/process result log')

    # get the experiment identification
    if OK:
        experiment_id = cinputs.input_experiment_id()
        if experiment_id == '':
            print('WARNING: There is not any experiment/process data.')
            OK = False

    # get the result_dataset identification
    if OK:
        result_dataset_id = cinputs.input_result_dataset_id(experiment_id, xlib.get_all_applications_selected_code())
        if result_dataset_id == '':
            print(f'WARNING: The experiment/process {experiment_id} does not have result datasets.')
            OK = False

    # get the dictionary of TOA configuration.
    if OK:
        toa_config_dict = xtoa.get_toa_config_dict()

    # get the log file name and build local and cluster paths
    if OK:
        log_file = f'{toa_config_dict["RESULT_DIR"]}/{experiment_id}/{result_dataset_id}/{xlib.get_run_log_file()}'
    
    # view the log file
    if OK:
        text = 'Logs - View an experiment/process log'
        OK = clib.view_file(log_file, text)

    # show continuation message 
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print('This file contains the functions related to forms corresponding to log menu items in mode console.')
    sys.exit(0)

#-------------------------------------------------------------------------------
