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
This file contains functions related to BioInfo applications used in both console
mode and gui mode.
'''

#-------------------------------------------------------------------------------

import os
import sys

import xlib
import xtoa

#-------------------------------------------------------------------------------

def is_setup_miniconda3():
    '''
    Check if Miniconda3 is set up.
    '''

    # initialize the control variable and the error list
    OK = True
    error_list = []

    # get the dictionary of TOA configuration
    toa_config_dict = xtoa.get_toa_config_dict()

    # check the Miniconda3 directory is created
    if not os.path.isdir(toa_config_dict['MINICONDA3_BIN_DIR']):
        error_list.append('*** ERROR: Miniconda 3 is not set up.\n')
        OK = False

    # return the control variable and error list
    return (OK, error_list)

#-------------------------------------------------------------------------------

def setup_miniconda3(log, function=None):
    '''
    Set up the Miniconda3.
    '''

    # initialize the control variable
    OK = True

    # get the dictionary of TOA configuration
    toa_config_dict = xtoa.get_toa_config_dict()

    # warn that the log window does not have to be closed
    if not isinstance(log, xlib.DevStdOut):
        log.write('This process might take several minutes. Do not close this window, please wait!\n')

    # determine the run directory
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Determining the run directory ...\n')
        current_run_dir = xlib.get_current_run_dir(toa_config_dict['RESULT_DIR'], 'setup', xlib.get_miniconda3_code())
        # -- command = 'mkdir --parents {0}'.format(current_run_dir)
        command = 'mkdir -p {0}'.format(current_run_dir)
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The directory path is {0}.\n'.format(current_run_dir))
        else:
            log.write('*** ERROR: RC {0} in command -> {1}\n'.format(rc, command))
            OK = False

    # build the Miniconda3 setup script
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Building the setup script {0} ...\n'.format(get_miniconda3_setup_script()))
        (OK, error_list) = build_miniconda3_setup_script(current_run_dir)
        if OK:
            log.write('The file is built.\n')
        else:
            log.write('*** ERROR: The file could not be built.\n')

    # copy the Miniconda3 setup script to the current run directory
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Copying the setup script {0} in the directory {1} ...\n'.format(get_miniconda3_setup_script(), current_run_dir))
        command = 'cp {0} {1}'.format(get_miniconda3_setup_script(), current_run_dir)
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The file is copied.\n')
        else:
            log.write('*** ERROR: The file could not be copied.\n')

    # set run permision to the Miniconda3 setup script in the current run directory
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Setting on the run permision of {0}/{1} ...\n'.format(current_run_dir, os.path.basename(get_miniconda3_setup_script())))
        command = 'chmod u+x {0}/{1}'.format(current_run_dir, os.path.basename(get_miniconda3_setup_script()))
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The run permision is set.\n')
        else:
            log.write('*** ERROR: RC {0} in command -> {1}\n'.format(rc, command))
            OK = False

    # build the Miniconda3 setup starter
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Building the process starter {0} ...\n'.format(get_miniconda3_setup_starter()))
        (OK, error_list) = build_miniconda3_setup_starter(current_run_dir)
        if OK:
            log.write('The file is built.\n')
        if not OK:
            log.write('***ERROR: The file could not be built.\n')

    # copy the Miniconda3 setup starter in the current run directory
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Copying the process starter {0} in the directory {1} ...\n'.format(get_miniconda3_setup_starter(), current_run_dir))
        command = 'cp {0} {1}'.format(get_miniconda3_setup_starter(), current_run_dir)
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The file is copied.\n')
        else:
            log.write('*** ERROR: The file could not be copied.\n')

    # set run permision to the Miniconda3 setup starter the current run directory
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Setting on the run permision of {0}/{1} ...\n'.format(current_run_dir, os.path.basename(get_miniconda3_setup_starter())))
        command = 'chmod u+x {0}/{1}'.format(current_run_dir, os.path.basename(get_miniconda3_setup_starter()))
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The run permision is set.\n')
        else:
            log.write('*** ERROR: RC {0} in command -> {1}\n'.format(rc, command))
            OK = False

    # submit the Miniconda3 setup
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Submitting the process script {0}/{1} ...\n'.format(current_run_dir, os.path.basename(get_miniconda3_setup_starter())))
        command = '{0}/{1} &'.format(current_run_dir, os.path.basename(get_miniconda3_setup_starter()))
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The script is submitted.\n')
        else:
            log.write('*** ERROR: RC {0} in command -> {1}\n'.format(rc, command))
            OK = False

    # warn that the log window can be closed
    if not isinstance(log, xlib.DevStdOut):
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('You can close this window now.\n')

    # execute final function
    if function is not None:
        function()

    # return the control variable
    return OK

#-------------------------------------------------------------------------------

def build_miniconda3_setup_script(current_run_dir):
    '''
    Build the Miniconda3 setup script.
    '''

    # initialize the control variable and the error list
    OK = True
    error_list = []

    # get the dictionary of TOA configuration
    toa_config_dict = xtoa.get_toa_config_dict()

    # write the Miniconda3 setup script
    try:
        if not os.path.exists(os.path.dirname(get_miniconda3_setup_script())):
            os.makedirs(os.path.dirname(get_miniconda3_setup_script()))
        with open(get_miniconda3_setup_script(), mode='w', encoding='iso-8859-1', newline='\n') as script_file_id:
            script_file_id.write('{0}\n'.format('#!/bin/bash'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('export DEBIAN_FRONTEND=noninteractive'))
            script_file_id.write('{0}\n'.format('SEP="#########################################"'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('STATUS_DIR={0}'.format(xlib.get_status_dir(current_run_dir))))
            script_file_id.write('{0}\n'.format('SCRIPT_STATUS_OK={0}'.format(xlib.get_status_ok(current_run_dir))))
            script_file_id.write('{0}\n'.format('SCRIPT_STATUS_WRONG={0}'.format(xlib.get_status_wrong(current_run_dir))))
            # -- script_file_id.write('{0}\n'.format('mkdir --parents $STATUS_DIR'))
            script_file_id.write('{0}\n'.format('mkdir -p $STATUS_DIR'))
            script_file_id.write('{0}\n'.format('if [ -f $SCRIPT_STATUS_OK ]; then rm $SCRIPT_STATUS_OK; fi'))
            script_file_id.write('{0}\n'.format('if [ -f $SCRIPT_STATUS_WRONG ]; then rm $SCRIPT_STATUS_WRONG; fi'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function init'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    INIT_DATETIME=`date +%s`'))
            # -- script_file_id.write('{0}\n'.format('    FORMATTED_INIT_DATETIME=`date --date="@$INIT_DATETIME" "+%Y-%m-%d %H:%M:%S"`'))
            script_file_id.write('{0}\n'.format('    FORMATTED_INIT_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Script started at $FORMATTED_INIT_DATETIME."'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function remove_miniconda3_directory'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Removing {0} directory ..."'.format(xlib.get_miniconda3_name())))
            script_file_id.write('{0}\n'.format('    if [ -d {0} ]; then'.format(toa_config_dict['MINICONDA3_DIR'])))
            script_file_id.write('{0}\n'.format('        rm -rf {0}'.format(toa_config_dict['MINICONDA3_DIR'])))
            script_file_id.write('{0}\n'.format('        echo "The directory is removed."'))
            script_file_id.write('{0}\n'.format('    else'))
            script_file_id.write('{0}\n'.format('        echo "The directory is not found."'))
            script_file_id.write('{0}\n'.format('    fi'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function download_miniconda3_package'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Downloading the {0} installation package ..."'.format(xlib.get_miniconda3_name())))
            script_file_id.write('{0}\n'.format('    cd ~'))
            script_file_id.write('{0}\n'.format('    wget --quiet --output-document {0}.sh {1}'.format(xlib.get_miniconda3_name(), xlib.get_miniconda3_url())))
            script_file_id.write('{0}\n'.format('    RC=$?'))
            script_file_id.write('{0}\n'.format('    if [ $RC -ne 0 ]; then manage_error wget $RC; fi'))
            script_file_id.write('{0}\n'.format('    echo'))
            script_file_id.write('{0}\n'.format('    echo "The package is downloaded."'))
            script_file_id.write('{0}\n'.format('    chmod u+x {0}.sh'.format(xlib.get_miniconda3_name())))
            script_file_id.write('{0}\n'.format('    echo "The run permision is set on."'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function install_miniconda3'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Installing {0} to create Python 3 environment ..."'.format(xlib.get_miniconda3_name())))
            script_file_id.write('{0}\n'.format('    cd ~'))
            script_file_id.write('{0}\n'.format('    ./{0}.sh -b -p {1}'.format(xlib.get_miniconda3_name(), toa_config_dict['MINICONDA3_DIR'])))
            script_file_id.write('{0}\n'.format('    RC=$?'))
            script_file_id.write('{0}\n'.format('    if [ $RC -ne 0 ]; then manage_error {0} $RC; fi'.format(xlib.get_miniconda3_name())))
            script_file_id.write('{0}\n'.format('    echo "Python 3 environment is created."'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function remove_miniconda3_package'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Removing the {0} installation package ..."'.format(xlib.get_miniconda3_name())))
            script_file_id.write('{0}\n'.format('    cd ~'))
            script_file_id.write('{0}\n'.format('    rm -f {0}.sh'.format(xlib.get_miniconda3_name())))
            script_file_id.write('{0}\n'.format('    echo "The software is removed."'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function install_gffutils_python3'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Installing package gffutils in Python 3 environment ..."'))
            script_file_id.write('{0}\n'.format('    cd {0}'.format(toa_config_dict['MINICONDA3_BIN_DIR'])))
            script_file_id.write('{0}\n'.format('    ./pip install --quiet gffutils'))
            script_file_id.write('{0}\n'.format('    RC=$?'))
            script_file_id.write('{0}\n'.format('    if [ $RC -ne 0 ]; then manage_error pip $RC; fi'))
            script_file_id.write('{0}\n'.format('    echo "The package is installed."'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function install_joblib_python3'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Installing package joblib in Python 3 environment ..."'))
            script_file_id.write('{0}\n'.format('    cd {0}'.format(toa_config_dict['MINICONDA3_BIN_DIR'])))
            script_file_id.write('{0}\n'.format('    ./conda install --quiet --yes joblib'))
            script_file_id.write('{0}\n'.format('    RC=$?'))
            script_file_id.write('{0}\n'.format('    if [ $RC -ne 0 ]; then manage_error pip $RC; fi'))
            script_file_id.write('{0}\n'.format('    echo "The package is installed."'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function install_matplotlib_python3'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Installing package matplotlib in Python 3 environment ..."'))
            script_file_id.write('{0}\n'.format('    cd {0}'.format(toa_config_dict['MINICONDA3_BIN_DIR'])))
            script_file_id.write('{0}\n'.format('    ./conda install --quiet --yes matplotlib'))
            script_file_id.write('{0}\n'.format('    RC=$?'))
            script_file_id.write('{0}\n'.format('    if [ $RC -ne 0 ]; then manage_error pip $RC; fi'))
            script_file_id.write('{0}\n'.format('    echo "The package is installed."'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function install_biopython_python3'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Installing package biopython in Python 3 environment ..."'))
            script_file_id.write('{0}\n'.format('    cd {0}'.format(toa_config_dict['MINICONDA3_BIN_DIR'])))
            script_file_id.write('{0}\n'.format('    ./conda install --quiet --yes biopython'))
            script_file_id.write('{0}\n'.format('    RC=$?'))
            script_file_id.write('{0}\n'.format('    if [ $RC -ne 0 ]; then manage_error pip $RC; fi'))
            script_file_id.write('{0}\n'.format('    echo "The package is installed."'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function install_requests_python3'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Installing package requests in Python 3 environment ..."'))
            script_file_id.write('{0}\n'.format('    cd {0}'.format(toa_config_dict['MINICONDA3_BIN_DIR'])))
            script_file_id.write('{0}\n'.format('    ./conda install --quiet --yes requests'))
            script_file_id.write('{0}\n'.format('    RC=$?'))
            script_file_id.write('{0}\n'.format('    if [ $RC -ne 0 ]; then manage_error pip $RC; fi'))
            script_file_id.write('{0}\n'.format('    echo "The package is installed."'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function end'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    END_DATETIME=`date +%s`'))
            # -- script_file_id.write('{0}\n'.format('    FORMATTED_END_DATETIME=`date --date="@$END_DATETIME" "+%Y-%m-%d %H:%M:%S"`'))
            script_file_id.write('{0}\n'.format('    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`'))
            script_file_id.write('{0}\n'.format('    calculate_duration'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Script ended OK at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    touch $SCRIPT_STATUS_OK'))
            script_file_id.write('{0}\n'.format('    exit 0'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function manage_error'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    END_DATETIME=`date +%s`'))
            # -- script_file_id.write('{0}\n'.format('    FORMATTED_END_DATETIME=`date --date="@$END_DATETIME" "+%Y-%m-%d %H:%M:%S"`'))
            script_file_id.write('{0}\n'.format('    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`'))
            script_file_id.write('{0}\n'.format('    calculate_duration'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "ERROR: $1 returned error $2"'))
            script_file_id.write('{0}\n'.format('    echo "Script ended WRONG at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    touch $SCRIPT_STATUS_WRONG'))
            script_file_id.write('{0}\n'.format('    exit 3'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function calculate_duration'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    DURATION=`expr $END_DATETIME - $INIT_DATETIME`'))
            script_file_id.write('{0}\n'.format('    HH=`expr $DURATION / 3600`'))
            script_file_id.write('{0}\n'.format('    MM=`expr $DURATION % 3600 / 60`'))
            script_file_id.write('{0}\n'.format('    SS=`expr $DURATION % 60`'))
            script_file_id.write('{0}\n'.format('    FORMATTED_DURATION=`printf "%03d:%02d:%02d\\n" $HH $MM $SS`'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('init'))
            script_file_id.write('{0}\n'.format('remove_miniconda3_directory'))
            script_file_id.write('{0}\n'.format('download_miniconda3_package'))
            script_file_id.write('{0}\n'.format('install_miniconda3'))
            script_file_id.write('{0}\n'.format('remove_miniconda3_package'))
            script_file_id.write('{0}\n'.format('install_gffutils_python3'))
            script_file_id.write('{0}\n'.format('install_joblib_python3'))
            script_file_id.write('{0}\n'.format('install_matplotlib_python3'))
            script_file_id.write('{0}\n'.format('install_biopython_python3'))
            script_file_id.write('{0}\n'.format('install_requests_python3'))
            script_file_id.write('{0}\n'.format('end'))
    except Exception as e:
        error_list.append('*** ERROR: The file {0} can not be created'.format(get_miniconda3_setup_script()))
        OK = False

    # return the control variable and the error list
    return (OK, error_list)

#-------------------------------------------------------------------------------

def build_miniconda3_setup_starter(current_run_dir):
    '''
    Build the starter of the Miniconda3 setup.
    '''

    # initialize the control variable and the error list
    OK = True
    error_list = []

    # write the Miniconda3 setup starter
    try:
        if not os.path.exists(os.path.dirname(get_miniconda3_setup_starter())):
            os.makedirs(os.path.dirname(get_miniconda3_setup_starter()))
        with open(get_miniconda3_setup_starter(), mode='w', encoding='iso-8859-1', newline='\n') as file_id:
            file_id.write('{0}\n'.format('#!/bin/bash'))
            file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            file_id.write('{0}\n'.format('{0}/{1} &>{0}/{2} &'.format(current_run_dir, os.path.basename(get_miniconda3_setup_script()), xlib.get_run_log_file())))
    except Exception as e:
        error_list.append('*** ERROR: The file {0} can not be created'.format(get_miniconda3_setup_starter()))
        OK = False

    # return the control variable and the error list
    return (OK, error_list)

#-------------------------------------------------------------------------------

def get_miniconda3_setup_script():
    '''
    Get the Miniconda3 setup path in the local computer.
    '''

    # assign the Miniconda3 setup path
    miniconda3_setup_script = '{0}/{1}-setup.sh'.format(xlib.get_temp_dir(), xlib.get_miniconda3_name())

    # return the Miniconda3 setup path
    return miniconda3_setup_script

#-------------------------------------------------------------------------------

def get_miniconda3_setup_starter():
    '''
    Get the Miniconda3 setup starter path in the local computer.
    '''

    # assign the Miniconda3 setup starter path
    miniconda3_setup_starter = '{0}/{1}-setup-starter.sh'.format(xlib.get_temp_dir(), xlib.get_miniconda3_name())

    # return the Miniconda3 setup starter path
    return miniconda3_setup_starter

#-------------------------------------------------------------------------------

def is_setup_bioconda_package(package_code):
    '''
    Check if a Bioconda package is set up.
    '''

    # initialize the control variable and the error list
    OK = True
    error_list = []

    # get the dictionary of TOA configuration
    toa_config_dict = xtoa.get_toa_config_dict()

    # check the Bioconda package directory is created
    if not os.path.isdir('{0}/{1}'.format(toa_config_dict['MINICONDA3_ENVS_DIR'], package_code)):
        error_list.append('*** ERROR: Bioconda package {0} is not set up.\n'.format(package_code))
        OK = False

    # return the control variable and error list
    return (OK, error_list)

#-------------------------------------------------------------------------------

def setup_bioconda_package_list(app_code, app_name, package_list, log, function=None):
    '''
    Set up the Bioconda package list.
    '''

    # initialize the control variable
    OK = True

    # get the dictionary of TOA configuration
    toa_config_dict = xtoa.get_toa_config_dict()

    # warn that the log window does not have to be closed
    if not isinstance(log, xlib.DevStdOut):
        log.write('This process might take several minutes. Do not close this window, please wait!\n')

    # warn that Bioconda package setup requirements are being verified
    if OK: 
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Checking the Bioconda package list ({0}) setup requirements ...\n'.format(str(package_list).strip('[]').replace('\'','')))

    # check the Miniconda3 setup
    if OK:
        (OK, error_list) = is_setup_miniconda3()
        if not OK:
            log.write('*** ERROR: {0} is not setup. It has to be previously set up.\n'.format(xlib.get_miniconda3_name()))

    # warn that the requirements are OK 
    if OK:
        log.write('Setup requirements are OK.\n')

    # determine the run directory
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Determining the run directory ...\n')
        current_run_dir = xlib.get_current_run_dir(toa_config_dict['RESULT_DIR'], 'setup', app_code)
        # -- command = 'mkdir --parents {0}'.format(current_run_dir)
        command = 'mkdir -p {0}'.format(current_run_dir)
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The directory path is {0}.\n'.format(current_run_dir))
        else:
            log.write('*** ERROR: RC {0} in command -> {1}\n'.format(rc, command))
            OK = False

    # build the Bioconda package setup script
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Building the setup script {0} ...\n'.format(get_bioconda_package_setup_script()))
        (OK, error_list) = build_bioconda_package_setup_script(current_run_dir, app_name, package_list)
        if OK:
            log.write('The file is built.\n')
        if not OK:
            log.write('*** ERROR: The file could not be built.\n')

    # copy the Bioconda package setup script in the current run directory
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Copying the setup script {0} in the directory {1} ...\n'.format(get_bioconda_package_setup_script(), current_run_dir))
        command = 'cp {0} {1}'.format(get_bioconda_package_setup_script(), current_run_dir)
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The file is copied.\n')
        else:
            log.write('*** ERROR: The file could not be copied.\n')

    # set run permision to the Bioconda package setup script in the current run directory
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Setting on the run permision of {0}/{1} ...\n'.format(current_run_dir, os.path.basename(get_bioconda_package_setup_script())))
        command = 'chmod u+x {0}/{1}'.format(current_run_dir, os.path.basename(get_bioconda_package_setup_script()))
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The run permision is set.\n')
        else:
            log.write('*** ERROR: RC {0} in command -> {1}\n'.format(rc, command))
            OK = False

    # build the Bioconda package setup starter
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Building the process starter {0} ...\n'.format(get_bioconda_package_setup_starter()))
        (OK, error_list) = build_bioconda_package_setup_starter(current_run_dir)
        if OK:
            log.write('The file is built.\n')
        if not OK:
            log.write('***ERROR: The file could not be built.\n')

    # copy the Bioconda package setup starter in the current run directory
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Copying the process starter {0} in the directory {1} ...\n'.format(get_bioconda_package_setup_starter(), current_run_dir))
        command = 'cp {0} {1}'.format(get_bioconda_package_setup_starter(), current_run_dir)
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The file is copied.\n')
        else:
            log.write('*** ERROR: The file could not be copied.\n')

    # set run permision to the Bioconda package setup starter in the current run directory
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Setting on the run permision of {0}/{1} ...\n'.format(current_run_dir, os.path.basename(get_bioconda_package_setup_starter())))
        command = 'chmod u+x {0}/{1}'.format(current_run_dir, os.path.basename(get_bioconda_package_setup_starter()))
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The run permision is set.\n')
        else:
            log.write('*** ERROR: RC {0} in command -> {1}\n'.format(rc, command))
            OK = False

    # submit the Bioconda package setup
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Submitting the process script {0}/{1} ...\n'.format(current_run_dir, os.path.basename(get_bioconda_package_setup_starter())))
        command = '{0}/{1} &'.format(current_run_dir, os.path.basename(get_bioconda_package_setup_starter()))
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The script is submitted.\n')
        else:
            log.write('*** ERROR: RC {0} in command -> {1}\n'.format(rc, command))
            OK = False

    # warn that the log window can be closed
    if not isinstance(log, xlib.DevStdOut):
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('You can close this window now.\n')

    # execute final function
    if function is not None:
        function()

    # return the control variable
    return OK

#-------------------------------------------------------------------------------

def build_bioconda_package_setup_script(current_run_dir, app_name, package_list):
    '''
    Build the Bioconda package setup script.
    '''

    # initialize the control variable and the error list
    OK = True
    error_list = []

    # get the dictionary of TOA configuration
    toa_config_dict = xtoa.get_toa_config_dict()

    # write the Bioconda package setup script
    #try:
    if True:
        if not os.path.exists(os.path.dirname(get_bioconda_package_setup_script())):
            os.makedirs(os.path.dirname(get_bioconda_package_setup_script()))
        with open(get_bioconda_package_setup_script(), mode='w', encoding='iso-8859-1', newline='\n') as script_file_id:
            script_file_id.write('{0}\n'.format('#!/bin/bash'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('export DEBIAN_FRONTEND=noninteractive'))
            script_file_id.write('{0}\n'.format('SEP="#########################################"'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('STATUS_DIR={0}'.format(xlib.get_status_dir(current_run_dir))))
            script_file_id.write('{0}\n'.format('SCRIPT_STATUS_OK={0}'.format(xlib.get_status_ok(current_run_dir))))
            script_file_id.write('{0}\n'.format('SCRIPT_STATUS_WRONG={0}'.format(xlib.get_status_wrong(current_run_dir))))
            # -- script_file_id.write('{0}\n'.format('mkdir --parents $STATUS_DIR'))
            script_file_id.write('{0}\n'.format('mkdir -p $STATUS_DIR'))
            script_file_id.write('{0}\n'.format('if [ -f $SCRIPT_STATUS_OK ]; then rm $SCRIPT_STATUS_OK; fi'))
            script_file_id.write('{0}\n'.format('if [ -f $SCRIPT_STATUS_WRONG ]; then rm $SCRIPT_STATUS_WRONG; fi'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function init'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    INIT_DATETIME=`date +%s`'))
            # -- script_file_id.write('{0}\n'.format('    FORMATTED_INIT_DATETIME=`date --date="@$INIT_DATETIME" "+%Y-%m-%d %H:%M:%S"`'))
            script_file_id.write('{0}\n'.format('    FORMATTED_INIT_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Script started at $FORMATTED_INIT_DATETIME."'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function add_channel_defaults'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Adding channel defaults ..."'))
            script_file_id.write('{0}\n'.format('    cd {0}'.format(toa_config_dict['MINICONDA3_BIN_DIR'])))
            script_file_id.write('{0}\n'.format('    ./conda config --add channels defaults'))
            script_file_id.write('{0}\n'.format('    RC=$?'))
            script_file_id.write('{0}\n'.format('    if [ $RC -ne 0 ]; then manage_error conda $RC; fi'))
            script_file_id.write('{0}\n'.format('    echo "The channel is added."'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function add_channel_conda_forge'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Adding channel conda-forge ..."'))
            script_file_id.write('{0}\n'.format('    cd {0}'.format(toa_config_dict['MINICONDA3_BIN_DIR'])))
            script_file_id.write('{0}\n'.format('    ./conda config --add channels conda-forge'))
            script_file_id.write('{0}\n'.format('    RC=$?'))
            script_file_id.write('{0}\n'.format('    if [ $RC -ne 0 ]; then manage_error conda $RC; fi'))
            script_file_id.write('{0}\n'.format('    echo "The channel is added."'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function add_channel_r'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Adding channel r ..."'))
            script_file_id.write('{0}\n'.format('    cd {0}'.format(toa_config_dict['MINICONDA3_BIN_DIR'])))
            script_file_id.write('{0}\n'.format('    ./conda config --add channels r'))
            script_file_id.write('{0}\n'.format('    RC=$?'))
            script_file_id.write('{0}\n'.format('    if [ $RC -ne 0 ]; then manage_error conda $RC; fi'))
            script_file_id.write('{0}\n'.format('    echo "The channel is added."'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function add_channel_bioconda'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Adding channel bioconda ..."'))
            script_file_id.write('{0}\n'.format('    cd {0}'.format(toa_config_dict['MINICONDA3_BIN_DIR'])))
            script_file_id.write('{0}\n'.format('    ./conda config --add channels bioconda'))
            script_file_id.write('{0}\n'.format('    RC=$?'))
            script_file_id.write('{0}\n'.format('    if [ $RC -ne 0 ]; then manage_error conda $RC; fi'))
            script_file_id.write('{0}\n'.format('    echo "The channel is added."'))
            script_file_id.write('{0}\n'.format('}'))
            for package in package_list:
                script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
                script_file_id.write('{0}\n'.format('function remove_bioconda_package_{0}'.format(package[0])))
                script_file_id.write('{0}\n'.format('{'))
                script_file_id.write('{0}\n'.format('    echo "$SEP"'))
                script_file_id.write('{0}\n'.format('    echo "Removing {0} package {1} ..."'.format(xlib.get_bioconda_name(), package[0])))
                script_file_id.write('{0}\n'.format('    cd {0}'.format(toa_config_dict['MINICONDA3_BIN_DIR'])))
                script_file_id.write('{0}\n'.format('    ./conda env remove --yes --quiet --name {0}'.format(package[0])))
                script_file_id.write('{0}\n'.format('    RC=$?'))
                script_file_id.write('{0}\n'.format('    if [ $RC -eq 0 ]; then'))
                script_file_id.write('{0}\n'.format('      echo "The old package is removed."'))
                script_file_id.write('{0}\n'.format('    else'))
                script_file_id.write('{0}\n'.format('      echo "The old package is not found."'))
                script_file_id.write('{0}\n'.format('    fi'))
                script_file_id.write('{0}\n'.format('}'))
                script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
                script_file_id.write('{0}\n'.format('function install_bioconda_package_{0}'.format(package[0])))
                script_file_id.write('{0}\n'.format('{'))
                script_file_id.write('{0}\n'.format('    echo "$SEP"'))
                if package[1] == 'last':
                    script_file_id.write('{0}\n'.format('    echo "Installing {0} package {1} - last version ..."'.format(xlib.get_bioconda_name(), package[0])))
                    script_file_id.write('{0}\n'.format('    cd {0}'.format(toa_config_dict['MINICONDA3_BIN_DIR'])))
                    script_file_id.write('{0}\n'.format('    ./conda create --yes --quiet --name {0} {0}'.format(package[0])))
                    script_file_id.write('{0}\n'.format('    RC=$?'))
                    script_file_id.write('{0}\n'.format('    if [ $RC -ne 0 ]; then manage_error conda $RC; fi'))
                    script_file_id.write('{0}\n'.format('    echo "The package is installed."'))
                else:
                    script_file_id.write('{0}\n'.format('    echo "Installing {0} package {1} - version {2} ..."'.format(xlib.get_bioconda_name(), package[0], package[1])))
                    script_file_id.write('{0}\n'.format('    cd {0}'.format(toa_config_dict['MINICONDA3_BIN_DIR'])))
                    script_file_id.write('{0}\n'.format('    ./conda create --yes --quiet --name {0} {0}={1}'.format(package[0], package[1])))
                    script_file_id.write('{0}\n'.format('    RC=$?'))
                    script_file_id.write('{0}\n'.format('    if [ $RC -ne 0 ]; then '))
                    script_file_id.write('{0}\n'.format('        echo "Installing {0} package {1} - last version ..."'.format(xlib.get_bioconda_name(), package[0])))
                    script_file_id.write('{0}\n'.format('    cd {0}'.format(toa_config_dict['MINICONDA3_BIN_DIR'])))
                    script_file_id.write('{0}\n'.format('        ./conda create --yes --quiet --name {0} {0}'.format(package[0])))
                    script_file_id.write('{0}\n'.format('        RC=$?'))
                    script_file_id.write('{0}\n'.format('        if [ $RC -ne 0 ]; then manage_error conda $RC; fi'))
                    script_file_id.write('{0}\n'.format('    fi'))
                    script_file_id.write('{0}\n'.format('    echo "The package is installed."'))
                script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function end'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    END_DATETIME=`date +%s`'))
            # -- script_file_id.write('{0}\n'.format('    FORMATTED_END_DATETIME=`date --date="@$END_DATETIME" "+%Y-%m-%d %H:%M:%S"`'))
            script_file_id.write('{0}\n'.format('    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`'))
            script_file_id.write('{0}\n'.format('    calculate_duration'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Script ended OK at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    touch $SCRIPT_STATUS_OK'))
            script_file_id.write('{0}\n'.format('    exit 0'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function manage_error'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    END_DATETIME=`date +%s`'))
            # -- script_file_id.write('{0}\n'.format('    FORMATTED_END_DATETIME=`date --date="@$END_DATETIME" "+%Y-%m-%d %H:%M:%S"`'))
            script_file_id.write('{0}\n'.format('    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`'))
            script_file_id.write('{0}\n'.format('    calculate_duration'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "ERROR: $1 returned error $2"'))
            script_file_id.write('{0}\n'.format('    echo "Script ended WRONG at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    touch $SCRIPT_STATUS_WRONG'))
            script_file_id.write('{0}\n'.format('    exit 3'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function calculate_duration'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    DURATION=`expr $END_DATETIME - $INIT_DATETIME`'))
            script_file_id.write('{0}\n'.format('    HH=`expr $DURATION / 3600`'))
            script_file_id.write('{0}\n'.format('    MM=`expr $DURATION % 3600 / 60`'))
            script_file_id.write('{0}\n'.format('    SS=`expr $DURATION % 60`'))
            script_file_id.write('{0}\n'.format('    FORMATTED_DURATION=`printf "%03d:%02d:%02d\\n" $HH $MM $SS`'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('init'))
            script_file_id.write('{0}\n'.format('add_channel_defaults'))
            script_file_id.write('{0}\n'.format('add_channel_conda_forge'))
            script_file_id.write('{0}\n'.format('add_channel_r'))
            script_file_id.write('{0}\n'.format('add_channel_bioconda'))
            for package in package_list:
                script_file_id.write('{0}\n'.format('remove_bioconda_package_{0}'.format(package[0])))
                script_file_id.write('{0}\n'.format('install_bioconda_package_{0}'.format(package[0])))
            script_file_id.write('{0}\n'.format('end'))
    #except Exception as e:
    #    error_list.append('*** ERROR: The file {0} can not be created'.format(get_bioconda_package_setup_script()))
    #    OK = False

    # return the control variable and the error list
    return (OK, error_list)

#-------------------------------------------------------------------------------

def build_bioconda_package_setup_starter(current_run_dir):
    '''
    Build the starter of the Bioconda package setup.
    '''

    # initialize the control variable and the error list
    OK = True
    error_list = []

    # write the Bioconda package setup starter
    try:
        if not os.path.exists(os.path.dirname(get_bioconda_package_setup_starter())):
            os.makedirs(os.path.dirname(get_bioconda_package_setup_starter()))
        with open(get_bioconda_package_setup_starter(), mode='w', encoding='iso-8859-1', newline='\n') as file_id:
            file_id.write('{0}\n'.format('#!/bin/bash'))
            file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            file_id.write('{0}\n'.format('{0}/{1} &>{0}/{2} &'.format(current_run_dir, os.path.basename(get_bioconda_package_setup_script()), xlib.get_run_log_file())))
    except Exception as e:
        error_list.append('*** ERROR: The file {0} can not be created'.format(get_bioconda_package_setup_starter()))
        OK = False

    # return the control variable and the error list
    return (OK, error_list)

#-------------------------------------------------------------------------------

def get_bioconda_package_setup_script():
    '''
    Get the Bioconda package setup path in the local computer.
    '''

    # assign the Bioconda package setup path
    bioconda_package_setup_script = '{0}/{1}-setup.sh'.format(xlib.get_temp_dir(), xlib.get_bioconda_name())

    # return the Bioconda package setup path
    return bioconda_package_setup_script

#-------------------------------------------------------------------------------

def get_bioconda_package_setup_starter():
    '''
    Get the Bioconda package setup starter path in the local computer.
    '''

    # assign the Bioconda package setup starter path
    bioconda_package_setup_starter = '{0}/{1}-setup-starter.sh'.format(xlib.get_temp_dir(), xlib.get_bioconda_name())

    # return the Bioconda package setup starter path
    return bioconda_package_setup_starter

#-------------------------------------------------------------------------------

def is_setup_r():
    '''
    Check if R is set up.
    '''

    # initialize the control variable and the error list
    OK = True
    error_list = []

    # get the dictionary of TOA configuration
    toa_config_dict = xtoa.get_toa_config_dict()

    # check the Bioconda package directory is created
    if not os.path.isdir('{0}/{1}'.format(toa_config_dict['MINICONDA3_ENVS_DIR'], xlib.get_r_name())):
        error_list.append('*** ERROR: Bioconda package {0} is not set up.\n'.format(xlib.get_r_name()))
        OK = False

    # return the control variable and error list
    return (OK, error_list)

#-------------------------------------------------------------------------------

def setup_r(log, function=None):
    '''
    Set up the Bioconda package list.
    '''

    # initialize the control variable
    OK = True

    # get the dictionary of TOA configuration
    toa_config_dict = xtoa.get_toa_config_dict()

    # set the addicional R package code list
    package_code_list = []

    # warn that the log window does not have to not be closed
    if not isinstance(log, xlib.DevStdOut):
        log.write('This process might take several minutes. Do not close this window, please wait!\n')

    # warn that R setup requirements are being verified
    if OK: 
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Checking the R and analysis packages ({0}) setup requirements ...\n'.format(str(package_code_list).strip('[]').replace('\'','')))

    # check the Miniconda3 setup
    if OK:
        (OK, error_list) = is_setup_miniconda3()
        if not OK:
            log.write('*** ERROR: {0} is not setup. It has to be previously set up.\n'.format(xlib.get_miniconda3_name()))

    # warn that the requirements are OK 
    if OK:
        log.write('Setup requirements are OK.\n')

    # determine the run directory
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Determining the run directory ...\n')
        current_run_dir = xlib.get_current_run_dir(toa_config_dict['RESULT_DIR'], 'setup', xlib.get_r_code())
        # -- command = 'mkdir --parents {0}'.format(current_run_dir)
        command = 'mkdir -p {0}'.format(current_run_dir)
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The directory path is {0}.\n'.format(current_run_dir))
        else:
            log.write('*** ERROR: RC {0} in command -> {1}\n'.format(rc, command))
            OK = False

    # build the R setup script
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Building the setup script {0} ...\n'.format(get_r_setup_script()))
        (OK, error_list) = build_r_setup_script(current_run_dir, package_code_list)
        if OK:
            log.write('The file is built.\n')
        if not OK:
            log.write('*** ERROR: The file could not be built.\n')

    # copy the R setup script in the current run directory
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Copying the setup script {0} in the directory {1} ...\n'.format(get_r_setup_script(), current_run_dir))
        command = 'cp {0} {1}'.format(get_r_setup_script(), current_run_dir)
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The file is copied.\n')
        else:
            log.write('*** ERROR: The file could not be copied.\n')

    # set run permision to the R setup script in the current run directory
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Setting on the run permision of {0}/{1} ...\n'.format(current_run_dir, os.path.basename(get_r_setup_script())))
        command = 'chmod u+x {0}/{1}'.format(current_run_dir, os.path.basename(get_r_setup_script()))
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The run permision is set.\n')
        else:
            log.write('*** ERROR: RC {0} in command -> {1}\n'.format(rc, command))
            OK = False

    # build the R setup starter
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Building the process starter {0} ...\n'.format(get_r_setup_starter()))
        (OK, error_list) = build_r_setup_starter(current_run_dir)
        if OK:
            log.write('The file is built.\n')
        if not OK:
            log.write('***ERROR: The file could not be built.\n')

    # copy the R setup starter in the current run directory
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Copying the process starter {0} in the directory {1} ...\n'.format(get_r_setup_starter(), current_run_dir))
        command = 'cp {0} {1}'.format(get_r_setup_starter(), current_run_dir)
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The file is copied.\n')
        else:
            log.write('*** ERROR: The file could not be copied.\n')

    # set run permision to the R setup starter in the current run directory
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Setting on the run permision of {0}/{1} ...\n'.format(current_run_dir, os.path.basename(get_r_setup_starter())))
        command = 'chmod u+x {0}/{1}'.format(current_run_dir, os.path.basename(get_r_setup_starter()))
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The run permision is set.\n')
        else:
            log.write('*** ERROR: RC {0} in command -> {1}\n'.format(rc, command))
            OK = False

    # submit the R setup
    if OK:
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('Submitting the process script {0}/{1} ...\n'.format(current_run_dir, os.path.basename(get_r_setup_starter())))
        command = '{0}/{1} &'.format(current_run_dir, os.path.basename(get_r_setup_starter()))
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The script is submitted.\n')
        else:
            log.write('*** ERROR: RC {0} in command -> {1}\n'.format(rc, command))
            OK = False

    # warn that the log window can be closed
    if not isinstance(log, xlib.DevStdOut):
        log.write('{0}\n'.format(xlib.get_separator()))
        log.write('You can close this window now.\n')

    # execute final function
    if function is not None:
        function()

    # return the control variable
    return OK

#-------------------------------------------------------------------------------

def build_r_setup_script(current_run_dir, package_code_list):
    '''
    Build the R setup script.
    '''

    # initialize the control variable and the error list
    OK = True
    error_list = []

    # get the dictionary of TOA configuration
    toa_config_dict = xtoa.get_toa_config_dict()

    # write the R setup script
    try:
        if not os.path.exists(os.path.dirname(get_r_setup_script())):
            os.makedirs(os.path.dirname(get_r_setup_script()))
        with open(get_r_setup_script(), mode='w', encoding='iso-8859-1', newline='\n') as script_file_id:
            script_file_id.write('{0}\n'.format('#!/bin/bash'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('export DEBIAN_FRONTEND=noninteractive'))
            script_file_id.write('{0}\n'.format('SEP="#########################################"'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('STATUS_DIR={0}'.format(xlib.get_status_dir(current_run_dir))))
            script_file_id.write('{0}\n'.format('SCRIPT_STATUS_OK={0}'.format(xlib.get_status_ok(current_run_dir))))
            script_file_id.write('{0}\n'.format('SCRIPT_STATUS_WRONG={0}'.format(xlib.get_status_wrong(current_run_dir))))
            # -- script_file_id.write('{0}\n'.format('mkdir --parents $STATUS_DIR'))
            script_file_id.write('{0}\n'.format('mkdir -p $STATUS_DIR'))
            script_file_id.write('{0}\n'.format('if [ -f $SCRIPT_STATUS_OK ]; then rm $SCRIPT_STATUS_OK; fi'))
            script_file_id.write('{0}\n'.format('if [ -f $SCRIPT_STATUS_WRONG ]; then rm $SCRIPT_STATUS_WRONG; fi'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function init'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    INIT_DATETIME=`date +%s`'))
            # -- script_file_id.write('{0}\n'.format('    FORMATTED_INIT_DATETIME=`date --date="@$INIT_DATETIME" "+%Y-%m-%d %H:%M:%S"`'))
            script_file_id.write('{0}\n'.format('    FORMATTED_INIT_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Script started at $FORMATTED_INIT_DATETIME."'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function add_channel_defaults'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Adding channel defaults ..."'))
            script_file_id.write('{0}\n'.format('    cd {0}'.format(toa_config_dict['MINICONDA3_BIN_DIR'])))
            script_file_id.write('{0}\n'.format('    ./conda config --add channels defaults'))
            script_file_id.write('{0}\n'.format('    RC=$?'))
            script_file_id.write('{0}\n'.format('    if [ $RC -ne 0 ]; then manage_error conda $RC; fi'))
            script_file_id.write('{0}\n'.format('    echo "The channel is added."'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function add_channel_conda_forge'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Adding channel conda-forge ..."'))
            script_file_id.write('{0}\n'.format('    cd {0}'.format(toa_config_dict['MINICONDA3_BIN_DIR'])))
            script_file_id.write('{0}\n'.format('    ./conda config --add channels conda-forge'))
            script_file_id.write('{0}\n'.format('    RC=$?'))
            script_file_id.write('{0}\n'.format('    if [ $RC -ne 0 ]; then manage_error conda $RC; fi'))
            script_file_id.write('{0}\n'.format('    echo "The channel is added."'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function add_channel_r'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Adding channel r ..."'))
            script_file_id.write('{0}\n'.format('    cd {0}'.format(toa_config_dict['MINICONDA3_BIN_DIR'])))
            script_file_id.write('{0}\n'.format('    ./conda config --add channels r'))
            script_file_id.write('{0}\n'.format('    RC=$?'))
            script_file_id.write('{0}\n'.format('    if [ $RC -ne 0 ]; then manage_error conda $RC; fi'))
            script_file_id.write('{0}\n'.format('    echo "The channel is added."'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function remove_r'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Removing {0} ..."'.format(xlib.get_r_name())))
            script_file_id.write('{0}\n'.format('    cd {0}'.format(toa_config_dict['MINICONDA3_BIN_DIR'])))
            script_file_id.write('{0}\n'.format('    ./conda env remove --yes --quiet --name {0}'.format(xlib.get_r_name())))
            script_file_id.write('{0}\n'.format('    RC=$?'))
            script_file_id.write('{0}\n'.format('    if [ $RC -eq 0 ]; then'))
            script_file_id.write('{0}\n'.format('      echo "The old package is removed."'))
            script_file_id.write('{0}\n'.format('    else'))
            script_file_id.write('{0}\n'.format('      echo "The old package is not found."'))
            script_file_id.write('{0}\n'.format('    fi'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function install_r'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Installing {0} ..."'.format(xlib.get_r_name())))
            script_file_id.write('{0}\n'.format('    cd {0}'.format(toa_config_dict['MINICONDA3_BIN_DIR'])))
            script_file_id.write('{0}\n'.format('    ./conda create --yes --quiet --name {0} r-essentials'.format(xlib.get_r_name())))
            script_file_id.write('{0}\n'.format('    RC=$?'))
            script_file_id.write('{0}\n'.format('    if [ $RC -ne 0 ]; then manage_error conda $RC; fi'))
            script_file_id.write('{0}\n'.format('    echo "The package is installed."'))
            script_file_id.write('{0}\n'.format('}'))
            for package_code in package_code_list:
                script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
                script_file_id.write('{0}\n'.format('function install_r_package_{0}'.format(package_code)))
                script_file_id.write('{0}\n'.format('{'))
                script_file_id.write('{0}\n'.format('    echo "$SEP"'))
                script_file_id.write('{0}\n'.format('    echo "Installing {0} package {1} ..."'.format(xlib.get_conda_name(), package_code)))
                script_file_id.write('{0}\n'.format('    cd {0}'.format(toa_config_dict['MINICONDA3_BIN_DIR'])))
                script_file_id.write('{0}\n'.format('    source activate {0}'.format(xlib.get_r_name())))
                script_file_id.write('{0}\n'.format('    ./conda install --quiet --yes {0}'.format(package_code)))
                script_file_id.write('{0}\n'.format('    RC=$?'))
                script_file_id.write('{0}\n'.format('    if [ $RC -ne 0 ]; then manage_error conda $RC; fi'))
                script_file_id.write('{0}\n'.format('    conda deactivate'))
                script_file_id.write('{0}\n'.format('    echo "The package is installed."'))
                script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function end'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    END_DATETIME=`date +%s`'))
            # -- script_file_id.write('{0}\n'.format('    FORMATTED_END_DATETIME=`date --date="@$END_DATETIME" "+%Y-%m-%d %H:%M:%S"`'))
            script_file_id.write('{0}\n'.format('    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`'))
            script_file_id.write('{0}\n'.format('    calculate_duration'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "Script ended OK at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    touch $SCRIPT_STATUS_OK'))
            script_file_id.write('{0}\n'.format('    exit 0'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function manage_error'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    END_DATETIME=`date +%s`'))
            # -- script_file_id.write('{0}\n'.format('    FORMATTED_END_DATETIME=`date --date="@$END_DATETIME" "+%Y-%m-%d %H:%M:%S"`'))
            script_file_id.write('{0}\n'.format('    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`'))
            script_file_id.write('{0}\n'.format('    calculate_duration'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    echo "ERROR: $1 returned error $2"'))
            script_file_id.write('{0}\n'.format('    echo "Script ended WRONG at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."'))
            script_file_id.write('{0}\n'.format('    echo "$SEP"'))
            script_file_id.write('{0}\n'.format('    touch $SCRIPT_STATUS_WRONG'))
            script_file_id.write('{0}\n'.format('    exit 3'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('function calculate_duration'))
            script_file_id.write('{0}\n'.format('{'))
            script_file_id.write('{0}\n'.format('    DURATION=`expr $END_DATETIME - $INIT_DATETIME`'))
            script_file_id.write('{0}\n'.format('    HH=`expr $DURATION / 3600`'))
            script_file_id.write('{0}\n'.format('    MM=`expr $DURATION % 3600 / 60`'))
            script_file_id.write('{0}\n'.format('    SS=`expr $DURATION % 60`'))
            script_file_id.write('{0}\n'.format('    FORMATTED_DURATION=`printf "%03d:%02d:%02d\\n" $HH $MM $SS`'))
            script_file_id.write('{0}\n'.format('}'))
            script_file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            script_file_id.write('{0}\n'.format('init'))
            script_file_id.write('{0}\n'.format('add_channel_defaults'))
            script_file_id.write('{0}\n'.format('add_channel_conda_forge'))
            script_file_id.write('{0}\n'.format('add_channel_r'))
            script_file_id.write('{0}\n'.format('remove_r'))
            script_file_id.write('{0}\n'.format('install_r'))
            for package_code in package_code_list:
                script_file_id.write('{0}\n'.format('install_r_package_{0}'.format(package_code)))
            script_file_id.write('{0}\n'.format('end'))
    except Exception as e:
        error_list.append('*** ERROR: The file {0} can not be created'.format(get_r_setup_script()))
        OK = False

    # return the control variable and the error list
    return (OK, error_list)

#-------------------------------------------------------------------------------

def build_r_setup_starter(current_run_dir):
    '''
    Build the starter of the R setup.
    '''

    # initialize the control variable and the error list
    OK = True
    error_list = []

    # write the R setup starter
    try:
        if not os.path.exists(os.path.dirname(get_r_setup_starter())):
            os.makedirs(os.path.dirname(get_r_setup_starter()))
        with open(get_r_setup_starter(), mode='w', encoding='iso-8859-1', newline='\n') as file_id:
            file_id.write('{0}\n'.format('#!/bin/bash'))
            file_id.write('{0}\n'.format('#-------------------------------------------------------------------------------'))
            file_id.write('{0}\n'.format('{0}/{1} &>{0}/{2} &'.format(current_run_dir, os.path.basename(get_r_setup_script()), xlib.get_run_log_file())))
    except Exception as e:
        error_list.append('*** ERROR: The file {0} can not be created'.format(get_r_setup_starter()))
        OK = False

    # return the control variable and the error list
    return (OK, error_list)

#-------------------------------------------------------------------------------

def get_r_setup_script():
    '''
    Get the R setup path in the local computer.
    '''

    # assign the R setup path
    r_setup_script = '{0}/{1}-setup.sh'.format(xlib.get_temp_dir(), xlib.get_r_name())

    # return the R setup path
    return r_setup_script

#-------------------------------------------------------------------------------

def get_r_setup_starter():
    '''
    Get the R setup starter path in the local computer.
    '''

    # assign the R setup starter path
    r_setup_starter = '{0}/{1}-setup-starter.sh'.format(xlib.get_temp_dir(), xlib.get_r_name())

    # return the R setup starter path
    return r_setup_starter

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print('This file contains functions related to BioInfo applications used in both console mode and gui mode.')
    sys.exit(0)

#-------------------------------------------------------------------------------
