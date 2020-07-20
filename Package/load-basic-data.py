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
This program loads datasets and species data into TOA database.
'''

#-------------------------------------------------------------------------------

import argparse
import gzip
import os
import re
import sys

import xlib
import xsqlite

#-------------------------------------------------------------------------------

def main(argv):
    '''
    Main line of the program.
    '''

    # check the operating system
    xlib.check_os()

    # get and check the arguments
    parser = build_parser()
    args = parser.parse_args()
    check_args(args)

    # connect to the TOA database
    conn = xsqlite.connect_database(args.toa_database)

    # load table "datasets"
    load_table_datasets(conn, args.dataset_file)

    # load table "species"
    load_table_species(conn, args.species_file)

    # load table "ec_ids"
    load_table_ec_ids(conn, args.ec_id_file)

    # load table "kegg_ids"
    load_table_kegg_ids(conn, args.kegg_id_file)

    # close connection to TOA database
    conn.close()

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program loads datasets and species data into TOA database.'
    text = f'{xlib.get_long_project_name()} v{xlib.get_project_version()} - {os.path.basename(__file__)}\n\n{description}\n'
    usage = f'\r{text.ljust(len("usage:"))}\nUsage: {os.path.basename(__file__)} arguments'
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--db', dest='toa_database', help='Path of the TOA database (mandatory).')
    parser.add_argument('--datasets', dest='dataset_file', help='Path of the dataset file (mandatory).')
    parser.add_argument('--species', dest='species_file', help='Path of species file (mandatory).')
    parser.add_argument('--ecids', dest='ec_id_file', help='Path of EC id file (mandatory).')
    parser.add_argument('--keggids', dest='kegg_id_file', help='Path of KEGG id file (mandatory).')
    parser.add_argument('--verbose', dest='verbose', help=f'Additional job status info during the run: {xlib.get_verbose_code_list_text()}; default: {xlib.Const.DEFAULT_VERBOSE}.')
    parser.add_argument('--trace', dest='trace', help=f'Additional info useful to the developer team: {xlib.get_trace_code_list_text()}; default: {xlib.Const.DEFAULT_TRACE}.')

    # return the paser
    return parser

#-------------------------------------------------------------------------------

def check_args(args):
    '''
    Check the input arguments.
    '''

    # initialize the control variable
    OK = True

    # check "toa_database"
    if args.toa_database is None:
        xlib.Message.print('error', '*** The TOA database is not indicated in the input arguments.')
        OK = False

    # check "dataset_file"
    if args.dataset_file is None:
        xlib.Message.print('error', '*** The dataset file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.dataset_file):
        xlib.Message.print('error', f'*** The file {args.dataset_file} does not exist.')
        OK = False

    # check "species_file"
    if args.species_file is None:
        xlib.Message.print('error', '*** The species file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.species_file):
        xlib.Message.print('error', f'*** The file {args.species_file} does not exist.')
        OK = False

    # check "ec_id_file"
    if args.ec_id_file is None:
        xlib.Message.print('error', '*** The EC id file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.ec_id_file):
        xlib.Message.print('error', f'*** The file {args.ec_id_file} does not exist.')
        OK = False

    # check "kegg_id_file"
    if args.kegg_id_file is None:
        xlib.Message.print('error', '*** The KEGG id file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.kegg_id_file):
        xlib.Message.print('error', f'*** The file {args.kegg_id_file} does not exist.')
        OK = False

    # check "verbose"
    if args.verbose is None:
        args.verbose = xlib.Const.DEFAULT_VERBOSE
    elif not xlib.check_code(args.verbose, xlib.get_verbose_code_list(), case_sensitive=False):
        xlib.Message.print('error', f'*** verbose has to be {xlib.get_verbose_code_list_text()}.')
        OK = False
    if args.verbose.upper() == 'Y':
        xlib.Message.set_verbose_status(True)

    # check "trace"
    if args.trace is None:
        args.trace = xlib.Const.DEFAULT_TRACE
    elif not xlib.check_code(args.trace, xlib.get_trace_code_list(), case_sensitive=False):
        xlib.Message.print('error', f'*** trace has to be {xlib.get_trace_code_list_text()}.')
        OK = False
    if args.trace.upper() == 'Y':
        xlib.Message.set_trace_status(True)

    # if there are errors, exit with exception
    if not OK:
        raise xlib.ProgramException('P001')

#-------------------------------------------------------------------------------

def load_table_datasets(conn, dataset_file):
    '''
    '''

    # initialize the record counter
    record_counter = 0

    # initialize the inserted row counter
    inserted_row_counter = 0

    # set the pattern of the data records
    # format: "repository_id";"dataset_id";"dataset_name";"ftp_adress"
    record_pattern = re.compile(r'^"(.*)";"(.*)";"(.*)";"(.*)"$')
    
    # drop table "datasets"
    xlib.Message.print('verbose', 'Droping the table "datasets" ...\n')
    xsqlite.drop_datasets(conn)
    xlib.Message.print('verbose', 'The table is droped.\n')
    
    # create table "datasets"
    xlib.Message.print('verbose', 'Creating the table "datasets" ...\n')
    xsqlite.create_datasets(conn)
    xlib.Message.print('verbose', 'The table is created.\n')

    # open the file of datasets
    if dataset_file.endswith('.gz'):
        try:
            dataset_file_id = gzip.open(dataset_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', dataset_file)
    else:
        try:
            dataset_file_id = open(dataset_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', dataset_file)

    # read the first record
    record = dataset_file_id.readline()

    # while there are records
    while record != '':

        # add 1 to record counter
        record_counter += 1

        # process data records
        if not record.lstrip().startswith('#') and record.strip() != '':

            # initialize the row data dictionary
            row_dict = {}

            # extract data
            try:
                mo = record_pattern.match(record)
                row_dict['dataset_id'] = mo.group(1).strip().lower()
                row_dict['dataset_name'] = mo.group(2).strip()
                row_dict['repository_id'] = mo.group(3).strip().lower()
                row_dict['ftp_adress'] = mo.group(4).strip()
            except Exception as e:
                raise xlib.ProgramException('F006', os.path.basename(dataset_file), record_counter)

            # review null values of "ftp_adress"
            if row_dict['ftp_adress'] == '':
                row_dict['ftp_adress'] = xlib.get_na()

            # insert data into table "datasets"
            xsqlite.insert_datasets_row(conn, row_dict)
            inserted_row_counter += 1

        # print record counter
        xlib.Message.print('verbose', f'\rProcessed records of dataset file: {record_counter} - Inserted rows: {inserted_row_counter}')

        # read the next record
        record = dataset_file_id.readline()

    xlib.Message.print('verbose', '\n')
    
    # create the index on the table "datasets"
    xlib.Message.print('verbose', 'Creating the index on the table "datasets" ...\n')
    xsqlite.create_datasets_index(conn)
    xlib.Message.print('verbose', 'The index is created.\n')

    # save changes into TOA database
    xlib.Message.print('verbose', 'Saving changes into TOA database ...\n')
    conn.commit()
    xlib.Message.print('verbose', 'Changes are saved.\n')

    # close dataset file
    dataset_file_id.close()

#-------------------------------------------------------------------------------

def load_table_species(conn, species_file):
    '''
    '''
    
    # drop table "species" (if it exists)
    xlib.Message.print('verbose', 'Droping the table "species" ...\n')
    xsqlite.drop_species(conn)
    xlib.Message.print('verbose', 'The table is droped.\n')
    
    # create table "species"
    xlib.Message.print('verbose', 'Creating the table "species" ...\n')
    xsqlite.create_species(conn)
    xlib.Message.print('verbose', 'The table is created.\n')

    # open the file of species data
    if species_file.endswith('.gz'):
        try:
            species_file_id = gzip.open(species_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', species_file)
    else:
        try:
            species_file_id = open(species_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', species_file)

    # set the pattern of the data records
    # format: "species_name";"plaza_id"
    record_pattern = re.compile(r'^"(.*)";"(.*)"$')

    # initialize the record counter
    record_counter = 0

    # initialize the inserted row counter
    inserted_row_counter = 0

    # read the first record
    record = species_file_id.readline()

    # while there are records
    while record != '':

        # add 1 to record counter
        record_counter += 1

        # process data records
        if not record.lstrip().startswith('#') and record.strip() != '':

            # initialize the row data dictionary
            row_dict = {}

            # extract data 
            try:
                mo = record_pattern.match(record)
                row_dict['species_name'] = mo.group(1).strip().capitalize()
                row_dict['plaza_species_id'] = mo.group(2).strip().lower()
            except Exception as e:
                raise xlib.ProgramException('F006', os.path.basename(species_file), record_counter)

            # get the taxonomy dictionary of the species name from taxonomy server
            taxonomy_dict = xlib.get_taxonomy_dict('name', row_dict['species_name'])
            if taxonomy_dict == {}:
                row_dict['family_name'] = xlib.get_na()
                row_dict['phylum_name'] = xlib.get_na()
                row_dict['kingdom_name'] = xlib.get_na()
                row_dict['superkingdom_name'] = xlib.get_na()
                row_dict['tax_id'] = xlib.get_na()
            else:
                row_dict['family_name'] = taxonomy_dict['family']['name']
                row_dict['phylum_name'] = taxonomy_dict['phylum']['name']
                row_dict['kingdom_name'] = taxonomy_dict['kingdom']['name']
                row_dict['superkingdom_name'] = taxonomy_dict['superkingdom']['name']
                row_dict['tax_id'] = taxonomy_dict['tax_id']

            # insert data into table species
            xsqlite.insert_species_row(conn, row_dict)
            inserted_row_counter += 1

        # print record counter
        xlib.Message.print('verbose', f'\rProcessed records of species file: {record_counter} - Inserted rows: {inserted_row_counter}')

        # read the next record
        record = species_file_id.readline()

    xlib.Message.print('verbose', '\n')
    
    # create the index on the table "species"
    xlib.Message.print('verbose', 'Creating the index on the table "species" ...\n')
    xsqlite.create_species_index(conn)
    xlib.Message.print('verbose', 'The index is created.\n')

    # save changes into TOA database
    xlib.Message.print('verbose', 'Saving changes into TOA database ...\n')
    conn.commit()
    xlib.Message.print('verbose', 'Changes are saved.\n')

    # close species file
    species_file_id.close()

#-------------------------------------------------------------------------------

def load_table_ec_ids(conn, ec_id_file):
    '''
    '''

    # drop table "ec_ids" (if it exists)
    xlib.Message.print('verbose', 'Droping the table "ec_ids" ...\n')
    xsqlite.drop_ec_ids(conn)
    xlib.Message.print('verbose', 'The table is droped.\n')

    # create table "ec_ids"
    xlib.Message.print('verbose', 'Creating the table "ec_ids" ...\n')
    xsqlite.create_ec_ids(conn)
    xlib.Message.print('verbose', 'The table is created.\n')

    # open the EC id file
    if ec_id_file.endswith('.gz'):
        try:
            ec_id_file_id = gzip.open(ec_id_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', ec_id_file)
    else:
        try:
            ec_id_file_id = open(ec_id_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', ec_id_file)

    # initialize the record counter
    record_counter = 0

    # initialize the inserted row counter
    inserted_row_counter = 0

    # read the first record
    record = ec_id_file_id.readline()

    # while there are records and they are the header
    while record != '' and not record.startswith('ID'):

        # add 1 to record counter
        record_counter += 1

        # print record counter
        xlib.Message.print('verbose', f'\rProcessed records of EC id file: {record_counter} - Inserted rows: {inserted_row_counter}')

        # read the next record
        record = ec_id_file_id.readline()

    # if there is a first definition block
    if record.startswith('ID'):

        # while there are records and the record is an identification
        while record != '':

            # when the record is an identification
            if record.startswith('ID'):

                # add 1 to record counter
                record_counter += 1

                # initialize the row dictionary
                row_dict = {}
                row_dict['ec_id'] = record[3:].strip()
                row_dict['desc'] = ''

                # print record counter
                xlib.Message.print('verbose', f'\rProcessed records of EC id file: {record_counter} - Inserted rows: {inserted_row_counter}')

                # read the next record
                record = ec_id_file_id.readline()

            # while there are records and the record is a definition
            while record != '' and record.startswith('DE'):

                # add 1 to record counter
                record_counter += 1

                # concat the description
                if row_dict['desc'] == '':
                    row_dict['desc'] = record[3:].strip()
                else:
                    row_dict['desc'] = f'''{row_dict['desc']}, {record[3:].strip()}'''

                # change quotation marks and semicolons in "desc"
                row_dict['desc'] = row_dict['desc'].replace("'", '|').replace(';', ',')

                # print record counter
                xlib.Message.print('verbose', f'\rProcessed records of EC id file: {record_counter} - Inserted rows: {inserted_row_counter}')

                # read the next record
                record = ec_id_file_id.readline()

            # insert data into table "ec_ids"
            row_dict['desc'] = row_dict['desc'][:-1]
            xsqlite.insert_ec_ids_row(conn, row_dict)
            inserted_row_counter += 1

            # while there are records and the record is not an identification and is not a definition
            while record != '' and not record.startswith('ID') and not record.startswith('DE'):

                # add 1 to record counter
                record_counter += 1

                # print record counter
                xlib.Message.print('verbose', f'\rProcessed records of EC id file: {record_counter} - Inserted rows: {inserted_row_counter}')

                # read the next record
                record = ec_id_file_id.readline()

    xlib.Message.print('verbose', '\n')

    # close EC id file
    ec_id_file_id.close()

    # create the index on the table "ec_ids"
    xlib.Message.print('verbose', 'Creating the index on the table "ec_ids" ...\n')
    xsqlite.create_ec_ids_index(conn)
    xlib.Message.print('verbose', 'The index is created.\n')

    # save changes into TOA database
    xlib.Message.print('verbose', 'Saving changes into TOA database ...\n')
    conn.commit()
    xlib.Message.print('verbose', 'Changes are saved.\n')

#-------------------------------------------------------------------------------

def load_table_kegg_ids(conn, kegg_id_file):
    '''
    '''

    # set the pattern of the data records
    # format: kegg_id\tthreshold\tscore_type\tprofile_type\tF-measure\tnseq\tnseq_used\talen\tmlen\teff_nseq\tre/pos\tdefinition
    record_pattern = re.compile(r'^(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)$')
    
    # drop table "kegg_ids"
    xlib.Message.print('verbose', 'Droping the table "kegg_ids" ...\n')
    xsqlite.drop_kegg_ids(conn)
    xlib.Message.print('verbose', 'The table is droped.\n')
    
    # create table "kegg_ids"
    xlib.Message.print('verbose', 'Creating the table "kegg_ids" ...\n')
    xsqlite.create_kegg_ids(conn)
    xlib.Message.print('verbose', 'The table is created.\n')

    # open the file of KEGG ids
    if kegg_id_file.endswith('.gz'):
        try:
            kegg_id_file_id = gzip.open(kegg_id_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', kegg_id_file)
    else:
        try:
            kegg_id_file_id = open(kegg_id_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', kegg_id_file)

    # initialize the record counter
    record_counter = 0

    # initialize the inserted row counter
    inserted_row_counter = 0

    # initialize the header record control
    header_record = True

    # read the first record
    record = kegg_id_file_id.readline()

    # while there are records
    while record != '':

        # add 1 to the record counter
        record_counter += 1

        # process the header record
        if header_record:
            header_record = False

        # process data records
        else:

            # initialize the row data dictionary
            row_dict = {}

            # extract data
            try:
                mo = record_pattern.match(record)
                row_dict['kegg_id'] = mo.group(1).strip().lower()
                # definition format: description [EC:ec_id]
                definition = mo.group(12).strip()
                open_bracket_pos = definition.find('[')
                if open_bracket_pos > -1:
                    row_dict['desc'] = definition[:open_bracket_pos].strip()
                    row_dict['ec_id'] = definition[open_bracket_pos+4:-1].strip()
                else:
                    row_dict['desc'] = definition
                    row_dict['ec_id'] = 'N/A'
            except Exception as e:
                raise xlib.ProgramException('F006', os.path.basename(kegg_id_file), record_counter)

            # change quotation marks and semicolons in "desc"
            row_dict['desc'] = row_dict['desc'].replace("'", '|').replace(';', ',')

            # insert data into table "kegg_ids"
            xsqlite.insert_kegg_ids_row(conn, row_dict)
            inserted_row_counter += 1

        # print record counter
        xlib.Message.print('verbose', f'\rProcessed records of KEGG ids file: {record_counter}  - Inserted rows: {inserted_row_counter}')

        # read the next record
        record = kegg_id_file_id.readline()

    xlib.Message.print('verbose', '\n')
    
    # create the index on the table "kegg_ids"
    xlib.Message.print('verbose', 'Creating the index on the table "kegg_ids" ...\n')
    xsqlite.create_kegg_ids_index(conn)
    xlib.Message.print('verbose', 'The index is created.\n')

    # save changes into TOA database
    xlib.Message.print('verbose', 'Saving changes into TOA database ...\n')
    conn.commit()
    xlib.Message.print('verbose', 'Changes are saved.\n')

    # close kegg_ids file
    kegg_id_file_id.close()

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
