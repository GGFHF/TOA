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
This source contains functions for the maintenance of the TOA SQLite database
used in both console mode and gui mode.
'''

#-------------------------------------------------------------------------------

import sqlite3
import sys

import xlib

#-------------------------------------------------------------------------------

def connect_database(database_path):
    '''
    Connect to the database.
    '''

    try:
        conn = sqlite3.connect(database_path)
    except Exception as e:
        raise xlib.ProgramException('B001', database_path)

    # return connection
    return conn

#-------------------------------------------------------------------------------

def rebuild_database(conn):
    '''
    Rebuild the database file.
    '''

    # initialize the control variable
    OK = True

    # rebuild
    sentence = 'VACUUM'
    try:
        conn.execute(sentence)
    except Exception as e:
        xlib.Message.print('error', f'*** WARNING: {e}')
        OK = False

    # return the control variable
    return OK

#-------------------------------------------------------------------------------
# table "blast"
#-------------------------------------------------------------------------------

def drop_blast(conn):
    '''
    Drop the table "blast" (if it exists)
    '''

    sentence = '''
               DROP TABLE IF EXISTS blast;
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_blast(conn):
    '''
    Create the table "blast" (if it does not exist).
    '''

    sentence = '''
               CREATE TABLE IF NOT EXISTS blast (
                   dataset_id          TEXT NOT NULL,
                   iteration_iter_num  INTEGER NOT NULL,
                   iteration_query_def TEXT NOT NULL,
                   hit_num             INTEGER NOT NULL,
                   hit_id              TEXT NOT NULL,
                   hit_def             TEXT NOT NULL,
                   hit_accession       TEXT NOT NULL,
                   hsp_num             INTEGER NOT NULL,
                   hsp_evalue          REAL NOT NULL,
                   hsp_identity        INTEGER NOT NULL,
                   hsp_positive        INTEGER NOT NULL,
                   hsp_gaps            INTEGER NOT NULL,
                   hsp_align_len       INTEGER NOT NULL,
                   hsp_qseq            TEXT NOT NULL);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_blast_index(conn):
    '''
    Create the index "blast_index" (if it does not exist) with the columns "dataset_id" and "iteration_query_def" on the table "blast"
    '''
    
    sentence = '''
               CREATE INDEX IF NOT EXISTS blast_index
                   ON blast (dataset_id, iteration_query_def);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def insert_blast_row(conn, row_dict):
    '''
    Insert a row into table "blast"
    '''

    sentence = f'''
                INSERT INTO blast
                    (dataset_id, iteration_iter_num, iteration_query_def, hit_num, hit_id, hit_def, hit_accession, hsp_num, hsp_evalue, hsp_identity, hsp_positive, hsp_gaps, hsp_align_len, hsp_qseq)
                    VALUES ('{row_dict["dataset_id"]}', '{row_dict["iteration_iter_num"]}', '{row_dict["iteration_query_def"]}', '{row_dict["hit_num"]}', '{row_dict["hit_id"]}', '{row_dict["hit_def"]}', '{row_dict["hit_accession"]}', '{row_dict["hsp_num"]}', '{row_dict["hsp_evalue"]}', '{row_dict["hsp_identity"]}', '{row_dict["hsp_positive"]}', '{row_dict["hsp_gaps"]}', '{row_dict["hsp_align_len"]}', '{row_dict["hsp_qseq"]}')
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def delete_blast_rows(conn, dataset_id):
    '''
    Delete rows from table "blast" corresponding to the dataset identification
    '''
    
    sentence = f'''
                DELETE FROM blast
                    WHERE dataset_id = '{dataset_id}';
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def get_blast_dict(conn, dataset_id, x_seq_id):
    '''
    Get a dictionary of data alignments corresponding to rows with a dataset identification and a sequence identification
    (nt_seq_id in nucleotide pipeline or aa_seq_id in amino acid pipeline) from the table "blast"
    '''

    # initialize the blast dictionary
    blast_dict = {}

    # initialize the dictionary key
    key = 0

    # select rows from the table "blast" corresponding to the iteration_query_def
    sentence = f'''
                SELECT iteration_iter_num, hit_num, hit_id, hit_def, hit_accession, hsp_num, hsp_evalue, hsp_identity, hsp_positive, hsp_gaps, hsp_align_len, hsp_qseq
                    FROM blast
                   WHERE dataset_id = '{dataset_id}'
                      AND iteration_query_def = '{x_seq_id}';
                '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # add hit-hsp data to list
    for row in rows:
        blast_dict[key] = {'iteration_iter_num':row[0], 'hit_num':row[1], 'hit_id':row[2], 'hit_def':row[3], 'hit_accession':row[4], 'hsp_num':row[5], 'hsp_evalue':float(row[6]), 'hsp_identity':int(row[7]), 'hsp_positive':int(row[8]), 'hsp_gaps':int(row[9]), 'hsp_align_len':int(row[10]), 'hsp_qseq':row[11]}
        key += 1

    # return the blast dictionary
    return blast_dict

#-------------------------------------------------------------------------------
# table "datasets"
#-------------------------------------------------------------------------------

def drop_datasets(conn):
    '''
    Drop the table "datasets" (if it exists)
    '''

    sentence = '''
               DROP TABLE IF EXISTS datasets;
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_datasets(conn):
    '''
    Create the table "datasets"
    '''
    
    sentence = '''
               CREATE TABLE datasets (
                   dataset_id      TEXT NOT NULL,
                   dataset_name    TEXT NOT NULL,
                   repository_id   TEXT NOT NULL,
                   ftp_adress      TEXT NOT NULL);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_datasets_index(conn):
    '''
    Create the unique index "datasets_index" with the column "dataset_id" on the table "datasets"
    '''
    
    sentence = '''
               CREATE UNIQUE INDEX datasets_index
                   ON datasets (dataset_id);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def insert_datasets_row(conn, row_dict):
    '''
    Insert a row into table "datasets"
    '''

    sentence = f'''
                INSERT INTO datasets
                    (dataset_id, dataset_name, repository_id, ftp_adress)
                    VALUES ('{row_dict["dataset_id"]}', '{row_dict["dataset_name"]}', '{row_dict["repository_id"]}', '{row_dict["ftp_adress"]}');
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def check_datasets(conn):
    '''
    Check if table "datasets exists and if there are rows.
    '''

    # check if table "datasets" exists
    sentence = '''
               SELECT EXISTS
                   (SELECT 1
                       FROM sqlite_master
                       WHERE type = 'table'
                         AND tbl_name = 'datasets'
                       LIMIT 1);
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # get the row number
    for row in rows:
        control = int(row[0])
        break

    # check if there are rows when the table "datasets" exists
    if control == 1:

        # select the row number
        sentence = '''
                   SELECT EXISTS
                       (SELECT 1
                           FROM datasets
                           LIMIT 1);
                   '''
        try:
            rows = conn.execute(sentence)
        except Exception as e:
            raise xlib.ProgramException('B002', e, sentence, conn)

        # get the row number
        for row in rows:
            control = int(row[0])
            break

    # return the row number
    return control

