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
This program loads cross-references between Gene Ontology and other databases
into TOA database.
'''

#-------------------------------------------------------------------------------

import argparse
import gzip
import os
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

    # load table "go_ontology"
    load_table_go_ontology(conn, args.ontology_file)

    # load table "go_cross_references"
    load_table_go_cross_references(conn, args.ec2go_file, args.kegg2go_file, args.metacyc2go_file, args.interpro2go_file)

    # close connection to TOA database
    conn.close()

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program loads cross-references between Gene Ontology and other databases into TOA database.'
    text = '{0} v{1} - {2}\n\n{3}\n'.format(xlib.get_long_project_name(), xlib.get_project_version(), os.path.basename(__file__), description)
    usage = '\r{0}\nUsage: {1} arguments'.format(text.ljust(len('usage:')), os.path.basename(__file__))
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--db', dest='toa_database', help='Path of the TOA database (mandatory).')
    parser.add_argument('--ontology', dest='ontology_file', help='Path of the ontology file (mandatory).')
    parser.add_argument('--ec2go', dest='ec2go_file', help='Path of the ec2go file (mandatory).')
    parser.add_argument('--kegg2go', dest='kegg2go_file', help='Path of the gene2go file (mandatory).')
    parser.add_argument('--metacyc2go', dest='metacyc2go_file', help='Path of the metacyc2go file (mandatory).')
    parser.add_argument('--interpro2go', dest='interpro2go_file', help='Path of the interpro2go file (mandatory).')
    parser.add_argument('--verbose', dest='verbose', help='Additional job status info during the run: {0}; default: {1}.'.format(xlib.get_verbose_code_list_text(), xlib.Const.DEFAULT_VERBOSE))
    parser.add_argument('--trace', dest='trace', help='Additional info useful to the developer team: {0}; default: {1}.'.format(xlib.get_trace_code_list_text(), xlib.Const.DEFAULT_TRACE))

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

    # check "ontology_file"
    if args.ontology_file is None:
        xlib.Message.print('error', '*** The ontology file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.ontology_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.ontology_file))
        OK = False

    # check "ec2go_file"
    if args.ec2go_file is None:
        xlib.Message.print('error', '*** The ec2go file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.ec2go_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.ec2go_file))
        OK = False

    # check "kegg2go_file"
    if args.kegg2go_file is None:
        xlib.Message.print('error', '*** The kegg2go file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.kegg2go_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.kegg2go_file))
        OK = False

    # check "metacyc2go_file"
    if args.metacyc2go_file is None:
        xlib.Message.print('error', '*** The metacyc2go file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.metacyc2go_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.metacyc2go_file))
        OK = False

    # check "interpro2go_file"
    if args.interpro2go_file is None:
        xlib.Message.print('error', '*** The interpro2go file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.interpro2go_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.interpro2go_file))
        OK = False

    # check "verbose"
    if args.verbose is None:
        args.verbose = xlib.Const.DEFAULT_VERBOSE
    elif not xlib.check_code(args.verbose, xlib.get_verbose_code_list(), case_sensitive=False):
        xlib.Message.print('error', '*** verbose has to be {0}.'.format(xlib.get_verbose_code_list_text()))
        OK = False
    if args.verbose.upper() == 'Y':
        xlib.Message.set_verbose_status(True)

    # check "trace"
    if args.trace is None:
        args.trace = xlib.Const.DEFAULT_TRACE
    elif not xlib.check_code(args.trace, xlib.get_trace_code_list(), case_sensitive=False):
        xlib.Message.print('error', '*** trace has to be {0}.'.format(xlib.get_trace_code_list_text()))
        OK = False
    if args.trace.upper() == 'Y':
        xlib.Message.set_trace_status(True)

    # if there are errors, exit with exception
    if not OK:
        raise xlib.ProgramException('P001')

#-------------------------------------------------------------------------------

def load_table_go_ontology(conn, ontology_file):
    '''
    '''

    # drop table "go_ontology" (if it exists)
    xlib.Message.print('verbose', 'Droping the table "go_ontology" ...\n')
    xsqlite.drop_go_ontology(conn)
    xlib.Message.print('verbose', 'The table is droped.\n')

    # create table "go_ontology"
    xlib.Message.print('verbose', 'Creating the table "go_ontology" ...\n')
    xsqlite.create_go_ontology(conn)
    xlib.Message.print('verbose', 'The table is created.\n')

    # initialize the row data dictionary and the external database name and description
    row_dict = {}
    row_dict['external_db'] = 'ec'
    row_dict['external_desc'] = xlib.get_na()

    # open the ontology file
    if ontology_file.endswith('.gz'):
        try:
            ontology_file_id = gzip.open(ontology_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', ontology_file)
    else:
        try:
            ontology_file_id = open(ontology_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', ontology_file)

    # initialize the record counter
    record_counter = 0

    # initialize the inserted row counter
    inserted_row_counter = 0

    # read the first record
    record = ontology_file_id.readline()

    # while there are records and they are the header
    while record != '' and not record.startswith('[Term]'):

        # add 1 to record counter
        record_counter += 1

        # print record counter
        xlib.Message.print('verbose', '\rOntology file: {0} processed records - Inserted rows: {1}'.format(record_counter, inserted_row_counter))

        # read the next record
        record = ontology_file_id.readline()

    # if there is a first term block
    if record.startswith('[Term]'):

        # while there are records
        while record != '':

            # add 1 to record counter
            record_counter += 1

            # print record counter
            xlib.Message.print('verbose', '\rOntology file: {0} processed records - Inserted rows: {1}'.format(record_counter, inserted_row_counter))

            # read the next record
            record = ontology_file_id.readline()

            # initialize the row dictionary
            row_dict = {}
            row_dict['go_id'] = ''
            row_dict['go_name'] = ''
            row_dict['namespace'] = ''

            # while there are records and they are term details
            while record != '' and not record.startswith('[Term]'):

                # add 1 to record counter
                record_counter += 1

                # get the GO identification
                if record.startswith('id:'):
                    start = record.find('GO:')
                    row_dict['go_id'] = record[start+3:].strip()

                # get the GO name
                if record.startswith('name:'):
                    start = record.find('name:')
                    row_dict['go_name'] = record[start+5:].strip()

                    # change quotation marks and semicolons in "go_name"
                    row_dict['go_name'] = row_dict['go_name'].replace("'", '|').replace(';', ',')

                # get the namespace
                if record.startswith('namespace:'):
                    start = record.find('namespace:')
                    row_dict['namespace'] = record[start+10:].strip()

                    # change quotation marks and semicolons in "namespace"
                    row_dict['namespace'] = row_dict['namespace'].replace("'", '|').replace(';', ',').replace('_', ' ')

                # print record counter
                xlib.Message.print('verbose', '\rOntology file: {0} processed records - Inserted rows: {1}'.format(record_counter, inserted_row_counter))

                # read the next record
                record = ontology_file_id.readline()

                # break the loop when typedef sections start
                if record.startswith('[Typedef]'):
                    break

            # insert data into table "go_ontology"
            xsqlite.insert_go_ontology_row(conn, row_dict)
            inserted_row_counter += 1

            # print record counter
            xlib.Message.print('verbose', '\rOntology file: {0} processed records - Inserted rows: {1}'.format(record_counter, inserted_row_counter))

            # break the loop when typedef sections start
            if record.startswith('[Typedef]'):
                break

    xlib.Message.print('verbose', '\n')

    # close ontology file
    ontology_file_id.close()

    # create the index on the table "go_ontology"
    xlib.Message.print('verbose', 'Creating the index on the table "go_ontology" ...\n')
    xsqlite.create_go_ontology_index(conn)
    xlib.Message.print('verbose', 'The index is created.\n')

    # save changes into TOA database
    xlib.Message.print('verbose', 'Saving changes into TOA database ...\n')
    conn.commit()
    xlib.Message.print('verbose', 'Changes are saved.\n')

#-------------------------------------------------------------------------------

def load_table_go_cross_references(conn, ec2go_file, kegg2go_file, metacyc2go_file, interpro2go_file):
    '''
    '''
    
    # drop table "go_cross_references" (if it exists)
    xlib.Message.print('verbose', 'Droping the table "go_cross_references" ...\n')
    xsqlite.drop_go_cross_references(conn)
    xlib.Message.print('verbose', 'The table is droped.\n')

    # create table "go_cross_references"
    xlib.Message.print('verbose', 'Creating the table "go_cross_references" ...\n')
    xsqlite.create_go_cross_references(conn)
    xlib.Message.print('verbose', 'The table is created.\n')

    # initialize the row data dictionary and the external database name and description
    row_dict = {}
    row_dict['external_db'] = 'ec'
    row_dict['external_desc'] = xlib.get_na()

    # open the ec2go file
    if ec2go_file.endswith('.gz'):
        try:
            ec2go_file_id = gzip.open(ec2go_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', ec2go_file)
    else:
        try:
            ec2go_file_id = open(ec2go_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', ec2go_file)

    # initialize the record counter
    record_counter = 0

    # initialize the inserted row counter
    inserted_row_counter = 0

    # read the first record
    record = ec2go_file_id.readline()

    # while there are records
    while record != '':

        # add 1 to record counter
        record_counter += 1

        # process data records
        if not record.startswith('!'):

            # extract data 
            # record format: ec_id > go_term ; go_id
            gt_position = record.find('>')
            semicolon_position = record.find(';')
            if gt_position == -1 or semicolon_position == -1 or gt_position > semicolon_position:
                raise xlib.ProgramException('F006', os.path.basename(ec2go_file), record_counter)
            row_dict['external_id'] = record[:gt_position].strip()
            row_dict['go_term'] = record[gt_position + 1:semicolon_position].strip()
            row_dict['go_id'] = record[semicolon_position + 1:].strip('\n').strip()

            # remove database name from text
            row_dict['go_id'] = row_dict['go_id'].replace('GO:', '')
            row_dict['go_term'] = row_dict['go_term'].replace('GO:', '')
            row_dict['external_id'] = row_dict['external_id'].replace('EC:', '')

            # change quotation marks and semicolons in "go_term"
            row_dict['go_term'] = row_dict['go_term'].replace("'", '|').replace(';', ',')

            # insert data into table "go_cross_references"
            xsqlite.insert_go_cross_references_row(conn, row_dict)
            inserted_row_counter += 1

            # print record counter
            xlib.Message.print('verbose', '\rec2go file: {0} processed records - Inserted rows: {1}'.format(record_counter, inserted_row_counter))

        # read the next record
        record = ec2go_file_id.readline()

    xlib.Message.print('verbose', '\n')

    # close ec2go file
    ec2go_file_id.close()

    # initialize the row data dictionary and the external database name and description
    row_dict = {}
    row_dict['external_db'] = 'kegg'
    row_dict['external_desc'] = xlib.get_na()

    # open the kegg2go file
    if kegg2go_file.endswith('.gz'):
        try:
            kegg2go_file_id = gzip.open(kegg2go_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', kegg2go_file)
    else:
        try:
            kegg2go_file_id = open(kegg2go_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', kegg2go_file)

    # initialize the record counter
    record_counter = 0

    # initialize the inserted row counter
    inserted_row_counter = 0

    # read the first record
    record = kegg2go_file_id.readline()

    # while there are records
    while record != '':

        # add 1 to record counter
        record_counter += 1

        # process data records
        if not record.startswith('!'):

            # extract data 
            # record format: kegg_id > go_term ; go_id
            gt_position = record.find('>')
            semicolon_position = record.find(';')
            if gt_position == -1 or semicolon_position == -1 or gt_position > semicolon_position:
                raise xlib.ProgramException('F006', os.path.basename(kegg2go_file), record_counter)
            row_dict['external_id'] = record[:gt_position].strip()
            row_dict['go_term'] = record[gt_position + 1:semicolon_position].strip()
            row_dict['go_id'] = record[semicolon_position + 1:].strip('\n').strip()

            # remove database name from text
            row_dict['go_id'] = row_dict['go_id'].replace('GO:', '')
            row_dict['go_term'] = row_dict['go_term'].replace('GO:', '')
            row_dict['external_id'] = row_dict['external_id'].replace('KEGG:', '')

            # change quotation marks and semicolons in "go_term"
            row_dict['go_term'] = row_dict['go_term'].replace("'", '|').replace(';', ',')

            # insert data into table "go_cross_references"
            xsqlite.insert_go_cross_references_row(conn, row_dict)
            inserted_row_counter += 1

            # print record counter
            xlib.Message.print('verbose', '\rkegg2go file: {0} processed records - Inserted rows: {1}'.format(record_counter, inserted_row_counter))

        # read the next record
        record = kegg2go_file_id.readline()

    xlib.Message.print('verbose', '\n')

    # close kegg2go file
    kegg2go_file_id.close()

    # initialize the row data dictionary and the external database name and description
    row_dict = {}
    row_dict['external_db'] = 'metacyc'
    row_dict['external_desc'] = xlib.get_na()

    # open the metacyc2go file
    if metacyc2go_file.endswith('.gz'):
        try:
            metacyc2go_file_id = gzip.open(metacyc2go_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', metacyc2go_file)
    else:
        try:
            metacyc2go_file_id = open(metacyc2go_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', metacyc2go_file)

    # initialize the record counter
    record_counter = 0

    # initialize the inserted row counter
    inserted_row_counter = 0

    # read the first record
    record = metacyc2go_file_id.readline()

    # while there are records
    while record != '':

        # add 1 to record counter
        record_counter += 1

        # process data records
        if not record.startswith('!'):

            # extract data 
            # record format: metacyc_id > go_term ; go_id
            gt_position = record.find('>')
            semicolon_position = record.find(';')
            if gt_position == -1 or semicolon_position == -1 or gt_position > semicolon_position:
                raise xlib.ProgramException('F006', os.path.basename(metacyc2go_file), record_counter)
            row_dict['external_id'] = record[:gt_position].strip()
            row_dict['go_term'] = record[gt_position + 1:semicolon_position].strip()
            row_dict['go_id'] = record[semicolon_position + 1:].strip('\n').strip()

            # remove database name from text
            row_dict['go_id'] = row_dict['go_id'].replace('GO:', '')
            row_dict['go_term'] = row_dict['go_term'].replace('GO:', '')
            row_dict['external_id'] = row_dict['external_id'].replace('MetaCyc:', '')

            # change quotation marks and semicolons in "go_term"
            row_dict['go_term'] = row_dict['go_term'].replace("'", '|').replace(';', ',')

            # insert data into table "go_cross_references"
            xsqlite.insert_go_cross_references_row(conn, row_dict)
            inserted_row_counter += 1

            # print record counter
            xlib.Message.print('verbose', '\rmetacyc2go file: {0} processed records - Inserted rows: {1}'.format(record_counter, inserted_row_counter))

        # read the next record
        record = metacyc2go_file_id.readline()

    xlib.Message.print('verbose', '\n')

    # close metacyc2go file
    metacyc2go_file_id.close()

    # initialize the row data dictionary and the external database name
    row_dict = {}
    row_dict['external_db'] = 'interpro'

    # open the interpro file
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

    # read the first record
    record = interpro2go_file_id.readline()

    # while there are records
    while record != '':

        # add 1 to record counter
        record_counter += 1

        # process data records
        if not record.startswith('!'):

            # extract data 
            # record format: interpro_id interpro_desc > go_term ; go_id
            first_space_position = record.find(' ')
            gt_position = record.find('>')
            semicolon_position = record.find(';')
            if first_space_position == -1 or gt_position == -1 or semicolon_position == -1 or first_space_position > gt_position or gt_position > semicolon_position:
                raise xlib.ProgramException('F006', os.path.basename(interpro2go_file), record_counter)
            row_dict['external_id'] = record[:first_space_position].strip()
            row_dict['external_desc'] = record[first_space_position + 1:gt_position].strip()
            row_dict['go_term'] = record[gt_position + 1:semicolon_position].strip()
            row_dict['go_id'] = record[semicolon_position + 1:].strip('\n').strip()

            # remove database name from text
            row_dict['go_id'] = row_dict['go_id'].replace('GO:', '')
            row_dict['go_term'] = row_dict['go_term'].replace('GO:', '')
            row_dict['external_id'] = row_dict['external_id'].replace('InterPro:', '')

            # change quotation marks and semicolons in "go_term" and "external_desc"
            row_dict['go_term'] = row_dict['go_term'].replace("'", '|').replace(';', ',')
            row_dict['external_desc'] = row_dict['external_desc'].replace("'", '|').replace(';', ',')

            # insert data into table "go_cross_references"
            xsqlite.insert_go_cross_references_row(conn, row_dict)
            inserted_row_counter += 1

            # print record counter
            xlib.Message.print('verbose', '\rinterpro2go file: {0} processed records - Inserted rows: {1}'.format(record_counter, inserted_row_counter))

        # read the next record
        record = interpro2go_file_id.readline()

    xlib.Message.print('verbose', '\n')

    # close interpro2go file
    interpro2go_file_id.close()

    # create the index on the table "go_cross_references"
    xlib.Message.print('verbose', 'Creating the index on the table "go_cross_references" ...\n')
    xsqlite.create_go_cross_references_index(conn)
    xlib.Message.print('verbose', 'The index is created.\n')

    # save changes into TOA database
    xlib.Message.print('verbose', 'Saving changes into TOA database ...\n')
    conn.commit()
    xlib.Message.print('verbose', 'Changes are saved.\n')

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
