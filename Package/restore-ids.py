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
This program restores original sequence identifications in a FASTA, XML or annotation CSV.
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

    # get the new-old identification relationship dictionary
    id_relationship_dict = xlib.get_id_relationship_dict(args.relationship_file)

    # restore old identification in a FASTA file
    if args.file_format == 'FASTA':
        restore_ids_fasta(args.input_file, id_relationship_dict, args.output_file)
    # restore old identification in a XML file
    elif args.file_format == 'XML':
        restore_ids_xml(args.input_file, id_relationship_dict, args.output_file)
    # restore old identification in a CSV file
    elif args.file_format == 'CSV':
        restore_ids_csv(args.input_file, id_relationship_dict, args.output_file)

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program restores original sequence identifications in a FASTA, XML or annotation CSV.'
    text = '{0} v{1} - {2}\n\n{3}\n'.format(xlib.get_long_project_name(), xlib.get_project_version(), os.path.basename(__file__), description)
    usage = '\r{0}\nUsage: {1} arguments'.format(text.ljust(len('usage:')), os.path.basename(__file__))
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--in', dest='input_file', help='Input file path (mandatory).')
    parser.add_argument('--format', dest='file_format', help='Format of the input file: {0} (mandatory).'.format(xlib.get_restored_file_format_code_list_text()))
    parser.add_argument('--relationships', dest='relationship_file', help='CSV file path with new-old identification relationships (mandatory).')
    parser.add_argument('--out', dest='output_file', help='Output file path (mandatory).')
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

    # check "input_file"
    if args.input_file is None:
        xlib.Message.print('error', '*** The input file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.input_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.input_file))
        OK = False

    # check "file_format"
    if args.file_format is None:
        xlib.Message.print('error', '*** The merger operation is not indicated in the input arguments.')
        OK = False
    elif not xlib.check_code(args.file_format, xlib.get_restored_file_format_code_list(), case_sensitive=False):
        xlib.Message.print('error', '*** The merger operation has to be {0}.'.format(xlib.get_restored_file_format_code_list_text()))
        OK = False
    else:
        args.file_format = args.file_format.upper()

    # check "relationship_file"
    if args.relationship_file is None:
        args.relationship_file = 'NONE'
    elif args.relationship_file.upper() == 'NONE':
        args.relationship_file = args.relationship_file.upper()
    elif not os.path.isfile(args.relationship_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.relationship_file))
        OK = False

    # check "output_file"
    if args.output_file is None:
        xlib.Message.print('error', '*** The output file is not indicated in the input arguments.')
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

