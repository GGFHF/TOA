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
This file contains the functions related to forms corresponding to TOA (Taxonomy-oriented Annotation)
menu items in console mode.
'''

#-------------------------------------------------------------------------------

import gzip
import os
import pathlib
import subprocess
import sys

import cinputs
import clib
import xlib
import xtoa

#-------------------------------------------------------------------------------

def form_create_toa_config_file():
    '''
    Create the TOA config file.
    '''

    # initialize the control variable
    OK = True

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment(f'{xlib.get_toa_name()} - Recreate config file')
    print(xlib.get_separator())

    # get the HOME directory
    home_dir = str(pathlib.Path.home())

    # set the TOA directory
    toa_dir = os.path.dirname(os.path.abspath(__file__))
    print(f'TOA directory: {toa_dir}')

    # set the Miniconda3 directory
    miniconda3_dir = cinputs.input_directory(directory_name='Miniconda3', default_directory=f'{home_dir}/{xlib.get_miniconda_dir()}', is_created=False)

    # set the database directory
    db_dir = cinputs.input_directory(directory_name='database', default_directory=f'{home_dir}/{xlib.get_toa_database_dir()}', is_created=False)

    # set the result directory
    result_dir = cinputs.input_directory(directory_name='result', default_directory=f'{home_dir}/{xlib.get_toa_result_dir()}', is_created=False)

    # create the TOA config file
    if OK:

        # confirm the creation of the config file
        print(xlib.get_separator())
        OK = clib.confirm_action(f'The file {xtoa.get_toa_config_file()} is going to be recreated. The previous files will be lost.')

        # recreate the config file
        if OK:
            (OK, error_list) = xtoa.create_toa_config_file(toa_dir, miniconda3_dir, db_dir, result_dir)
            if OK:
                print('The file is recreated.')
            else:
                for error in error_list:
                    print(error)

    # show continuation message 
    print(xlib.get_separator())
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

def form_manage_toa_database(process_type):
    '''
    Manage the TOA database.
    '''

    # initialize the control variable
    OK = True

    # print the header
    clib.clear_screen()
    if process_type == xlib.get_toa_type_recreate():
        clib.print_headers_with_environment(f'{xlib.get_toa_name()} - Recreate database')
    elif process_type == xlib.get_toa_type_rebuild():
        clib.print_headers_with_environment(f'{xlib.get_toa_name()} - Rebuild database')

    # confirm the process run
    if OK:
        print(xlib.get_separator())
        OK = clib.confirm_action(f'The {xlib.get_toa_name()} database is going to be {process_type}.')

    # run the process
    if OK:
        devstdout = xlib.DevStdOut(xtoa.manage_toa_database.__name__)
        OK = xtoa.manage_toa_database(process_type, devstdout, function=None)

    # show continuation message 
    print(xlib.get_separator())
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

def form_view_toa_config_file():
    '''
    List the TOA config file corresponding to the environment.
    '''

    # get the TOA config file
    toa_config_file = xtoa.get_toa_config_file()

    # view the file
    text = f'{xlib.get_toa_name()} - View config file'
    clib.view_file(toa_config_file, text)

    # show continuation message 
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

def form_manage_genomic_database(process_type, genomic_database):
    '''
    Manage processes of genomic database.
    '''

    # initialize the control variable
    OK = True

    # set the genomica database name
    if genomic_database == xlib.get_toa_data_basic_data_code():
        name = xlib.get_toa_data_basic_data_name()
    elif genomic_database == xlib.get_toa_data_gymno_01_code():
        name = xlib.get_toa_data_gymno_01_name()
    elif genomic_database == xlib.get_toa_data_dicots_04_code():
        name = xlib.get_toa_data_dicots_04_name()
    elif genomic_database == xlib.get_toa_data_monocots_04_code():
        name = xlib.get_toa_data_monocots_04_name()
    elif genomic_database == xlib.get_toa_data_refseq_plant_code():
        name = xlib.get_toa_data_refseq_plant_name()
    elif genomic_database == xlib.get_toa_data_taxonomy_code():
        name = xlib.get_toa_data_taxonomy_name()
    elif genomic_database == xlib.get_toa_data_nt_code():
        name = xlib.get_toa_data_nt_name()
    elif genomic_database == xlib.get_toa_data_viridiplantae_nucleotide_gi_code():
        name = xlib.get_toa_data_viridiplantae_nucleotide_gi_name()
    elif genomic_database == xlib.get_toa_data_nr_code():
        name = xlib.get_toa_data_nr_name()
    elif genomic_database == xlib.get_toa_data_viridiplantae_protein_gi_code():
        name = xlib.get_toa_data_viridiplantae_protein_gi_name()
    elif genomic_database == xlib.get_toa_data_gene_code():
        name = xlib.get_toa_data_gene_name()
    elif genomic_database == xlib.get_toa_data_interpro_code():
        name = xlib.get_toa_data_interpro_name()
    elif genomic_database == xlib.get_toa_data_go_code():
        name = xlib.get_toa_data_go_name()

    # print the header
    clib.clear_screen()
    if process_type == xlib.get_toa_type_build_blastplus_db():
        clib.print_headers_with_environment(f'Build {name} for BLAST+')
    elif process_type == xlib.get_toa_type_build_diamond_db():
        clib.print_headers_with_environment(f'Build {name} for DIAMOND')
    elif process_type == xlib.get_toa_type_build_gilist():
        clib.print_headers_with_environment(f'Build {name}')
    elif process_type == xlib.get_toa_type_build_proteome():
        clib.print_headers_with_environment(f'Build {name} proteome')
    elif process_type == xlib.get_toa_type_download_data():
        clib.print_headers_with_environment(f'Download {name} functional annotations')
    elif process_type == xlib.get_toa_type_load_data():
        clib.print_headers_with_environment(f'Load {name} data in {xlib.get_toa_name()} database')
    print(xlib.get_separator())

    # confirm the process run
    if OK:
        OK = clib.confirm_action(f'The {name} process is going to be run.')

    # run the process
    if OK:
        devstdout = xlib.DevStdOut(xtoa.manage_genomic_database.__name__)
        OK = xtoa.manage_genomic_database(process_type, genomic_database, devstdout, function=None)

    # show continuation message 
    print(xlib.get_separator())
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

def form_recreate_pipeline_config_file(pipeline_type):
    '''
    Recreate a pipeline config file.
    '''

    # initialize the control variable
    OK = True

    # set the pipeline name
    if pipeline_type == xlib.get_toa_process_pipeline_nucleotide_code():
        name = xlib.get_toa_process_pipeline_nucleotide_name()
    elif pipeline_type == xlib.get_toa_process_pipeline_aminoacid_code():
        name = xlib.get_toa_process_pipeline_aminoacid_name()

    # set the config file
    if pipeline_type == xlib.get_toa_process_pipeline_nucleotide_code():
        config_file = xtoa.get_nucleotide_pipeline_config_file()
    elif pipeline_type == xlib.get_toa_process_pipeline_aminoacid_code():
        config_file = xtoa.get_aminoacid_pipeline_config_file()

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment(f'{name} - Recreate config file')
    print(xlib.get_separator())

    # get the transcriptome directory
    transcriptome_dir = ''
    while transcriptome_dir == '':
        transcriptome_dir = input('Enter transcriptome directory: ')
        if not os.path.isdir(transcriptome_dir):
            print(f'***ERROR: The directory {transcriptome_dir} is not valid.')
            transcriptome_dir = ''

    # get the transcriptome file
    transcriptome_file = ''
    while transcriptome_file == '':
        transcriptome_dir = input('Enter transcriptome file: ')
        if not os.path.isfile(f'{transcriptome_dir}/{transcriptome_file}'):
            print(f'***ERROR: The file {transcriptome_file} is not valid.')
            transcriptome_dir = ''

    # get the database list
    if OK:

        # nucleotide pipelines
        if pipeline_type == xlib.get_toa_process_pipeline_nucleotide_code():
            database_list = cinputs.input_database_list(xtoa.get_nucleotide_annotation_database_code_list(), 'nt')

        # amino acid pipelines
        elif pipeline_type == xlib.get_toa_process_pipeline_aminoacid_code():
            database_list = cinputs.input_database_list(xtoa.get_aminoacid_annotation_database_code_list(), 'nr')

    # recreate the pipeline config file
    if OK:

        # confirm the creation of the config file
        print(xlib.get_separator())
        OK = clib.confirm_action(f'The file {config_file} is going to be recreated. The previous files will be lost.')

        # recreate the config file
        if OK:
            (OK, error_list) = xtoa.create_pipeline_config_file(pipeline_type, transcriptome_dir, transcriptome_file, database_list)
            if OK:
                print('The file is recreated.')
            else:
                for error in error_list:
                    print(error)

    # show continuation message 
    print(xlib.get_separator())
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

def form_recreate_annotation_merger_config_file():
    '''
    Recreate the annotation merger config file.
    '''

    # initialize the control variable
    OK = True

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment(f'{xlib.get_toa_process_merge_annotations_name()} - Recreate config file')

    # get the identification of the first pipeline dataset
    app_list = [xlib.get_toa_process_pipeline_nucleotide_code(), xlib.get_toa_process_pipeline_aminoacid_code(), xlib.get_toa_process_merge_annotations_code()]
    print('First pipeline ...')
    pipeline_dataset_id_1 = cinputs.input_result_dataset_id(xlib.get_toa_result_pipeline_dir(), app_list)
    if pipeline_dataset_id_1 == '':
        print( 'WARNING: There are not any pipeline datasets.')
        OK = False

    # get the identification of the second pipeline dataset
    app_list = [xlib.get_toa_process_pipeline_nucleotide_code(), xlib.get_toa_process_pipeline_aminoacid_code(), xlib.get_toa_process_merge_annotations_code()]
    print('Second pipeline ...')
    pipeline_dataset_id_2 = cinputs.input_result_dataset_id(xlib.get_toa_result_pipeline_dir(), app_list)
    if pipeline_dataset_id_2 == '':
        print( 'WARNING: There are not any pipeline datasets.')
        OK = False
    elif pipeline_dataset_id_1 == pipeline_dataset_id_2:
        print( 'ERROR: The first pipeline dataset is equal to the second one.')
        OK = False

    # get the merger operation
    if OK:
        merger_operation = cinputs.input_code(text='Merger operation', code_list=xlib.get_annotation_merger_operation_code_list(), default_code=None).upper()

    # recreate the pipeline config file
    if OK:

        # confirm the creation of the config file
        print(xlib.get_separator())
        OK = clib.confirm_action(f'The file {xtoa.get_annotation_merger_config_file()} is going to be recreated. The previous files will be lost.')

        # recreate the config file
        if OK:
            (OK, error_list) = xtoa.create_annotation_merger_config_file(pipeline_dataset_id_1, pipeline_dataset_id_2, merger_operation)
            if OK:
                print('The file is recreated.')
            else:
                for error in error_list:
                    print(error)

    # show continuation message 
    print(xlib.get_separator())
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

def form_edit_pipeline_config_file(pipeline_type):
    '''
    Edit a pipeline config file to change the parameters of each process.
    '''

    # initialize the control variable
    OK = True

    # set the pipeline name
    if pipeline_type == xlib.get_toa_process_pipeline_nucleotide_code():
        name = xlib.get_toa_process_pipeline_nucleotide_name()
    elif pipeline_type == xlib.get_toa_process_pipeline_aminoacid_code():
        name = xlib.get_toa_process_pipeline_aminoacid_name()
    elif pipeline_type == xlib.get_toa_process_merge_annotations_code():
        name = xlib.get_toa_process_merge_annotations_name()

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment(f'{name} - Edit config file')

    # get the config file
    if pipeline_type == xlib.get_toa_process_pipeline_nucleotide_code():
        config_file = xtoa.get_nucleotide_pipeline_config_file()
    elif pipeline_type == xlib.get_toa_process_pipeline_aminoacid_code():
        config_file = xtoa.get_aminoacid_pipeline_config_file()
    elif pipeline_type == xlib.get_toa_process_merge_annotations_code():
        config_file = xtoa.get_annotation_merger_config_file()

    # edit the read transfer config file
    print(xlib.get_separator())
    print(f'Editing the {name} config file ...')
    command = f'{xlib.get_editor()} {config_file}'
    rc = subprocess.call(command, shell=True)
    if rc != 0:
        print(f'*** ERROR: RC {rc} in command -> {command}')
        OK = False

    # check the config file
    if OK:
        print(xlib.get_separator())
        print(f'Checking the {name} config file ...')
        if pipeline_type == xlib.get_toa_process_pipeline_nucleotide_code():
            (OK, error_list) = xtoa.check_pipeline_config_file(pipeline_type, strict=False)
        elif pipeline_type == xlib.get_toa_process_pipeline_aminoacid_code():
            (OK, error_list) = xtoa.check_pipeline_config_file(pipeline_type, strict=False)
        elif pipeline_type == xlib.get_toa_process_merge_annotations_code():
            (OK, error_list) = xtoa.check_annotation_merger_config_file(strict=False)
        if OK:
            print('The file is OK.')
        else:
            print()
            for error in error_list:
                print(error)

    # show continuation message 
    print(xlib.get_separator())
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

def form_run_pipeline_process(pipeline_type):
    '''
    Run a pipeline process with the parameters in the corresponding config file.
    '''

    # initialize the control variable
    OK = True

    # set the pipeline name
    if pipeline_type == xlib.get_toa_process_pipeline_nucleotide_code():
        name = xlib.get_toa_process_pipeline_nucleotide_name()

    elif pipeline_type == xlib.get_toa_process_pipeline_aminoacid_code():
        name = xlib.get_toa_process_pipeline_aminoacid_name()

    elif pipeline_type == xlib.get_toa_process_merge_annotations_code():
        name = xlib.get_toa_process_merge_annotations_name()

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment(f'{name} - Run process')

    # confirm the process run
    if OK:
        print(xlib.get_separator())
        OK = clib.confirm_action(f'The {name} process is going to be run.')

    # run the process
    if OK:

        if pipeline_type == xlib.get_toa_process_pipeline_nucleotide_code():
            devstdout = xlib.DevStdOut(xtoa.run_pipeline_process.__name__)
            OK = xtoa.run_pipeline_process(pipeline_type, devstdout, function=None)

        elif pipeline_type == xlib.get_toa_process_pipeline_aminoacid_code():
            devstdout = xlib.DevStdOut(xtoa.run_pipeline_process.__name__)
            OK = xtoa.run_pipeline_process(pipeline_type, devstdout, function=None)

        elif pipeline_type == xlib.get_toa_process_merge_annotations_code():
            devstdout = xlib.DevStdOut(xtoa.run_annotation_merger_process.__name__)
            OK = xtoa.run_annotation_merger_process(devstdout, function=None)

    # show continuation message 
    print(xlib.get_separator())
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

def form_restart_pipeline_process(pipeline_type):
    '''
    Restart a pipeline process from the last step ended OK.
    '''

    # initialize the control variable
    OK = True

    # set the pipeline name
    if pipeline_type == xlib.get_toa_process_pipeline_nucleotide_code():
        name = xlib.get_toa_process_pipeline_nucleotide_name()
    elif pipeline_type == xlib.get_toa_process_pipeline_aminoacid_code():
        name = xlib.get_toa_process_pipeline_aminoacid_name()

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment(f'{name} - Run process')

    # get the pipeline dataset identification
    app_list = [pipeline_type]
    pipeline_dataset_id = cinputs.input_result_dataset_id(xlib.get_toa_result_pipeline_dir(), app_list)
    if pipeline_dataset_id == '':
        print(f'WARNING: There are not any {pipeline_type} result datasets.')
        OK = False

    # confirm the process run
    if OK:
        print(xlib.get_separator())
        OK = clib.confirm_action(f'The {name} process is going to be run.')

    # run the process
    if OK:

        devstdout = xlib.DevStdOut(xtoa.restart_pipeline_process.__name__)
        OK = xtoa.restart_pipeline_process(pipeline_type, pipeline_dataset_id, devstdout, function=None)

    # show continuation message 
    print(xlib.get_separator())
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

def form_view_x_per_y_data(stats_code):
    '''
    View the x per y data.
    '''

    # initialize the control variable
    OK = True

    # assign the text of the "name"
    if stats_code == 'hit_per_hsp':
        name = '# HITs per # HSPs'
    elif stats_code == 'seq_per_go':
        name = '# sequences per # GO terms'
    elif stats_code == 'seq_per_ec':
        name = '# sequences per # EC ids'
    elif stats_code == 'seq_per_interpro':
        name = '# sequences per # InterPro ids'
    elif stats_code == 'seq_per_kegg':
        name = '# sequences per # KEGG ids'
    elif stats_code == 'seq_per_mapman':
        name = '# sequences per # MapMan ids'
    elif stats_code == 'seq_per_metacyc':
        name = '# sequences per # MetaCyc ids'

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment(f'Statistics - {name} data')

    # get the pipeline dataset identification
    if stats_code == 'hit_per_hsp':
        app_list = [xlib.get_toa_process_pipeline_nucleotide_code(), xlib.get_toa_process_pipeline_aminoacid_code()]
    else:
        app_list = [xlib.get_toa_process_pipeline_nucleotide_code(), xlib.get_toa_process_pipeline_aminoacid_code(), xlib.get_toa_process_merge_annotations_code()]
    pipeline_dataset_id = cinputs.input_result_dataset_id(xlib.get_toa_result_pipeline_dir(), app_list)
    if pipeline_dataset_id == '':
        print('WARNING: There are not any annotation pipeline result datasets.')
        OK = False

    # build distribution dictionary
    if OK:

        # initialize the distribution dictionary
        distribution_dict = {}

        # get the dictionary of TOA configuration
        toa_config_dict = xtoa.get_toa_config_dict()

        # get the statistics file path
        stats_file = f'{toa_config_dict["RESULT_DIR"]}/{xlib.get_toa_result_pipeline_dir()}/{pipeline_dataset_id}/{toa_config_dict["STATS_SUBDIR_NAME"]}/{stats_code}-{toa_config_dict["STATS_BASE_NAME"]}.csv'

        # open the statistics file
        if stats_file.endswith('.gz'):
            try:
                stats_file_id = gzip.open(stats_file, mode='rt', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F002', stats_file)
        else:
            try:
                stats_file_id = open(stats_file, mode='r', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F001', stats_file)

        # initialize the record counter
        record_counter = 0

        # initialize the header record control
        header_record = True

        # read the first record
        record = stats_file_id.readline()

        # while there are records
        while record != '':

            # add 1 to the record counter
            record_counter += 1

            # process the header record
            if header_record:
                header_record = False

            # process data records
            else:

                # extract data
                # record format: "x_count";"y_count"
                data_list = []
                begin = 0
                for end in [i for i, chr in enumerate(record) if chr == ';']:
                    data_list.append(record[begin:end].strip('"'))
                    begin = end + 1
                data_list.append(record[begin:].strip('\n').strip('"'))
                try:
                    x_count = data_list[0]
                    y_count = data_list[1]
                except Exception as e:
                    raise xlib.ProgramException('F006', os.path.basename(stats_file), record_counter)

                # add dato to the dictionary
                distribution_dict[record_counter] = {'x_count': x_count, 'y_count': y_count}

            # read the next record
            record = stats_file_id.readline()

    # print the distribution
    if OK:
        print(xlib.get_separator())
        if distribution_dict == {}:
            print('*** WARNING: There is not any stats data.')
        else:
            # set data width
            x_count_width = 15
            y_count_width = 15
            # set line template
            line_template = '{0:' + str(x_count_width) + '}   {1:' + str(y_count_width) + '}'
            # print header
            if stats_code == 'hit_per_hsp':
                print(line_template.format('# HSPs', '# HITs'))
            elif stats_code == 'seq_per_go':
                print(line_template.format('# GO terms', '# sequences'))
            elif stats_code == 'seq_per_ec':
                print(line_template.format('# EC ids', '# sequences'))
            elif stats_code == 'seq_per_interpro':
                print(line_template.format('# InterPro ids', '# sequences'))
            elif stats_code == 'seq_per_kegg':
                print(line_template.format('# KEGG ids', '# sequences'))
            elif stats_code == 'seq_per_mapman':
                print(line_template.format('# MapMan ids', '# sequences'))
            elif stats_code == 'seq_per_metacyc':
                print(line_template.format('# MetaCyc ids', '# sequences'))
            print(line_template.format('=' * x_count_width, '=' * y_count_width))
            # print detail lines
            for key in sorted(distribution_dict.keys()):
                print(line_template.format(distribution_dict[key]['x_count'], distribution_dict[key]['y_count']))

    # show continuation message 
    print(xlib.get_separator())
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

def form_view_dataset_data_frecuency():
    '''
    View the frecuency distribution of annotation dataset data.
    '''

    # initialize the control variable
    OK = True

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment('Statistics - Annotation datasets - Frequency distribution data')

    # get the pipeline dataset identification
    app_list = [xlib.get_toa_process_pipeline_nucleotide_code(), xlib.get_toa_process_pipeline_aminoacid_code()]
    pipeline_dataset_id = cinputs.input_result_dataset_id(xlib.get_toa_result_pipeline_dir(), app_list)
    if pipeline_dataset_id == '':
        print('WARNING: There are not any annotation pipeline result datasets.')
        OK = False

    # build distribution dictionary
    if OK:

        # initialize the distribution dictionary
        distribution_dict = {}

        # get the dictionary of TOA configuration
        toa_config_dict = xtoa.get_toa_config_dict()

        # get the statistics file path
        stats_file = f'{toa_config_dict["RESULT_DIR"]}/{xlib.get_toa_result_pipeline_dir()}/{pipeline_dataset_id}/{toa_config_dict["STATS_SUBDIR_NAME"]}/dataset-{toa_config_dict["STATS_BASE_NAME"]}.csv'

        # open the statistics file
        if stats_file.endswith('.gz'):
            try:
                stats_file_id = gzip.open(stats_file, mode='rt', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F002', stats_file)
        else:
            try:
                stats_file_id = open(stats_file, mode='r', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F001', stats_file)

        # initialize the record counter
        record_counter = 0

        # initialize the header record control
        header_record = True

        # read the first record
        record = stats_file_id.readline()

        # while there are records
        while record != '':

            # add 1 to the record counter
            record_counter += 1

            # process the header record
            if header_record:
                header_record = False

            # process data records
            else:

                # extract data
                # record format: "dataset_name";"annotated_seq_count";"remained_seq_count"
                data_list = []
                begin = 0
                for end in [i for i, chr in enumerate(record) if chr == ';']:
                    data_list.append(record[begin:end].strip('"'))
                    begin = end + 1
                data_list.append(record[begin:].strip('\n').strip('"'))
                try:
                    dataset_name = data_list[0]
                    annotated_seq_count = data_list[1]
                    remained_seq_count = data_list[2]
                except Exception as e:
                    raise xlib.ProgramException('F006', os.path.basename(stats_file), record_counter)

                # add dato to the dictionary
                distribution_dict[record_counter] = {'dataset_name': dataset_name, 'annotated_seq_count': annotated_seq_count, 'remained_seq_count': remained_seq_count}

            # read the next record
            record = stats_file_id.readline()

    # print the distribution
    if OK:
        print(xlib.get_separator())
        if distribution_dict == {}:
            print('*** WARNING: There is not any distribution.')
        else:
            # set data width
            dataset_name_width = 19
            annotated_seq_count_width = 14
            remained_seq_count_width = 14
            # set line template
            line_template = '{0:' + str(dataset_name_width) + '}   {1:' + str(annotated_seq_count_width) + '}   {2:' + str(remained_seq_count_width) + '}'
            # print header
            print(line_template.format('Dataset', 'Annotated seqs', 'Remained seqs'))
            print(line_template.format('=' * dataset_name_width, '=' * annotated_seq_count_width, '=' * remained_seq_count_width))
            # print detail lines
            for key in sorted(distribution_dict.keys()):
                print(line_template.format(distribution_dict[key]['dataset_name'], distribution_dict[key]['annotated_seq_count'], distribution_dict[key]['remained_seq_count']))

    # show continuation message 
    print(xlib.get_separator())
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

def form_view_phylogenic_data_frecuency(stats_code):
    '''
    View the frecuency distribution of phylogenic data.
    '''

    # initialize the control variable
    OK = True

    # assign the text of the "name"
    if stats_code == 'species':
        name = 'Species - Frequency distribution'
    elif stats_code == 'family':
        name = 'Family - Frequency distribution'
    elif stats_code == 'phylum':
        name = 'Phylum - Frequency distribution'
    elif stats_code == 'namespace':
        name = 'GO - Frequency distribution per namespace'

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment(f'Statistics - {name} data')

    # get the pipeline dataset identification
    app_list = [xlib.get_toa_process_pipeline_nucleotide_code(), xlib.get_toa_process_pipeline_aminoacid_code(), xlib.get_toa_process_merge_annotations_code()]
    pipeline_dataset_id = cinputs.input_result_dataset_id(xlib.get_toa_result_pipeline_dir(), app_list)
    if pipeline_dataset_id == '':
        print('WARNING: There are not any annotation pipeline result datasets.')
        OK = False

    # build distribution dictionary
    if OK:

        # initialize the distribution dictionary
        distribution_dict = {}

        # get the dictionary of TOA configuration
        toa_config_dict = xtoa.get_toa_config_dict()

        # get the statistics file path
        stats_file = f'{toa_config_dict["RESULT_DIR"]}/{xlib.get_toa_result_pipeline_dir()}/{pipeline_dataset_id}/{toa_config_dict["STATS_SUBDIR_NAME"]}/{stats_code}-{toa_config_dict["STATS_BASE_NAME"]}.csv'

        # open the statistics file
        if stats_file.endswith('.gz'):
            try:
                stats_file_id = gzip.open(stats_file, mode='rt', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F002', stats_file)
        else:
            try:
                stats_file_id = open(stats_file, mode='r', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F001', stats_file)

        # initialize the record counter
        record_counter = 0

        # initialize the header record control
        header_record = True

        # read the first record
        record = stats_file_id.readline()

        # while there are records
        while record != '':

            # add 1 to the record counter
            record_counter += 1

            # process the header record
            if header_record:
                header_record = False

            # process data records
            else:

                # extract data
                # record format: "stats_code_id";"all_count";"first_hsp_count";"min_evalue_count"
                data_list = []
                begin = 0
                for end in [i for i, chr in enumerate(record) if chr == ';']:
                    data_list.append(record[begin:end].strip('"'))
                    begin = end + 1
                data_list.append(record[begin:].strip('\n').strip('"'))
                try:
                    id = data_list[0]
                    all_count = data_list[1]
                    first_hsp_count = data_list[2]
                    min_evalue_count = data_list[3]
                except Exception as e:
                    raise xlib.ProgramException('F006', os.path.basename(stats_file), record_counter)

                # add dato to the dictionary
                distribution_dict[id] = {'id': id, 'all_count': all_count, 'first_hsp_count': first_hsp_count, 'min_evalue_count': min_evalue_count}

            # read the next record
            record = stats_file_id.readline()

    # print the distribution
    if OK:
        print(xlib.get_separator())
        if distribution_dict == {}:
            print('*** WARNING: There is not any distribution.')
        else:
            # set data width
            id_width = 50
            all_count_width = 11
            first_hsp_count_width = 11
            min_evalue_count_width = 11
            # set line template
            line_template = '{0:' + str(id_width) + '}   {1:' + str(all_count_width) + '}   {2:' + str(first_hsp_count_width) + '}   {3:' + str(min_evalue_count_width) + '}'
            # print header
            print(line_template.format(stats_code.capitalize(), 'All', 'First HSP', 'Min e-value'))
            print(line_template.format('=' * id_width, '=' * all_count_width, '=' * first_hsp_count_width, '=' * min_evalue_count_width))
            # print detail lines
            for key in sorted(distribution_dict.keys()):
                print(line_template.format(distribution_dict[key]['id'], distribution_dict[key]['all_count'], distribution_dict[key]['first_hsp_count'], distribution_dict[key]['min_evalue_count']))

    # show continuation message 
    print(xlib.get_separator())
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

def form_view_ontologic_data_frecuency(stats_code):
    '''
    View the frecuency distribution of ontologic data.
    '''

    # initialize the control variable
    OK = True

    # assign the text of the "name"
    if stats_code == 'go':
        name = 'Gene Ontology - Frequency distribution'
    elif stats_code == 'ec':
        name = 'EC - Frequency distribution'
    elif stats_code == 'interpro':
        name = 'InterPro - Frequency distribution'
    elif stats_code == 'kegg':
        name = 'KEGG - Frequency distribution'
    elif stats_code == 'mapman':
        name = 'MapMan - Frequency distribution'
    elif stats_code == 'metacyc':
        name = 'MetaCyc - Frequency distribution'

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment(f'Statistics - {name} data')

    # get the pipeline dataset identification
    app_list = [xlib.get_toa_process_pipeline_nucleotide_code(), xlib.get_toa_process_pipeline_aminoacid_code(), xlib.get_toa_process_merge_annotations_code()]
    pipeline_dataset_id = cinputs.input_result_dataset_id(xlib.get_toa_result_pipeline_dir(), app_list)
    if pipeline_dataset_id == '':
        print('WARNING: There are not any annotation pipeline result datasets.')
        OK = False

    # build distribution dictionary
    if OK:

        # initialize the distribution dictionary
        distribution_dict = {}

        # get the dictionary of TOA configuration
        toa_config_dict = xtoa.get_toa_config_dict()

        # get the statistics file path
        stats_file = f'{toa_config_dict["RESULT_DIR"]}/{xlib.get_toa_result_pipeline_dir()}/{pipeline_dataset_id}/{toa_config_dict["STATS_SUBDIR_NAME"]}/{stats_code}-{toa_config_dict["STATS_BASE_NAME"]}.csv'

        # open the statistics file
        if stats_file.endswith('.gz'):
            try:
                stats_file_id = gzip.open(stats_file, mode='rt', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F002', stats_file)
        else:
            try:
                stats_file_id = open(stats_file, mode='r', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F001', stats_file)

        # initialize the record counter
        record_counter = 0

        # initialize the header record control
        header_record = True

        # read the first record
        record = stats_file_id.readline()

        # while there are records
        while record != '':

            # add 1 to the record counter
            record_counter += 1

            # process the header record
            if header_record:
                header_record = False

            # process data records
            else:

                # extract data
                # record format: "stats_code_id";"description";"all_count";"first_hsp_count";"min_evalue_count"
                data_list = []
                begin = 0
                for end in [i for i, chr in enumerate(record) if chr == ';']:
                    data_list.append(record[begin:end].strip('"'))
                    begin = end + 1
                data_list.append(record[begin:].strip('\n').strip('"'))
                try:
                    id = data_list[0]
                    desc = data_list[1]
                    all_count = data_list[2]
                    first_hsp_count = data_list[3]
                    min_evalue_count = data_list[4]
                except Exception as e:
                    raise xlib.ProgramException('F006', os.path.basename(stats_file), record_counter)

                # add dato to the dictionary
                distribution_dict[id] = {'id': id, 'desc': desc, 'all_count': all_count, 'first_hsp_count': first_hsp_count, 'min_evalue_count': min_evalue_count}

            # read the next record
            record = stats_file_id.readline()

    # print the distribution
    if OK:
        print(xlib.get_separator())
        if distribution_dict == {}:
            print('*** WARNING: There is not any distribution.')
        else:
            # set data width
            id_width = 30
            desc_width = 70
            all_count_width = 11
            first_hsp_count_width = 11
            min_evalue_count_width = 11
            # set line template
            line_template = '{0:' + str(id_width) + '}   {1:' + str(desc_width) + '}   {2:' + str(all_count_width) + '}   {3:' + str(first_hsp_count_width) + '}   {4:' + str(min_evalue_count_width) + '}'
            # print header
            print(line_template.format(f'{stats_code.capitalize()} id', 'Description', 'All', 'First HSP', 'Min e-value'))
            print(line_template.format('=' * id_width, '=' * desc_width, '=' * all_count_width, '=' * first_hsp_count_width, '=' * min_evalue_count_width))
            # print detail lines
            for key in sorted(distribution_dict.keys()):
                print(line_template.format(distribution_dict[key]['id'], distribution_dict[key]['desc'], distribution_dict[key]['all_count'], distribution_dict[key]['first_hsp_count'], distribution_dict[key]['min_evalue_count']))

    # show continuation message 
    print(xlib.get_separator())
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

def form_view_go_data_frecuency():
    '''
    View the frecuency distribution of Gene Ontology data.
    '''

    # initialize the control variable
    OK = True

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment('Statistics - Gene Ontology - Frequency distribution data')

    # get the pipeline dataset identification
    app_list = [xlib.get_toa_process_pipeline_nucleotide_code(), xlib.get_toa_process_pipeline_aminoacid_code(), xlib.get_toa_process_merge_annotations_code()]
    pipeline_dataset_id = cinputs.input_result_dataset_id(xlib.get_toa_result_pipeline_dir(), app_list)
    if pipeline_dataset_id == '':
        print('WARNING: There are not any annotation pipeline result datasets.')
        OK = False

    # build distribution dictionary
    if OK:

        # initialize the distribution dictionary
        distribution_dict = {}

        # get the dictionary of TOA configuration
        toa_config_dict = xtoa.get_toa_config_dict()

        # get the statistics file path
        stats_file = f'{toa_config_dict["RESULT_DIR"]}/{xlib.get_toa_result_pipeline_dir()}/{pipeline_dataset_id}/{toa_config_dict["STATS_SUBDIR_NAME"]}/go-{toa_config_dict["STATS_BASE_NAME"]}.csv'

        # open the statistics file
        if stats_file.endswith('.gz'):
            try:
                stats_file_id = gzip.open(stats_file, mode='rt', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F002', stats_file)
        else:
            try:
                stats_file_id = open(stats_file, mode='r', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F001', stats_file)

        # initialize the record counter
        record_counter = 0

        # initialize the header record control
        header_record = True

        # read the first record
        record = stats_file_id.readline()

        # while there are records
        while record != '':

            # add 1 to the record counter
            record_counter += 1

            # process the header record
            if header_record:
                header_record = False

            # process data records
            else:

                # extract data
                # record format: "go_id";"description";"namespace";"all_count";"first_hsp_count";"min_evalue_count"
                data_list = []
                begin = 0
                for end in [i for i, chr in enumerate(record) if chr == ';']:
                    data_list.append(record[begin:end].strip('"'))
                    begin = end + 1
                data_list.append(record[begin:].strip('\n').strip('"'))
                try:
                    id = data_list[0]
                    desc = data_list[1]
                    namespace = data_list[2]
                    all_count = data_list[3]
                    first_hsp_count = data_list[4]
                    min_evalue_count = data_list[5]
                except Exception as e:
                    raise xlib.ProgramException('F006', os.path.basename(stats_file), record_counter)

                # add dato to the dictionary
                distribution_dict[id] = {'id': id, 'desc': desc, 'namespace': namespace, 'all_count': all_count, 'first_hsp_count': first_hsp_count, 'min_evalue_count': min_evalue_count}

            # read the next record
            record = stats_file_id.readline()

    # print the distribution
    if OK:
        print(xlib.get_separator())
        if distribution_dict == {}:
            print('*** WARNING: There is not any distribution.')
        else:
            # set data width
            id_width = 10
            desc_width = 50
            namespace_width = 18
            all_count_width = 11
            first_hsp_count_width = 11
            min_evalue_count_width = 11
            # set line template
            line_template = '{0:' + str(id_width) + '}   {1:' + str(desc_width) + '}   {2:' + str(namespace_width) + '}   {3:' + str(all_count_width) + '}   {4:' + str(first_hsp_count_width) + '}   {5:' + str(min_evalue_count_width) + '}'
            # print header
            print(line_template.format('GO id', 'Description', 'Namespace', 'All', 'First HSP', 'Min e-value'))
            print(line_template.format('=' * id_width, '=' * desc_width, '=' * namespace_width, '=' * all_count_width, '=' * first_hsp_count_width, '=' * min_evalue_count_width))
            # print detail lines
            for key in sorted(distribution_dict.keys()):
                print(line_template.format(distribution_dict[key]['id'], distribution_dict[key]['desc'], distribution_dict[key]['namespace'], distribution_dict[key]['all_count'], distribution_dict[key]['first_hsp_count'], distribution_dict[key]['min_evalue_count']))

    # show continuation message 
    print(xlib.get_separator())
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print('This file contains the functions related to forms corresponding to TOA (Taxonomy-oriented Annotation) menu items in console mode.')
    sys.exit(0)

#-------------------------------------------------------------------------------
