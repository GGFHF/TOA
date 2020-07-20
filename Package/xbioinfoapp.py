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

def is_installed_miniconda3():
    '''
    Check if Miniconda3 is installed.
    '''

    # initialize the control variable and the error list
    OK = True
    error_list = []

    # get the dictionary of TOA configuration
    toa_config_dict = xtoa.get_toa_config_dict()

    # check the Miniconda3 directory is created
    if not os.path.isdir(toa_config_dict['MINICONDA3_BIN_DIR']):
        error_list.append('*** ERROR: Miniconda 3 is not installed.\n')
        OK = False

    # return the control variable and error list
    return (OK, error_list)

#-------------------------------------------------------------------------------

def install_miniconda3(log, function=None):
    '''
    Install the Miniconda3.
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
        log.write(f'{xlib.get_separator()}\n')
        log.write('Determining the run directory ...\n')
        current_run_dir = xlib.get_current_run_dir(toa_config_dict['RESULT_DIR'], xlib.get_toa_result_installation_dir(), xlib.get_miniconda3_code())
        command = f'mkdir -p {current_run_dir}'
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write(f'The directory path is {current_run_dir}.\n')
        else:
            log.write(f'*** ERROR: RC {rc} in command -> {command}\n')
            OK = False

    # build the Miniconda3 installation script
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Building the installation script {get_miniconda3_installation_script()} ...\n')
        (OK, error_list) = build_miniconda3_installation_script(current_run_dir)
        if OK:
            log.write('The file is built.\n')
        else:
            log.write('*** ERROR: The file could not be built.\n')

    # copy the Miniconda3 installation script to the current run directory
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Copying the installation script {get_miniconda3_installation_script()} in the directory {current_run_dir} ...\n')
        command = f'cp {get_miniconda3_installation_script()} {current_run_dir}'
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The file is copied.\n')
        else:
            log.write('*** ERROR: The file could not be copied.\n')

    # set run permision to the Miniconda3 installation script in the current run directory
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Setting on the run permision of {current_run_dir}/{os.path.basename(get_miniconda3_installation_script())} ...\n')
        command = f'chmod u+x {current_run_dir}/{os.path.basename(get_miniconda3_installation_script())}'
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The run permision is set.\n')
        else:
            log.write(f'*** ERROR: RC {rc} in command -> {command}\n')
            OK = False

    # build the Miniconda3 installation starter
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Building the process starter {get_miniconda3_installation_starter()} ...\n')
        (OK, error_list) = build_miniconda3_installation_starter(current_run_dir)
        if OK:
            log.write('The file is built.\n')
        if not OK:
            log.write('***ERROR: The file could not be built.\n')

    # copy the Miniconda3 installation starter in the current run directory
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Copying the process starter {get_miniconda3_installation_starter()} in the directory {current_run_dir} ...\n')
        command = f'cp {get_miniconda3_installation_starter()} {current_run_dir}'
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The file is copied.\n')
        else:
            log.write('*** ERROR: The file could not be copied.\n')

    # set run permision to the Miniconda3 installation starter the current run directory
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Setting on the run permision of {current_run_dir}/{os.path.basename(get_miniconda3_installation_starter())} ...\n')
        command = f'chmod u+x {current_run_dir}/{os.path.basename(get_miniconda3_installation_starter())}'
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The run permision is set.\n')
        else:
            log.write(f'*** ERROR: RC {rc} in command -> {command}\n')
            OK = False

    # submit the Miniconda3 installation
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Submitting the process script {current_run_dir}/{os.path.basename(get_miniconda3_installation_starter())} ...\n')
        command = f'{current_run_dir}/{os.path.basename(get_miniconda3_installation_starter())} &'
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The script is submitted.\n')
        else:
            log.write(f'*** ERROR: RC {rc} in command -> {command}\n')
            OK = False

    # warn that the log window can be closed
    if not isinstance(log, xlib.DevStdOut):
        log.write(f'{xlib.get_separator()}\n')
        log.write('You can close this window now.\n')

    # execute final function
    if function is not None:
        function()

    # return the control variable
    return OK

#-------------------------------------------------------------------------------

def build_miniconda3_installation_script(current_run_dir):
    '''
    Build the Miniconda3 installation script.
    '''

    # initialize the control variable and the error list
    OK = True
    error_list = []

    # get the dictionary of TOA configuration
    toa_config_dict = xtoa.get_toa_config_dict()

    # write the Miniconda3 installation script
    try:
        if not os.path.exists(os.path.dirname(get_miniconda3_installation_script())):
            os.makedirs(os.path.dirname(get_miniconda3_installation_script()))
        with open(get_miniconda3_installation_script(), mode='w', encoding='iso-8859-1', newline='\n') as script_file_id:
            script_file_id.write( '#!/bin/bash\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'SEP="#########################################"\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write(f'STATUS_DIR={xlib.get_status_dir(current_run_dir)}\n')
            script_file_id.write(f'SCRIPT_STATUS_OK={xlib.get_status_ok(current_run_dir)}\n')
            script_file_id.write(f'SCRIPT_STATUS_WRONG={xlib.get_status_wrong(current_run_dir)}\n')
            script_file_id.write( 'mkdir -p $STATUS_DIR\n')
            script_file_id.write( 'if [ -f $SCRIPT_STATUS_OK ]; then rm $SCRIPT_STATUS_OK; fi\n')
            script_file_id.write( 'if [ -f $SCRIPT_STATUS_WRONG ]; then rm $SCRIPT_STATUS_WRONG; fi\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function init\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    INIT_DATETIME=`date +%s`\n')
            script_file_id.write( '    FORMATTED_INIT_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "Script started at $FORMATTED_INIT_DATETIME."\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function remove_miniconda3_directory\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write(f'    echo "Removing {xlib.get_miniconda3_name()} directory ..."\n')
            script_file_id.write(f'    if [ -d {toa_config_dict["MINICONDA3_DIR"]} ]; then\n')
            if os.getcwd() == xlib.get_docker_toa_dir():
                script_file_id.write(f'        rm -rf {toa_config_dict["MINICONDA3_DIR"]}\*\n')
            else:
                script_file_id.write(f'        rm -rf {toa_config_dict["MINICONDA3_DIR"]}\n')
            script_file_id.write( '        echo "The directory is removed."\n')
            script_file_id.write( '    else\n')
            script_file_id.write( '        echo "The directory is not found."\n')
            script_file_id.write( '    fi\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function download_miniconda3_package\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write(f'    echo "Downloading the {xlib.get_miniconda3_name()} installation package ..."\n')
            script_file_id.write( '    cd ~\n')
            script_file_id.write(f'    wget --quiet --output-document {xlib.get_miniconda3_name()}.sh {xlib.get_miniconda3_url()}\n')
            script_file_id.write( '    RC=$?\n')
            script_file_id.write( '    if [ $RC -ne 0 ]; then manage_error wget $RC; fi\n')
            script_file_id.write( '    echo\n')
            script_file_id.write( '    echo "The package is downloaded."\n')
            script_file_id.write(f'    chmod u+x {xlib.get_miniconda3_name()}.sh\n')
            script_file_id.write( '    echo "The run permision is set on."\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function install_miniconda3\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write(f'    echo "Installing {xlib.get_miniconda3_name()} to create Python 3 environment ..."\n')
            script_file_id.write( '    cd ~\n')
            script_file_id.write(f'    ./{xlib.get_miniconda3_name()}.sh -b -u -p {toa_config_dict["MINICONDA3_DIR"]}\n')
            script_file_id.write( '    RC=$?\n')
            script_file_id.write(f'    if [ $RC -ne 0 ]; then manage_error {xlib.get_miniconda3_name()} $RC; fi\n')
            script_file_id.write( '    echo "Python 3 environment is created."\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function remove_miniconda3_package\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write(f'    echo "Removing the {xlib.get_miniconda3_name()} installation package ..."\n')
            script_file_id.write( '    cd ~\n')
            script_file_id.write(f'    rm -f {xlib.get_miniconda3_name()}.sh\n')
            script_file_id.write( '    echo "The software is removed."\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function install_gffutils_python3\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "Installing package gffutils in Python 3 environment ..."\n')
            script_file_id.write(f'    cd {toa_config_dict["MINICONDA3_BIN_DIR"]}\n')
            script_file_id.write( '    ./pip install --quiet gffutils\n')
            script_file_id.write( '    RC=$?\n')
            script_file_id.write( '    if [ $RC -ne 0 ]; then manage_error pip $RC; fi\n')
            script_file_id.write( '    echo "The package is installed."\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function install_joblib_python3\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "Installing package joblib in Python 3 environment ..."\n')
            script_file_id.write(f'    cd {toa_config_dict["MINICONDA3_BIN_DIR"]}\n')
            script_file_id.write( '    ./conda install --quiet --yes joblib\n')
            script_file_id.write( '    RC=$?\n')
            script_file_id.write( '    if [ $RC -ne 0 ]; then manage_error pip $RC; fi\n')
            script_file_id.write( '    echo "The package is installed."\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function install_matplotlib_python3\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "Installing package matplotlib in Python 3 environment ..."\n')
            script_file_id.write(f'    cd {toa_config_dict["MINICONDA3_BIN_DIR"]}\n')
            script_file_id.write( '    ./conda install --quiet --yes matplotlib\n')
            script_file_id.write( '    RC=$?\n')
            script_file_id.write( '    if [ $RC -ne 0 ]; then manage_error pip $RC; fi\n')
            script_file_id.write( '    echo "The package is installed."\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function install_biopython_python3\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "Installing package biopython in Python 3 environment ..."\n')
            script_file_id.write(f'    cd {toa_config_dict["MINICONDA3_BIN_DIR"]}\n')
            script_file_id.write( '    ./conda install --quiet --yes biopython\n')
            script_file_id.write( '    RC=$?\n')
            script_file_id.write( '    if [ $RC -ne 0 ]; then manage_error pip $RC; fi\n')
            script_file_id.write( '    echo "The package is installed."\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function install_requests_python3\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "Installing package requests in Python 3 environment ..."\n')
            script_file_id.write(f'    cd {toa_config_dict["MINICONDA3_BIN_DIR"]}\n')
            script_file_id.write( '    ./conda install --quiet --yes requests\n')
            script_file_id.write( '    RC=$?\n')
            script_file_id.write( '    if [ $RC -ne 0 ]; then manage_error pip $RC; fi\n')
            script_file_id.write( '    echo "The package is installed."\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function end\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    END_DATETIME=`date --utc +%s`\n')
            script_file_id.write( '    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
            script_file_id.write( '    calculate_duration\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "Script ended OK at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    touch $SCRIPT_STATUS_OK\n')
            script_file_id.write( '    exit 0\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function manage_error\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    END_DATETIME=`date --utc +%s`\n')
            script_file_id.write( '    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
            script_file_id.write( '    calculate_duration\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "ERROR: $1 returned error $2"\n')
            script_file_id.write( '    echo "Script ended WRONG at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    touch $SCRIPT_STATUS_WRONG\n')
            script_file_id.write( '    exit 3\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function calculate_duration\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    DURATION=`expr $END_DATETIME - $INIT_DATETIME`\n')
            script_file_id.write( '    HH=`expr $DURATION / 3600`\n')
            script_file_id.write( '    MM=`expr $DURATION % 3600 / 60`\n')
            script_file_id.write( '    SS=`expr $DURATION % 60`\n')
            script_file_id.write( '    FORMATTED_DURATION=`printf "%03d:%02d:%02d\\n" $HH $MM $SS`\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'init\n')
            script_file_id.write( 'remove_miniconda3_directory\n')
            script_file_id.write( 'download_miniconda3_package\n')
            script_file_id.write( 'install_miniconda3\n')
            script_file_id.write( 'remove_miniconda3_package\n')
            script_file_id.write( 'install_gffutils_python3\n')
            script_file_id.write( 'install_joblib_python3\n')
            script_file_id.write( 'install_matplotlib_python3\n')
            script_file_id.write( 'install_biopython_python3\n')
            script_file_id.write( 'install_requests_python3\n')
            script_file_id.write( 'end\n')
    except Exception as e:
        error_list.append(f'*** EXCEPTION: "{e}".')
        error_list.append(f'*** ERROR: The file {get_miniconda3_installation_script()} can not be created.')
        OK = False

    # return the control variable and the error list
    return (OK, error_list)

#-------------------------------------------------------------------------------

def build_miniconda3_installation_starter(current_run_dir):
    '''
    Build the starter of the Miniconda3 installation.
    '''

    # initialize the control variable and the error list
    OK = True
    error_list = []

    # write the Miniconda3 installation starter
    try:
        if not os.path.exists(os.path.dirname(get_miniconda3_installation_starter())):
            os.makedirs(os.path.dirname(get_miniconda3_installation_starter()))
        with open(get_miniconda3_installation_starter(), mode='w', encoding='iso-8859-1', newline='\n') as file_id:
            file_id.write( '#!/bin/bash\n')
            file_id.write( '#-------------------------------------------------------------------------------\n')
            file_id.write(f'{current_run_dir}/{os.path.basename(get_miniconda3_installation_script())} &>{current_run_dir}/{xlib.get_run_log_file()} &\n')
    except Exception as e:
        error_list.append(f'*** EXCEPTION: "{e}".')
        error_list.append(f'*** ERROR: The file {get_miniconda3_installation_starter()} can not be created.')
        OK = False

    # return the control variable and the error list
    return (OK, error_list)

#-------------------------------------------------------------------------------

def get_miniconda3_installation_script():
    '''
    Get the Miniconda3 installation path in the local computer.
    '''

    # assign the Miniconda3 installation path
    miniconda3_installation_script = f'{xlib.get_temp_dir()}/{xlib.get_miniconda3_name()}-installation.sh'

    # return the Miniconda3 installation path
    return miniconda3_installation_script

#-------------------------------------------------------------------------------

def get_miniconda3_installation_starter():
    '''
    Get the Miniconda3 installation starter path in the local computer.
    '''

    # assign the Miniconda3 installation starter path
    miniconda3_installation_starter = f'{xlib.get_temp_dir()}/{xlib.get_miniconda3_name()}-installation-starter.sh'

    # return the Miniconda3 installation starter path
    return miniconda3_installation_starter

#-------------------------------------------------------------------------------

def is_installed_conda_package(package_code):
    '''
    Check if a Conda package is installed.
    '''

    # initialize the control variable and the error list
    OK = True
    error_list = []

    # get the dictionary of TOA configuration
    toa_config_dict = xtoa.get_toa_config_dict()

    # check the Conda package directory is created
    if not os.path.isdir(f'{toa_config_dict["MINICONDA3_ENVS_DIR"]}/{package_code}'):
        error_list.append(f'*** ERROR: Conda package {package_code} is not installed.\n')
        OK = False

    # return the control variable and error list
    return (OK, error_list)

#-------------------------------------------------------------------------------

def install_conda_package_list(app_code, app_name, package_list, log, function=None):
    '''
    Install the Conda package list.
    '''

    # initialize the control variable
    OK = True

    # get the dictionary of TOA configuration
    toa_config_dict = xtoa.get_toa_config_dict()

    # warn that the log window does not have to be closed
    if not isinstance(log, xlib.DevStdOut):
        log.write('This process might take several minutes. Do not close this window, please wait!\n')

    # warn that Conda package installation requirements are being verified
    if OK: 
        log.write(f'{xlib.get_separator()}\n')
        package_list_text = str(package_list).strip('[]').replace('\'','')
        log.write(f'Checking the Conda package list ({package_list_text}) installation requirements ...\n')

    # check the Miniconda3 installation
    if OK:
        (OK, error_list) = is_installed_miniconda3()
        if not OK:
            log.write(f'*** ERROR: {xlib.get_miniconda3_name()} is not installed.\n')

    # warn that the requirements are OK 
    if OK:
        log.write('Installation requirements are OK.\n')

    # determine the run directory
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write('Determining the run directory ...\n')
        current_run_dir = xlib.get_current_run_dir(toa_config_dict['RESULT_DIR'], xlib.get_toa_result_installation_dir(), app_code)
        command = f'mkdir -p {current_run_dir}'
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write(f'The directory path is {current_run_dir}.\n')
        else:
            log.write(f'*** ERROR: RC {rc} in command -> {command}\n')
            OK = False

    # build the Conda package installation script
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Building the installation script {get_conda_package_installation_script()} ...\n')
        (OK, error_list) = build_conda_package_installation_script(current_run_dir, app_name, package_list)
        if OK:
            log.write('The file is built.\n')
        if not OK:
            log.write('*** ERROR: The file could not be built.\n')

    # copy the Conda package installation script in the current run directory
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Copying the installation script {get_conda_package_installation_script()} in the directory {current_run_dir} ...\n')
        command = f'cp {get_conda_package_installation_script()} {current_run_dir}'
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The file is copied.\n')
        else:
            log.write('*** ERROR: The file could not be copied.\n')

    # set run permision to the Conda package installation script in the current run directory
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Setting on the run permision of {current_run_dir}/{os.path.basename(get_conda_package_installation_script())} ...\n')
        command = f'chmod u+x {current_run_dir}/{os.path.basename(get_conda_package_installation_script())}'
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The run permision is set.\n')
        else:
            log.write(f'*** ERROR: RC {rc} in command -> {command}\n')
            OK = False

    # build the Conda package installation starter
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Building the process starter {get_conda_package_installation_starter()} ...\n')
        (OK, error_list) = build_conda_package_installation_starter(current_run_dir)
        if OK:
            log.write('The file is built.\n')
        if not OK:
            log.write('***ERROR: The file could not be built.\n')

    # copy the Conda package installation starter in the current run directory
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Copying the process starter {get_conda_package_installation_starter()} in the directory {current_run_dir} ...\n')
        command = f'cp {get_conda_package_installation_starter()} {current_run_dir}'
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The file is copied.\n')
        else:
            log.write('*** ERROR: The file could not be copied.\n')

    # set run permision to the Conda package installation starter in the current run directory
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Setting on the run permision of {current_run_dir}/{os.path.basename(get_conda_package_installation_starter())} ...\n')
        command = f'chmod u+x {current_run_dir}/{os.path.basename(get_conda_package_installation_starter())}'
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The run permision is set.\n')
        else:
            log.write(f'*** ERROR: RC {rc} in command -> {command}\n')
            OK = False

    # submit the Conda package installation
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Submitting the process script {current_run_dir}/{os.path.basename(get_conda_package_installation_starter())} ...\n')
        command = f'{current_run_dir}/{os.path.basename(get_conda_package_installation_starter())} &'
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The script is submitted.\n')
        else:
            log.write(f'*** ERROR: RC {rc} in command -> {command}\n')
            OK = False

    # warn that the log window can be closed
    if not isinstance(log, xlib.DevStdOut):
        log.write(f'{xlib.get_separator()}\n')
        log.write('You can close this window now.\n')

    # execute final function
    if function is not None:
        function()

    # return the control variable
    return OK

#-------------------------------------------------------------------------------

def build_conda_package_installation_script(current_run_dir, app_name, package_list):
    '''
    Build the Conda package installation script.
    '''

    # initialize the control variable and the error list
    OK = True
    error_list = []

    # get the dictionary of TOA configuration
    toa_config_dict = xtoa.get_toa_config_dict()

    # write the conda package installation script
    try:
        if not os.path.exists(os.path.dirname(get_conda_package_installation_script())):
            os.makedirs(os.path.dirname(get_conda_package_installation_script()))
        with open(get_conda_package_installation_script(), mode='w', encoding='iso-8859-1', newline='\n') as script_file_id:
            script_file_id.write( '#!/bin/bash\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'SEP="#########################################"\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write(f'STATUS_DIR={xlib.get_status_dir(current_run_dir)}\n')
            script_file_id.write(f'SCRIPT_STATUS_OK={xlib.get_status_ok(current_run_dir)}\n')
            script_file_id.write(f'SCRIPT_STATUS_WRONG={xlib.get_status_wrong(current_run_dir)}\n')
            script_file_id.write( 'mkdir -p $STATUS_DIR\n')
            script_file_id.write( 'if [ -f $SCRIPT_STATUS_OK ]; then rm $SCRIPT_STATUS_OK; fi\n')
            script_file_id.write( 'if [ -f $SCRIPT_STATUS_WRONG ]; then rm $SCRIPT_STATUS_WRONG; fi\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function init\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    INIT_DATETIME=`date +%s`\n')
            script_file_id.write( '    FORMATTED_INIT_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "Script started at $FORMATTED_INIT_DATETIME."\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function add_channel_defaults\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "Adding channel defaults ..."\n')
            script_file_id.write(f'    cd {toa_config_dict["MINICONDA3_BIN_DIR"]}\n')
            script_file_id.write( '    ./conda config --add channels defaults\n')
            script_file_id.write( '    RC=$?\n')
            script_file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
            script_file_id.write( '    echo "The channel is added."\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function add_channel_conda_forge\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "Adding channel conda-forge ..."\n')
            script_file_id.write(f'    cd {toa_config_dict["MINICONDA3_BIN_DIR"]}\n')
            script_file_id.write( '    ./conda config --add channels conda-forge\n')
            script_file_id.write( '    RC=$?\n')
            script_file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
            script_file_id.write( '    echo "The channel is added."\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function add_channel_r\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "Adding channel r ..."\n')
            script_file_id.write(f'    cd {toa_config_dict["MINICONDA3_BIN_DIR"]}\n')
            script_file_id.write( '    ./conda config --add channels r\n')
            script_file_id.write( '    RC=$?\n')
            script_file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
            script_file_id.write( '    echo "The channel is added."\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function add_channel_bioconda\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "Adding channel bioconda ..."\n')
            script_file_id.write(f'    cd {toa_config_dict["MINICONDA3_BIN_DIR"]}\n')
            script_file_id.write( '    ./conda config --add channels bioconda\n')
            script_file_id.write( '    RC=$?\n')
            script_file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
            script_file_id.write( '    echo "The channel is added."\n')
            script_file_id.write( '}\n')
            for package in package_list:
                script_file_id.write( '#-------------------------------------------------------------------------------\n')
                script_file_id.write(f'function remove_conda_package_{package[0]}\n')
                script_file_id.write( '{\n')
                script_file_id.write( '    echo "$SEP"\n')
                script_file_id.write(f'    echo "Removing {xlib.get_conda_name()} package {package[0]} ..."\n')
                script_file_id.write(f'    cd {toa_config_dict["MINICONDA3_BIN_DIR"]}\n')
                script_file_id.write(f'    ./conda env remove --yes --quiet --name {package[0]}\n')
                script_file_id.write( '    RC=$?\n')
                script_file_id.write( '    if [ $RC -eq 0 ]; then\n')
                script_file_id.write( '      echo "The old package is removed."\n')
                script_file_id.write( '    else\n')
                script_file_id.write( '      echo "The old package is not found."\n')
                script_file_id.write( '    fi\n')
                script_file_id.write( '}\n')
                script_file_id.write( '#-------------------------------------------------------------------------------\n')
                script_file_id.write(f'function install_conda_package_{package[0]}\n')
                script_file_id.write( '{\n')
                script_file_id.write( '    echo "$SEP"\n')
                if package[1] == 'last':
                    script_file_id.write(f'    echo "Installing {xlib.get_conda_name()} package {package[0]} - last version ..."\n')
                    script_file_id.write(f'    cd {toa_config_dict["MINICONDA3_BIN_DIR"]}\n')
                    script_file_id.write(f'    ./conda create --yes --quiet --name {package[0]} {package[0]}\n')
                    script_file_id.write( '    RC=$?\n')
                    script_file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                    script_file_id.write( '    echo "The package is installed."\n')
                else:
                    script_file_id.write(f'    echo "Installing {xlib.get_conda_name()} package {package[0]} - version {package[1]} ..."\n')
                    script_file_id.write(f'    cd {toa_config_dict["MINICONDA3_BIN_DIR"]}\n')
                    script_file_id.write(f'    ./conda create --yes --quiet --name {package[0]} {package[0]}={package[1]}\n')
                    script_file_id.write( '    RC=$?\n')
                    script_file_id.write( '    if [ $RC -ne 0 ]; then\n')
                    script_file_id.write(f'        echo "Installing {xlib.get_conda_name()} package {package[0]} - last version ..."\n')
                    script_file_id.write(f'    cd {toa_config_dict["MINICONDA3_BIN_DIR"]}\n')
                    script_file_id.write(f'        ./conda create --yes --quiet --name {package[0]} {package[0]}\n')
                    script_file_id.write( '        RC=$?\n')
                    script_file_id.write( '        if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                    script_file_id.write( '    fi\n')
                    script_file_id.write( '    echo "The package is installed."\n')
                script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function end\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    END_DATETIME=`date --utc +%s`\n')
            script_file_id.write( '    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
            script_file_id.write( '    calculate_duration\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "Script ended OK at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    touch $SCRIPT_STATUS_OK\n')
            script_file_id.write( '    exit 0\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function manage_error\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    END_DATETIME=`date --utc +%s`\n')
            script_file_id.write( '    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
            script_file_id.write( '    calculate_duration\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "ERROR: $1 returned error $2"\n')
            script_file_id.write( '    echo "Script ended WRONG at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    touch $SCRIPT_STATUS_WRONG\n')
            script_file_id.write( '    exit 3\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function calculate_duration\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    DURATION=`expr $END_DATETIME - $INIT_DATETIME`\n')
            script_file_id.write( '    HH=`expr $DURATION / 3600`\n')
            script_file_id.write( '    MM=`expr $DURATION % 3600 / 60`\n')
            script_file_id.write( '    SS=`expr $DURATION % 60`\n')
            script_file_id.write( '    FORMATTED_DURATION=`printf "%03d:%02d:%02d\\n" $HH $MM $SS`\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'init\n')
            script_file_id.write( 'add_channel_defaults\n')
            script_file_id.write( 'add_channel_conda_forge\n')
            script_file_id.write( 'add_channel_r\n')
            script_file_id.write( 'add_channel_bioconda\n')
            for package in package_list:
                script_file_id.write(f'remove_conda_package_{package[0]}\n')
                script_file_id.write(f'install_conda_package_{package[0]}\n')
            script_file_id.write( 'end\n')
    except Exception as e:
        error_list.append(f'*** EXCEPTION: "{e}".')
        error_list.append(f'*** ERROR: The file {get_conda_package_installation_script()} can not be created.')
        OK = False

    # return the control variable and the error list
    return (OK, error_list)

#-------------------------------------------------------------------------------

def build_conda_package_installation_starter(current_run_dir):
    '''
    Build the starter of the Conda package installation.
    '''

    # initialize the control variable and the error list
    OK = True
    error_list = []

    # write the Conda package installation starter
    try:
        if not os.path.exists(os.path.dirname(get_conda_package_installation_starter())):
            os.makedirs(os.path.dirname(get_conda_package_installation_starter()))
        with open(get_conda_package_installation_starter(), mode='w', encoding='iso-8859-1', newline='\n') as file_id:
            file_id.write( '#!/bin/bash\n')
            file_id.write( '#-------------------------------------------------------------------------------\n')
            file_id.write(f'{current_run_dir}/{os.path.basename(get_conda_package_installation_script())} &>{current_run_dir}/{xlib.get_run_log_file()} &\n')
    except Exception as e:
        error_list.append(f'*** EXCEPTION: "{e}".')
        error_list.append(f'*** ERROR: The file {get_conda_package_installation_starter()} can not be created.')
        OK = False

    # return the control variable and the error list
    return (OK, error_list)

#-------------------------------------------------------------------------------

def get_conda_package_installation_script():
    '''
    Get the Conda package installation path in the local computer.
    '''

    # assign the Conda package installation path
    conda_package_installation_script = f'{xlib.get_temp_dir()}/{xlib.get_conda_name()}-installation.sh'

    # return the Conda package installation path
    return conda_package_installation_script

#-------------------------------------------------------------------------------

def get_conda_package_installation_starter():
    '''
    Get the Conda package installation starter path in the local computer.
    '''

    # assign the Conda package installation starter path
    conda_package_installation_starter = f'{xlib.get_temp_dir()}/{xlib.get_conda_name()}-installation-starter.sh'

    # return the Conda package installation starter path
    return conda_package_installation_starter

#-------------------------------------------------------------------------------

def is_installed_r():
    '''
    Check if R is installed.
    '''

    # initialize the control variable and the error list
    OK = True
    error_list = []

    # get the dictionary of TOA configuration
    toa_config_dict = xtoa.get_toa_config_dict()

    # check the Conda package directory is created
    if not os.path.isdir(f'{toa_config_dict["MINICONDA3_ENVS_DIR"]}/{xlib.get_r_name()}'):
        error_list.append(f'*** ERROR: Conda package {xlib.get_r_name()} is not installed.\n')
        OK = False

    # return the control variable and error list
    return (OK, error_list)

#-------------------------------------------------------------------------------

def install_r(log, function=None):
    '''
    Install the R package list.
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

    # warn that R installation requirements are being verified
    if OK: 
        log.write(f'{xlib.get_separator()}\n')
        package_code_list_text = str(package_code_list).strip('[]').replace('\'','')
        log.write(f'Checking the R and analysis packages ({package_code_list_text}) installation requirements ...\n')

    # check the Miniconda3 installation
    if OK:
        (OK, error_list) = is_installed_miniconda3()
        if not OK:
            log.write(f'*** ERROR: {xlib.get_miniconda3_name()} is not installed.\n')

    # warn that the requirements are OK 
    if OK:
        log.write('Installation requirements are OK.\n')

    # determine the run directory
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write('Determining the run directory ...\n')
        current_run_dir = xlib.get_current_run_dir(toa_config_dict['RESULT_DIR'], xlib.get_toa_result_installation_dir(), xlib.get_r_code())
        command = f'mkdir -p {current_run_dir}'
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write(f'The directory path is {current_run_dir}.\n')
        else:
            log.write(f'*** ERROR: RC {rc} in command -> {command}\n')
            OK = False

    # build the R installation script
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Building the installation script {get_r_installation_script()} ...\n')
        (OK, error_list) = build_r_installation_script(current_run_dir, package_code_list)
        if OK:
            log.write('The file is built.\n')
        if not OK:
            log.write('*** ERROR: The file could not be built.\n')

    # copy the R installation script in the current run directory
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Copying the installation script {get_r_installation_script()} in the directory {current_run_dir} ...\n')
        command = f'cp {get_r_installation_script()} {current_run_dir}'
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The file is copied.\n')
        else:
            log.write('*** ERROR: The file could not be copied.\n')

    # set run permision to the R installation script in the current run directory
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Setting on the run permision of {current_run_dir}/{os.path.basename(get_r_installation_script())} ...\n')
        command = f'chmod u+x {current_run_dir}/{os.path.basename(get_r_installation_script())}'
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The run permision is set.\n')
        else:
            log.write(f'*** ERROR: RC {rc} in command -> {command}\n')
            OK = False

    # build the R installation starter
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Building the process starter {get_r_installation_starter()} ...\n')
        (OK, error_list) = build_r_installation_starter(current_run_dir)
        if OK:
            log.write('The file is built.\n')
        if not OK:
            log.write('***ERROR: The file could not be built.\n')

    # copy the R installation starter in the current run directory
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Copying the process starter {get_r_installation_starter()} in the directory {current_run_dir} ...\n')
        command = f'cp {get_r_installation_starter()} {current_run_dir}'
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The file is copied.\n')
        else:
            log.write('*** ERROR: The file could not be copied.\n')

    # set run permision to the R installation starter in the current run directory
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Setting on the run permision of {current_run_dir}/{os.path.basename(get_r_installation_starter())} ...\n')
        command = f'chmod u+x {current_run_dir}/{os.path.basename(get_r_installation_starter())}'
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The run permision is set.\n')
        else:
            log.write(f'*** ERROR: RC {rc} in command -> {command}\n')
            OK = False

    # submit the R installation
    if OK:
        log.write(f'{xlib.get_separator()}\n')
        log.write(f'Submitting the process script {current_run_dir}/{os.path.basename(get_r_installation_starter())} ...\n')
        command = f'{current_run_dir}/{os.path.basename(get_r_installation_starter())} &'
        rc = xlib.run_command(command, log)
        if rc == 0:
            log.write('The script is submitted.\n')
        else:
            log.write(f'*** ERROR: RC {rc} in command -> {command}\n')
            OK = False

    # warn that the log window can be closed
    if not isinstance(log, xlib.DevStdOut):
        log.write(f'{xlib.get_separator()}\n')
        log.write('You can close this window now.\n')

    # execute final function
    if function is not None:
        function()

    # return the control variable
    return OK

