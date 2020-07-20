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
This program loads functional annotation data (Gene Ontology and Interpro) from
PLAZA into TOA database.
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

    # get the PLAZA dataset identification list
    plaza_dataset_id_list = xsqlite.get_plaza_dataset_id_list(conn)
   
    # check the dataset identification
    if args.dataset_id not in plaza_dataset_id_list:
        raise xlib.ProgramException('L001', 'dataset', args.dataset_id)

    # get the PLAZA species identification list
    plaza_species_id_list = xsqlite.get_plaza_species_id_list(conn)

    # check the PLAZA species identification
    if args.species_id != 'all' and args.species_id not in plaza_species_id_list:
        raise xlib.ProgramException('L003', args.species_id)

    # load table "plaza_gene_description"
    load_table_plaza_gene_description(conn, args.dataset_id, args.species_id, args.gene_desc_dir, plaza_species_id_list)

    # load table "plaza_interpro"
    load_table_plaza_interpro(conn, args.dataset_id, args.species_id, args.interpro_file, plaza_species_id_list)

    # load table "plaza_go"
    load_table_plaza_go(conn, args.dataset_id, args.species_id, args.go_file, plaza_species_id_list)

    # load table "plaza_mapman"
    load_table_plaza_mapman(conn, args.dataset_id, args.species_id, args.mapman_file, plaza_species_id_list)

    # close connection to TOA database
    conn.close()

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program loads functional annotation data (Gene Ontology and Interpro) from PLAZA into TOA database.'
    text = f'{xlib.get_long_project_name()} v{xlib.get_project_version()} - {os.path.basename(__file__)}\n\n{description}\n'
    usage = f'\r{text.ljust(len("usage:"))}\nUsage: {os.path.basename(__file__)} arguments'
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--db', dest='toa_database', help='Path of the TOA database (mandatory).')
    parser.add_argument('--dataset', dest='dataset_id', help='Type: PLAZA dataset identification (mandatory).')
    parser.add_argument('--species', dest='species_id', help='PLAZA species identification or all if all species (mandatory).')
    parser.add_argument('--genedesc', dest='gene_desc_dir', help='Path of the gene description file directoty (mandatory).')
    parser.add_argument('--interpro', dest='interpro_file', help='Path of the InterPro file (mandatory).')
    parser.add_argument('--go', dest='go_file', help='Path of the Gene Ontology file (mandatory).')
    parser.add_argument('--mapman', dest='mapman_file', help='Path of the Mapman file (mandatory).')
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

    # check "dataset_id"
    if args.dataset_id is None:
        xlib.Message.print('error', '*** The dataset identification is not indicated in the input arguments.')
        OK = False
    else:
        args.dataset_id = args.dataset_id.lower()

    # check "species_id"
    if args.species_id is None:
        xlib.Message.print('error', '*** The species identification is not indicated in the input arguments.')
        OK = False
    else:
        args.species_id = args.species_id.lower()

    # check "gene_desc_dir"
    if args.gene_desc_dir is None:
        xlib.Message.print('error', '*** The gene description file directoty is not indicated in the input arguments.')
        OK = False
    elif not os.path.isdir(args.gene_desc_dir):
        xlib.Message.print('error', f'*** The directory {args.gene_desc_dir} does not exist.')
        OK = False

    # check "interpro_file"
    if args.interpro_file is None:
        xlib.Message.print('error', '*** The InterPro file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.interpro_file):
        xlib.Message.print('error', f'*** The file {args.interpro_file} does not exist.')
        OK = False

    # check "go_file"
    if args.go_file is None:
        xlib.Message.print('error', '*** The Gene Ontology file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.go_file):
        xlib.Message.print('error', f'*** The file {args.go_file} does not exist.')
        OK = False

    # check "mapman_file"
    if args.mapman_file is None:
        xlib.Message.print('error', '*** The MapMan file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.mapman_file):
        xlib.Message.print('error', f'*** The file {args.mapman_file} does not exist.')
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

def load_table_plaza_gene_description(conn, dataset_id, species_id, gene_desc_dir, plaza_species_id_list):
    '''
    '''

    # create table "plaza_gene_description" (if not exists)
    xlib.Message.print('verbose', 'Creating the table "plaza_gene_description" (if it does not exist) ...\n')
    xsqlite.create_plaza_gene_description(conn)
    xlib.Message.print('verbose', 'The table is created.\n')
     
    # create index "plaza_gene_description_index" with columns "dataset_id" and "gene_id"  (if not exists)
    xlib.Message.print('verbose', 'Creating the index on the table "plaza_gene_description" (if it does not exist) ...\n')
    xsqlite.create_plaza_gene_description_index(conn)
    xlib.Message.print('verbose', 'The index is created.\n')
    
    # delete files from table "plaza_gene_description" corresponding to the dataset and species identifications
    xlib.Message.print('verbose', 'Deleting previous rows from the table "plaza_gene_description" ...\n')
    xsqlite.delete_plaza_gene_description_rows(conn, dataset_id, species_id)
    xlib.Message.print('verbose', 'Rows are deleted.\n')

    # get the gene description file list
    if species_id != 'all':
        gene_desc_file_list = ['gene_description.{}.csv.gz'.format(species_id)]
    else:
        gene_desc_file_list = os.listdir(gene_desc_dir)

    # for each file in the gene description file list
    for gene_desc_file in gene_desc_file_list:

        # get the species identifiation
        literal = 'gene_description.'
        literal_len = len(literal)
        pos1 = gene_desc_file.find(literal)
        if pos1 >= 0:
            pos2 = gene_desc_file[literal_len + 1:].find('.')
            plaza_species_id = gene_desc_file[literal_len + pos1:literal_len + pos1 + pos2 + 1].strip()
            if plaza_species_id not in plaza_species_id_list:
                raise xlib.ProgramException('L004', plaza_species_id, gene_desc_file)
        else:
            raise xlib.ProgramException('L005', gene_desc_file)

        # concat the directory to the name of the gene description file 
        gene_desc_file = f'{gene_desc_dir}/{gene_desc_file}'

        # open the gene description file
        if gene_desc_file.endswith('.gz'):
            try:
                gene_desc_file_id = gzip.open(gene_desc_file, mode='rt', encoding='iso-8859-1')
            except Exception as e:
                raise xlib.ProgramException('F002', gene_desc_file)
        else:
            try:
                gene_desc_file_id = open(gene_desc_file, mode='r', encoding='iso-8859-1')
            except Exception as e:
                raise xlib.ProgramException('F001', gene_desc_file)

        # initialize the record counter
        record_counter = 0

        # initialize the inserted row counter
        inserted_row_counter = 0

        # initialize the header record control
        header_record = True

        # read the first record
        record = gene_desc_file_id.readline()

        # while there are records
        while record != '':

            # add 1 to record counter
            record_counter += 1

            # process the header record for Gymno PLAZA 1.0
            if dataset_id in ['gymno_01'] and header_record:
                header_record = False

            # process data records
            else:

                # initialize the row data dictionary
                row_dict = {}
                row_dict['dataset_id'] = dataset_id
                row_dict['plaza_species_id'] = plaza_species_id

                # extract data Gymno PLAZA 1.0
                if dataset_id in ['gymno_01']:
                    # record format: "gene_id";"id_type";"id"
                    data_list = []
                    begin = 0
                    for end in [i for i, chr in enumerate(record) if chr == ';']:
                        data_list.append(record[begin:end].strip('"'))
                        begin = end + 1
                    data_list.append(record[begin:].strip('\n').strip('"'))
                    try:
                        row_dict['gene_id'] = data_list[0]
                        row_dict['desc_type'] = data_list[1]
                        row_dict['desc'] = data_list[2]
                    except Exception as e:
                        raise xlib.ProgramException('F006', os.path.basename(gene_desc_file), record_counter)

                # extract data Dicots PLAZA 4.0 and Monocots PLAZA 4.0 (for non-comment records)
                elif not record.startswith('#') and dataset_id in ['dicots_04', 'monocots_04']:
                    # record format: gene_id\tid_type\tid
                    data_list = []
                    start = 0
                    for end in [i for i, chr in enumerate(record) if chr == '\t']:
                        data_list.append(record[start:end].strip())
                        start = end + 1
                    data_list.append(record[start:].strip('\n').strip())
                    try:
                        row_dict['gene_id'] = data_list[0]
                        row_dict['desc_type'] = data_list[1]
                        row_dict['desc'] = data_list[2]
                    except Exception as e:
                        raise xlib.ProgramException('F006', os.path.basename(gene_desc_file), record_counter)

                # if PLAZA species identification has value not null (for non-comment records)
                if not record.startswith('#'):

                    # change quotation marks and semicolons in "desc"
                    row_dict['desc'] = row_dict['desc'].replace("'", '|').replace(';', ',')

                    # insert data into table "plaza_gene_description"
                    xsqlite.insert_plaza_gene_description_row(conn, row_dict)
                    inserted_row_counter += 1

                # print record counter
                xlib.Message.print('verbose', f'\rProcessed records of {os.path.basename(gene_desc_file)}: {record_counter} - Inserted rows: {inserted_row_counter}')

            # read the next record
            record = gene_desc_file_id.readline()

        xlib.Message.print('verbose', '\n')

        # close gene description file
        gene_desc_file_id.close()

    # save changes into TOA database
    xlib.Message.print('verbose', 'Saving changes into TOA database ...\n')
    conn.commit()
    xlib.Message.print('verbose', 'Changes are saved.\n')

#-------------------------------------------------------------------------------

def load_table_plaza_interpro(conn, dataset_id, species_id, interpro_file, plaza_species_id_list):
    '''
    '''

    # create table "plaza_interpro" (if not exists)
    xlib.Message.print('verbose', 'Creating the table "plaza_interpro" (if it does not exist) ...\n')
    xsqlite.create_plaza_interpro(conn)
    xlib.Message.print('verbose', 'The table is created.\n')
     
    # create index "plaza_interpro_index" with columns "dataset_id" and "gene_id"  (if not exists)
    xlib.Message.print('verbose', 'Creating the index on the table "plaza_interpro" (if it does not exist) ...\n')
    xsqlite.create_plaza_interpro_index(conn)
    xlib.Message.print('verbose', 'The index is created.\n')
    
    # delete files from table "plaza_interpro" corresponding to the dataset and species identifications
    xlib.Message.print('verbose', 'Deleting previous rows from the table "plaza_interpro" ...\n')
    xsqlite.delete_plaza_interpro_rows(conn, dataset_id, species_id)
    xlib.Message.print('verbose', 'Rows are deleted.\n')

    # open the InterPro file
    if interpro_file.endswith('.gz'):
        try:
            interpro_file_id = gzip.open(interpro_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', interpro_file)
    else:
        try:
            interpro_file_id = open(interpro_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', interpro_file)

    # initialize the record counter
    record_counter = 0

    # initialize the inserted row counter
    inserted_row_counter = 0

    # initialize the header record control
    header_record = True

    # read the first record
    record = interpro_file_id.readline()

    # while there are records
    while record != '':

        # add 1 to record counter
        record_counter += 1

        # process the header record for Gymno PLAZA 1.0
        if dataset_id in ['gymno_01'] and header_record:
            header_record = False

        # process data records
        else:

            # initialize the row data dictionary
            row_dict = {}
            row_dict['dataset_id'] = dataset_id

            # extract data Gymno PLAZA 1.0
            if dataset_id in ['gymno_01']:
                # record format: "id";"motif_id";"species";"gene_id";"start";"stop";"score";"comment";"desc"
                data_list = []
                begin = 0
                for end in [i for i, chr in enumerate(record) if chr == ';']:
                    data_list.append(record[begin:end].strip('"'))
                    begin = end + 1
                data_list.append(record[begin:].strip('\n').strip('"'))
                try:
                    row_dict['id'] = data_list[0]
                    row_dict['motif_id'] = data_list[1]
                    row_dict['plaza_species_id'] = data_list[2]
                    row_dict['gene_id'] = data_list[3]
                    row_dict['start'] = data_list[4]
                    row_dict['stop'] = data_list[5]
                    row_dict['score'] = data_list[6]
                    comment = data_list[7]
                    row_dict['desc'] = data_list[8]
                except Exception as e:
                    raise xlib.ProgramException('F006', os.path.basename(interpro_file), record_counter)

            # extract data Dicots PLAZA 4.0 and Monocots PLAZA 4.0 (for non-comment records)
            elif not record.startswith('#') and dataset_id in ['dicots_04', 'monocots_04']:
                # record format: gene_id\tspecies\tmotif_id\tdescription\tstart\tstop\tscore\tcomment
                data_list = []
                start = 0
                for end in [i for i, chr in enumerate(record) if chr == '\t']:
                    data_list.append(record[start:end].strip())
                    start = end + 1
                data_list.append(record[start:].strip('\n').strip())
                try:
                    row_dict['gene_id'] = data_list[0]
                    row_dict['plaza_species_id'] = data_list[1]
                    row_dict['motif_id'] = data_list[2]
                    row_dict['desc'] = data_list[3]
                    row_dict['start'] = data_list[4]
                    row_dict['stop'] = data_list[5]
                    row_dict['score'] = data_list[6]
                    comment = data_list[7]
                    row_dict['id'] = 0
                except Exception as e:
                    raise xlib.ProgramException('F006', os.path.basename(interpro_file), record_counter)

            # if PLAZA species identification has value not null (for non-comment records)
            if not record.startswith('#') and row_dict['plaza_species_id'] != '':

                # check plaza_species_id
                if row_dict['plaza_species_id'] not in plaza_species_id_list:
                    raise xlib.ProgramException('L002', 'species', os.path.basename(interpro_file), record_counter)

                # check "start"
                try:
                    row_dict['start'] = int(row_dict['start'])
                except Exception as e:
                    raise xlib.ProgramException('D001', 'start', os.path.basename(interpro_file), record_counter)

                # check "end"
                try:
                    row_dict['stop'] = int(row_dict['stop'])
                except Exception as e:
                    raise xlib.ProgramException('D001', 'stop', os.path.basename(interpro_file), record_counter)

                # check "score"
                try:
                    row_dict['score'] = float(row_dict['score'])
                except Exception as e:
                    raise xlib.ProgramException('D002', 'score', os.path.basename(interpro_file), record_counter)

                # split "comment" in "source" and "domain_id"
                # "comment" format: source=x,domainId=x
                pos1 = comment.find('source=')
                if pos1 >= 0:
                    pos2 = comment.find(',domainId=')
                    row_dict['source'] = comment[pos1+7:pos2].strip()
                    row_dict['domain_id'] = comment[pos2+10:].strip()
                else:
                    row_dict['source'] = xlib.get_na()
                    row_dict['domain_id'] = xlib.get_na()

                # change quotation marks and semicolons in "desc"
                row_dict['desc'] = row_dict['desc'].replace("'", '|').replace(';', ',')

                # insert data into table "plaza_interpro"
                xsqlite.insert_plaza_interpro_row(conn, row_dict)
                inserted_row_counter += 1

            # print record counter
            xlib.Message.print('verbose', f'\rProcessed records of InterPro file: {record_counter} - Inserted rows: {inserted_row_counter}')

        # read the next record
        record = interpro_file_id.readline()

    xlib.Message.print('verbose', '\n')

    # save changes into TOA database
    xlib.Message.print('verbose', 'Saving changes into TOA database ...\n')
    conn.commit()
    xlib.Message.print('verbose', 'Changes are saved.\n')

    # close InterPro file
    interpro_file_id.close()

#-------------------------------------------------------------------------------

def load_table_plaza_go(conn, dataset_id, species_id, go_file, plaza_species_id_list):
    '''
    '''
    
    # create table "plaza_go"
    xlib.Message.print('verbose', 'Creating the table "plaza_go" (if it does not exist) ...\n')
    xsqlite.create_plaza_go(conn)
    xlib.Message.print('verbose', 'The table is created.\n')
    
    # create the index on table "plaza_go"
    xlib.Message.print('verbose', 'Creating the index on the table "plaza_go" (if it does not exist) ...\n')
    xsqlite.create_plaza_go_index(conn)
    xlib.Message.print('verbose', 'The index is created.\n')
   
    # delete files from table "plaza_go" corresponding to the dataset and species identifications
    xlib.Message.print('verbose', 'Deleting previous rows from the table "plaza_go" ...\n')
    xsqlite.delete_plaza_go_rows(conn, dataset_id, species_id)
    xlib.Message.print('verbose', 'Rows are deleted.\n')

    # open the Gene Ontology file
    if go_file.endswith('.gz'):
        try:
            go_file_id = gzip.open(go_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', go_file)
    else:
        try:
            go_file_id = open(go_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', go_file)

    # initialize the record counter
    record_counter = 0

    # initialize the inserted row counter
    inserted_row_counter = 0

    # initialize the header record control
    header_record = True

    # read the first record
    record = go_file_id.readline()

    # while there are records
    while record != '':

        # add 1 to record counter
        record_counter += 1

        # process the header record for Gymno PLAZA 1.0
        if dataset_id in ['gymno_01'] and header_record:
            header_record = False

        # process other records
        else:

            # initialize the row data dictionary
            row_dict = {}
            row_dict['dataset_id'] = dataset_id

            # extract data Gymno PLAZA 1.0
            if dataset_id in ['gymno_01']:

                # record format: "id";"species";"gene_id";"go";"evidence";"go_source";"provider";"comment";"is_shown";"desc"
                pos_list = [i for i, chr in enumerate(record) if chr == '"']
                try:
                    row_dict['id'] = record[pos_list[0]+1:pos_list[1]].strip()
                    row_dict['plaza_species_id'] = record[pos_list[2]+1:pos_list[3]].strip()
                    row_dict['gene_id'] = record[pos_list[4]+1:pos_list[5]].strip()
                    row_dict['go_id'] = record[pos_list[6]+1:pos_list[7]].strip()
                    row_dict['evidence'] = record[pos_list[8]+1:pos_list[9]].strip()
                    row_dict['desc'] = record[pos_list[18]+1:pos_list[19]].strip()
                except Exception as e:
                    raise xlib.ProgramException('F006', os.path.basename(go_file), record_counter)

            # extract data Dicots PLAZA 4.0 and Monocots PLAZA 4.0 (for non-comment records)
            elif not record.startswith('#') and dataset_id in ['dicots_04', 'monocots_04']:

                # record format: gene_id\tspecies\tgo\tevidence\tdescription\tgo_source\tprovider\tcomment
                # warning: there may be double quote in "comment"
                data_list = []
                begin = 0
                for end in [i for i, chr in enumerate(record) if chr == '\t']:
                    data_list.append(record[begin:end].strip())
                    begin = end + 1
                data_list.append(record[begin:].strip('\n').strip())
                try:
                    row_dict['gene_id'] = data_list[0]
                    row_dict['plaza_species_id'] = data_list[1]
                    row_dict['go_id'] = data_list[2]
                    row_dict['evidence'] = data_list[3]
                    row_dict['desc'] = data_list[4]
                    row_dict['id'] = 0
                except Exception as e:
                    raise xlib.ProgramException('F006', os.path.basename(go_file), record_counter)

            # if PLAZA species identification has value not null (for non-comment records)
            if not record.startswith('#') and row_dict['plaza_species_id'] != '':

                # check "plaza_species_id"
                if row_dict['plaza_species_id'] not in plaza_species_id_list:
                    xlib.Message.print('trace', f'\nrecord: {record}')
                    print('plaza_species_id: {}'.format(row_dict['plaza_species_id']))
                    raise xlib.ProgramException('L002', 'species', os.path.basename(go_file), record_counter)

                # remove database name from text
                row_dict['go_id'] = row_dict['go_id'].replace('GO:', '')

                # change quotation marks and semicolos in "desc"
                row_dict['desc'] = row_dict['desc'].replace("'", '|').replace(';', ',')

                # insert data into table "plaza_go"
                xsqlite.insert_plaza_go_row(conn, row_dict)
                inserted_row_counter += 1

            # print record counter
            xlib.Message.print('verbose', f'\rProcessed records of Gene Ontology file: {record_counter} - Inserted rows: {inserted_row_counter}')

        # read the next record
        record = go_file_id.readline()

    xlib.Message.print('verbose', '\n')

    # save changes into TOA database
    xlib.Message.print('verbose', 'Saving changes into TOA database ...\n')
    conn.commit()
    xlib.Message.print('verbose', 'Changes are saved.\n')

    # close Gene Ontology file
    go_file_id.close()

#-------------------------------------------------------------------------------

def load_table_plaza_mapman(conn, dataset_id, species_id, mapman_file, plaza_species_id_list):
    '''
    '''
    
    # create table "plaza_mapman"
    xlib.Message.print('verbose', 'Creating the table "plaza_mapman" (if it does not exist) ...\n')
    xsqlite.create_plaza_mapman(conn)
    xlib.Message.print('verbose', 'The table is created.\n')
    
    # create the index on table "plaza_mapman"
    xlib.Message.print('verbose', 'Creating the index on the table "plaza_mapman" (if it does not exist) ...\n')
    xsqlite.create_plaza_mapman_index(conn)
    xlib.Message.print('verbose', 'The index is created.\n')
   
    # delete files from table "plaza_mapman" corresponding to the dataset and species identifications
    xlib.Message.print('verbose', 'Deleting previous rows from the table "plaza_mapman" ...\n')
    xsqlite.delete_plaza_mapman_rows(conn, dataset_id, species_id)
    xlib.Message.print('verbose', 'Rows are deleted.\n')

    # open the Gene Ontology file
    if mapman_file.endswith('.gz'):
        try:
            mapman_file_id = gzip.open(mapman_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', mapman_file)
    else:
        try:
            mapman_file_id = open(mapman_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', mapman_file)

    # initialize the record counter
    record_counter = 0

    # initialize the inserted row counter
    inserted_row_counter = 0

    # initialize the header record control
    header_record = True

    # read the first record
    record = mapman_file_id.readline()

    # while there are records
    while record != '':

        # add 1 to record counter
        record_counter += 1

        # process the header record for Gymno PLAZA 1.0
        if dataset_id in ['gymno_01'] and header_record:
            header_record = False

        # process other records
        else:

            # initialize the row data dictionary
            row_dict = {}
            row_dict['dataset_id'] = dataset_id

            # extract data Gymno PLAZA 1.0
            if dataset_id in ['gymno_01']:

                # record format: "species";"gene_id";"mapman";"evidence";"desc"
                pos_list = [i for i, chr in enumerate(record) if chr == '"']
                try:
                    row_dict['plaza_species_id'] = record[pos_list[0]+1:pos_list[1]].strip()
                    row_dict['gene_id'] = record[pos_list[2]+1:pos_list[3]].strip()
                    row_dict['mapman_id'] = record[pos_list[4]+1:pos_list[5]].strip()
                    row_dict['desc'] = record[pos_list[6]+1:pos_list[7]].strip()
                except Exception as e:
                    raise xlib.ProgramException('F006', os.path.basename(mapman_file), record_counter)

            # extract data Dicots PLAZA 4.0 and Monocots PLAZA 4.0 (for non-comment records)
            elif not record.startswith('#') and dataset_id in ['dicots_04', 'monocots_04']:

                # the record format is unknown
                pass

            # if PLAZA species identification has value not null (for non-comment records)
            if not record.startswith('#') and row_dict['plaza_species_id'] != '':

                # check "plaza_species_id"
                if row_dict['plaza_species_id'] not in plaza_species_id_list:
                    xlib.Message.print('trace', f'\nrecord: {record}')
                    print('plaza_species_id: {}'.format(row_dict['plaza_species_id']))
                    raise xlib.ProgramException('L002', 'species', os.path.basename(mapman_file), record_counter)

                # change quotation marks and semicolos in "desc"
                row_dict['desc'] = row_dict['desc'].replace("'", '|').replace(';', ',')

                # insert data into table "plaza_mapman"
                xsqlite.insert_plaza_mapman_row(conn, row_dict)
                inserted_row_counter += 1

            # print record counter
            xlib.Message.print('verbose', f'\rProcessed records of Mapman file: {record_counter} - Inserted rows: {inserted_row_counter}')

        # read the next record
        record = mapman_file_id.readline()

    xlib.Message.print('verbose', '\n')

    # save changes into TOA database
    xlib.Message.print('verbose', 'Saving changes into TOA database ...\n')
    conn.commit()
    xlib.Message.print('verbose', 'Changes are saved.\n')

    # close Gene Ontology file
    mapman_file_id.close()

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
