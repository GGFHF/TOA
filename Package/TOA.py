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
This source starts Taxonomy-oriented Annotation (TOA) both console mode and gui mode.
'''

#-------------------------------------------------------------------------------

import argparse
import os
import sys

#-------------------------------------------------------------------------------

def main(argv):
    '''
    Main line of the program.
    '''

    # check the operating system
    if not sys.platform.startswith('linux') and not sys.platform.startswith('darwin'):
        print(f'*** ERROR: The {sys.platform} OS is not supported.')
        sys.exit(1)

    # check the Python version
    if sys.version_info[0] == 3 and sys.version_info[1] >= 5:
        pass
    else:
        print('*** ERROR: Python 3.5 or greater is required.')
        sys.exit(1)

    # check if the current directory is TOA home directory
    current_dir = os.getcwd()
    program_name = os.path.basename(__file__)
    if not os.path.isfile(os.path.join(current_dir, program_name)):
        print(f'*** ERROR: {program_name} has to be run in the TOA home directory.')
        sys.exit(1)

    # check if Plotnine is installed
    try:
        import plotnine
    except Exception as e:
        print('*** ERROR: The library paramiko is not installed.')
        print('Please, review how to install Paramiko in the manual.')
        sys.exit(1)

    # get and check the arguments
    parser = build_parser()
    args = parser.parse_args()
    check_args(args)

    # check if the required graphical libraries are installed
    if args.mode == 'gui' or args.mode is None:

        # check if the library PIL.Image is installed
        try:
            import tkinter
        except Exception as e:
            print('*** ERROR: The library tkinter is not installed.')
            print('Please, review how to install Tkinter in the manual.')
            sys.exit(1)

        # check if the library PIL.Image is installed
        try:
            import PIL.Image
        except Exception as e:
            print('*** ERROR: The library PIL.Image is not installed.')
            print('Please, review how to install PIL.Image in the manual.')
            sys.exit(1)

        # check if the library PIL.ImageTk is installed
        try:
            import PIL.ImageTk
        except Exception as e:
            print('*** ERROR: The library PIL.ImageTk is not installed.')
            print('Please, review how to install PIL.ImageTk in the manual.')
            sys.exit(1)

        # check if the library requests is installed
        try:
            import requests
        except Exception as e:
            print('*** ERROR: The library requests is not installed.')
            print('Please, review how to requests in the manual.')
            sys.exit(1)

        # check if the library plotnine is installed
        try:
            import plotnine
        except Exception as e:
            print('*** ERROR: The library plotnine is not installed.')
            print('Please, review how to requests in the manual.')
            sys.exit(1)

    # import required modules
    import cmenu
    import gmain

    # start the user interface depending on the mode
    if args.mode == 'gui' or args.mode is None:
        main = gmain.Main()
        main.mainloop()
    else:
        cmenu.build_menu_main()

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # import the module xlib
    import xlib

    # create the parser and add arguments
    description = f'Description: This program starts {xlib.get_long_project_name()} both console mode and gui mode.'
    text = f'{xlib.get_long_project_name()} v{xlib.get_project_version()} - {os.path.basename(__file__)}\n\n{description}\n'
    usage = f'\r{text.ljust(len("usage:"))}\nUsage: {os.path.basename(__file__)} arguments'
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--mode', dest='mode', help='Mode: console or gui')

    # return the paser
    return parser

#-------------------------------------------------------------------------------

def check_args(args):
    '''
    Check the input arguments.
    '''

    # import the module xlib
    import xlib

    # initialize the control variable
    OK = True

    # check mode
    if args.mode is not None and args.mode not in ['console', 'gui']:
        print('*** ERROR: The mode has to be console or gui.')
        OK = False

    # control if there are any errors
    if not OK:
        raise xlib.ProgramException('P001')

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
