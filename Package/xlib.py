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
This source contains general functions and classes used in TOA
software package used in both console mode and gui mode.
'''

#-------------------------------------------------------------------------------

import configparser
import datetime
import os
import re
import requests
import subprocess
import sys

import xsqlite

#-------------------------------------------------------------------------------
    
def get_project_code():
    '''
    Get the project code.
    '''

    return 'toa'

#-------------------------------------------------------------------------------
    
def get_long_project_name():
    '''
    Get the project name.
    '''

    return 'TOA (Tree-oriented Annotation)'

#-------------------------------------------------------------------------------
    
def get_short_project_name():
    '''
    Get the project name.
    '''

    return 'TOA'

#-------------------------------------------------------------------------------

def get_project_version():
    '''
    Get the project version.
    '''

    return '0.56'

#-------------------------------------------------------------------------------
    
def get_project_manual_file():
    '''
    Get the project name.
    '''

    return './TOA-manual.pdf'

#-------------------------------------------------------------------------------
    
def get_project_image_file():
    '''
    Get the project name.
    '''

    return './image_TOA.png'

#-------------------------------------------------------------------------------

def check_os():
    '''
    Check the operating system.
    '''    

    # if the operating system is unsupported, exit with exception
    if not sys.platform.startswith('linux') and not sys.platform.startswith('darwin') and not sys.platform.startswith('win32') and not sys.platform.startswith('cygwin'):
        raise ProgramException('S001', sys.platform)

#-------------------------------------------------------------------------------

def get_editor():
    '''
    Get the editor depending on the Operating System.
    '''

    # assign the editor
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        editor = 'nano'
    elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
        editor = 'notepad'

    # return the editor
    return editor

#-------------------------------------------------------------------------------

def get_os_size_fix():
    '''
    Get the size fix of the button line in a GUI form.
    '''

    # assign the size fix
    if sys.platform.startswith('linux'):
        os_size_fix = 0
    elif sys.platform.startswith('darwin'):
        os_size_fix = 0
    elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
        os_size_fix = 20

    # return the size fix
    return os_size_fix

#-------------------------------------------------------------------------------

def get_na():
    '''
    Get the characters to represent not available.
    '''

    return 'N/A'

#-------------------------------------------------------------------------------

def get_separator():
    '''
    Get the separation line between process steps.
    '''

    return '**************************************************'

#-------------------------------------------------------------------------------

def get_config_dir():
    '''
    Get the configuration directory.
    '''

    return './config'

#-------------------------------------------------------------------------------

def get_result_dir():
    '''
    Get the result directory.
    '''

    return './results'

#-------------------------------------------------------------------------------

def get_temp_dir():
    '''
    Get the temporal directory.
    '''

    return './temp'

#-------------------------------------------------------------------------------

def get_log_dir():
    '''
    Get the temporal directory.
    '''

    return './logs'

#-------------------------------------------------------------------------------

def get_current_run_dir(result_dir, group, process):
    '''
    Get the run directory of a process.
    '''

    # set the run identificacion
    now = datetime.datetime.now()
    date = datetime.datetime.strftime(now, '%y%m%d')
    time = datetime.datetime.strftime(now, '%H%M%S')
    run_id = '{0}-{1}-{2}'.format(process, date, time)

    # set the current run directory
    current_run_dir = '{0}/{1}/{2}'.format(result_dir, group, run_id)

    # return the run directory
    return current_run_dir

#-------------------------------------------------------------------------------

def get_status_dir(current_run_dir):
    '''
    Get the status directory of a process.
    '''

    # set the status directory
    status_dir = '{0}/status'.format(current_run_dir)

    # return the status directory
    return status_dir

#-------------------------------------------------------------------------------

def get_status_ok(current_run_dir):
    '''
    Get the OK status file.
    '''

    # set the OK status file
    ok_status = '{0}/status/script.ok'.format(current_run_dir)

    # return the OK status file
    return ok_status

#-------------------------------------------------------------------------------

def get_status_wrong(current_run_dir):
    '''
    Get the WRONG status file.
    '''

    # set the WRONG status file
    wrong_status = '{0}/status/script.wrong'.format(current_run_dir)

    # return the WRONG status file
    return wrong_status

#-------------------------------------------------------------------------------

def get_run_log_file():
    '''
    Get the log file name of a process run.
    '''

    return 'log.txt'

#-------------------------------------------------------------------------------

def get_submission_log_file(function_name):
    '''
    Get the log file name of a process submission.
    '''
    # set the log file name
    now = datetime.datetime.now()
    date = datetime.datetime.strftime(now, '%y%m%d')
    time = datetime.datetime.strftime(now, '%H%M%S')
    log_file_name = '{0}/{1}-{2}-{3}.txt'.format(get_log_dir(), function_name, date, time)

    # return the log file name
    return log_file_name

#-------------------------------------------------------------------------------

def list_log_files_command(local_process_id):
    '''
    Get the command to list log files depending on the Operating System.
    '''
    # get log dir
    log_dir = get_log_dir()

    # assign the command
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        if local_process_id == 'all':
            command = 'ls {0}/*.txt'.format(log_dir)
        else:
            command = 'ls {0}/{1}-*.txt'.format(log_dir, local_process_id)
    elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
        log_dir = log_dir.replace('/', '\\')
        if local_process_id == 'all':
            command = 'dir /B {0}\*.txt'.format(log_dir)
        else:
            command = 'dir /B {0}\{1}-*.txt'.format(log_dir, local_process_id)

    # return the command
    return command

#-------------------------------------------------------------------------------

def get_submission_process_dict():
    '''
    Get the submission process dictionary.
    '''

    # build the submission process dictionary
    submission_process_dict = {}
    submission_process_dict['manage_genomic_database']= {'text': 'Manage genomic database processes'}
    submission_process_dict['manage_toa_database']= {'text': 'Manage {0} database'.format(get_toa_name())}
    submission_process_dict['manage_toa_pipeline']= {'text': 'Manage {0} pipelines'.format(get_toa_name())}
    submission_process_dict['restart_pipeline_process']= {'text': 'Restart {0} process'.format(get_toa_pipeline_name())}
    submission_process_dict['run_pipeline_process']= {'text': 'Run {0} process'.format(get_toa_pipeline_name())}
    submission_process_dict['setup_bioconda_package_list']= {'text': 'Set up Bioconda package list'}
    submission_process_dict['setup_miniconda3']= {'text': 'Set up {0}'.format(get_miniconda3_name())}
    submission_process_dict['setup_r']= {'text': 'Set up {0}'.format(get_r_name())}

    # return the submission process dictionary
    return submission_process_dict

#-------------------------------------------------------------------------------

def get_submission_process_id(submission_process_text):
    '''
    Get the submission process identification from the submission process text.
    '''

    # initialize the control variable
    submission_process_id_found = None

    # get the dictionary of the submission processes
    submission_process_dict = get_submission_process_dict()

    # search the submission process identification
    for submission_process_id in submission_process_dict.keys():
        if submission_process_dict[submission_process_id]['text'] == submission_process_text:
            submission_process_id_found = submission_process_id
            break

    # return the submission process identification
    return submission_process_id_found

#-------------------------------------------------------------------------------

def get_all_applications_selected_code():
    '''
    Get the code that means all applications.
    '''

    return 'all_applications_selected'

#-------------------------------------------------------------------------------

def get_bioconda_code():
    '''
    Get the Bioconda code used to identify its processes.
    '''

    return 'bioconda'

#-------------------------------------------------------------------------------

def get_bioconda_name():
    '''
    Get the Bioconda name used to title.
    '''

    return 'Bioconda'

#-------------------------------------------------------------------------------

def get_blastplus_code():
    '''
    Get the BLAST+ code used to identify its processes.
    '''

    return 'blast'

#-------------------------------------------------------------------------------

def get_blastplus_name():
    '''
    Get the BLAST+ name used to title.
    '''

    return 'BLAST+'

#-------------------------------------------------------------------------------

def get_blastplus_bioconda_code():
    '''
    Get the BLAST+ code used to identify the Bioconda package.
    '''

    return 'blast'

#-------------------------------------------------------------------------------

def get_entrez_direct_code():
    '''
    Get the Entrez Direct code used to identify its processes.
    '''

    return 'edirect'

#-------------------------------------------------------------------------------

def get_entrez_direct_name():
    '''
    Get the Entrez Direct name used to title.
    '''

    return 'Entrez Direct'

#-------------------------------------------------------------------------------

def get_entrez_direct_bioconda_code():
    '''
    Get the Entrez Direct code used to the Bioconda package.
    '''

    return 'entrez-direct'

#-------------------------------------------------------------------------------

def get_miniconda3_code():
    '''
    Get the Miniconda3 code used to identify its processes.
    '''

    return 'miniconda3'

#-------------------------------------------------------------------------------

def get_miniconda3_name():
    '''
    Get the Miniconda3 name used to title.
    '''

    return 'Miniconda3'

#-------------------------------------------------------------------------------

def get_miniconda3_url():
    '''
    Get the Miniconda3 URL.
    '''

    # assign the Miniconda 3 URL
    if sys.platform.startswith('linux'):
        miniconda3_url = 'https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh'
    elif sys.platform.startswith('darwin'):
        miniconda3_url = 'https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh'

    # return the Miniconda 3 URL
    return miniconda3_url

#-------------------------------------------------------------------------------

def get_r_code():
    '''
    Get the R code used to identify its processes.
    '''

    return 'r'

#-------------------------------------------------------------------------------

def get_r_name():
    '''
    Get the R name used to title.
    '''

    return 'R'

#-------------------------------------------------------------------------------

def get_toa_code():
    '''
    Get the TOA code used to identify its processes.
    '''

    return 'toa'

#-------------------------------------------------------------------------------

def get_toa_name():
    '''
    Get the TOA name used to title.
    '''

    return 'TOA'

#-------------------------------------------------------------------------------

def get_toa_data_basic_data_code():
    '''
    Get the code used to identify basic data in TOA processes.
    '''

    return 'basic data'

#-------------------------------------------------------------------------------

def get_toa_data_basic_data_name():
    '''
    Get the code used to title basic data in TOA processes.
    '''

    return 'basic data'

#-------------------------------------------------------------------------------

def get_toa_data_dicots_04_code():
    '''
    Get the code used to identify Dicots PLAZA 4.0 in TOA processes.
    '''

    return 'dicots_04'

#-------------------------------------------------------------------------------

def get_toa_data_dicots_04_name():
    '''
    Get the code used to identify Dicots PLAZA 4.0 in TOA processes.
    '''

    return 'Dicots PLAZA 4.0'

#-------------------------------------------------------------------------------

def get_toa_data_gene_code():
    '''
    Get the code used to title NCBI Gene in TOA processes.
    '''

    return 'gene'

#-------------------------------------------------------------------------------

def get_toa_data_gene_name():
    '''
    Get the code used to identify NCBI Gene in TOA processes.
    '''

    return 'NCBI Gene'

#-------------------------------------------------------------------------------

def get_toa_data_go_code():
    '''
    Get the code used to identify Gene Ontology in TOA processes.
    '''

    return 'go'

#-------------------------------------------------------------------------------

def get_toa_data_go_name():
    '''
    Get the code used to title Gene Ontology in TOA processes.
    '''

    return 'Gene Ontology'

#-------------------------------------------------------------------------------

def get_toa_data_gymno_01_code():
    '''
    Get the code used to identify Gymno PLAZA 1.0 in TOA processes.
    '''

    return 'gymno_01'

#-------------------------------------------------------------------------------

def get_toa_data_gymno_01_name():
    '''
    Get the code used to title Gymno PLAZA 1.0 in TOA processes.
    '''

    return 'Gymno PLAZA 1.0'

#-------------------------------------------------------------------------------

def get_toa_data_interpro_code():
    '''
    Get the code used to title InterPro in TOA processes.
    '''

    return 'interpro'

#-------------------------------------------------------------------------------

def get_toa_data_interpro_name():
    '''
    Get the code used to title InterPro in TOA processes.
    '''

    return 'InterPro'

#-------------------------------------------------------------------------------

def get_toa_data_monocots_04_code():
    '''
    Get the code used to identify Monocots PLAZA 4.0 in TOA processes.
    '''

    return 'monocots_04'

#-------------------------------------------------------------------------------

def get_toa_data_monocots_04_name():
    '''
    Get the code used to title Monocots PLAZA 4.0 in TOA processes.
    '''

    return 'Monocots PLAZA 4.0'

#-------------------------------------------------------------------------------

def get_toa_data_nr_code():
    '''
    Get the code used to identify NCBI BLAST database NR in TOA processes.
    '''

    return 'nr'

#-------------------------------------------------------------------------------

def get_toa_data_nr_name():
    '''
    Get the code used to title NCBI BLAST database NR in TOA processes.
    '''

    return 'NCBI BLAST database NR'

#-------------------------------------------------------------------------------

def get_toa_data_nt_code():
    '''
    Get the code used to identify NCBI BLAST database NT in TOA processes.
    '''

    return 'nt'

#-------------------------------------------------------------------------------

def get_toa_data_nt_name():
    '''
    Get the code used to title NCBI BLAST database NT in TOA processes.
    '''

    return 'NCBI BLAST database NT'

#-------------------------------------------------------------------------------

def get_toa_data_refseq_plant_code():
    '''
    Get the code used to identify NCBI RefSeq Plant in TOA processes.
    '''

    return 'refseq_plant'

#-------------------------------------------------------------------------------

def get_toa_data_refseq_plant_name():
    '''
    Get the name used to title NCBI RefSeq Plant in TOA processes.
    '''

    return 'NCBI RefSeq Plant'

#-------------------------------------------------------------------------------

def get_toa_data_viridiplantae_nucleotide_gi_code():
    '''
    Get the code used to identify NCBI Nucleotide GenInfo viridiplantae identifier list in TOA processes.
    '''

    return 'viridiplantae_nucleotide_gi'

#-------------------------------------------------------------------------------

def get_toa_data_viridiplantae_nucleotide_gi_name():
    '''
    Get the code used to title NCBI Nucleotide GenInfo viridiplantae identifier list in TOA processes.
    '''

    return 'NCBI Nucleotide GenInfo viridiplantae identifier list'

#-------------------------------------------------------------------------------

def get_toa_data_viridiplantae_protein_gi_code():
    '''
    Get the code used to identify NCBI Protein GenInfo viridiplantae identifier list in TOA processes.
    '''

    return 'viridiplantae_protein_gi'

#-------------------------------------------------------------------------------

def get_toa_data_viridiplantae_protein_gi_name():
    '''
    Get the code used to title NCBI Protein GenInfo viridiplantae identifier list in TOA processes.
    '''

    return 'NCBI Protein GenInfo viridiplantae identifier list'

#-------------------------------------------------------------------------------

def get_toa_process_blastdb_nr_code():
    '''
    Get the code of the BLAST database NR build process used to identify its processes.
    '''

    return 'toabbnr'

#-------------------------------------------------------------------------------

def get_toa_process_blastdb_nr_name():
    '''
    Get the name of the BLAST database NR build process used to title.
    '''

    return 'Build BLAST database NR'

#-------------------------------------------------------------------------------

def get_toa_process_blastdb_nt_code():
    '''
    Get the code of the BLAST database NT build process used to identify its processes.
    '''

    return 'toabbnt'

#-------------------------------------------------------------------------------

def get_toa_process_blastdb_nt_name():
    '''
    Get the name of the BLAST database NT build process used to title.
    '''

    return 'Build BLAST database NT'

#-------------------------------------------------------------------------------

def get_toa_process_download_basic_data_code():
    '''
    Get the code used to identify processes to download Gene Ontology functional annotations.
    '''

    return 'toaddbasic'

#-------------------------------------------------------------------------------

def get_toa_process_download_basic_data_name():
    '''
    Get the name used to title processes to download Gene Ontology functional annotations.
    '''

    return 'Download basic data'

#-------------------------------------------------------------------------------

def get_toa_process_download_dicots_04_code():
    '''
    Get the code used to identify processes to download Dicots PLAZA 4.0 functional annotations.
    '''

    return 'toadddicots04'

#-------------------------------------------------------------------------------

def get_toa_process_download_dicots_04_name():
    '''
    Get the name used to title processes to download Dicots PLAZA 4.0 functional annotations.
    '''

    return 'Download Dicots PLAZA 4.0 funcional annotations'

#-------------------------------------------------------------------------------

def get_toa_process_download_gene_code():
    '''
    Get the code used to identify processes to download NCBI Gene functional annotations.
    '''

    return 'toaddgene'

#-------------------------------------------------------------------------------

def get_toa_process_download_gene_name():
    '''
    Get the name used to title processes to download NCBI Gene functional annotations.
    '''

    return 'Download NCBI Gene funcional annotations'

#-------------------------------------------------------------------------------

def get_toa_process_download_go_code():
    '''
    Get the code used to identify processes to download Gene Ontology functional annotations.
    '''

    return 'toaddgo'

#-------------------------------------------------------------------------------

def get_toa_process_download_go_name():
    '''
    Get the name used to title processes to download Gene Ontology functional annotations.
    '''

    return 'Download Gene Ontology funcional annotations'

#-------------------------------------------------------------------------------

def get_toa_process_download_gymno_01_code():
    '''
    Get the code used to identify processes to download Gymno PLAZA 1.0 functional annotations.
    '''

    return 'toaddgymno01'

#-------------------------------------------------------------------------------

def get_toa_process_download_gymno_01_name():
    '''
    Get the name used to title processes to download Gymno PLAZA 1.0 functional annotations.
    '''

    return 'Download Gymno PLAZA 1.0 funcional annotations'

#-------------------------------------------------------------------------------

def get_toa_process_download_interpro_code():
    '''
    Get the code used to identify process to download InterPro functional annotations.
    '''

    return 'toaddinterpro'

#-------------------------------------------------------------------------------

def get_toa_process_download_interpro_name():
    '''
    Get the name used to title process to download InterPro functional annotations.
    '''

    return 'Download InterPro funcional annotations'

#-------------------------------------------------------------------------------

def get_toa_process_download_monocots_04_code():
    '''
    Get the code used to identify process to download Monocots PLAZA 4.0 functional annotations.
    '''

    return 'toaddmonocots04'

#-------------------------------------------------------------------------------

def get_toa_process_download_monocots_04_name():
    '''
    Get the name used to title process to download Monocots PLAZA 4.0 functional annotations.
    '''

    return 'Download Monocots PLAZA 4.0 funcional annotations'

#-------------------------------------------------------------------------------

def get_toa_process_gilist_viridiplantae_nucleotide_gi_code():
    '''
    Get the code used to identifiy processes to build the NCBI Nucleotide GenInfo viridiplantae identifier list.
    '''

    return 'toablvpntgi'

#-------------------------------------------------------------------------------

def get_toa_process_gilist_viridiplantae_nucleotide_gi_name():
    '''
    Get the name used to title processes to build the NCBI Nucleotide GenInfo viridiplantae identifier list.
    '''

    return 'Build NCBI Nucleotide GenInfo viridiplantae identifier list'

#-------------------------------------------------------------------------------

def get_toa_process_gilist_viridiplantae_protein_gi_code():
    '''
    Get the code used to identify processes to build the NCBI Protein GenInfo viridiplantae identifier list.
    '''

    return 'toablvpprgi'

#-------------------------------------------------------------------------------

def get_toa_process_gilist_viridiplantae_protein_gi_name():
    '''
    Get the name used to title processes to build the NCBI Protein GenInfo viridiplantae identifier list.
    '''

    return 'Build NCBI Protein GenInfo viridiplantae identifier list'

#-------------------------------------------------------------------------------

def get_toa_process_load_basic_data_code():
    '''
    Get the code used to identify processes to load basic data.
    '''

    return 'toaldbasic'

#-------------------------------------------------------------------------------

def get_toa_process_load_basic_data_name():
    '''
    Get the name to title processes to load basic data.
    '''

    return 'Load basic data into TOA database'

#-------------------------------------------------------------------------------

def get_toa_process_load_dicots_04_code():
    '''
    Get the code used to identify processes to load the Dicots PLAZA 4.0  data.
    '''

    return 'toalddicots04'

#-------------------------------------------------------------------------------

def get_toa_process_load_dicots_04_name():
    '''
    Get the name used to title processes to load the Dicots PLAZA 4.0  data.
    '''

    return 'Load Dicots PLAZA 4.0  data into TOA database'

#-------------------------------------------------------------------------------

def get_toa_process_load_gene_code():
    '''
    Get the code used to identify processes to load the NCBI Gene data load.
    '''

    return 'toaldgene'

#-------------------------------------------------------------------------------

def get_toa_process_load_gene_name():
    '''
    Get the name used to title processes to load the NCBI Gene data load.
    '''

    return 'Load NCBI Gene data into TOA database'

#-------------------------------------------------------------------------------

def get_toa_process_load_go_code():
    '''
    Get the code used to identify processes to load the Gene Ontology data.
    '''

    return 'toaldgo'

#-------------------------------------------------------------------------------

def get_toa_process_load_go_name():
    '''
    Get the name used to title processes to load the Gene Ontology data.
    '''

    return 'Load Gene Ontology data into TOA database'

#-------------------------------------------------------------------------------

def get_toa_process_load_gymno_01_code():
    '''
    Get the code used to identify processes to load the Gymno PLAZA 1.0 data.
    '''

    return 'toaldgymno01'

#-------------------------------------------------------------------------------

def get_toa_process_load_gymno_01_name():
    '''
    Get the name used to title processes to load the Gymno PLAZA 1.0 data.
    '''

    return 'Load Gymno PLAZA 1.0 data into TOA database'

#-------------------------------------------------------------------------------

def get_toa_process_load_interpro_code():
    '''
    Get the code used to identify processes to load the Interpro data.
    '''

    return 'toaldinterpro'

#-------------------------------------------------------------------------------

def get_toa_process_load_interpro_name():
    '''
    Get the name used to title processes to load the Interpro data.
    '''

    return 'Load Interpro data into TOA database'

#-------------------------------------------------------------------------------

def get_toa_process_load_monocots_04_code():
    '''
    Get the code used to identify processes to load the Monocots PLAZA 4.0 data.
    '''

    return 'toaldmonocots04'

#-------------------------------------------------------------------------------

def get_toa_process_load_monocots_04_name():
    '''
    Get the name used to title processes to load the Monocots PLAZA 4.0 data.
    '''

    return 'Load Monocots PLAZA 4.0 data into TOA database'

#-------------------------------------------------------------------------------

def get_toa_process_pipeline_aminoacid_code():
    '''
    Get the code used to identify amino acid pipelines.
    '''

    return 'toapipelineaa'

#-------------------------------------------------------------------------------

def get_toa_process_pipeline_aminoacid_name():
    '''
    Get the name used to title amino acid pipelines.
    '''

    return 'amino acid pipeline'

#-------------------------------------------------------------------------------

def get_toa_process_pipeline_nucleotide_code():
    '''
    Get the code used to identify nucleotide pipelines.
    '''

    return 'toapipelinent'

#-------------------------------------------------------------------------------

def get_toa_process_pipeline_nucleotide_name():
    '''
    Get the name used to title nucleotide pipelines.
    '''

    return 'nucleotide pipeline'

#-------------------------------------------------------------------------------

def get_toa_process_proteome_dicots_04_code():
    '''
    Get the code used to identify processes to build the Dicots PLAZA 4.0 proteome.
    '''

    return 'toabpdicots04'

#-------------------------------------------------------------------------------

def get_toa_process_proteome_dicots_04_name():
    '''
    Get the name used to title processes to build the Dicots PLAZA 4.0 proteome.
    '''

    return 'Build Dicots PLAZA 4.0 proteome'

#-------------------------------------------------------------------------------

def get_toa_process_proteome_gymno_01_code():
    '''
    Get the code used to identify processes to build the Gymno PLAZA 1.0 proteome.
    '''

    return 'toabpgymno01'

#-------------------------------------------------------------------------------

def get_toa_process_proteome_gymno_01_name():
    '''
    Get the name to title processes to build the Gymno PLAZA 1.0 proteome.
    '''

    return 'Build Gymno PLAZA 1.0 proteome'

#-------------------------------------------------------------------------------

def get_toa_process_proteome_monocots_04_code():
    '''
    Get the code used to identify processes to build the Monocots PLAZA 4.0 proteome.
    '''

    return 'toabpmonocots04'

#-------------------------------------------------------------------------------

def get_toa_process_proteome_monocots_04_name():
    '''
    Get the name used to title processes to build the Monocots PLAZA 4.0 proteome.
    '''

    return 'Build Monocots PLAZA 4.0 proteome'

#-------------------------------------------------------------------------------

def get_toa_process_proteome_refseq_plant_code():
    '''
    Get the code used to identify processes to build the NCBI RefSeq Plant proteome.
    '''

    return 'toabprefseqplt'

#-------------------------------------------------------------------------------

def get_toa_process_proteome_refseq_plant_name():
    '''
    Get the name used to title processes to build the NCBI RefSeq Plant proteome.
    '''

    return 'Build NCBI RefSeq Plant proteome'

#-------------------------------------------------------------------------------

def get_toa_process_recreate_toa_database_code():
    '''
    Get the code used to identify processes to recreate the TOA database.
    '''

    return 'toarecreatedb'

#-------------------------------------------------------------------------------

def get_get_toa_process_recreate_toa_database_name():
    '''
    Get the name used to title processes to recreate the TOA database.
    '''

    return 'Recreate TOA database'

#-------------------------------------------------------------------------------

def get_toa_process_rebuild_toa_database_code():
    '''
    Get the code used to identify processes to rebuild the TOA database.
    '''

    return 'toarebuilddb'

#-------------------------------------------------------------------------------

def get_get_toa_process_rebuild_toa_database_name():
    '''
    Get the name used to title processes to rebuild the TOA database.
    '''

    return 'Rebuild TOA database'

#-------------------------------------------------------------------------------

def get_toa_pipeline_name():
    '''
    Get the name used to title nucleotide or amino acid pipelines.
    '''

    return 'TOA nucleotide or amino acid pipeline'

#-------------------------------------------------------------------------------

def get_toa_result_database_dir():
    '''
    Get the result subdirectory where TOA process results related to the genomic database managment are saved.
    '''

    return 'TOA-databases'

#-------------------------------------------------------------------------------

def get_toa_result_pipeline_dir():
    '''
    Get the result subdirectory where TOA process results related to pipelines are saved.
    '''

    return 'TOA-pipelines'

#-------------------------------------------------------------------------------

def get_toa_type_build_blastdb():
    '''
    Get the code used to identify processes to build BLAST databases.
    '''

    return 'build_blastdb'

#-------------------------------------------------------------------------------

def get_toa_type_build_gilist():
    '''
    Get the code used to identify processes to build GeneId identifier list.
    '''

    return 'build_gilist'

#-------------------------------------------------------------------------------

def get_toa_type_build_proteome():
    '''
    Get the code used to identify processes to build proteomes.
    '''

    return 'build_proteome'

#-------------------------------------------------------------------------------

def get_toa_type_download_data():
    '''
    Get the code used to identify processes to download functional annotations from a genomic database server.
    '''

    return 'download_data'

#-------------------------------------------------------------------------------

def get_toa_type_load_data():
    '''
    Get the code used to identify processes to load data of a genomic database into TOA database.
    '''

    return 'load_data'

#-------------------------------------------------------------------------------

def get_toa_type_rebuild():
    '''
    Get the code used to identify processes to rebuild the TOA database.
    '''

    return 'rebuild'

#-------------------------------------------------------------------------------

def get_toa_type_recreate():
    '''
    Get the code used to identify processes to recreate the TOA database.
    '''

    return 'recreate'

#-------------------------------------------------------------------------------

def get_transdecoder_code():
    '''
    Get the TransDecoder code used to identify its processes.
    '''

    return 'transdecod'

#-------------------------------------------------------------------------------

def get_transdecoder_name():
    '''
    Get the TransDecoder name used to title.
    '''

    return 'TransDecoder'

#-------------------------------------------------------------------------------

def get_transdecoder_bioconda_code():
    '''
    Get the TransDecoder code used to the Bioconda package.
    '''

    return 'transdecoder'

#-------------------------------------------------------------------------------

def get_option_dict(config_file):
    '''
    Get a dictionary with the options retrieved from a configuration file.
    '''

    # initialize the options dictionary
    option_dict = {}

    # create class to parse the configuration files
    config = configparser.ConfigParser()

    # read the configuration file
    config.read(config_file)

    # build the dictionary
    for section in config.sections():
        # get the keys dictionary
        keys_dict = option_dict.get(section, {})
        # for each key in the section
        for key in config[section]:
            # get the value of the key
            value = config.get(section, key, fallback='')
            # add a new enter in the keys dictionary
            keys_dict[key] = get_option_value(value)
        # update the section with its keys dictionary
        option_dict[section] = keys_dict

    # return the options dictionary
    return option_dict

#-------------------------------------------------------------------------------

def get_option_value(option):
    '''
    Remove comments ans spaces from an option retrieve from a configuration file.
    '''

    # Remove comments
    position = option.find('#')
    if position == -1:
        value = option
    else:
        value = option[:position]

    # Remove comments
    value = value.strip()

    # return the value without comments and spaces
    return value

#-------------------------------------------------------------------------------

def check_startswith(literal, text_list, case_sensitive=False):
    '''
    Check if a literal starts with a text in a list.
    '''

    # initialize the control variable
    OK = False
  
    # initialize the working list
    list = []

    # if the codification is not case sensitive, convert the code and code list to uppercase
    if not case_sensitive:
        try:
            literal = literal.upper()
        except Exception as e:
            pass
        try:
            list = [x.upper() for x in text_list]
        except Exception as e:
            pass
    else:
        list = text_list

    # check if the literal starts with a text in the list
    for text in list:
        if literal.startswith(text):
            OK = True
            break

    # return control variable
    return OK

#-------------------------------------------------------------------------------

def check_code(literal, code_list, case_sensitive=False):
    '''
    Check if a literal is in a code list.
    '''
    
    # initialize the working list
    list = []

    # if the codification is not case sensitive, convert the code and code list to uppercase
    if not case_sensitive:
        try:
            literal = literal.upper()
        except Exception as e:
            pass
        try:
            list = [x.upper() for x in code_list]
        except Exception as e:
            pass
    else:
        list = code_list

    # check if the code is in the code list
    OK = literal in list

    # return control variable
    return OK

#-------------------------------------------------------------------------------

def check_int(literal, minimum=(-sys.maxsize - 1), maximum=sys.maxsize):
    '''
    Check if a numeric or string literal is an integer number.
    '''

    # initialize the control variable
    OK = True
  
    # check the number
    try:
        int(literal)
        int(minimum)
        int(maximum)
    except Exception as e:
        OK = False
    else:
        if int(literal) < int(minimum) or int(literal) > int(maximum):
            OK = False

    # return control variable
    return OK

#-------------------------------------------------------------------------------

def check_float(literal, minimum=float(-sys.maxsize - 1), maximum=float(sys.maxsize), mne=0.0, mxe=0.0):
    '''
    Check if a numeric or string literal is a float number.
    '''

    # initialize the control variable
    OK = True
  
    # check the number
    try:
        float(literal)
        float(minimum)
        float(maximum)
        float(mne)
        float(mxe)
    except Exception as e:
        OK = False
    else:
        if float(literal) < (float(minimum) + float(mne)) or float(literal) > (float(maximum) - float(mxe)):
            OK = False

    # return control variable
    return OK

#-------------------------------------------------------------------------------

def split_literal_to_integer_list(literal):
    '''
    Split a string literal with values are separated by comma in a integer value list.
    '''
  
    # initialize the string values list and the interger values list
    strings_list = []
    integers_list = []
    
    # split the string literal in a string values list
    strings_list = split_literal_to_string_list(literal)

    # convert each value from string to integer
    for i in range(len(strings_list)):
        try:
            integers_list.append(int(strings_list[i]))
        except Exception as e:
            integers_list = []
            break

    # return the integer values list
    return integers_list

#-------------------------------------------------------------------------------

def split_literal_to_float_list(literal):
    '''
    Split a string literal with values are separated by comma in a float value list.
    '''
  
    # initialize the string values list and the float values list
    strings_list = []
    float_list = []
    
    # split the string literal in a string values list
    strings_list = split_literal_to_string_list(literal)

    # convert each value from string to float
    for i in range(len(strings_list)):
        try:
            float_list.append(float(strings_list[i]))
        except Exception as e:
            float_list = []
            break

    # return the float values list
    return float_list

#-------------------------------------------------------------------------------

def split_literal_to_string_list(literal):
    '''
    Split a string literal with values are separated by comma in a string value.
    '''
  
    # initialize the string values list
    string_list = []

    # split the string literal in a string values list
    string_list = literal.split(',')

    # remove the leading and trailing whitespaces in each value
    for i in range(len(string_list)):
        string_list[i] = string_list[i].strip()

    # return the string values list
    return string_list

#-------------------------------------------------------------------------------

def join_string_list_to_string(string_list):
    '''
    Join a string value list in a literal (strings with simple quote and separated by comma).
    '''
  
    # initialize the literal
    literal = ''

    # concat the string items of string_list
    for string in string_list:
        literal = "'{0}'".format(string) if literal == '' else "{0},'{1}'".format(literal, string)

    # return the literal
    return literal

#-------------------------------------------------------------------------------

def is_valid_path(path, operating_system=sys.platform):
    '''
    Check if a path is a valid path.
    '''

    # initialize control variable
    valid = False

    # check if the path is valid
    if operating_system.startswith('linux') or operating_system.startswith('darwin'):
        # -- valid = re.match(r'^(/.+)(/.+)*/?$', path)
        valid = True
    elif operating_system.startswith('win32') or operating_system.startswith('cygwin'):
        valid = True

    # return control variable
    return valid
#-------------------------------------------------------------------------------

def is_absolute_path(path, operating_system=sys.platform):
    '''
    Check if a path is a absolute path.
    '''

    # initialize control variable
    valid = False

    # check if the path is absolute
    if operating_system.startswith('linux') or operating_system.startswith('darwin'):
        if path != '':
            # -- valid = is_path_valid(path) and path[0] == '/'
            valid = True
    elif operating_system.startswith('win32') or operating_system.startswith('cygwin'):
        valid = True

    # return control variable
    return valid

#-------------------------------------------------------------------------------

def run_command(command, log):
    '''
    Run a Bash shell command and redirect stdout and stderr to log.
    '''

    # run the command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    for line in iter(process.stdout.readline, b''):
        # replace non-ASCII caracters by one blank space
        line = re.sub(b'[^\x00-\x7F]+', b' ', line)
        # control return code and new line characters
        if not isinstance(log, DevStdOut):
            line = re.sub(b'\r\n', b'\r', line)
            line = re.sub(b'\r', b'\r\n', line)
        elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            pass
        elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
            line = re.sub(b'\r\n', b'\r', line)
            line = re.sub(b'\r', b'\r\n', line)
        # create a string from the bytes literal
        line = line.decode('utf-8')
        # write the line in log
        log.write('{0}'.format(line))
    rc = process.wait()

    # return the return code of the command run
    return rc

#-------------------------------------------------------------------------------

def get_taxonomy_dict(type, value):
    '''
    Get a taxonomy dictionary with the a species data downloaded from the taxonomy server.
    '''

    # initialize the taxonomy dictionary
    taxonomy_dict = {}

    # set the taxonomy server
    taxonomy_server = 'https://taxonomy.jgi-psf.org/'

    # replace spaces by underscores in value
    value = value.strip().replace(' ', '_')

    # inquire the taxonomy data to the server
    try:
        r = requests.get('{0}/{1}/{2}'.format(taxonomy_server, type, value))
    except requests.exceptions.ConnectionError:
        raise ProgramException('W002', taxonomy_server)
    except Exception as e:
        raise ProgramException('W001', taxonomy_server)

    # build the taxonomy dictionary
    if r.status_code == requests.codes.ok:
        try:
            if r.json()[value].get('error','OK') == 'OK' :
                taxonomy_dict = r.json()[value]
        except Exception as e:
            pass
    else:
        raise ProgramException('W003', taxonomy_server, r.status_code)

    # return taxonomy dictionary
    return taxonomy_dict

#-------------------------------------------------------------------------------

def get_species_data(conn, species_dict, species_name):
    '''
    Get species data from the species dictionary.
    '''

    # initialize the row data dictionary
    row_dict = {}
    row_dict['species_name'] = species_name

    # if species dictionary is empty, load data from the table "species"
    if species_dict == {}:
        species_dict = xsqlite.get_species_dict(conn)

    # get the species taxonomy data
    try:

        row_dict['family_name'] = species_dict[species_name]['family_name']
        row_dict['phylum_name'] = species_dict[species_name]['phylum_name']
        row_dict['kingdom_name'] = species_dict[species_name]['kingdom_name']
        row_dict['superkingdom_name'] = species_dict[species_name]['superkingdom_name']

    except Exception as e:

        # get the taxonomy dictionary of the species name from taxonomy server
        taxonomy_dict = get_taxonomy_dict('name', species_name)
        if taxonomy_dict == {}:
            row_dict['family_name'] = get_na()
            row_dict['phylum_name'] = get_na()
            row_dict['kingdom_name'] = get_na()
            row_dict['superkingdom_name'] = get_na()
            row_dict['tax_id'] = get_na()
            row_dict['plaza_species_id'] = get_na()
        else:
            row_dict['family_name'] = taxonomy_dict.get('family', {}).get('name', get_na())
            row_dict['phylum_name'] = taxonomy_dict.get('phylum', {}).get('name', get_na())
            row_dict['kingdom_name'] = taxonomy_dict.get('kingdom', {}).get('name', get_na())
            row_dict['superkingdom_name'] = taxonomy_dict.get('superkingdom', {}).get('name', get_na())
            row_dict['tax_id'] = taxonomy_dict.get('tax_id', get_na())
            row_dict['plaza_species_id']  = get_na()

        # insert data into the table "species"
        if taxonomy_dict != {}:
            xsqlite.insert_species_row(conn, row_dict)

        # insert data into species dictionary
        species_dict[species_name] = row_dict

        # save changes into TOA database
        conn.commit()

    # return the species taxonomy data
    return species_dict, row_dict['family_name'], row_dict['phylum_name'], row_dict['kingdom_name'], row_dict['superkingdom_name']

#-------------------------------------------------------------------------------

def read_annotation_record(file_name, file_id, type, record_counter):
    '''
    '''

    # initialize the data dictionary
    data_dict = {}

    # initialize the key
    key = None

    # read next record
    record = file_id.readline()

    # if there is record 
    if record != '':

        # remove EOL
        record = record.strip('\n')

        # if type is PLAZA
        if type.upper() == 'PLAZA':

            # extract data 
            # PLAZA record format:  "seq_id";"iteration_iter_num";"hit_num";"hit_accession";"hsp_num";"hsp_evalue";"hsp_identity";"hsp_positive";"hsp_gaps";"hsp_align_len";"hsp_qseq";"species";"family";"phylum";"kingdom";"superkingdom";"desc";"databases";"go_id";"go_desc";"interpro_id";"interpro_desc";"mapman_id";"mapman_desc";"ec_id";"kegg_id";"metacyc_id"
            data_list = []
            start = 0
            for end in [i for i, chr in enumerate(record) if chr == ';']:
                data_list.append(record[start:end].strip('"'))
                start = end + 1
            data_list.append(record[start:].strip('\n').strip('"'))
            try:
                seq_id = data_list[0]
                iteration_iter_num = data_list[1]
                hit_num = data_list[2]
                hit_accession = data_list[3]
                hsp_num = data_list[4]
                hsp_evalue = data_list[5]
                hsp_identity = data_list[6]
                hsp_positive = data_list[7]
                hsp_gaps = data_list[8]
                hsp_align_len = data_list[9]
                hsp_qseq = data_list[10]
                species = data_list[11]
                family = data_list[12]
                phylum = data_list[13]
                kingdom = data_list[14]
                superkingdom = data_list[15]
                desc = data_list[16]
                databases = data_list[17]
                go_id = data_list[18]
                go_desc = data_list[19]
                interpro_id = data_list[20]
                interpro_desc = data_list[21]
                mapman_id = data_list[22]
                mapman_desc = data_list[23]
                ec_id = data_list[24]
                kegg_id = data_list[25]
                metacyc_id = data_list[26]
            except Exception as e:
                raise ProgramException('F006', os.path.basename(file_name), record_counter)

            # set the key
            key = '{0}'.format(seq_id)

            # get the record data dictionary
            data_dict = {'seq_id': seq_id, 'iteration_iter_num': iteration_iter_num, 'hit_num': hit_num, 'hit_accession': hit_accession, 'hsp_num': hsp_num, 'hsp_evalue': hsp_evalue, 'hsp_identity': hsp_identity, 'hsp_positive': hsp_positive, 'hsp_gaps': hsp_gaps, 'hsp_align_len': hsp_align_len, 'hsp_qseq': hsp_qseq, 'species': species, 'family': family, 'phylum': phylum, 'kingdom': kingdom, 'superkingdom': superkingdom, 'desc': desc, 'databases': databases, 'go_id': go_id, 'go_desc': go_desc, 'interpro_id': interpro_id, 'interpro_desc': interpro_desc, 'mapman_id': mapman_id, 'mapman_desc': mapman_desc, 'ec_id': ec_id, 'kegg_id': kegg_id, 'metacyc_id': metacyc_id}

        # if type is REFSEQ
        elif type.upper() == 'REFSEQ':

            # extract data 
            # REFSEQ record format:  "seq_id";"iteration_iter_num";"hit_num";"hit_id";"hsp_num";"hsp_evalue";"hsp_identity";"hsp_positive";"hsp_gaps";"hsp_align_len";"hsp_qseq";"species";"family";"phylum";"kingdom";"superkingdom";"desc";"databases";"gene_id";"status";"rna_nucleotide_accession";"protein_accession";"genomic_nucleotide_accession";"gene_symbol";"go_id";"evidence";"go_term";"category";"interpro_id";"interpro_desc";"ec_id";"kegg_id";"metacyc_id"
            data_list = []
            start = 0
            for end in [i for i, chr in enumerate(record) if chr == ';']:
                data_list.append(record[start:end].strip('"'))
                start = end + 1
            data_list.append(record[start:].strip('"').strip('\n'))
            try:
                seq_id = data_list[0]
                iteration_iter_num = data_list[1]
                hit_num = data_list[2]
                hit_id = data_list[3]
                hsp_num = data_list[4]
                hsp_evalue = data_list[5]
                hsp_identity = data_list[6]
                hsp_positive = data_list[7]
                hsp_gaps = data_list[8]
                hsp_align_len = data_list[9]
                hsp_qseq = data_list[10]
                species = data_list[11]
                family = data_list[12]
                phylum = data_list[13]
                kingdom = data_list[14]
                superkingdom = data_list[15]
                desc = data_list[16]
                databases = data_list[17]
                gene_id = data_list[18]
                status = data_list[19]
                rna_nucleotide_accession = data_list[20]
                protein_accession = data_list[21]
                genomic_nucleotide_accession = data_list[22]
                gene_symbol = data_list[23]
                go_id = data_list[24]
                evidence = data_list[25]
                go_term = data_list[26]
                category = data_list[27]
                interpro_id = data_list[28]
                interpro_desc = data_list[29]
                ec_id = data_list[30]
                kegg_id = data_list[31]
                metacyc_id = data_list[32]
            except Exception as e:
                raise ProgramException('F006', os.path.basename(file_name), record_counter)

            # set the key
            key = '{0}'.format(seq_id)

            # get the record data dictionary
            data_dict = {'seq_id': seq_id, 'iteration_iter_num': iteration_iter_num, 'hit_num': hit_num, 'hit_id': hit_id, 'hsp_num': hsp_num,  'hsp_evalue': hsp_evalue,  'hsp_identity': hsp_identity, 'hsp_positive': hsp_positive, 'hsp_gaps': hsp_gaps, 'hsp_align_len': hsp_align_len, 'hsp_qseq': hsp_qseq, 'species': species, 'family': family, 'phylum': phylum, 'kingdom': kingdom, 'superkingdom': superkingdom, 'desc': desc, 'databases': databases, 'gene_id': gene_id, 'status': status, 'rna_nucleotide_accession': rna_nucleotide_accession, 'protein_accession': protein_accession, 'genomic_nucleotide_accession': genomic_nucleotide_accession, 'gene_symbol': gene_symbol, 'go_id': go_id, 'evidence': evidence, 'go_term': go_term, 'category':category, 'interpro_id': interpro_id, 'interpro_desc': interpro_desc, 'ec_id': ec_id, 'kegg_id': kegg_id, 'metacyc_id': metacyc_id}

        # if type is NT o NR
        if type.upper() in ['NT', 'NR']:

            # extract data 
            # PLAZA record format:  "seq_id";"iteration_iter_num";"hit_num";"hit_id";"hsp_num";"hsp_evalue";"hsp_identity";"hsp_positive";"hsp_gaps";"hsp_align_len";"hsp_qseq";"species";"family";"phylum";"kingdom";"superkingdom";"desc";"databases"
            data_list = []
            start = 0
            for end in [i for i, chr in enumerate(record) if chr == ';']:
                data_list.append(record[start:end].strip('"'))
                start = end + 1
            data_list.append(record[start:].strip('"'))
            try:
                seq_id = data_list[0]
                iteration_iter_num = data_list[12]
                hit_num = data_list[2]
                hit_id = data_list[3]
                hsp_num = data_list[4]
                hsp_evalue = data_list[5]
                hsp_identity = data_list[6]
                hsp_positive = data_list[7]
                hsp_gaps = data_list[8]
                hsp_align_len = data_list[9]
                hsp_qseq = data_list[10]
                species = data_list[11]
                family = data_list[12]
                phylum = data_list[13]
                kingdom = data_list[14]
                superkingdom = data_list[15]
                desc = data_list[16]
                databases = data_list[17]
            except Exception as e:
                raise ProgramException('F006', os.path.basename(file_name), record_counter)

            # set the key
            key = '{0}'.format(seq_id)

            # get the record data dictionary
            data_dict = {'seq_id': seq_id, 'iteration_iter_num': iteration_iter_num, 'hit_num': hit_num, 'hit_id': hit_id, 'hsp_num': hsp_num, 'hsp_evalue': hsp_evalue, 'hsp_identity': hsp_identity, 'hsp_positive': hsp_positive, 'hsp_gaps': hsp_gaps, 'hsp_align_len': hsp_align_len, 'hsp_qseq': hsp_qseq, 'species': species, 'family': family, 'phylum': phylum, 'kingdom': kingdom, 'superkingdom': superkingdom, 'desc': desc, 'databases': databases}

        # if type is MERGER
        # MERGER record format:  "seq_id";"hit_num";"hit_id";"hsp_num";"hsp_evalue";"hsp_identity";"hsp_positive";"hsp_gaps";"hsp_align_len";"hsp_qseq";"species";"family";"phylum";"kingdom";"superkingdom";"desc";"databases";"go_id";"go_desc";"interpro_id";"interpro_desc";"mapman_id";"mapman_desc";"refseq_gene_id";"refseq_desc";"refseq_status";"refseq_protein_accession";"refseq_genomic_nucleotide_accession";"refseq_gene_symbol"
        elif type.upper() == 'MERGER':

            # extract data 
            data_list = []
            start = 0
            for end in [i for i, chr in enumerate(record) if chr == ';']:
                data_list.append(record[start:end].strip('"'))
                start = end + 1
            data_list.append(record[start:].strip('"').strip('\n'))
            try:
                seq_id = data_list[0]
                hit_num = data_list[1]
                hit_id = data_list[2]
                hsp_num = data_list[3]
                hsp_evalue = data_list[4]
                hsp_identity = data_list[5]
                hsp_positive = data_list[6]
                hsp_gaps = data_list[7]
                hsp_align_len = data_list[8]
                hsp_qseq = data_list[9]
                species = data_list[10]
                family = data_list[11]
                phylum = data_list[12]
                kingdom = data_list[13]
                superkingdom = data_list[14]
                desc = data_list[15]
                databases = data_list[16]
                go_id = data_list[17]
                go_desc = data_list[18]
                interpro_id = data_list[19]
                interpro_desc = data_list[20]
                mapman_id = data_list[21]
                mapman_desc = data_list[22]
                ec_id = data_list[23]
                kegg_id = data_list[24]
                metacyc_id = data_list[25]
                refseq_gene_id = data_list[26]
                refseq_desc = data_list[27]
                refseq_status = data_list[28]
                refseq_rna_nucleotide_accession = data_list[29]
                refseq_protein_accession = data_list[30]
                refseq_genomic_nucleotide_accession = data_list[31]
                refseq_gene_symbol = data_list[32]
            except Exception as e:
                raise ProgramException('F006', os.path.basename(file_name), record_counter)

            # set the key
            key = '{0}'.format(seq_id)
    
            # get the record data dictionary
            data_dict = {'seq_id': seq_id, 'hit_num': hit_num, 'hsp_num': hsp_num, 'hit_id': hit_id, 'hsp_evalue': hsp_evalue,  'hsp_identity': hsp_identity, 'hsp_positive': hsp_positive, 'hsp_gaps': hsp_gaps, 'hsp_align_len': hsp_align_len, 'hsp_qseq': hsp_qseq, 'species': species, 'family': family, 'phylum': phylum, 'kingdom': kingdom, 'superkingdom': superkingdom, 'desc': desc, 'databases': databases, 'go_id': go_id, 'go_desc': go_desc, 'interpro_id': interpro_id, 'interpro_desc': interpro_desc, 'mapman_id': mapman_id, 'mapman_desc': mapman_desc, 'ec_id': ec_id, 'kegg_id': kegg_id, 'metacyc_id': metacyc_id, 'refseq_gene_id': refseq_gene_id, 'refseq_desc': refseq_desc, 'refseq_status': refseq_status, 'refseq_rna_nucleotide_accession': refseq_rna_nucleotide_accession, 'refseq_protein_accession': refseq_protein_accession, 'refseq_genomic_nucleotide_accession': refseq_genomic_nucleotide_accession, 'refseq_gene_symbol': refseq_gene_symbol}

    # if there is not record 
    else:

        # set the key
        key = bytes.fromhex('7E').decode('utf-8')

    # return the record, key and data dictionary
    return record, key, data_dict

#-------------------------------------------------------------------------------

def write_annotation_header(file_id, type):
    '''
    '''

    # if type is PLAZA
    if type.upper() == 'PLAZA':
        file_id.write('"seq_id";"iteration_iter_num";"hit_num";"hit_accession";"hsp_num";"hsp_evalue";"hsp_identity";"hsp_positive";"hsp_gaps";"hsp_align_len";"hsp_qseq";"species";"family";"phylum";"kingdom";"superkingdom";"desc";"databases";"go_id";"go_desc";"interpro_id";"interpro_desc";"mapman_id";"mapman_desc";"ec_id";"kegg_id";"metacyc_id"\n')

    # if type is REFSEQ
    elif type.upper() == 'REFSEQ':
        file_id.write('"seq_id";"iteration_iter_num";"hit_num";"hit_id";"hsp_num";"hsp_evalue";"hsp_identity";"hsp_positive";"hsp_gaps";"hsp_align_len";"hsp_qseq";"species";"family";"phylum";"kingdom";"superkingdom";"desc";"databases";"gene_id";"status";"rna_nucleotide_accession";"protein_accession";"genomic_nucleotide_accession";"gene_symbol";"go_id";"evidence";"go_term";"category";"interpro_id";"interpro_desc";"ec_id";"kegg_id";"metacyc_id"\n')

    # if type is NT or NR
    elif type.upper() in ['NT', 'NR']:
        file_id.write('"seq_id";"iteration_iter_num";"hit_num";"hit_id";"hsp_num";"hsp_evalue";"hsp_identity";"hsp_positive";"hsp_gaps";"hsp_align_len";"hsp_qseq";"species";"family";"phylum";"kingdom";"superkingdom";"desc";"databases"\n')

    # if type is MERGER
    elif type.upper() == 'MERGER':
        file_id.write('"seq_id";"hit_num";"hit_id";"hsp_num";"hsp_evalue";"hsp_identity";"hsp_positive";"hsp_gaps";"hsp_align_len";"hsp_qseq";"species";"family";"phylum";"kingdom";"superkingdom";"desc";"databases";"go_id";"go_desc";"interpro_id";"interpro_desc";"mapman_id";"mapman_desc";"ec_id";"kegg_id";"metacyc_id";"refseq_gene_id";"refseq_desc";"refseq_status";"refseq_rna_nucleotide_accession";"refseq_protein_accession";"refseq_genomic_nucleotide_accession";"refseq_gene_symbol"\n')

#-------------------------------------------------------------------------------

def write_annotation_record(file_id, type, data_dict):
    '''
    '''

    # if type is PLAZA
    # format: "seq_id";"iteration_iter_num";"hit_num";"hit_accession";"hsp_num";"hsp_evalue";"hsp_identity";"hsp_positive";"hsp_gaps";"hsp_align_len";"hsp_qseq";"species";"family";"phylum";"kingdom";"superkingdom";"desc";"databases";"go_id";"go_desc";"interpro_id";"interpro_desc";"mapman_id";"mapman_desc";"ec_id";"kegg_id";"metacyc_id"
    if type.upper() == 'PLAZA':
        if data_dict['accum_go_id'] != '': data_dict['accum_go_id'] = 'GO:{0}'.format(data_dict['accum_go_id'])
        output_format= '"{0}";"{1}";"{2}";"{3}";"{4}";"{5}";"{6}";"{7}";"{8}";"{9}";"{10}";"{11}";"{12}";"{13}";"{14}";"{15}";"{16}";"{17}";"{18}";"{19}";"{20}";"{21}";"{22}";"{23}";"{24}";"{25}";"{26}"\n'
        file_id.write(output_format.format(data_dict['seq_id'], data_dict['iteration_iter_num'], data_dict['hit_num'], data_dict['hit_accession'], data_dict['hsp_num'], data_dict['hsp_evalue'], data_dict['hsp_identity'], data_dict['hsp_positive'], data_dict['hsp_gaps'], data_dict['hsp_align_len'], data_dict['hsp_qseq'], data_dict['species'], data_dict['family'], data_dict['phylum'], data_dict['kingdom'], data_dict['superkingdom'], data_dict['desc'], data_dict['accum_databases'], data_dict['accum_go_id'], data_dict['accum_go_desc'], data_dict['accum_interpro_id'], data_dict['accum_interpro_desc'], data_dict['accum_mapman_id'], data_dict['accum_mapman_desc'], data_dict['accum_ec_id'], data_dict['accum_kegg_id'], data_dict['accum_metacyc_id']))

    # if type is REFSEQ
    # format: "seq_id";"iteration_iter_num";"hit_num";"hit_id";"hsp_num";"hsp_evalue";"hsp_identity";"hsp_positive";"hsp_gaps";"hsp_align_len";"hsp_qseq";"species";"family";"phylum";"kingdom";"superkingdom";"desc";"gene_id";"status";"rna_nucleotide_accession";"protein_accession";"genomic_nucleotide_accession";"gene_symbol";"go_id";"evidence";"go_term";"category";"interpro_id";"interpro_desc";"ec_id";"kegg_id";"metacyc_id"
    elif type.upper() == 'REFSEQ':
        if data_dict['accum_go_id'] != '': data_dict['accum_go_id'] = 'GO:{0}'.format(data_dict['accum_go_id'])
        output_format= '"{0}";"{1}";"{2}";"{3}";"{4}";"{5}";"{6}";"{7}";"{8}";"{9}";"{10}";"{11}";"{12}";"{13}";"{14}";"{15}";"{16}";"{17}";"{18}";"{19}";"{20}";"{21}";"{22}";"{23}";"{24}";"{25}";"{26}";"{27}";"{28}";"{29}";"{30}";"{31}";"{32}"\n'
        file_id.write(output_format.format(data_dict['seq_id'], data_dict['iteration_iter_num'], data_dict['hit_num'], data_dict['hit_id'], data_dict['hsp_num'], data_dict['hsp_evalue'], data_dict['hsp_identity'], data_dict['hsp_positive'], data_dict['hsp_gaps'], data_dict['hsp_align_len'], data_dict['hsp_qseq'], data_dict['species'], data_dict['family'], data_dict['phylum'], data_dict['kingdom'], data_dict['superkingdom'], data_dict['desc'], data_dict['accum_databases'], data_dict['gene_id'], data_dict['status'], data_dict['rna_nucleotide_accession'], data_dict['protein_accession'], data_dict['genomic_nucleotide_accession'], data_dict['gene_symbol'], data_dict['accum_go_id'], data_dict['accum_evidence'], data_dict['accum_go_term'], data_dict['accum_category'], data_dict['accum_interpro_id'], data_dict['accum_interpro_desc'], data_dict['accum_ec_id'], data_dict['accum_kegg_id'], data_dict['accum_metacyc_id']))

    # if type is NT or NR
    # format: "seq_id";"iteration_iter_num";"hit_num";"hit_id";"hsp_num";"hsp_evalue";"hsp_identity";"hsp_positive";"hsp_gaps";"hsp_align_len";"hsp_qseq";"species";"family";"phylum";"kingdom";"superkingdom";"desc";"databases"
    elif type.upper() in ['NT', 'NR']:
        output_format= '"{0}";"{1}";"{2}";"{3}";"{4}";"{5}";"{6}";"{7}";"{8}";"{9}";"{10}";"{11}";"{12}";"{13}";"{14}";"{15}";"{16}";"{17}"\n'
        file_id.write(output_format.format(data_dict['seq_id'], data_dict['iteration_iter_num'], data_dict['hit_num'], data_dict['hit_id'], data_dict['hsp_num'], data_dict['hsp_evalue'], data_dict['hsp_identity'], data_dict['hsp_positive'], data_dict['hsp_gaps'], data_dict['hsp_align_len'], data_dict['hsp_qseq'], data_dict['species'], data_dict['family'], data_dict['phylum'], data_dict['kingdom'], data_dict['superkingdom'], data_dict['desc'], data_dict['accum_databases']))

    # if type is MERGER
    # format:  "seq_id";"hit_num";"hit_id";"hsp_num";"hsp_evalue";"hsp_identity";"hsp_positive";"hsp_gaps";"hsp_align_len";"hsp_qseq";"species";"family";"phylum";"kingdom";"superkingdom";"desc";"databases";"go_id";"go_desc";"interpro_id";"interpro_desc";"mapman_id";"mapman_desc";"ec_id";"kegg_id";"metacyc_id";"refseq_gene_id";"refseq_desc";"refseq_status";"refseq_rna_nucleotide_accession";"refseq_protein_accession";"refseq_genomic_nucleotide_accession";"refseq_gene_symbol"
    elif type.upper() == 'MERGER':
        output_format= '"{0}";"{1}";"{2}";"{3}";"{4}";"{5}";"{6}";"{7}";"{8}";"{9}";"{10}";"{11}";"{12}";"{13}";"{14}";"{15}";"{16}";"{17}";"{18}";"{19}";"{20}";"{21}";"{22}";"{23}";"{24}";"{25}";"{26}";"{26}";"{27}";"{28}";"{29}";"{30}";"{31}";"{32}"\n'
        file_id.write(output_format.format(data_dict['seq_id'], data_dict['hit_num'], data_dict['hit_id'], data_dict['hsp_num'], data_dict['hsp_evalue'], data_dict['hsp_identity'], data_dict['hsp_positive'], data_dict['hsp_gaps'], data_dict['hsp_align_len'], data_dict['hsp_qseq'], data_dict['species'], data_dict['family'], data_dict['phylum'], data_dict['kingdom'], data_dict['superkingdom'], data_dict['desc'], data_dict['databases'], data_dict['go_id'], data_dict['go_desc'], data_dict['interpro_id'], data_dict['interpro_desc'], data_dict['mapman_id'], data_dict['mapman_desc'], data_dict['ec_id'], data_dict['kegg_id'], data_dict['metacyc_id'], data_dict['refseq_gene_id'], data_dict['refseq_desc'], data_dict['refseq_status'], data_dict['refseq_rna_nucleotide_accession'], data_dict['refseq_protein_accession'], data_dict['refseq_genomic_nucleotide_accession'], data_dict['refseq_gene_symbol']))

#-------------------------------------------------------------------------------

def write_merged_annotation_record(file_id, type, data_dict):
    '''
    '''

    # merged record format:  "seq_id";"hit_num";"hit_id";"hsp_num";"hsp_evalue";"hsp_identity";"hsp_positive";"hsp_gaps";"hsp_align_len";"hsp_qseq";"species";"family";"phylum";"kingdom";"superkingdom";"desc";"databases";"go_id";"go_desc";"interpro_id";"interpro_desc";"mapman_id";"mapman_desc";"ec_id";"kegg_id";"metacyc_id";"refseq_gene_id";"refseq_desc";"refseq_status";"refseq_rna_nucleotide_accession";"refseq_protein_accession";"refseq_genomic_nucleotide_accession";"refseq_gene_symbol"
    output_format= '"{0}";"{1}";"{2}";"{3}";"{4}";"{5}";"{6}";"{7}";"{8}";"{9}";"{10}";"{11}";"{12}";"{13}";"{14}";"{15}";"{16}";"{17}";"{18}";"{19}";"{20}";"{21}";"{22}";"{23}";"{24}";"{25}";"{26}";"{27}";"{28}";"{29}";"{30}";"{31}";"{32}"\n'

    # if type is PLAZA
    if type.upper() == 'PLAZA':
        file_id.write(output_format.format(data_dict['seq_id'], data_dict['hit_num'], data_dict['hit_accession'], data_dict['hsp_num'], data_dict['hsp_evalue'], data_dict['hsp_identity'], data_dict['hsp_positive'], data_dict['hsp_gaps'], data_dict['hsp_align_len'], data_dict['hsp_qseq'], data_dict['species'], data_dict['family'], data_dict['phylum'], data_dict['kingdom'], data_dict['superkingdom'], data_dict['desc'], data_dict['databases'], data_dict['go_id'], data_dict['go_desc'], data_dict['interpro_id'], data_dict['interpro_desc'], data_dict['mapman_id'], data_dict['mapman_desc'], data_dict['ec_id'], data_dict['kegg_id'], data_dict['metacyc_id'], '', '', '', '', '', '', '', ''))

    # if type is REFSEQ
    elif type.upper() == 'REFSEQ':
        file_id.write(output_format.format(data_dict['seq_id'], data_dict['hit_num'], data_dict['hit_id'], data_dict['hsp_num'], data_dict['hsp_evalue'], data_dict['hsp_identity'], data_dict['hsp_positive'], data_dict['hsp_gaps'], data_dict['hsp_align_len'], data_dict['hsp_qseq'], data_dict['species'], data_dict['family'], data_dict['phylum'], data_dict['kingdom'], data_dict['superkingdom'], data_dict['desc'], data_dict['databases'], data_dict['go_id'], data_dict['go_term'], data_dict['interpro_id'], data_dict['interpro_desc'], '', '', data_dict['ec_id'], data_dict['kegg_id'], data_dict['metacyc_id'], data_dict['gene_id'], data_dict['desc'], data_dict['status'], data_dict['rna_nucleotide_accession'], data_dict['protein_accession'], data_dict['genomic_nucleotide_accession'], data_dict['gene_symbol']))

    # if type is NT or NR
    elif type.upper() in ['NT', 'NR']:
        file_id.write(output_format.format(data_dict['seq_id'], data_dict['hit_num'], data_dict['hit_id'], data_dict['hsp_num'], data_dict['hsp_evalue'], data_dict['hsp_identity'], data_dict['hsp_positive'], data_dict['hsp_gaps'], data_dict['hsp_align_len'], data_dict['hsp_qseq'], data_dict['species'], data_dict['family'], data_dict['phylum'], data_dict['kingdom'], data_dict['superkingdom'], data_dict['desc'], data_dict['databases'], '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''))

    # if type is MERGER
    elif type.upper() == 'MERGER':
        file_id.write(output_format.format(data_dict['seq_id'], data_dict['hit_num'], data_dict['hit_id'], data_dict['hsp_num'], data_dict['hsp_evalue'], data_dict['hsp_identity'], data_dict['hsp_positive'], data_dict['hsp_gaps'], data_dict['hsp_align_len'], data_dict['hsp_qseq'], data_dict['species'], data_dict['family'], data_dict['phylum'], data_dict['kingdom'], data_dict['superkingdom'], data_dict['desc'], data_dict['databases'], data_dict['go_id'], data_dict['go_desc'], data_dict['interpro_id'], data_dict['interpro_desc'], data_dict['mapman_id'], data_dict['mapman_desc'], data_dict['ec_id'], data_dict['kegg_id'], data_dict['metacyc_id'], data_dict['refseq_gene_id'], data_dict['refseq_desc'], data_dict['refseq_status'], data_dict['refseq_rna_nucleotide_accession'], data_dict['refseq_protein_accession'], data_dict['refseq_genomic_nucleotide_accession'], data_dict['refseq_gene_symbol']))

#-------------------------------------------------------------------------------

def get_id_relationship_dict(relationship_file):
    '''
    Get the new-old identification relationship dictionary.
    '''

    # initialize the new-old identification relationship dictionary
    id_relationship_dict = {}

    # when the relationship file is not NONE
    if relationship_file != 'NONE':

        # open the relationship file
        if relationship_file.endswith('.gz'):
            try:
                relationship_file_id = gzip.open(relationship_file, mode='rt', encoding='iso-8859-1')
            except Exception as e:
                raise ProgramException('F002', relationship_file)
        else:
            try:
                relationship_file_id = open(relationship_file, mode='r', encoding='iso-8859-1')
            except Exception as e:
                raise ProgramException('F001', relationship_file)

        # set the pattern of the data records
        # format: "new_seq_id";"old_seq_id"
        record_pattern = re.compile(r'^"(.*)";"(.*)"$')

        # initialize the record counter
        record_counter = 0

        # read the first record
        record = relationship_file_id.readline()

        # while there are records
        while record != '':

            # add 1 to record counter
            record_counter += 1

            # process data records
            if not record.startswith('#'):

                # extract data 
                try:
                    mo = record_pattern.match(record)
                    new_seq_id = mo.group(1).strip()
                    old_seq_id = mo.group(2).strip()
                except Exception as e:
                    raise ProgramException('F006', os.path.basename(relationship_file), record_counter)

                # add the new-old identification relationship to the dictionary
                id_relationship_dict[new_seq_id] = old_seq_id

            # print record counter
            Message.print('verbose', '\rRelationship file: {0} processed records.'.format(record_counter))

            # read the next record
            record = relationship_file_id.readline()

        # close relationship file
        relationship_file_id.close()

    # return the new-old identification relationship dictionary
    return id_relationship_dict

#-------------------------------------------------------------------------------
    
def get_blast_file_format_code_list():
    '''
    Get the code list of "blast_file_format".
    '''

    return ['5']

#-------------------------------------------------------------------------------
    
def get_blast_file_format_code_list_text():
    '''
    Get the code list of "blast_file_format" as text.
    '''

    return '5 (BLAST XML)'

#-------------------------------------------------------------------------------
    
def get_table_group_code_list():
    '''
    Get the code list of "table_group".
    '''

    return ['basic', 'dicots_04', 'gene', 'go', 'gymno_01', 'interpro', 'monocots_04']

#-------------------------------------------------------------------------------
    
def get_table_group_code_list_text():
    '''
    Get the code list of "table_group" as text.
    '''

    return str(get_table_group_code_list()).strip('[]').replace('\'', '').replace(',', ' or')

#-------------------------------------------------------------------------------
    
def get_type_code_list():
    '''
    Get the code list of "type".
    '''

    return ['PLAZA', 'REFSEQ', 'NT', 'NR', 'MERGER']

#-------------------------------------------------------------------------------
    
def get_type_code_list_text():
    '''
    Get the code list of "type" as text.
    '''

    return str(get_type_code_list()).strip('[]').replace('\'', '').replace(',', ' or')

#-------------------------------------------------------------------------------
    
def get_type2_code_list():
    '''
    Get the code list of "type2" ("type" of database with GO terms).
    '''

    return ['PLAZA', 'REFSEQ', 'MERGER']

#-------------------------------------------------------------------------------
    
def get_type2_code_list_text():
    '''
    Get the code list of "type2" as text.
    '''

    return str(get_type2_code_list()).strip('[]').replace('\'', '').replace(',', ' or')

#-------------------------------------------------------------------------------
    
def get_genomic_feature_format_code_list():
    '''
    Get the code list of "genomic_feature_format".
    '''

    return ['GFF', 'GFF3', 'GTF']

#-------------------------------------------------------------------------------
    
def get_genomic_feature_format_code_list_text():
    '''
    Get the code list of "genomic_feature_format" as text.
    '''

    return str(get_genomic_feature_format_code_list()).strip('[]').replace('\'', '').replace(',', ' or')

#-------------------------------------------------------------------------------
    
def get_merger_operation_code_list():
    '''
    Get the code list of "merger_operation".
    '''

    return ['1AND2', '1LESS2']

#-------------------------------------------------------------------------------
    
def get_merger_operation_code_list_text():
    '''
    Get the code list of "merger_operation" as text.
    '''

    return '1AND2 (sequences included in both files) or 1LESS2 (sequences in 1 and not in 2)'

#-------------------------------------------------------------------------------
    
def get_header_code_list():
    '''
    Get the code list of "header".
    '''

    return ['Y', 'N']

#-------------------------------------------------------------------------------
    
def get_header_code_list_text():
    '''
    Get the code list of "header" as text.
    '''

    return 'Y (yes) or N (no)'

#-------------------------------------------------------------------------------
    
def get_restored_file_format_code_list():
    '''
    Get the code list of "restored_file_format".
    '''

    return ['FASTA', 'XML', 'CSV']

#-------------------------------------------------------------------------------
    
def get_restored_file_format_code_list_text():
    '''
    Get the code list of "restored_file_format" as text.
    '''

    return str(get_restored_file_format_code_list()).strip('[]').replace('\'', '').replace(',', ' or')

#-------------------------------------------------------------------------------
    
def get_verbose_code_list():
    '''
    Get the code list of "verbose".
    '''

    return ['Y', 'N']

#-------------------------------------------------------------------------------
    
def get_verbose_code_list_text():
    '''
    Get the code list of "verbose" as text.
    '''

    return 'Y (yes) or N (no)'

#-------------------------------------------------------------------------------
    
def get_trace_code_list():
    '''
    Get the code list of "trace".
    '''

    return ['Y', 'N']

#-------------------------------------------------------------------------------
    
def get_trace_code_list_text():
    '''
    Get the code list of "trace" as text.
    '''

    return 'Y (yes) or N (no)'

#-------------------------------------------------------------------------------

class DevStdOut(object):
    '''
    This class is used when it is necessary write in sys.stdout and in a log file
    '''

    #---------------

    def __init__(self, calling_function=None, print_stdout=True):
        '''
        Execute actions correspending to the creation of a "DevStdOut" instance.
        '''

        # save initial parameters in instance variables
        self.calling_function = calling_function
        self.print_stdout = print_stdout

        # get the local log file
        self.log_file = get_submission_log_file(self.calling_function)

        # open the local log file
        try:
            if not os.path.exists(os.path.dirname(self.log_file)):
                os.makedirs(os.path.dirname(self.log_file))
            self.log_file_id = open(self.log_file, mode='w', encoding='iso-8859-1', newline='\n')
        except Exception as e:
            print('*** ERROR: The file {0} can not be created'.format(self.log_file))

    #---------------

    def write(self, message):
        '''
        Write the message in sys.stadout and in the log file
        '''

        # write in sys.stdout
        if self.print_stdout:
            sys.stdout.write(message)

        # write in the log file
        self.log_file_id.write(message)
        self.log_file_id.flush()
        os.fsync(self.log_file_id.fileno())

    #---------------

    def get_log_file(self):
        '''
        Get the current log file name
        '''

        return self.log_file

    #---------------

    def __del__(self):
        '''
        Execute actions correspending to the object removal.
        '''

        # close the local log file
        self.log_file_id.close()

    #---------------

#-------------------------------------------------------------------------------

class DevNull(object):
    '''
    This class is used when it is necessary do not write a output
    '''

    #---------------

    def write(self, *_):
        '''
        Do not write anything.
        '''

        pass

    #---------------

#-------------------------------------------------------------------------------
 
class Const():
    '''
    This class has attributes with values will be used as constants.
    '''

    #---------------

    DEFAULT_HEADER = 'N'
    DEFAULT_RNUM = 1000000
    DEFAULT_TRACE = 'N'
    DEFAULT_VERBOSE = 'N'

   #---------------

    MAX_QUERY_NUMBER_PER_FILE = 10000000

   #---------------

#-------------------------------------------------------------------------------
 
class Message():
    '''
    This class controls the informative messages printed on the console.
    '''

    #---------------

    verbose_status = False
    trace_status = False

    #---------------

    def set_verbose_status(status):

        Message.verbose_status = status

    #---------------

    def set_trace_status(status):

        Message.trace_status = status

    #---------------

    def print(message_type, message_text):

        if message_type == 'info':
            print(message_text, file=sys.stdout)
            sys.stdout.flush()
        elif message_type == 'verbose' and Message.verbose_status:
            sys.stdout.write(message_text)
            sys.stdout.flush()
        elif message_type == 'trace' and Message.trace_status:
            print(message_text, file=sys.stdout)
            sys.stdout.flush()
        elif message_type == 'error':
            print(message_text, file=sys.stderr)
            sys.stderr.flush()

    #---------------

#-------------------------------------------------------------------------------

class ProgramException(Exception):
    '''
    This class controls various exceptions that can occur in the execution of the application.
    '''

   #---------------

    def __init__(self, code_exception, param1='', param2='', param3='', conn=None):
        '''Initialize the object to manage a passed exception.''' 

        # manage the code of exception
        if code_exception == 'B001':
            Message.print('error', '*** ERROR {0}: The database {1} can not be connected.'.format(code_exception, param1))
        elif code_exception == 'B002':
            Message.print('error', '*** ERROR {0}: {1}'.format(code_exception, param1))
            Message.print('error', '{0}'.format(param2))
        elif code_exception == 'D001':
            Message.print('error', '*** ERROR {0}: The record {3} of file {2} has a {1} value not integer.'.format(code_exception, param1, param2, param3))
        elif code_exception == 'D002':
            Message.print('error', '*** ERROR {0}: The record {3} of file {2} has a {1} value not float.'.format(code_exception, param1, param2, param3))
        elif code_exception == 'F001':
            Message.print('error', '*** ERROR {0}: The file {1} can not be opened.'.format(code_exception, param1))
        elif code_exception == 'F002':
            Message.print('error', '*** ERROR {0}: The GZ compressed file {1} can not be opened.'.format(code_exception, param1))
        elif code_exception == 'F003':
            Message.print('error', '*** ERROR {0}: The file {1} can not be written.'.format(code_exception, param1))
        elif code_exception == 'F004':
            Message.print('error', '*** ERROR {0}: The GZ compressed file {1} can not be written.'.format(code_exception, param1))
        elif code_exception == 'F005':
            Message.print('error', '*** ERROR {0}: The format file {1} is not {2}.'.format(code_exception, param1, param2))
        elif code_exception == 'F006':
            Message.print('error', '*** ERROR {0}: The record format in record {2} of the file {1} is wrong.'.format(code_exception, param1, param2))
        elif code_exception == 'L001':
            Message.print('error', '*** ERROR {0}: {1} is not a valid dataset identification.'.format(code_exception, param1))
        elif code_exception == 'L002':
            Message.print('error', '*** ERROR {0}: The record {3} of file {2} has a wrong {1} identification.'.format(code_exception, param1, param2, param3))
        elif code_exception == 'L003':
            Message.print('error', '*** ERROR {0}: {1} is not a valid species identification.'.format(code_exception, param1))
        elif code_exception == 'L004':
            Message.print('error', '*** ERROR {0}: {1} in the file name {2} is not a valid species identification.'.format(code_exception, param1, param2))
        elif code_exception == 'L005':
            Message.print('error', '*** ERROR {0}: The name of the file {1} is not a valid name (gene_description.species_id.csv.gz with a valid species_id).'.format(code_exception, param1))
        elif code_exception == 'L006':
            Message.print('error', '*** ERROR {0}: {1} is not a valid scientific name of a species.'.format(code_exception, param1))
        elif code_exception == 'L007':
            Message.print('error', '*** ERROR {0}: There are not data loaded into TOA database to the species {1}.'.format(code_exception, param1))
        elif code_exception == 'L008':
            Message.print('error', '*** ERROR {0}: The sequence identification {1} is not found in the relation file.'.format(code_exception, param1))
        elif code_exception == 'P001':
            Message.print('error', '*** ERROR {0}: The program has parameters with invalid values.'.format(code_exception))
        elif code_exception == 'S001':
            Message.print('error', '*** ERROR {0}: The {1} OS is not supported.'.format(code_exception, param1))
        elif code_exception == 'W001':
            Message.print('error', '*** ERROR {0}: The server {1} is not reachable.'.format(code_exception, param1))
        elif code_exception == 'W002':
            Message.print('error', '*** ERROR {0}: Connection to the server {1} is timed out.'.format(code_exception, param1))
        elif code_exception == 'W003':
            Message.print('error', '*** ERROR {0}: The server {1} returned the code {2}.'.format(code_exception, param1, param2))
        else:
            Message.print('error', '*** ERROR {0}: The exception is not managed.'.format(code_exception))
            sys.exit(1)

        # roll back changes into TOA database since the last call to commit()
        if conn is not None:
            conn.rollback()

        # close connection to TOA database
        if conn is not None:
            conn.close()

        # exit with RC 1
        sys.exit(1)

   #---------------

#-------------------------------------------------------------------------------

class BreakAllLoops(Exception):
    '''
    This class is used to break out of nested loops.
    '''

    pass

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print('This source contains general functions and classes used in {0} software package used in both console mode and gui mode.'.format(get_long_project_name()))
    sys.exit(0)

#-------------------------------------------------------------------------------