#-------------------------------------------------------------------------------

def is_dataset_id_found(conn, dataset_id):
    '''
    Check if a dataset identification is in the table "datasets"
    '''

    # initialize tha control variable
    is_found = False

    # select rows from the table "datasets"
    sentence = f'''
                SELECT dataset_id
                    FROM datasets
                    WHERE dataset_id = '{dataset_id}';
                '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # add dataset identifications to list
    for row in rows:
        is_found = True

    # return the control variable
    return is_found

#-------------------------------------------------------------------------------

def get_plaza_dataset_id_list(conn):
    '''
    Get a list of dataset identification corresponding to rows with repository identification PLAZA from the table "datasets"
    '''

    # initialize PLAZA dataset identification list
    plaza_dataset_id_list = []

    # select the dataset identification from the table "datasets"
    sentence = '''
               SELECT dataset_id
                   FROM datasets
                   WHERE repository_id = 'plaza';
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # add dataset identifications to list
    for row in rows:
        dataset_id = row[0]
        plaza_dataset_id_list.append(dataset_id)

    # return PLAZA dataset identification list
    return plaza_dataset_id_list

#-------------------------------------------------------------------------------

def get_dataset_dict(conn):
    '''
    Get a dictionary of datasets from the table "datasets".
    '''

    # initialize the dataset dictionary
    dataset_dict = {}

    # select rows from the table "dataset"
    sentence = '''
                SELECT DISTINCT dataset_id, dataset_name, repository_id, ftp_adress
                    FROM datasets;
                '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # add dataset data to the dictionary
    for row in rows:
        dataset_dict[row[0]] = {'dataset_id':row[0], 'dataset_name':row[1], 'repository_id':row[2], 'ftp_adress':row[3]}

    # return the dataset dictionary
    return dataset_dict

#-------------------------------------------------------------------------------
# table "ec_ids"
#-------------------------------------------------------------------------------

def drop_ec_ids(conn):
    '''
    Drop the table "ec_ids" (if it exists)
    '''

    sentence = '''
               DROP TABLE IF EXISTS ec_ids;
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_ec_ids(conn):
    '''
    Create the table "ec_ids"
    '''
    
    sentence = '''
               CREATE TABLE ec_ids (
                   ec_id TEXT NOT NULL,
                   desc  TEXT NOT NULL);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_ec_ids_index(conn):
    '''
    Create the unique index "ec_ids_index" with the column "dataset_id" on the table "ec_ids"
    '''
    
    sentence = '''
               CREATE UNIQUE INDEX ec_ids_index
                   ON ec_ids (ec_id);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def insert_ec_ids_row(conn, row_dict):
    '''
    Insert a row into table "ec_ids"
    '''

    sentence = f'''
                INSERT INTO ec_ids
                    (ec_id, desc)
                    VALUES ('{row_dict["ec_id"]}', '{row_dict["desc"]}');
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def check_ec_ids(conn):
    '''
    Check if table "ec_ids exists and if there are rows.
    '''

    # check if table "ec_ids" exists
    sentence = '''
               SELECT EXISTS
                   (SELECT 1
                       FROM sqlite_master
                       WHERE type = 'table'
                         AND tbl_name = 'ec_ids'
                       LIMIT 1);
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # get the row number
    for row in rows:
        control = int(row[0])
        break

    # check if there are rows when the table "ec_ids" exists
    if control == 1:

        # select the row number
        sentence = '''
                   SELECT EXISTS
                       (SELECT 1
                           FROM ec_ids
                           LIMIT 1);
                   '''
        try:
            rows = conn.execute(sentence)
        except Exception as e:
            raise xlib.ProgramException('B002', e, sentence, conn)

        # get the row number
        for row in rows:
            control = int(row[0])
            break

    # return the row number
    return control

#-------------------------------------------------------------------------------

def get_ec_id_dict(conn):
    '''
    Get a dictionary of ec_ids from the table "ec_ids".
    '''

    # initialize the dataset dictionary
    dataset_dict = {}

    # select rows from the table "dataset"
    sentence = '''
                SELECT DISTINCT ec_id, desc
                    FROM ec_ids;
                '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # add dataset data to the dictionary
    for row in rows:
        dataset_dict[row[0]] = {'ec_id':row[0], 'desc':row[1]}

    # return the dataset dictionary
    return dataset_dict

#-------------------------------------------------------------------------------
# table "genomic_features"
#-------------------------------------------------------------------------------

def create_genomic_features(conn):
    '''
    Create table "genomic_features" (if it does not exist).
    '''
    
    sentence = '''
               CREATE TABLE IF NOT EXISTS genomic_features (
                   species_name  TEXT NOT NULL,
                   seq_id        TEXT NOT NULL,
                   start         INTEGER NOT NULL,
                   end           INTEGER NOT NULL,
                   type          TEXT NOT NULL,
                   gene_id       TEXT NOT NULL,
                   genbank_id    TEXT NOT NULL,
                   gene          TEXT NOT NULL,
                   protein_id    TEXT NOT NULL,
                   transcript_id TEXT NOT NULL,
                   product       TEXT NOT NULL);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_genomic_features_index(conn):
    '''
    Create the index "genomic_features_index" (if it does not exist) with the columns "species_name" and "seq_id" on the table "genomic_features".
    '''
    
    sentence = '''
               CREATE INDEX IF NOT EXISTS genomic_features_index
                   ON genomic_features (species_name, seq_id);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def insert_genomic_features_row(conn, row_dict):
    '''
    Insert a row into table "genomic_features".
    '''

    sentence = f'''
                INSERT INTO genomic_features
                    (species_name, seq_id, start, end, type, gene_id, genbank_id, gene, protein_id, transcript_id, product)
                    VALUES ('{row_dict["species_name"]}', '{row_dict["seq_id"]}', {row_dict["start"]}, {row_dict["end"]}, '{row_dict["type"]}', '{row_dict["gene_id"]}', '{row_dict["genbank_id"]}', '{row_dict["gene"]}', '{row_dict["protein_id"]}', '{row_dict["transcript_id"]}', '{row_dict["product"]}');
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def delete_genomic_features_rows(conn, species_name):
    '''
    Delete rows from table "genomic_features" corresponding to the species.
    '''
    
    sentence = f'''
                DELETE FROM genomic_features
                    WHERE species_name = '{species_name}';
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def get_genomic_features_dict(conn, species_name, transcript_seq_id, transcript_start, transcript_end):
    '''
    Get a sequence features dictionary from the table "genomic_features" corresponding to a species and a sequence identification and its start less than or equal to the transcript start.
    '''

    # initialize the sequence feature dictionary
    genomic_feature_dict = {}

    # initialize the dictionary key
    key = 0

    # select rows from the table "genomic_features"
    sentence = f'''
                SELECT start, end, type, gene_id, genbank_id, gene, protein_id, transcript_id, product
                    FROM genomic_features
                    WHERE species_name = '{species_name}'
                      AND seq_id = '{transcript_seq_id}'
                      AND start <= {transcript_start}
                      AND end >= {transcript_end};
                '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # add row data to the dictionary
    for row in rows:
        genomic_feature_dict[key] = {'start': row[0], 'end': row[1], 'type': row[2], 'gene_id': row[3], 'genbank_id': row[4], 'gene': row[5], 'protein_id': row[6], 'transcript_id': row[7], 'product': row[8]}
        key += 1

    # return the sequence feature dictionary
    return genomic_feature_dict

