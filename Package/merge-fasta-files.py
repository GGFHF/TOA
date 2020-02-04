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
This program merges two FASTA files.
'''

#-------------------------------------------------------------------------------

import argparse
import gzip
import os
import re
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

    # get the dictionary with sequence identifications of the second FASTA file
    file_2_id_dict = get_file_2_id_dict(args.fasta_file_2)

    # get the new-old identification relationship dictionary
    id_relationship_dict = xlib.get_id_relationship_dict(args.relationship_file)

    # merge FASTA files with operation "1AND2" (sequences included in both files)
    if args.merger_operation ==  '1AND2':
        merge_files_operation_1and2(args.fasta_file_1, file_2_id_dict, args.merged_file, id_relationship_dict)
    # merge FASTA files with operation "1LESS2" (sequences in file 1 and not in file 2)
    elif args.merger_operation ==  '1LESS2':
        merge_files_operation_1less2(args.fasta_file_1, file_2_id_dict, args.merged_file, id_relationship_dict)

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program merges two FASTA files.'
    text = '{0} v{1} - {2}\n\n{3}\n'.format(xlib.get_long_project_name(), xlib.get_project_version(), os.path.basename(__file__), description)
    usage = '\r{0}\nUsage: {1} arguments'.format(text.ljust(len('usage:')), os.path.basename(__file__))
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--file1', dest='fasta_file_1', help='First FASTA file path (mandatory).')
    parser.add_argument('--file2', dest='fasta_file_2', help='Second FASTA file path (mandatory).')
    parser.add_argument('--mfile', dest='merged_file', help='Merged FASTA file path (mandatory).')
    parser.add_argument('--operation', dest='merger_operation', help='Merger operation (mandatory): {0}.'.format(xlib.get_merger_operation_code_list_text()))
    parser.add_argument('--relationships', dest='relationship_file', help='CSV file path with new-old identification relationships or NONE; default: NONE.')
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

    # check "fasta_file_1"
    if args.fasta_file_1 is None:
        xlib.Message.print('error', '*** The first FASTA file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.fasta_file_1):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.fasta_file_1))
        OK = False

    # check "fasta_file_2"
    if args.fasta_file_2 is None:
        xlib.Message.print('error', '*** The second FASTA file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.fasta_file_2):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.fasta_file_2))
        OK = False

    # check "merged_file"
    if args.merged_file is None:
        xlib.Message.print('error', '*** The merged file is not indicated in the input arguments.')
        OK = False

    # check "merger_operation"
    if args.merger_operation is None:
        xlib.Message.print('error', '*** The merger operation is not indicated in the input arguments.')
        OK = False
    elif not xlib.check_code(args.merger_operation, xlib.get_merger_operation_code_list(), case_sensitive=False):
        xlib.Message.print('error', '*** The merger operation has to be {0}.'.format(xlib.get_merger_operation_code_list_text()))
        OK = False
    else:
        args.merger_operation = args.merger_operation.upper()

    # check "relationship_file"
    if args.relationship_file is None:
        args.relationship_file = 'NONE'
    elif args.relationship_file.upper() == 'NONE':
        args.relationship_file = args.relationship_file.upper()
    elif not os.path.isfile(args.relationship_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.relationship_file))
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

def get_file_2_id_dict(fasta_file_2):
    '''
    '''

    # initialize the dictionary with sequence identifications of the second file
    file_2_id_dict = {}

    # set the pattern of the header records (>sequence_info)
    pattern = r'^>(.*)$'

    # open the second FASTA file
    if fasta_file_2.endswith('.gz'):
        try:
            fasta_file_2_id = gzip.open(fasta_file_2, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', fasta_file_2)
    else:
        try:
            fasta_file_2_id = open(fasta_file_2, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', fasta_file_2)

    # initialize the sequence counter
    seq_counter = 0

    # read the first record
    record = fasta_file_2_id.readline()

    # while there are records
    while record != '':

        # process the header record 
        if record.startswith('>'):

            # extract the data 
            mo = re.search(pattern, record)
            sequence_id = mo.group(1).strip()

            # add sequence identification to the dictionary
            file_2_id_dict[sequence_id] = True

            # read the next record
            record = fasta_file_2_id.readline()

        else:

            # control the FASTA format
            raise xlib.ProgramException('F005', fasta_file_2, 'FASTA')

        # while there are records and they are sequence
        while record != '' and not record.startswith('>'):

            # read the next record
            record = fasta_file_2_id.readline()

        # add 1 to sequence counter and print it
        seq_counter += 1
        xlib.Message.print('verbose', '\r{0} sequences processed of the second FASTA file'.format(seq_counter))

    xlib.Message.print('verbose', '\n')

    # close file
    fasta_file_2_id.close()

    # return the dictionary with sequence identifications of the second file
    return file_2_id_dict

#-------------------------------------------------------------------------------

def merge_files_operation_1and2(fasta_file_1, file_2_id_dict, merged_file, id_relationship_dict):
    '''
    '''

    # initialize the sequence counters
    read_seq_counter = 0
    written_seq_counter = 0

    # set the pattern of the header records (>sequence_info)
    pattern = r'^>(.*)$'

    # open the first FASTA file
    if fasta_file_1.endswith('.gz'):
        try:
            fasta_file_1_id = gzip.open(fasta_file_1, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', fasta_file_1)
    else:
        try:
            fasta_file_1_id = open(fasta_file_1, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', fasta_file_1)

    # open the merged file
    if merged_file.endswith('.gz'):
        try:
            merged_file_id = gzip.open(merged_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', merged_file)
    else:
        try:
            merged_file_id = open(merged_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', merged_file)

    # read the first record
    record = fasta_file_1_id.readline()

    # while there are records
    while record != '':

        # process the header record 
        if record.startswith('>'):

            # extract the data 
            mo = re.search(pattern, record)
            seq_id = mo.group(1).strip()

            # find the sequence identification in the dictionary with sequence identifications of the second FASTA file
            found = file_2_id_dict.get(seq_id, False)

            # if the sequence identification is found, i. e. the sequence is in both FASTA files
            if found:

                # get the sequence identification
                if id_relationship_dict == {}:
                    old_seq_id = seq_id
                else:
                    try:
                        old_seq_id = id_relationship_dict[seq_id]
                    except Exception as e:
                        raise xlib.ProgramException('L008', seq_id)

                # write the header record
                header_record = '>{0}\n'.format(old_seq_id)
                merged_file_id.write(header_record)

                # add 1 to written sequence counter
                written_seq_counter += 1

            # read the next record
            record = fasta_file_1_id.readline()

        else:

            # control the FASTA format
            raise xlib.ProgramException('F005', fasta_file_1, 'FASTA')

        # while there are records and they are sequence
        while record != '' and not record.startswith('>'):

            # if the sequence identification is found, i. e. the sequence is in both FASTA files
            if found:

                # write the sequence
                merged_file_id.write(record)

            # read the next record
            record = fasta_file_1_id.readline()

        # add 1 to read sequence count and print it
        read_seq_counter += 1
        xlib.Message.print('verbose', '\r{0} sequences processed of the first FASTA file'.format(read_seq_counter))

    xlib.Message.print('verbose', '\n')
    xlib.Message.print('verbose', '{0} sequences written of the merged FASTA file\n'.format(written_seq_counter))

    # close files
    fasta_file_1_id.close()
    merged_file_id.close()

#-------------------------------------------------------------------------------

def merge_files_operation_1less2(fasta_file_1, file_2_id_dict, merged_file, id_relationship_dict):
    '''
    '''

    # initialize the sequence counter
    read_seq_counter = 0
    written_seq_counter = 0

    # set the pattern of the header records (>sequence_info)
    pattern = r'^>(.*)$'

    # open the first FASTA file
    if fasta_file_1.endswith('.gz'):
        try:
            fasta_file_1_id = gzip.open(fasta_file_1, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', fasta_file_1)
    else:
        try:
            fasta_file_1_id = open(fasta_file_1, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', fasta_file_1)

    # open the merged file
    if merged_file.endswith('.gz'):
        try:
            merged_file_id = gzip.open(merged_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', merged_file)
    else:
        try:
            merged_file_id = open(merged_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', merged_file)

    # read the first record
    record = fasta_file_1_id.readline()

    # while there are records
    while record != '':

        # process the header record 
        if record.startswith('>'):

            # extract the data 
            mo = re.search(pattern, record)
            seq_id = mo.group(1).strip()

            # find the sequence identification in the dictionary with sequence identifications of the second FASTA file
            found = file_2_id_dict.get(seq_id, False)

            # if the sequence identification is not found in the FASTA file
            if not found:

                # get the sequence identification
                if id_relationship_dict == {}:
                    old_seq_id = seq_id
                else:
                    try:
                        old_seq_id = id_relationship_dict[seq_id]
                    except Exception as e:
                        raise xlib.ProgramException('L008', seq_id)

                # write the header record
                header_record = '>{0}\n'.format(old_seq_id)
                merged_file_id.write(header_record)

                # add 1 to written sequence counter
                written_seq_counter += 1

            # read the next record
            record = fasta_file_1_id.readline()

        else:

            # control the FASTA format
            raise xlib.ProgramException('F005', fasta_file_1, 'FASTA')

        # while there are records and they are sequence
        while record != '' and not record.startswith('>'):

            # if the sequence identification is not found in the second FASTA file
            if not found:

                # write the sequence
                merged_file_id.write(record)

            # read the next record
            record = fasta_file_1_id.readline()

        # add 1 to read sequence counter and print it
        read_seq_counter += 1
        xlib.Message.print('verbose', '\r{0} sequences processed of the first FASTA file'.format(read_seq_counter))

    xlib.Message.print('verbose', '\n')
    xlib.Message.print('verbose', '{0} sequences written of the merged FASTA file\n'.format(written_seq_counter))

    # close files
    fasta_file_1_id.close()
    merged_file_id.close()

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
