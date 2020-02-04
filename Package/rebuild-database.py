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
This program rebuilds a TOA database.
'''

#-------------------------------------------------------------------------------

import argparse
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

    # rebuild the TOA database file
    xlib.Message.print('verbose', 'Rebuilding TOA database ...\n')
    OK = xsqlite.rebuild_database(conn)
    if OK:
        xlib.Message.print('verbose', 'The database is rebuilt.\n')
    else:
        xlib.Message.print('error', '*** WARNING: The database file can not be rebuilt.')

    # close connection to TOA database
    conn.close()

#-------------------------------------------------------------------------------

def build_parser():
    '''
    Build the parser with the available arguments.
    '''

    # create the parser and add arguments
    description = 'Description: This program rebuilds a TOA database.'
    text = '{0} v{1} - {2}\n\n{3}\n'.format(xlib.get_long_project_name(), xlib.get_project_version(), os.path.basename(__file__), description)
    usage = '\r{0}\nUsage: {1} arguments'.format(text.ljust(len('usage:')), os.path.basename(__file__))
    parser = argparse.ArgumentParser(usage=usage)
    parser._optionals.title = 'Arguments'
    parser.add_argument('--db', dest='toa_database', help='Path of the TOA database (mandatory).')
    parser.add_argument('--verbose', dest='verbose', help='Additional job status info during the run: {0}; default: {1}.'.format(xlib.get_verbose_code_list_text(), xlib.Const.DEFAULT_VERBOSE))
    parser.add_argument('--trace', dest='trace', help='Additional info useful to the developer team: {0}; default: {1}.'.format(xlib.get_trace_code_list_text(), xlib.Const.DEFAULT_TRACE))

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

    # check "verbose"
    if args.verbose is None:
        args.verbose = xlib.Const.DEFAULT_VERBOSE
    elif not xlib.check_code(args.verbose, xlib.get_verbose_code_list(), case_sensitive=False):
        xlib.Message.print('error', '*** verbose has to be {0}.'.format(xlib.get_verbose_code_list_text()))
        OK = False
    if args.verbose.upper() == 'Y':
        xlib.Message.set_verbose_status(True)

    # check "trace"
    if args.trace is None:
        args.trace = xlib.Const.DEFAULT_TRACE
    elif not xlib.check_code(args.trace, xlib.get_trace_code_list(), case_sensitive=False):
        xlib.Message.print('error', '*** trace has to be {0}.'.format(xlib.get_trace_code_list_text()))
        OK = False
    if args.trace.upper() == 'Y':
        xlib.Message.set_trace_status(True)

    # if there are errors, exit with exception
    if not OK:
        raise xlib.ProgramException('P001')

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    main(sys.argv[1:])
    sys.exit(0)

#-------------------------------------------------------------------------------
