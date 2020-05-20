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
This program calculates annotation statistics.
'''

#-------------------------------------------------------------------------------

import argparse
import gzip
import os
import re
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

    # calculate general statistics
    calculate_general_stats(conn, args.transcriptome_file, args.peptide_file, args.dataset_list, args.non_annotation_file_list, args.stats_file)

    # calculate functional statistics
    calculate_functional_stats(conn, args.annotation_file, args.type, args.stats_file)

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program calculates annotation statistics.'
    text = '{0} v{1} - {2}\n\n{3}\n'.format(xlib.get_long_project_name(), xlib.get_project_version(), os.path.basename(__file__), description)
    usage = '\r{0}\nUsage: {1} arguments'.format(text.ljust(len('usage:')), os.path.basename(__file__))
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--db', dest='toa_database', help='Path of the TOA database (mandatory).')
    parser.add_argument('--transcriptome', dest='transcriptome_file', help='Path of transcriptome file in FASTA format (mandatory).')
    parser.add_argument('--peptides', dest='peptide_file', help='Path of peptide file in FASTA format in peptide pipeline case or NONE in nucleotide pipeline case (mandatory).')
    parser.add_argument('--dslist', dest='dataset_list', help='List of datasets with format ds_1,ds_2,...,ds_n (mandatoty).')
    parser.add_argument('--nonannlist', dest='non_annotation_file_list', help='List of non annotated file paths with format file_1,file_2,...,file_n  (mandatoty).')
    parser.add_argument('--annotation', dest='annotation_file', help='Path of annotation file in CSV format (mandatory).')
    parser.add_argument('--type', dest='type', help='Type of the annotation file (mandatory): {0}.'.format(xlib.get_type_code_list_text()))
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

    # check "toa_database"
    if args.toa_database is None:
        xlib.Message.print('error', '*** The TOA database is not indicated in the input arguments.')
        OK = False

    # check "transcriptome_file"
    if args.transcriptome_file is None:
        xlib.Message.print('error', '*** The transcriptome file is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.transcriptome_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.transcriptome_file))
        OK = False

    # check "peptide_file"
    if args.peptide_file is None:
        xlib.Message.print('error', '*** The peptide file is not indicated in the input arguments.')
        OK = False
    elif args.peptide_file.upper() == 'NONE':
        args.peptide_file = 'NONE'
    elif not os.path.isfile(args.peptide_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.peptide_file))
        OK = False

    # check "dataset_list"
    if args.dataset_list is None:
        xlib.Message.print('error', '*** The list of annotation databases is not indicated in the input arguments.')
        OK = False
    else:
        args.dataset_list = xlib.split_literal_to_string_list(args.dataset_list)

    # check "non_annotation_file_list"
    if args.non_annotation_file_list is None:
        xlib.Message.print('error', '*** The list of non annotated file paths is not indicated in the input arguments.')
        OK = False
    else:
        args.non_annotation_file_list = xlib.split_literal_to_string_list(args.non_annotation_file_list)
        for non_annotation_file in args.non_annotation_file_list:
            if not os.path.isfile(non_annotation_file):
                xlib.Message.print('error', '*** The file {0} does not exist.'.format(non_annotation_file))
                OK = False

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

def calculate_general_stats(conn, transcriptome_file, peptide_file, dataset_list, non_annotation_file_list, stats_file):
    '''
    Calculate general statistics.
    '''

    # initialize the dataset statistics dictionary
    dataset_stats_dict = {}

    # get the dataset dictionary
    dataset_dict = xsqlite.get_dataset_dict(conn)

    # calculate transcriptome sequence number
    remained_seq_number = calculate_seq_number(transcriptome_file)

    # add transcriptome data to the dataset statistics dictionary
    dataset_stats_dict[1] = {'name': 'Transcriptome', 'annotated': '', 'remained': '{0}'.format(remained_seq_number)}

    # if there is a peptides_file
    if peptide_file != 'NONE':

        # calculate peptide sequence number
        remained_seq_number = calculate_seq_number(peptide_file)

        # add peptide data to the dataset statistics dictionary
        dataset_stats_dict[2] = {'name': 'Predicted peptides', 'annotated': '', 'remained': '{0}'.format(remained_seq_number)}

    # for each annotation dataset
    for i in range(len(dataset_list)):

        # calculate non-annotated sequence number
        non_annotated_seq_number = calculate_seq_number(non_annotation_file_list[i])

        # calculate annotated sequence number
        annotated_seq_number = remained_seq_number - non_annotated_seq_number
        remained_seq_number = non_annotated_seq_number

        # add dataset data to the sgeneral tatistics dictionary
        dataset_stats_dict[i+10] = {'name': dataset_dict[dataset_list[i]]['dataset_name'], 'annotated': '{0}'.format(annotated_seq_number), 'remained': '{0}'.format(remained_seq_number)}

    # write dataset statistics file
    write_dataset_stats(dataset_stats_dict, stats_file)

#-------------------------------------------------------------------------------

def calculate_functional_stats(conn, annotation_file, type, stats_file):
    '''
    Calculate distribution statistics.
    '''

    # initialize the statistics dictionaries
    hit_num_per_hsp_num_stats_dict = {}
    species_stats_dict = {}
    family_stats_dict = {}
    phylum_stats_dict = {}
    go_stats_dict = {}
    seq_num_per_go_id_num_stats_dict = {}
    interpro_stats_dict = {}
    seq_num_per_interpro_id_num_stats_dict = {}
    mapman_stats_dict = {}
    seq_num_per_mapman_id_num_stats_dict = {}
    ec_stats_dict = {}
    seq_num_per_ec_id_num_stats_dict = {}
    kegg_stats_dict = {}
    seq_num_per_kegg_id_num_stats_dict = {}
    metacyc_stats_dict = {}
    seq_num_per_metacyc_id_num_stats_dict = {}

    # initialize the description dictionaries
    interpro_desc_dict = {}
    mapman_desc_dict = {}
    ec_desc_dict = xsqlite.get_ec_id_dict(conn)
    kegg_desc_dict = xsqlite.get_kegg_id_dict(conn)
    metacyc_desc_dict = {}

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

    # initialize the annotation counter
    annotation_counter = 0

    # read the first record of the annotation file (header)
    (record, key, data_dict) = xlib.read_annotation_record(annotation_file, annotation_file_id, type, annotation_counter)

    # read the secord record of the annotation file (first data record)
    (record, key, data_dict) = xlib.read_annotation_record(annotation_file, annotation_file_id, type, annotation_counter)
    xlib.Message.print('trace', 'key: {0} - record: {1}'.format(key, record))

    # while there are records
    while record != '':

        # initialize the old sequence identification
        old_seq_id = data_dict['seq_id']

        # initialize the minimum e-value
        min_evalue = 9999

        # initialize the lists of ontology identifications per sequence
        go_ids_per_seq_list = []
        interpro_ids_per_seq_list = []
        mapman_ids_per_seq_list = []
        ec_ids_per_seq_list = []
        kegg_ids_per_seq_list = []
        metacyc_ids_per_seq_list = []

        # while there are records and the same sequence identification
        while record != '' and data_dict['seq_id'] == old_seq_id:

            # initialize the old hit identification
            old_hit_num = data_dict['hit_num']

            # initialize the HSP counter per HIT
            hsp_counter = 0

            # while there are records and the same sequence identification and the same hit
            while record != '' and data_dict['seq_id'] == old_seq_id and data_dict['hit_num'] == old_hit_num:

                # add 1 to the annotation counter
                annotation_counter += 1

                # add 1 to the HSP counter per HIT
                hsp_counter += 1

                # increase the species counters in the corresponding statistics dictionary (all and first hsp cases)
                species_data = species_stats_dict.get(data_dict['species'], {'all': 0, 'hsp1': 0, 'minevalue':0})
                species_data['all'] = species_data['all'] + 1
                if data_dict['hsp_num'] == '1':
                    species_data['hsp1'] = species_data['hsp1'] + 1
                species_stats_dict[data_dict['species']] = species_data

                # increase the family counters in the corresponding statistics dictionary (all and first hsp cases)
                family_data = family_stats_dict.get(data_dict['family'], {'all': 0, 'hsp1': 0, 'minevalue':0})
                family_data['all'] = family_data['all'] + 1
                if data_dict['hsp_num'] == '1':
                    family_data['hsp1'] = family_data['hsp1'] + 1
                family_stats_dict[data_dict['family']] = family_data

                # increase the phylum counters in the corresponding statistics dictionary (all and first hsp cases)
                phylum_data = phylum_stats_dict.get(data_dict['phylum'], {'all': 0, 'hsp1': 0, 'minevalue':0})
                phylum_data['all'] = phylum_data['all'] + 1
                if data_dict['hsp_num'] == '1':
                    phylum_data['hsp1'] = phylum_data['hsp1'] + 1
                phylum_stats_dict[data_dict['phylum']] = phylum_data

                # extract the GO identifications and add them into the GO identifications list.
                # go_id format: "GO:go_id1*go_id2*...*go_idn"
                if data_dict['go_id'] != '':
                    go_id_list = data_dict['go_id'][3:].split('*')
                else:
                    go_id_list = []

                # increase the GO identification counters in the corresponding statistics dictionary (all and first hsp cases)
                for go_id in go_id_list:
                    go_data = go_stats_dict.get(go_id, {'all': 0, 'hsp1': 0, 'minevalue':0})
                    go_data['all'] = go_data['all'] + 1
                    if data_dict['hsp_num'] == '1':
                        go_data['hsp1'] = go_data['hsp1'] + 1
                    go_stats_dict[go_id] = go_data

                # add GO identifications to the list of GO identifications per sequence
                for go_id in go_id_list:
                    if go_id not in go_ids_per_seq_list:
                        go_ids_per_seq_list.append(go_id)

                # extract the InterPro identifications and add them into the InterPro identifications list.
                # interpro_id format: "interpro_id1*interpro_id2*...*interpro_idn"
                if data_dict['interpro_id'] != '':
                    interpro_id_list = data_dict['interpro_id'].split('*')
                else:
                    interpro_id_list = []

                # extract the InterPro descriptions and add them into the InterPro description dictionary.
                # interpro_id format: "interpro_desc1*interpro_desc2*...*interpro_descn"
                if data_dict['interpro_desc'] != '':
                    interpro_desc_list = data_dict['interpro_desc'].split('*')
                else:
                    interpro_desc_list = []
                for i in range(len(interpro_id_list)):
                    interpro_desc_dict[interpro_id_list[i]] = interpro_desc_list[i]

                # increase the InterPro identification counters in the corresponding statistics dictionary (all and first hsp cases)
                for interpro_id in interpro_id_list:
                    interpro_data = interpro_stats_dict.get(interpro_id, {'all': 0, 'hsp1': 0, 'minevalue':0})
                    interpro_data['all'] = interpro_data['all'] + 1
                    if data_dict['hsp_num'] == '1':
                        interpro_data['hsp1'] = interpro_data['hsp1'] + 1
                    interpro_stats_dict[interpro_id] = interpro_data

                # add InterPro identifications to the list of InterPro identifications per sequence
                for interpro_id in interpro_id_list:
                    if interpro_id not in interpro_ids_per_seq_list:
                        interpro_ids_per_seq_list.append(interpro_id)

                # extract the Mapman identifications and add them into the Mapman identifications list.
                # mapman_id format: "mapman_id1*mapman_id2*...*mapman_idn"
                try:
                    if data_dict['mapman_id'] != '':
                        mapman_id_list = data_dict['mapman_id'].split('*')
                    else:
                        mapman_id_list = []
                except:
                    mapman_id_list = []

                # extract the Mapman descriptions and add them into the Mapman description dictionary.
                # mapman_id format: "mapman_desc1*mapman_desc2*...*mapman_descn"
                try:
                    if data_dict['mapman_desc'] != '':
                            mapman_desc_list = data_dict['mapman_desc'].split('*')
                    else:
                        mapman_desc_list = []
                except:
                    mapman_desc_list = []
                for i in range(len(mapman_id_list)):
                    mapman_desc_dict[mapman_id_list[i]] = mapman_desc_list[i]

                # increase the Mapman identification counters in the corresponding statistics dictionary (all and first hsp cases)
                for mapman_id in mapman_id_list:
                    mapman_data = mapman_stats_dict.get(mapman_id, {'all': 0, 'hsp1': 0, 'minevalue':0})
                    mapman_data['all'] = mapman_data['all'] + 1
                    if data_dict['hsp_num'] == '1':
                        mapman_data['hsp1'] = mapman_data['hsp1'] + 1
                    mapman_stats_dict[mapman_id] = mapman_data

                # add Mapman identifications to the list of Mapman identifications per sequence
                for mapman_id in mapman_id_list:
                    if mapman_id not in mapman_ids_per_seq_list:
                        mapman_ids_per_seq_list.append(mapman_id)

                # extract the EC identifications and add them into the EC identifications list.
                # ec_id format: "ec_id1*ec_id2*...*ec_idn"
                try:
                    if data_dict['ec_id'] != '':
                        ec_id_list = data_dict['ec_id'].split('*')
                    else:
                        ec_id_list = []
                except:
                    ec_id_list = []

                # increase the EC identification counters in the corresponding statistics dictionary (all and first hsp cases)
                for ec_id in ec_id_list:
                    ec_data = ec_stats_dict.get(ec_id, {'all': 0, 'hsp1': 0, 'minevalue':0})
                    ec_data['all'] = ec_data['all'] + 1
                    if data_dict['hsp_num'] == '1':
                        ec_data['hsp1'] = ec_data['hsp1'] + 1
                    ec_stats_dict[ec_id] = ec_data

                # add EC identifications to the list of EC identifications per sequence
                for ec_id in ec_id_list:
                    if ec_id not in ec_ids_per_seq_list:
                        ec_ids_per_seq_list.append(ec_id)

                # extract the KEGG identifications and add them into the KEGG identifications list.
                # kegg_id format: "kegg_id1*kegg_id2*...*kegg_idn"
                try:
                    if data_dict['kegg_id'] != '':
                        kegg_id_list = data_dict['kegg_id'].split('*')
                    else:
                        kegg_id_list = []
                except:
                    kegg_id_list = []

                # increase the KEGG identification counters in the corresponding statistics dictionary (all and first hsp cases)
                for kegg_id in kegg_id_list:
                    kegg_data = kegg_stats_dict.get(kegg_id, {'all': 0, 'hsp1': 0, 'minevalue':0})
                    kegg_data['all'] = kegg_data['all'] + 1
                    if data_dict['hsp_num'] == '1':
                        kegg_data['hsp1'] = kegg_data['hsp1'] + 1
                    kegg_stats_dict[kegg_id] = kegg_data

                # add KEGG identifications to the list of KEGG identifications per sequence
                for kegg_id in kegg_id_list:
                    if kegg_id not in kegg_ids_per_seq_list:
                        kegg_ids_per_seq_list.append(kegg_id)

                # extract the Metacyc identifications and add them into the Metacyc identifications list.
                # metacyc_id format: "metacyc_id1*metacyc_id2*...*metacyc_idn"
                try:
                    if data_dict['metacyc_id'] != '':
                        metacyc_id_list = data_dict['metacyc_id'].split('*')
                    else:
                        metacyc_id_list = []
                except:
                    metacyc_id_list = []

                # increase the Metacyc identification counters in the corresponding statistics dictionary (all and first hsp cases)
                for metacyc_id in metacyc_id_list:
                    metacyc_data = metacyc_stats_dict.get(metacyc_id, {'all': 0, 'hsp1': 0, 'minevalue':0})
                    metacyc_data['all'] = metacyc_data['all'] + 1
                    if data_dict['hsp_num'] == '1':
                        metacyc_data['hsp1'] = metacyc_data['hsp1'] + 1
                    metacyc_stats_dict[metacyc_id] = metacyc_data

                # add Metacyc identifications to the list of Metacyc identifications per sequence
                for metacyc_id in metacyc_id_list:
                    if metacyc_id not in metacyc_ids_per_seq_list:
                        metacyc_ids_per_seq_list.append(metacyc_id)

                # save the species, family and phylum of the hsp with less e-value of the sequence identification
                if float(data_dict['hsp_evalue']) < min_evalue:
                    min_evalue = float(data_dict['hsp_evalue'])
                    min_evalue_species = data_dict['species']
                    min_evalue_family = data_dict['family']
                    min_evalue_phylum = data_dict['phylum']
                    min_evalue_go_id_list = go_id_list
                    min_evalue_interpro_id_list = interpro_id_list
                    min_evalue_mapman_id_list = mapman_id_list
                    min_evalue_ec_id_list = ec_id_list
                    min_evalue_kegg_id_list = kegg_id_list
                    min_evalue_metacyc_id_list = metacyc_id_list

                xlib.Message.print('verbose', '\r{0} processed annotations'.format(annotation_counter))

                # read the next record of the annotation file
                (record, key, data_dict) = xlib.read_annotation_record(annotation_file, annotation_file_id, type, annotation_counter)
                xlib.Message.print('trace', 'key: {0} - record: {1}'.format(key, record))

            # increase the HIT number per HSP number in the corresponding statistics dictionary
            hit_per_hsp_data = hit_num_per_hsp_num_stats_dict.get(hsp_counter, 0)
            hit_num_per_hsp_num_stats_dict[hsp_counter] = hit_per_hsp_data + 1

        # increase the species counters in the corresponding statistics dictionary (minimum e-value case)
        species_data = species_stats_dict.get(min_evalue_species, {'all': 0, 'hsp1': 0, 'minevalue':0})
        species_data['minevalue'] = species_data['minevalue'] + 1
        species_stats_dict[min_evalue_species] = species_data

        # increase the family counters in the corresponding statistics dictionary (minimum e-value case)
        family_data = family_stats_dict.get(min_evalue_family, {'all': 0, 'hsp1': 0, 'minevalue':0})
        family_data['minevalue'] = family_data['minevalue'] + 1
        family_stats_dict[min_evalue_family] = family_data

        # increase the phylum counters in the corresponding statistics dictionary (minimum e-value case)
        phylum_data = phylum_stats_dict.get(min_evalue_phylum, {'all': 0, 'hsp1': 0, 'minevalue':0})
        phylum_data['minevalue'] = phylum_data['minevalue'] + 1
        phylum_stats_dict[min_evalue_phylum] = phylum_data

        # increase the GO identification counters in the corresponding statistics dictionary (minimum e-value case)
        for go_id in min_evalue_go_id_list:
            go_data = go_stats_dict.get(go_id, {'all': 0, 'hsp1': 0, 'minevalue':0})
            go_data['minevalue'] = go_data['minevalue'] + 1
            go_stats_dict[go_id] = go_data

        # increase the sequence number per Gene Ontology identification number in the corresponding statistics dictionary
        seq_per_go_data = seq_num_per_go_id_num_stats_dict.get(len(go_ids_per_seq_list), 0)
        seq_num_per_go_id_num_stats_dict[len(go_ids_per_seq_list)] = seq_per_go_data + 1

        # increase the InterPro identification counters in the corresponding statistics dictionary (minimum e-value case)
        for interpro_id in min_evalue_interpro_id_list:
            interpro_data = interpro_stats_dict.get(interpro_id, {'all': 0, 'hsp1': 0, 'minevalue':0})
            interpro_data['minevalue'] = interpro_data['minevalue'] + 1
            interpro_stats_dict[interpro_id] = interpro_data

        # increase the sequence number per InterPro identification number in the corresponding statistics dictionary
        interpro_per_seq_data = seq_num_per_interpro_id_num_stats_dict.get(len(interpro_ids_per_seq_list), 0)
        seq_num_per_interpro_id_num_stats_dict[len(interpro_ids_per_seq_list)] = interpro_per_seq_data + 1

        # increase the Mapman identification counters in the corresponding statistics dictionary (minimum e-value case)
        for mapman_id in min_evalue_mapman_id_list:
            mapman_data = mapman_stats_dict.get(mapman_id, {'all': 0, 'hsp1': 0, 'minevalue':0})
            mapman_data['minevalue'] = mapman_data['minevalue'] + 1
            mapman_stats_dict[mapman_id] = mapman_data

        # increase sequence number per Mapman identificaction number in the corresponding statistics dictionary
        mapman_per_seq_data = seq_num_per_mapman_id_num_stats_dict.get(len(mapman_ids_per_seq_list), 0)
        seq_num_per_mapman_id_num_stats_dict[len(mapman_ids_per_seq_list)] = mapman_per_seq_data + 1

        # increase the EC identification counters in the corresponding statistics dictionary (minimum e-value case)
        for ec_id in min_evalue_ec_id_list:
            ec_data = ec_stats_dict.get(ec_id, {'all': 0, 'hsp1': 0, 'minevalue':0})
            ec_data['minevalue'] = ec_data['minevalue'] + 1
            ec_stats_dict[ec_id] = ec_data

        # increase sequence number per EC identification number in the corresponding statistics dictionary
        ec_per_seq_data = seq_num_per_ec_id_num_stats_dict.get(len(ec_ids_per_seq_list), 0)
        seq_num_per_ec_id_num_stats_dict[len(ec_ids_per_seq_list)] = ec_per_seq_data + 1

        # increase the KEGG identification counters in the corresponding statistics dictionary (minimum e-value case)
        for kegg_id in min_evalue_kegg_id_list:
            kegg_data = kegg_stats_dict.get(kegg_id, {'all': 0, 'hsp1': 0, 'minevalue':0})
            kegg_data['minevalue'] = kegg_data['minevalue'] + 1
            kegg_stats_dict[kegg_id] = kegg_data

        # increase sequence number per KEGG identification number in the corresponding statistics dictionary
        kegg_per_seq_data = seq_num_per_kegg_id_num_stats_dict.get(len(kegg_ids_per_seq_list), 0)
        seq_num_per_kegg_id_num_stats_dict[len(kegg_ids_per_seq_list)] = kegg_per_seq_data + 1

        # increase the Metacyc identification counters in the corresponding statistics dictionary (minimum e-value case)
        for metacyc_id in min_evalue_metacyc_id_list:
            metacyc_data = metacyc_stats_dict.get(metacyc_id, {'all': 0, 'hsp1': 0, 'minevalue':0})
            metacyc_data['minevalue'] = metacyc_data['minevalue'] + 1
            metacyc_stats_dict[metacyc_id] = metacyc_data

        # increase sequence number per Metacyc identificacion number in the corresponding statistics dictionary
        metacyc_per_seq_data = seq_num_per_metacyc_id_num_stats_dict.get(len(metacyc_ids_per_seq_list), 0)
        seq_num_per_metacyc_id_num_stats_dict[len(metacyc_ids_per_seq_list)] = metacyc_per_seq_data + 1

    xlib.Message.print('verbose', '\n')

    # print summary
    xlib.Message.print('info', '{0} annotation records in annotation file.'.format(annotation_counter))

    # close files
    annotation_file_id.close()

    # write alignment statistics files
    write_x_per_y_stats(hit_num_per_hsp_num_stats_dict, stats_file, stats_code='hit_per_hsp')

    # write phylogenic statistics files
    write_phylogenic_data_frecuency(species_stats_dict, stats_file, stats_code='species')
    write_phylogenic_data_frecuency(family_stats_dict, stats_file, stats_code='family')
    write_phylogenic_data_frecuency(phylum_stats_dict, stats_file, stats_code='phylum')

    # write ontology statistics files
    write_go_data_frecuency(conn, go_stats_dict, stats_file)
    write_x_per_y_stats(seq_num_per_go_id_num_stats_dict, stats_file, stats_code='seq_per_go')
    write_ontologic_data_frecuency(interpro_stats_dict, interpro_desc_dict, stats_file, stats_code='interpro')
    write_x_per_y_stats(seq_num_per_interpro_id_num_stats_dict, stats_file, stats_code='seq_per_interpro')
    write_ontologic_data_frecuency(mapman_stats_dict, mapman_desc_dict, stats_file, stats_code='mapman')
    write_x_per_y_stats(seq_num_per_mapman_id_num_stats_dict, stats_file, stats_code='seq_per_mapman')
    write_ontologic_data_frecuency(ec_stats_dict, ec_desc_dict, stats_file, stats_code='ec')
    write_x_per_y_stats(seq_num_per_ec_id_num_stats_dict, stats_file, stats_code='seq_per_ec')
    write_ontologic_data_frecuency(kegg_stats_dict, kegg_desc_dict, stats_file, stats_code='kegg')
    write_x_per_y_stats(seq_num_per_kegg_id_num_stats_dict, stats_file, stats_code='seq_per_kegg')
    write_ontologic_data_frecuency(metacyc_stats_dict, metacyc_desc_dict, stats_file, stats_code='metacyc')
    write_x_per_y_stats(seq_num_per_metacyc_id_num_stats_dict, stats_file, stats_code='seq_per_metacyc')

    # show OK message 
    xlib.Message.print('info', 'The statistics can be consulted in the file {0}.'.format(os.path.basename(stats_file)))

#-------------------------------------------------------------------------------

def calculate_seq_number(fasta_file):
    '''
    Calculate the sequence number of a FASTA file.
    '''


    # set the pattern of the header records (>sequence_info)
    pattern = r'^>(.*)$'

    # open the FASTA file
    if fasta_file.endswith('.gz'):
        try:
            fasta_file_id = gzip.open(fasta_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', fasta_file)
    else:
        try:
            fasta_file_id = open(fasta_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', fasta_file)

    # initialize the sequence counter
    seq_counter = 0

    # read the first record
    record = fasta_file_id.readline()

    # while there are records
    while record != '':

        # process the header record 
        if record.startswith('>'):

            # extract the data 
            mo = re.search(pattern, record)
            sequence_id = mo.group(1).strip()

            # read the next record
            record = fasta_file_id.readline()

        else:

            # control the FASTA format
            raise xlib.ProgramException('F005', fasta_file, 'FASTA')

        # while there are records and they are sequence
        while record != '' and not record.startswith('>'):

            # read the next record
            record = fasta_file_id.readline()

        # add 1 to sequence counter and print it
        seq_counter += 1

    # close file
    fasta_file_id.close()

    # return the sequence counter
    return seq_counter

#-------------------------------------------------------------------------------

def write_dataset_stats(stats_dict, generic_stats_file):
    '''
    Write a dataset statistics file
    '''

    # get the current file name
    dir_path, filename = os.path.split(generic_stats_file)
    stats_file = '{0}/{1}-{2}'.format(dir_path, 'dataset', filename)

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
    stats_file_id.write( '"dataset_name";"annotated_seq_count";"remained_seq_count"\n')

    # write data record
    for key in sorted(stats_dict.keys()):
        stats_file_id.write( '"{0}";"{1}";{2}\n'.format(stats_dict[key]['name'], stats_dict[key]['annotated'], stats_dict[key]['remained']))

    # close statistics file
    stats_file_id.close()

#-------------------------------------------------------------------------------

def write_x_per_y_stats(stats_dict, generic_stats_file, stats_code):
    '''
    Write a data per other data statistics file
    '''

    # get the current file name
    dir_path, filename = os.path.split(generic_stats_file)
    stats_file = '{0}/{1}-{2}'.format(dir_path, stats_code, filename)

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
    if stats_code == 'hit_per_hsp':
        stats_file_id.write( '"hsp_num";"hit_num"\n')
    elif stats_code == 'seq_per_go':
        stats_file_id.write( '"go_num";"seq_num"\n')
    elif stats_code == 'seq_per_interpro':
        stats_file_id.write( '"interpro_num";"seq_num"\n')
    elif stats_code == 'seq_per_mapman':
        stats_file_id.write( '"mapman_num";"seq_num"\n')
    elif stats_code == 'seq_per_ec':
        stats_file_id.write( '"ec_num";"seq_num"\n')
    elif stats_code == 'seq_per_kegg':
        stats_file_id.write( '"kegg_num";"seq_num"\n')
    elif stats_code == 'seq_per_metacyc':
        stats_file_id.write( '"metacyc_num";"seq_num"\n')

    # write data record
    for key in sorted(stats_dict.keys()):
        stats_file_id.write( '"{0}";"{1}"\n'.format(key, stats_dict[key]))

    # close statistics file
    stats_file_id.close()

#-------------------------------------------------------------------------------

def write_phylogenic_data_frecuency(stats_dict, generic_stats_file, stats_code):
    '''
    Write phylogenic data frecuency.
    '''

    # get the current file name
    dir_path, filename = os.path.split(generic_stats_file)
    stats_file = '{0}/{1}-{2}'.format(dir_path, stats_code, filename)

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
    if stats_code == 'species':
        stats_file_id.write( '"species";"all_count";"first_hsp_countT";"min_evalue_count"\n')
    elif stats_code == 'family':
        stats_file_id.write( '"family";"all_count";"first_hsp_count";"min_evalue_count"\n')
    elif stats_code == 'phylum':
        stats_file_id.write( '"phylum";"all_count";"first_hsp_count";"min_evalue_count"\n')

    # write data record
    for key in sorted(stats_dict.keys()):
        stats_file_id.write( '"{0}";{1};{2};{3}\n'.format(key, stats_dict[key]['all'], stats_dict[key]['hsp1'], stats_dict[key]['minevalue']))

    # close statistics file
    stats_file_id.close()

#-------------------------------------------------------------------------------

def write_ontologic_data_frecuency(stats_dict, desc_dict, generic_stats_file, stats_code):
    '''
    Write ontology data frecuency.
    '''

    # get the current file name
    dir_path, filename = os.path.split(generic_stats_file)
    stats_file = os.path.join(dir_path, '{0}-{1}'.format(stats_code, filename))

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
    if stats_code == 'interpro':
        stats_file_id.write( '"interpro_id";"description";"all_count";"first_hsp_countT";"min_evalue_count"\n')
    elif stats_code == 'mapman':
        stats_file_id.write( '"mapman_id";"description";"all_count";"first_hsp_countT";"min_evalue_count"\n')
    elif stats_code == 'ec':
        stats_file_id.write( '"ec_id";"description";"all_count";"first_hsp_countT";"min_evalue_count"\n')
    elif stats_code == 'kegg':
        stats_file_id.write( '"kegg_id";"description";"all_count";"first_hsp_countT";"min_evalue_count"\n')
    elif stats_code == 'metacyc':
        stats_file_id.write( '"metacyc_id";"description";"all_count";"first_hsp_countT";"min_evalue_count"\n')

    # write data record
    for key in sorted(stats_dict.keys()):
        if stats_code == 'ec':
            desc = desc_dict.get(key, {}).get('desc', 'N/A')
        elif stats_code == 'kegg':
            key2 = 'k{}'.format(key[1:])
            desc = desc_dict.get(key2, {}).get('desc', 'N/A')
        else:
            desc = desc_dict.get(key, 'N/A')
        stats_file_id.write( '"{0}";"{1}";{2};{3};{4}\n'.format(key, desc, stats_dict[key]['all'], stats_dict[key]['hsp1'], stats_dict[key]['minevalue']))

    # close statistics file
    stats_file_id.close()

#-------------------------------------------------------------------------------

def write_go_data_frecuency(conn, go_id_stats_dict, generic_stats_file):
    '''
    Write GO data frencuency.
    '''

    # iitialize namespace statistics dictionary
    namespace_stats_dict = {}

    # get the GO ontology dictionary
    go_ontology_dictionary = xsqlite.get_go_ontology_dict(conn, go_id_list=[])

    # get the current file names
    dir_path, filename = os.path.split(generic_stats_file)
    go_id_stats_file = '{0}/{1}-{2}'.format(dir_path, 'go', filename)
    namespace_stats_file = '{0}/{1}-{2}'.format(dir_path, 'namespace', filename)

    # open the file of statistics by GO identifier
    if go_id_stats_file.endswith('.gz'):
        try:
            go_id_stats_file_id = gzip.open(go_id_stats_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', go_id_stats_file)
    else:
        try:
            go_id_stats_file_id = open(go_id_stats_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', go_id_stats_file)

    # write the header in the file of statistics by GO identifier
    go_id_stats_file_id.write( '"go_term";"description";"namespace";"all_count";"first_hsp_countT";"min_evalue_count"\n')

    # write data in the file of statistics by GO identifier and accumulate data in the namespace statistics dictionary
    for key in sorted(go_id_stats_dict.keys()):
        try:
            go_id_stats_file_id.write( '"GO:{0}";{1};{2};{3};{4};{5}\n'.format(key, go_ontology_dictionary[key]['go_name'], go_ontology_dictionary[key]['namespace'], go_id_stats_dict[key]['all'], go_id_stats_dict[key]['hsp1'], go_id_stats_dict[key]['minevalue']))
            namespace_data = namespace_stats_dict.get(go_ontology_dictionary[key]['namespace'], {'all': 0, 'hsp1': 0, 'minevalue':0})
            namespace_data['all'] = namespace_data['all'] + go_id_stats_dict[key]['all']
            namespace_data['hsp1'] = namespace_data['hsp1'] + go_id_stats_dict[key]['hsp1']
            namespace_data['minevalue'] = namespace_data['minevalue'] + go_id_stats_dict[key]['minevalue']
            namespace_stats_dict[go_ontology_dictionary[key]['namespace']] = namespace_data
        except Exception as e:
            go_id_stats_file_id.write( '"GO:{0}";{1};{2};{3};{4};{5}\n'.format(key, 'N/A', 'N/A', go_id_stats_dict[key]['all'], go_id_stats_dict[key]['hsp1'], go_id_stats_dict[key]['minevalue']))
            namespace_data = namespace_stats_dict.get('N/A', {'all': 0, 'hsp1': 0, 'minevalue':0})
            namespace_data['all'] = namespace_data['all'] + go_id_stats_dict[key]['all']
            namespace_data['hsp1'] = namespace_data['hsp1'] + go_id_stats_dict[key]['hsp1']
            namespace_data['minevalue'] = namespace_data['minevalue'] + go_id_stats_dict[key]['minevalue']
            namespace_stats_dict['N/A'] = namespace_data

    # close the file of statistics by GO identifier
    go_id_stats_file_id.close()

    # open the file of statistics by namespace
    if namespace_stats_file.endswith('.gz'):
        try:
            namespace_stats_file_id = gzip.open(namespace_stats_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', namespace_stats_file)
    else:
        try:
            namespace_stats_file_id = open(namespace_stats_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', namespace_stats_file)

    # write the header in the file of statistics by namespace
    namespace_stats_file_id.write( '"namespace";"all_count";"first_hsp_countT";"min_evalue_count"\n')

    # write data in the file of statistics by namespace
    for key in sorted(namespace_stats_dict.keys()):

        # write data record
        namespace_stats_file_id.write( '"{0}";{1};{2};{3}\n'.format(key, namespace_stats_dict[key]['all'], namespace_stats_dict[key]['hsp1'], namespace_stats_dict[key]['minevalue']))

    # close the file of statistics by namespace
    namespace_stats_file_id.close()

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