#-------------------------------------------------------------------------------

def check_genomic_features(conn, species_name):
    '''
    Check if table "genomic_feature" exists and if there are rows corresponding to features of a species.
    '''

    # check if table "genomic_feature" exists
    sentence = '''
               SELECT EXISTS
                   (SELECT 1
                       FROM sqlite_master
                       WHERE type = 'table'
                         AND tbl_name = 'genomic_feature'
                       LIMIT 1);
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # get the row number
    for row in rows:
        control = int(row[0])
        break

    # check if there are rows when the table "genomic_feature" exists
    if control == 1:

        # select the row number
        sentence = f'''
                    SELECT EXISTS
                        (SELECT 1
                            FROM genomic_feature
                            where  species_name = '{species_name}';
                            LIMIT 1);
                    '''
        try:
            rows = conn.execute(sentence)
        except Exception as e:
            raise xlib.ProgramException('B002', e, sentence, conn)

        # get the row number
        for row in rows:
            control = int(row[0])
            break

    # return the row number
    return control

#-------------------------------------------------------------------------------
# table "go_ontology"
#-------------------------------------------------------------------------------

def drop_go_ontology(conn):
    '''
    Drop the table "go_ontology" (if it exists).
    '''

    sentence = '''
               DROP TABLE IF EXISTS go_ontology;
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_go_ontology(conn):
    '''
    Create the table "go_ontology".
    '''

    sentence = '''
               CREATE TABLE go_ontology (
                   go_id         TEXT NOT NULL,
                   go_name       TEXT NOT NULL,
                   namespace     TEXT NOT NULL);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_go_ontology_index(conn):
    '''
    Create the index "go_ontology_index" with the column "go_id" on the table "go_ontology".
    '''
    
    sentence = '''
               CREATE INDEX go_ontology_index
                   ON go_ontology (go_id);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def insert_go_ontology_row(conn, row_dict):
    '''
    Insert a row into table "go_ontology".
    '''

    sentence = f'''
                INSERT INTO go_ontology
                    (go_id, go_name, namespace)
                    VALUES ('{row_dict["go_id"]}', '{row_dict["go_name"]}', '{row_dict["namespace"]}');
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def check_go_ontology(conn):
    '''
    Check if table "go_ontology" exists and if there are rows.
    '''

    # check if table "go_ontology" exists
    sentence = '''
               SELECT EXISTS
                   (SELECT 1
                       FROM sqlite_master
                       WHERE type = 'table'
                         AND tbl_name = 'go_ontology'
                       LIMIT 1);
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # get the row number
    for row in rows:
        control = int(row[0])
        break

    # check if there are rows when the table "go_ontology" exists
    if control == 1:

        # select the row number
        sentence = '''
                   SELECT EXISTS
                       (SELECT 1
                           FROM go_ontology
                           LIMIT 1);
                   '''
        try:
            rows = conn.execute(sentence)
        except Exception as e:
            raise xlib.ProgramException('B002', e, sentence, conn)

        # get the row number
        for row in rows:
            control = int(row[0])
            break

    # return the row number
    return control

#-------------------------------------------------------------------------------

def get_go_ontology_dict(conn, go_id_list):
    '''
    Get a dictionary of ontology from the table "go_ontology".
    '''

    # initialize the ontology dictionary
    go_onlology_dict = {}

    # select rows from the table "go_ontology"
    if go_id_list == []:
        sentence = '''
                   SELECT DISTINCT go_id, go_name, namespace
                       FROM go_ontology;
                   '''
    else:
        sentence = f'''
                    SELECT DISTINCT go_id, go_name, namespace
                        FROM go_ontology
                        WHERE go_id in ({xlib.join_string_list_to_string(go_id_list)});
                    '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # add ontology data to the dictionary
    for row in rows:
        go_onlology_dict[row[0]] = {'go_id':row[0], 'go_name':row[1], 'namespace':row[2]}

    # return the ontology dictionary
    return go_onlology_dict

#-------------------------------------------------------------------------------
# table "go_cross_references"
#-------------------------------------------------------------------------------

def drop_go_cross_references(conn):
    '''
    Drop the table "go_cross_references" (if it exists).
    '''

    sentence = '''
               DROP TABLE IF EXISTS go_cross_references;
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_go_cross_references(conn):
    '''
    Create the table "go_cross_references".
    '''

    sentence = '''
               CREATE TABLE go_cross_references (
                   go_id         TEXT NOT NULL,
                   go_term       TEXT NOT NULL,
                   external_db   TEXT NOT NULL,
                   external_id   TEXT NOT NULL,
                   external_desc TEXT NOT NULL);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_go_cross_references_index(conn):
    '''
    Create the index "go_cross_references_index" with the column "go_id" on the table "go_cross_references".
    '''
    
    sentence = '''
               CREATE INDEX go_cross_references_index
                   ON go_cross_references (go_id);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def insert_go_cross_references_row(conn, row_dict):
    '''
    Insert a row into table "go_cross_references".
    '''

    sentence = f'''
                INSERT INTO go_cross_references
                    (go_id, go_term, external_db, external_id, external_desc)
                    VALUES ('{row_dict["go_id"]}', '{row_dict["go_term"]}', '{row_dict["external_db"]}', '{row_dict["external_id"]}', '{row_dict["external_desc"]}');
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def check_go_cross_references(conn):
    '''
    Check if table "go_cross_references" exists and if there are rows.
    '''

    # check if table "go_cross_references" exists
    sentence = '''
               SELECT EXISTS
                   (SELECT 1
                       FROM sqlite_master
                       WHERE type = 'table'
                         AND tbl_name = 'go_cross_references'
                       LIMIT 1);
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # get the row number
    for row in rows:
        control = int(row[0])
        break

    # check if there are rows when the table "go_cross_references" exists
    if control == 1:

        # select the row number
        sentence = '''
                   SELECT EXISTS
                       (SELECT 1
                           FROM go_cross_references
                           LIMIT 1);
                   '''
        try:
            rows = conn.execute(sentence)
        except Exception as e:
            raise xlib.ProgramException('B002', e, sentence, conn)

        # get the row number
        for row in rows:
            control = int(row[0])
            break

    # return the row number
    return control

#-------------------------------------------------------------------------------

