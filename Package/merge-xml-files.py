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

    # get the new-old identification relationship dictionary
    id_relationship_dict = xlib.get_id_relationship_dict(args.relationship_file)

    # merge XML file
    merge_files(args.xml_file_list, id_relationship_dict, args.merged_file)

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program merges several XML files.'
    text = '{0} v{1} - {2}\n\n{3}\n'.format(xlib.get_long_project_name(), xlib.get_project_version(), os.path.basename(__file__), description)
    usage = '\r{0}\nUsage: {1} arguments'.format(text.ljust(len('usage:')), os.path.basename(__file__))
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--list', dest='xml_file_list', help='List of XML file paths with the following format: file1,file2,...,filen (mandatory).')
    parser.add_argument('--relationships', dest='relationship_file', help='CSV file path with new-old identification relationships or NONE; default: NONE.')
    parser.add_argument('--mfile', dest='merged_file', help='Merged XML file path (mandatory).')
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
                xlib.Message.print('error', '*** The file {0} does not exist.'.format(xml_file_list[i].strip()))
                OK = False
        # set the argument value
        args.xml_file_list = xml_file_list

    # check "relationship_file"
    if args.relationship_file is None:
        args.relationship_file = 'NONE'
    elif args.relationship_file.upper() == 'NONE':
        args.relationship_file = args.relationship_file.upper()
    elif not os.path.isfile(args.relationship_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.relationship_file))
        OK = False

    # check "merged_file"
    if args.merged_file is None:
        xlib.Message.print('error', '*** The merged file is not indicated in the input arguments.')
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

def merge_files(xml_file_list, id_relationship_dict, merged_file):
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
        xlib.Message.print('verbose', 'Reading fhe file {0} ...\n'.format(os.path.basename(xml_file_list[i])))

        # read the first record
        record = xml_file_id.readline()

        # while there are records
        while record != '':

            # when the tag is BlastOutput_query-def
            if record.strip().startswith('<BlastOutput_query-def>'):

                # get the sequence identification
                start = record.find('>')
                end = record.find('</')
                new_seq_id = record[start + 1:end]

                # get the original sequence identification
                if id_relationship_dict == {}:
                    old_seq_id = new_seq_id
                else:
                    try:
                        old_seq_id = id_relationship_dict[new_seq_id]
                    except Exception as e:
                        raise xlib.ProgramException('L008', new_seq_id)

                # set the record with the original sequence identification
                record = '  <BlastOutput_query-def>{0}</BlastOutput_query-def>\n'.format(old_seq_id)

            # when the tag is Iteration_query-def
            elif record.strip().startswith('<Iteration_query-def>'):

                # get the sequence identification
                start = record.find('>')
                end = record.find('</')
                new_seq_id = record[start + 1:end]

                # get the original sequence identification
                if id_relationship_dict == {}:
                    old_seq_id = new_seq_id
                else:
                    try:
                        old_seq_id = id_relationship_dict[new_seq_id]
                    except Exception as e:
                        raise xlib.ProgramException('L008', new_seq_id)

                # set the record with the original sequence identification
                record = '  <Iteration_query-def>{0}</Iteration_query-def>\n'.format(old_seq_id)

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
                merged_file_id.write('  <Iteration_iter-num>{0}</Iteration_iter-num>\n'.format(query_number))
                merged_file_id.write('  <Iteration_query-ID>Query_{0}</Iteration_query-ID>>\n'.format(query_number))
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
    xlib.Message.print('verbose', 'The file {0} is created\n'.format(os.path.basename(merged_file)))

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
