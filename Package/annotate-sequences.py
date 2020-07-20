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
    if not xsqlite.is_dataset_id_found(conn, args.dataset_id):
        raise xlib.ProgramException('L001', args.dataset_id)

    # get the TOA-transcriptome identification relationship dictionary
    toa_transcriptome_relationship_dict = xlib.get_id_relationship_dict(args.toa_transcriptome_relationship_file)

    # get the TOA-TransDecoder identification relationship dictionary
    if args.toa_transdecoder_relationship_file == 'NONE':
        toa_transdecoder_relationship_dict = {}
    else:
        toa_transdecoder_relationship_dict = xlib.get_id_relationship_dict(args.toa_transdecoder_relationship_file)

    # annotate sequences depending of the dataset identification
    if args.dataset_id in ['gymno_01', 'dicots_04', 'monocots_04']: 
        annotate_sequences_plaza(conn, args.dataset_id, args.aligner_tool, args.seq_file, toa_transcriptome_relationship_dict, toa_transdecoder_relationship_dict, args.annotation_file, args.nonann_seq_file, type='PLAZA')
    elif args.dataset_id in ['refseq_plant']: 
        annotate_sequences_refseq(conn, args.dataset_id, args.aligner_tool, args.seq_file, toa_transcriptome_relationship_dict, toa_transdecoder_relationship_dict, args.annotation_file, args.nonann_seq_file, type='REFSEQ')
    elif args.dataset_id in ['nt']: 
        annotate_sequences_nx(conn, args.dataset_id, args.aligner_tool, args.seq_file, toa_transcriptome_relationship_dict, toa_transdecoder_relationship_dict, args.annotation_file, args.contamination_annotation_file, args.nonann_seq_file, type='NT')
    elif args.dataset_id in ['nr']: 
        annotate_sequences_nx(conn, args.dataset_id, args.aligner_tool, args.seq_file, toa_transcriptome_relationship_dict, toa_transdecoder_relationship_dict, args.annotation_file, args.contamination_annotation_file, args.nonann_seq_file, type='NR')

    # close connection to TOA database
    conn.close()

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program annotates sequences (nucleotides or proteins) using the TOA database.'
    text = f'{xlib.get_long_project_name()} v{xlib.get_project_version()} - {os.path.basename(__file__)}\n\n{description}\n'
    usage = f'\r{text.ljust(len("usage:"))}\nUsage: {os.path.basename(__file__)} arguments'
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--db', dest='toa_database', help='Path of the TOA database (mandatory).')
    parser.add_argument('--dataset', dest='dataset_id', help='Dataset identification (mandatory).')
    parser.add_argument('--aligner', dest='aligner_tool', help=f'Aligner tool: {xlib.get_alignment_tool_code_list_text()} (mandatory).')
    parser.add_argument('--seqs', dest='seq_file', help='Path of the file with sequences to be annotated (mandatory).')
    parser.add_argument('--relationships', dest='toa_transcriptome_relationship_file', help='CSV file path with TOA-transcriptome identification relationships  (mandatory)')
    parser.add_argument('--relationships2', dest='toa_transdecoder_relationship_file', help='CSV file path with TOA-TransDecoder identification relationships or NONE (mandatory)')
    parser.add_argument('--annotation', dest='annotation_file', help='Path of annotation file in CSV format (mandatory).')
    parser.add_argument('--annotation2', dest='contamination_annotation_file', help='Path of contamination annotation file in CSV format when NCBI NT or NR; else: NONE.')
    parser.add_argument('--nonann', dest='nonann_seq_file', help='Path of file with non-annotated sequences (mandatory).')
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

    # check "toa_database"
    if args.toa_database is None:
        xlib.Message.print('error', '*** The TOA database is not indicated in the input arguments.')
        OK = False

    # check "dataset_id"
    if args.dataset_id is None:
        xlib.Message.print('error', '*** The dataset identification is not indicated in the input arguments.')
        OK = False
    else:
        args.dataset_id = args.dataset_id.lower()

    # check "aligner_tool"
    if args.aligner_tool is None:
        xlib.Message.print('error', '*** The aligner tool is not indicated in the input arguments.')
    elif not xlib.check_code(args.aligner_tool, xlib.get_alignment_tool_code_list() + ['SAVE1'], case_sensitive=False):
        xlib.Message.print('error', f'*** The aligner tool has to be {xlib.get_alignment_tool_code_list_text()}.')
        OK = False
    else:
        args.aligner_tool = args.aligner_tool.upper()

    # check "seq_file"
    if args.seq_file is None:
        xlib.Message.print('error', '*** The file with sequences to be annotated is not indicated in the input arguments.')
        OK = False
    elif not os.path.isfile(args.seq_file):
        xlib.Message.print('error', f'*** The file {args.seq_file} does not exist.')
        OK = False

    # check "toa_transcriptome_relationship_file"
    if args.toa_transcriptome_relationship_file is None:
        xlib.Message.print('error', '*** The file with TOA-transcriptome identification relationships.')
        OK = False
    elif not os.path.isfile(args.toa_transcriptome_relationship_file):
        xlib.Message.print('error', f'*** The file {args.toa_transcriptome_relationship_file} does not exist.')
        OK = False

    # check "toa_transdecoder_relationship_file"
    if args.toa_transdecoder_relationship_file is None:
        xlib.Message.print('error', '*** The file path with TOA-TransDecoder identification relationships.')
    elif args.toa_transdecoder_relationship_file.upper() == 'NONE':
        args.toa_transdecoder_relationship_file = args.toa_transdecoder_relationship_file.upper()
    elif not os.path.isfile(args.toa_transdecoder_relationship_file):
        xlib.Message.print('error', f'*** The file {args.toa_transdecoder_relationship_file} does not exist.')
        OK = False

    # check "annotation_file"
    if args.annotation_file is None:
        xlib.Message.print('error', '*** The annotation file is not indicated in the input arguments.')
        OK = False

    # check "contamination_annotation_file"
    if args.contamination_annotation_file is None:
        args.contamination_annotation_file = 'NONE'
    elif args.contamination_annotation_file.upper() == 'NONE':
        args.contamination_annotation_file = args.contamination_annotation_file.upper()

    # check "nonann_seq_file"
    if args.nonann_seq_file is None:
        xlib.Message.print('error', '*** The file with non-annotated sequences is not indicated in the input arguments.')
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

