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
This program splits a annotation file in several files with a certain record number.
'''

#-------------------------------------------------------------------------------

import argparse
import gzip
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

    # split annotation file
    split_files(args.annotation_file, args.type, args.record_number_per_file, args.header)

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program splits a annotation file in several files with a certain record number.'
    text = '{0} v{1} - {2}\n\n{3}\n'.format(xlib.get_long_project_name(), xlib.get_project_version(), os.path.basename(__file__), description)
    usage = '\r{0}\nUsage: {1} arguments'.format(text.ljust(len('usage:')), os.path.basename(__file__))
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--annotation', dest='annotation_file', help='Path of annotation file in CSV format (mandatory).')
    parser.add_argument('--type', dest='type', help='Type of the first annotation file (mandatory): {0}'.format(xlib.get_type_code_list_text()))
    parser.add_argument('--header', dest='header', help='There is a header record in the annotation file: {0}; default: {1}.'.format(xlib.get_header_code_list_text(), xlib.Const.DEFAULT_HEADER))
    parser.add_argument('--rnum', dest='record_number_per_file', help='Record number per splitted file; default: {0}.'.format(xlib.Const.DEFAULT_RNUM))
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

    # check "annotation_file"
    if args.annotation_file is None:
        xlib.Message.print('error', '*** The annotation file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.annotation_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.annotation_file))
        OK = False

    # check "type"
    if args.type is None:
        xlib.Message.print('error', '*** The type of annotation file is not indicated in the input arguments.')
        OK = False
    elif not xlib.check_code(args.type, xlib.get_type_code_list(), case_sensitive=False):
        xlib.Message.print('error', '*** The type of annotation file has to be {0}.'.format(xlib.get_type_code_list_text()))
        OK = False
    else:
        args.type = args.type.upper()

    # check "header"
    if args.header is None:
        args.header = xlib.Const.DEFAULT_HEADER
    elif not xlib.check_code(args.header, xlib.get_header_code_list(), case_sensitive=False):
        xlib.Message.print('error', '*** header has to be {0}.'.format(xlib.get_header_code_list_text()))
        OK = False
    else:
        args.header = args.header.upper()

    # check "record_number_per_file"
    if args.record_number_per_file is None:
        args.record_number_per_file = xlib.Const.DEFAULT_RNUM
    elif not xlib.check_int(args.record_number_per_file, minimum=1):
        xlib.Message.print('error', '*** The record number per splitted file has to be an integer number greater than 0.')
        OK = False
    else:
        args.record_number_per_file = int(args.record_number_per_file)

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

def split_files(annotation_file, type, record_number_per_file, header):
    '''
    '''

    # open the first annotation file
    if annotation_file.endswith('.gz'):
        try:
            annotation_file_id = gzip.open(annotation_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', annotation_file)
    else:
        try:
            annotation_file_id = open(annotation_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', annotation_file)

    # initialize the output file counter
    output_file_counter = 0

    # initialize record counters
    input_record_counter = 0
    output_record_counter = 99999999

    # read the header record
    if header == 'Y':
        annotation_file_id.readline()

    # read the first/second (when header record exists) record of the annotation file
    input_record_counter += 1
    (record, key, data_dict) = xlib.read_annotation_record(annotation_file, annotation_file_id, type, input_record_counter)

    # while there are records in the annotation file
    while record != '':

        # if there are more records written than the maximum record number per file
        if output_record_counter > record_number_per_file:
            
            # if a output_file is opened before
            if output_file_counter > 0:
                
                # close the output_file
                output_file_id.close()

            # add 1 to the counter of output files
            output_file_counter += 1

            # set the output file name
            if annotation_file.endswith('.csv'):
                output_file = '{0}-{1:02d}.csv'.format(annotation_file[:-4], output_file_counter)
            elif annotation_file.endswith('.csv.gz'):
                output_file = '{0}-{1:02d}.csv.gz'.format(annotation_file[:-7], output_file_counter)

            # open the output file
            if output_file.endswith('.gz'):
                try:
                    output_file_id = gzip.open(output_file, mode='wt', encoding='iso-8859-1', newline='\n')
                except Exception as e:
                    raise xlib.ProgramException('F004', output_file)
            else:
                try:
                    output_file_id = open(output_file, mode='w', encoding='iso-8859-1', newline='\n')
                except Exception as e:
                    raise xlib.ProgramException('F003', output_file)
          
            # print header record in the output_file
            xlib.write_annotation_header(output_file_id, type)

            # initialize the output annotation counter
            output_record_counter = 0

        # save the key
        key_old = key

        # while there are records in the annotation file and the transcript identification is same
        while record != '' and key == key_old:

            # write in the output file
            output_record_counter += 1
            xlib.write_annotation_record(output_file_id, type, data_dict)
            xlib.Message.print('verbose', '\r{0} read annotations - {1} annotations written in the file {2}.'.format(input_record_counter, output_record_counter, os.path.basename(output_file)))

            # read the next record of the first annotation file
            input_record_counter += 1
            (record, key, data_dict) = xlib.read_annotation_record(annotation_file, annotation_file_id, type, input_record_counter)

    # print summary
    xlib.Message.print('verbose', '\n')

    # close files
    annotation_file_id.close()
    output_file_id.close()

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
