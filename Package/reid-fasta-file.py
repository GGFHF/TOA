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
This program re-identifies sequences of a FASTA file.
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

    # re-identify sequence identifications of a FASTA file
    reidentify_seq_ids(args.input_fasta_file, args.sequence_type, args.output_fasta_file, args.relationship_file)

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program merges two FASTA files.'
    text = f'{xlib.get_long_project_name()} v{xlib.get_project_version()} - {os.path.basename(__file__)}\n\n{description}\n'
    usage = f'\r{text.ljust(len("usage:"))}\nUsage: {os.path.basename(__file__)} arguments'
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--fasta', dest='input_fasta_file', help='FASTA file path to be re-identificated (mandatory).')
    parser.add_argument('--type', dest='sequence_type', help=f'type of FASTA sequence: {xlib.get_sequence_type_code_list_text()} (mandatory).')
    parser.add_argument('--out', dest='output_fasta_file', help='FASTA file path with sequences re-identificated (mandatory).')
    parser.add_argument('--relationships', dest='relationship_file', help='CSV file path with new-old identification relationships (mandatory).')
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

    # check "input_fasta_file"
    if args.input_fasta_file is None:
        xlib.Message.print('error', '*** The FASTA file to be re-identificated is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.input_fasta_file):
        xlib.Message.print('error', f'*** The file {args.input_fasta_file} does not exist.')
        OK = False

    # check "sequence_type"
    if args.sequence_type is None:
        xlib.Message.print('error', '*** The type of FASTA sequence is not indicated in the input arguments.')
        OK = False
    elif not xlib.check_code(args.sequence_type, xlib.get_sequence_type_code_list(), case_sensitive=False):
        xlib.Message.print('error', f'*** The type of FASTA sequence has to be {xlib.get_sequence_type_code_list_text()}.')
        OK = False
    else:
        args.sequence_type = args.sequence_type.upper()

    # check "output_fasta_file"
    if args.output_fasta_file is None:
        xlib.Message.print('error', '*** The FASTA file with sequences re-identificated is not indicated in the input arguments.')
        OK = False

    # check "relationship_file"
    if args.relationship_file is None:
        xlib.Message.print('error', '*** The CSV file with new-old identification relationships is not indicated in the input arguments.')
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

def reidentify_seq_ids(input_fasta_file, sequence_type, output_fasta_file, relationship_file):
    '''
    Re-identify sequence identifications of a FASTA file.
    '''

    # initialize the new-old identification relationship dictionary
    id_relationship_dict = {}

    # open the input FASTA file
    if input_fasta_file.endswith('.gz'):
        try:
            input_fasta_file_id = gzip.open(input_fasta_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', input_fasta_file)
    else:
        try:
            input_fasta_file_id = open(input_fasta_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', input_fasta_file)

    # open the output FASTA file
    if output_fasta_file.endswith('.gz'):
        try:
            output_fasta_file_id = gzip.open(output_fasta_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', output_fasta_file)
    else:
        try:
            output_fasta_file_id = open(output_fasta_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', output_fasta_file)

    # initialize the sequence counter
    seq_counter = 0

    # set the pattern of the header records (>sequence_info)
    pattern = r'^>(.*)$'

    # read the input record
    record = input_fasta_file_id.readline()

    # while there are records
    while record != '':

        # process the header record 
        if record.startswith('>'):

            # extract the data of the transcript/amino acid
            mo = re.search(pattern, record)
            x_sequence_id = mo.group(1).strip()

            # set the new identification
            toa_sequence_id = f'TOA{sequence_type}{seq_counter:07d}'

            # add the identification relationship to the dictionary
            id_relationship_dict[toa_sequence_id] = x_sequence_id

            # write the header record
            output_fasta_file_id.write(f'>{toa_sequence_id}\n')

            # read the next record
            record = input_fasta_file_id.readline()

        else:

            # control the FASTA format
            raise xlib.ProgramException('F005', input_fasta_file, 'FASTA')

        # while there are records and they are sequence
        while record != '' and not record.startswith('>'):

            # write the sequence
            #  record
            output_fasta_file_id.write(record)

            # read the next record
            record = input_fasta_file_id.readline()

        # add 1 to sequence counter and print it
        seq_counter += 1
        xlib.Message.print('verbose', f'\r{seq_counter} sequences processed of the input FASTA file')

    xlib.Message.print('verbose', '\n')

    # close files
    input_fasta_file_id.close()
    output_fasta_file_id.close()

    # open the relationship file
    if relationship_file.endswith('.gz'):
        try:
            relationship_file_id = gzip.open(relationship_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', relationship_file)
    else:
        try:
            relationship_file_id = open(relationship_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', relationship_file)

    # write header record
    if sequence_type == 'NT':
        header_record = '#toa_sequence_id;transcript_sequence_id\n'
    elif sequence_type == 'AA':
        header_record = '#toa_sequence_id;peptide_sequence_id\n'
    relationship_file_id.write(header_record)

    # write relationship records
    for key in sorted(id_relationship_dict.keys()):
        relationship_record = f'"{key}";"{id_relationship_dict[key]}"\n'
        relationship_file_id.write(relationship_record)

    # close relationship file
    relationship_file_id.close()

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
