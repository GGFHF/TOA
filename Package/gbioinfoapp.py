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

class FormInstallBioinfoApp(tkinter.Frame):

    #---------------

    def __init__(self, parent, main, app):
        '''
        Execute actions correspending to the creation of a "FormInstallBioinfoApp" instance.
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

        elif self.app_code == xlib.get_diamond_code():
            self.app_name = xlib.get_diamond_name()

        elif self.app_code == xlib.get_entrez_direct_code():
            self.app_name = xlib.get_entrez_direct_name()

        elif self.app_code == xlib.get_miniconda3_code():
            self.app_name = xlib.get_miniconda3_name()

        elif self.app_code == xlib.get_r_code():
            self.app_name = xlib.get_r_name()

        elif self.app_code == xlib.get_transdecoder_code():
            self.app_name = xlib.get_transdecoder_name()

        # assign the text of the "head"
        self.head = f'{self.app_name} - Install software'

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
        Build the graphical user interface of "FormInstallBioinfoApp".
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
        Check the content of each input of "FormInstallBioinfoApp" and do the actions linked to its value
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def execute(self):
        '''
        Execute the app installation process.
        '''

        # check inputs
        OK = self.check_inputs()
        if not OK:
            message = 'Some input values are not OK.'
            tkinter.messagebox.showerror(f'{xlib.get_short_project_name()} - {self.head}', message)

        # confirm the software installation
        if OK:
            if self.app_code == xlib.get_miniconda3_code():
                message = f'{self.app_name} (Conda infrastructure) is going to be installed. All Conda packages previously installed will be lost and they have to be reinstalled.\n\nAre you sure to continue?'
            elif self.app_code == xlib.get_r_code():
                message = f'{self.app_name} and analysis packages are going to be installed. The previous version will be lost, if it exists.\n\nAre you sure to continue?'
            else:
                message = f'The {self.app_name} Conda package is going to be installed. The previous version will be lost, if it exists.\n\nAre you sure to continue?'
            OK = tkinter.messagebox.askyesno(f'{xlib.get_short_project_name()} - {self.head}', message)

        # install the software
        if OK:

            # install the BLAST+ software
            if self.app_code == xlib.get_blastplus_code():
                # -- package_list = [(xlib.get_blastplus_conda_code(), 'last')]
                package_list = [(xlib.get_blastplus_conda_code(), '2.9.0')]
                dialog_log = gdialogs.DialogLog(self, self.head, xbioinfoapp.install_conda_package_list.__name__)
                threading.Thread(target=self.wait_window, args=(dialog_log,)).start()
                threading.Thread(target=xbioinfoapp.install_conda_package_list, args=(self.app_code, self.app_name, package_list, dialog_log, lambda: dialog_log.enable_button_close())).start()

            # install the DIAMOND software
            elif self.app_code == xlib.get_diamond_code():
                # -- package_list = [(xlib.get_diamond_conda_code(), 'last')]
                package_list = [(xlib.get_diamond_conda_code(), '0.9.34')]
                dialog_log = gdialogs.DialogLog(self, self.head, xbioinfoapp.install_conda_package_list.__name__)
                threading.Thread(target=self.wait_window, args=(dialog_log,)).start()
                threading.Thread(target=xbioinfoapp.install_conda_package_list, args=(self.app_code, self.app_name, package_list, dialog_log, lambda: dialog_log.enable_button_close())).start()

            # install the Entrez Direct software
            elif self.app_code == xlib.get_entrez_direct_code():
                package_list = [(xlib.get_entrez_direct_conda_code(), 'last')]
                dialog_log = gdialogs.DialogLog(self, self.head, xbioinfoapp.install_conda_package_list.__name__)
                threading.Thread(target=self.wait_window, args=(dialog_log,)).start()
                threading.Thread(target=xbioinfoapp.install_conda_package_list, args=(self.app_code, self.app_name, package_list, dialog_log, lambda: dialog_log.enable_button_close())).start()

            # install the Miniconda3 software
            elif self.app_code == xlib.get_miniconda3_code():
                dialog_log = gdialogs.DialogLog(self, self.head, xbioinfoapp.install_miniconda3.__name__)
                threading.Thread(target=self.wait_window, args=(dialog_log,)).start()
                threading.Thread(target=xbioinfoapp.install_miniconda3, args=(dialog_log, lambda: dialog_log.enable_button_close())).start()

            # install R and analysis packages
            elif self.app_code == xlib.get_r_code():
                dialog_log = gdialogs.DialogLog(self, self.head, xbioinfoapp.install_r.__name__)
                threading.Thread(target=self.wait_window, args=(dialog_log,)).start()
                threading.Thread(target=xbioinfoapp.install_r, args=(dialog_log, lambda: dialog_log.enable_button_close())).start()

            # install the TransDecoder software
            elif self.app_code == xlib.get_transdecoder_code():
                package_list = [(xlib.get_transdecoder_conda_code(), 'last')]
                dialog_log = gdialogs.DialogLog(self, self.head, xbioinfoapp.install_conda_package_list.__name__)
                threading.Thread(target=self.wait_window, args=(dialog_log,)).start()
                threading.Thread(target=xbioinfoapp.install_conda_package_list, args=(self.app_code, self.app_name, package_list, dialog_log, lambda: dialog_log.enable_button_close())).start()

        # close the form
        if OK:
            self.close()

    #---------------

    def close(self):
        '''
        Close "FormInstallBioinfoApp".
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
