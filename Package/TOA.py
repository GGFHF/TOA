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
This source starts Tree-oriented Annotation (TOA) both console mode and gui mode.
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
        print('*** ERROR: The {0} OS is not supported.'.format(sys.platform))
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
        print('*** ERROR: {0} has to be run in the TOA home directory.'.format(program_name))
        sys.exit(1)

    # check if Plotnine is set up
    try:
        import plotnine
    except Exception as e:
        print('*** ERROR: The library paramiko is not installed.')
        print('Please, review how to set up Paramiko in the manual.')
        sys.exit(1)

    # get and check the arguments
    parser = build_parser()
    args = parser.parse_args()
    check_args(args)

    # check if the required graphical libraries are setup
    if args.mode == 'gui' or args.mode is None:

        # check if the library PIL.Image is set up
        try:
            import tkinter
        except Exception as e:
            print('*** ERROR: The library tkinter is not installed.')
            print('Please, review how to set up Tkinter in the manual.')
            sys.exit(1)

        # check if the library PIL.Image is set up
        try:
            import PIL.Image
        except Exception as e:
            print('*** ERROR: The library PIL.Image is not installed.')
            print('Please, review how to set up PIL.Image in the manual.')
            sys.exit(1)

        # check if the library PIL.ImageTk is set up
        try:
            import PIL.ImageTk
        except Exception as e:
            print('*** ERROR: The library PIL.ImageTk is not installed.')
            print('Please, review how to set up PIL.ImageTk in the manual.')
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
    description = 'Description: This program starts {0} both console mode and gui mode.'.format(xlib.get_long_project_name())
    text = '{0} v{1} - {2}\n\n{3}\n'.format(xlib.get_long_project_name(), xlib.get_project_version(), os.path.basename(__file__), description)
    usage = '\r{0}\nUsage: {1} arguments'.format(text.ljust(len('usage:')), os.path.basename(__file__))
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