def annotate_sequences_plaza(conn, dataset_id, aligner_tool, seq_file, toa_transcriptome_relationship_dict, toa_transdecoder_relationship_dict, annotation_file, nonann_seq_file, type):
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
    total_seq_counter = 0
    non_annotated_seq_counter = 0

    # write header record of the annotation file
    xlib.write_annotation_header(annotation_file_id, type)

    # read the first record
    record = seq_file_id.readline()

    # while there are records
    while record != '':

        # process the header record 
        if record.startswith('>'):

            # get the sequence identifiers
            x_seq_id = record[1:].strip()
            (transcript_seq_id, nt_seq_id, aa_seq_id) = xlib.get_seq_ids(x_seq_id, toa_transcriptome_relationship_dict, toa_transdecoder_relationship_dict)
            xlib.Message.print('trace', f'transcript_seq_id: {transcript_seq_id} - nt_seq_id: {nt_seq_id} - aa_seq_id: {aa_seq_id}')

            # initialize the sequence annotation control variable
            is_seq_annotated = False

            # find the BLAST dictionary with data corresponding to the sequence identification
            blast_dict = xsqlite.get_blast_dict(conn, dataset_id, x_seq_id)
            
            # annotate the sequence for each hit-hsp if the dictionary has data
            if blast_dict != {}:
                for key1 in blast_dict.keys():

                    xlib.Message.print('trace', f'key: {key1}')

                    # initialize the hsp annotation control variable
                    is_hsp_annotated = False

                    # initialize data dictionary
                    data_dict = {}
                    data_dict['seq_id'] = transcript_seq_id
                    data_dict['nt_seq_id'] = nt_seq_id
                    data_dict['aa_seq_id'] = aa_seq_id

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
                    xlib.Message.print('trace', f'iteration_iter_num: {data_dict["iteration_iter_num"]}')
                    xlib.Message.print('trace', f'hit_num: {data_dict["hit_num"]} - hit_def: {data_dict["hit_def"]} - hit_accession: {data_dict["hit_accession"]}')
                    xlib.Message.print('trace', f'hsp_num: {data_dict["hsp_num"]} - hsp_evalue:{data_dict["hsp_evalue"]} - hsp_identity: {data_dict["hsp_identity"]} - hsp_positive: {data_dict["hsp_positive"]} - hsp_gaps: {data_dict["hsp_gaps"]} - hsp_align_len: {data_dict["hsp_align_len"]}')
                    xlib.Message.print('trace', f'hsp_qseq: {data_dict["hsp_qseq"]}')

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
                    xlib.Message.print('trace', f'plaza_species_id: {description_plaza_species_id} ({data_dict["species"]})')

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
                        data_dict['accum_databases'] = 'GO' if data_dict['accum_databases'] == '' else f'{data_dict["accum_databases"]}*GO'

                        # get the species name and taxonomy data and its taxonomy data
                        if data_dict['species'] == xlib.get_na():
                            go_plaza_species_id = go_dict[0]['plaza_species_id']
                            data_dict['species'] = species_dict.get(go_plaza_species_id, {}).get('species_name', xlib.get_na())
                            data_dict['family'] = species_dict.get(go_plaza_species_id, {}).get('family_name', xlib.get_na())
                            data_dict['phylum'] = species_dict.get(go_plaza_species_id, {}).get('phylum_name', xlib.get_na())
                            data_dict['kingdom'] = species_dict.get(go_plaza_species_id, {}).get('kingdom_name', xlib.get_na())
                            data_dict['superkingdom'] = species_dict.get(go_plaza_species_id, {}).get('superkingdom_name', xlib.get_na())
                            xlib.Message.print('trace', f'GO -> plaza_species_id: {go_plaza_species_id} ({data_dict["species"]})')

                        # for each Gene Ontology annotation
                        for key2 in go_dict.keys():

                            # get annotation values
                            go_id = go_dict[key2]['go_id']
                            go_desc = go_dict[key2]['desc']
                            xlib.Message.print('trace', f'GO -> id: {go_id} - desc: {go_desc}')

                            # accumulate values
                            data_dict['accum_go_id'] = go_id if data_dict['accum_go_id'] == '' else f'{data_dict["accum_go_id"]}*{go_id}'
                            data_dict['accum_go_desc'] = go_desc if data_dict['accum_go_desc'] == '' else f'{data_dict["accum_go_desc"]}*{go_desc}'

                    # get InterPro dictionary with data corresponding to the gene identification
                    interpro_dict = xsqlite.get_interpro_dict(conn, dataset_id, gene_id)

                    # annotate using Interpro data
                    if interpro_dict != {}:

                        # set the annotation control variables
                        is_seq_annotated = True
                        is_hsp_annotated = True

                        # set accumulate database list
                        data_dict['accum_databases'] = 'InterPro' if data_dict['accum_databases'] == '' else f'{data_dict["accum_databases"]}*InterPro'

                        # get the species name
                        if data_dict['species'] == xlib.get_na():
                            interpro_plaza_species_id = interpro_dict[0]['plaza_species_id']
                            data_dict['species'] = species_dict.get(interpro_plaza_species_id, {}).get('species_name', xlib.get_na())
                            data_dict['family'] = species_dict.get(interpro_plaza_species_id, {}).get('family_name', xlib.get_na())
                            data_dict['phylum'] = species_dict.get(interpro_plaza_species_id, {}).get('phylum_name', xlib.get_na())
                            data_dict['kingdom'] = species_dict.get(interpro_plaza_species_id, {}).get('kingdom_name', xlib.get_na())
                            data_dict['superkingdom'] = species_dict.get(interpro_plaza_species_id, {}).get('superkingdom_name', xlib.get_na())
                            xlib.Message.print('trace', f'INTERPRO -> plaza_species_id: {interpro_plaza_species_id} ({data_dict["species"]})')

                        # for each Interpro annotation
                        for key3 in interpro_dict.keys():

                            # get annotation values
                            interpro_id = interpro_dict[key3]['motif_id']
                            interpro_desc = interpro_dict[key3]['desc']
                            xlib.Message.print('trace', f'InterPro -> id: {interpro_id} - desc: {interpro_desc}')

                            # accumulate values
                            data_dict['accum_interpro_id'] = interpro_id if data_dict['accum_interpro_id'] == '' else f'{data_dict["accum_interpro_id"]}*{interpro_id}'
                            data_dict['accum_interpro_desc'] = interpro_desc if data_dict['accum_interpro_desc'] == '' else f'{data_dict["accum_interpro_desc"]}*{interpro_desc}'

                        # if there are not Gene Ontology data
                        if go_dict == {}:

                            # get data from InterPro interpro2go
                            interpro2go_dict = xsqlite.get_interpro2go_dict(conn, interpro_id)

                            # annotate using Interpro interpro2go
                            if interpro2go_dict != {}:

                                # set accumulate database list
                                data_dict['accum_databases'] = f'{data_dict["accum_databases"]}*GO2'

                                # for each interpro2go annotation
                                for key4 in interpro2go_dict.keys():

                                    # get annotation values
                                    go_id = interpro2go_dict[key4]['go_id']
                                    go_desc = interpro2go_dict[key4]['go_desc']
                                    xlib.Message.print('trace', f'GO2 -> id: {go_id} - desc: {go_desc}')

                                    # accumulate values
                                    data_dict['accum_go_id'] = go_id if data_dict['accum_go_id'] == '' else f'{data_dict["accum_go_id"]}*{go_id}'
                                    data_dict['accum_go_desc'] = go_desc if data_dict['accum_go_desc'] == '' else f'{data_dict["accum_go_desc"]}*{go_desc}'

                    # get Mapman dictionary with data corresponding to the gene identification
                    mapman_dict = xsqlite.get_mapman_dict(conn, dataset_id, gene_id)

                    # annotate using Mapman data
                    if mapman_dict != {}:

                        # set the annotation control variables
                        is_seq_annotated = True
                        is_hsp_annotated = True

                        # set accumulate database list
                        data_dict['accum_databases'] = 'MapMan' if data_dict['accum_databases'] == '' else f'{data_dict["accum_databases"]}*MapMan'

                        # get the species name and taxonomy data and its taxonomy data
                        if data_dict['species'] == xlib.get_na():
                            mapman_plaza_species_id = mapman_dict[0]['plaza_species_id']
                            data_dict['species'] = species_dict.get(mapman_plaza_species_id, {}).get('species_name', xlib.get_na())
                            data_dict['family'] = species_dict.get(mapman_plaza_species_id, {}).get('family_name', xlib.get_na())
                            data_dict['phylum'] = species_dict.get(mapman_plaza_species_id, {}).get('phylum_name', xlib.get_na())
                            data_dict['kingdom'] = species_dict.get(mapman_plaza_species_id, {}).get('kingdom_name', xlib.get_na())
                            data_dict['superkingdom'] = species_dict.get(mapman_plaza_species_id, {}).get('superkingdom_name', xlib.get_na())
                            xlib.Message.print('trace', f'MAPMAN -> plaza_species_id: {mapman_plaza_species_id} ({data_dict["species"]})')

                        # for each Mapman annotation
                        for key5 in mapman_dict.keys():

                            # get annotation values
                            mapman_id = mapman_dict[key5]['mapman_id']
                            mapman_desc = mapman_dict[key5]['desc']
                            xlib.Message.print('trace', f'MAPMAN -> id: {mapman_id} - desc: {mapman_desc}')

                            # accumulate values
                            data_dict['accum_mapman_id'] = mapman_id if data_dict['accum_mapman_id'] == '' else f'{data_dict["accum_mapman_id"]}*{mapman_id}'
                            data_dict['accum_mapman_desc'] = mapman_desc if data_dict['accum_mapman_desc'] == '' else f'{data_dict["accum_mapman_desc"]}*{mapman_desc}'

                    # get Enzyme Commission, KEGG and MetaCyc data from Gene Onlology identification
                    if data_dict['accum_go_id'] != '':

                        # get the Gene Ontology identification list
                        go_id_list = data_dict['accum_go_id'].split('*')

                        # get Enzyme Commission dictionary with data corresponding to the Gene Onlology identification list
                        ec_dict = xsqlite.get_cross_references_dict(conn, go_id_list, 'ec')

                        # annotate using Enzyme Commission data
                        if ec_dict != {}:

                            # set accumulate database list
                            data_dict['accum_databases'] = 'EC' if data_dict['accum_databases'] == '' else f'{data_dict["accum_databases"]}*EC'

                            # for each Enzyme Commission annotation
                            for key6 in ec_dict.keys():

                                # get annotation values
                                ec_id = ec_dict[key6]['external_id']
                                xlib.Message.print('trace', f'EC -> id: {ec_id}')

                                # accumulate values
                                data_dict['accum_ec_id'] = ec_id if data_dict['accum_ec_id'] == '' else f'{data_dict["accum_ec_id"]}*{ec_id}'

                        # get KEGG dictionary with data corresponding to the Gene Onlology identification list
                        kegg_dict = xsqlite.get_cross_references_dict(conn, go_id_list, 'kegg')

                        # annotate using KEGG data
                        if kegg_dict != {}:

                            # set accumulate database list
                            data_dict['accum_databases'] = 'KEGG' if data_dict['accum_databases'] == '' else f'{data_dict["accum_databases"]}*KEGG'

                            # for each KEGG annotation
                            for key7 in kegg_dict.keys():

                                # get annotation values
                                kegg_id = kegg_dict[key7]['external_id']
                                xlib.Message.print('trace', f'KEGG -> id: {kegg_id}')

                                # accumulate values
                                data_dict['accum_kegg_id'] = kegg_id if data_dict['accum_kegg_id'] == '' else f'{data_dict["accum_kegg_id"]}*{kegg_id}'

                        # get MetaCyc dictionary with data corresponding to the Gene Onlology identification list
                        metacyc_dict = xsqlite.get_cross_references_dict(conn, go_id_list, 'metacyc')

                        # annotate using MetaCyc data
                        if metacyc_dict != {}:

                            # set accumulate database list
                            data_dict['accum_databases'] = 'MetaCyc' if data_dict['accum_databases'] == '' else f'{data_dict["accum_databases"]}*MetaCyc'

                            # for each MetaCyc annotation
                            for key8 in metacyc_dict.keys():

                                # get annotation values
                                metacyc_id = metacyc_dict[key8]['external_id']
                                xlib.Message.print('trace', f'MetaCyc -> id: {metacyc_id}')

                                # accumulate values
                                data_dict['accum_metacyc_id'] = metacyc_id if data_dict['accum_metacyc_id'] == '' else f'{data_dict["accum_metacyc_id"]}*{metacyc_id}'

                    # if there are annotation data for the hsp, write in annotation file
                    if is_hsp_annotated:
                        xlib.write_annotation_record(annotation_file_id, type, data_dict)

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
        total_seq_counter += 1
        xlib.Message.print('verbose', f'\rProcessed sequences... {total_seq_counter}')

    xlib.Message.print('verbose', '\n')
    xlib.Message.print('info', f'Total seqs: {total_seq_counter} - Annotated seqs: {total_seq_counter - non_annotated_seq_counter} - Non-annotated seqs: {non_annotated_seq_counter}.')

    # close files
    seq_file_id.close()
    nonann_seq_file_id.close()