def get_cross_references_dict(conn, go_id_list, external_db):
    '''
    Get a dictionary of cross_references corresponding to rows with a Gene Ontology identification list from the table "go_cross_references".
    '''

    # initialize the cross_references dictionary
    cross_references_dict = {}

    # initialize the dictionary key
    key = 0

    # select rows from the table "go_cross_references"
    if external_db == 'all':
        sentence = f'''
                    SELECT DISTINCT go_id, go_term, external_db, external_id, external_desc
                        FROM go_cross_references
                        WHERE go_id in ({xlib.join_string_list_to_string(go_id_list)});
                    '''
    else:
        sentence = f'''
                    SELECT DISTINCT go_id, go_term, external_db, external_id, external_desc
                        FROM go_cross_references
                        WHERE go_id in ({xlib.join_string_list_to_string(go_id_list)})
                          AND external_db = '{external_db}';
                    '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # add cross references data to dictionary
    for row in rows:
        cross_references_dict[key] = {'go_id':row[0], 'go_term':row[1], 'external_db':row[2], 'external_id':row[3], 'external_desc':row[4]}
        key += 1

    # return the cross references dictionary
    return cross_references_dict

#-------------------------------------------------------------------------------
# table "interpro_interpro2go"
#-------------------------------------------------------------------------------

def drop_interpro_interpro2go(conn):
    '''
    Drop the table "interpro_interpro2go" (if it exists).
    '''

    sentence = '''
               DROP TABLE IF EXISTS interpro_interpro2go;
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_interpro_interpro2go(conn):
    '''
    Create the table "interpro_interpro2go".
    '''

    sentence = '''
               CREATE TABLE interpro_interpro2go (
                   interpro_id     TEXT NOT NULL,
                   interpro_desc   TEXT NOT NULL,
                   go_desc         TEXT NOT NULL,
                   go_id           TEXT NOT NULL);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_interpro_interpro2go_index_1(conn):
    '''
    Create the index "interpro_interpro2go_index_1" with the column "interpro_id" on the table "interpro_interpro2go".
    '''
    
    sentence = '''
               CREATE INDEX interpro_interpro2go_index_1
                   ON interpro_interpro2go (interpro_id);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_interpro_interpro2go_index_2(conn):
    '''
    Create the index "interpro_interpro2go_index_2" with the column "go_id" on the table "interpro_interpro2go".
    '''
    
    sentence = '''
               CREATE INDEX interpro_interpro2go_index_2
                   ON interpro_interpro2go (go_id);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def insert_interpro_interpro2go_row(conn, row_dict):
    '''
    Insert a row into table "interpro_interpro2go".
    '''

    sentence = f'''
                INSERT INTO interpro_interpro2go
                    (interpro_id, interpro_desc, go_desc, go_id)
                    VALUES ('{row_dict["interpro_id"]}', '{row_dict["interpro_desc"]}', '{row_dict["go_desc"]}', '{row_dict["go_id"]}');
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def check_interpro_interpro2go(conn):
    '''
    Check if table "interpro_interpro2go" exists and if there are rows.
    '''

    # check if table "interpro_interpro2go" exists
    sentence = '''
               SELECT EXISTS
                   (SELECT 1
                       FROM sqlite_master
                       WHERE type = 'table'
                         AND tbl_name = 'interpro_interpro2go'
                       LIMIT 1);
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # get the row number
    for row in rows:
        control = int(row[0])
        break

    # check if there are rows when the table "interpro_interpro2go" exists
    if control == 1:

        # select the row number
        sentence = '''
                   SELECT EXISTS
                       (SELECT 1
                           FROM interpro_interpro2go
                           LIMIT 1);
                   '''
        try:
            rows = conn.execute(sentence)
        except Exception as e:
            raise xlib.ProgramException('B002', e, sentence, conn)

        # get the row number
        for row in rows:
            control = int(row[0])
            break

    # return the row number
    return control

#-------------------------------------------------------------------------------

def get_interpro2go_dict(conn, interpro_id):
    '''
    Get a dictionary of annotation data corresponding to rows with a InterPro identification from the table "interpro_interpro2go".
    '''

    # initialize the interpro2go dictionary
    interpro2go_dict = {}

    # initialize the dictionary key
    key = 0

    # select rows from the table "interpro_interpro2go"
    sentence = f'''
                SELECT DISTINCT go_id, go_desc
                    FROM interpro_interpro2go
                    WHERE interpro_id = '{interpro_id}'
                    ORDER BY go_id;
                '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # add annotation data to list
    for row in rows:
        interpro2go_dict[key] = {'go_id':row[0], 'go_desc':row[1]}
        key += 1

    # return the gene2go dictionary
    return interpro2go_dict

#-------------------------------------------------------------------------------
# table "ncbi_gene2go"
#-------------------------------------------------------------------------------

def drop_ncbi_gene2go(conn):
    '''
    Drop the table "ncbi_gene2go" (if it exists).
    '''

    sentence = '''
               DROP TABLE IF EXISTS ncbi_gene2go;
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_ncbi_gene2go(conn):
    '''
    Create the table "ncbi_gene2go".
    '''

    sentence = '''
               CREATE TABLE  ncbi_gene2go (
                   gene_id   INTEGER NOT NULL,
                   go_id     TEXT NOT NULL,
                   evidence  TEXT NOT NULL,
                   go_term   TEXT NOT NULL,
                   category  TEXT NOT NULL);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_ncbi_gene2go_index(conn):
    '''
    Create the index "ncbi_gene2go_index" with the column "gene_id" on the table "ncbi_gene2go".
    '''
    
    sentence = '''
               CREATE INDEX ncbi_gene2go_index
                   ON ncbi_gene2go (gene_id);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def insert_ncbi_gene2go_row(conn, row_dict):
    '''
    Insert a row into table "ncbi_gene2go".
    '''

    sentence = f'''
                INSERT INTO ncbi_gene2go
                    (gene_id, go_id, evidence, go_term, category)
                    VALUES ({row_dict["gene_id"]}, '{row_dict["go_id"]}', '{row_dict["evidence"]}', '{row_dict["go_term"]}', '{row_dict["category"]}');
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def check_ncbi_gene2go(conn):
    '''
    Check if table "ncbi_gene2go· exists and its if there are rows.
    '''

    # check if table "ncbi_gene2go" exists
    sentence = '''
               SELECT EXISTS
                   (SELECT 1
                       FROM sqlite_master
                       WHERE type = 'table'
                         AND tbl_name = 'ncbi_gene2go'
                       LIMIT 1);
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # get the row number
    for row in rows:
        control = int(row[0])
        break

    # check if there are rows when the table "ncbi_gene2go" exists
    if control == 1:

        # select the row number
        sentence = '''
                   SELECT EXISTS
                       (SELECT 1
                           FROM ncbi_gene2go
                           LIMIT 1);
                   '''
        try:
            rows = conn.execute(sentence)
        except Exception as e:
            raise xlib.ProgramException('B002', e, sentence, conn)

        # get the row number
        for row in rows:
            control = int(row[0])
            break

    # return the row number
    return control

#-------------------------------------------------------------------------------

def get_gene2go_dict(conn, gene_id):
    '''
    Get a dictionary of annotation data corresponding to rows with a gene identification from the table "ncbi_gene2go".
    '''

    # initialize the gene2go dictionary
    gene2go_dict = {}

    # initialize the dictionary key
    key = 0

    # select rows from the table "ncbi_gene2go"
    sentence = f'''
                SELECT DISTINCT gene_id, go_id, evidence, go_term, category
                    FROM ncbi_gene2go
                    WHERE gene_id = '{gene_id}';
                '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # add annotation data to list
    for row in rows:
        gene2go_dict[key] = {'gene_id':row[0], 'go_id':row[1], 'evidence':row[2], 'go_term':row[3], 'category':row[4]}
        key += 1

    # return the gene2go dictionary
    return gene2go_dict

