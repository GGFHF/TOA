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
This program loads genomic features into TOA database from a species from a GFF file.
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

    # get the taxonomy dictionary of the species name from taxonomy server
    taxonomy_dict = xlib.get_taxonomy_dict('name', args.species_name)
    if taxonomy_dict == {}:
        raise xlib.ProgramException('L006', args.dataset_id)


    # load genomic features depending of format of the genomic feature file
    load_genomic_features(conn, args.species_name, args.gff_file, args.gff_format)

    # close connection to TOA database
    conn.close()

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program loads genomic features into TOA database from a species from a GFF file.'
    text = f'{xlib.get_long_project_name()} v{xlib.get_project_version()} - {os.path.basename(__file__)}\n\n{description}\n'
    usage = f'\r{text.ljust(len("usage:"))}\nUsage: {os.path.basename(__file__)} arguments'
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--db', dest='toa_database', help='Path of the TOA database (mandatory).')
    parser.add_argument('--species', dest='species_name', help='The scientific name of the species using underscore as separator, e.g. Quercus_suber (mandatory).')
    parser.add_argument('--gff', dest='gff_file', help='Path of the GFF file (mandatory).')
    parser.add_argument('--format', dest='gff_format', help='The format of the GFF file: GFF3; default: GFF3.')
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

    # check "species_name"
    if args.species_name is None:
        xlib.Message.print('error', '*** The scientific name of the species is not indicated in the input arguments.')
        OK = False

    # check "gff_file"
    if args.gff_file is None:
        args.gff_file = 'GFF3'
    elif not os.path.isfile(args.gff_file):
        xlib.Message.print('error', f'*** The file {args.gff_file} does not exist.')
        OK = False

    # check "gff_format"
    if args.gff_file is None:
        xlib.Message.print('error', '*** The format of the GFF file is not indicated in the input arguments.')
        OK = False
    elif args.gff_format.upper() != 'GFF3':
        xlib.Message.print('error', '*** The format of the GFF file has to be GFF3.')
        OK = False
    else:
        args.gff_format = args.gff_format.upper()

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

