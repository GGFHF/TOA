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

def form_install_bioinfo_app(app_code):
    '''
    Install the bioinfo application software in the cluster.
    '''

    # initialize the control variable
    OK = True

    # set the bioinfo application name
    if app_code == xlib.get_blastplus_code():
        app_name = xlib.get_blastplus_name()

    elif app_code == xlib.get_diamond_code():
        app_name = xlib.get_diamond_name()

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
    clib.print_headers_with_environment(f'{app_name} - Install software')

    # confirm the software installation
    print(xlib.get_separator())
    if app_code == xlib.get_miniconda3_code():
        OK = clib.confirm_action(f'{app_name} (Conda infrastructure) is going to be installed. All Conda packages previously installed will be lost and they have to be reinstalled.')
    elif app_code == xlib.get_r_code():
        OK = clib.confirm_action(f'{app_name} and analysis packages are going to be installed. The previous version will be lost, if it exists.')
    else:
        OK = clib.confirm_action(f'The {app_name} Conda package is going to be installed. The previous version will be lost, if it exists.')

    # install the software
    if OK:

        # install the BLAST+ software
        if app_code == xlib.get_blastplus_code():
            package_code_list = [(xlib.get_blastplus_conda_code(), 'last')]
            devstdout = xlib.DevStdOut(xbioinfoapp.install_conda_package_list.__name__)
            OK = xbioinfoapp.install_conda_package_list(app_code, app_name, package_code_list, devstdout, function=None)

        # install the DIAMOND software
        elif app_code == xlib.get_diamond_code():
            package_code_list = [(xlib.get_diamond_conda_code(), 'last')]
            devstdout = xlib.DevStdOut(xbioinfoapp.install_conda_package_list.__name__)
            OK = xbioinfoapp.install_conda_package_list(app_code, app_name, package_code_list, devstdout, function=None)

        # install the Entrez Direct software
        elif app_code == xlib.get_entrez_direct_code():
            package_code_list = [(xlib.get_entrez_direct_conda_code(), 'last')]
            devstdout = xlib.DevStdOut(xbioinfoapp.install_conda_package_list.__name__)
            OK = xbioinfoapp.install_conda_package_list(app_code, app_name, package_code_list, devstdout, function=None)

        # install the Miniconda3 software
        elif app_code == xlib.get_miniconda3_code():
            devstdout = xlib.DevStdOut(xbioinfoapp.install_miniconda3.__name__)
            OK = xbioinfoapp.install_miniconda3(devstdout, function=None)

        # install R and analysis packages
        elif app_code == xlib.get_r_code():
            devstdout = xlib.DevStdOut(xbioinfoapp.install_r.__name__)
            OK = xbioinfoapp.install_r(devstdout, function=None)

        # install the TransDecoder software
        elif app_code == xlib.get_transdecoder_code():
            package_code_list = [(xlib.get_transdecoder_conda_code(), 'last')]
            devstdout = xlib.DevStdOut(xbioinfoapp.install_conda_package_list.__name__)
            OK = xbioinfoapp.install_conda_package_list(app_code, app_name, package_code_list, devstdout, function=None)

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
        head = f'{xlib.get_toa_name()} - Recreate the file of genomic dataset'
    elif data_file == xtoa.get_species_file():
        head = f'{xlib.get_toa_name()} - Recreate the file of species'

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment(head)

    # confirm the creation of the data file
    print(xlib.get_separator())
    OK = clib.confirm_action(f'The file {data_file} is going to be recreated. The previous files will be lost.')

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
        head = f'{xlib.get_toa_name()} - Edit the file of genomic dataset'
    elif data_file == xtoa.get_species_file():
        head = f'{xlib.get_toa_name()} - Edit the file of species'

    # print the header
    clib.clear_screen()
    clib.print_headers_with_environment(head)

    # edit the read transfer config file
    print(xlib.get_separator())
    print(f'Editing the file {data_file} ...')
    command = f'{xlib.get_editor()} {data_file}'
    rc = subprocess.call(command, shell=True)
    if rc != 0:
        print(f'*** ERROR: Return code {rc} in command -> {command}')
        OK = False

    # check the data file
    if OK:
        print(xlib.get_separator())
        print(f'Checking the file {data_file} ...')
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