def restore_ids_fasta(input_file, id_relationship_dict, output_file):
    '''
    Restore original sequence identifications in a FASTA file
    '''

    # initialize the sequence counter
    seq_counter = 0

    # set the pattern of the header records (>sequence_info)
    pattern = r'^>(.*)$'

    # open the input FASTA file
    if input_file.endswith('.gz'):
        try:
            input_file_id = gzip.open(input_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', input_file)
    else:
        try:
            input_file_id = open(input_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', input_file)

    # open the output FASTA file
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

    # read the first record
    record = input_file_id.readline()

    # while there are records
    while record != '':

        # process the header record 
        if record.startswith('>'):

            # extract the data 
            mo = re.search(pattern, record)
            seq_id = mo.group(1).strip()

            # get the original sequence identification
            try:
                old_seq_id = id_relationship_dict[seq_id]
            except Exception as e:
                raise xlib.ProgramException('L008', seq_id)

            # write the header record
            header_record = '>{0}\n'.format(old_seq_id)
            output_file_id.write(header_record)

            # read the next record
            record = input_file_id.readline()

        else:

            # control the FASTA format
            raise xlib.ProgramException('F005', input_file, 'FASTA')

        # while there are records and they are sequence
        while record != '' and not record.startswith('>'):

            # write the sequence
            output_file_id.write(record)

            # read the next record
            record = input_file_id.readline()

        # add 1 to read sequence count and print it
        seq_counter += 1
        xlib.Message.print('verbose', '\r{0} sequences processed of the input FASTA file'.format(seq_counter))

    xlib.Message.print('verbose', '\n')

    # close files
    input_file_id.close()
    output_file_id.close()

    # print OK message 
    xlib.Message.print('verbose', 'The file {0} is created\n.'.format(os.path.basename(output_file)))

#-------------------------------------------------------------------------------

def restore_ids_xml(input_file, id_relationship_dict, output_file):
    '''
    Restore original sequence identifications in a XML file
    '''

    # open the input XML file
    if input_file.endswith('.gz'):
        try:
            input_file_id = gzip.open(input_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', input_file)
    else:
        try:
            input_file_id = open(input_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', input_file)

    # open the output XML file
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

    # initialize input record counter
    input_record_counter = 0

    # read the first record
    record = input_file_id.readline()

    # while there are records
    while record != '':

        # add 1 to the input record counter
        input_record_counter += 1

        # when the tag is BlastOutput_query-def
        if record.strip().startswith('<BlastOutput_query-def>'):

            # get the sequence identification
            start = record.find('>')
            end = record.find('</')
            seq_id = record[start + 1:end]

            # get the original sequence identification
            try:
                old_seq_id = id_relationship_dict[seq_id]
            except Exception as e:
                raise xlib.ProgramException('L008', seq_id)

            # set the record with the original sequence identification
            record = '  <BlastOutput_query-def>{0}</BlastOutput_query-def>\n'.format(old_seq_id)

        # when the tag is Iteration_query-def
        elif record.strip().startswith('<Iteration_query-def>'):

            # get the sequence identification
            start = record.find('>')
            end = record.find('</')
            seq_id = record[start + 1:end]

            # get the original sequence identification
            try:
                old_seq_id = id_relationship_dict[seq_id]
            except Exception as e:
                raise xlib.ProgramException('L008', seq_id)

            # set the record with the original sequence identification
            record = '  <Iteration_query-def>{0}</Iteration_query-def>\n'.format(old_seq_id)

        # write the record in the output XML file
        output_file_id.write(record)

        # print the input record counter
        xlib.Message.print('verbose', '\rProcessed records ... {0:8d}'.format(input_record_counter))

        # read the next record
        record = input_file_id.readline()

    xlib.Message.print('verbose', '\n')

    # close files
    input_file_id.close()
    output_file_id.close()

    # print OK message 
    xlib.Message.print('verbose', 'The file {0} is created\n.'.format(os.path.basename(output_file)))

#-------------------------------------------------------------------------------

def restore_ids_csv(input_file, id_relationship_dict, output_file):
    '''
    Restore original sequence identifications in a CSV file
    '''

    # open the input CSV file
    if input_file.endswith('.gz'):
        try:
            input_file_id = gzip.open(input_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', input_file)
    else:
        try:
            input_file_id = open(input_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', input_file)

    # open the ouput CSV file
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

    # initialize the input record counter
    input_record_counter = 0

    # read the first record
    record = input_file_id.readline()

    # while there are records
    while record != '':

        # add 1 to record counter
        input_record_counter += 1

        # get the sequence identification
        comma_pos = record.find(';')
        seq_id = record[:comma_pos].strip('"')

        # if the record is not the header
        if seq_id != 'seq_id':

            # get the original sequence identification
            try:
                old_seq_id = id_relationship_dict[seq_id]
            except Exception as e:
                raise xlib.ProgramException('L008', seq_id)

            # set the record with the original sequence identification
            record = '"{0}"'.format(seq_id) + record[comma_pos:]

        # write the record in the output CSV file
        output_file_id.write(record)

        # print the input record counter
        xlib.Message.print('verbose', '\rProcessed records ... {0:8d}'.format(input_record_counter))

        # read the next record
        record = input_file_id.readline()

    # print summary
    xlib.Message.print('verbose', '\n')

    # close files
    input_file_id.close()
    output_file_id.close()

    # print OK message 
    xlib.Message.print('verbose', 'The file {0} is created\n.'.format(os.path.basename(output_file)))

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
