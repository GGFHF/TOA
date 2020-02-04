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
This file contains the classes related to BioInfo application forms in gui mode.
'''

#-------------------------------------------------------------------------------

import sys
import threading
import tkinter
import tkinter.ttk

import gdialogs
import xbioinfoapp
import xlib

#-------------------------------------------------------------------------------

class FormSetupBioinfoApp(tkinter.Frame):

    #---------------

    def __init__(self, parent, main, app):
        '''
        Execute actions correspending to the creation of a "FormSetupBioinfoApp" instance.
        '''

        # save initial parameters in instance variables
        self.parent = parent
        self.main = main
        self.app_code = app

        # call the init method of the parent class
        tkinter.Frame.__init__(self, self.parent)

        # set cursor to show busy status
        self.main.config(cursor='watch')
        self.main.update()

        # set the software name
        if self.app_code == xlib.get_blastplus_code():
            self.app_name = xlib.get_blastplus_name()
        elif self.app_code == xlib.get_entrez_direct_code():
            self.app_name = xlib.get_entrez_direct_name()
        elif self.app_code == xlib.get_miniconda3_code():
            self.app_name = xlib.get_miniconda3_name()
        elif self.app_code == xlib.get_r_code():
            self.app_name = xlib.get_r_name()
        elif self.app_code == xlib.get_transdecoder_code():
            self.app_name = xlib.get_transdecoder_name()

        # assign the text of the "head"
        self.head = '{0} - Set up software'.format(self.app_name)

        # create the wrappers to track changes in the inputs
        pass

        # build the graphical user interface
        self.build_gui()

        # load initial data in inputs
        self.initialize_inputs()

        # set cursor to show normal status
        self.main.config(cursor='')
        self.main.update()

    #---------------

    def build_gui(self):
        '''
        Build the graphical user interface of "FormSetupBioinfoApp".
        '''

        # assign the text to the label of the current process name
        self.main.label_process['text'] = self.head

        # create "label_fit" and register it with the grid geometry manager
        self.label_fit = tkinter.Label(self, text=' '*(168+xlib.get_os_size_fix()))
        self.label_fit.grid(row=0, column=3, padx=(0,0), pady=(75,5), sticky='e')

        # create "button_execute" and register it with the grid geometry manager
        self.button_execute = tkinter.ttk.Button(self, text='Execute', command=self.execute)
        self.button_execute.grid(row=0, column=4, padx=(5,5), pady=(75,5), sticky='e')

        # create "button_close" and register it with the grid geometry manager
        self.button_close = tkinter.ttk.Button(self, text='Close', command=self.close)
        self.button_close.grid(row=0, column=5, padx=(5,5), pady=(75,5), sticky='w')

        # link a handler to events
        pass

    #---------------

    def initialize_inputs(self):
        '''
        Load initial data in inputs.
        '''

        pass

    #---------------

    def check_inputs(self, *args):
        '''
        Check the content of each input of "FormSetupBioinfoApp" and do the actions linked to its value
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def execute(self):
        '''
        Execute the app set up process.
        '''

        # check inputs
        OK = self.check_inputs()
        if not OK:
            message = 'Some input values are not OK.'
            tkinter.messagebox.showerror('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # confirm the software set up
        if OK:
            if self.app_code == xlib.get_miniconda3_code():
                message = '{0} (Bioconda infrastructure) is going to be set up. All Bioconda packages previously set up will be lost and they have to be reinstalled.\n\nAre you sure to continue?'.format(self.app_name)
            elif self.app_code == xlib.get_r_code():
                message = '{0} and analysis packages are going to be set up. The previous version will be lost, if it exists.\n\nAre you sure to continue?'.format(self.app_name)
            else:
                message = 'The {0} Bioconda package is going to be set up. The previous version will be lost, if it exists.\n\nAre you sure to continue?'.format(self.app_name)
            OK = tkinter.messagebox.askyesno('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # set up the software
        if OK:

            # set up the BLAST+ software
            if self.app_code == xlib.get_blastplus_code():
                package_list = [(xlib.get_blastplus_bioconda_code(), 'last')]
                dialog_log = gdialogs.DialogLog(self, self.head, xbioinfoapp.setup_bioconda_package_list.__name__)
                threading.Thread(target=self.wait_window, args=(dialog_log,)).start()
                threading.Thread(target=xbioinfoapp.setup_bioconda_package_list, args=(self.app_code, self.app_name, package_list, dialog_log, lambda: dialog_log.enable_button_close())).start()


            # set up the Entrez Direct software
            elif self.app_code == xlib.get_entrez_direct_code():
                package_list = [(xlib.get_entrez_direct_bioconda_code(), 'last')]
                dialog_log = gdialogs.DialogLog(self, self.head, xbioinfoapp.setup_bioconda_package_list.__name__)
                threading.Thread(target=self.wait_window, args=(dialog_log,)).start()
                threading.Thread(target=xbioinfoapp.setup_bioconda_package_list, args=(self.app_code, self.app_name, package_list, dialog_log, lambda: dialog_log.enable_button_close())).start()

            # set up the Miniconda3 software
            elif self.app_code == xlib.get_miniconda3_code():
                dialog_log = gdialogs.DialogLog(self, self.head, xbioinfoapp.setup_miniconda3.__name__)
                threading.Thread(target=self.wait_window, args=(dialog_log,)).start()
                threading.Thread(target=xbioinfoapp.setup_miniconda3, args=(dialog_log, lambda: dialog_log.enable_button_close())).start()

            # set up R and analysis packages
            elif self.app_code == xlib.get_r_code():
                dialog_log = gdialogs.DialogLog(self, self.head, xbioinfoapp.setup_r.__name__)
                threading.Thread(target=self.wait_window, args=(dialog_log,)).start()
                threading.Thread(target=xbioinfoapp.setup_r, args=(dialog_log, lambda: dialog_log.enable_button_close())).start()

            # set up the TransDecoder software
            elif self.app_code == xlib.get_transdecoder_code():
                package_list = [(xlib.get_transdecoder_bioconda_code(), 'last')]
                dialog_log = gdialogs.DialogLog(self, self.head, xbioinfoapp.setup_bioconda_package_list.__name__)
                threading.Thread(target=self.wait_window, args=(dialog_log,)).start()
                threading.Thread(target=xbioinfoapp.setup_bioconda_package_list, args=(self.app_code, self.app_name, package_list, dialog_log, lambda: dialog_log.enable_button_close())).start()

        # close the form
        if OK:
            self.close()

    #---------------

    def close(self):
        '''
        Close "FormSetupBioInfoApp".
        '''

        # clear the label of the current process name
        self.main.label_process['text'] = ''

        # close the current form
        self.main.close_current_form()

    #---------------

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print('This file contains the classes related to BioInfo application forms in gui mode.')
    sys.exit(0)

#-------------------------------------------------------------------------------