#-------------------------------------------------------------------------------

def build_r_installation_script(current_run_dir, package_code_list):
    '''
    Build the R installation script.
    '''

    # initialize the control variable and the error list
    OK = True
    error_list = []

    # get the dictionary of TOA configuration
    toa_config_dict = xtoa.get_toa_config_dict()

    # write the R installation script
    try:
        if not os.path.exists(os.path.dirname(get_r_installation_script())):
            os.makedirs(os.path.dirname(get_r_installation_script()))
        with open(get_r_installation_script(), mode='w', encoding='iso-8859-1', newline='\n') as script_file_id:
            script_file_id.write( '#!/bin/bash\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'SEP="#########################################"\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write(f'STATUS_DIR={xlib.get_status_dir(current_run_dir)}\n')
            script_file_id.write(f'SCRIPT_STATUS_OK={xlib.get_status_ok(current_run_dir)}\n')
            script_file_id.write(f'SCRIPT_STATUS_WRONG={xlib.get_status_wrong(current_run_dir)}\n')
            script_file_id.write( 'mkdir -p $STATUS_DIR\n')
            script_file_id.write( 'if [ -f $SCRIPT_STATUS_OK ]; then rm $SCRIPT_STATUS_OK; fi\n')
            script_file_id.write( 'if [ -f $SCRIPT_STATUS_WRONG ]; then rm $SCRIPT_STATUS_WRONG; fi\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function init\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    INIT_DATETIME=`date +%s`\n')
            script_file_id.write( '    FORMATTED_INIT_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "Script started at $FORMATTED_INIT_DATETIME."\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function add_channel_defaults\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "Adding channel defaults ..."\n')
            script_file_id.write(f'    cd {toa_config_dict["MINICONDA3_BIN_DIR"]}\n')
            script_file_id.write( '    ./conda config --add channels defaults\n')
            script_file_id.write( '    RC=$?\n')
            script_file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
            script_file_id.write( '    echo "The channel is added."\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function add_channel_conda_forge\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "Adding channel conda-forge ..."\n')
            script_file_id.write(f'    cd {toa_config_dict["MINICONDA3_BIN_DIR"]}\n')
            script_file_id.write( '    ./conda config --add channels conda-forge\n')
            script_file_id.write( '    RC=$?\n')
            script_file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
            script_file_id.write( '    echo "The channel is added."\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function add_channel_r\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "Adding channel r ..."\n')
            script_file_id.write(f'    cd {toa_config_dict["MINICONDA3_BIN_DIR"]}\n')
            script_file_id.write( '    ./conda config --add channels r\n')
            script_file_id.write( '    RC=$?\n')
            script_file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
            script_file_id.write( '    echo "The channel is added."\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function remove_r\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write(f'    echo "Removing {xlib.get_r_name()} ..."\n')
            script_file_id.write(f'    cd {toa_config_dict["MINICONDA3_BIN_DIR"]}\n')
            script_file_id.write(f'    ./conda env remove --yes --quiet --name {xlib.get_r_name()}\n')
            script_file_id.write( '    RC=$?\n')
            script_file_id.write( '    if [ $RC -eq 0 ]; then\n')
            script_file_id.write( '      echo "The old package is removed."\n')
            script_file_id.write( '    else\n')
            script_file_id.write( '      echo "The old package is not found."\n')
            script_file_id.write( '    fi\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function install_r\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write(f'    echo "Installing {xlib.get_r_name()} ..."\n')
            script_file_id.write(f'    cd {toa_config_dict["MINICONDA3_BIN_DIR"]}\n')
            script_file_id.write(f'    ./conda create --yes --quiet --name {xlib.get_r_name()} r-essentials\n')
            script_file_id.write( '    RC=$?\n')
            script_file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
            script_file_id.write( '    echo "The package is installed."\n')
            script_file_id.write( '}\n')
            for package_code in package_code_list:
                script_file_id.write( '#-------------------------------------------------------------------------------\n')
                script_file_id.write(f'function install_r_package_{package_code}\n')
                script_file_id.write( '{\n')
                script_file_id.write( '    echo "$SEP"\n')
                script_file_id.write(f'    echo "Installing {xlib.get_conda_name()} package {package_code} ..."\n')
                script_file_id.write(f'    cd {toa_config_dict["MINICONDA3_BIN_DIR"]}\n')
                script_file_id.write( '    source activate {xlib.get_r_name()}\n')
                script_file_id.write(f'    ./conda install --quiet --yes {package_code}\n')
                script_file_id.write( '    RC=$?\n')
                script_file_id.write( '    if [ $RC -ne 0 ]; then manage_error conda $RC; fi\n')
                script_file_id.write( '    conda deactivate\n')
                script_file_id.write( '    echo "The package is installed."\n')
                script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function end\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    END_DATETIME=`date --utc +%s`\n')
            script_file_id.write( '    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
            script_file_id.write( '    calculate_duration\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "Script ended OK at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    touch $SCRIPT_STATUS_OK\n')
            script_file_id.write( '    exit 0\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function manage_error\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    END_DATETIME=`date --utc +%s`\n')
            script_file_id.write( '    FORMATTED_END_DATETIME=`date "+%Y-%m-%d %H:%M:%S"`\n')
            script_file_id.write( '    calculate_duration\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    echo "ERROR: $1 returned error $2"\n')
            script_file_id.write( '    echo "Script ended WRONG at $FORMATTED_END_DATETIME with a run duration of $DURATION s ($FORMATTED_DURATION)."\n')
            script_file_id.write( '    echo "$SEP"\n')
            script_file_id.write( '    touch $SCRIPT_STATUS_WRONG\n')
            script_file_id.write( '    exit 3\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'function calculate_duration\n')
            script_file_id.write( '{\n')
            script_file_id.write( '    DURATION=`expr $END_DATETIME - $INIT_DATETIME`\n')
            script_file_id.write( '    HH=`expr $DURATION / 3600`\n')
            script_file_id.write( '    MM=`expr $DURATION % 3600 / 60`\n')
            script_file_id.write( '    SS=`expr $DURATION % 60`\n')
            script_file_id.write( '    FORMATTED_DURATION=`printf "%03d:%02d:%02d\\n" $HH $MM $SS`\n')
            script_file_id.write( '}\n')
            script_file_id.write( '#-------------------------------------------------------------------------------\n')
            script_file_id.write( 'init\n')
            script_file_id.write( 'add_channel_defaults\n')
            script_file_id.write( 'add_channel_conda_forge\n')
            script_file_id.write( 'add_channel_r\n')
            script_file_id.write( 'remove_r\n')
            script_file_id.write( 'install_r\n')
            for package_code in package_code_list:
                script_file_id.write(f'install_r_package_{package_code}\n')
            script_file_id.write( 'end\n')
    except Exception as e:
        error_list.append(f'*** EXCEPTION: "{e}".')
        error_list.append(f'*** ERROR: The file {get_r_installation_script()} can not be created.')
        OK = False

    # return the control variable and the error list
    return (OK, error_list)

#-------------------------------------------------------------------------------

def build_r_installation_starter(current_run_dir):
    '''
    Build the starter of the R installation.
    '''

    # initialize the control variable and the error list
    OK = True
    error_list = []

    # write the R installation starter
    try:
        if not os.path.exists(os.path.dirname(get_r_installation_starter())):
            os.makedirs(os.path.dirname(get_r_installation_starter()))
        with open(get_r_installation_starter(), mode='w', encoding='iso-8859-1', newline='\n') as file_id:
            file_id.write( '#!/bin/bash\n')
            file_id.write( '#-------------------------------------------------------------------------------\n')
            file_id.write(f'{current_run_dir}/{os.path.basename(get_r_installation_script())} &>{current_run_dir}/{xlib.get_run_log_file()} &\n')
    except Exception as e:
        error_list.append(f'*** EXCEPTION: "{e}".')
        error_list.append(f'*** ERROR: The file {get_r_installation_starter()} can not be created.')
        OK = False

    # return the control variable and the error list
    return (OK, error_list)

#-------------------------------------------------------------------------------

def get_r_installation_script():
    '''
    Get the R installation path in the local computer.
    '''

    # assign the R installation path
    r_installation_script = f'{xlib.get_temp_dir()}/{xlib.get_r_name()}-installation.sh'

    # return the R installation path
    return r_installation_script

#-------------------------------------------------------------------------------

def get_r_installation_starter():
    '''
    Get the R installation starter path in the local computer.
    '''

    # assign the R installation starter path
    r_installation_starter = f'{xlib.get_temp_dir()}/{xlib.get_r_name()}-installation-starter.sh'

    # return the R installation starter path
    return r_installation_starter

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print('This file contains functions related to BioInfo applications used in both console mode and gui mode.')
    sys.exit(0)

#-------------------------------------------------------------------------------
