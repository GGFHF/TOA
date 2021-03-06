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
This program merges several XML files.
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

    # get the TOA-transcriptome identification relationship dictionary
    if args.toa_transcriptome_relationship_file == 'NONE':
        toa_transcriptome_relationship_dict = {}
    else:
        toa_transcriptome_relationship_dict = xlib.get_id_relationship_dict(args.toa_transcriptome_relationship_file)

    # get the TOA-TransDecoder identification relationship dictionary
    if args.toa_transdecoder_relationship_file == 'NONE':
        toa_transdecoder_relationship_dict = {}
    else:
        toa_transdecoder_relationship_dict = xlib.get_id_relationship_dict(args.toa_transdecoder_relationship_file)

    # merge XML file
    merge_files(args.xml_file_list, toa_transcriptome_relationship_dict, toa_transdecoder_relationship_dict, args.merged_file)

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program merges several XML files.'
    text = f'{xlib.get_long_project_name()} v{xlib.get_project_version()} - {os.path.basename(__file__)}\n\n{description}\n'
    usage = f'\r{text.ljust(len("usage:"))}\nUsage: {os.path.basename(__file__)} arguments'
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--list', dest='xml_file_list', help='List of XML file paths with the following format: file1,file2,...,filen (mandatory).')
    parser.add_argument('--relationships', dest='toa_transcriptome_relationship_file', help='CSV file path with TOA-transcriptome identification relationships or NONE; default: NONE.')
    parser.add_argument('--relationships2', dest='toa_transdecoder_relationship_file', help='CSV file path with TOA-TransDecoder identification relationships or NONE (mandatory)')
    parser.add_argument('--mfile', dest='merged_file', help='Merged XML file path (mandatory).')
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

    # check "xml_file_list"
    if args.xml_file_list is None:
        xlib.Message.print('error', '*** The list of XML file paths is not indicated in the input arguments.')
        OK = False
    else:
        # initialize the XML file list
        xml_file_list = []
        # split "xml_file_list" in a string values list
        xml_file_list = args.xml_file_list.split(',')
        # check if XML file exist
        for i in range(len(xml_file_list)):
            xml_file_list[i] = xml_file_list[i].strip()
            if not os.path.isfile(xml_file_list[i]):
                xlib.Message.print('error', f'*** The file {xml_file_list[i].strip()} does not exist.')
                OK = False
        # set the argument value
        args.xml_file_list = xml_file_list

    # check "toa_transcriptome_relationship_file"
    if args.toa_transcriptome_relationship_file is None:
        args.toa_transcriptome_relationship_file = 'NONE'
    elif args.toa_transcriptome_relationship_file.upper() == 'NONE':
        args.toa_transcriptome_relationship_file = args.toa_transcriptome_relationship_file.upper()
    elif not os.path.isfile(args.toa_transcriptome_relationship_file):
        xlib.Message.print('error', f'*** The file {args.toa_transcriptome_relationship_file} does not exist.')
        OK = False

    # check "toa_transdecoder_relationship_file"
    if args.toa_transdecoder_relationship_file is None:
        args.toa_transdecoder_relationship_file = 'NONE'
    elif args.toa_transdecoder_relationship_file.upper() == 'NONE':
        args.toa_transdecoder_relationship_file = args.toa_transdecoder_relationship_file.upper()
    elif args.toa_transdecoder_relationship_file.upper() != 'NONE' and args.toa_transcriptome_relationship_file.upper() == 'NONE':
        xlib.Message.print('error', '*** The TOA-TransDecoder identification relationships file has to be NONE when TOA-transcriptome identification relationships file is NONE.')
        OK = False
    elif not os.path.isfile(args.toa_transdecoder_relationship_file):
        xlib.Message.print('error', f'*** The file {args.toa_transdecoder_relationship_file} does not exist.')
        OK = False

    # check "merged_file"
    if args.merged_file is None:
        xlib.Message.print('error', '*** The merged file is not indicated in the input arguments.')
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

def merge_files(xml_file_list, toa_transcriptome_relationship_dict, toa_transdecoder_relationship_dict, merged_file):
    '''
    '''
    # open the merged XML file
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
                
    # process every annotation file
    for i in range(len(xml_file_list)):

        # set the query number
        query_number = (i + 1) * xlib.Const.MAX_QUERY_NUMBER_PER_FILE

        # open the XML file
        if xml_file_list[i].endswith('.gz'):
            try:
                xml_file_id = gzip.open(xml_file_list[i], mode='rt', encoding='iso-8859-1')
            except Exception as e:
                raise xlib.ProgramException('F002', xml_file_list[i])
        else:
            try:
                xml_file_id = open(xml_file_list[i], mode='r', encoding='iso-8859-1')
            except Exception as e:
                raise xlib.ProgramException('F001', xml_file_list[i])
        xlib.Message.print('verbose', f'Reading the file {os.path.basename(xml_file_list[i])} ...\n')

        # read the first record
        record = xml_file_id.readline()

        # while there are records
        while record != '':

            # when the tag is BlastOutput_query-def
            if record.strip().startswith('<BlastOutput_query-def>'):

                # get the sequence identification
                start = record.find('>')
                end = record.find('</')
                seq_id = record[start + 1:end]

                # get the transcript sequence identification
                if toa_transcriptome_relationship_dict == {}:
                    transcript_seq_id = seq_id
                else:
                    (transcript_seq_id, nt_seq_id, aa_seq_id) = xlib.get_seq_ids(seq_id, toa_transcriptome_relationship_dict, toa_transdecoder_relationship_dict)

                # set the record with the original sequence identification
                record = f'  <BlastOutput_query-def>{transcript_seq_id}</BlastOutput_query-def>\n'

            # when the tag is Iteration_query-def
            elif record.strip().startswith('<Iteration_query-def>'):

                # get the sequence identification
                start = record.find('>')
                end = record.find('</')
                seq_id = record[start + 1:end]

                # get the transcript sequence identification
                if toa_transcriptome_relationship_dict == {}:
                    transcript_seq_id = seq_id
                else:
                    (transcript_seq_id, nt_seq_id, aa_seq_id) = xlib.get_seq_ids(seq_id, toa_transcriptome_relationship_dict, toa_transdecoder_relationship_dict)

                # set the record with the original sequence identification
                record = f'  <Iteration_query-def>{transcript_seq_id}</Iteration_query-def>\n'

            # write the record in the merged XML file
            if record.strip().startswith('<?xml') or record.strip().startswith('<!DOCTYPE') or record.strip().startswith('<BlastOutput') or record.strip().startswith('</BlastOutput_param>') or record.strip().startswith('<Parameters') or record.strip().startswith('</Parameters>'):
                if i == 0:
                    merged_file_id.write(record)
                else:
                    pass
            elif record.strip().startswith('</BlastOutput_iterations>') or record.strip().startswith('</BlastOutput>'):
                if i == len(xml_file_list) - 1:
                    merged_file_id.write(record)
                else:
                    pass
            elif record.strip().startswith('<Iteration_iter-num>'):
                merged_file_id.write(f'  <Iteration_iter-num>{query_number}</Iteration_iter-num>\n')
                merged_file_id.write(f'  <Iteration_query-ID>Query_{query_number}</Iteration_query-ID>>\n')
                query_number += 1
            elif record.strip().startswith('<Iteration_query-ID>'):
                pass
            elif record.strip() != '':
                merged_file_id.write(record)

            # read the next record
            record = xml_file_id.readline()

        # close the XML file
        xml_file_id.close()

    # close the merged XML file
    merged_file_id.close()
    xlib.Message.print('verbose', f'The file {os.path.basename(merged_file)} is created\n')

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
