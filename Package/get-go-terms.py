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
This program gets a file with Gene Ontology terms corresponding to each sequence.
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

    # get Gene Ontology terms per sequence
    get_go_terms(args.annotation_file, args.type, args.score_file, args.go_file)

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program gets a file with Gene Ontology terms corresponding to each sequence.'
    text = f'{xlib.get_long_project_name()} v{xlib.get_project_version()} - {os.path.basename(__file__)}\n\n{description}\n'
    usage = f'\r{text.ljust(len("usage:"))}\nUsage: {os.path.basename(__file__)} arguments'
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--annotation', dest='annotation_file', help='Path of annotation file in CSV format (mandatory).')
    parser.add_argument('--type', dest='type', help=f'Type of the annotation file (mandatory): {xlib.get_type2_code_list_text()}.')
    parser.add_argument('--score', dest='score_file', help='Path of file with sequence scores in CSV format (mandatory).')
    parser.add_argument('--go', dest='go_file', help='Path of file with GO terms per sequence in CSV format (mandatory).')
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

    # check "annotation_file"
    if args.annotation_file is None:
        xlib.Message.print('error', '*** The annotation file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.annotation_file):
        xlib.Message.print('error', f'*** The file {args.annotation_file} does not exist.')
        OK = False

    # check "type"
    if args.type is None:
        xlib.Message.print('error', '*** The type of annotation file is not indicated in the input arguments.')
        OK = False
    elif not xlib.check_code(args.type, xlib.get_type2_code_list(), case_sensitive=False):
        xlib.Message.print('error', f'*** The type of annotation file has to be {xlib.get_type2_code_list_text()}.')
        OK = False
    else:
        args.type = args.type.upper()

    # check "score_file"
    if args.score_file is None:
        xlib.Message.print('error', '*** The sequence score file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.score_file):
        xlib.Message.print('error', f'*** The file {args.score_file} does not exist.')
        OK = False

    # check "go_file"
    if args.go_file is None:
        xlib.Message.print('error', '*** The file with GO terms per sequence is not indicated in the input arguments.')
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

def get_go_terms(annotation_file, type, score_file, go_file):
    '''
    '''

    # initialize the sequence identification dictionary
    seq_id_dict = {}

    # get the score dictionary
    score_dict = get_score_dict(score_file)

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

    # initialize record counters
    read_record_counter = 0
    written_record_counter = 0

    # read the header and first data records of the annotation file
    (record, key, data_dict) = xlib.read_annotation_record(annotation_file, annotation_file_id, type, read_record_counter)
    (record, key, data_dict) = xlib.read_annotation_record(annotation_file, annotation_file_id, type, read_record_counter)
    read_record_counter += 2

    # while there are records
    while record != '':

        # extract the GO identifications and add them into the GO identifications list of the sequence.
        # go_id format: "go_id1|||go_id2|||...|||go_idn"
        if data_dict['go_id'] != '':
            go_id_list = seq_id_dict.get(key, [])
            begin = 0
            while True:
                next = data_dict['go_id'][begin:].find('|||')
                if next == -1:
                    break
                end = begin + next
                go_id = data_dict['go_id'][begin:end]
                if go_id not in go_id_list:
                    go_id_list.append(go_id)
                begin = end + 3
            go_id = data_dict['go_id'][begin:]
            if go_id not in go_id_list:
                go_id_list.append(go_id)
            seq_id_dict[key] = go_id_list

        # read the next record of the annotation file
        (record, key, data_dict) = xlib.read_annotation_record(annotation_file, annotation_file_id, type, read_record_counter)
        read_record_counter += 1
        xlib.Message.print('verbose', f'\rRead annotations: {read_record_counter}')

    xlib.Message.print('verbose', '\n')

    # close file
    annotation_file_id.close()

    # open the Gene Ontology term file
    if go_file.endswith('.gz'):
        try:
            go_file_id = gzip.open(go_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', go_file)
    else:
        try:
            go_file_id = open(go_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', go_file)

    # Write the Gene Ontology term file
    for seq_id in seq_id_dict.keys():

        # get the sequence score
        score = score_dict.get(seq_id, '0')

        # for each seq_id, get the GO identifications
        for go_id in seq_id_dict[seq_id]:

            # write in the Gene Ontology term file
            written_record_counter += 1
            go_file_id.write(f'{go_id} {score}\n')
            xlib.Message.print('verbose', f'\rWritten GO identifications: {written_record_counter}')

    xlib.Message.print('verbose', '\n')

    # close file
    go_file_id.close()

#-------------------------------------------------------------------------------

def get_score_dict(score_file):
    '''
    '''

    # initialize the score dictonary
    score_dict = {}

    # open the score file
    if score_file.endswith('.gz'):
        try:
            score_file_id = gzip.open(score_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', score_file)
    else:
        try:
            score_file_id = open(score_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', score_file)

    # initialize the record counter
    record_counter = 0

    # read the header and first data records
    record = score_file_id.readline()
    record = score_file_id.readline()

    # while there are records
    while record != '':

        # add 1 to the identification counter
        record_counter += 1
        xlib.Message.print('verbose', f'\rScores: {record_counter}')

        # extract score data
        # record format: "seq_id";"score"
        pos_list = [i for i, chr in enumerate(record) if chr == '"']
        try:
            seq_id = record[pos_list[0]+1:pos_list[1]].strip()
            FPKM = float(record[pos_list[2]+1:pos_list[3]].strip())
        except Exception as e:
            raise xlib.ProgramException('F006', os.path.basename(score_file), record_counter)

        # add score data to the dictionary
        score_dict[seq_id] = FPKM

        # read the next record
        record = score_file_id.readline()

    xlib.Message.print('verbose', '\n')

    # close file
    score_file_id.close()

    # return the score dictonary
    return score_dict

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