def load_genomic_features(conn, species_name, gff_file, gff_format):
    '''
    '''

    # create table "genomic_features" (if not exists)
    xlib.Message.print('verbose', 'Creating the table "genomic_features" (if it does not exist) ...\n')
    xsqlite.create_genomic_features(conn)
    xlib.Message.print('verbose', 'The table is created.\n')
     
    # create index "genomic_features_index" with columns "dataset_id" and "gene_id"  (if not exists)
    xlib.Message.print('verbose', 'Creating the index on the table "genomic_features" (if it does not exist) ...\n')
    xsqlite.create_genomic_features_index(conn)
    xlib.Message.print('verbose', 'The index is created.\n')
    
    # delete files from table "genomic_features" corresponding to the dataset and species identifications
    xlib.Message.print('verbose', 'Deleting previous rows from the table "genomic_features" ...\n')
    xsqlite.delete_genomic_features_rows(conn, species_name)
    xlib.Message.print('verbose', 'Rows are deleted.\n')

    # open the GFF file
    if gff_file.endswith('.gz'):
        try:
            gff_file_id = gzip.open(gff_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', gff_file)
    else:
        try:
            gff_file_id = open(gff_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', gff_file)

    # initialize the record counter
    record_counter = 0

    # initialize the inserted row counter
    inserted_row_counter = 0

    # initialize the first header record control
    first_header_record = True

    # read the first record
    record = gff_file_id.readline()

    # while there are records
    while record != '':

        # add 1 to record counter
        record_counter += 1

        # process the header records
        if record.startswith('#'):
            if first_header_record == True and gff_format == 'GFF3':
                if not record.startswith('##gff-version 3'):
                    raise xlib.ProgramException('F005', os.path.basename(gff_file), 'GFF3')
            first_header_record = False

        # process data records
        else:

            # initialize the row data dictionary
            row_dict = {}
            row_dict['species_name'] = species_name

            # extract data
            # record format: seqid\tsource\ttype\tstart\tend\tscore\tstrand\tphase\tattributes
            data_list = []
            pos_1 = 0
            for pos_2 in [i for i, chr in enumerate(record) if chr == '\t']:
                data_list.append(record[pos_1:pos_2].strip())
                pos_1 = pos_2 + 1
            data_list.append(record[pos_1:].strip('\n').strip())
            try:
                row_dict['seq_id'] = data_list[0]
                row_dict['type'] = data_list[2]
                row_dict['start'] = data_list[3]
                row_dict['end'] = data_list[4]
                attributes = data_list[8]
            except Exception as e:
                raise xlib.ProgramException('F006', os.path.basename(gff_file), record_counter)

            # only the types "gene", "CDS" and "mRNA" have to be inserted in the table "genomic_features"
            if row_dict['type'] in ['gene', 'CDS', 'mRNA']:

                # check "start"
                try:
                    row_dict['start'] = int(row_dict['start'])
                except Exception as e:
                    raise xlib.ProgramException('D001', 'start', os.path.basename(gff_file), record_counter)

                # check "end"
                try:
                    row_dict['end'] = int(row_dict['end'])
                except Exception as e:
                    raise xlib.ProgramException('D001', 'stop', os.path.basename(gff_file), record_counter)

                # get "gene_id" data from "attributes"
                row_dict['gene_id'] = xlib.get_na()
                literal = 'GeneID:'
                pos_1 = attributes.find(literal)
                if pos_1 > -1:
                    pos_comma = attributes.find(',', pos_1 + len(literal) + 1)
                    pos_semicolon = attributes.find(';', pos_1 + len(literal) + 1)
                    if pos_comma == -1:
                        pos_2 = pos_semicolon
                    elif pos_semicolon == -1:
                        pos_2 = pos_comma
                    else:
                        pos_2 = min(pos_comma, pos_semicolon)
                    row_dict['gene_id'] = attributes[pos_1 + len(literal):pos_2]

                # get "genbank_id" data from "attributes"
                row_dict['genbank_id'] = xlib.get_na()
                literal = 'Genbank:'
                pos_1 = attributes.find(literal)
                if pos_1 > -1:
                    pos_comma = attributes.find(',', pos_1 + len(literal) + 1)
                    pos_semicolon = attributes.find(';', pos_1 + len(literal) + 1)
                    if pos_comma == -1:
                        pos_2 = pos_semicolon
                    elif pos_semicolon == -1:
                        pos_2 = pos_comma
                    else:
                        pos_2 = min(pos_comma, pos_semicolon)
                    row_dict['genbank_id'] = attributes[pos_1 + len(literal):pos_2]

                # get "gene" data from "attributes"
                row_dict['gene'] = xlib.get_na()
                literal = 'gene='
                pos_1 = attributes.find(literal)
                if pos_1 > -1:
                    pos_2 = attributes.find(';', pos_1 + len(literal) + 1)
                    row_dict['gene'] = attributes[pos_1 + len(literal):pos_2]

                # get "protein_id" data from "attributes"
                row_dict['protein_id'] = xlib.get_na()
                literal = 'protein_id='
                pos_1 = attributes.find(literal)
                if pos_1 > -1:
                    pos_2 = attributes.find(';', pos_1 + len(literal) + 1)
                    if pos_2 > -1:
                        row_dict['protein_id'] = attributes[pos_1 + len(literal):pos_2]
                    else:
                        row_dict['protein_id'] = attributes[pos_1 + len(literal):]

                # get "transcript_id" data from "attributes"
                row_dict['transcript_id'] = xlib.get_na()
                literal = 'transcript_id='
                pos_1 = attributes.find(literal)
                if pos_1 > -1:
                    pos_2 = attributes.find(';', pos_1 + len(literal) + 1)
                    if pos_2 > -1:
                        row_dict['transcript_id'] = attributes[pos_1 + len(literal):pos_2]
                    else:
                        row_dict['transcript_id'] = attributes[pos_1 + len(literal):]

                # get "product" data from "attributes"
                row_dict['product'] = xlib.get_na()
                literal = 'product='
                pos_1 = attributes.find(literal)
                if pos_1 > -1:
                    pos_2 = attributes.find(';', pos_1 + len(literal) + 1)
                    row_dict['product'] = attributes[pos_1 + len(literal):pos_2]

                # change quotation marks, semicolons and %2C in "product"
                row_dict['product'] = row_dict['product'].replace("'", '|').replace(';', ',').replace('%2C', ',')

                # insert data into table "genomic_features"
                xsqlite.insert_genomic_features_row(conn, row_dict)
                inserted_row_counter += 1

        # print record counter
        xlib.Message.print('verbose', f'\rProcessed records of GFF file: {record_counter} - Inserted rows: {inserted_row_counter}')

        # read the next record
        record = gff_file_id.readline()

    xlib.Message.print('verbose', '\n')

    # save changes into TOA database
    xlib.Message.print('verbose', 'Saving changes into TOA database ...\n')
    conn.commit()
    xlib.Message.print('verbose', 'Changes are saved.\n')

    # close GFF file
    gff_file_id.close()

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