#-------------------------------------------------------------------------------
# table "kegg_ids"
#-------------------------------------------------------------------------------

def drop_kegg_ids(conn):
    '''
    Drop the table "kegg_ids" (if it exists)
    '''

    sentence = '''
               DROP TABLE IF EXISTS kegg_ids;
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_kegg_ids(conn):
    '''
    Create the table "kegg_ids"
    '''
    
    sentence = '''
               CREATE TABLE kegg_ids (
                   kegg_id TEXT NOT NULL,
                   desc    TEXT NOT NULL,
                   ec_id   TEXT NOT NULL);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_kegg_ids_index(conn):
    '''
    Create the unique index "kegg_ids_index" with the column "dataset_id" on the table "kegg_ids"
    '''
    
    sentence = '''
               CREATE UNIQUE INDEX kegg_ids_index
                   ON kegg_ids (kegg_id);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def insert_kegg_ids_row(conn, row_dict):
    '''
    Insert a row into table "kegg_ids"
    '''

    sentence = f'''
                INSERT INTO kegg_ids
                    (kegg_id, desc, ec_id)
                    VALUES ('{row_dict["kegg_id"]}', '{row_dict["desc"]}', '{row_dict["ec_id"]}');
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def check_kegg_ids(conn):
    '''
    Check if table "kegg_ids exists and if there are rows.
    '''

    # check if table "kegg_ids" exists
    sentence = '''
               SELECT EXISTS
                   (SELECT 1
                       FROM sqlite_master
                       WHERE type = 'table'
                         AND tbl_name = 'kegg_ids'
                       LIMIT 1);
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # get the row number
    for row in rows:
        control = int(row[0])
        break

    # check if there are rows when the table "kegg_ids" exists
    if control == 1:

        # select the row number
        sentence = '''
                   SELECT EXISTS
                       (SELECT 1
                           FROM kegg_ids
                           LIMIT 1);
                   '''
        try:
            rows = conn.execute(sentence)
        except Exception as e:
            raise xlib.ProgramException('B002', e, sentence, conn)

        # get the row number
        for row in rows:
            control = int(row[0])
            break

    # return the row number
    return control

#-------------------------------------------------------------------------------

def get_kegg_id_dict(conn):
    '''
    Get a dictionary of kegg_ids from the table "kegg_ids".
    '''

    # initialize the dataset dictionary
    dataset_dict = {}

    # select rows from the table "dataset"
    sentence = '''
                SELECT DISTINCT kegg_id, desc, ec_id
                    FROM kegg_ids;
                '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # add dataset data to the dictionary
    for row in rows:
        dataset_dict[row[0]] = {'kegg_id':row[0], 'desc':row[1], 'ec_id':row[2]}

    # return the dataset dictionary
    return dataset_dict

#-------------------------------------------------------------------------------
# table "ncbi_gene2refseq"
#-------------------------------------------------------------------------------

def drop_ncbi_gene2refseq(conn):
    '''
    Drop the table "ncbi_gene2refseq" (if it exists).
    '''

    sentence = '''
               DROP TABLE IF EXISTS ncbi_gene2refseq;
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_ncbi_gene2refseq(conn):
    '''
    Create table "_ncbi_gene2refseq".
    '''
    
    sentence = '''
               CREATE TABLE  ncbi_gene2refseq (
                   gene_id                      INTEGER NOT NULL,
                   status                       TEXT NOT NULL,
                   rna_nucleotide_accession     TEXT NOT NULL,
                   protein_accession            TEXT NOT NULL,
                   genomic_nucleotide_accession TEXT NOT NULL,
                   gene_symbol                  TEXT NOT NULL);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_ncbi_gene2refseq_index(conn):
    '''
    Create the index "ncbi_gene2refseq_index" with the column "protein_accession" on the table "ncbi_gene2refseq".
    '''
    
    sentence = '''
               CREATE INDEX ncbi_gene2refseq_index
                   ON ncbi_gene2refseq (protein_accession);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def insert_ncbi_gene2refseq_row(conn, row_dict):
    '''
    Insert a row into table "ncbi_gene2refseq".
    '''

    sentence = f'''
                INSERT INTO ncbi_gene2refseq
                    (gene_id, status, rna_nucleotide_accession, protein_accession, genomic_nucleotide_accession, gene_symbol)
                    VALUES ({row_dict["gene_id"]}, '{row_dict["status"]}', '{row_dict["rna_nucleotide_accession"]}', '{row_dict["protein_accession"]}', '{row_dict["genomic_nucleotide_accession"]}', '{row_dict["gene_symbol"]}');
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def check_ncbi_gene2refseq(conn):
    '''
    Check if table "ncbi_gene2refseq" exists and if there are rows.
    '''

    # check if table "ncbi_gene2refseq" exists
    sentence = '''
               SELECT EXISTS
                   (SELECT 1
                       FROM sqlite_master
                       WHERE type = 'table'
                         AND tbl_name = 'ncbi_gene2refseq'
                       LIMIT 1);
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # get the row number
    for row in rows:
        control = int(row[0])
        break

    # check if there are rows when the table "ncbi_gene2refseq" exists
    if control == 1:

        # select the row number
        sentence = '''
                   SELECT EXISTS
                       (SELECT 1
                           FROM ncbi_gene2refseq
                           LIMIT 1);
                   '''
        try:
            rows = conn.execute(sentence)
        except Exception as e:
            raise xlib.ProgramException('B002', e, sentence, conn)

        # get the row number
        for row in rows:
            control = int(row[0])
            break

    # return the row number
    return control

#-------------------------------------------------------------------------------

def get_gene2refseq_dict(conn, protein_accession):
    '''
    Get a dictionary of gene data corresponding to rows with a protein accesion from the table "ncbi_gene2refseq".
    '''

    # initialize the gene2refseq dictionary
    gene2refseq_dict = {}

    # initialize the dictionary key
    key = 0

    # select rows from the table "ncbi_gene2refseq"
    sentence = f'''
                SELECT DISTINCT gene_id, status, rna_nucleotide_accession, genomic_nucleotide_accession, gene_symbol
                    FROM ncbi_gene2refseq
                    WHERE protein_accession = '{protein_accession}';
                '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn) 

    # add annotation data to list
    for row in rows:
        gene2refseq_dict[key] = {'gene_id':row[0], 'status':row[1], 'rna_nucleotide_accession':row[2], 'genomic_nucleotide_accession':row[3], 'gene_symbol':row[4]}
        key += 1

    # return the gene2refseq dictionary
    return gene2refseq_dict

