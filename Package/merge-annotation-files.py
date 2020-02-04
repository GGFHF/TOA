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
This program merges two annotation files.
'''

#-------------------------------------------------------------------------------

import argparse
import os
import sys

import xlib

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

    # merge annotation files
    merge_files(args.annotation_file_1, args.type_1, args.annotation_file_2, args.type_2, args.merger_file, args.header)

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'This program merges two annotation files.'
    text = '{0} v{1} - {2}\n\n{3}\n'.format(xlib.get_long_project_name(), xlib.get_project_version(), os.path.basename(__file__), description)
    usage = '\r{0}\nUsage: {1} arguments'.format(text.ljust(len('usage:')), os.path.basename(__file__))
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--file1', dest='annotation_file_1', help='Path of the first annotation file in CSV format (mandatory).')
    parser.add_argument('--type1', dest='type_1', help='Type of the first annotation file (mandatory): {0}.'.format(xlib.get_type_code_list_text()))
    parser.add_argument('--file2', dest='annotation_file_2', help='Path of the second annotation file in CSV format (mandatory).')
    parser.add_argument('--type2', dest='type_2', help='Type of the second annotation file (mandatory): {0}.'.format(xlib.get_type_code_list_text()))
    parser.add_argument('--mfile', dest='merger_file', help='Path of the merged non-annotated transcrip file (mandatory).')
    parser.add_argument('--header', dest='header', help='Insertion of a header record: {0}; default: {1}.'.format(xlib.get_header_code_list_text(), xlib.Const.DEFAULT_HEADER))
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

    # check "annotation_file_1"
    if args.annotation_file_1 is None:
        xlib.Message.print('error', '*** The first annotation file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.annotation_file_1):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.annotation_file_1))
        OK = False

    # check "type_1"
    if args.type_1 is None:
        xlib.Message.print('error', '*** The type of first annotation file is not indicated in the input arguments.')
        OK = False
    elif not xlib.check_code(args.type_1, xlib.get_type_code_list(), case_sensitive=False):
        xlib.Message.print('error', '*** The type of annotation file has to be {0}.'.format(xlib.get_type_code_list_text()))
        OK = False
    else:
        args.type_1 = args.type_1.upper()

    # check "annotation_file_2"
    if args.annotation_file_2 is None:
        xlib.Message.print('error', '*** The second annotation file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.annotation_file_2):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.annotation_file_2))
        OK = False

    # check "type_2"
    if args.type_2 is None:
        xlib.Message.print('error', '*** The format of second annotation file is not indicated in the input arguments.')
        OK = False
    elif not xlib.check_code(args.type_2, xlib.get_type_code_list(), case_sensitive=False):
        xlib.Message.print('error', '*** The type of annotation file has to be {0}.'.format(xlib.get_type_code_list_text()))
        OK = False
    else:
        args.type_2 = args.type_2.upper()

    # check "merger_file"
    if args.merger_file is None:
        xlib.Message.print('error', '*** The merged file is not indicated in the input arguments.')
        OK = False

    # check "header"
    if args.header is None:
        args.header = xlib.Const.DEFAULT_HEADER
    elif not xlib.check_code(args.header, xlib.get_header_code_list(), case_sensitive=False):
        xlib.Message.print('error', '*** header has to be {0}.'.format(xlib.get_header_code_list_text()))
        OK = False
    else:
        args.header = args.header.upper()

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

def merge_files(annotation_file_1, type_1, annotation_file_2, type_2, merger_file, header):
    '''
    '''

    # open the first annotation file
    if annotation_file_1.endswith('.gz'):
        try:
            annotation_file_1_id = gzip.open(annotation_file_1, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', annotation_file_1)
    else:
        try:
            annotation_file_1_id = open(annotation_file_1, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', annotation_file_1)

    # open the second annotation file
    if annotation_file_2.endswith('.gz'):
        try:
            annotation_file_2_id = gzip.open(annotation_file_2, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', annotation_file_2)
    else:
        try:
            annotation_file_2_id = open(annotation_file_2, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', annotation_file_2)

    # open the merged file with non-annotated transcrips
    if merger_file.endswith('.gz'):
        try:
            merger_file_id = gzip.open(merger_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', merger_file)
    else:
        try:
            merger_file_id = open(merger_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', merger_file)

    # initialize record counters
    read_record_counter_1 = 0
    read_record_counter_2 = 0
    written_record_counter = 0
          
    # print header record in merged file with non-annotated transcrips
    if header == 'Y':
        xlib.write_annotation_header(merger_file_id, 'MERGER')

    # read the first record of the first annotation file
    (record_1, key_1, data_dict_1) = xlib.read_annotation_record(annotation_file_1, annotation_file_1_id, type_1, read_record_counter_1)
    xlib.Message.print('trace', 'key_1: {0} - record_1: {1}'.format(key_1 , record_1))

    # read the first record of the second annotation file
    (record_2, key_2, data_dict_2) = xlib.read_annotation_record(annotation_file_2, annotation_file_2_id, type_2, read_record_counter_2)
    xlib.Message.print('trace', 'key_2: {0} - record_2: {1}'.format(key_2 , record_2))

    # while there are records in any annotation file
    while record_1 != '' or record_2 != '':

        # while there are records in the first annotation file and key of the first annotation file is less or equal to the key of the second annotation file
        while record_1 != '' and (record_2 != '' and key_1 <= key_2 or record_2 == ''):

            # add 1 to record counter
            read_record_counter_1 += 1

            # write in the merged annotation file
            xlib.write_merged_annotation_record(merger_file_id, type_1, data_dict_1)
            written_record_counter += 1
            xlib.Message.print('verbose', '\r{0} annotations written'.format(written_record_counter))

            # read the next record of the first annotation file
            (record_1, key_1, data_dict_1) = xlib.read_annotation_record(annotation_file_1, annotation_file_1_id, type_1, read_record_counter_1)
            xlib.Message.print('trace', 'key_1: {0} - record_1: {1}'.format(key_1 , record_1))

        # while there are records in the first annotation file and key of the first annotation file is less or equal to the key of the second annotation file
        while record_2 != '' and (record_1 != '' and key_1 > key_2 or record_1 == ''):

            # add 1 to record counter
            read_record_counter_2 += 1

            # write in the merged annotation file
            xlib.write_merged_annotation_record(merger_file_id, type_2, data_dict_2)
            written_record_counter += 1
            xlib.Message.print('verbose', '\r{0} annotations written'.format(written_record_counter))

            # read the next record of the second annotation file
            (record_2, key_2, data_dict_2) = xlib.read_annotation_record(annotation_file_2, annotation_file_2_id, type_2, read_record_counter_2)
            xlib.Message.print('trace', 'key_2: {0} - record_2: {1}'.format(key_2 , record_2))

    # print summary
    xlib.Message.print('verbose', '\n')
    xlib.Message.print('info', '{0} annotations read in the first annotation file.'.format(read_record_counter_1 - 1))
    xlib.Message.print('info', '{0} annotations read in the second annotation file.'.format(read_record_counter_2 - 1))
    xlib.Message.print('info', '{0} annotations written in the merged annotation file.'.format(written_record_counter))

    # close files
    annotation_file_1_id.close()
    annotation_file_2_id.close()
    merger_file_id.close()

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
