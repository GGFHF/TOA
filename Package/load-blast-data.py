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
This program loads BLAST alignment data into TOA database.
'''

#-------------------------------------------------------------------------------

import argparse
import os
import sys
import xml.etree.ElementTree

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
    if not xsqlite.is_dataset_id_found(conn, args.dataset_id):
        raise xlib.ProgramException('L001', args.dataset_id)

    # load table "blast" where the BLAST file format is 5 (BLAST XML)
    if args.blast_file_format == '5':
        load_table_blast_5(conn, args.dataset_id, args.blast_file)

    # close connection to TOA database
    conn.close()

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program loads BLAST alignment data into TOA database.'
    text = '{0} v{1} - {2}\n\n{3}\n'.format(xlib.get_long_project_name(), xlib.get_project_version(), os.path.basename(__file__), description)
    usage = '\r{0}\nUsage: {1} arguments'.format(text.ljust(len('usage:')), os.path.basename(__file__))
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--db', dest='toa_database', help='Path of the TOA database (mandatory).')
    parser.add_argument('--dataset', dest='dataset_id', help='Dataset identification (mandatory).')
    parser.add_argument('--format', dest='blast_file_format', help='Format of the BLAST file (mandatory): {0}.'.format(xlib.get_blast_file_format_code_list_text()))
    parser.add_argument('--blast', dest='blast_file', help='Path of the blastx/blastn file (mandatory).')
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

    # check "blast_file_format"
    if args.blast_file_format is None:
        xlib.Message.print('error', '*** The BLAST file format is not indicated in the input arguments.')
        OK = False
    elif not xlib.check_code(args.blast_file_format, xlib.get_blast_file_format_code_list(), case_sensitive=False):
        xlib.Message.print('error', '*** The BLAST file format has to be {0}.'.format(xlib.get_blast_file_format_code_list_text()))
        OK = False

    # check "blast_file"
    if args.blast_file is None:
        xlib.Message.print('error', '*** The BLAST file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.blast_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.blast_file))
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

def load_table_blast_5(conn, dataset_id, blast_file):
    '''
    '''

    # initialize the iteration counter
    iteration_counter = 0
 
    # initialize the inserted row counter
    inserted_row_counter = 0
   
    # create table "blast"
    xlib.Message.print('verbose', 'Creating the table "blast" (if it does not exist) ...\n')
    xsqlite.create_blast(conn)
    xlib.Message.print('verbose', 'The table is created.\n')
     
    # create the index on the table "blast"
    xlib.Message.print('verbose', 'Creating the index on the table "blast" (if it does not exist) ...\n')
    xsqlite.create_blast_index(conn)
    xlib.Message.print('verbose', 'The index is created.\n')
    
    # delete files from table "blast" corresponding to the repository and dataset identification
    xlib.Message.print('verbose', 'Deleting previous rows from the table "blast" ...\n')
    xsqlite.delete_blast_rows(conn, dataset_id)
    xlib.Message.print('verbose', 'Rows are deleted.\n')

    # build the complee item tree from BLAST XML file
    tree = xml.etree.ElementTree.parse(blast_file)
    root = tree.getroot()
    
    # walk the tree and insert data into table "blast" for each iteration-hit-hsp
    for item_blastoutput_iterations in root.iter(tag= 'BlastOutput_iterations'):
        xlib.Message.print('verbose', '-> tag: {0} - attrib: {1} - text: {2}\n'.format(item_blastoutput_iterations.tag, item_blastoutput_iterations.attrib, item_blastoutput_iterations.text))

        # get items "Iteration"
        for item_iteration in item_blastoutput_iterations.iter(tag= 'Iteration'):
            xlib.Message.print('verbose', '---> tag: {0} - attrib: {1} - text: {2}\n'.format(item_iteration.tag, item_iteration.attrib, item_iteration.text))

            # initialize the row data dictionary
            row_dict = {}
            row_dict['dataset_id'] = dataset_id

            # add 1 to iteration counter
            iteration_counter += 1

            # initialize iteration data
            iteration_iter_num = 0
            iteration_query_def = ''

            # get data of item "Iteration_iter-num"
            for item_iteration_iter_num in item_iteration.iter(tag='Iteration_iter-num'):
                xlib.Message.print('verbose', '-----> tag: {0} - attrib: {1} - text: {2}\n'.format(item_iteration_iter_num.tag, item_iteration_iter_num.attrib, item_iteration_iter_num.text))
                row_dict['iteration_iter_num'] = int(item_iteration_iter_num.text)

            # get data of item "Iteration_query-def"
            for item_iteration_query_def in item_iteration.iter(tag='Iteration_query-def'):
                xlib.Message.print('verbose', '-----> tag: {0} - attrib: {1} - text: {2}\n'.format(item_iteration_query_def.tag, item_iteration_query_def.attrib, item_iteration_query_def.text))
                row_dict['iteration_query_def'] = item_iteration_query_def.text

            # get items "Iteration_hits"
            for item_iteration_hits in item_iteration.iter(tag='Iteration_hits'):
                xlib.Message.print('verbose', '-----> tag: {0} - attrib: {1} - text: {2}\n'.format(item_iteration_hits.tag, item_iteration_hits.attrib, item_iteration_hits.text))

                # get items "Hit"
                for item_hit in item_iteration_hits.iter(tag='Hit'):
                    xlib.Message.print('verbose', '-------> tag: {0} - attrib: {1} - text: {2}'.format(item_hit.tag, item_hit.attrib, item_hit.text))

                    # initialize hit data
                    row_dict['hit_num'] = 0
                    row_dict['hit_id'] = xlib.get_na()
                    row_dict['hit_def'] = xlib.get_na()
                    row_dict['hit_accession'] = xlib.get_na()

                    # get data of item "Hit_num"
                    for item_hit_num in item_hit.iter(tag='Hit_num'):
                        xlib.Message.print('verbose', '---------> tag: {0} - attrib: {1} - text: {2}\n'.format(item_hit_num.tag, item_hit_num.attrib, item_hit_num.text))
                        row_dict['hit_num'] = int(item_hit_num.text)

                    # get data of item "Hit_id"
                    for item_hit_id in item_hit.iter(tag='Hit_id'):
                        xlib.Message.print('verbose', '---------> tag: {0} - attrib: {1} - text: {2}\n'.format(item_hit_id.tag, item_hit_id.attrib, item_hit_id.text))
                        row_dict['hit_id'] = item_hit_id.text

                    # get data of item "Hit_def"
                    for item_hit_def in item_hit.iter(tag='Hit_def'):
                        xlib.Message.print('verbose', '---------> tag: {0} - attrib: {1} - text: {2}\n'.format(item_hit_def.tag, item_hit_def.attrib, item_hit_def.text))
                        row_dict['hit_def'] = item_hit_def.text.replace("'", '|').replace(';', ',')

                    # get data of item "Hit_accession"
                    for item_hit_accession in item_hit.iter(tag='Hit_accession'):
                        xlib.Message.print('verbose', '---------> tag: {0} - attrib: {1} - text: {2}\n'.format(item_hit_accession.tag, item_hit_accession.attrib, item_hit_accession.text))
                        row_dict['hit_accession'] = item_hit_accession.text
                        
                    # get items "Hit_hsps"
                    for item_hit_hsps in item_hit.iter(tag='Hit_hsps'):
                        xlib.Message.print('verbose', '---------> tag: {0} - attrib: {1} - text: {2}\n'.format(item_hit_hsps.tag, item_hit_hsps.attrib, item_hit_hsps.text))
                        
                        # get items "Hsp"
                        for item_hsp in item_hit.iter(tag='Hsp'):
                            xlib.Message.print('verbose', '-----------> tag: {0} - attrib: {1} - text: {2}\n'.format(item_hsp.tag, item_hsp.attrib, item_hsp.text))

                            # initialize hsp data
                            row_dict['hsp_num'] = 0
                            row_dict['hsp_evalue'] = 0.
                            row_dict['hsp_identity'] = 0
                            row_dict['hsp_positive'] = 0
                            row_dict['hsp_gaps'] = 0
                            row_dict['hsp_align_len'] = 0
                            row_dict['hsp_qseq'] = ''

                            # get data of item "Hsp_num"
                            for item_hsp_num in item_hsp.iter(tag='Hsp_num'):
                                xlib.Message.print('verbose', '-------------> tag: {0} - attrib: {1} - text: {2}\n'.format(item_hsp_num.tag, item_hsp_num.attrib, item_hsp_num.text))
                                row_dict['hsp_num'] = int(item_hsp_num.text)

                            # get data of item "Hsp_evalue"
                            for item_hsp_evalue in item_hsp.iter(tag='Hsp_evalue'):
                                xlib.Message.print('verbose', '-------------> tag: {0} - attrib: {1} - text: {2}\n'.format(item_hsp_evalue.tag, item_hsp_evalue.attrib, item_hsp_evalue.text))
                                row_dict['hsp_evalue'] = float(item_hsp_evalue.text)

                            # get data of item "Hsp_identity"
                            for item_hsp_identity in item_hsp.iter(tag='Hsp_identity'):
                                xlib.Message.print('verbose', '-------------> tag: {0} - attrib: {1} - text: {2}\n'.format(item_hsp_identity.tag, item_hsp_identity.attrib, item_hsp_identity.text))
                                row_dict['hsp_identity'] = int(item_hsp_identity.text)

                            # get data of item "Hsp_positive"
                            for item_hsp_positive in item_hsp.iter(tag='Hsp_positive'):
                                xlib.Message.print('verbose', '-------------> tag: {0} - attrib: {1} - text: {2}\n'.format(item_hsp_positive.tag, item_hsp_positive.attrib, item_hsp_positive.text))
                                row_dict['hsp_positive'] = int(item_hsp_positive.text)

                            # get data of item "Hsp_gaps"
                            for item_hsp_gaps in item_hsp.iter(tag='Hsp_gaps'):
                                xlib.Message.print('verbose', '-------------> tag: {0} - attrib: {1} - text: {2}\n'.format(item_hsp_gaps.tag, item_hsp_gaps.attrib, item_hsp_gaps.text))
                                row_dict['hsp_gaps'] = int(item_hsp_gaps.text)

                            # get data of item "Hsp_align-len"
                            for item_hsp_align_len in item_hsp.iter(tag='Hsp_align-len'):
                                xlib.Message.print('verbose', '-------------> tag: {0} - attrib: {1} - text: {2}\n'.format(item_hsp_align_len.tag, item_hsp_align_len.attrib, item_hsp_align_len.text))
                                row_dict['hsp_align_len'] = int(item_hsp_align_len.text)

                            # get data of item "Hsp_qseq"
                            for item_hsp_qseq in item_hsp.iter(tag='Hsp_qseq'):
                                xlib.Message.print('verbose', '-------------> tag: {0} - attrib: {1} - text: {2}\n'.format(item_hsp_qseq.tag, item_hsp_qseq.attrib, item_hsp_qseq.text))
                                row_dict['hsp_qseq'] = item_hsp_qseq.text

                            # insert data into table "blast"
                            xsqlite.insert_blast_row(conn, row_dict)
                            inserted_row_counter += 1

            # print iteration counter
            xlib.Message.print('verbose', '\rIterations: {0} - Inserted rows: {1}'.format(iteration_counter, inserted_row_counter))

    xlib.Message.print('verbose', '\n')

    # save changes into TOA database
    xlib.Message.print('verbose', 'Saving changes into TOA database ...\n')
    conn.commit()
    xlib.Message.print('verbose', 'Changes are saved.\n')

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
