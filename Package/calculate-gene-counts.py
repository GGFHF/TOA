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
This program calculates the read counts per sample corresponding to each gene
from a file with transcript read counts.
'''

#-------------------------------------------------------------------------------

import argparse
import gzip
import os
import sys

import xlib
import xsqlite

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

    # connect to the TOA database
    conn = xsqlite.connect_database(args.toa_database)

    # get the taxonomy dictionary of the species name from taxonomy server
    taxonomy_dict = xlib.get_taxonomy_dict('name', args.species_name)
    if taxonomy_dict == {}:
        raise xlib.ProgramException('L006', args.dataset_id)

    # check that species genomic features are loaded in the TOA database
    if xsqlite.check_genomic_features(conn, args.species_name) ==  0:
        raise xlib.ProgramException('L007', args.species_name)

    # load genomic features depending of format of the genomic feature file
    calculate_gene_counts(conn, args.species_name, args.gff_file, args.gff_format, args.transcript_count_file, args.out_transcriptome_count_file, args.out_gene_count_file, args.tsi_list)

    # close connection to TOA database
    conn.close()

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program calculates the read counts per sample corresponding to each gene from a file with transcript read counts.'
    text = '{0} v{1} - {2}\n\n{3}\n'.format(xlib.get_long_project_name(), xlib.get_project_version(), os.path.basename(__file__), description)
    usage = '\r{0}\nUsage: {1} arguments'.format(text.ljust(len('usage:')), os.path.basename(__file__))
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--db', dest='toa_database', help='Path of the TOA database (mandatory).')
    parser.add_argument('--species', dest='species_name', help='The scientific name of the species using underscore as separator, e.g. Quercus_suber (mandatory).')
    parser.add_argument('--gff', dest='gff_file', help='Path of the GFF file (mandatory).')
    parser.add_argument('--format', dest='gff_format', help='The format of the transcript GFF file: {0}; default: {1}.'.format('GTF', 'GTF'))
    parser.add_argument('--tc', dest='transcript_count_file', help='Path of the transcript read count file (mandatory).')
    parser.add_argument('--out-tc', dest='out_transcriptome_count_file', help='Path of the output transcript read count file (mandatory).')
    parser.add_argument('--out-gc', dest='out_gene_count_file', help='Path of the gene read count file (mandatory).')
    parser.add_argument('--verbose', dest='verbose', help='Additional job status info during the run: {0}; default: {1}.'.format(xlib.get_verbose_code_list_text(), xlib.Const.DEFAULT_VERBOSE))
    parser.add_argument('--trace', dest='trace', help='Additional info useful to the developer team: {0}; default: {1}.'.format(xlib.get_trace_code_list_text(), xlib.Const.DEFAULT_TRACE))
    parser.add_argument('--tsi', dest='tsi_list', help='Sequence identification list to trace with format seq_id,seq_id_2,...,seq_id_n or NONE; default: NONE.')

    # return the paser
    return parser

#-------------------------------------------------------------------------------

def check_args(args):
    '''
    Check the input arguments.
    '''

    # initialize the control variable
    OK = True

    # check "toa_database"
    if args.toa_database is None:
        xlib.Message.print('error', '*** The TOA is not indicated in the input arguments.')
        OK = False

    # check "species_name"
    if args.species_name is None:
        xlib.Message.print('error', '*** The scientific name of the species is not indicated in the input arguments.')
        OK = False

    # check "gff_file"
    if args.gff_file is None:
        xlib.Message.print('error', '*** The transcript GFF file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.gff_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.gff_file))
        OK = False

    # check "gff_format"
    if args.gff_file is None:
        args.gff_file = 'GTF'
    elif args.gff_format.upper() != 'GTF':
        xlib.Message.print('error', '*** The format of the GFF file has to be {0}.'.format('GTF'))
        OK = False
    else:
        args.gff_format = args.gff_format.upper()

    # check "transcript_count_file"
    if args.transcript_count_file is None:
        xlib.Message.print('error', '*** The transcript read count file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.transcript_count_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.transcript_count_file))
        OK = False

    # check "out_transcriptome_count_file"
    if args.out_transcriptome_count_file is None:
        xlib.Message.print('error', '*** The output transcript read count file is not indicated in the input arguments.')
        OK = False

    # check "out_gene_count_file"
    if args.out_gene_count_file is None:
        xlib.Message.print('error', '*** The output gene read count file is not indicated in the input arguments.')
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

    # check "tsi_list"
    if args.tsi_list is None or args.tsi_list == 'NONE':
        args.tsi_list = []
    else:
        args.tsi_list = xlib.split_literal_to_string_list(args.tsi_list)

    # if there are errors, exit with exception
    if not OK:
        raise xlib.ProgramException('P001')

#-------------------------------------------------------------------------------

def calculate_gene_counts(conn, species_name, gff_file, gff_format, transcript_count_file, out_transcriptome_count_file, out_gene_count_file, tsi_list):
    '''
    Calculates the gene counts per sample from a file with transcripts counts.
    '''

    # initialize the transcript feature dict
    transcript_feature_dict = {} 

    # open the transcript GFF file
    if gff_file.endswith('.gz'):
        try:
            gff_file_id = gzip.open(gff_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', gff_file)
    else:
        try:
            gff_file_id = open(gff_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', gff_file)

    # initialize the record counter
    record_counter = 0

    # read the first record
    record = gff_file_id.readline()

    # while there are records
    while record != '':

        # add 1 to record counter
        record_counter += 1

        # process data records
        if not record.startswith('#'):

            # extract data
            # record format: seqid\tsource\ttype\tstart\tend\tscore\tstrand\tphase\tattributes
            data_list = []
            pos_1 = 0
            for pos_2 in [i for i, chr in enumerate(record) if chr == '\t']:
                data_list.append(record[pos_1:pos_2].strip())
                pos_1 = pos_2 + 1
            data_list.append(record[pos_1:].strip('\n').strip())
            try:
                transcript_seq_id = data_list[0]
                transcript_type = data_list[2]
                transcript_start = data_list[3]
                transcript_end = data_list[4]
                transcript_attributes = data_list[8]
            except Exception as e:
                raise xlib.ProgramException('F006', os.path.basename(gff_file), record_counter)

            # when type is "transcript"
            if transcript_type == 'transcript':

                # get "gene_id" data from "attributes"
                transcript_gene_id = xlib.get_na()
                literal = 'gene_id "'
                pos_1 = transcript_attributes.find(literal)
                if pos_1 > -1:
                    pos_2 = transcript_attributes.find('"', pos_1 + len(literal) + 1)
                    transcript_gene_id = transcript_attributes[pos_1 + len(literal):pos_2]

                # get the genomic features dictionary
                genomic_features_dict = xsqlite.get_genomic_features_dict(conn, species_name, transcript_seq_id, transcript_start, transcript_end)

                if transcript_seq_id in tsi_list:
                    xlib.Message.print('trace', '\n\n\ntranscript_seq_id: {}'.format(transcript_seq_id))
                    xlib.Message.print('trace', 'transcript_start: {} - transcript_end: {}'.format(transcript_start, transcript_end))
                    xlib.Message.print('trace', 'transcript_gene_id: {}'.format(transcript_gene_id))
                    xlib.Message.print('trace', 'genomic_features_dict: {}'.format(genomic_features_dict))

                # save the transcript gene data in gene_dict
                for i in genomic_features_dict.keys():
                    if genomic_features_dict[i]['type'] == 'mRNA':
                        transcript_feature_dict[transcript_gene_id] = genomic_features_dict[i].get('gene', xlib.get_na())

        # print record counter
        xlib.Message.print('verbose', '\rtranscript GFF file: {0} processed records.'.format(record_counter))

        # read the next record
        record = gff_file_id.readline()

    xlib.Message.print('verbose', '\n')

    # save changes into TOA database
    xlib.Message.print('verbose', 'Saving changes into TOA database ...\n')
    conn.commit()
    xlib.Message.print('verbose', 'Changes are saved.\n')

    # close transcript GFF file
    gff_file_id.close()

    # initialize the sample number
    sample_number = -1

    # initialize sample count per gene dictionary
    gene_count_dict = {}

    # open the transcript read count file
    if transcript_count_file.endswith('.gz'):
        try:
            transcript_count_file_id = gzip.open(transcript_count_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', transcript_count_file)
    else:
        try:
            transcript_count_file_id = open(transcript_count_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', transcript_count_file)

    # open the output transcript read count file which has the gene data added
    if out_transcriptome_count_file.endswith('.gz'):
        try:
            out_transcriptome_count_file_id = gzip.open(out_transcriptome_count_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', out_transcriptome_count_file)
    else:
        try:
            out_transcriptome_count_file_id = open(out_transcriptome_count_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', out_transcriptome_count_file)

    # initialize the record counter
    record_counter = 0

    # read the first record
    record = transcript_count_file_id.readline()

    # while there are records
    while record != '':

        # add 1 to record counter
        record_counter += 1

        # initialize the transcript count list
        transcript_count_list = []

        # extract data
        # record format: transcript_gene_id\tsample_count_1\tsample_count_2\t...\tsample_count_n
        data_list = []
        pos_1 = 0
        for pos_2 in [i for i, chr in enumerate(record) if chr == '\t']:
            data_list.append(record[pos_1:pos_2].strip())
            pos_1 = pos_2 + 1
        data_list.append(record[pos_1:].strip('\n').strip())
        if sample_number == -1:
            sample_number = len(data_list) -1
        else:
            if sample_number != len(data_list) -1:
                raise xlib.ProgramException('F006', os.path.basename(transcript_count_file), record_counter)
        try:
            transcript_gene_id = data_list[0]
            for i in range(1, len(data_list)):
                transcript_count_list.append(int(data_list[i]))
        except Exception as e:
            raise xlib.ProgramException('F006', os.path.basename(transcript_count_file), record_counter)

        # get the transcript gene identification
        gene = transcript_feature_dict.get(transcript_gene_id, xlib.get_na())

        # add transcript sample counts to gene sample counts when gene is not N/A
        if gene != xlib.get_na():
            total_transcript_count_list = gene_count_dict.get(gene, [])
            if total_transcript_count_list == []:
                gene_count_dict[gene] = transcript_count_list
            else:
                gene_count_dict[gene] =  [x + y for x, y in zip(total_transcript_count_list, transcript_count_list)]

        # write the output transcript read count file
        out_record = '{0}\t{1}\t{2}\n'.format(transcript_gene_id, gene, '\t'.join([str(x) for x in transcript_count_list]))
        out_transcriptome_count_file_id.write(out_record)

        # print record counter
        xlib.Message.print('verbose', '\rtranscript read count file: {0} processed records.'.format(record_counter))

        # read the next record
        record = transcript_count_file_id.readline()

    xlib.Message.print('verbose', '\n')

    # close files
    transcript_count_file_id.close()
    out_transcriptome_count_file_id.close()

    # open the output gene read count file
    if out_gene_count_file.endswith('.gz'):
        try:
            out_gene_count_file_id = gzip.open(out_gene_count_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', out_gene_count_file)
    else:
        try:
            out_gene_count_file_id = open(out_gene_count_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', out_gene_count_file)

    # initialize the record counter
    record_counter = 0

    # for each gene
    for key in sorted (gene_count_dict.keys()):

        # write the gene read counts
        out_record = '{0}\t{1}\n'.format(key, '\t'.join([str(x) for x in gene_count_dict[key]]))
        out_gene_count_file_id.write(out_record)

        # add 1 to record counter
        record_counter += 1

        # print record counter
        xlib.Message.print('verbose', '\rgene read count file: {0} processed records.'.format(record_counter))

    xlib.Message.print('verbose', '\n')

    # print OK message 
    xlib.Message.print('info', 'The file {0} containing the gene read counts has been created.'.format(os.path.basename(out_gene_count_file)))

    # close the output gene read count file
    out_gene_count_file_id.close()

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
