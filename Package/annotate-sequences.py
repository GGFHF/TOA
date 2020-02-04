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
This program annotates sequences (nucleotides or proteins) using the TOA database.
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

    # check the dataset identification
    dataset_id = args.dataset_id.lower()
    if not xsqlite.is_dataset_id_found(conn, dataset_id):
        raise xlib.ProgramException('L001', args.dataset_id)

    # get the new-old identification relationship dictionary
    id_relationship_dict = xlib.get_id_relationship_dict(args.relationship_file)

    # annotate sequences depending of the dataset identification
    if dataset_id in ['gymno_01', 'dicots_04', 'monocots_04']: 
        annotate_sequences_plaza(conn, dataset_id, args.seq_file, id_relationship_dict, args.annotation_file, args.nonann_seq_file, type='PLAZA')
    elif dataset_id in ['refseq_plant']: 
        annotate_sequences_refseq(conn, dataset_id, args.seq_file, id_relationship_dict, args.annotation_file, args.nonann_seq_file, type='REFSEQ')
    elif dataset_id in ['nt_viridiplantae', 'nt_remainder']: 
        annotate_sequences_nx(conn, dataset_id, args.seq_file, id_relationship_dict, args.annotation_file, args.nonann_seq_file, type='NT')
    elif dataset_id in ['nr_viridiplantae', 'nr_remainder']: 
        annotate_sequences_nx(conn, dataset_id, args.seq_file, id_relationship_dict, args.annotation_file, args.nonann_seq_file, type='NR')

    # close connection to TOA database
    conn.close()

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program annotates sequences (nucleotides or proteins) using the TOA database.'
    text = '{0} v{1} - {2}\n\n{3}\n'.format(xlib.get_long_project_name(), xlib.get_project_version(), os.path.basename(__file__), description)
    usage = '\r{0}\nUsage: {1} arguments'.format(text.ljust(len('usage:')), os.path.basename(__file__))
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--db', dest='toa_database', help='Path of the TOA database (mandatory).')
    parser.add_argument('--dataset', dest='dataset_id', help='Dataset identification (mandatory).')
    parser.add_argument('--seqs', dest='seq_file', help='Path of the file with sequences to be annotated (mandatory).')
    parser.add_argument('--relationships', dest='relationship_file', help='CSV file path with new-old identification relationships or NONE; default: NONE.')
    parser.add_argument('--annotation', dest='annotation_file', help='Path of annotation file in CSV format (mandatory).')
    parser.add_argument('--nonann', dest='nonann_seq_file', help='Path of file with non-annotated sequences (mandatory).')
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

    # check "dataset_id"
    if args.dataset_id is None:
        xlib.Message.print('error', '*** The dataset identification is not indicated in the input arguments.')
        OK = False

    # check "seq_file"
    if args.seq_file is None:
        xlib.Message.print('error', '*** The file with sequences to be annotated is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.seq_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.seq_file))
        OK = False

    # check "relationship_file"
    if args.relationship_file is None:
        args.relationship_file = 'NONE'
    elif args.relationship_file.upper() == 'NONE':
        args.relationship_file = args.relationship_file.upper()
    elif not os.path.isfile(args.relationship_file):
        xlib.Message.print('error', '*** The file {0} does not exist.'.format(args.relationship_file))
        OK = False

    # check "annotation_file"
    if args.annotation_file is None:
        xlib.Message.print('error', '*** The annotation file is not indicated in the input arguments.')
        OK = False

    # check "nonann_seq_file"
    if args.nonann_seq_file is None:
        xlib.Message.print('error', '*** The file with non-annotated sequences is not indicated in the input arguments.')
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

def annotate_sequences_plaza(conn, dataset_id, seq_file, id_relationship_dict, annotation_file, nonann_seq_file, type):
    '''
    '''

    # get the species dictionary
    species_dict = xsqlite.get_plaza_species_dict(conn)

    # get the PLAZA gene description dictionary
    gene_description_dict = xsqlite.get_gene_description_dict(conn, dataset_id, 'all')

    # open the sequence file
    if seq_file.endswith('.gz'):
        try:
            seq_file_id = gzip.open(seq_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', seq_file)
    else:
        try:
            seq_file_id = open(seq_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', seq_file)

    # open the annotation file
    if annotation_file.endswith('.gz'):
        try:
            annotation_file_id = gzip.open(annotation_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', annotation_file)
    else:
        try:
            annotation_file_id = open(annotation_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', annotation_file)

    # open the file with non-annotated sequences
    if nonann_seq_file.endswith('.gz'):
        try:
            nonann_seq_file_id = gzip.open(nonann_seq_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', nonann_seq_file)
    else:
        try:
            nonann_seq_file_id = open(nonann_seq_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', nonann_seq_file)

    # initialize the counters
    seq_counter = 0
    non_annotated_seq_counter = 0
    written_annotation_counter = 0

    # write header record of the annotation file
    xlib.write_annotation_header(annotation_file_id, type)
    written_annotation_counter += 1

    # read the first record
    record = seq_file_id.readline()

    # while there are records
    while record != '':

        # process the header record 
        if record.startswith('>'):

            # get the sequence id 
            new_seq_id = record[1:].strip()
            if id_relationship_dict == {}:
                old_seq_id = new_seq_id
            else:
                try:
                    old_seq_id = id_relationship_dict[new_seq_id]
                except Exception as e:
                    raise xlib.ProgramException('L008', new_seq_id)
            xlib.Message.print('trace', 'new_seq_id: {0} - old_seq_id: {1}'. format(new_seq_id, old_seq_id))

            # initialize the sequence annotation control variable
            is_seq_annotated = False

            # find the BLAST dictionary with data corresponding to the sequence identification
            blast_dict = xsqlite.get_blast_dict(conn, dataset_id, new_seq_id)
            
            # annotate the sequence for each hit-hsp if the dictionary has data
            if blast_dict != {}:
                for key1 in blast_dict.keys():

                    xlib.Message.print('trace', 'key: {0}'. format(key1))

                    # initialize the hsp annotation control variable
                    is_hsp_annotated = False

                    # initialize data dictionary
                    data_dict = {}
                    data_dict['seq_id'] = old_seq_id

                    # asign iteration-hit-hsp values
                    data_dict['iteration_iter_num'] = blast_dict[key1]['iteration_iter_num']
                    data_dict['hit_num'] = blast_dict[key1]['hit_num']
                    data_dict['hit_def'] = blast_dict[key1]['hit_def']
                    data_dict['hit_accession'] = blast_dict[key1]['hit_accession']
                    data_dict['hsp_num'] = blast_dict[key1]['hsp_num']
                    data_dict['hsp_evalue'] = blast_dict[key1]['hsp_evalue']
                    data_dict['hsp_identity'] = blast_dict[key1]['hsp_identity']
                    data_dict['hsp_positive'] = blast_dict[key1]['hsp_positive']
                    data_dict['hsp_gaps'] = blast_dict[key1]['hsp_gaps']
                    data_dict['hsp_align_len'] = blast_dict[key1]['hsp_align_len']
                    data_dict['hsp_qseq'] = blast_dict[key1]['hsp_qseq']
                    xlib.Message.print('trace', 'iteration_iter_num: {0}'.format(data_dict['iteration_iter_num']))
                    xlib.Message.print('trace', 'hit_num: {0} - hit_def: {1} - hit_accession: {2}'.format(data_dict['hit_num'], data_dict['hit_def'], data_dict['hit_accession']))
                    xlib.Message.print('trace', 'hsp_num: {0} - hsp_evalue:{1} - hsp_identity: {2} - hsp_positive: {3} - hsp_gaps: {4} - hsp_align_len: {5}'.format(data_dict['hsp_num'], data_dict['hsp_evalue'], data_dict['hsp_identity'], data_dict['hsp_positive'], data_dict['hsp_gaps'], data_dict['hsp_align_len']))
                    xlib.Message.print('trace', 'hsp_qseq: {0}'.format(data_dict['hsp_qseq']))

                    # get the gene identification
                    # case 1:
                    if xlib.check_int(data_dict['hit_accession']):
                        if dataset_id in ['gymno_01']:
                            gene_id = data_dict['hit_def'].strip()
                        elif dataset_id in ['dicots_04', 'monocots_04']:
                            gene_id = data_dict['hit_def'][data_dict['hit_def'].find('|')+1:].strip()
                    # case 2:
                    else:
                        if dataset_id in ['gymno_01']:
                            gene_id = data_dict['hit_accession'].strip()
                        elif dataset_id in ['dicots_04', 'monocots_04']:
                            gene_id = data_dict['hit_accession'][data_dict['hit_accession'].find('|')+1:].strip()

                    # get the PLAZA species identification
                    description_plaza_species_id = gene_description_dict.get(gene_id, {}).get('plaza_species_id', xlib.get_na())

                    # get the PLAZA gene description
                    data_dict['desc'] = gene_description_dict.get(gene_id, {}).get('desc', xlib.get_na())

                    # get the specie name and its taxonomy data
                    data_dict['species'] = species_dict.get(description_plaza_species_id, {}).get('species_name', xlib.get_na())
                    data_dict['family'] = species_dict.get(description_plaza_species_id, {}).get('family_name', xlib.get_na())
                    data_dict['phylum'] = species_dict.get(description_plaza_species_id, {}).get('phylum_name', xlib.get_na())
                    data_dict['kingdom'] = species_dict.get(description_plaza_species_id, {}).get('kingdom_name', xlib.get_na())
                    data_dict['superkingdom'] = species_dict.get(description_plaza_species_id, {}).get('superkingdom_name', xlib.get_na())
                    xlib.Message.print('trace', 'plaza_species_id: {0} ({1})'.format(description_plaza_species_id, data_dict['species']))

                    # initialize accumulate annotation values
                    if dataset_id == 'gymno_01':
                        data_dict['accum_databases'] = 'GymnoPLAZA1.0'
                    elif dataset_id == 'dicots_04':
                        data_dict['accum_databases'] = 'DicotsPLAZA4.0'
                    elif dataset_id == 'monocots_04':
                        data_dict['accum_databases'] = 'MonocotsPLAZA4.0'
                    data_dict['accum_interpro_id'] = ''
                    data_dict['accum_interpro_desc'] = ''
                    data_dict['accum_go_id'] = ''
                    data_dict['accum_go_desc'] = ''
                    data_dict['accum_mapman_id'] = ''
                    data_dict['accum_mapman_desc'] = ''
                    data_dict['accum_ec_id'] = ''
                    data_dict['accum_kegg_id'] = ''
                    data_dict['accum_metacyc_id'] = ''

                    # get Gene Ontology dictionary with data corresponding to the gene identification
                    go_dict = xsqlite.get_go_dict(conn, dataset_id, gene_id)

                    # annotate using Gene Ontology data
                    if go_dict != {}:

                        # set the annotation control variables
                        is_seq_annotated = True
                        is_hsp_annotated = True

                        # set accumulate database list
                        data_dict['accum_databases'] = 'GO' if data_dict['accum_databases'] == '' else '{0}*GO'.format(data_dict['accum_databases'])

                        # get the species name and taxonomy data and its taxonomy data
                        if data_dict['species'] == xlib.get_na():
                            go_plaza_species_id = go_dict[0]['plaza_species_id']
                            data_dict['species'] = species_dict.get(go_plaza_species_id, {}).get('species_name', xlib.get_na())
                            data_dict['family'] = species_dict.get(go_plaza_species_id, {}).get('family_name', xlib.get_na())
                            data_dict['phylum'] = species_dict.get(go_plaza_species_id, {}).get('phylum_name', xlib.get_na())
                            data_dict['kingdom'] = species_dict.get(go_plaza_species_id, {}).get('kingdom_name', xlib.get_na())
                            data_dict['superkingdom'] = species_dict.get(go_plaza_species_id, {}).get('superkingdom_name', xlib.get_na())
                            xlib.Message.print('trace', 'GO -> plaza_species_id: {0} ({1})'.format(go_plaza_species_id, data_dict['species']))

                        # for each Gene Ontology annotation
                        for key2 in go_dict.keys():

                            # get annotation values
                            go_id = go_dict[key2]['go_id']
                            go_desc = go_dict[key2]['desc']
                            xlib.Message.print('trace', 'GO -> id: {0} - desc: {1}'.format(go_id, go_desc))

                            # accumulate values
                            data_dict['accum_go_id'] = go_id if data_dict['accum_go_id'] == '' else '{0}*{1}'.format(data_dict['accum_go_id'], go_id)
                            data_dict['accum_go_desc'] = go_desc if data_dict['accum_go_desc'] == '' else '{0}*{1}'.format(data_dict['accum_go_desc'], go_desc)

                    # get InterPro dictionary with data corresponding to the gene identification
                    interpro_dict = xsqlite.get_interpro_dict(conn, dataset_id, gene_id)

                    # annotate using Interpro data
                    if interpro_dict != {}:

                        # set the annotation control variables
                        is_seq_annotated = True
                        is_hsp_annotated = True

                        # set accumulate database list
                        data_dict['accum_databases'] = 'InterPro' if data_dict['accum_databases'] == '' else '{0}*InterPro'.format(data_dict['accum_databases'])

                        # get the species name
                        if data_dict['species'] == xlib.get_na():
                            interpro_plaza_species_id = interpro_dict[0]['plaza_species_id']
                            data_dict['species'] = species_dict.get(interpro_plaza_species_id, {}).get('species_name', xlib.get_na())
                            data_dict['family'] = species_dict.get(interpro_plaza_species_id, {}).get('family_name', xlib.get_na())
                            data_dict['phylum'] = species_dict.get(interpro_plaza_species_id, {}).get('phylum_name', xlib.get_na())
                            data_dict['kingdom'] = species_dict.get(interpro_plaza_species_id, {}).get('kingdom_name', xlib.get_na())
                            data_dict['superkingdom'] = species_dict.get(interpro_plaza_species_id, {}).get('superkingdom_name', xlib.get_na())
                            xlib.Message.print('trace', 'INTERPRO -> plaza_species_id: {0} ({1})'.format(interpro_plaza_species_id, data_dict['species']))

                        # for each Interpro annotation
                        for key3 in interpro_dict.keys():

                            # get annotation values
                            interpro_id = interpro_dict[key3]['motif_id']
                            interpro_desc = interpro_dict[key3]['desc']
                            xlib.Message.print('trace', 'InterPro -> id: {0} - desc: {1}'.format(interpro_id, interpro_desc))

                            # accumulate values
                            data_dict['accum_interpro_id'] = interpro_id if data_dict['accum_interpro_id'] == '' else '{0}*{1}'.format(data_dict['accum_interpro_id'], interpro_id)
                            data_dict['accum_interpro_desc'] = interpro_desc if data_dict['accum_interpro_desc'] == '' else '{0}*{1}'.format(data_dict['accum_interpro_desc'], interpro_desc)

                        # if there are not Gene Ontology data
                        if go_dict == {}:

                            # get data from InterPro interpro2go
                            interpro2go_dict = xsqlite.get_interpro2go_dict(conn, interpro_id)

                            # annotate using Interpro interpro2go
                            if interpro2go_dict != {}:

                                # set accumulate database list
                                data_dict['accum_databases'] = '{0}*GO2'.format(data_dict['accum_databases'])

                                # for each interpro2go annotation
                                for key4 in interpro2go_dict.keys():

                                    # get annotation values
                                    go_id = interpro2go_dict[key4]['go_id']
                                    go_desc = interpro2go_dict[key4]['go_desc']
                                    xlib.Message.print('trace', 'GO2 -> id: {0} - desc: {1}'.format(go_id, go_desc))

                                    # accumulate values
                                    data_dict['accum_go_id'] = go_id if data_dict['accum_go_id'] == '' else '{0}*{1}'.format(data_dict['accum_go_id'], go_id)
                                    data_dict['accum_go_desc'] = go_desc if data_dict['accum_go_desc'] == '' else '{0}*{1}'.format(data_dict['accum_go_desc'], go_desc)

                    # get Mapman dictionary with data corresponding to the gene identification
                    mapman_dict = xsqlite.get_mapman_dict(conn, dataset_id, gene_id)

                    # annotate using Mapman data
                    if mapman_dict != {}:

                        # set the annotation control variables
                        is_seq_annotated = True
                        is_hsp_annotated = True

                        # set accumulate database list
                        data_dict['accum_databases'] = 'MapMan' if data_dict['accum_databases'] == '' else '{0}*MapMan'.format(data_dict['accum_databases'])

                        # get the species name and taxonomy data and its taxonomy data
                        if data_dict['species'] == xlib.get_na():
                            mapman_plaza_species_id = mapman_dict[0]['plaza_species_id']
                            data_dict['species'] = species_dict.get(mapman_plaza_species_id, {}).get('species_name', xlib.get_na())
                            data_dict['family'] = species_dict.get(mapman_plaza_species_id, {}).get('family_name', xlib.get_na())
                            data_dict['phylum'] = species_dict.get(mapman_plaza_species_id, {}).get('phylum_name', xlib.get_na())
                            data_dict['kingdom'] = species_dict.get(mapman_plaza_species_id, {}).get('kingdom_name', xlib.get_na())
                            data_dict['superkingdom'] = species_dict.get(mapman_plaza_species_id, {}).get('superkingdom_name', xlib.get_na())
                            xlib.Message.print('trace', 'MAPMAN -> plaza_species_id: {0} ({1})'.format(mapman_plaza_species_id, data_dict['species']))

                        # for each Mapman annotation
                        for key5 in mapman_dict.keys():

                            # get annotation values
                            mapman_id = mapman_dict[key5]['mapman_id']
                            mapman_desc = mapman_dict[key5]['desc']
                            xlib.Message.print('trace', 'MAPMAN -> id: {0} - desc: {1}'.format(mapman_id, mapman_desc))

                            # accumulate values
                            data_dict['accum_mapman_id'] = mapman_id if data_dict['accum_mapman_id'] == '' else '{0}*{1}'.format(data_dict['accum_mapman_id'], mapman_id)
                            data_dict['accum_mapman_desc'] = mapman_desc if data_dict['accum_mapman_desc'] == '' else '{0}*{1}'.format(data_dict['accum_mapman_desc'], mapman_desc)

                    # get Enzyme Commission, KEGG and MetaCyc data from Gene Onlology identification
                    if data_dict['accum_go_id'] != '':

                        # get the Gene Ontology identification list
                        go_id_list = data_dict['accum_go_id'].split('*')

                        # get Enzyme Commission dictionary with data corresponding to the Gene Onlology identification list
                        ec_dict = xsqlite.get_cross_references_dict(conn, go_id_list, 'ec')

                        # annotate using Enzyme Commission data
                        if ec_dict != {}:

                            # set accumulate database list
                            data_dict['accum_databases'] = 'EC' if data_dict['accum_databases'] == '' else '{0}*EC'.format(data_dict['accum_databases'])

                            # for each Enzyme Commission annotation
                            for key6 in ec_dict.keys():

                                # get annotation values
                                ec_id = ec_dict[key6]['external_id']
                                xlib.Message.print('trace', 'EC -> id: {0}'.format(ec_id))

                                # accumulate values
                                data_dict['accum_ec_id'] = ec_id if data_dict['accum_ec_id'] == '' else '{0}*{1}'.format(data_dict['accum_ec_id'], ec_id)

                        # get KEGG dictionary with data corresponding to the Gene Onlology identification list
                        kegg_dict = xsqlite.get_cross_references_dict(conn, go_id_list, 'kegg')

                        # annotate using KEGG data
                        if kegg_dict != {}:

                            # set accumulate database list
                            data_dict['accum_databases'] = 'KEGG' if data_dict['accum_databases'] == '' else '{0}*KEGG'.format(data_dict['accum_databases'])

                            # for each KEGG annotation
                            for key7 in kegg_dict.keys():

                                # get annotation values
                                kegg_id = kegg_dict[key7]['external_id']
                                xlib.Message.print('trace', 'KEGG -> id: {0}'.format(kegg_id))

                                # accumulate values
                                data_dict['accum_kegg_id'] = kegg_id if data_dict['accum_kegg_id'] == '' else '{0}*{1}'.format(data_dict['accum_kegg_id'], kegg_id)

                        # get MetaCyc dictionary with data corresponding to the Gene Onlology identification list
                        metacyc_dict = xsqlite.get_cross_references_dict(conn, go_id_list, 'metacyc')

                        # annotate using MetaCyc data
                        if metacyc_dict != {}:

                            # set accumulate database list
                            data_dict['accum_databases'] = 'MetaCyc' if data_dict['accum_databases'] == '' else '{0}*MetaCyc'.format(data_dict['accum_databases'])

                            # for each MetaCyc annotation
                            for key8 in metacyc_dict.keys():

                                # get annotation values
                                metacyc_id = metacyc_dict[key8]['external_id']
                                xlib.Message.print('trace', 'MetaCyc -> id: {0}'.format(metacyc_id))

                                # accumulate values
                                data_dict['accum_metacyc_id'] = metacyc_id if data_dict['accum_metacyc_id'] == '' else '{0}*{1}'.format(data_dict['accum_metacyc_id'], metacyc_id)

                    # if there are annotation data for the hsp, write in annotation file
                    if is_hsp_annotated:
                        xlib.write_annotation_record(annotation_file_id, type, data_dict)
                        written_annotation_counter += 1

            # if there are not annotation data to the sequence identification, write in non-annotated sequence file
            if not is_seq_annotated:
                non_annotated_seq_counter += 1
                nonann_seq_file_id.write(record)

            # read the next record
            record = seq_file_id.readline()

        else:

            # control the FASTA format
            raise xlib.ProgramException('F005', seq_file, 'FASTA')

        # while there are records and they are sequence
        while record != '' and not record.startswith('>'):

            # write the sequence record in file with non-annotated sequences
            if not is_seq_annotated:
                nonann_seq_file_id.write(record)

            # read the next record
            record = seq_file_id.readline()

        # add 1 to sequence counter
        seq_counter += 1
        xlib.Message.print('verbose', '\rSequences... {0:8d} sequences'.format(seq_counter))

    xlib.Message.print('verbose', '\n')
    xlib.Message.print('info', 'There are {0} sequences; {1} were not annotated.'.format(seq_counter, non_annotated_seq_counter))

    # close files
    seq_file_id.close()
    nonann_seq_file_id.close()

#-------------------------------------------------------------------------------

def annotate_sequences_refseq(conn, dataset_id, seq_file, id_relationship_dict, annotation_file, nonann_seq_file, type):
    '''
    '''

    # get species dictionary
    species_dict = xsqlite.get_species_dict(conn)

    # open the sequence file
    if seq_file.endswith('.gz'):
        try:
            seq_file_id = gzip.open(seq_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', seq_file)
    else:
        try:
            seq_file_id = open(seq_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', seq_file)

    # open the annotation file
    if annotation_file.endswith('.gz'):
        try:
            annotation_file_id = gzip.open(annotation_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', annotation_file)
    else:
        try:
            annotation_file_id = open(annotation_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', annotation_file)

    # open the file with non-annotated sequences
    if nonann_seq_file.endswith('.gz'):
        try:
            nonann_seq_file_id = gzip.open(nonann_seq_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', nonann_seq_file)
    else:
        try:
            nonann_seq_file_id = open(nonann_seq_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', nonann_seq_file)

    # initialize the counters
    seq_counter = 0
    non_annotated_seq_counter = 0
    written_annotation_counter = 0

    # write header record of the annotation file
    xlib.write_annotation_header(annotation_file_id, type)
    written_annotation_counter += 1

    # read the first record
    record = seq_file_id.readline()

    # while there are records
    while record != '':

        # process the header record 
        if record.startswith('>'):

            # get the sequence id 
            new_seq_id = record[1:].strip()
            if id_relationship_dict == {}:
                old_seq_id = new_seq_id
            else:
                try:
                    old_seq_id = id_relationship_dict[new_seq_id]
                except Exception as e:
                    raise xlib.ProgramException('L008', new_seq_id)
            xlib.Message.print('trace', 'new_seq_id: {0} - old_seq_id: {1}'. format(new_seq_id, old_seq_id))

            # initialize the sequence annotation control variable
            is_seq_annotated = False

            # find the BLAST dictionary with data corresponding to the sequence identification
            blast_dict = xsqlite.get_blast_dict(conn, dataset_id, new_seq_id)
            
            # annotate the sequence for each hit-hsp if the dictionary has data
            if blast_dict != {}:
                for key in blast_dict.keys():

                    xlib.Message.print('trace', 'key: {0}'. format(key))

                    # initialize the hsp annotation control variable
                    is_hsp_annotated = False

                    # initialize data dictionary
                    data_dict = {}
                    data_dict['seq_id'] = old_seq_id

                    # asign iteration-hit-hsp values
                    data_dict['iteration_iter_num'] = blast_dict[key]['iteration_iter_num']
                    data_dict['hit_num'] = blast_dict[key]['hit_num']
                    data_dict['hit_id'] = blast_dict[key]['hit_id']
                    data_dict['hit_def'] = blast_dict[key]['hit_def']
                    data_dict['hit_accession'] = blast_dict[key]['hit_accession']
                    data_dict['hsp_num'] = blast_dict[key]['hsp_num']
                    data_dict['hsp_evalue'] = blast_dict[key]['hsp_evalue']
                    data_dict['hsp_identity'] = blast_dict[key]['hsp_identity']
                    data_dict['hsp_positive'] = blast_dict[key]['hsp_positive']
                    data_dict['hsp_gaps'] = blast_dict[key]['hsp_gaps']
                    data_dict['hsp_align_len'] = blast_dict[key]['hsp_align_len']
                    data_dict['hsp_qseq'] = blast_dict[key]['hsp_qseq']
                    xlib.Message.print('trace', 'iteration_iter_num: {0}'.format(data_dict['iteration_iter_num']))
                    xlib.Message.print('trace', 'hit_num: {0} - hit_id: {1} - hit_def: {2} - hit_accession: {3}'.format(data_dict['hit_num'], data_dict['hit_id'], data_dict['hit_def'], data_dict['hit_accession']))
                    xlib.Message.print('trace', 'hsp_num: {0} - hsp_evalue:{1} - hsp_identity: {2} - hsp_positive: {3} - hsp_gaps: {4} - hsp_align_len: {5}'.format(data_dict['hsp_num'], data_dict['hsp_evalue'], data_dict['hsp_identity'], data_dict['hsp_positive'], data_dict['hsp_gaps'], data_dict['hsp_align_len']))
                    xlib.Message.print('trace', 'hsp_qseq: {0}'.format(data_dict['hsp_qseq']))

                    # get the protein accession value, description and species name
                    # case 1:
                    # "hit_id" format: ref|protein_accession.version|
                    # "hit_def" format: desc [species_name]
                    pos1 = data_dict['hit_id'].find('|')
                    if data_dict['hit_id'] == 'ref':
                        # get protein accession value
                        pos2 = data_dict['hit_id'].find('|', pos1+1)
                        data_dict['protein_accession'] = data_dict['hit_id'][pos1+1:pos2].strip()
                        # get the description and species name
                        pos3 = data_dict['hit_def'].find('[')
                        pos4 = data_dict['hit_def'].find(']')
                        data_dict['desc'] = data_dict['hit_def'][:pos3].strip()
                        data_dict['species'] = data_dict['hit_def'][pos3+1:pos4].strip().capitalize()
                    # case 2:
                    # "hit_def" format: protein_accession.version desc [species_name]
                    else:
                        # get protein accession value
                        pos5 = data_dict['hit_def'].find(' ')
                        data_dict['protein_accession'] = data_dict['hit_def'][:pos5].strip()
                        # get the description and species name
                        pos6 = data_dict['hit_def'][pos5:].find('[')
                        pos7 = data_dict['hit_def'][pos5:].find(']')
                        data_dict['desc'] = data_dict['hit_def'][pos5+1:pos5+1+pos6].strip()
                        data_dict['species'] = data_dict['hit_def'][pos5+1+pos6+1:pos5+1+pos7].strip().capitalize()

                    # get the protein accession value, description, species name and taxonomy data
                    (species_dict, family_name, phylum_name, kingdom_name, superkingdom_name) = xlib.get_species_data(conn, species_dict, data_dict['species'])
                    data_dict['family'] = family_name
                    data_dict['phylum'] = phylum_name
                    data_dict['kingdom'] = kingdom_name
                    data_dict['superkingdom'] = superkingdom_name

                    # get gene2refseq dictionary with data corresponding to the "hit_id" value (gene identification)
                    # -- gene2refseq_dict = xsqlite.get_gene2refseq_dict(conn, data_dict['protein_accession'])
                    gene2refseq_dict = xsqlite.get_gene2refseq_dict(conn, data_dict['protein_accession'])

                    # annotate using gene2refseq data
                    if gene2refseq_dict != {}:

                        # set the annotation control variables
                        is_seq_annotated = True
                        is_hsp_annotated = True

                        # initialize Gene values
                        data_dict['gene_id'] = ''
                        data_dict['status'] = ''
                        data_dict['rna_nucleotide_accession'] = ''
                        data_dict['genomic_nucleotide_accession'] = ''
                        data_dict['gene_symbol'] = ''

                        # initialize accumulate annotation values
                        data_dict['accum_databases'] = 'RefSeqPlant'
                        data_dict['accum_go_id'] = ''
                        data_dict['accum_evidence'] = ''
                        data_dict['accum_go_term'] = ''
                        data_dict['accum_category'] = ''
                        data_dict['accum_interpro_id'] = ''
                        data_dict['accum_interpro_desc'] = ''
                        data_dict['accum_ec_id'] = ''
                        data_dict['accum_kegg_id'] = ''
                        data_dict['accum_metacyc_id'] = ''

                        # for each gene2refseq annotation
                        for key1 in gene2refseq_dict.keys():

                            # asign annotation values
                            gene_id = gene2refseq_dict[key1]['gene_id']
                            data_dict['gene_id'] = gene_id if data_dict['gene_id'] == '' else '{0}*{1}'.format(data_dict['gene_id'], gene_id)
                            data_dict['status'] = gene2refseq_dict[key1]['status'] if data_dict['status'] == '' else '{0}*{1}'.format(data_dict['status'], gene2refseq_dict[key1]['status'])
                            data_dict['rna_nucleotide_accession'] = gene2refseq_dict[key1]['rna_nucleotide_accession'] if data_dict['rna_nucleotide_accession'] == '' else '{0}*{1}'.format(data_dict['rna_nucleotide_accession'], gene2refseq_dict[key1]['rna_nucleotide_accession'])
                            data_dict['genomic_nucleotide_accession'] = gene2refseq_dict[key1]['genomic_nucleotide_accession'] if data_dict['genomic_nucleotide_accession'] == '' else '{0}*{1}'.format(data_dict['genomic_nucleotide_accession'], gene2refseq_dict[key1]['genomic_nucleotide_accession'])
                            data_dict['gene_symbol'] = gene2refseq_dict[key1]['gene_symbol'] if data_dict['gene_symbol'] == '' else '{0}*{1}'.format(data_dict['gene_symbol'], gene2refseq_dict[key1]['gene_symbol'])
                            xlib.Message.print('trace', 'gene2refseq -> gene_id: {0} - protein_accession: {1}'.format(gene_id, data_dict['protein_accession']))

                            # get gene2go dictionary with data corresponding to the "gene_id"
                            gene2go_dict = xsqlite.get_gene2go_dict(conn, gene_id)

                            # if there are not data for the "gene_id" in gene2go
                            if gene2go_dict != {}:

                                # set accumulate database list
                                data_dict['accum_databases'] = 'GO' if data_dict['accum_databases'] == '' else '{0}*GO'.format(data_dict['accum_databases'])

                                # for each Gene Ontology annotation
                                for key2 in gene2go_dict.keys():

                                    # asign annotation values
                                    data_dict['accum_go_id'] = gene2go_dict[key2]['go_id'] if data_dict['accum_go_id'] == '' else '{0}*{1}'.format(data_dict['accum_go_id'], gene2go_dict[key2]['go_id'])
                                    data_dict['accum_evidence'] = gene2go_dict[key2]['evidence'] if data_dict['accum_evidence'] == '' else '{0}*{1}'.format(data_dict['accum_evidence'], gene2go_dict[key2]['evidence'])
                                    data_dict['accum_go_term'] = gene2go_dict[key2]['go_term'] if data_dict['accum_go_term'] == '' else '{0}*{1}'.format(data_dict['accum_go_term'], gene2go_dict[key2]['go_term'])
                                    data_dict['accum_category'] = gene2go_dict[key2]['category'] if data_dict['accum_category'] == '' else '{0}*{1}'.format(data_dict['accum_category'], gene2go_dict[key2]['category'])
                                    xlib.Message.print('trace', 'gene2go -> id: {0} - evidence: {1} - desc: {2} - category: {3}'.format(data_dict['accum_go_id'], data_dict['accum_evidence'], data_dict['accum_go_term'], data_dict['accum_category']))

                            # get InterPro, Enzyme Commission, KEGG and MetaCyc data from Gene Onlology identification
                            if data_dict['accum_go_id'] != '':

                                # get the Gene Ontology identification list
                                go_id_list = data_dict['accum_go_id'].split('*')

                                # get InterPro dictionary with data corresponding to the Gene Onlology identification list
                                interpro_dict = xsqlite.get_cross_references_dict(conn, go_id_list, 'interpro')

                                # annotate using InterPro data
                                if interpro_dict != {}:

                                    # set accumulate repository list
                                    data_dict['accum_databases'] = 'InterPro' if data_dict['accum_databases'] == '' else '{0}*InterPro'.format(data_dict['accum_databases'])

                                    # for each InterPro annotation
                                    for key3 in interpro_dict.keys():

                                        # get annotation values
                                        interpro_id = interpro_dict[key3]['external_id']
                                        interpro_desc = interpro_dict[key3]['external_desc']
                                        xlib.Message.print('trace', 'InterPro -> id: {0} - desc: {1}'.format(interpro_id, interpro_desc))

                                        # accumulate values
                                        data_dict['accum_interpro_id'] = interpro_id if data_dict['accum_interpro_id'] == '' else '{0}*{1}'.format(data_dict['accum_interpro_id'], interpro_id)
                                        data_dict['accum_interpro_desc'] = interpro_id if data_dict['accum_interpro_desc'] == '' else '{0}*{1}'.format(data_dict['accum_interpro_desc'], interpro_desc)

                                # get Enzyme Commission dictionary with data corresponding to the Gene Onlology identification list
                                ec_dict = xsqlite.get_cross_references_dict(conn, go_id_list, 'ec')

                                # annotate using Enzyme Commission data
                                if ec_dict != {}:

                                    # set accumulate repository list
                                    data_dict['accum_databases'] = 'EC' if data_dict['accum_databases'] == '' else '{0}*EC'.format(data_dict['accum_databases'])

                                    # for each Enzyme Commission annotation
                                    for key4 in ec_dict.keys():

                                        # get annotation values
                                        ec_id = ec_dict[key4]['external_id']
                                        xlib.Message.print('trace', 'EC -> id: {0}'.format(ec_id))

                                        # accumulate values
                                        data_dict['accum_ec_id'] = ec_id if data_dict['accum_ec_id'] == '' else '{0}*{1}'.format(data_dict['accum_ec_id'], ec_id)

                                # get KEGG dictionary with data corresponding to the Gene Onlology identification list
                                kegg_dict = xsqlite.get_cross_references_dict(conn, go_id_list, 'kegg')

                                # annotate using KEGG data
                                if kegg_dict != {}:

                                    # set accumulate repository list
                                    data_dict['accum_databases'] = 'KEGG' if data_dict['accum_databases'] == '' else '{0}*KEGG'.format(data_dict['accum_databases'])

                                    # for each KEGG annotation
                                    for key5 in kegg_dict.keys():

                                        # get annotation values
                                        kegg_id = kegg_dict[key5]['external_id']
                                        xlib.Message.print('trace', 'KEGG -> id: {0}'.format(kegg_id))

                                        # accumulate values
                                        data_dict['accum_kegg_id'] = kegg_id if data_dict['accum_kegg_id'] == '' else '{0}*{1}'.format(data_dict['accum_kegg_id'], kegg_id)

                                # get MetaCyc dictionary with data corresponding to the Gene Onlology identification list
                                metacyc_dict = xsqlite.get_cross_references_dict(conn, go_id_list, 'metacyc')

                                # annotate using MetaCyc data
                                if metacyc_dict != {}:

                                    # set accumulate repository list
                                    data_dict['accum_databases'] = 'MetaCyc' if data_dict['accum_databases'] == '' else '{0}*MetaCyc'.format(data_dict['accum_databases'])

                                    # for each MetaCyc annotation
                                    for key6 in metacyc_dict.keys():

                                        # get annotation values
                                        metacyc_id = metacyc_dict[key6]['external_id']
                                        xlib.Message.print('trace', 'MetaCyc -> id: {0}'.format(metacyc_id))

                                        # accumulate values
                                        data_dict['accum_metacyc_id'] = metacyc_id if data_dict['accum_metacyc_id'] == '' else '{0}*{1}'.format(data_dict['accum_metacyc_id'], metacyc_id)

                    # write in annotation file
                    if is_hsp_annotated:
                        xlib.write_annotation_record(annotation_file_id, type, data_dict)
                        written_annotation_counter += 1
            
            # write in file with non-annotated sequences
            if not is_seq_annotated:
                non_annotated_seq_counter += 1
                nonann_seq_file_id.write(record)

            # read the next record
            record = seq_file_id.readline()

        else:

            # control the FASTA format
            raise xlib.ProgramException('F005', seq_file, 'FASTA')

        # while there are records and they are sequence
        while record != '' and not record.startswith('>'):

            # write the sequence record in file with non-annotated sequences
            if not is_seq_annotated:
                nonann_seq_file_id.write(record)

            # read the next record
            record = seq_file_id.readline()

        # add 1 to sequence counter
        seq_counter += 1
        xlib.Message.print('verbose', '\rSequences... {0:8d} sequences'.format(seq_counter))

    # print summary
    xlib.Message.print('verbose', '\n')
    xlib.Message.print('info', 'There are {0} sequences; {1} were not annotated.'.format(seq_counter, non_annotated_seq_counter))

    # close files
    seq_file_id.close()
    nonann_seq_file_id.close()

#-------------------------------------------------------------------------------

def annotate_sequences_nx(conn, dataset_id, seq_file, id_relationship_dict, annotation_file, nonann_seq_file, type):
    '''
    '''

    # get species dictionary
    species_dict = xsqlite.get_species_dict(conn)

    # open the sequence file
    if seq_file.endswith('.gz'):
        try:
            seq_file_id = gzip.open(seq_file, mode='rt', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F002', seq_file)
    else:
        try:
            seq_file_id = open(seq_file, mode='r', encoding='iso-8859-1')
        except Exception as e:
            raise xlib.ProgramException('F001', seq_file)

    # open the annotation file
    if annotation_file.endswith('.gz'):
        try:
            annotation_file_id = gzip.open(annotation_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', annotation_file)
    else:
        try:
            annotation_file_id = open(annotation_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', annotation_file)

    # open the file with non-annotated sequences
    if nonann_seq_file.endswith('.gz'):
        try:
            nonann_seq_file_id = gzip.open(nonann_seq_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', nonann_seq_file)
    else:
        try:
            nonann_seq_file_id = open(nonann_seq_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', nonann_seq_file)

    # initialize the counters
    seq_counter = 0
    non_annotated_seq_counter = 0
    written_annotation_counter = 0

    # write header record of the annotation file
    xlib.write_annotation_header(annotation_file_id, type)
    written_annotation_counter += 1

    # read the first record
    record = seq_file_id.readline()

    # while there are records
    while record != '':

        # process the header record 
        if record.startswith('>'):

            # get the sequence id 
            new_seq_id = record[1:].strip()
            if id_relationship_dict == {}:
                old_seq_id = new_seq_id
            else:
                try:
                    old_seq_id = id_relationship_dict[new_seq_id]
                except Exception as e:
                    raise xlib.ProgramException('L008', new_seq_id)
            xlib.Message.print('trace', 'new_seq_id: {0} - old_seq_id: {1}'. format(new_seq_id, old_seq_id))

            # initialize the sequence annotation control variable
            is_seq_annotated = False

            # find the BLAST dictionary with data corresponding to the sequence identification
            blast_dict = xsqlite.get_blast_dict(conn, dataset_id, new_seq_id)
            
            # annotate the sequence for each hit-hsp if the dictionary has data
            if blast_dict != {}:
                for key in blast_dict.keys():

                    xlib.Message.print('trace', 'key: {0}'. format(key))
 
                    # set annotation control variable
                    is_seq_annotated = True

                    # initialize data dictionary
                    data_dict = {}
                    data_dict['seq_id'] = old_seq_id

                    # asign iteration-hit-hsp values
                    data_dict['iteration_iter_num'] = blast_dict[key]['iteration_iter_num']
                    data_dict['hit_num'] = blast_dict[key]['hit_num']
                    data_dict['hit_id'] = blast_dict[key]['hit_id']
                    data_dict['hsp_num'] = blast_dict[key]['hsp_num']
                    data_dict['hsp_evalue'] = blast_dict[key]['hsp_evalue']
                    data_dict['hsp_identity'] = blast_dict[key]['hsp_identity']
                    data_dict['hsp_positive'] = blast_dict[key]['hsp_positive']
                    data_dict['hsp_gaps'] = blast_dict[key]['hsp_gaps']
                    data_dict['hsp_align_len'] = blast_dict[key]['hsp_align_len']
                    data_dict['hsp_qseq'] = blast_dict[key]['hsp_qseq']
                    xlib.Message.print('trace', 'iteration_iter_num: {0} - hit_num: {1} - hit_id: {2}'.format(data_dict['iteration_iter_num'], data_dict['hit_num'], data_dict['hit_id']))
                    xlib.Message.print('trace', 'hsp_num: {0} - hsp_evalue:{1} - hsp_identity: {2} - hsp_positive: {3} - hsp_gaps: {4} - hsp_align_len: {5}'.format(data_dict['hsp_num'], data_dict['hsp_evalue'], data_dict['hsp_identity'], data_dict['hsp_positive'], data_dict['hsp_gaps'], data_dict['hsp_align_len']))
                    xlib.Message.print('trace', 'hsp_qseq: {0}'.format(data_dict['hsp_qseq']))

                    # get description and species name its taxonomy data
                    hit_def = blast_dict[key]['hit_def']
                    if type == 'NT':
                        # "hit_def" format in NT: desc (the species name is the first two words of desc)
                        data_dict['desc'] = hit_def
                        hit_def = hit_def.strip().replace('PREDICTED: ', '').replace(':', '').replace('/', ' ').replace('.', ' ')
                        pos1 = hit_def.find(' ')
                        pos2 = hit_def[pos1+1:].find(' ')
                        data_dict['species'] = hit_def[:pos1+pos2+1].strip().capitalize()
                    elif type == 'NR':
                        # "hit_def" format in NR: desc [species_name]
                        hit_def = blast_dict[key]['hit_def']
                        pos1 = hit_def.find('[')
                        pos2 = hit_def.find(']')
                        data_dict['desc'] = hit_def[:pos1].strip()
                        data_dict['species'] = hit_def[pos1+1:pos2].strip().capitalize()

                    # get taxonomy data
                    if data_dict['species'].find('virus') != -1:
                        data_dict['family'] = 'virus'
                        data_dict['phylum'] = 'virus'
                        data_dict['kingdom'] = 'virus'
                        data_dict['superkingdom'] = 'virus'
                    else:
                        (species_dict, family_name, phylum_name, kingdom_name, superkingdom_name) = xlib.get_species_data(conn, species_dict, data_dict['species'])
                        data_dict['family'] = family_name
                        data_dict['phylum'] = phylum_name
                        data_dict['kingdom'] = kingdom_name
                        data_dict['superkingdom'] = superkingdom_name

                    # initialize accumulate annotation values
                    if type == 'NT':
                        data_dict['accum_databases'] = 'nt'
                    elif type == 'NR':
                        data_dict['accum_databases'] = 'nr'

                    # write in annotation file
                    xlib.write_annotation_record(annotation_file_id, type, data_dict)
                    written_annotation_counter += 1
          
            # write in file with non-annotated sequneces
            else:
                non_annotated_seq_counter += 1
                nonann_seq_file_id.write(record)

            # read the next record
            record = seq_file_id.readline()

        else:

            # control the FASTA format
            raise xlib.ProgramException('F005', seq_file, 'FASTA')

        # while there are records and they are sequence
        while record != '' and not record.startswith('>'):

            # write the sequence record in file with non-annotated sequences
            if not is_seq_annotated:
                nonann_seq_file_id.write(record)

            # read the next record
            record = seq_file_id.readline()

        # add 1 to sequence counter
        seq_counter += 1
        xlib.Message.print('verbose', '\rSequences... {0:8d} sequences'.format(seq_counter))

    # print summary
    xlib.Message.print('verbose', '\n')
    xlib.Message.print('info', 'There are {0} sequences; {1} were not annotated.'.format(seq_counter, non_annotated_seq_counter))

    # close files
    seq_file_id.close()
    nonann_seq_file_id.close()

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
