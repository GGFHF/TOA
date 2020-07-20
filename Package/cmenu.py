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
This file contains the functions related to menus in console mode.
'''
#-------------------------------------------------------------------------------

import sys

import cbioinfoapp
import clib
import clog
import ctoa
import xlib
import xtoa

#-------------------------------------------------------------------------------

def build_menu_main():
    '''
    Build the menu Main.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment('Main')

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Configuration')
        print()
        print( '    2. Genomic databases')
        print()
        print( '    3. Annotation pipelines')
        print()
        print( '    4. Statistics')
        print()
        print( '    5. Logs')
        print()
        print(f'    X. Exit {xlib.get_short_project_name()}')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            build_menu_toa_configuration()
        elif option == '2':
            build_menu_toa_databases()
        elif option == '3':
            build_menu_toa_pipelines()
        elif option == '4':
            build_menu_toa_stats()
        elif option == '5':
            build_menu_logs()
        elif option == 'X':
            sure = ''
            print( '')
            while sure not in ['Y', 'N']:
                sure = input(f'Are you sure to exit {xlib.get_short_project_name()}? (y or n): ').upper()
            if sure == 'Y':
                break

#-------------------------------------------------------------------------------

def build_menu_toa_configuration():
    '''
    Build the menu Configuration.
    '''


    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment('Configuration')

        # print the menu options
        print( 'Options:')
        print()
        print(f'    1. Recreate {xlib.get_toa_name()} config file')
        print(f'    2. View {xlib.get_toa_name()} config file')
        print()
        print(f'    3. Recreate {xlib.get_toa_name()} database')
        print(f'    4. Rebuild {xlib.get_toa_name()} database')
        print()
        print( '    5. Bioinfo software installation')
        print()
        print( '    X. Return to menu Main')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_create_toa_config_file()
        elif option == '2':
            ctoa.form_view_toa_config_file()
        elif option == '3':
            ctoa.form_manage_toa_database(xlib.get_toa_type_recreate())
        elif option == '4':
            ctoa.form_manage_toa_database(xlib.get_toa_type_rebuild())
        elif option == '5':
            build_menu_bioinfo_software_installation()
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_bioinfo_software_installation():
    '''
    Build the menu Bioinfo software installation.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment('Bioinfo software installation')

        # print the menu options
        print( 'Options:')
        print()
        print(f'    1. {xlib.get_miniconda3_name()} (Conda infrastructure)')
        print()
        print(f'    2. {xlib.get_blastplus_name()}'.format())
        print(f'    3. {xlib.get_diamond_name()}')
        print(f'    4. {xlib.get_entrez_direct_name()}')
        print(f'    5. {xlib.get_transdecoder_name()}')
        # -- print()
        # -- print(f'    X. {xlib.get_r_name()} & analysis packages')
        print()
        print( '    X. Return to menu Main')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            cbioinfoapp.form_install_bioinfo_app(xlib.get_miniconda3_code())
        elif option == '2':
            cbioinfoapp.form_install_bioinfo_app(xlib.get_blastplus_code())
        elif option == '3':
            cbioinfoapp.form_install_bioinfo_app(xlib.get_diamond_code())
        elif option == '4':
            cbioinfoapp.form_install_bioinfo_app(xlib.get_entrez_direct_code())
        elif option == '5':
            cbioinfoapp.form_install_bioinfo_app(xlib.get_transdecoder_code())
        # -- elif option == 'X':
        # --     cbioinfoapp.form_install_bioinfo_app(xlib.get_r_code())
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_toa_databases():
    '''
    Build the menu Genomic databases.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment('Genomic databases')

        # print the menu options
        print( 'Options:')
        print()
        print(f'    1. {xlib.get_toa_data_basic_data_name()}')
        print()
        print(f'    2. {xlib.get_toa_data_gymno_01_name()}')
        print(f'    3. {xlib.get_toa_data_dicots_04_name()}')
        print(f'    4. {xlib.get_toa_data_monocots_04_name()}')
        print()
        print(f'    5. {xlib.get_toa_data_refseq_plant_name()}')
        # -- print(f'    x. {xlib.get_toa_data_taxonomy_name()}')
        print(f'    6. {xlib.get_toa_data_nt_name()}')
        # -- print(f'    x. {xlib.get_toa_data_viridiplantae_nucleotide_gi_name()}')
        print(f'    7. {xlib.get_toa_data_nr_name()}')
        # -- print(f'    x. {xlib.get_toa_data_viridiplantae_protein_gi_name()}')
        print(f'    8. {xlib.get_toa_data_gene_name()}')
        print()
        print(f'    9. {xlib.get_toa_data_interpro_name()}')
        print()
        print(f'    A. {xlib.get_toa_data_go_name()}')
        print()
        print( '    X. Return to menu Main')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            build_menu_toa_basic_data()
        elif option == '2':
            build_menu_toa_gymno_01()
        elif option == '3':
            build_menu_toa_dicots_04()
        elif option == '4':
            build_menu_toa_monocots_04()
        elif option == '5':
            build_menu_toa_refseq_plant()
        # -- elif option == 'X':
        # --     build_menu_toa_taxonomy()
        elif option == '6':
            build_menu_toa_nt()
        # -- elif option == 'X':
        # --     build_menu_toa_nucleotide_gi()
        elif option == '7':
            build_menu_toa_nr()
        # -- elif option == 'X':
        # --     build_menu_toa_protein_gi()
        elif option == '8':
            build_menu_toa_gene()
        elif option == '9':
            build_menu_toa_interpro()
        elif option == 'A':
            build_menu_toa_go()
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_toa_basic_data():
    '''
    Build the menu Basic data.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment(xlib.get_toa_data_basic_data_name())

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Recreate genomic dataset file')
        print( '    2. Edit genomic file')
        print()
        print( '    3. Recreate species file')
        print( '    4. Edit species file')
        print()
        print( '    5. Download other basic data')
        print()
        print(f'    6. Load data into {xlib.get_toa_name()} database')
        print()
        print( '    X. Return to menu Genomic databases')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            cbioinfoapp.form_recreate_data_file(xtoa.get_dataset_file())
        elif option == '2':
            cbioinfoapp.form_edit_data_file(xtoa.get_dataset_file())
        elif option == '3':
            cbioinfoapp.form_recreate_data_file(xtoa.get_species_file())
        elif option == '4':
            cbioinfoapp.form_edit_data_file(xtoa.get_species_file())
        elif option == '5':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_download_data(), xlib.get_toa_data_basic_data_code())
        elif option == '6':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_load_data(), xlib.get_toa_data_basic_data_code())
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_toa_gymno_01():
    '''
    Build the menu Gymno PLAZA 1.0.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment(xlib.get_toa_data_gymno_01_name())

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Build proteome')
        print()
        print( '    2. Download functional annotations from PLAZA server')
        print(f'    3. Load data into {xlib.get_toa_name()} database')
        print()
        print( '    X. Return to menu Genomic databases')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_build_proteome(), xlib.get_toa_data_gymno_01_code())
        elif option == '2':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_download_data(), xlib.get_toa_data_gymno_01_code())
        elif option == '3':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_load_data(), xlib.get_toa_data_gymno_01_code())
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_toa_dicots_04():
    '''
    Build the menu Dicots PLAZA 4.0.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment(xlib.get_toa_data_dicots_04_name())

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Build proteome')
        print()
        print( '    2. Download functional annotations from PLAZA server')
        print(f'    3. Load data into {xlib.get_toa_name()} database')
        print()
        print( '    X. Return to menu Genomic databases')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_build_proteome(), xlib.get_toa_data_dicots_04_code())
        elif option == '2':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_download_data(), xlib.get_toa_data_dicots_04_code())
        elif option == '3':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_load_data(), xlib.get_toa_data_dicots_04_code())
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_toa_monocots_04():
    '''
    Build the menu Monocots PLAZA 4.0.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment(xlib.get_toa_data_monocots_04_name())

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Build proteome')
        print()
        print( '    2. Download functional annotations from PLAZA server')
        print(f'    3. Load data into {xlib.get_toa_name()} database')
        print()
        print( '    X. Return to menu Genomic databases')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_build_proteome(), xlib.get_toa_data_monocots_04_code())
        elif option == '2':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_download_data(), xlib.get_toa_data_monocots_04_code())
        elif option == '3':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_load_data(), xlib.get_toa_data_monocots_04_code())
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_toa_refseq_plant():
    '''
    Build the menu NCBI RefSeq Plant.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment(xlib.get_toa_data_refseq_plant_name())

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Build proteome')
        print()
        print( '    X. Return to menu Genomic databases')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_build_proteome(), xlib.get_toa_data_refseq_plant_code())
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_toa_taxonomy():
    '''
    Build the menu NCBI Taxonomy.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment(xlib.get_toa_data_taxonomy_name())

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Download taxonomy data from NCBI server')
        print()
        print( '    X. Return to menu Genomic databases')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_download_data(), xlib.get_toa_data_taxonomy_code())
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_toa_nt():
    '''
    Build the menu NCBI BLAST database NT.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment(xlib.get_toa_data_nt_name())

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Build database for BLAST+')
        print()
        print( '    X. Return to menu Genomic databases')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_build_blastplus_db(), xlib.get_toa_data_nt_code())
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_toa_nucleotide_gi():
    '''
    Build the menu NCBI Nucleotide GenInfo identifier list.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment(xlib.get_toa_data_viridiplantae_nucleotide_gi_name())

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Build identifier list using NCBI server')
        print()
        print( '    X. Return to menu Genomic databases')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_build_gilist(), xlib.get_toa_data_viridiplantae_nucleotide_gi_code())
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_toa_nr():
    '''
    Build the menu NCBI BLAST database NR.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment(xlib.get_toa_data_nr_name())

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Build database for BLAST+')
        print( '    2. Build database for DIAMOND')
        print()
        print( '    X. Return to menu Genomic databases')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_build_blastplus_db(), xlib.get_toa_data_nr_code())
        elif option == '2':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_build_diamond_db(), xlib.get_toa_data_nr_code())
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_toa_protein_gi():
    '''
    Build the menu NCBI Protein GenInfo identifier lists.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment(xlib.get_toa_data_viridiplantae_protein_gi_name())

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Build identifier list using NCBI server')
        print()
        print( '    X. Return to menu Genomic databases')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_build_gilist(), xlib.get_toa_data_viridiplantae_protein_gi_code())
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_toa_gene():
    '''
    Build the menu NCBI Gene.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment(xlib.get_toa_data_gene_name())

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Download functional annotations from NCBI server')
        print(f'    2. Load data into {xlib.get_toa_name()} database')
        print()
        print( '    X. Return to menu Genomic databases')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_download_data(), xlib.get_toa_data_gene_code())
        elif option == '2':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_load_data(), xlib.get_toa_data_gene_code())
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_toa_interpro():
    '''
    Build the menu InterPro.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment(xlib.get_toa_data_interpro_name())

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Download functional annotations from InterPro server')
        print(f'    2. Load data into {xlib.get_toa_name()} database')
        print()
        print( '    X. Return to menu Genomic databases')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_download_data(), xlib.get_toa_data_interpro_code())
        elif option == '2':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_load_data(), xlib.get_toa_data_interpro_code())
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_toa_go():
    '''
    Build the menu Gene Ontology.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment(xlib.get_toa_data_go_name())

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Download functional annotations from Gene Ontology server')
        print(f'    2. Load data into {xlib.get_toa_name()} database')
        print()
        print( '    X. Return to menu Genomic databases')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_download_data(), xlib.get_toa_data_go_code())
        elif option == '2':
            ctoa.form_manage_genomic_database(xlib.get_toa_type_load_data(), xlib.get_toa_data_go_code())
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_toa_pipelines():
    '''
    Build the menu Pipelines.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment('Pipelines')

        # print the menu options
        print( 'Options:')
        print()
        print(f'    1. {xlib.get_toa_name()} {xlib.get_toa_process_pipeline_nucleotide_name()}')
        print(f'    2. {xlib.get_toa_name()} {xlib.get_toa_process_pipeline_aminoacid_name()}')
        print()
        print(f'    3. Annotation merger of {xlib.get_toa_name()} pipelines')
        print()
        print( '    X. Return to menu Main')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            build_menu_toa_nucleotide_pipeline()
        elif option == '2':
            build_menu_toa_aminoacid_pipeline()
        elif option == '3':
            build_menu_toa_annotation_merger()
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_toa_nucleotide_pipeline():
    '''
    Build the menu Nucleotide pipeline.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment(f'{xlib.get_toa_name()} {xlib.get_toa_process_pipeline_nucleotide_name()}')

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Recreate config file')
        print( '    2. Edit config file')
        print()
        print( '    3. Run pipeline')
        print( '    4. Restart pipeline')
        print()
        print( '    X. Return to menu Pipelines')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_recreate_pipeline_config_file(xlib.get_toa_process_pipeline_nucleotide_code())
        elif option == '2':
            ctoa.form_edit_pipeline_config_file(xlib.get_toa_process_pipeline_nucleotide_code())
        elif option == '3':
            ctoa.form_run_pipeline_process(xlib.get_toa_process_pipeline_nucleotide_code())
        elif option == '4':
            ctoa.form_restart_pipeline_process(xlib.get_toa_process_pipeline_nucleotide_code())
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_toa_aminoacid_pipeline():
    '''
    Build the menu amino acid pipeline.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment(f'{xlib.get_toa_name()} {xlib.get_toa_process_pipeline_aminoacid_name()}')

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Recreate config file')
        print( '    2. Edit config file')
        print()
        print( '    3. Run pipeline')
        print( '    4. Restart pipeline')
        print()
        print( '    X. Return to menu Pipelines')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_recreate_pipeline_config_file(xlib.get_toa_process_pipeline_aminoacid_code())
        elif option == '2':
            ctoa.form_edit_pipeline_config_file(xlib.get_toa_process_pipeline_aminoacid_code())
        elif option == '3':
            ctoa.form_run_pipeline_process(xlib.get_toa_process_pipeline_aminoacid_code())
        elif option == '4':
            ctoa.form_restart_pipeline_process(xlib.get_toa_process_pipeline_aminoacid_code())
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_toa_annotation_merger():
    '''
    Build the menu annotation merger of TOA pipelines.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment(f'Annotation merger of {xlib.get_toa_name()} pipelines')

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Recreate config file')
        print( '    2. Edit config file')
        print()
        print( '    3. Run process')
        print()
        print( '    X. Return to menu Pipelines')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_recreate_annotation_merger_config_file()
        elif option == '2':
            ctoa.form_edit_pipeline_config_file(xlib.get_toa_process_merge_annotations_code())
        elif option == '3':
            ctoa.form_run_pipeline_process(xlib.get_toa_process_merge_annotations_code())
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_toa_stats():
    '''
    Build the menu Statistics.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment('Statistics')

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Alignment')
        print()
        print( '    2. Annotation datasets')
        print()
        print( '    3. Species')
        print( '    4. Family')
        print( '    5. Phylum')
        print()
        print( '    6. EC')
        print( '    7. Gene Ontology')
        print( '    8. InterPro')
        print( '    9. KEGG')
        print( '    A. MapMan')
        print( '    B. MetaCyc')
        print()
        print( '    X. Return to menu Main')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            build_menu_alignment_stats()
        elif option == '2':
            build_menu_annotation_dataset_stats()
        elif option == '3':
            build_menu_species_stats()
        elif option == '4':
            build_menu_family_stats()
        elif option == '5':
            build_menu_phylum_stats()
        elif option == '6':
            build_menu_ec_stats()
        elif option == '7':
            build_menu_go_stats()
        elif option == '8':
            build_menu_interpro_stats()
        elif option == '9':
            build_menu_kegg_stats()
        elif option == 'A':
            build_menu_mapman_stats()
        elif option == 'B':
            build_menu_metacyc_stats()
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_alignment_stats():
    '''
    Build the menu Statistics - Alignment.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment('Statistics - Alignment')

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. # HITs per # HSPs data')
        print()
        print( '    X. Return to menu Statistics')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_view_x_per_y_data(stats_code='hit_per_hsp')
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_annotation_dataset_stats():
    '''
    Build the menu Statistics - Annotation datases.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment('Statistics - Annotation datases')

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Frecuency distribution data')
        print()
        print( '    X. Return to menu Statistics')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_view_dataset_data_frecuency()
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_species_stats():
    '''
    Build the menu Statistics - Species.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment('Statistics - Species')

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Frecuency distribution data')
        print()
        print( '    X. Return to menu Statistics')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_view_phylogenic_data_frecuency(stats_code='species')
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_family_stats():
    '''
    Build the menu Statistics - Family.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment('Statistics - Family')

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Frecuency distribution data')
        print()
        print( '    X. Return to menu Statistics')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_view_phylogenic_data_frecuency(stats_code='family')
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_phylum_stats():
    '''
    Build the menu Statistics - Phylum.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment('Statistics - Phylum')

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Frecuency distribution data')
        print()
        print( '    X. Return to menu Statistics')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_view_phylogenic_data_frecuency(stats_code='phylum')
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_ec_stats():
    '''
    Build the menu Statistics - EC.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment('Statistics - EC')

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Frecuency distribution data')
        print( '    2. # sequences per # ids data')
        print()
        print( '    X. Return to menu Statistics')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_view_ontologic_data_frecuency(stats_code='ec')
        elif option == '2':
            ctoa.form_view_x_per_y_data(stats_code='seq_per_ec')
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_go_stats():
    '''
    Build the menu Statistics - Gene Ontology.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment('Statistics - Gene Ontology')

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Frecuency distribution data per term')
        print( '    2. Frecuency distribution data per namespace')
        print( '    3. # sequences per # terms data')
        print()
        print( '    X. Return to menu Statistics')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_view_go_data_frecuency()
        elif option == '2':
            ctoa.form_view_phylogenic_data_frecuency(stats_code='namespace')
        elif option == '3':
            ctoa.form_view_x_per_y_data(stats_code='seq_per_go')
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_interpro_stats():
    '''
    Build the menu Statistics - InterPro.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment('Statistics - InterPro')

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Frecuency distribution data')
        print( '    2. # sequences per # ids data')
        print()
        print( '    X. Return to menu Statistics')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_view_ontologic_data_frecuency(stats_code='interpro')
        elif option == '2':
            ctoa.form_view_x_per_y_data(stats_code='seq_per_interpro')
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_kegg_stats():
    '''
    Build the menu Statistics - KEGG.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment('Statistics - KEGG')

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Frecuency distribution data')
        print( '    2. # sequences per # ids data')
        print()
        print( '    X. Return to menu Statistics')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_view_ontologic_data_frecuency(stats_code='kegg')
        elif option == '2':
            ctoa.form_view_x_per_y_data(stats_code='seq_per_kegg')
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_mapman_stats():
    '''
    Build the menu Statistics - Mapman.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment('Statistics - Mapman')

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Frecuency distribution data')
        print( '    2. # sequences per # ids data')
        print()
        print( '    X. Return to menu Statistics')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_view_ontologic_data_frecuency(stats_code='mapman')
        elif option == '2':
            ctoa.form_view_x_per_y_data(stats_code='seq_per_mapman')
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_metacyc_stats():
    '''
    Build the menu Statistics - MetaCyc.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment('Statistics - MetaCyc')

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. Frecuency distribution data')
        print( '    2. # sequences per # ids data')
        print()
        print( '    X. Return to menu Statistics')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            ctoa.form_view_ontologic_data_frecuency(stats_code='metacyc')
        elif option == '2':
            ctoa.form_view_x_per_y_data(stats_code='seq_per_metacyc')
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

def build_menu_logs():
    '''
    Build the menu Logs.
    '''

    while True:

        # print headers
        clib.clear_screen()
        clib.print_headers_with_environment('Cluster logs')

        # print the menu options
        print( 'Options:')
        print()
        print( '    1. List submission logs')
        print( '    2. View a submission log')
        print()
        print( '    3. List result logs')
        print( '    4. View a result log')
        print()
        print( '    X. Return to menu Logs')
        print()

        # get the selected option
        option = input('Input the selected option: ').upper()

        # process the selected option
        if option == '1':
            clog.form_list_submission_logs()
        elif option == '2':
            clog.form_view_submission_log()
        elif option == '3':
            clog.form_list_results_logs()
        elif option == '4':
            clog.form_view_result_log()
        elif option == 'X':
            break

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print( 'This file contains the functions related to menus in console mode.')
    sys.exit(0)

#-------------------------------------------------------------------------------