#-------------------------------------------------------------------------------
# table "plaza_gene_description"
#-------------------------------------------------------------------------------

def create_plaza_gene_description(conn):
    '''
    Create the table "plaza_gene_description" (if it does not exist).
    '''

    sentence = '''
               CREATE TABLE IF NOT EXISTS plaza_gene_description (
                   dataset_id       TEXT NOT NULL,
                   gene_id          TEXT NOT NULL,
                   plaza_species_id TEXT NOT NULL,
                   desc_type        TEXT NOT NULL,
                   desc             TEXT NOT NULL);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_plaza_gene_description_index(conn):
    '''
    Create the index "plaza_gene_description_index" (if it does not exist) with the columns "dataset_id" and "gene_id" on the table "plaza_gene_description".
    '''
    
    sentence = '''
               CREATE INDEX IF NOT EXISTS plaza_gene_description_index
                   ON plaza_gene_description (dataset_id, gene_id);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def insert_plaza_gene_description_row(conn, row_dict):
    '''
    Insert a row into table "plaza_gene_description".
    '''

    sentence = f'''
                INSERT INTO plaza_gene_description
                    (dataset_id, gene_id, plaza_species_id, desc_type, desc)
                    VALUES ('{row_dict["dataset_id"]}', '{row_dict["gene_id"]}', '{row_dict["plaza_species_id"]}', '{row_dict["desc_type"]}', '{row_dict["desc"]}');
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def delete_plaza_gene_description_rows(conn, dataset_id, species_id):
    '''
    Delete rows from table "plaza_gene_description" corresponding to the dataset identification and, optionally, the PLAZA species identification.
    '''
    
    if species_id == 'all':
        sentence = f'''
                    DELETE FROM plaza_gene_description
                        WHERE dataset_id = '{dataset_id}';
                    '''
    else:
        sentence = f'''
                    DELETE FROM plaza_gene_description
                        WHERE dataset_id = '{dataset_id}'
                          AND plaza_species_id = '{species_id}';
                    '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def check_plaza_gene_description(conn, dataset_id):
    '''
    Check if table "plaza_gene_description" exists and if there are rows corresponding to a dataset.
    '''

    # check if table "plaza_gene_description" exists
    sentence = '''
               SELECT EXISTS
                   (SELECT 1
                       FROM sqlite_master
                       WHERE type = 'table'
                         AND tbl_name = 'plaza_gene_description'
                       LIMIT 1);
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # get the row number
    for row in rows:
        control = int(row[0])
        break

    # check if there are rows when the table "plaza_gene_description" exists
    if control == 1:

        # select the row number
        sentence = f'''
                    SELECT EXISTS
                        (SELECT 1
                            FROM plaza_gene_description
                            where  dataset_id = '{dataset_id}'
                            LIMIT 1);
                    '''
        try:
            rows = conn.execute(sentence)
        except Exception as e:
            raise xlib.ProgramException('B002', e, sentence, conn)

        # get the row number
        for row in rows:
            control = int(row[0])
            break

    # return the row number
    return control

#-------------------------------------------------------------------------------

def get_gene_description_dict(conn, dataset_id, gene_id):
    '''
    Get a dictionary of description data corresponding to rows with a dataset identification and a gene identification from the table "plaza_gene_description".
    '''

    # initialize the Gene Ontology dictionary
    gene_description_dict = {}

    # select rows from the table "plaza_gene_description"
    
    if gene_id == 'all':
        sentence = f'''
                    SELECT DISTINCT gene_id, plaza_species_id, desc_type, desc 
                        FROM plaza_gene_description
                        WHERE dataset_id = '{dataset_id}';
                    '''
    else:
        sentence = f'''
                    SELECT DISTINCT gene_id, plaza_species_id, desc_type, desc 
                        FROM plaza_gene_description
                        WHERE dataset_id = '{dataset_id}'
                          AND gene_id = '{gene_id}';
                    '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # add annotation data to list
    for row in rows:
        gene_description_dict[row[0]] = {'gene_id':row[0], 'plaza_species_id':row[1], 'desc_type':row[2], 'desc':row[3]}

    # return the Gene Ontology dictionary
    return gene_description_dict

#-------------------------------------------------------------------------------
# table "plaza_go"
#-------------------------------------------------------------------------------

def create_plaza_go(conn):
    '''
    Create the table "plaza_go" (if it does not exist).
    '''

    sentence = '''
               CREATE TABLE IF NOT EXISTS plaza_go (
                   dataset_id       TEXT NOT NULL,
                   id               INTEGER NOT NULL,
                   plaza_species_id TEXT NOT NULL,
                   gene_id          TEXT NOT NULL,
                   go_id            TEXT NOT NULL,
                   evidence         TEXT NOT NULL,
                   desc             TEXT NOT NULL);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_plaza_go_index(conn):
    '''
    Create the index "plaza_go_index" (if it does not exist) with the columns "dataset_id" and "gene_id" on the table "plaza_go".
    '''
    
    sentence = '''
               CREATE INDEX IF NOT EXISTS plaza_go_index
                   ON plaza_go (dataset_id, gene_id);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def insert_plaza_go_row(conn, row_dict):
    '''
    Insert a row into table "plaza_go".
    '''

    sentence = f'''
                INSERT INTO plaza_go
                    (dataset_id, id, plaza_species_id, gene_id, go_id, evidence, desc)
                    VALUES ('{row_dict["dataset_id"]}', '{row_dict["id"]}', '{row_dict["plaza_species_id"]}', '{row_dict["gene_id"]}', '{row_dict["go_id"]}', '{row_dict["evidence"]}', '{row_dict["desc"]}');
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def delete_plaza_go_rows(conn, dataset_id, species_id):
    '''
    Delete rows from table "plaza_go" corresponding to the dataset identification and, optionally, the PLAZA species identification.
    '''
    
    if species_id == 'all':
        sentence = f'''
                    DELETE FROM plaza_go
                        WHERE dataset_id = '{dataset_id}';
                    '''
    else:
        sentence = f'''
                    DELETE FROM plaza_go
                        WHERE dataset_id = '{dataset_id}'
                          AND plaza_species_id = '{species_id}';
                    '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def check_plaza_go(conn, dataset_id):
    '''
    Check if table "plaza_go" exists and if there are rows corresponding to a dataset.
    '''

    # check if table "plaza_go" exists
    sentence = '''
               SELECT EXISTS
                   (SELECT 1
                       FROM sqlite_master
                       WHERE type = 'table'
                         AND tbl_name = 'plaza_go'
                       LIMIT 1);
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # get the row number
    for row in rows:
        control = int(row[0])
        break

    # check if there are rows when the table "plaza_go" exists
    if control == 1:

        # select the row number
        sentence = f'''
                    SELECT EXISTS
                        (SELECT 1
                            FROM plaza_go
                            where  dataset_id = '{dataset_id}'
                            LIMIT 1);
                    '''
        try:
            rows = conn.execute(sentence)
        except Exception as e:
            raise xlib.ProgramException('B002', e, sentence, conn)

        # get the row number
        for row in rows:
            control = int(row[0])
            break

    # return the row number
    return control

#-------------------------------------------------------------------------------

def get_go_dict(conn, dataset_id, gene_id):
    '''
    Get a dictionary of annotation data corresponding to rows with a dataset identification and a gene identification from the table "plaza_go".
    '''

    # initialize the Gene Ontology dictionary
    go_dict = {}


    # initialize the dictionary key
    key = 0

    # select rows from the table "plaza_go"
    sentence = f'''
                SELECT DISTINCT plaza_species_id, go_id, evidence, desc 
                    FROM plaza_go
                    WHERE dataset_id = '{dataset_id}'
                      AND gene_id = '{gene_id}';
                '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # add annotation data to list
    for row in rows:
        go_dict[key] = {'plaza_species_id':row[0], 'go_id':row[1], 'evidence':row[2], 'desc':row[3]}
        key += 1

    # return the Gene Ontology dictionary
    return go_dict

