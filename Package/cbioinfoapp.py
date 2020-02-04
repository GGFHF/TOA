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
This file contains the functions related to forms corresponding BioInfo application
menu items in console mode.
'''

#-------------------------------------------------------------------------------

import subprocess
import sys

import clib
import xbioinfoapp
import xlib
import xtoa

#-------------------------------------------------------------------------------

def form_setup_bioinfo_app(app_code):
    '''
    Set up the bioinfo application software in the cluster.
    '''

    # initialize the control variable
    OK = True

    # set the bioinfo application name
    if app_code == xlib.get_blastplus_code():
        app_name = xlib.get_blastplus_name()
    elif app_code == xlib.get_entrez_direct_code():
        app_name = xlib.get_entrez_direct_name()
    elif app_code == xlib.get_miniconda3_code():
        app_name = xlib.get_miniconda3_name()
    elif app_code == xlib.get_r_code():
        app_name = xlib.get_r_name()
    elif app_code == xlib.get_transdecoder_code():
        app_name = xlib.get_transdecoder_name()

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment('{0} - Set up software'.format(app_name))

    # confirm the software set up
    print(xlib.get_separator())
    if app_code == xlib.get_miniconda3_code():
        OK = clib.confirm_action('{0} (Bioconda infrastructure) is going to be set up. All Bioconda packages previously set up will be lost and they have to be reinstalled.'.format(app_name))
    elif app_code == xlib.get_r_code():
        OK = clib.confirm_action('{0} and analysis packages are going to be set up. The previous version will be lost, if it exists.'.format(app_name))
    else:
        OK = clib.confirm_action('The {0} Bioconda/Conda package is going to be set up. The previous version will be lost, if it exists.'.format(app_name))

    # set up the software
    if OK:

        # set up the BLAST+ software
        if app_code == xlib.get_blastplus_code():
            package_code_list = [(xlib.get_blastplus_bioconda_code(), 'last')]
            devstdout = xlib.DevStdOut(xbioinfoapp.setup_bioconda_package_list.__name__)
            OK = xbioinfoapp.setup_bioconda_package_list(app_code, app_name, package_code_list, devstdout, function=None)

        # set up the Entrez Direct software
        elif app_code == xlib.get_entrez_direct_code():
            package_code_list = [(xlib.get_entrez_direct_bioconda_code(), 'last')]
            devstdout = xlib.DevStdOut(xbioinfoapp.setup_bioconda_package_list.__name__)
            OK = xbioinfoapp.setup_bioconda_package_list(app_code, app_name, package_code_list, devstdout, function=None)

        # set up the Miniconda3 software
        elif app_code == xlib.get_miniconda3_code():
            devstdout = xlib.DevStdOut(xbioinfoapp.setup_miniconda3.__name__)
            OK = xbioinfoapp.setup_miniconda3(devstdout, function=None)

        # set up R and analysis packages
        elif app_code == xlib.get_r_code():
            devstdout = xlib.DevStdOut(xbioinfoapp.setup_r.__name__)
            OK = xbioinfoapp.setup_r(devstdout, function=None)

        # set up the TransDecoder software
        elif app_code == xlib.get_transdecoder_code():
            package_code_list = [(xlib.get_transdecoder_bioconda_code(), 'last')]
            devstdout = xlib.DevStdOut(xbioinfoapp.setup_bioconda_package_list.__name__)
            OK = xbioinfoapp.setup_bioconda_package_list(app_code, app_name, package_code_list, devstdout, function=None)

    # show continuation message 
    print(xlib.get_separator())
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

def form_recreate_data_file(data_file):
    '''
    Recreate a data file.
    '''

    # get the head
    if data_file == xtoa.get_dataset_file():
        head = '{0} - Recreate the file of genomic dataset'.format(xlib.get_toa_name())
    elif data_file == xtoa.get_species_file():
        head = '{0} - Recreate the file of species'.format(xlib.get_toa_name())

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment(head)

    # confirm the creation of the data file
    print(xlib.get_separator())
    OK = clib.confirm_action('The file {0} is going to be recreated. The previous files will be lost.'.format(data_file))

    # recreate the config file
    if OK:
        if data_file == xtoa.get_dataset_file():
            (OK, error_list) = xtoa.create_dataset_file()
        elif data_file == xtoa.get_species_file():
            (OK, error_list) = xtoa.create_species_file()
        if OK:
            print('The file is recreated.')
        else:
            for error in error_list:
                print(error)

    # show continuation message 
    print(xlib.get_separator())
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

def form_edit_data_file(data_file):
    '''
    Edit a data file.
    '''

    # initialize the control variable
    OK = True

    # get the head
    if data_file == xtoa.get_dataset_file():
        head = '{0} - Edit the file of genomic dataset'.format(xlib.get_toa_name())
    elif data_file == xtoa.get_species_file():
        head = '{0} - Edit the file of species'.format(xlib.get_toa_name())

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment(head)

    # edit the read transfer config file
    print(xlib.get_separator())
    print('Editing the file {0} ...'.format(data_file))
    command = '{0} {1}'.format(xlib.get_editor(), data_file)
    rc = subprocess.call(command, shell=True)
    if rc != 0:
        print('*** ERROR: Return code {0} in command -> {1}'.format(rc, command))
        OK = False

    # check the data file
    if OK:
        print(xlib.get_separator())
        print('Checking the file {0} ...'.format(data_file))
        if data_file == xtoa.get_dataset_file():
            (OK, error_list) = xtoa.check_dataset_file(strict=False)
        elif data_file == xtoa.get_species_file():
            (OK, error_list) = xtoa.check_species_file(strict=False)
        if OK:
            print('The file is OK.')
        else:
            print()
            for error in error_list:
                print(error)

    # show continuation message 
    print(xlib.get_separator())
    input('Press [Intro] to continue ...')

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print('This file contains the functions related to forms corresponding BioInfo application menu items in console mode.')
    sys.exit(0)

#-------------------------------------------------------------------------------
