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
This program loads functional annotation data (gene2refseq y gene2go) from NCBI Gene
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
   
    # check the dataset identification
    if args.dataset_id != 'gene':
        raise xlib.ProgramException('L001', 'dataset', args.dataset_id)

    # load table "gene2refseq_file"
    load_table_ncbi_gene2refseq_file(conn, args.dataset_id, args.gene2refseq_file)

    # load table "ncbi_gene2go"
    load_table_ncbi_gene2go(conn, args.dataset_id, args.gene2go_file)

    # close connection to TOA database
    conn.close()

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program loads functional annotation data (gene2refseq y gene2go) from NCBI Gene into TOA database.'
    text = '{0} v{1} - {2}\n\n{3}\n'.format(xlib.get_long_project_name(), xlib.get_project_version(), os.path.basename(__file__), description)
    usage = '\r{0}\nUsage: {1} arguments'.format(text.ljust(len('usage:')), os.path.basename(__file__))
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--db', dest='toa_database', help='Path of the TOA database (mandatory).')
    parser.add_argument('--dataset', dest='dataset_id', help='Type: NCBI dataset identification (mandatory).')
    parser.add_argument('--gene2refseq', dest='gene2refseq_file', help='Path of the gene2refseq file (mandatory).')
    parser.add_argument('--gene2go', dest='gene2go_file', help='Path of the gene2go file (mandatory).')
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

    # check "dataset_id"
    if args.dataset_id is None:
        xlib.Message.print('error', '*** The dataset identification is not indicated in the input arguments.')
        OK = False
    else:
        args.dataset_id = args.dataset_id.lower()

    # check "gene2refseq_file"
    if args.gene2refseq_file is None:
        xlib.Message.print('error', '*** The file gene2refseq is not indicated in the options.')
        OK = False
    elif not os.path.isfile(args.gene2refseq_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.gene2refseq_file))
        OK = False

    # check "gene2go_file"
    if args.gene2go_file is None:
        xlib.Message.print('error', '*** The file gene2go is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.gene2go_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.gene2go_file))
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

def load_table_ncbi_gene2refseq_file(conn, dataset_id, gene2refseq_file):
    '''
    '''

    # initialize the record counter
    record_counter = 0

    # initialize the inserted row counter
    inserted_row_counter = 0

    # initialize the header record control
    header_record = True
    
    # drop table "ncbi_gene2refseq" (if it exists)
    xlib.Message.print('verbose', 'Droping the table "ncbi_gene2refseq" ...\n')
    xsqlite.drop_ncbi_gene2refseq(conn)
    xlib.Message.print('verbose', 'The table is droped.\n')

    # create table "ncbi_gene2refseq"
    xlib.Message.print('verbose', 'Creating the table "ncbi_gene2refseq" ...\n')
    xsqlite.create_ncbi_gene2refseq(conn)
    xlib.Message.print('verbose', 'The table is created.\n')

    # open the gene2refseq file
    if gene2refseq_file.endswith('.gz'):
        try:
            gene2refseq_file_id = gzip.open(gene2refseq_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', gene2refseq_file)
    else:
        try:
            gene2refseq_file_id = open(gene2refseq_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', gene2refseq_file)

    # read the first record
    record = gene2refseq_file_id.readline()

    # while there are records
    while record != '':

        # add 1 to record counter
        record_counter += 1

        # process the header record 
        if header_record:
            header_record = False

        # process data records
        else:

            # initialize the row data dictionary
            row_dict = {}

            # extract data 
            # record format: tax_id\tGeneID\tstatus\tRNA_nucleotide_accession.version\tRNA_nucleotide_gi\tprotein_accession.version\tprotein_gi\tgenomic_nucleotide_accession.version\tgenomic_nucleotide_gi\tstart_position_on_the_genomic_accession\tend_position_on_the_genomic_accession\torientation\tassembly\tmature_peptide_accession.version\tmature_peptide_gi\tSymbol
            data_list = []
            begin = 0
            for end in [i for i, chr in enumerate(record) if chr == '\t']:
                data_list.append(record[begin:end].strip())
                begin = end + 1
            data_list.append(record[begin:].strip('\n').strip())
            try:
                row_dict['gene_id'] = data_list[1]
                row_dict['status'] = data_list[2]
                row_dict['rna_nucleotide_accession'] = data_list[3]
                row_dict['protein_accession'] = data_list[5]
                row_dict['genomic_nucleotide_accession'] = data_list[7]
                row_dict['gene_symbol'] = data_list[15]
            except Exception as e:
                raise xlib.ProgramException('F006', os.path.basename(gene2refseq_file), record_counter)

            # check "gene_id"
            try:
                row_dict['gene_id'] = int(row_dict['gene_id'])
            except Exception as e:
                raise xlib.ProgramException('D001', 'GeneID', os.path.basename(gene2refseq_file), record_counter)

            # change quotation marks in "gene_symbol"
            row_dict['gene_symbol'] = row_dict['gene_symbol'].replace("'", '|')

            # insert data into table "ncbi_gene2refseq"
            xsqlite.insert_ncbi_gene2refseq_row(conn, row_dict)
            inserted_row_counter += 1

            # print counters
            xlib.Message.print('verbose', '\rgene2refseq file: {0} processed records - Inserted rows: {1}'.format(record_counter, inserted_row_counter))

        # read the next record
        record = gene2refseq_file_id.readline()

    xlib.Message.print('verbose', '\n')

    # create the index on the table "ncbi_gene2refseq"
    xlib.Message.print('verbose', 'Creating index on the table "ncbi_gene2refseq" ...\n')
    xsqlite.create_ncbi_gene2refseq_index(conn)
    xlib.Message.print('verbose', 'The index is created.\n')

    # save changes into TOA database
    xlib.Message.print('verbose', 'Saving changes into TOA database ...\n')
    conn.commit()
    xlib.Message.print('verbose', 'Changes are saved.\n')

    # close gene2refseq file
    gene2refseq_file_id.close()

#-------------------------------------------------------------------------------

def load_table_ncbi_gene2go(conn, dataset_id, gene2go_file):
    '''
    '''
    
    # drop table "ncbi_gene2go" (if it exists)
    xlib.Message.print('verbose', 'Droping the table "ncbi_gene2go" ...\n')
    xsqlite.drop_ncbi_gene2go(conn)
    xlib.Message.print('verbose', 'The table is droped.\n')

    # create table "ncbi_gene2go"
    xlib.Message.print('verbose', 'Creating the table "ncbi_gene2go" ...\n')
    xsqlite.create_ncbi_gene2go(conn)
    xlib.Message.print('verbose', 'The table is created.\n')

    # initialize the record counter
    record_counter = 0

    # initialize the inserted row counter
    inserted_row_counter = 0

    # initialize the header record control
    header_record = True

    # open the gene2go file
    if gene2go_file.endswith('.gz'):
        try:
            gene2go_file_id = gzip.open(gene2go_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', gene2go_file)
    else:
        try:
            gene2go_file_id = open(gene2go_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', gene2go_file)

    # read the first record
    record = gene2go_file_id.readline()

    # while there are records
    while record != '':

        # add 1 to record counter
        record_counter += 1

        # initialize the row data dictionary
        row_dict = {}

        # process the header record 
        if header_record:
            header_record = False

        # process data records
        else:

            # extract data 
            # record format: tax_id\tGeneID\tGO_ID\tEvidence\tQualifier\tGO_term\tPubMed\tCategory
            data_list = []
            begin = 0
            for end in [i for i, chr in enumerate(record) if chr == '\t']:
                data_list.append(record[begin:end].strip())
                begin = end + 1
            data_list.append(record[begin:].strip('\n').strip())
            try:
                row_dict['gene_id'] = data_list[1]
                row_dict['go_id'] = data_list[2]
                row_dict['evidence'] = data_list[3]
                row_dict['go_term'] = data_list[5]
                row_dict['category'] = data_list[7]
            except Exception as e:
                raise xlib.ProgramException('F006', os.path.basename(gene2go_file), record_counter)

            # check "gene_id"
            try:
                row_dict['gene_id'] = int(row_dict['gene_id'])
            except Exception as e:
                raise xlib.ProgramException('D001', 'GeneID', os.path.basename(gene2go_file), record_counter)

            # remove database name from text
            row_dict['go_id'] = row_dict['go_id'].replace('GO:', '')

            # change quotation marks and semicolons in "go_term"
            row_dict['go_term'] = row_dict['go_term'].replace("'", '|').replace(';', ',')

            # insert data into table "ncbi_gene2go"
            xsqlite.insert_ncbi_gene2go_row(conn, row_dict)
            inserted_row_counter += 1

            # print counters
            xlib.Message.print('verbose', '\rgene2go file: {0} processed records - Inserted rows: {1}'.format(record_counter, inserted_row_counter))

        # read the next record
        record = gene2go_file_id.readline()

    xlib.Message.print('verbose', '\n')

    # create the index on the table "ncbi_gene2go"
    xlib.Message.print('verbose', 'Creating the index on the table "ncbi_gene2go" ...\n')
    xsqlite.create_ncbi_gene2go_index(conn)
    xlib.Message.print('verbose', 'The index is created.\n')

    # save changes into TOA database
    xlib.Message.print('verbose', 'Saving changes into TOA database ...\n')
    conn.commit()
    xlib.Message.print('verbose', 'Changes are saved.\n')

    # close gene2go file
    gene2go_file_id.close()

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