#-------------------------------------------------------------------------------
# table "plaza_interpro"
#-------------------------------------------------------------------------------

def create_plaza_interpro(conn):
    '''
    Create the table "plaza_interpro" (if it does not exist).
    '''

    sentence = ''' 
               CREATE TABLE IF NOT EXISTS plaza_interpro (
                   dataset_id       TEXT NOT NULL,
                   id               INTEGER NOT NULL,
                   motif_id         TEXT NOT NULL,
                   plaza_species_id TEXT NOT NULL,
                   gene_id          TEXT NOT NULL,
                   start            INTEGER NOT NULL,
                   stop             INTEGER NOT NULL,
                   score            REAL NOT NULL,
                   source           TEXT NOT NULL,
                   domain_id        TEXT NOT NULL,
                   desc             TEXT NOT NULL);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_plaza_interpro_index(conn):
    '''
    Create the index "plaza_interpro_index" (if it does not exist) with the columns "dataset_id" and "gene_id" on the table "plaza_interpro".
    '''
    
    sentence = ''' 
               CREATE INDEX IF NOT EXISTS plaza_interpro_index
                   ON plaza_interpro (dataset_id, gene_id);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def insert_plaza_interpro_row(conn, row_dict):
    '''
    Insert a row into table "plaza_interpro".
    '''

    sentence = f'''
                INSERT INTO plaza_interpro
                    (dataset_id, id, motif_id, plaza_species_id, gene_id, start, stop, score, source, domain_id, desc)
                    VALUES ('{row_dict["dataset_id"]}', '{row_dict["id"]}', '{row_dict["motif_id"]}', '{row_dict["plaza_species_id"]}', '{row_dict["gene_id"]}', {row_dict["start"]}, {row_dict["stop"]}, {row_dict["score"]}, '{row_dict["source"]}', '{row_dict["domain_id"]}', '{row_dict["desc"]}');
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def delete_plaza_interpro_rows(conn, dataset_id, species_id):
    '''
    Delete rows from table "plaza_interpro" corresponding to the dataset identification and, optionally, the PLAZA species identification.
    '''
    
    if species_id == 'all':
        sentence = f'''
                    DELETE FROM plaza_interpro
                        WHERE dataset_id = '{dataset_id}';
                    '''
    else:
        sentence = f'''
                    DELETE FROM plaza_interpro
                        WHERE dataset_id = '{dataset_id}'
                          AND plaza_species_id = '{species_id}';
                    '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def check_plaza_interpro(conn, dataset_id):
    '''
    Check if table "plaza_interpro" exists and if there are rows corresponding to a dataset.
    '''

    # check if table "plaza_interpro" exists
    sentence = '''
               SELECT EXISTS
                   (SELECT 1
                       FROM sqlite_master
                       WHERE type = 'table'
                         AND tbl_name = 'plaza_interpro'
                       LIMIT 1);
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # get the row number
    for row in rows:
        control = int(row[0])
        break

    # check if there are rows when the table "plaza_interpro" exists
    if control == 1:

        # select the row number
        sentence = f'''
                    SELECT EXISTS
                        (SELECT 1
                            FROM plaza_interpro
                            where  dataset_id = '{dataset_id}'
                            LIMIT 1);
                    '''
        try:
            rows = conn.execute(sentence)
        except Exception as e:
            raise xlib.ProgramException('B002', e, sentence, conn)

        # get the row number
        for row in rows:
            control = int(row[0])
            break

    # return the row number
    return control

#-------------------------------------------------------------------------------

def get_interpro_dict(conn, dataset_id, gene_id):
    '''
    Get a dictionary of annotation data corresponding to rows with a dataset identification and a gene identification from the table "plaza_interpro".
    '''

    # initialize the Interpro dictionary
    interpro_dict = {}

    # initialize the dictionary key
    key = 0

    # select rows from the table "plaza_interpro"
    sentence = f'''
                SELECT DISTINCT plaza_species_id, motif_id, desc
                    FROM plaza_interpro
                    WHERE dataset_id = '{dataset_id}'
                      AND gene_id = '{gene_id}';
                '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # add annotation data to list
    for row in rows:
        interpro_dict[key] = {'plaza_species_id':row[0], 'motif_id':row[1], 'desc':row[2]}
        key += 1

    # return the Interpro dictionary
    return interpro_dict

#-------------------------------------------------------------------------------
# table "plaza_mapman"
#-------------------------------------------------------------------------------

