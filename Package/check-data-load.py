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
This program checks the load of a data group into the TOA database.
'''

#-------------------------------------------------------------------------------

import argparse
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

    # initialize the control variable
    OK = True

    # check basic data
    if args.table_group == 'BASIC':
        if xsqlite.check_datasets(conn) == 0 or xsqlite.check_species(conn) == 0:
            OK = False


    # check Gymno PLAZA 1.0
    elif args.table_group == 'gymno_01':
        dataset_id = args.table_group
        if xsqlite.check_plaza_gene_description(conn, dataset_id) == 0 or xsqlite.check_plaza_go(conn, dataset_id) == 0 or xsqlite.check_plaza_interpro(conn, dataset_id) == 0 or xsqlite.check_plaza_mapman(conn, dataset_id) == 0:
            OK = False

    # check Dicots PLAZA 4.0
    elif args.table_group == 'dicots_04':
        dataset_id = args.table_group
        if xsqlite.check_plaza_gene_description(conn, dataset_id) == 0 or xsqlite.check_plaza_go(conn, dataset_id) == 0 or xsqlite.check_plaza_interpro(conn, dataset_id) == 0 or xsqlite.check_plaza_mapman(conn, dataset_id) == 0:
            OK = False

    # check Monocots PLAZA 4.0
    elif args.table_group == 'monocots_04':
        dataset_id = args.table_group
        if xsqlite.check_plaza_gene_description(conn, dataset_id) == 0 or xsqlite.check_plaza_go(conn, dataset_id) == 0 or xsqlite.check_plaza_interpro(conn, dataset_id) == 0 or xsqlite.check_plaza_mapman(conn, dataset_id) == 0:
            OK = False

    # check NCBI Gene
    elif args.table_group == 'gene':
        if xsqlite.check_ncbi_gene2go(conn) == 0 or xsqlite.check_ncbi_gene2refseq(conn) == 0:
            OK = False

    # check InterPro
    elif args.table_group == 'interpro':
        if xsqlite.check_interpro_interpro2go(conn) == 0:
            OK = False

    # check Gene Ontology
    elif args.table_group == 'go':
        if xsqlite.check_go_ontology(conn) == 0 or xsqlite.check_go_cross_references(conn) == 0:
            OK = False

    # close connection to TOA database
    conn.close()

    # check if there are errors
    if OK:
        xlib.Message.print('verbose', f'The table group {args.table_group} has data loaded.\n')
    else:
        xlib.Message.print('verbose', f'The table group {args.table_group} has problems in the data load.\n')
        sys.exit(1)

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program checks the load of a data group into the TOA database.'
    text = f'{xlib.get_long_project_name()} v{xlib.get_project_version()} - {os.path.basename(__file__)}\n\n{description}\n'
    usage = f'\r{text.ljust(len("usage:"))}\nUsage: {os.path.basename(__file__)} arguments'
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--db', dest='toa_database', help='Path of the TOA database (mandatory).')
    parser.add_argument('--group', dest='table_group', help=f'Table group (mandatory): {xlib.get_table_group_code_list_text()}.')
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

    # check "table_group"
    if args.table_group is None:
        xlib.Message.print('error', '*** The table group is not indicated in the input arguments.')
        OK = False
    elif not xlib.check_code(args.table_group, xlib.get_table_group_code_list(), case_sensitive=False):
        xlib.Message.print('error', f'*** The table group has to be {xlib.get_table_group_code_list_text()}.')
        OK = False
    else:
        args.table_group = args.table_group.lower()

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

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
