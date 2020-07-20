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
This program loads InterPro data into TOA database.
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

    # load table of mappings of InterPro entries to Gene Ontology terms
    load_table_interpro_interpro2go(conn, args.interpro2go_file)

    # close connection to TOA database
    conn.close()

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program loads InterPro data into TOA database.'
    text = f'{xlib.get_long_project_name()} v{xlib.get_project_version()} - {os.path.basename(__file__)}\n\n{description}\n'
    usage = f'\r{text.ljust(len("usage:"))}\nUsage: {os.path.basename(__file__)} arguments'
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--db', dest='toa_database', help='Path of the TOA database (mandatory).')
    parser.add_argument('--interpro2go', dest='interpro2go_file', help='Path of the interpro2go file (mandatory).')
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

    # check "interpro2go_file"
    if args.interpro2go_file is None:
        xlib.Message.print('error', '*** The interpro2go file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.interpro2go_file):
        xlib.Message.print('error', f'*** The file {args.interpro2go_file} does not exist.')
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

def load_table_interpro_interpro2go(conn, interpro2go_file):
    '''
    '''
    
    # drop table "interpro_interpro2go" (if it exists)
    xlib.Message.print('verbose', 'Droping the table "interpro_interpro2go" ...\n')
    xsqlite.drop_interpro_interpro2go(conn)
    xlib.Message.print('verbose', 'The table is droped.\n')
    
    # create table "interpro_interpro2go"
    xlib.Message.print('verbose', 'Creating the table interpro_interpro2go ...\n')
    xsqlite.create_interpro_interpro2go(conn)
    xlib.Message.print('verbose', 'The table is created.\n')

    # open the file of interpro2go
    if interpro2go_file.endswith('.gz'):
        try:
            interpro2go_file_id = gzip.open(interpro2go_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', interpro2go_file)
    else:
        try:
            interpro2go_file_id = open(interpro2go_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', interpro2go_file)

    # initialize the record counter
    record_counter = 0

    # initialize the inserted row counter
    inserted_row_counter = 0

    # set the pattern of the data records
    # format: InterPro:interpro_id interpro_desc > GO:go_desc ; go_id
    record_pattern = re.compile(r'^InterPro:(.{9}) (.*) > GO:(.*) ; (.{10})$')

    # read the first record
    record = interpro2go_file_id.readline()

    # while there are records
    while record != '':

        # add 1 to record counter
        record_counter += 1

        # if the record is not a comment
        if not record.startswith('!'):

            # initialize the row data dictionary
            row_dict = {}

            # extract data
            try:
                mo = record_pattern.match(record)
                row_dict['interpro_id'] = mo.group(1).strip()
                row_dict['interpro_desc'] = mo.group(2).strip()
                row_dict['go_desc'] = mo.group(3).strip()
                row_dict['go_id'] = mo.group(4).strip()
            except Exception as e:
                raise xlib.ProgramException('F006', os.path.basename(interpro2go_file), record_counter)

            # remove database name from text
            row_dict['go_id'] = row_dict['go_id'].replace('GO:', '')

            # change quotation marks and semicolons in "interpro_desc"
            row_dict['interpro_desc'] = row_dict['interpro_desc'].replace("'", '|').replace(';', ',')

            # change quotation marks and semicolon in "go_desc"
            row_dict['go_desc'] = row_dict['go_desc'].replace("'", '|').replace(';', ',')

            # insert data into table "interpro_interpro2go"
            xsqlite.insert_interpro_interpro2go_row(conn, row_dict)
            inserted_row_counter += 1

        # print record counter
        xlib.Message.print('verbose', f'\rProcessed records of interpro2go file: {record_counter} - Inserted rows: {inserted_row_counter}')

        # read the next record
        record = interpro2go_file_id.readline()

    xlib.Message.print('verbose', '\n')
    
    # create the index 1 on the table "interpro_interpro2go"
    xlib.Message.print('verbose', 'Creating the index 1 on the table "interpro_interpro2go" ...\n')
    xsqlite.create_interpro_interpro2go_index_1(conn)
    xlib.Message.print('verbose', 'The index is created.\n')
    
    # create the index 2 on the table "interpro_interpro2go"
    xlib.Message.print('verbose', 'Creating the index 2 on the table interpro_interpro2go ...\n')
    xsqlite.create_interpro_interpro2go_index_2(conn)
    xlib.Message.print('verbose', 'The index is created.\n')

    # save changes into TOA database
    xlib.Message.print('verbose', 'Saving changes into TOA database ...\n')
    conn.commit()
    xlib.Message.print('verbose', 'Changes are saved.\n')

    # close dataset file
    interpro2go_file_id.close()

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
