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
This program extracts annotations of an annotation file.
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

    # extract annotations
    extract_annotations(args.annotation_file, args.type, args.id_file, args.extract_file, args.stats_file)

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program extracts annotations of an annotation file.'
    text = '{0} v{1} - {2}\n\n{3}\n'.format(xlib.get_long_project_name(), xlib.get_project_version(), os.path.basename(__file__), description)
    usage = '\r{0}\nUsage: {1} arguments'.format(text.ljust(len('usage:')), os.path.basename(__file__))
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--annotation', dest='annotation_file', help='Path of annotation file in CSV format (mandatory).')
    parser.add_argument('--type', dest='type', help='Type of the annotation file (mandatory): {0}.'.format(xlib.get_type_code_list_text()))
    parser.add_argument('--id', dest='id_file', help='Path of the identification file in plane text (mandatory).')
    parser.add_argument('--extract', dest='extract_file', help='Path of extracted annotation file in CSV format (mandatory).')
    parser.add_argument('--stats', dest='stats_file', help='Path of statistics file in CSV format (mandatory).')
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

    # check "id_file"
    if args.id_file is None:
        xlib.Message.print('error', '*** The identification file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.id_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.id_file))
        OK = False

    # check "extract_file"
    if args.extract_file is None:
        xlib.Message.print('error', '*** The extracted annotation file is not indicated in the input arguments.')
        OK = False

    # check "stats_file"
    if args.stats_file is None:
        xlib.Message.print('error', '*** The statistics file is not indicated in the input arguments.')
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

def extract_annotations(annotation_file, type, id_file, extract_file, stats_file):
    '''
    '''

    # get the identification data
    (id_list, id_dict) = get_id_data(id_file)

    # open the annotation file
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

    # open the extracted identification file
    if extract_file.endswith('.gz'):
        try:
            extract_file_id = gzip.open(extract_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', extract_file)
    else:
        try:
            extract_file_id = open(extract_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', extract_file)

    # initialize record counters
    read_record_counter = 0
    written_record_counter = 0
          
    # write header record in the extracted identification file
    xlib.write_annotation_header(extract_file_id, type)
    written_record_counter += 1

    # read the first record of the annotation file (header)
    read_record_counter += 1
    (record, key, data_dict) = xlib.read_annotation_record(annotation_file, annotation_file_id, type, read_record_counter)
    xlib.Message.print('trace', 'key: {0} - record: {1}'.format(key, record))

    # while there are records
    while record != '':

        # get the identification of the current record
        id = key

        # this sentence block is only used in a particular case
        if key.startswith('CUFF'):
            first_dot_position = key.find('.')
            second_dot_position = key.find('.', first_dot_position + 1)
            id = key[:second_dot_position]
        elif key.startswith('scaffold'):
            id = key[:key.find(' ')]

        # if the key is in the identification list
        if id in id_list:

            # add 1 to the annotation counter of the identification
            id_dict[id] += 1

            # write in the extracted identification file
            xlib.write_merged_annotation_record(extract_file_id, type, data_dict)
            written_record_counter += 1

        xlib.Message.print('verbose', '\r{0} read annotations - {1} written annotations'.format(read_record_counter, written_record_counter))

        # read the next record of the annotation file
        read_record_counter += 1
        (record, key, data_dict) = xlib.read_annotation_record(annotation_file, annotation_file_id, type, read_record_counter)
        xlib.Message.print('trace', 'key: {0} - record: {1}'.format(key, record))

    xlib.Message.print('verbose', '\n')

    # print summary
    xlib.Message.print('info', '{0} annotations read in annotation file.'.format(read_record_counter - 1))
    xlib.Message.print('info', '{0} annotations written in the extracted identification file.'.format(written_record_counter))

    # close files
    annotation_file_id.close()
    extract_file_id.close()

    # write stats
    write_stats(stats_file, id_list, id_dict)

#-------------------------------------------------------------------------------

def get_id_data(id_file):
    '''
    '''

    # initialize the list and dictonary of identifications
    id_list = []
    id_dict = {}

    # initialize the identification counter
    id_counter = 0

    # open the identification file
    if id_file.endswith('.gz'):
        try:
            id_file_id = gzip.open(id_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', id_file)
    else:
        try:
            id_file_id = open(id_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', id_file)

    # read the first record
    record = id_file_id.readline()

    # while there are records
    while record != '':

        # add identification to the list and dictionary
        id_list.append(record.strip())
        id_dict[record.strip()] = 0

        # add 1 to the identification counter
        id_counter += 1
        xlib.Message.print('verbose', '\r{0} identifications.'.format(id_counter))

        # read the next record
        record = id_file_id.readline()

    xlib.Message.print('verbose', '\n')

    # close file
    id_file_id.close()

    # sort the identification list
    if id_list != []:
        id_list.sort()

    # return the list and dictonary of identifications
    return id_list, id_dict

#-------------------------------------------------------------------------------

def write_stats(stats_file, id_list, id_dict):
    '''
    '''

    # open the statistics file
    if stats_file.endswith('.gz'):
        try:
            stats_file_id = gzip.open(stats_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', stats_file)
    else:
        try:
            stats_file_id = open(stats_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', stats_file)

    # write the header
    stats_file_id.write('"IDENTIFICATION";"ANNOTATION NUMBER";\n')

    # write the statistics
    for key in id_list:

        # write the data in the statistics file
        stats_file_id.write('"{0}";{1};\n'.format(key, id_dict[key]))

    # close statistics file
    stats_file_id.close()

    # show OK message 
    xlib.Message.print('info', 'The statistics can be consulted in the file {0}.'.format(os.path.basename(stats_file)))

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