def create_plaza_mapman(conn):
    '''
    Create the table "plaza_mapman" (if it does not exist).
    '''

    sentence = '''
               CREATE TABLE IF NOT EXISTS plaza_mapman (
                   dataset_id       TEXT NOT NULL,
                   plaza_species_id TEXT NOT NULL,
                   gene_id          TEXT NOT NULL,
                   mapman_id        TEXT NOT NULL,
                   desc             TEXT NOT NULL);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_plaza_mapman_index(conn):
    '''
    Create the index "plaza_mapman_index" (if it does not exist) with the columns "dataset_id" and "gene_id" on the table "plaza_mapman".
    '''
    
    sentence = '''
               CREATE INDEX IF NOT EXISTS plaza_mapman_index
                   ON plaza_mapman (dataset_id, gene_id);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def insert_plaza_mapman_row(conn, row_dict):
    '''
    Insert a row into table "plaza_mapman".
    '''

    sentence = f'''
                INSERT INTO plaza_mapman
                    (dataset_id, plaza_species_id, gene_id, mapman_id, desc)
                    VALUES ('{row_dict["dataset_id"]}', '{row_dict["plaza_species_id"]}', '{row_dict["gene_id"]}', '{row_dict["mapman_id"]}', '{row_dict["desc"]}');
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def delete_plaza_mapman_rows(conn, dataset_id, species_id):
    '''
    Delete rows from table "plaza_mapman" corresponding to the dataset identification and, optionally, the PLAZA species identification.
    '''
    
    if species_id == 'all':
        sentence = f'''
                    DELETE FROM plaza_mapman
                        WHERE dataset_id = '{dataset_id}';
                    '''
    else:
        sentence = f'''
                    DELETE FROM plaza_mapman
                        WHERE dataset_id = '{dataset_id}'
                          AND plaza_species_id = '{species_id}';
                    '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def check_plaza_mapman(conn, dataset_id):
    '''
    Check if table "plaza_mapman" exists and if there are rows corresponding to a dataset.
    '''

    # check if table "plaza_mapman" exists
    sentence = '''
               SELECT EXISTS
                   (SELECT 1
                       FROM sqlite_master
                       WHERE type = 'table'
                         AND tbl_name = 'plaza_mapman'
                       LIMIT 1);
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # get the row number
    for row in rows:
        control = int(row[0])
        break

    # check if there are rows when the table "plaza_mapman" exists
    if control == 1 and dataset_id == 'gymno_01':

        # select the row number
        sentence = f'''
                    SELECT EXISTS
                        (SELECT 1
                            FROM plaza_mapman
                            where  dataset_id = '{dataset_id}'
                            LIMIT 1);
                    '''
        try:
            rows = conn.execute(sentence)
        except Exception as e:
            raise xlib.ProgramException('B002', e, sentence, conn)

        # get the row number
        for row in rows:
            control = int(row[0])
            break

    # return the row number
    return control

#-------------------------------------------------------------------------------

def get_mapman_dict(conn, dataset_id, gene_id):
    '''
    Get a dictionary of annotation data corresponding to rows with a dataset identification and a gene identification from the table "plaza_mapman".
    '''

    # initialize the Gene Ontology dictionary
    mapman_dict = {}


    # initialize the dictionary key
    key = 0

    # select rows from the table "plaza_mapman"
    sentence = f'''
                SELECT DISTINCT plaza_species_id, mapman_id, desc 
                    FROM plaza_mapman
                    WHERE dataset_id = '{dataset_id}'
                      AND gene_id = '{gene_id}';
                '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # add annotation data to list
    for row in rows:
        mapman_dict[key] = {'plaza_species_id':row[0], 'mapman_id':row[1], 'desc':row[2]}
        key += 1

    # return the Gene Ontology dictionary
    return mapman_dict

#-------------------------------------------------------------------------------
# table "species"
#-------------------------------------------------------------------------------

def drop_species(conn):
    '''
    Drop the table "species" (if it exists).
    '''

    sentence = '''
               DROP TABLE IF EXISTS species;
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_species(conn):
    '''
    Create table "species".
    '''
    
    sentence = '''
               CREATE TABLE species (
                   species_name      TEXT UNIQUE,
                   family_name       TEXT NOT NULL,
                   phylum_name       TEXT NOT NULL,
                   kingdom_name      TEXT NOT NULL,
                   superkingdom_name TEXT NOT NULL,
                   tax_id            TEXT NOT NULL,
                   plaza_species_id  TEXT NOT NULL);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def create_species_index(conn):
    '''
    Create the unique index "species_index" with the column "species_name" on the table "species".
    '''
    
    sentence = '''
               CREATE UNIQUE INDEX species_index
                   ON species (species_name);
               '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def insert_species_row(conn, row_dict):
    '''
    Insert a row into table "species".
    '''

    sentence = f'''
                INSERT INTO species
                    (species_name, family_name, phylum_name, kingdom_name, superkingdom_name, tax_id, plaza_species_id)
                    VALUES ('{row_dict["species_name"]}', '{row_dict["family_name"]}', '{row_dict["phylum_name"]}', '{row_dict["kingdom_name"]}', '{row_dict["superkingdom_name"]}', '{row_dict["tax_id"]}', '{row_dict["plaza_species_id"]}');
                '''
    try:
        conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

#-------------------------------------------------------------------------------

def check_species(conn):
    '''
    Check if table "species" exists and if there are rows.
    '''

    # check if table "species" exists
    sentence = '''
               SELECT EXISTS
                   (SELECT 1
                       FROM sqlite_master
                       WHERE type = 'table'
                         AND tbl_name = 'species'
                       LIMIT 1);
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # get the row number
    for row in rows:
        control = int(row[0])
        break

    # check if there are rows when the table "species" exists
    if control == 1:

        # select the row number
        sentence = '''
                   SELECT EXISTS
                       (SELECT 1
                           FROM species
                           LIMIT 1);
                   '''
        try:
            rows = conn.execute(sentence)
        except Exception as e:
            raise xlib.ProgramException('B002', e, sentence, conn)

        # get the row number
        for row in rows:
            control = int(row[0])
            break

    # return the row number
    return control

#-------------------------------------------------------------------------------

def get_plaza_species_id_list(conn):
    '''
    Get a list of species identification corresponding to rows with PLAZA identification not equal to "N/A" from the table "species".
    '''

    # initialize PLAZA species identification list
    plaza_species_id_list = []

    # select the PLAZA species identification from the table "species"
    sentence = f'''
                SELECT plaza_species_id
                    FROM species
                    WHERE plaza_species_id <> "{xlib.get_na()}";
                '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # add PLAZA species identifications to list
    for row in rows:
        plaza_id = row[0]
        plaza_species_id_list.append(plaza_id)

    # return PLAZA species identification list
    return plaza_species_id_list

#-------------------------------------------------------------------------------

def get_species_dict(conn):
    '''
    Get a species dictionary from the table "species".
    '''

    # initialize the species dictionary
    species_dict = {}

    # select rows from the table "species"
    sentence = '''
               SELECT species_name, family_name, phylum_name, kingdom_name, superkingdom_name, tax_id, plaza_species_id
                   FROM species;
               '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # add row data to the dictionary
    for row in rows:
        species_dict[row[0]] = {'species_name': row[0], 'family_name': row[1], 'phylum_name': row[2], 'kingdom_name': row[3], 'superkingdom_name': row[4], 'tax_id': row[5], 'plaza_species_id': row[6]}

    # return the species dictionary
    return species_dict

#-------------------------------------------------------------------------------

def get_plaza_species_dict(conn):
    '''
    Get a species dictionary corresponding to rows with PLAZA identification not equal to "N/A" from the table "species".
    '''

    # initialize the PLAZA species dictionary
    plaza_species_dict = {}

    # select rows from the table "species"
    sentence = f'''
                SELECT species_name, family_name, phylum_name, kingdom_name, superkingdom_name, tax_id, plaza_species_id
                    FROM species
                    WHERE plaza_species_id <> "{xlib.get_na()}";
                '''
    try:
        rows = conn.execute(sentence)
    except Exception as e:
        raise xlib.ProgramException('B002', e, sentence, conn)

    # add row data to the dictionary
    for row in rows:
        plaza_species_dict[row[6]] = {'species_name': row[0], 'family_name': row[1], 'phylum_name': row[2], 'kingdom_name': row[3], 'superkingdom_name': row[4], 'tax_id': row[5], 'plaza_species_id': row[6]}

    # return the PLAZA species dictionary
    return plaza_species_dict

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print('This source contains general functions for the maintenance of the TOA SQLite database in both console mode and gui mode.')
    sys.exit(0)

#-------------------------------------------------------------------------------