#-------------------------------------------------------------------------------

def annotate_sequences_refseq(conn, dataset_id, aligner_tool, seq_file, toa_transcriptome_relationship_dict, toa_transdecoder_relationship_dict, annotation_file, nonann_seq_file, type):
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
    total_seq_counter = 0
    non_annotated_seq_counter = 0

    # write header record of the annotation file
    xlib.write_annotation_header(annotation_file_id, type)

    # read the first record
    record = seq_file_id.readline()

    # while there are records
    while record != '':

        # process the header record 
        if record.startswith('>'):

            # get the sequence identifiers
            x_seq_id = record[1:].strip()
            (transcript_seq_id, nt_seq_id, aa_seq_id) = xlib.get_seq_ids(x_seq_id, toa_transcriptome_relationship_dict, toa_transdecoder_relationship_dict)
            xlib.Message.print('trace', f'transcript_seq_id: {transcript_seq_id} - nt_seq_id: {nt_seq_id} - aa_seq_id: {aa_seq_id}')

            # initialize the sequence annotation control variable
            is_seq_annotated = False

            # find the BLAST dictionary with data corresponding to the sequence identification
            blast_dict = xsqlite.get_blast_dict(conn, dataset_id, x_seq_id)
            
            # annotate the sequence for each hit-hsp if the dictionary has data
            if blast_dict != {}:
                for key in blast_dict.keys():

                    xlib.Message.print('trace', f'key: {key}')

                    # initialize the hsp annotation control variable
                    is_hsp_annotated = False

                    # initialize data dictionary
                    data_dict = {}
                    data_dict['seq_id'] = transcript_seq_id
                    data_dict['nt_seq_id'] = nt_seq_id
                    data_dict['aa_seq_id'] = aa_seq_id

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
                    xlib.Message.print('trace', f'iteration_iter_num: {data_dict["iteration_iter_num"]}')
                    xlib.Message.print('trace', f'hit_num: {data_dict["hit_num"]} - hit_id: {data_dict["hit_id"]} - hit_def: {data_dict["hit_def"]} - hit_accession: {data_dict["hit_accession"]}')
                    xlib.Message.print('trace', f'hsp_num: {data_dict["hsp_num"]} - hsp_evalue:{data_dict["hsp_evalue"]} - hsp_identity: {data_dict["hsp_identity"]} - hsp_positive: {data_dict["hsp_positive"]} - hsp_gaps: {data_dict["hsp_gaps"]} - hsp_align_len: {data_dict["hsp_align_len"]}')
                    xlib.Message.print('trace', f'hsp_qseq: {data_dict["hsp_qseq"]}')

                    # get the protein accession value, description and species name for aligner BLAST+
                    if aligner_tool == xlib.get_blastplus_name():
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
                            data_dict['desc'] = data_dict['hit_def'][pos5+1:pos5+1+pos6-1].strip()
                            data_dict['species'] = data_dict['hit_def'][pos5+pos6+1:pos5+1+pos7-1].strip().capitalize()

                    # get the protein accession value, description and species name for aligner DIAMOND
                    elif aligner_tool == xlib.get_diamond_name():
                        # "hit_def" format: desc [species_name]
                        # get protein accession value
                        data_dict['protein_accession'] = data_dict['hit_accession']
                        # get the description and species name
                        pos8 = data_dict['hit_def'].find('[')
                        pos9 = data_dict['hit_def'].find(']')
                        data_dict['desc'] = data_dict['hit_def'][:pos8].strip()
                        data_dict['species'] = data_dict['hit_def'][pos8+1:pos9].strip().capitalize()

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
                            data_dict['gene_id'] = gene_id if data_dict['gene_id'] == '' else f'{data_dict["gene_id"]}*{gene_id}'
                            data_dict['status'] = gene2refseq_dict[key1]['status'] if data_dict['status'] == '' else f'{data_dict["status"]}*{gene2refseq_dict[key1]["status"]}'
                            data_dict['rna_nucleotide_accession'] = gene2refseq_dict[key1]['rna_nucleotide_accession'] if data_dict['rna_nucleotide_accession'] == '' else f'{data_dict["rna_nucleotide_accession"]}*{gene2refseq_dict[key1]["rna_nucleotide_accession"]}'
                            data_dict['genomic_nucleotide_accession'] = gene2refseq_dict[key1]['genomic_nucleotide_accession'] if data_dict['genomic_nucleotide_accession'] == '' else f'{data_dict["genomic_nucleotide_accession"]}*{gene2refseq_dict[key1]["genomic_nucleotide_accession"]}'
                            data_dict['gene_symbol'] = gene2refseq_dict[key1]['gene_symbol'] if data_dict['gene_symbol'] == '' else f'{data_dict["gene_symbol"]}*{gene2refseq_dict[key1]["gene_symbol"]}'
                            xlib.Message.print('trace', f'gene2refseq -> gene_id: {gene_id} - protein_accession: {data_dict["protein_accession"]}')

                            # get gene2go dictionary with data corresponding to the "gene_id"
                            gene2go_dict = xsqlite.get_gene2go_dict(conn, gene_id)

                            # if there are not data for the "gene_id" in gene2go
                            if gene2go_dict != {}:

                                # set accumulate database list
                                data_dict['accum_databases'] = 'GO' if data_dict['accum_databases'] == '' else f'{data_dict["accum_databases"]}*GO'

                                # for each Gene Ontology annotation
                                for key2 in gene2go_dict.keys():

                                    # asign annotation values
                                    data_dict['accum_go_id'] = gene2go_dict[key2]['go_id'] if data_dict['accum_go_id'] == '' else f'{data_dict["accum_go_id"]}*{gene2go_dict[key2]["go_id"]}'
                                    data_dict['accum_evidence'] = gene2go_dict[key2]['evidence'] if data_dict['accum_evidence'] == '' else f'{data_dict["accum_evidence"]}*{gene2go_dict[key2]["evidence"]}'
                                    data_dict['accum_go_term'] = gene2go_dict[key2]['go_term'] if data_dict['accum_go_term'] == '' else f'{data_dict["accum_go_term"]}*{gene2go_dict[key2]["go_term"]}'
                                    data_dict['accum_category'] = gene2go_dict[key2]['category'] if data_dict['accum_category'] == '' else f'{data_dict["accum_category"]}*{gene2go_dict[key2]["category"]}'
                                    xlib.Message.print('trace', f'gene2go -> id: {data_dict["accum_go_id"]} - evidence: {data_dict["accum_evidence"]} - desc: {data_dict["accum_go_term"]} - category: {data_dict["accum_category"]}')

                            # get InterPro, Enzyme Commission, KEGG and MetaCyc data from Gene Onlology identification
                            if data_dict['accum_go_id'] != '':

                                # get the Gene Ontology identification list
                                go_id_list = data_dict['accum_go_id'].split('*')

                                # get InterPro dictionary with data corresponding to the Gene Onlology identification list
                                interpro_dict = xsqlite.get_cross_references_dict(conn, go_id_list, 'interpro')

                                # annotate using InterPro data
                                if interpro_dict != {}:

                                    # set accumulate repository list
                                    data_dict['accum_databases'] = 'InterPro' if data_dict['accum_databases'] == '' else f'{data_dict["accum_databases"]}*InterPro'

                                    # for each InterPro annotation
                                    for key3 in interpro_dict.keys():

                                        # get annotation values
                                        interpro_id = interpro_dict[key3]['external_id']
                                        interpro_desc = interpro_dict[key3]['external_desc']
                                        xlib.Message.print('trace', f'InterPro -> id: {interpro_id} - desc: {interpro_desc}')

                                        # accumulate values
                                        data_dict['accum_interpro_id'] = interpro_id if data_dict['accum_interpro_id'] == '' else f'{data_dict["accum_interpro_id"]}*{interpro_id}'
                                        data_dict['accum_interpro_desc'] = interpro_id if data_dict['accum_interpro_desc'] == '' else f'{data_dict["accum_interpro_desc"]}*{interpro_desc}'

                                # get Enzyme Commission dictionary with data corresponding to the Gene Onlology identification list
                                ec_dict = xsqlite.get_cross_references_dict(conn, go_id_list, 'ec')

                                # annotate using Enzyme Commission data
                                if ec_dict != {}:

                                    # set accumulate repository list
                                    data_dict['accum_databases'] = 'EC' if data_dict['accum_databases'] == '' else f'{data_dict["accum_databases"]}*EC'

                                    # for each Enzyme Commission annotation
                                    for key4 in ec_dict.keys():

                                        # get annotation values
                                        ec_id = ec_dict[key4]['external_id']
                                        xlib.Message.print('trace', f'EC -> id: {ec_id}')

                                        # accumulate values
                                        data_dict['accum_ec_id'] = ec_id if data_dict['accum_ec_id'] == '' else f'{data_dict["accum_ec_id"]}*{ec_id}'

                                # get KEGG dictionary with data corresponding to the Gene Onlology identification list
                                kegg_dict = xsqlite.get_cross_references_dict(conn, go_id_list, 'kegg')

                                # annotate using KEGG data
                                if kegg_dict != {}:

                                    # set accumulate repository list
                                    data_dict['accum_databases'] = 'KEGG' if data_dict['accum_databases'] == '' else f'{data_dict["accum_databases"]}*KEGG'

                                    # for each KEGG annotation
                                    for key5 in kegg_dict.keys():

                                        # get annotation values
                                        kegg_id = kegg_dict[key5]['external_id']
                                        xlib.Message.print('trace', f'KEGG -> id: {kegg_id}')

                                        # accumulate values
                                        data_dict['accum_kegg_id'] = kegg_id if data_dict['accum_kegg_id'] == '' else f'{data_dict["accum_kegg_id"]}*{kegg_id}'

                                # get MetaCyc dictionary with data corresponding to the Gene Onlology identification list
                                metacyc_dict = xsqlite.get_cross_references_dict(conn, go_id_list, 'metacyc')

                                # annotate using MetaCyc data
                                if metacyc_dict != {}:

                                    # set accumulate repository list
                                    data_dict['accum_databases'] = 'MetaCyc' if data_dict['accum_databases'] == '' else f'{data_dict["accum_databases"]}*MetaCyc'

                                    # for each MetaCyc annotation
                                    for key6 in metacyc_dict.keys():

                                        # get annotation values
                                        metacyc_id = metacyc_dict[key6]['external_id']
                                        xlib.Message.print('trace', f'MetaCyc -> id: {metacyc_id}')

                                        # accumulate values
                                        data_dict['accum_metacyc_id'] = metacyc_id if data_dict['accum_metacyc_id'] == '' else f'{data_dict["accum_metacyc_id"]}*{metacyc_id}'

                    # write in annotation file
                    if is_hsp_annotated:
                        xlib.write_annotation_record(annotation_file_id, type, data_dict)
            
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
        total_seq_counter += 1
        xlib.Message.print('verbose', f'\rProcessed sequences... {total_seq_counter}')

    # print summary
    xlib.Message.print('verbose', '\n')
    xlib.Message.print('info', f'Total seqs: {total_seq_counter} - Annotated seqs: {total_seq_counter - non_annotated_seq_counter} - Non-annotated seqs: {non_annotated_seq_counter}.')

    # close files
    seq_file_id.close()
    nonann_seq_file_id.close()

