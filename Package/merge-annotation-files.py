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

    # merge annotation files with operation "1AND2" (annotations included in both files)
    if args.merger_operation ==  '1AND2':
        merge_files_operation_1and2(args.annotation_file_1, args.type_1, args.annotation_file_2, args.type_2, args.merger_file, args.header)
    # merge annotation files with operation "1BEST" (all annotations of the first file and annotations if the second file if their seq id is not in the first)
    elif args.merger_operation ==  '1BEST':
        merge_files_operation_1best(args.annotation_file_1, args.type_1, args.annotation_file_2, args.type_2, args.merger_file, args.header)
    # save a annotation file with record format "PLAZA", "REFSEQ", "NT" or "NR" in record format "MERGER"
    elif args.merger_operation ==  'SAVE1':
        save_annotation_file_merger_format(args.annotation_file_1, args.type_1, args.merger_file, args.header)

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'This program merges two annotation files.'
    text = f'{xlib.get_long_project_name()} v{xlib.get_project_version()} - {os.path.basename(__file__)}\n\n{description}\n'
    usage = f'\r{text.ljust(len("usage:"))}\nUsage: {os.path.basename(__file__)} arguments'
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--file1', dest='annotation_file_1', help='Path of the first annotation file in CSV format (mandatory).')
    parser.add_argument('--type1', dest='type_1', help=f'Type of the first annotation file (mandatory): {xlib.get_type_code_list_text()}.')
    parser.add_argument('--file2', dest='annotation_file_2', help='Path of the second annotation file in CSV format or NONE if operation is "SAVE1" (mandatory).')
    parser.add_argument('--type2', dest='type_2', help=f'Type of the second annotation file (mandatory): {xlib.get_type_code_list_text()} or NONE if operation is "SAVE1".')
    parser.add_argument('--mfile', dest='merger_file', help='Path of the merged non-annotated transcrip file (mandatory).')
    parser.add_argument('--operation', dest='merger_operation', help=f'Merger operation (mandatory): {xlib.get_annotation_merger_operation_code_list_text()}.')
    parser.add_argument('--header', dest='header', help=f'Insertion of a header record: {xlib.get_header_code_list_text()}; default: {xlib.Const.DEFAULT_HEADER}.')
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

    # check "annotation_file_1"
    if args.annotation_file_1 is None:
        xlib.Message.print('error', '*** The first annotation file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.annotation_file_1):
        xlib.Message.print('error', f'*** The file {args.annotation_file_1} does not exist.')
        OK = False

    # check "type_1"
    if args.type_1 is None:
        xlib.Message.print('error', '*** The type of first annotation file is not indicated in the input arguments.')
        OK = False
    elif not xlib.check_code(args.type_1, xlib.get_type_code_list(), case_sensitive=False):
        xlib.Message.print('error', f'*** The type of annotation file has to be {xlib.get_type_code_list_text()}.')
        OK = False
    else:
        args.type_1 = args.type_1.upper()

    # check "annotation_file_2"
    if args.annotation_file_2 is None:
        xlib.Message.print('error', '*** The second annotation file is not indicated in the input arguments.')
        OK = False
    elif args.annotation_file_2.upper() == 'NONE':
        args.annotation_file_2 = args.annotation_file_2.upper()
    elif not os.path.isfile(args.annotation_file_2):
        xlib.Message.print('error', f'*** The file {args.annotation_file_2} does not exist.')
        OK = False

    # check "type_2"
    if args.type_2 is None:
        xlib.Message.print('error', '*** The format of second annotation file is not indicated in the input arguments.')
        OK = False
    elif args.type_2.upper() == 'NONE' and args.annotation_file_2 != 'NONE':
        xlib.Message.print('error', '*** The format of second annotation file has to be NONE if the second annotation file is NONE')
        OK = False
    elif args.type_2.upper() == 'NONE' and args.annotation_file_2 == 'NONE':
        args.type_2 = args.type_2.upper()
    elif not xlib.check_code(args.type_2, xlib.get_type_code_list(), case_sensitive=False):
        xlib.Message.print('error', f'*** The type of annotation file has to be {xlib.get_type_code_list_text()}.')
        OK = False
    else:
        args.type_2 = args.type_2.upper()

    # check "merger_file"
    if args.merger_file is None:
        xlib.Message.print('error', '*** The merged file is not indicated in the input arguments.')
        OK = False

    # check "merger_operation"
    if args.merger_operation is None:
        xlib.Message.print('error', '*** The merger operation is not indicated in the input arguments.')
        OK = False
    elif args.merger_operation.upper() == 'SAVE1' and args.annotation_file_2 != 'NONE':
        xlib.Message.print('error', '*** The merger operation SAVE1 is only valid when the second annotation file is NONE.')
        OK = False
    elif args.merger_operation.upper() != 'SAVE1' and not xlib.check_code(args.merger_operation, xlib.get_annotation_merger_operation_code_list(), case_sensitive=False) :
        xlib.Message.print('error', f'*** The merger operation has to be {xlib.get_annotation_merger_operation_code_list_text()}.')
        OK = False
    else:
        args.merger_operation = args.merger_operation.upper()

    # check "header"
    if args.header is None:
        args.header = xlib.Const.DEFAULT_HEADER
    elif not xlib.check_code(args.header, xlib.get_header_code_list(), case_sensitive=False):
        xlib.Message.print('error', f'*** header has to be {xlib.get_header_code_list_text()}.')
        OK = False
    else:
        args.header = args.header.upper()

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

def merge_files_operation_1and2(annotation_file_1, type_1, annotation_file_2, type_2, merger_file, header):
    '''
    Merge annotation files with operation "1AND2" (annotations included in both files).
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

    # open the merged annotation file
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

    # print header record in merged file if necessary
    if header == 'Y':
        xlib.write_annotation_header(merger_file_id, 'MERGER')
        written_record_counter += 1

    # read the first record of the first annotation file
    (record_1, key_1, data_dict_1) = xlib.read_annotation_record(annotation_file_1, annotation_file_1_id, type_1, read_record_counter_1)
    xlib.Message.print('trace', f'key_1: {key_1} - record_1: {record_1}')

    # read the first record of the second annotation file
    (record_2, key_2, data_dict_2) = xlib.read_annotation_record(annotation_file_2, annotation_file_2_id, type_2, read_record_counter_2)
    xlib.Message.print('trace', f'key_2: {key_2} - record_2: {record_2}')

    # while there are records in any annotation file
    while record_1 != '' or record_2 != '':

        # while there are records in the first annotation file and key of the first annotation file is less then the key of the second annotation file
        while record_1 != '' and (record_2 != '' and key_1 < key_2 or record_2 == ''):

            # add 1 to record counter
            read_record_counter_1 += 1

            # write in the merged annotation file
            xlib.write_merged_annotation_record(merger_file_id, type_1, data_dict_1)
            written_record_counter += 1
            xlib.Message.print('verbose', f'\rWritten annotations: {written_record_counter}')

            # read the next record of the first annotation file
            (record_1, key_1, data_dict_1) = xlib.read_annotation_record(annotation_file_1, annotation_file_1_id, type_1, read_record_counter_1)
            xlib.Message.print('trace', f'key_1: {key_1} - record_1: {record_1}')

        # while there are records in both annotation files and key of the first annotation file is equal to the key of the second annotation file
        while record_1 != '' and record_2 != '' and key_1 == key_2:

            # add 1 to record counter
            read_record_counter_1 += 1

            # write the first file record in the merged annotation file
            xlib.write_merged_annotation_record(merger_file_id, type_1, data_dict_1)
            written_record_counter += 1
            xlib.Message.print('verbose', f'\rWritten annotations: {written_record_counter}')

            # read the next record of the first annotation file
            (record_1, key_1, data_dict_1) = xlib.read_annotation_record(annotation_file_1, annotation_file_1_id, type_1, read_record_counter_1)
            xlib.Message.print('trace', f'key_1: {key_1} - record_1: {record_1}')

            # write the second file record in the merged annotation file
            xlib.write_merged_annotation_record(merger_file_id, type_2, data_dict_2)
            written_record_counter += 1
            xlib.Message.print('verbose', f'\rWritten annotations: {written_record_counter}')

            # read the next record of the second annotation file
            (record_2, key_2, data_dict_2) = xlib.read_annotation_record(annotation_file_2, annotation_file_2_id, type_2, read_record_counter_2)
            xlib.Message.print('trace', f'key_2: {key_2} - record_2: {record_2}')

        # while there are records in the second annotation file and key of the first annotation file is greater than the key of the second annotation file
        while record_2 != '' and (record_1 != '' and key_1 > key_2 or record_1 == ''):

            # add 1 to record counter
            read_record_counter_2 += 1

            # write in the merged annotation file
            xlib.write_merged_annotation_record(merger_file_id, type_2, data_dict_2)
            written_record_counter += 1
            xlib.Message.print('verbose', f'\rWritten annotations: {written_record_counter}')

            # read the next record of the second annotation file
            (record_2, key_2, data_dict_2) = xlib.read_annotation_record(annotation_file_2, annotation_file_2_id, type_2, read_record_counter_2)
            xlib.Message.print('trace', f'key_2: {key_2} - record_2: {record_2}')

    # print summary
    xlib.Message.print('verbose', '\n')
    xlib.Message.print('info', f'{read_record_counter_1} records read from the first annotation file.')
    xlib.Message.print('info', f'{read_record_counter_2} records read from the second annotation file.')
    xlib.Message.print('info', f'{written_record_counter} records written in the merged annotation file.')

    # close files
    annotation_file_1_id.close()
    annotation_file_2_id.close()
    merger_file_id.close()

#-------------------------------------------------------------------------------

def merge_files_operation_1best(annotation_file_1, type_1, annotation_file_2, type_2, merger_file, header):
    '''
    Merge annotation files with operation "1BEST" (all annotations of the first file and
    annotations if the second file if their seq id is not in the first).
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

    # open the merged annotation file
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

    # print header record in merged file if necessary
    if header == 'Y':
        xlib.write_annotation_header(merger_file_id, 'MERGER')
        written_record_counter += 1

    # read the first record of the first annotation file
    (record_1, key_1, data_dict_1) = xlib.read_annotation_record(annotation_file_1, annotation_file_1_id, type_1, read_record_counter_1)
    xlib.Message.print('trace', f'key_1: {key_1} - record_1: {record_1}')

    # read the first record of the second annotation file
    (record_2, key_2, data_dict_2) = xlib.read_annotation_record(annotation_file_2, annotation_file_2_id, type_2, read_record_counter_2)
    xlib.Message.print('trace', f'key_2: {key_2} - record_2: {record_2}')

    # while there are records in any annotation file
    # (the first compound of the key, the sequence identification of transcripts nt_seq_id, is only considered in this processing)
    while record_1 != '' or record_2 != '':

        # while there are records in the first annotation file and key of the first annotation file is less then the key of the second annotation file
        while record_1 != '' and (record_2 != '' and data_dict_1['nt_seq_id'] < data_dict_2['nt_seq_id'] or record_2 == ''):

            # add 1 to record counter
            read_record_counter_1 += 1

            # write in the merged annotation file
            xlib.write_merged_annotation_record(merger_file_id, type_1, data_dict_1)
            written_record_counter += 1
            xlib.Message.print('verbose', f'\rWritten annotations: {written_record_counter}')

            # read the next record of the first annotation file
            (record_1, key_1, data_dict_1) = xlib.read_annotation_record(annotation_file_1, annotation_file_1_id, type_1, read_record_counter_1)
            xlib.Message.print('trace', f'key_1: {key_1} - record_1: {record_1}')

        # while there are records in the first annotation file and key of the first annotation file is equal to the key of the second annotation file
        while record_1 != '' and record_2 != '' and data_dict_1['nt_seq_id'] == data_dict_2['nt_seq_id']:

            # add 1 to record counter
            read_record_counter_1 += 1

            # write in the merged annotation file
            xlib.write_merged_annotation_record(merger_file_id, type_1, data_dict_1)
            written_record_counter += 1
            xlib.Message.print('verbose', f'\rWritten annotations: {written_record_counter}')

            # read next records of the second annotation file while their key is equal to the key of the first annotation file
            while record_2 != '' and data_dict_1['nt_seq_id'] == data_dict_2['nt_seq_id']:
                (record_2, key_2, data_dict_2) = xlib.read_annotation_record(annotation_file_2, annotation_file_2_id, type_2, read_record_counter_2)
                xlib.Message.print('trace', f'key_2: {key_2} - record_2: {record_2}')

            # read the next record of the first annotation file
            (record_1, key_1, data_dict_1) = xlib.read_annotation_record(annotation_file_1, annotation_file_1_id, type_1, read_record_counter_1)
            xlib.Message.print('trace', f'key_1: {key_1} - record_1: {record_1}')

        # while there are records in the second annotation file and key of the first annotation file is greater than the key of the second annotation file
        while record_2 != '' and (record_1 != '' and data_dict_1['nt_seq_id'] > data_dict_2['nt_seq_id'] or record_1 == ''):

            # add 1 to record counter
            read_record_counter_2 += 1

            # write in the merged annotation file
            xlib.write_merged_annotation_record(merger_file_id, type_2, data_dict_2)
            written_record_counter += 1
            xlib.Message.print('verbose', f'\rWritten annotations: {written_record_counter}')

            # read the next record of the second annotation file
            (record_2, key_2, data_dict_2) = xlib.read_annotation_record(annotation_file_2, annotation_file_2_id, type_2, read_record_counter_2)
            xlib.Message.print('trace', f'key_2: {key_2} - record_2: {record_2}')

    # print summary
    xlib.Message.print('verbose', '\n')
    xlib.Message.print('info', f'{read_record_counter_1} records read from the first annotation file.')
    xlib.Message.print('info', f'{read_record_counter_2} records read from the second annotation file.')
    xlib.Message.print('info', f'{written_record_counter} records written in the merged annotation file.')

    # close files
    annotation_file_1_id.close()
    annotation_file_2_id.close()
    merger_file_id.close()

#-------------------------------------------------------------------------------

def save_annotation_file_merger_format(annotation_file_1, type_1, merger_file, header):
    '''
    Save a annotation file with record format "PLAZA", "REFSEQ", "NT" or "NR" in record format "MERGER".
    '''

    # open the annotation file
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

    # open the merger file
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
    written_record_counter = 0
          
    # print header record in merged file if necessary
    if header == 'Y':
        xlib.write_annotation_header(merger_file_id, 'MERGER')
        written_record_counter += 1

    # read the first record of the annotation file
    (record_1, key_1, data_dict_1) = xlib.read_annotation_record(annotation_file_1, annotation_file_1_id, type_1, read_record_counter_1)
    xlib.Message.print('trace', f'key_1: {key_1} - record_1: {record_1}')

    # while there are records in annotation file
    while record_1 != '':

            # add 1 to record counter
            read_record_counter_1 += 1

            # write in the merged annotation file
            xlib.write_merged_annotation_record(merger_file_id, type_1, data_dict_1)
            written_record_counter += 1
            xlib.Message.print('verbose', f'\rWritten annotations: {written_record_counter}')

            # read the next record of the annotation file
            (record_1, key_1, data_dict_1) = xlib.read_annotation_record(annotation_file_1, annotation_file_1_id, type_1, read_record_counter_1)
            xlib.Message.print('trace', f'key_1: {key_1} - record_1: {record_1}')

    # print summary
    xlib.Message.print('verbose', '\n')
    xlib.Message.print('info', f'{read_record_counter_1} read records in the annotation file.')
    xlib.Message.print('info', f'{written_record_counter} written records in the merged annotation file.')

    # close files
    annotation_file_1_id.close()
    merger_file_id.close()

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