#-------------------------------------------------------------------------------

def annotate_sequences_nx(conn, dataset_id, aligner_tool, seq_file, toa_transcriptome_relationship_dict, toa_transdecoder_relationship_dict, viridiplantae_annotation_file, contamination_annotation_file, nonann_seq_file, type):
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

    # open the Viridiplantae annotation file
    if viridiplantae_annotation_file.endswith('.gz'):
        try:
            viridiplantae_annotation_file_id = gzip.open(viridiplantae_annotation_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', viridiplantae_annotation_file)
    else:
        try:
            viridiplantae_annotation_file_id = open(viridiplantae_annotation_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', viridiplantae_annotation_file)

    # open the contamination annotation file
    if contamination_annotation_file.endswith('.gz'):
        try:
            contamination_annotation_file_id = gzip.open(contamination_annotation_file, mode='wt', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F004', contamination_annotation_file)
    else:
        try:
            contamination_annotation_file_id = open(contamination_annotation_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            raise xlib.ProgramException('F003', contamination_annotation_file)

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
    total_seq_counter = 0
    non_annotated_seq_counter = 0

    # initialize the sequence lists
    viridiplantae_seq_list = []
    contamination_seq_list = []

    # write header record of the Viridiplantae annotation file
    xlib.write_annotation_header(viridiplantae_annotation_file_id, type)

    # write header record of the contamination annotation file
    xlib.write_annotation_header(contamination_annotation_file_id, type)

    # read the first record
    record = seq_file_id.readline()

    # while there are records
    while record != '':

        # process the header record 
        if record.startswith('>'):

            # get the sequence identifiers
            x_seq_id = record[1:].strip()
            (transcript_seq_id, nt_seq_id, aa_seq_id) = xlib.get_seq_ids(x_seq_id, toa_transcriptome_relationship_dict, toa_transdecoder_relationship_dict)
            xlib.Message.print('trace', f'transcript_seq_id: {transcript_seq_id} - nt_seq_id: {nt_seq_id} - aa_seq_id: {aa_seq_id}')

            # initialize the sequence annotation control variable
            is_seq_annotated = False

            # find the BLAST dictionary with data corresponding to the sequence identification
            blast_dict = xsqlite.get_blast_dict(conn, dataset_id, x_seq_id)
            
            # annotate the sequence for each hit-hsp if the dictionary has data
            if blast_dict != {}:
                for key in blast_dict.keys():

                    xlib.Message.print('trace', f'key: {key}')
 
                    # set annotation control variable
                    is_seq_annotated = True

                    # initialize data dictionary
                    data_dict = {}
                    data_dict['seq_id'] = transcript_seq_id
                    data_dict['nt_seq_id'] = nt_seq_id
                    data_dict['aa_seq_id'] = aa_seq_id

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
                    xlib.Message.print('trace', f'iteration_iter_num: {data_dict["iteration_iter_num"]} - hit_num: {data_dict["hit_num"]} - hit_id: {data_dict["hit_id"]}')
                    xlib.Message.print('trace', f'hsp_num: {data_dict["hsp_num"]} - hsp_evalue:{data_dict["hsp_evalue"]} - hsp_identity: {data_dict["hsp_identity"]} - hsp_positive: {data_dict["hsp_positive"]} - hsp_gaps: {data_dict["hsp_gaps"]} - hsp_align_len: {data_dict["hsp_align_len"]}')
                    xlib.Message.print('trace', f'hsp_qseq: {data_dict["hsp_qseq"]}')

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
                        data_dict['family'] = 'Virus'
                        data_dict['phylum'] = 'Virus'
                        data_dict['kingdom'] = 'Virus'
                        data_dict['superkingdom'] = 'Virus'
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

                    # when the kingdom is Viridiplantae, write in the Viridiplantae annotation file
                    if data_dict['kingdom'] == 'Viridiplantae':
                        xlib.write_annotation_record(viridiplantae_annotation_file_id, type, data_dict)
                        if data_dict['seq_id'] not in viridiplantae_seq_list:
                            viridiplantae_seq_list.append(data_dict['seq_id'])

                    # otherwise, write in the the contamination annotation file
                    else:
                        xlib.write_annotation_record(contamination_annotation_file_id, type, data_dict)
                        if data_dict['seq_id'] not in contamination_seq_list:
                            contamination_seq_list.append(data_dict['seq_id'])
          
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
        total_seq_counter += 1
        xlib.Message.print('verbose', f'\rProcessed sequences... {total_seq_counter}')

    # print summary
    xlib.Message.print('verbose', '\n')
    both_seq_list = set(viridiplantae_seq_list).intersection(contamination_seq_list)
    xlib.Message.print('info', f'Total seqs: {total_seq_counter}')
    xlib.Message.print('info', f'Viridiplantae seqs: {len(viridiplantae_seq_list) - len(both_seq_list)} - Contamination seqs: {len(contamination_seq_list)- len(both_seq_list)} - Viridiplantae&contamination seqs : {len(both_seq_list)}')
    xlib.Message.print('info', f'Not annotate seqs: {non_annotated_seq_counter}')

    # close files
    seq_file_id.close()
    viridiplantae_annotation_file_id.close()
    contamination_annotation_file_id.close()
    nonann_seq_file_id.close()

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
