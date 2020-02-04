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
This file contains the classes related to forms corresponding to TOA (Tree-oriented Annotation)
menu items in gui mode.
'''

#-------------------------------------------------------------------------------

import matplotlib
import os
import pandas
import pathlib
import PIL.Image
import PIL.ImageTk
import plotnine
import sys
import threading
import tkinter
import tkinter.filedialog
import tkinter.ttk
import webbrowser

import gdialogs
import xlib
import xtoa

#-------------------------------------------------------------------------------

class FormRecreateToaConfigFile(tkinter.Frame):

    #---------------

    def __init__(self, parent, main):
        '''
        Execute actions correspending to the creation of a "FormRecreateToaConfigFile" instance.
        '''

        # save initial parameters in instance variables
        self.parent = parent
        self.main = main

        # call the init method of the parent class
        tkinter.Frame.__init__(self, self.parent)

        # set cursor to show busy status
        self.main.config(cursor='watch')
        self.main.update()

        # assign the text of the "head"
        self.head = 'Recreate {0} config file'.format(xlib.get_toa_name())

        # create the wrappers to track changes in inputs
        self.wrapper_miniconda3_dir = tkinter.StringVar()
        self.wrapper_miniconda3_dir.trace('w', self.check_inputs)
        self.wrapper_db_dir = tkinter.StringVar()
        self.wrapper_db_dir.trace('w', self.check_inputs)
        self.wrapper_result_dir = tkinter.StringVar()
        self.wrapper_result_dir.trace('w', self.check_inputs)

        # build the graphical user interface
        self.build_gui()

        # load initial value to inputs
        self.initialize_inputs()

        # set cursor to show normal status
        self.main.config(cursor='')
        self.main.update()

    #---------------

    def build_gui(self):
        '''
        Build the graphical user interface of "FormRecreateToaConfigFile".
        '''

        # assign the text to the label of the current process name
        self.main.label_process['text'] = self.head

        # create "label_miniconda3_dir" and register it with the grid geometry manager
        self.label_miniconda3_dir = tkinter.Label(self, text='Miniconda directory')
        self.label_miniconda3_dir.grid(row=0, column=0, padx=(15,5), pady=(75,5), sticky='e')

        # create "entry_miniconda3_dir" and register it with the grid geometry manager
        self.entry_miniconda3_dir = tkinter.Entry(self, textvariable=self.wrapper_miniconda3_dir, width=60, validatecommand=self.check_inputs)
        self.entry_miniconda3_dir.grid(row=0, column=1, padx=(5,5), pady=(75,5), sticky='w')

        # create "label_miniconda3_dir_warning" and register it with the grid geometry manager
        self.label_miniconda3_dir_warning = tkinter.Label(self, text='')
        self.label_miniconda3_dir_warning.grid(row=1, column=1, padx=(5,5), pady=(5,5), sticky='w')

        # create "label_db_dir" and register it with the grid geometry manager
        self.label_db_dir = tkinter.Label(self, text='Database directory')
        self.label_db_dir.grid(row=2, column=0, padx=(15,5), pady=(25,5), sticky='e')

        # create "entry_db_dir" and register it with the grid geometry manager
        self.entry_db_dir = tkinter.Entry(self, textvariable=self.wrapper_db_dir, width=60, validatecommand=self.check_inputs)
        self.entry_db_dir.grid(row=2, column=1, padx=(5,5), pady=(25,5), sticky='w')

        # create "label_db_dir_warning" and register it with the grid geometry manager
        self.label_db_dir_warning = tkinter.Label(self, text='')
        self.label_db_dir_warning.grid(row=3, column=1, padx=(5,5), pady=(5,5), sticky='w')

        # create "label_result_dir" and register it with the grid geometry manager
        self.label_result_dir = tkinter.Label(self, text='Result directory')
        self.label_result_dir.grid(row=4, column=0, padx=(15,5), pady=(25,5), sticky='e')

        # create "entry_result_dir" and register it with the grid geometry manager
        self.entry_result_dir = tkinter.Entry(self, textvariable=self.wrapper_result_dir, width=60, validatecommand=self.check_inputs)
        self.entry_result_dir.grid(row=4, column=1, padx=(5,5), pady=(25,5), sticky='w')

        # create "label_result_dir_warning" and register it with the grid geometry manager
        self.label_result_dir_warning = tkinter.Label(self, text='')
        self.label_result_dir_warning.grid(row=5, column=1, padx=(5,5), pady=(5,5), sticky='w')

        # create "label_fit" and register it with the grid geometry manager
        self.label_fit = tkinter.Label(self, text=' '*(1+xlib.get_os_size_fix()))
        self.label_fit.grid(row=6, column=2, padx=(0,0), pady=(25,5), sticky='e')

        # create "button_execute" and register it with the grid geometry manager
        self.button_execute = tkinter.ttk.Button(self, text='Execute', command=self.execute, state='disabled')
        self.button_execute.grid(row=6, column=3, padx=(5,5), pady=(25,5), sticky='e')

        # create "button_close" and register it with the grid geometry manager
        self.button_close = tkinter.ttk.Button(self, text='Close', command=self.close)
        self.button_close.grid(row=6, column=4, padx=(5,5), pady=(25,5), sticky='w')

        # link a handler to events
        pass

    #---------------

    def initialize_inputs(self):
        '''
        Load initial data in inputs.
        '''

        # get the HOME directory
        home_dir = str(pathlib.Path.home())

        # load initial data in inputs
        self.wrapper_miniconda3_dir.set('{0}/TOA-Miniconda3'.format(home_dir))
        self.wrapper_db_dir.set('{0}/TOA-databases'.format(home_dir))
        self.wrapper_result_dir.set('{0}/TOA-results'.format(home_dir))

    #---------------

    def check_inputs(self, *args):
        '''
        Check the content of each input of "FormRecreateToaConfigFile" and do the actions linked to its value
        '''

        # initialize the control variable
        OK = True

        # check the content of "entry_miniconda3_dir"
        if not self.check_entry_miniconda3_dir():
            OK = False

        # check the content of "entry_db_dir"
        if not self.check_entry_db_dir():
            OK = False

        # check the content of "entry_result_dir"
        if not self.check_entry_result_dir():
            OK = False

        # check if "button_execute" has to be enabled or disabled
        if self.wrapper_miniconda3_dir.get() != '' and self.wrapper_db_dir.get() != '' and self.wrapper_result_dir.get() != '':
            self.button_execute['state'] = 'enable'
        else:
            self.button_execute['state'] = 'disabled'

        # return the control variable
        return OK

    #---------------

    def check_entry_miniconda3_dir(self):
        '''
        Check the content of "entry_miniconda3_dir"
        '''

        # initialize the control variable
        OK = True

        # check if the path in "entry_miniconda3_dir" is valid
        if self.wrapper_miniconda3_dir.get() == '' or not xlib.is_absolute_path(self.wrapper_miniconda3_dir.get()):
            self.label_miniconda3_dir_warning['text'] = 'It is not an absolute path.'
            self.label_miniconda3_dir_warning['foreground'] = 'red'
            OK = False
        else:
            self.label_miniconda3_dir_warning['text'] = ''
            self.label_miniconda3_dir_warning['foreground'] = 'black'

        # return the control variable
        return OK

    #---------------

    def check_entry_db_dir(self):
        '''
        Check the content of "entry_db_dir"
        '''

        # initialize the control variable
        OK = True

        # check if the path in "entry_db_dir" is valid
        if self.wrapper_db_dir.get() == ''  or not xlib.is_absolute_path(self.wrapper_db_dir.get()):
            self.label_db_dir_warning['text'] = 'It is not an absolute path.'
            self.label_db_dir_warning['foreground'] = 'red'
            OK = False
        else:
            self.label_db_dir_warning['text'] = ''
            self.label_db_dir_warning['foreground'] = 'black'

        # return the control variable
        return OK

    #---------------

    def check_entry_result_dir(self):
        '''
        Check the content of "entry_result_dir"
        '''

        # initialize the control variable
        OK = True

        # check if the path in "entry_result_dir" is valid
        if self.wrapper_result_dir.get() == ''  or not xlib.is_absolute_path(self.wrapper_result_dir.get()):
            self.label_result_dir_warning['text'] = 'It is not an absolute path.'
            self.label_result_dir_warning['foreground'] = 'red'
            OK = False
        else:
            self.label_result_dir_warning['text'] = ''
            self.label_result_dir_warning['foreground'] = 'black'

        # return the control variable
        return OK

    #---------------

    def execute(self):
        '''
        Execute the recreation of the TOA config file.
        '''

        # check inputs
        OK = self.check_inputs()
        if not OK:
            message = 'Some input values are not OK.'
            tkinter.messagebox.showerror('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # confirm the recreation of the TOA config file
        if OK:
            message = 'The file {0} is going to be recreated. The previous file will be lost.\n\nAre you sure to continue?'.format(xtoa.get_toa_config_file())
            OK = tkinter.messagebox.askyesno('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # set the TOA directory
        if OK:
            toa_dir = os.path.dirname(os.path.abspath(__file__))

        # recreate the TOA config file corresponding to the environment
        if OK:
            (OK, error_list) = xtoa.create_toa_config_file(toa_dir, self.wrapper_miniconda3_dir.get(), self.wrapper_db_dir.get(), self.wrapper_result_dir.get())
            if OK:
                message = 'The file {0} is created with default values.'.format(xtoa.get_toa_config_file())
                tkinter.messagebox.showinfo('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)
            else:
                message = ''
                for error in error_list:
                    message = '{0}{1}\n'.format(message, error) 
                tkinter.messagebox.showerror('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)
                OK = False

        # close the form
        if OK:
            self.close()

    #---------------

    def close(self):
        '''
        Close "FormRecreateToaConfigFile".
        '''

        # clear the label of the current process name
        self.main.label_process['text'] = ''

        # close the current form
        self.main.close_current_form()

   #---------------

#-------------------------------------------------------------------------------

class FormManageToaDatabase(tkinter.Frame):

    #---------------

    def __init__(self, parent, main, process_type):
        '''
        Execute actions correspending to the creation of a "FormManageToaDatabase" instance.
        '''

        # save initial parameters in instance variables
        self.parent = parent
        self.main = main
        self.process_type = process_type

        # call the init method of the parent class
        tkinter.Frame.__init__(self, self.parent)

        # set cursor to show busy status
        self.main.config(cursor='watch')
        self.main.update()

        # assign the text of the "head"
        if self.process_type == xlib.get_toa_type_recreate():
            self.head = 'Recreate {0} database'.format(xlib.get_toa_name())
        elif self.process_type == xlib.get_toa_type_rebuild():
            self.head = 'Rebuild {0} database'.format(xlib.get_toa_name())

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
        Build the graphical user interface of "FormManageToaDatabase".
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
        Check the content of each input of "FormManageToaDatabase" and do the actions linked to its value
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def execute(self):
        '''
        Run TOA process.
        '''

        # check inputs
        OK = self.check_inputs()
        if not OK:
            message = 'Some input values are not OK.'
            tkinter.messagebox.showerror('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # confirm the process run
        if OK:
            message = 'The {0} database is going to be {1}.\n\nAre you sure to continue?'.format(xlib.get_toa_name(), self.process_type)
            OK = tkinter.messagebox.askyesno('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # execute the process
        if OK:

            dialog_log = gdialogs.DialogLog(self, self.head, xtoa.manage_toa_database.__name__)
            threading.Thread(target=self.wait_window, args=(dialog_log,)).start()
            threading.Thread(target=xtoa.manage_toa_database, args=(self.process_type, dialog_log, lambda: dialog_log.enable_button_close())).start()

        # close the form
        if OK:
            self.close()

    #---------------

    def close(self):
        '''
        Close "FormManageToaDatabase".
        '''

        # clear the label of the current process name
        self.main.label_process['text'] = ''

        # close the current form
        self.main.close_current_form()

    #---------------

#-------------------------------------------------------------------------------

class FormManageGenomicDatabase(tkinter.Frame):

    #---------------

    def __init__(self, parent, main, process_type, genomic_database):
        '''
        Execute actions correspending to the creation of a "FormManageGenomicDatabase" instance.
        '''

        # save initial parameters in instance variables
        self.parent = parent
        self.main = main
        self.process_type = process_type
        self.genomic_database = genomic_database

        # call the init method of the parent class
        tkinter.Frame.__init__(self, self.parent)

        # set cursor to show busy status
        self.main.config(cursor='watch')
        self.main.update()

        # set the genomica database name
        if self.genomic_database == xlib.get_toa_data_basic_data_code():
            self.name = xlib.get_toa_data_basic_data_name()
        elif self.genomic_database == xlib.get_toa_data_gymno_01_code():
            self.name = xlib.get_toa_data_gymno_01_name()
        elif self.genomic_database == xlib.get_toa_data_dicots_04_code():
            self.name = xlib.get_toa_data_dicots_04_name()
        elif self.genomic_database == xlib.get_toa_data_monocots_04_code():
            self.name = xlib.get_toa_data_monocots_04_name()
        elif self.genomic_database == xlib.get_toa_data_refseq_plant_code():
            self.name = xlib.get_toa_data_refseq_plant_name()
        elif self.genomic_database == xlib.get_toa_data_nt_code():
            self.name = xlib.get_toa_data_nt_name()
        elif self.genomic_database == xlib.get_toa_data_viridiplantae_nucleotide_gi_code():
            self.name = xlib.get_toa_data_viridiplantae_nucleotide_gi_name()
        elif self.genomic_database == xlib.get_toa_data_nr_code():
            self.name = xlib.get_toa_data_nr_name()
        elif self.genomic_database == xlib.get_toa_data_viridiplantae_protein_gi_code():
            self.name = xlib.get_toa_data_viridiplantae_protein_gi_name()
        elif self.genomic_database == xlib.get_toa_data_gene_code():
            self.name = xlib.get_toa_data_gene_name()
        elif self.genomic_database == xlib.get_toa_data_interpro_code():
            self.name = xlib.get_toa_data_interpro_name()
        elif self.genomic_database == xlib.get_toa_data_go_code():
            self.name = xlib.get_toa_data_go_name()

        # assign the text of the "head"
        if process_type == xlib.get_toa_type_build_blastdb():
            self.head = 'Build {0}'.format(self.name)
        elif process_type == xlib.get_toa_type_build_gilist():
            self.head = 'Build {0}'.format(self.name)
        elif process_type == xlib.get_toa_type_build_proteome():
            self.head = 'Build {0} proteome'.format(self.name)
        elif process_type == xlib.get_toa_type_download_data():
            self.head = 'Download {0} functional annotations'.format(self.name)
        elif process_type == xlib.get_toa_type_load_data():
            self.head = 'Load {0} data in {1} database'.format(self.name, xlib.get_toa_name())

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
        Build the graphical user interface of "FormManageGenomicDatabase".
        '''

        # assign the text to the label of the current process name
        self.main.label_process['text'] = self.head

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
        Check the content of each input of "FormManageGenomicDatabase" and do the actions linked to its value
        '''

        # initialize the control variable
        OK = True

        # return the control variable
        return OK

    #---------------

    def execute(self):
        '''
        Run TOA process.
        '''

        # check inputs
        OK = self.check_inputs()
        if not OK:
            message = 'Some input values are not OK.'
            tkinter.messagebox.showerror('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # confirm the process run
        if OK:
            message = 'The {0} process is going to be run.\n\nAre you sure to continue?'.format(self.name)
            OK = tkinter.messagebox.askyesno('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # execute the process
        if OK:

            dialog_log = gdialogs.DialogLog(self, self.head, xtoa.manage_genomic_database.__name__)
            threading.Thread(target=self.wait_window, args=(dialog_log,)).start()
            threading.Thread(target=xtoa.manage_genomic_database, args=(self.process_type, self.genomic_database, dialog_log, lambda: dialog_log.enable_button_close())).start()

        # close the form
        if OK:
            self.close()

    #---------------

    def close(self):
        '''
        Close "FormManageGenomicDatabase".
        '''

        # clear the label of the current process name
        self.main.label_process['text'] = ''

        # close the current form
        self.main.close_current_form()

    #---------------

#-------------------------------------------------------------------------------

class FormRecreatePipelineConfigFile(tkinter.Frame):

    #---------------

    def __init__(self, parent, main, pipeline_type):
        '''
        Execute actions correspending to the creation of a "FormRecreatePipelineConfigFile" instance.
        '''

        # save initial parameters in instance variables
        self.parent = parent
        self.main = main
        self.pipeline_type = pipeline_type

        # call the init method of the parent class
        tkinter.Frame.__init__(self, self.parent)

        # set cursor to show busy status
        self.main.config(cursor='watch')
        self.main.update()

        # set the name
        if self.pipeline_type == xlib.get_toa_process_pipeline_nucleotide_code():
            self.name = xlib.get_toa_process_pipeline_nucleotide_name()
        elif self.pipeline_type == xlib.get_toa_process_pipeline_aminoacid_code():
            self.name = xlib.get_toa_process_pipeline_aminoacid_name()

        # assign the text of the "head"
        self.head = '{0} - Recreate config file'.format(self.name)

        # initialize the selected alignment dataset list
        self.selected_database_list = []

        # initialize the database dictionary
        self.database_dict = {}
        if self.pipeline_type == xlib.get_toa_process_pipeline_nucleotide_code():
            candidate_database_list = xtoa.get_nucleotide_annotation_database_code_list()
        elif self.pipeline_type == xlib.get_toa_process_pipeline_aminoacid_code():
            candidate_database_list = xtoa.get_aminoacid_annotation_database_code_list()
        for database in candidate_database_list:
            self.database_dict [database] = 0

        # create the wrappers to track changes in inputs
        self.wrapper_transcriptome_dir = tkinter.StringVar()
        self.wrapper_transcriptome_dir.trace('w', self.check_inputs)
        self.wrapper_transcriptome_file = tkinter.StringVar()
        self.wrapper_transcriptome_file.trace('w', self.check_inputs)
        self.wrapper_selected_databases = tkinter.StringVar()
        self.wrapper_selected_databases.trace('w', self.check_inputs)

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
        Build the graphical user interface of "FormRecreatePipelineConfigFile".
        '''

        # assign the text to the label of the current process name
        self.main.label_process['text'] = self.head

        # create "image_select_dirs"
        image_open_folder = PIL.Image.open('./image_open_folder.png')
        imagetk_open_folder = PIL.ImageTk.PhotoImage(image_open_folder)  
        image_select_dirs = PIL.Image.open('./image_select_dirs.png')
        imagetk_select_dirs = PIL.ImageTk.PhotoImage(image_select_dirs)

        # create "label_transcriptome_dir" and register it with the grid geometry manager
        self.label_transcriptome_dir = tkinter.Label(self, text='Transcriptome dir')
        self.label_transcriptome_dir.grid(row=0, column=0, padx=(15,5), pady=(75,5), sticky='e')

        # create "entry_transcriptome_dir" and register it with the grid geometry manager
        self.entry_transcriptome_dir = tkinter.Entry(self, textvariable=self.wrapper_transcriptome_dir, width=58, state='disabled', validatecommand=self.check_inputs)
        self.entry_transcriptome_dir.grid(row=0, column=1, padx=(5,5), pady=(75,5), sticky='w')

        # create "button_select_dir" and register it with the grid geometry manager
        self.button_select_dir = tkinter.ttk.Button(self, image=imagetk_open_folder, command=self.select_dir)
        self.button_select_dir.image = imagetk_open_folder
        self.button_select_dir.grid(row=0, column=2, padx=(5,0), pady=(75,5), sticky='w')

        # create "label_transcriptome_file" and register it with the grid geometry manager
        self.label_transcriptome_file = tkinter.Label(self, text='Transcriptome file')
        self.label_transcriptome_file.grid(row=1, column=0, padx=(5,5), pady=(45,5), sticky='e')

        # create "combobox_transcriptome_file" and register it with the grid geometry manager
        self.combobox_transcriptome_file = tkinter.ttk.Combobox(self, width=45, height=4, state='readonly', textvariable=self.wrapper_transcriptome_file)
        self.combobox_transcriptome_file.grid(row=1, column=1, padx=(5,5), pady=(45,5), sticky='w')

        # create "label_selected_databases" and register it with the grid geometry manager
        self.label_selected_databases = tkinter.Label(self, text='Selected databases')
        self.label_selected_databases.grid(row=2, column=0, padx=(15,5), pady=(45,5), sticky='e')

        # create "entry_selected_databases" and register it with the grid geometry manager
        self.entry_selected_databases = tkinter.Entry(self, textvariable=self.wrapper_selected_databases, width=58, state='disabled', validatecommand=self.check_inputs)
        self.entry_selected_databases.grid(row=2, column=1, padx=(5,5), pady=(45,5), sticky='w')

        # create "button_select_selected_databases" and register it with the grid geometry manager
        self.button_select_selected_databases = tkinter.ttk.Button(self, image=imagetk_select_dirs, command=self.select_databases, state='enable')
        self.button_select_selected_databases.image = imagetk_select_dirs
        self.button_select_selected_databases.grid(row=2, column=2, padx=(5,0), pady=(45,5), sticky='w')

        # create "label_fit" and register it with the grid geometry manager
        self.label_fit = tkinter.Label(self, text=' '*(1+xlib.get_os_size_fix()))
        self.label_fit.grid(row=3, column=3, padx=(0,0), pady=(45,5), sticky='e')

        # create "button_execute" and register it with the grid geometry manager
        self.button_execute = tkinter.ttk.Button(self, text='Execute', command=self.execute, state='disabled')
        self.button_execute.grid(row=3, column=4, padx=(0,5), pady=(45,5), sticky='e')

        # create "button_close" and register it with the grid geometry manager
        self.button_close = tkinter.ttk.Button(self, text='Close', command=self.close)
        self.button_close.grid(row=3, column=5, padx=(5,5), pady=(45,5), sticky='w')

        # link a handler to events
        self.combobox_transcriptome_file.bind('<<ComboboxSelected>>', self.combobox_transcriptome_file_selected_item)

    #---------------

    def initialize_inputs(self):
        '''
        Load initial data in inputs.
        '''

        # load initial data in inputs
        self.wrapper_transcriptome_dir.set('')
        self.combobox_transcriptome_file['values'] = []
        self.wrapper_transcriptome_file.set('')
        self.wrapper_selected_databases.set('')

    #---------------

    def populate_combobox_transcriptome_file(self):
        '''
        Populate data in "combobox_transcriptome_file".
        '''

        # clear the value selected in the combobox
        self.wrapper_transcriptome_file.set('')


        # initialize the transcriptome file name list
        transcriptome_file_name_list = []

        # get the transcriptome file name list
        file_name_list = [file_name for file_name in os.listdir(self.wrapper_transcriptome_dir.get()) if os.path.isfile(os.path.join(self.wrapper_transcriptome_dir.get(), file_name))]
        for file_name in file_name_list:
            transcriptome_file_name_list.append(file_name)

        # load the transcriptome file names in the combobox
        self.combobox_transcriptome_file['values'] = sorted(transcriptome_file_name_list)

    #---------------

    def select_dir(self):
        '''
        Select a directory and assign it to "entry_local_dir".
        '''

        # select the directory
        directory = tkinter.filedialog.askdirectory(parent=self, initialdir=".", title='Please select the transcriptome directory')

        # assign the directory to "entry_local_dir"
        if directory != '':
            self.wrapper_transcriptome_dir.set(directory)
            self.wrapper_transcriptome_file.set('')
            self.populate_combobox_transcriptome_file()
    
    #---------------

    def select_databases(self):
        '''
        Select the databases to annotate and update "entry_selected_databases".
        '''

        # get the database dictionary
        item_dict = {}
        for database_code in self.database_dict.keys():
            database_order = self.database_dict[database_code]
            item_dict[database_code] = {'option_id': database_code, 'option_value': database_order, 'comment': 'integer between 0 and 6', 'value_type': 'integer_list', 'admitted_option_value_list': [0, 1, 2, 3, 4, 5, 6]}

        # build the data dictionary
        data_dict = {}
        data_dict['option_id']= {'text': 'Database', 'width': 22, 'alignment': 'left'}
        data_dict['option_value'] = {'text': 'Annotation Order', 'width': 16, 'alignment': 'left'}
        data_dict['comment'] = {'text': 'Admitted Values', 'width': 22, 'alignment': 'left'}

        # create the dialog Table to show the nodes running
        title_text = 'Select databases'
        if sys.platform.startswith('linux'):
            window_height = 600
            window_width = 495
            auxliary_window_height = 60
            auxliary_window_width = 760
        elif sys.platform.startswith('darwin'):
            window_height = 600
            window_width = 495
            auxliary_window_height = 60
            auxliary_window_width = 830
        elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
            window_height = 600
            window_width = 485
            auxliary_window_height = 60
            auxliary_window_width = 760
        dialog_table = gdialogs.DialogOptionUpdate(self, title_text, window_height, window_width, auxliary_window_height, auxliary_window_width, data_dict, item_dict, item_dict.keys())
        self.wait_window(dialog_table)

        # update the database dictionary
        for database_code in self.database_dict.keys():
            self.database_dict[database_code] = item_dict[database_code]['option_value']

        # recreate the selected database list
        temp_dict = {}
        for database_code in self.database_dict.keys():
            if self.database_dict[database_code] != 0:
                temp_dict[self.database_dict[database_code]] = database_code
        self.selected_database_list = []
        for database_order in sorted(temp_dict.keys()):
            self.selected_database_list.append(temp_dict[database_order])

        # update "entry_selected_databases"
        self.wrapper_selected_databases.set(str(self.selected_database_list).strip('[]').replace('\'',''))

    #---------------

    def combobox_transcriptome_file_selected_item(self, event=None):
        '''
        Process the event when an item of "combobox_transcriptome_file" has been selected
        '''

        pass

    #---------------

    def check_inputs(self, *args):
        '''
        Check the content of each input of "FormRecreatePipelineConfigFile" and do the actions linked to its value
        '''

        # initialize the control variable
        OK = True

        # check the selected database order
        if self.wrapper_selected_databases.get() != '' and not self.check_database_order():
            OK = False

        # check if "button_execute" has to be enabled or disabled
        if self.wrapper_transcriptome_dir.get() != '' and self.wrapper_transcriptome_file.get() != '' and self.wrapper_selected_databases.get() != '':
            self.button_execute['state'] = 'enable'
        else:
            self.button_execute['state'] = 'disabled'

        # return the control variable
        return OK

    #---------------

    def check_database_order(self):
        '''
        Check the selected database order
        '''

        # initialize the control variable
        OK = True

        if self.pipeline_type == xlib.get_toa_process_pipeline_nucleotide_code():
            database_code_list = xtoa.get_nucleotide_annotation_database_code_list()
            database_order_list = [self.database_dict['dicots_04'], self.database_dict['gymno_01'], self.database_dict['monocots_04'], self.database_dict['refseq_plant'], self.database_dict['nt_viridiplantae'], self.database_dict['nt_complete']]
            last_database_code = 'nt_complete'
        elif self.pipeline_type == xlib.get_toa_process_pipeline_aminoacid_code():
            database_code_list = xtoa.get_aminoacid_annotation_database_code_list()
            database_order_list = [self.database_dict['dicots_04'], self.database_dict['gymno_01'], self.database_dict['monocots_04'], self.database_dict['refseq_plant'], self.database_dict['nr_viridiplantae'], self.database_dict['nr_complete']]
            last_database_code = 'nr_complete'
        (OK, error_list) = xtoa.check_database_order(database_code_list, database_order_list, last_database_code)
        if not OK:
            message = ''
            for error in error_list:
                message = '{0}{1}\n'.format(message, error) 
            tkinter.messagebox.showerror('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # return the control variable
        return OK

    #---------------

    def execute(self):
        '''
        Execute the creation of the config file.
        '''

        # check inputs
        OK = self.check_inputs()
        if not OK:
            message = 'Some input values are not OK.'
            tkinter.messagebox.showerror('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # get the config file
        if self.pipeline_type == xlib.get_toa_process_pipeline_nucleotide_code():
            config_file = xtoa.get_nucleotide_pipeline_config_file()
        elif self.pipeline_type == xlib.get_toa_process_pipeline_aminoacid_code():
            config_file = xtoa.get_aminoacid_pipeline_config_file()

        # confirm the creation of the pipeline config file
        if OK:
            message = 'The file {0} is going to be recreated. The previous file will be lost.\n\nAre you sure to continue?'.format(config_file)
            OK = tkinter.messagebox.askyesno('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # recreate the pipeline config file
        if OK:
            (OK, error_list) = xtoa.create_pipeline_config_file(self.pipeline_type, self.wrapper_transcriptome_dir.get(), self.wrapper_transcriptome_file.get(), self.selected_database_list)
            if not OK:
                message = ''
                for error in error_list:
                    message = '{0}{1}\n'.format(message, error) 
                tkinter.messagebox.showerror('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # edit the pipeline config file
        if OK:

            # edit the config file using "DialogEditor" 
            dialog_editor = gdialogs.DialogEditor(self, config_file)
            self.wait_window(dialog_editor)

            # check the config file
            (OK, error_list) = xtoa.check_pipeline_config_file(self.pipeline_type, strict=False)
            if OK:
                message = 'The {0} config file is OK.'.format(self.name)
                tkinter.messagebox.showinfo('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)
            else:
                message = 'Detected errors:\n\n'
                for error in error_list:
                    message = '{0}{1}\n'.format(message, error) 
                tkinter.messagebox.showerror('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # close the form
        self.close()

    #---------------

    def close(self):
        '''
        Close "FormRecreatePipelineConfigFile".
        '''

        # clear the label of the current process name
        self.main.label_process['text'] = ''

        # close the current form
        self.main.close_current_form()

    #---------------

#-------------------------------------------------------------------------------

class FormRunPipelineProcess(tkinter.Frame):

    #---------------

    def __init__(self, parent, main, pipeline_type):
        '''
        Execute actions correspending to the creation of a "FormRunPipelineProcess" instance.
        '''

        # save initial parameters in instance variables
        self.parent = parent
        self.main = main
        self.pipeline_type = pipeline_type

        # call the init method of the parent class
        tkinter.Frame.__init__(self, self.parent)

        # set cursor to show busy status
        self.main.config(cursor='watch')
        self.main.update()

        # set the name
        if self.pipeline_type == xlib.get_toa_process_pipeline_nucleotide_code():
            self.name = xlib.get_toa_process_pipeline_nucleotide_name()
        elif self.pipeline_type == xlib.get_toa_process_pipeline_aminoacid_code():
            self.name = xlib.get_toa_process_pipeline_aminoacid_name()

        # assign the text of the "head"
        self.head = '{0} - Run process'.format(self.name)

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
        Build the graphical user interface of "FormRunPipelineProcess".
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
        Check the content of each input of "FormRunPipelineProcess" and do the actions linked to its value
        '''

        # initialize the control variable
        OK = True


        # return the control variable
        return OK

    #---------------

    def execute(self):
        '''
        Run TOA process.
        '''

        # check inputs
        OK = self.check_inputs()
        if not OK:
            message = 'Some input values are not OK.'
            tkinter.messagebox.showerror('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # confirm the process run
        if OK:
            message = 'The {0} process is going to be run.\n\nAre you sure to continue?'.format(self.name)
            OK = tkinter.messagebox.askyesno('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # execute the process
        if OK:

            dialog_log = gdialogs.DialogLog(self, self.head, xtoa.run_pipeline_process.__name__)
            threading.Thread(target=self.wait_window, args=(dialog_log,)).start()
            threading.Thread(target=xtoa.run_pipeline_process, args=(self.pipeline_type, dialog_log, lambda: dialog_log.enable_button_close())).start()

        # close the form
        if OK:
            self.close()

    #---------------

    def close(self):
        '''
        Close "FormRunPipelineProcess".
        '''

        # clear the label of the current process name
        self.main.label_process['text'] = ''

        # close the current form
        self.main.close_current_form()

    #---------------

#-------------------------------------------------------------------------------

class FormRestartPipelineProcess(tkinter.Frame):

    #---------------

    def __init__(self, parent, main, pipeline_type):
        '''
        Execute actions correspending to the creation of a "FormRestartPipelineProcess" instance.
        '''

        # save initial parameters in instance variables
        self.parent = parent
        self.main = main
        self.pipeline_type = pipeline_type

        # call the init method of the parent class
        tkinter.Frame.__init__(self, self.parent)

        # set cursor to show busy status
        self.main.config(cursor='watch')
        self.main.update()

        # set the name
        if self.pipeline_type == xlib.get_toa_process_pipeline_nucleotide_code():
            self.name = xlib.get_toa_process_pipeline_nucleotide_name()
        elif self.pipeline_type == xlib.get_toa_process_pipeline_aminoacid_code():
            self.name = xlib.get_toa_process_pipeline_aminoacid_name()

        # assign the text of the "head"
        self.head = '{0} - Restart process'.format(self.name)

        # create the wrappers to track changes in the inputs
        self.wrapper_experiment_id = tkinter.StringVar()
        self.wrapper_experiment_id.trace('w', self.check_inputs)
        self.wrapper_pipeline_dataset = tkinter.StringVar()
        self.wrapper_pipeline_dataset.trace('w', self.check_inputs)

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
        Build the graphical user interface of "FormRestartPipelineProcess".
        '''

        # assign the text to the label of the current process name
        self.main.label_process['text'] = self.head

        # create "label_experiment_id" and register it with the grid geometry manager
        self.label_experiment_id = tkinter.Label(self, text='Experiment/process')
        self.label_experiment_id.grid(row=0, column=0, padx=(15,5), pady=(75,5), sticky='e')

        # create "combobox_experiment_id" and register it with the grid geometry manager
        self.combobox_experiment_id = tkinter.ttk.Combobox(self, width=30, height=4, state='readonly', textvariable=self.wrapper_experiment_id)
        self.combobox_experiment_id.grid(row=0, column=1, padx=(5,5), pady=(75,5), sticky='w')

        # create "label_pipeline_dataset" and register it with the grid geometry manager
        self.label_pipeline_dataset = tkinter.Label(self, text='Pipeline dataset')
        self.label_pipeline_dataset.grid(row=1, column=0, padx=(15,5), pady=(45,5), sticky='e')

        # create "combobox_pipeline_dataset" and register it with the grid geometry manager
        self.combobox_pipeline_dataset = tkinter.ttk.Combobox(self, width=45, height=4, state='readonly', textvariable=self.wrapper_pipeline_dataset)
        self.combobox_pipeline_dataset.grid(row=1, column=1, padx=(5,5), pady=(45,5), sticky='w')

        # create "label_fit" and register it with the grid geometry manager
        self.label_fit = tkinter.Label(self, text=' '*(35+xlib.get_os_size_fix()))
        self.label_fit.grid(row=2, column=2, padx=(0,0), pady=(45,5), sticky='e')

        # create "button_execute" and register it with the grid geometry manager
        self.button_execute = tkinter.ttk.Button(self, text='Execute', command=self.execute, state='disabled')
        self.button_execute.grid(row=2, column=3, padx=(5,5), pady=(45,5), sticky='e')

        # create "button_close" and register it with the grid geometry manager
        self.button_close = tkinter.ttk.Button(self, text='Close', command=self.close)
        self.button_close.grid(row=2, column=4, padx=(5,5), pady=(45,5), sticky='w')

        # link a handler to events
        self.combobox_experiment_id.bind('<<ComboboxSelected>>', self.combobox_experiment_id_selected_item)
        self.combobox_pipeline_dataset.bind('<<ComboboxSelected>>', self.combobox_pipeline_dataset_selected_item)

    #---------------

    def initialize_inputs(self):
        '''
        Load initial data in inputs.
        '''

        # load initial data in inputs
        self.combobox_experiment_id['values'] = []
        self.wrapper_experiment_id.set('')
        self.combobox_pipeline_dataset['values'] = []
        self.wrapper_pipeline_dataset.set('')

        # populate data in comboboxes
        self.populate_combobox_experiment_id()

    #---------------

    def populate_combobox_experiment_id(self):
        '''
        Populate data in "combobox_experiment_id".
        '''

        # clear the value selected in the combobox
        self.wrapper_experiment_id.set('')

        # initialize the experiment identification list
        experiment_id_list = [xlib.get_toa_result_pipeline_dir()]

        # load the experiment identifications in the combobox
        self.combobox_experiment_id['values'] = sorted(experiment_id_list)

    #---------------

    def populate_combobox_pipeline_dataset(self):
        '''
        Populate data in "combobox_pipeline_dataset".
        '''

        # clear the value selected in the combobox
        self.wrapper_pipeline_dataset.set('')

        # get the dictionary of TOA configuration.
        toa_config_dict = xtoa.get_toa_config_dict()

        # initialize the pipeline dataset name list
        pipeline_dataset_name_list = []

        # get the result dataset identifications of the experiment
        experiment_dir = '{0}/{1}'.format(toa_config_dict['RESULT_DIR'], xlib.get_toa_result_pipeline_dir())
        subdir_list = [subdir for subdir in os.listdir(experiment_dir) if os.path.isdir(os.path.join(experiment_dir, subdir))]
        for subdir in subdir_list:
            if subdir.startswith(self.pipeline_type):
                pipeline_dataset_name_list.append(subdir)

        # load the pipeline dataset names in the combobox
        self.combobox_pipeline_dataset['values'] = sorted(pipeline_dataset_name_list)

    #---------------

    def combobox_experiment_id_selected_item(self, event=None):
        '''
        Process the event when an item of "combobox_experiment_id" has been selected
        '''

        # set cursor to show busy status
        self.main.config(cursor='watch')
        self.main.update()

        # load data in "combobox_pipeline_dataset"
        self.populate_combobox_pipeline_dataset()

        # set cursor to show normal status
        self.main.config(cursor='')
        self.main.update()

    #---------------

    def combobox_pipeline_dataset_selected_item(self, event=None):
        '''
        Process the event when an item of "combobox_pipeline_dataset" has been selected
        '''

        pass

    #---------------

    def check_inputs(self, *args):
        '''
        Check the content of each input of "FormRestartPipelineProcess" and do the actions linked to its value
        '''

        # initialize the control variable
        OK = True

        # check if "button_execute" has to be enabled or disabled
        if self.wrapper_experiment_id.get() != ''  and self.wrapper_pipeline_dataset.get() != '':
            self.button_execute['state'] = 'enable'
        else:
            self.button_execute['state'] = 'disabled'

        # return the control variable
        return OK

    #---------------

    def execute(self):
        '''
        Run TOA process.
        '''

        # check inputs
        OK = self.check_inputs()
        if not OK:
            message = 'Some input values are not OK.'
            tkinter.messagebox.showerror('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # confirm the process run
        if OK:
            message = 'The {0} process is going to be run.\n\nAre you sure to continue?'.format(self.name)
            OK = tkinter.messagebox.askyesno('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # execute the process
        if OK:

            dialog_log = gdialogs.DialogLog(self, self.head, xtoa.restart_pipeline_process.__name__)
            threading.Thread(target=self.wait_window, args=(dialog_log,)).start()
            threading.Thread(target=xtoa.restart_pipeline_process, args=(self.pipeline_type, self.wrapper_pipeline_dataset.get(), dialog_log, lambda: dialog_log.enable_button_close())).start()

        # close the form
        if OK:
            self.close()

    #---------------

    def close(self):
        '''
        Close "FormRestartPipelineProcess".
        '''

        # clear the label of the current process name
        self.main.label_process['text'] = ''

        # close the current form
        self.main.close_current_form()

    #---------------

#-------------------------------------------------------------------------------

class FormViewStats(tkinter.Frame):

    #---------------

    def __init__(self, parent, main, stats_code):
        '''
        Execute actions correspending to the creation of a "FormViewStats" instance.
        '''

        # save initial parameters in instance variables
        self.parent = parent
        self.main = main
        self.stats_code = stats_code

        # call the init method of the parent class
        tkinter.Frame.__init__(self, self.parent)

        # set cursor to show busy status
        self.main.config(cursor='watch')
        self.main.update()

        # assign the text of the "name"
        if self.stats_code == 'hit_per_hsp':
            self.name = 'Alignment - # HITs per # HSPs'
        elif self.stats_code == 'dataset':
            self.name = 'Annotation datasets - Frequency distribution'
        elif self.stats_code == 'species':
            self.name = 'Species - Frequency distribution'
        elif self.stats_code == 'family':
            self.name = 'Family - Frequency distribution'
        elif self.stats_code == 'phylum':
            self.name = 'Phylum - Frequency distribution'
        elif self.stats_code == 'go':
            self.name = 'Gene Ontology - Frequency distribution per term'
        elif self.stats_code == 'namespace':
            self.name = 'Gene Ontology - Frequency distribution per namespace'
        elif self.stats_code == 'seq_per_go':
            self.name = 'Gene Ontology - # sequences per # terms'
        elif self.stats_code == 'ec':
            self.name = 'EC - Frequency distribution'
        elif self.stats_code == 'seq_per_ec':
            self.name = 'EC - # sequences per # ids'
        elif self.stats_code == 'interpro':
            self.name = 'InterPro - Frequency distribution'
        elif self.stats_code == 'seq_per_interpro':
            self.name = 'InterPro - # sequences per # ids'
        elif self.stats_code == 'kegg':
            self.name = 'KEGG - Frequency distribution'
        elif self.stats_code == 'seq_per_kegg':
            self.name = 'KEGG - # sequences per # ids'
        elif self.stats_code == 'mapman':
            self.name = 'MapMan - Frequency distribution'
        elif self.stats_code == 'seq_per_mapman':
            self.name = 'MapMan - # sequences per # ids'
        elif self.stats_code == 'metacyc':
            self.name = 'MetaCyc - Frequency distribution'
        elif self.stats_code == 'seq_per_metacyc':
            self.name = 'MetaCyc - # sequences per # ids'

        # assign the text of the "head"
        self.head = 'Statistics - {0} data'.format(self.name)

        # create the wrappers to track changes in the inputs
        self.wrapper_experiment_id = tkinter.StringVar()
        self.wrapper_experiment_id.trace('w', self.check_inputs)
        self.wrapper_pipeline_dataset = tkinter.StringVar()
        self.wrapper_pipeline_dataset.trace('w', self.check_inputs)

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
        Build the graphical user interface of "FormViewStats".
        '''

        # assign the text to the label of the current process name
        self.main.label_process['text'] = self.head

        # create "label_experiment_id" and register it with the grid geometry manager
        self.label_experiment_id = tkinter.Label(self, text='Experiment/process')
        self.label_experiment_id.grid(row=0, column=0, padx=(15,5), pady=(75,5), sticky='e')

        # create "combobox_experiment_id" and register it with the grid geometry manager
        self.combobox_experiment_id = tkinter.ttk.Combobox(self, width=30, height=4, state='readonly', textvariable=self.wrapper_experiment_id)
        self.combobox_experiment_id.grid(row=0, column=1, padx=(5,5), pady=(75,5), sticky='w')

        # create "label_pipeline_dataset" and register it with the grid geometry manager
        self.label_pipeline_dataset = tkinter.Label(self, text='Pipeline dataset')
        self.label_pipeline_dataset.grid(row=1, column=0, padx=(15,5), pady=(45,5), sticky='e')

        # create "combobox_pipeline_dataset" and register it with the grid geometry manager
        self.combobox_pipeline_dataset = tkinter.ttk.Combobox(self, width=45, height=4, state='readonly', textvariable=self.wrapper_pipeline_dataset)
        self.combobox_pipeline_dataset.grid(row=1, column=1, padx=(5,5), pady=(45,5), sticky='w')

        # create "label_fit" and register it with the grid geometry manager
        self.label_fit = tkinter.Label(self, text=' '*(35+xlib.get_os_size_fix()))
        self.label_fit.grid(row=2, column=2, padx=(0,0), pady=(45,5), sticky='e')

        # create "button_execute" and register it with the grid geometry manager
        self.button_execute = tkinter.ttk.Button(self, text='Execute', command=self.execute, state='disabled')
        self.button_execute.grid(row=2, column=3, padx=(5,5), pady=(45,5), sticky='e')

        # create "button_close" and register it with the grid geometry manager
        self.button_close = tkinter.ttk.Button(self, text='Close', command=self.close)
        self.button_close.grid(row=2, column=4, padx=(5,5), pady=(45,5), sticky='w')

        # link a handler to events
        self.combobox_experiment_id.bind('<<ComboboxSelected>>', self.combobox_experiment_id_selected_item)
        self.combobox_pipeline_dataset.bind('<<ComboboxSelected>>', self.combobox_pipeline_dataset_selected_item)

    #---------------

    def initialize_inputs(self):
        '''
        Load initial data in inputs.
        '''

        # load initial data in inputs
        self.combobox_experiment_id['values'] = []
        self.wrapper_experiment_id.set('')
        self.combobox_pipeline_dataset['values'] = []
        self.wrapper_pipeline_dataset.set('')

        # populate data in comboboxes
        self.populate_combobox_experiment_id()

    #---------------

    def populate_combobox_experiment_id(self):
        '''
        Populate data in "combobox_experiment_id".
        '''

        # clear the value selected in the combobox
        self.wrapper_experiment_id.set('')

        # initialize the experiment identification list
        experiment_id_list = [xlib.get_toa_result_pipeline_dir()]

        # load the experiment identifications in the combobox
        self.combobox_experiment_id['values'] = sorted(experiment_id_list)

    #---------------

    def populate_combobox_pipeline_dataset(self):
        '''
        Populate data in "combobox_pipeline_dataset".
        '''

        # clear the value selected in the combobox
        self.wrapper_pipeline_dataset.set('')

        # get the dictionary of TOA configuration.
        toa_config_dict = xtoa.get_toa_config_dict()

        # initialize the pipeline dataset name list
        pipeline_dataset_name_list = []

        # get the result dataset identifications of the experiment
        experiment_dir = '{0}/{1}'.format(toa_config_dict['RESULT_DIR'], xlib.get_toa_result_pipeline_dir())
        subdir_list = [subdir for subdir in os.listdir(experiment_dir) if os.path.isdir(os.path.join(experiment_dir, subdir))]
        for subdir in subdir_list:
            pipeline_dataset_name_list.append(subdir)

        # load the pipeline dataset names in the combobox
        self.combobox_pipeline_dataset['values'] = sorted(pipeline_dataset_name_list)

    #---------------

    def combobox_experiment_id_selected_item(self, event=None):
        '''
        Process the event when an item of "combobox_experiment_id" has been selected
        '''

        # set cursor to show busy status
        self.main.config(cursor='watch')
        self.main.update()

        # load data in "combobox_pipeline_dataset"
        self.populate_combobox_pipeline_dataset()

        # set cursor to show normal status
        self.main.config(cursor='')
        self.main.update()

    #---------------

    def combobox_pipeline_dataset_selected_item(self, event=None):
        '''
        Process the event when an item of "combobox_pipeline_dataset" has been selected
        '''

        pass

    #---------------

    def check_inputs(self, *args):
        '''
        Check the content of each input of "FormViewStats" and do the actions linked to its value
        '''

        # initialize the control variable
        OK = True

        # check if "button_execute" has to be enabled or disabled
        if self.wrapper_experiment_id.get() != ''  and self.wrapper_pipeline_dataset.get() != '':
            self.button_execute['state'] = 'enable'
        else:
            self.button_execute['state'] = 'disabled'

        # return the control variable
        return OK

    #---------------

    def execute(self):
        '''
        Run TOA process.
        '''

        # check inputs
        OK = self.check_inputs()
        if not OK:
            message = 'Some input values are not OK.'
            tkinter.messagebox.showerror('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # execute the corresponding process
        if OK:
            if self.stats_code in ['hit_per_hsp', 'seq_per_go', 'seq_per_ec', 'seq_per_interpro', 'seq_per_kegg', 'seq_per_mapman', 'seq_per_metacyc']:
                self.execute_x_per_y_data()
            elif self.stats_code == 'dataset':
                self.execute_dataset_data_frecuency()
            elif self.stats_code in ['namespace', 'species', 'family', 'phylum']:
                self.execute_phylogenic_data_frecuency()
            elif self.stats_code in ['interpro', 'mapman', 'ec', 'kegg', 'metacyc']:
                self.execute_ontologic_data_frecuency()
            elif self.stats_code == 'go':
                self.execute_go_data_frecuency()

        # close the form
        if OK:
            self.close()

    #---------------

    def execute_x_per_y_data(self):
        '''
        Run TOA process to write x per y data.
        '''

        # initialize the control variable
        OK = True

        # initialize the distribution dictionary
        distribution_dict = {}

        # get the dictionary of TOA configuration
        toa_config_dict = xtoa.get_toa_config_dict()

        # get the statistics file path
        stats_file = '{0}/{1}/{2}/{3}/{4}-{5}.csv'.format(toa_config_dict['RESULT_DIR'], self.wrapper_experiment_id.get(), self.combobox_pipeline_dataset.get(), toa_config_dict['STATS_SUBDIR_NAME'], self.stats_code, toa_config_dict['STATS_BASE_NAME'])

        # open the statistics file
        if stats_file.endswith('.gz'):
            try:
                stats_file_id = gzip.open(stats_file, mode='rt', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F002', stats_file)
        else:
            try:
                stats_file_id = open(stats_file, mode='r', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F001', stats_file)

        # initialize the record counter
        record_counter = 0

        # initialize the header record control
        header_record = True

        # read the first record
        record = stats_file_id.readline()

        # while there are records
        while record != '':

            # add 1 to the record counter
            record_counter += 1

            # process the header record
            if header_record:
                header_record = False

            # process data records
            else:

                # extract data
                # record format: "x_count";"y_count"
                data_list = []
                begin = 0
                for end in [i for i, chr in enumerate(record) if chr == ';']:
                    data_list.append(record[begin:end].strip('"'))
                    begin = end + 1
                data_list.append(record[begin:].strip('\n').strip('"'))
                try:
                    x_count = data_list[0]
                    y_count = data_list[1]
                except Exception as e:
                    raise xlib.ProgramException('F006', os.path.basename(stats_file), record_counter)

                # add dato to the dictionary
                distribution_dict[record_counter] = {'x_count': x_count, 'y_count': y_count}

            # read the next record
            record = stats_file_id.readline()

        # check if there are any stats
        if distribution_dict == {}:
            message = 'There is not any stats data.'
            tkinter.messagebox.showwarning('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)
            OK = False

        # build the data list
        if OK:
            data_list = ['x_count', 'y_count']

        # build the data dictionary
        if OK:
            data_dict = {}
            if self.stats_code == 'hit_per_hsp':
                data_dict['x_count'] = {'text': '# HSPs', 'width': 150, 'alignment': 'right'}
                data_dict['y_count'] = {'text': '# HITs', 'width': 150, 'alignment': 'right'}
            elif self.stats_code == 'seq_per_go':
                data_dict['x_count'] = {'text': '# GO terms', 'width': 150, 'alignment': 'right'}
                data_dict['y_count'] = {'text': '# sequences', 'width': 150, 'alignment': 'right'}
            elif self.stats_code == 'seq_per_ec':
                data_dict['x_count'] = {'text': '# EC ids', 'width': 150, 'alignment': 'right'}
                data_dict['y_count'] = {'text': '# sequences', 'width': 150, 'alignment': 'right'}
            elif self.stats_code == 'seq_per_interpro':
                data_dict['x_count'] = {'text': '# InterPro ids', 'width': 150, 'alignment': 'right'}
                data_dict['y_count'] = {'text': '# sequences', 'width': 150, 'alignment': 'right'}
            elif self.stats_code == 'seq_per_kegg':
                data_dict['x_count'] = {'text': '# KEGG ids', 'width': 150, 'alignment': 'right'}
                data_dict['y_count'] = {'text': '# sequences', 'width': 150, 'alignment': 'right'}
            elif self.stats_code == 'seq_per_mapman':
                data_dict['x_count'] = {'text': '# MapMan ids', 'width': 150, 'alignment': 'right'}
                data_dict['y_count'] = {'text': '# sequences', 'width': 150, 'alignment': 'right'}
            elif self.stats_code == 'seq_per_metacyc':
                data_dict['x_count'] = {'text': '# MetaCyc ids', 'width': 150, 'alignment': 'right'}
                data_dict['y_count'] = {'text': '# sequences', 'width': 150, 'alignment': 'right'}

        # create the dialog Table to list the submission process logs
        if OK:
            dialog_table = gdialogs.DialogTable(self, self.name, 400, 320, data_list, data_dict, distribution_dict, sorted(distribution_dict.keys()), 'view_distribution')
            self.wait_window(dialog_table)

    #---------------

    def execute_dataset_data_frecuency(self):
        '''
        Run TOA process to write dataset data frecuency.
        '''

        # initialize the control variable
        OK = True

        # initialize the distribution dictionary
        distribution_dict = {}

        # get the dictionary of TOA configuration
        toa_config_dict = xtoa.get_toa_config_dict()

        # get the statistics file path
        stats_file = '{0}/{1}/{2}/{3}/{4}-{5}.csv'.format(toa_config_dict['RESULT_DIR'], self.wrapper_experiment_id.get(), self.combobox_pipeline_dataset.get(), toa_config_dict['STATS_SUBDIR_NAME'], self.stats_code, toa_config_dict['STATS_BASE_NAME'])

        # open the statistics file
        if stats_file.endswith('.gz'):
            try:
                stats_file_id = gzip.open(stats_file, mode='rt', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F002', stats_file)
        else:
            try:
                stats_file_id = open(stats_file, mode='r', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F001', stats_file)

        # initialize the record counter
        record_counter = 0

        # initialize the header record control
        header_record = True

        # read the first record
        record = stats_file_id.readline()

        # while there are records
        while record != '':

            # add 1 to the record counter
            record_counter += 1

            # process the header record
            if header_record:
                header_record = False

            # process data records
            else:

                # extract data
                # record format: "dataset_name";"annotated_seq_count";"remained_seq_count"
                data_list = []
                begin = 0
                for end in [i for i, chr in enumerate(record) if chr == ';']:
                    data_list.append(record[begin:end].strip('"'))
                    begin = end + 1
                data_list.append(record[begin:].strip('\n').strip('"'))
                try:
                    dataset_name = data_list[0]
                    annotated_seq_count = data_list[1]
                    remained_seq_count = data_list[2]
                except Exception as e:
                    raise xlib.ProgramException('F006', os.path.basename(stats_file), record_counter)

                # add dato to the dictionary
                distribution_dict[record_counter] = {'dataset_name': dataset_name, 'annotated_seq_count': annotated_seq_count, 'remained_seq_count': remained_seq_count}

            # read the next record
            record = stats_file_id.readline()

        # check if there are any stats
        if distribution_dict == {}:
            message = 'There is not any stats data.'
            tkinter.messagebox.showwarning('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)
            OK = False

        # build the data list
        if OK:
            data_list = ['dataset_name', 'annotated_seq_count', 'remained_seq_count']

        # build the data dictionary
        if OK:
            data_dict = {}
            data_dict['dataset_name'] = {'text': self.stats_code.capitalize(), 'width': 200, 'alignment': 'left'}
            data_dict['annotated_seq_count'] = {'text': 'Annotated seqs', 'width': 150, 'alignment': 'right'}
            data_dict['remained_seq_count'] = {'text': 'Remained seqs', 'width': 150, 'alignment': 'right'}

        # create the dialog Table to list the submission process logs
        if OK:
            dialog_table = gdialogs.DialogTable(self, self.name, 400, 520, data_list, data_dict, distribution_dict, sorted(distribution_dict.keys()), 'view_distribution')
            self.wait_window(dialog_table)

    #---------------

    def execute_phylogenic_data_frecuency(self):
        '''
        Run TOA process to write phylogenic data frecuency.
        '''

        # initialize the control variable
        OK = True

        # initialize the distribution dictionary
        distribution_dict = {}

        # get the dictionary of TOA configuration
        toa_config_dict = xtoa.get_toa_config_dict()

        # get the statistics file path
        stats_file = '{0}/{1}/{2}/{3}/{4}-{5}.csv'.format(toa_config_dict['RESULT_DIR'], self.wrapper_experiment_id.get(), self.combobox_pipeline_dataset.get(), toa_config_dict['STATS_SUBDIR_NAME'], self.stats_code, toa_config_dict['STATS_BASE_NAME'])

        # open the statistics file
        if stats_file.endswith('.gz'):
            try:
                stats_file_id = gzip.open(stats_file, mode='rt', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F002', stats_file)
        else:
            try:
                stats_file_id = open(stats_file, mode='r', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F001', stats_file)

        # initialize the record counter
        record_counter = 0

        # initialize the header record control
        header_record = True

        # read the first record
        record = stats_file_id.readline()

        # while there are records
        while record != '':

            # add 1 to the record counter
            record_counter += 1

            # process the header record
            if header_record:
                header_record = False

            # process data records
            else:

                # extract data
                # record format: "stats_code_id";"all_count";"first_hsp_count";"min_evalue_count"
                data_list = []
                begin = 0
                for end in [i for i, chr in enumerate(record) if chr == ';']:
                    data_list.append(record[begin:end].strip('"'))
                    begin = end + 1
                data_list.append(record[begin:].strip('\n').strip('"'))
                try:
                    id = data_list[0]
                    all_count = data_list[1]
                    first_hsp_count = data_list[2]
                    min_evalue_count = data_list[3]
                except Exception as e:
                    raise xlib.ProgramException('F006', os.path.basename(stats_file), record_counter)

                # add dato to the dictionary
                distribution_dict[id] = {'id': id, 'all_count': all_count, 'first_hsp_count': first_hsp_count, 'min_evalue_count': min_evalue_count}

            # read the next record
            record = stats_file_id.readline()

        # check if there are any stats
        if distribution_dict == {}:
            message = 'There is not any stats data.'
            tkinter.messagebox.showwarning('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)
            OK = False

        # build the data list
        if OK:
            data_list = ['id', 'all_count', 'first_hsp_count', 'min_evalue_count']

        # build the data dictionary
        if OK:
            data_dict = {}
            data_dict['id'] = {'text': self.stats_code.capitalize(), 'width': 400, 'alignment': 'left'}
            data_dict['all_count'] = {'text': 'All count', 'width': 160, 'alignment': 'right'}
            data_dict['first_hsp_count'] = {'text': 'First HSP count', 'width': 160, 'alignment': 'right'}
            data_dict['min_evalue_count'] = {'text': 'Min e-value count', 'width': 160, 'alignment': 'right'}

        # create the dialog Table to list the submission process logs
        if OK:
            dialog_table = gdialogs.DialogTable(self, self.name, 400, 900, data_list, data_dict, distribution_dict, sorted(distribution_dict.keys()), 'view_distribution')
            self.wait_window(dialog_table)

    #---------------

    def execute_ontologic_data_frecuency(self):
        '''
        Run TOA process to write ontologic data frecuency.
        '''

        # initialize the control variable
        OK = True

        # initialize the distribution dictionary
        distribution_dict = {}

        # get the dictionary of TOA configuration
        toa_config_dict = xtoa.get_toa_config_dict()

        # get the statistics file path
        stats_file = '{0}/{1}/{2}/{3}/{4}-{5}.csv'.format(toa_config_dict['RESULT_DIR'], self.wrapper_experiment_id.get(), self.combobox_pipeline_dataset.get(), toa_config_dict['STATS_SUBDIR_NAME'], self.stats_code, toa_config_dict['STATS_BASE_NAME'])

        # open the statistics file
        if stats_file.endswith('.gz'):
            try:
                stats_file_id = gzip.open(stats_file, mode='rt', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F002', stats_file)
        else:
            try:
                stats_file_id = open(stats_file, mode='r', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F001', stats_file)

        # initialize the record counter
        record_counter = 0

        # initialize the header record control
        header_record = True

        # read the first record
        record = stats_file_id.readline()

        # while there are records
        while record != '':

            # add 1 to the record counter
            record_counter += 1

            # process the header record
            if header_record:
                header_record = False

            # process data records
            else:

                # extract data
                # record format: "stats_code_id";"description";"all_count";"first_hsp_count";"min_evalue_count"
                data_list = []
                begin = 0
                for end in [i for i, chr in enumerate(record) if chr == ';']:
                    data_list.append(record[begin:end].strip('"'))
                    begin = end + 1
                data_list.append(record[begin:].strip('\n').strip('"'))
                try:
                    id = data_list[0]
                    desc = data_list[1]
                    all_count = data_list[2]
                    first_hsp_count = data_list[3]
                    min_evalue_count = data_list[4]
                except Exception as e:
                    raise xlib.ProgramException('F006', os.path.basename(stats_file), record_counter)

                # add dato to the dictionary
                distribution_dict[id] = {'id': id, 'desc': desc, 'all_count': all_count, 'first_hsp_count': first_hsp_count, 'min_evalue_count': min_evalue_count}

            # read the next record
            record = stats_file_id.readline()

        # check if there are any stats
        if distribution_dict == {}:
            message = 'There is not any stats data.'
            tkinter.messagebox.showwarning('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)
            OK = False

        # build the data list
        if OK:
            data_list = ['id', 'desc', 'all_count', 'first_hsp_count', 'min_evalue_count']

        # build the data dictionary
        if OK:
            data_dict = {}
            data_dict['id'] = {'text': '{0} id'.format(self.stats_code.capitalize()), 'width': 250, 'alignment': 'left'}
            data_dict['desc'] = {'text': 'Description', 'width': 400, 'alignment': 'left'}
            data_dict['all_count'] = {'text': 'All count', 'width': 135, 'alignment': 'right'}
            data_dict['first_hsp_count'] = {'text': 'First HSP count', 'width': 135, 'alignment': 'right'}
            data_dict['min_evalue_count'] = {'text': 'Min e-value count', 'width': 140, 'alignment': 'right'}

        # create the dialog Table to list the submission process logs
        if OK:
            dialog_table = gdialogs.DialogTable(self, self.name, 400, 1090, data_list, data_dict, distribution_dict, sorted(distribution_dict.keys()), 'view_distribution')
            self.wait_window(dialog_table)

    #---------------

    def execute_go_data_frecuency(self):
        '''
        Run TOA process to write Gene Ontology data frecuency.
        '''

        # initialize the control variable
        OK = True

        # initialize the distribution dictionary
        distribution_dict = {}

        # get the dictionary of TOA configuration
        toa_config_dict = xtoa.get_toa_config_dict()

        # get the statistics file path
        stats_file = '{0}/{1}/{2}/{3}/{4}-{5}.csv'.format(toa_config_dict['RESULT_DIR'], self.wrapper_experiment_id.get(), self.combobox_pipeline_dataset.get(), toa_config_dict['STATS_SUBDIR_NAME'], self.stats_code, toa_config_dict['STATS_BASE_NAME'])

        # open the statistics file
        if stats_file.endswith('.gz'):
            try:
                stats_file_id = gzip.open(stats_file, mode='rt', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F002', stats_file)
        else:
            try:
                stats_file_id = open(stats_file, mode='r', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F001', stats_file)

        # initialize the record counter
        record_counter = 0

        # initialize the header record control
        header_record = True

        # read the first record
        record = stats_file_id.readline()

        # while there are records
        while record != '':

            # add 1 to the record counter
            record_counter += 1

            # process the header record
            if header_record:
                header_record = False

            # process data records
            else:

                # extract data
                # record format: "go_term";"description";"namespace";"all_count";"first_hsp_count";"min_evalue_count"
                data_list = []
                begin = 0
                for end in [i for i, chr in enumerate(record) if chr == ';']:
                    data_list.append(record[begin:end].strip('"'))
                    begin = end + 1
                data_list.append(record[begin:].strip('\n').strip('"'))
                try:
                    id = data_list[0]
                    desc = data_list[1]
                    namespace = data_list[2]
                    all_count = data_list[3]
                    first_hsp_count = data_list[4]
                    min_evalue_count = data_list[5]
                except Exception as e:
                    raise xlib.ProgramException('F006', os.path.basename(stats_file), record_counter)

                # add dato to the dictionary
                distribution_dict[id] = {'id': id, 'desc': desc, 'namespace': namespace, 'all_count': all_count, 'first_hsp_count': first_hsp_count, 'min_evalue_count': min_evalue_count}

            # read the next record
            record = stats_file_id.readline()

        # check if there are any stats
        if distribution_dict == {}:
            message = 'There is not any stats data.'
            tkinter.messagebox.showwarning('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)
            OK = False

        # build the data list
        if OK:
            data_list = ['id', 'desc', 'namespace', 'all_count', 'first_hsp_count', 'min_evalue_count']

        # build the data dictionary
        if OK:
            data_dict = {}
            data_dict['id'] = {'text': 'GO term', 'width': 140, 'alignment': 'left'}
            data_dict['desc'] = {'text': 'Description', 'width': 400, 'alignment': 'left'}
            data_dict['namespace'] = {'text': 'Namespace', 'width': 145, 'alignment': 'left'}
            data_dict['all_count'] = {'text': 'All count', 'width': 135, 'alignment': 'right'}
            data_dict['first_hsp_count'] = {'text': 'First HSP count', 'width': 135, 'alignment': 'right'}
            data_dict['min_evalue_count'] = {'text': 'Min e-value count', 'width': 140, 'alignment': 'right'}

        # create the dialog Table to list the submission process logs
        if OK:
            dialog_table = gdialogs.DialogTable(self, self.name, 400, 1120, data_list, data_dict, distribution_dict, sorted(distribution_dict.keys()), 'view_distribution')
            self.wait_window(dialog_table)

    #---------------

    def close(self):
        '''
        Close "FormViewStats".
        '''

        # clear the label of the current process name
        self.main.label_process['text'] = ''

        # close the current form
        self.main.close_current_form()

    #---------------

#-------------------------------------------------------------------------------

class FormPlotStats(tkinter.Frame):

    #---------------

    def __init__(self, parent, main, stats_code):
        '''
        Execute actions correspending to the creation of a "FormPlotStats" instance.
        '''

        # save initial parameters in instance variables
        self.parent = parent
        self.main = main
        self.stats_code = stats_code

        # call the init method of the parent class
        tkinter.Frame.__init__(self, self.parent)

        # set cursor to show busy status
        self.main.config(cursor='watch')
        self.main.update()

        # get the dictionary of TOA configuration
        self.toa_config_dict = xtoa.get_toa_config_dict()

        # assign the text of the "name"
        if self.stats_code == 'hit_per_hsp':
            self.name = 'Alignment - # HITs per # HSPs'
        elif self.stats_code == 'dataset':
            self.name = 'Annotation datasets - Frequency distribution'
        elif self.stats_code == 'species':
            self.name = 'Species - Frequency distribution'
        elif self.stats_code == 'family':
            self.name = 'Family - Frequency distribution'
        elif self.stats_code == 'phylum':
            self.name = 'Phylum - Frequency distribution'
        elif self.stats_code == 'go':
            self.name = 'Gene Ontology - Frequency distribution per term'
        elif self.stats_code == 'namespace':
            self.name = 'Gene Ontology - Frequency distribution per namespace'
        elif self.stats_code == 'seq_per_go':
            self.name = 'Gene Ontology - # sequences per # terms'
        elif self.stats_code == 'ec':
            self.name = 'EC - Frequency distribution'
        elif self.stats_code == 'seq_per_ec':
            self.name = 'EC - # sequences per # ids'
        elif self.stats_code == 'interpro':
            self.name = 'InterPro - Frequency distribution'
        elif self.stats_code == 'seq_per_interpro':
            self.name = 'InterPro - # sequences per # ids'
        elif self.stats_code == 'kegg':
            self.name = 'KEGG - Frequency distribution'
        elif self.stats_code == 'seq_per_kegg':
            self.name = 'KEGG - # sequences per # ids'
        elif self.stats_code == 'mapman':
            self.name = 'MapMan - Frequency distribution'
        elif self.stats_code == 'seq_per_mapman':
            self.name = 'MapMan - # sequences per # ids'
        elif self.stats_code == 'metacyc':
            self.name = 'MetaCyc - Frequency distribution'
        elif self.stats_code == 'seq_per_metacyc':
            self.name = 'MetaCyc - # sequences per # ids'

        # assign the text of the "head"
        self.head = 'Statistics - {0} plot'.format(self.name)

        # create the wrappers to track changes in the inputs
        self.wrapper_experiment_id = tkinter.StringVar()
        self.wrapper_experiment_id.trace('w', self.check_inputs)
        self.wrapper_pipeline_dataset = tkinter.StringVar()
        self.wrapper_pipeline_dataset.trace('w', self.check_inputs)
        if self.stats_code == 'go':
            self.wrapper_namespace = tkinter.StringVar()
            self.wrapper_namespace.trace('w', self.check_inputs)
        if self.stats_code in ['species', 'family', 'phylum', 'go', 'namespace', 'ec', 'interpro', 'kegg', 'mapman', 'metacyc']:
            self.wrapper_alignment_count_level = tkinter.StringVar()
            self.wrapper_alignment_count_level.trace('w', self.check_inputs)
        self.wrapper_image_format = tkinter.StringVar()
        self.wrapper_image_format.trace('w', self.check_inputs)
        self.wrapper_dpi = tkinter.StringVar()
        self.wrapper_dpi.trace('w', self.check_inputs)
        self.wrapper_image_dir = tkinter.StringVar()
        self.wrapper_image_dir.trace('w', self.check_inputs)
        self.wrapper_image_name = tkinter.StringVar()
        self.wrapper_image_name.trace('w', self.check_inputs)

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
        Build the graphical user interface of "FormPlotStats".
        '''

        # assign the text to the label of the current process name
        self.main.label_process['text'] = self.head

        # create "image_open_folder"
        image_open_folder = PIL.Image.open('./image_open_folder.png')
        imagetk_open_folder = PIL.ImageTk.PhotoImage(image_open_folder)  

        # create "label_experiment_id" and register it with the grid geometry manager
        self.label_experiment_id = tkinter.Label(self, text='Experiment / process')
        self.label_experiment_id.grid(row=0, column=0, padx=(15,5), pady=(50,5), sticky='e')

        # create "combobox_experiment_id" and register it with the grid geometry manager
        self.combobox_experiment_id = tkinter.ttk.Combobox(self, width=30, height=4, state='readonly', textvariable=self.wrapper_experiment_id)
        self.combobox_experiment_id.grid(row=0, column=1, padx=(5,5), pady=(50,5), sticky='w')

        # create "label_pipeline_dataset" and register it with the grid geometry manager
        self.label_pipeline_dataset = tkinter.Label(self, text='Pipeline dataset')
        self.label_pipeline_dataset.grid(row=1, column=0, padx=(15,5), pady=(25,5), sticky='e')

        # create "combobox_pipeline_dataset" and register it with the grid geometry manager
        self.combobox_pipeline_dataset = tkinter.ttk.Combobox(self, width=45, height=4, state='readonly', textvariable=self.wrapper_pipeline_dataset)
        self.combobox_pipeline_dataset.grid(row=1, column=1, padx=(5,5), pady=(25,5), sticky='w')

        # create "label_namespace" and register it with the grid geometry manager
        if self.stats_code == 'go':
            self.label_namespace = tkinter.Label(self, text='Namespace')
            self.label_namespace.grid(row=2, column=0, padx=(15,5), pady=(25,5), sticky='e')

        # create "combobox_namespace" and register it with the grid geometry manager
        if self.stats_code == 'go':
            self.combobox_namespace = tkinter.ttk.Combobox(self, width=30, height=4, state='readonly', textvariable=self.wrapper_namespace)
            self.combobox_namespace.grid(row=2, column=1, padx=(5,5), pady=(25,5), sticky='w')

        # create "label_alignment_count_level" and register it with the grid geometry manager
        if self.stats_code in ['species', 'family', 'phylum', 'go', 'namespace', 'ec', 'interpro', 'kegg', 'mapman', 'metacyc']:
            self.label_alignment_count_level = tkinter.Label(self, text='Alignment count level')
            self.label_alignment_count_level.grid(row=3, column=0, padx=(15,5), pady=(25,5), sticky='e')

        # create "combobox_alignment_count_level" and register it with the grid geometry manager
        if self.stats_code in ['species', 'family', 'phylum', 'go', 'namespace', 'ec', 'interpro', 'kegg', 'mapman', 'metacyc']:
            self.combobox_alignment_count_level = tkinter.ttk.Combobox(self, width=30, height=4, state='readonly', textvariable=self.wrapper_alignment_count_level)
            self.combobox_alignment_count_level.grid(row=3, column=1, padx=(5,5), pady=(25,5), sticky='w')

        # create "label_image_format" and register it with the grid geometry manager
        self.label_image_format = tkinter.Label(self, text='Image format')
        self.label_image_format.grid(row=4, column=0, padx=(15,5), pady=(25,5), sticky='e')

        # create "combobox_image_format" and register it with the grid geometry manager
        self.combobox_image_format = tkinter.ttk.Combobox(self, width=10, height=4, state='readonly', textvariable=self.wrapper_image_format)
        self.combobox_image_format.grid(row=4, column=1, padx=(5,5), pady=(25,5), sticky='w')

        # create "label_dpi" and register it with the grid geometry manager
        self.label_dpi = tkinter.Label(self, text='DPI')
        self.label_dpi.grid(row=5, column=0, padx=(15,5), pady=(25,0), sticky='e')

        # create "entry_dpi" and register it with the grid geometry manager
        self.entry_dpi = tkinter.Entry(self, textvariable=self.wrapper_dpi, width=10, validatecommand=self.check_inputs)
        self.entry_dpi.grid(row=5, column=1, padx=(5,5), pady=(25,0), sticky='w')

        # create "label_dpi_warning" and register it with the grid geometry manager
        self.label_dpi_warning = tkinter.Label(self, text='')
        self.label_dpi_warning.grid(row=6, column=1, columnspan=4, padx=(5,5), pady=(0,0), sticky='w')

        # create "label_image_dir" and register it with the grid geometry manager
        self.label_image_dir = tkinter.Label(self, text='Image dir')
        self.label_image_dir.grid(row=7, column=0, padx=(15,5), pady=(0,0), sticky='e')

        # create "entry_image_dir" and register it with the grid geometry manager
        self.entry_image_dir = tkinter.Entry(self, textvariable=self.wrapper_image_dir, width=58, state='disabled', validatecommand=self.check_inputs)
        self.entry_image_dir.grid(row=7, column=1, padx=(5,5), pady=(0,0), sticky='w')

        # create "button_select_dir" and register it with the grid geometry manager
        self.button_select_dir = tkinter.ttk.Button(self, image=imagetk_open_folder, command=self.select_dir)
        self.button_select_dir.image = imagetk_open_folder
        self.button_select_dir.grid(row=7, column=2, padx=(5,0), pady=(0,0), sticky='w')

        # create "label_image_name" and register it with the grid geometry manager
        self.label_image_name = tkinter.Label(self, text='Image name')
        self.label_image_name.grid(row=8, column=0, padx=(15,5), pady=(25,0), sticky='e')

        # create "entry_image_name" and register it with the grid geometry manager
        self.entry_image_name = tkinter.Entry(self, textvariable=self.wrapper_image_name, width=45, validatecommand=self.check_inputs)
        self.entry_image_name.grid(row=8, column=1, padx=(5,5), pady=(25,0), sticky='w')

        # create "label_image_name_warning" and register it with the grid geometry manager
        self.label_image_name_warning = tkinter.Label(self, text='')
        self.label_image_name_warning.grid(row=9, column=1, columnspan=4, padx=(5,5), pady=(0,0), sticky='w')

        # create "label_fit" and register it with the grid geometry manager
        self.label_fit = tkinter.Label(self, text=' '*(1+xlib.get_os_size_fix()))
        self.label_fit.grid(row=10, column=2, padx=(0,0), pady=(15,5), sticky='e')

        # create "button_execute" and register it with the grid geometry manager
        self.button_execute = tkinter.ttk.Button(self, text='Execute', command=self.execute, state='disabled')
        self.button_execute.grid(row=10, column=3, padx=(5,5), pady=(15,5), sticky='e')

        # create "button_close" and register it with the grid geometry manager
        self.button_close = tkinter.ttk.Button(self, text='Close', command=self.close)
        self.button_close.grid(row=10, column=4, padx=(5,5), pady=(15,5), sticky='w')

        # link a handler to events
        self.combobox_experiment_id.bind('<<ComboboxSelected>>', self.combobox_experiment_id_selected_item)
        self.combobox_pipeline_dataset.bind('<<ComboboxSelected>>', self.combobox_pipeline_dataset_selected_item)
        if self.stats_code == 'go':
            self.combobox_namespace.bind('<<ComboboxSelected>>', self.combobox_namespace_selected_item)
        if self.stats_code in ['species', 'family', 'phylum', 'go', 'namespace', 'ec', 'interpro', 'kegg', 'mapman', 'metacyc']:
            self.combobox_alignment_count_level.bind('<<ComboboxSelected>>', self.combobox_alignment_count_level_selected_item)
        self.combobox_image_format.bind('<<ComboboxSelected>>', self.combobox_image_format_selected_item)

    #---------------

    def initialize_inputs(self):
        '''
        Load initial data in inputs.
        '''

        # load initial data in inputs
        self.combobox_experiment_id['values'] = []
        self.wrapper_experiment_id.set('')
        self.combobox_pipeline_dataset['values'] = []
        self.wrapper_pipeline_dataset.set('')
        self.wrapper_dpi.set(600)
        default_image_dir = os.path.join(os.getcwd(), 'graphics')
        if not os.path.isdir(default_image_dir): os.mkdir(default_image_dir)
        self.wrapper_image_dir.set(default_image_dir)
        self.wrapper_image_name.set('Figure.jpeg')

        # populate data in comboboxes
        self.populate_combobox_experiment_id()
        if self.stats_code == 'go':
            self.populate_combobox_namespace()
        if self.stats_code in ['species', 'family', 'phylum', 'go', 'namespace', 'ec', 'interpro', 'kegg', 'mapman', 'metacyc']:
            self.populate_combobox_alignment_count_level()
        self.populate_combobox_image_format()

    #---------------

    def populate_combobox_experiment_id(self):
        '''
        Populate data in "combobox_experiment_id".
        '''

        # clear the value selected in the combobox
        self.wrapper_experiment_id.set('')

        # initialize the experiment identification list
        experiment_id_list = [xlib.get_toa_result_pipeline_dir()]

        # load the experiment identifications in the combobox
        self.combobox_experiment_id['values'] = sorted(experiment_id_list)

    #---------------

    def populate_combobox_pipeline_dataset(self):
        '''
        Populate data in "combobox_pipeline_dataset".
        '''

        # clear the value selected in the combobox
        self.wrapper_pipeline_dataset.set('')

        # initialize the pipeline dataset name list
        pipeline_dataset_name_list = []

        # get the result dataset identifications of the experiment
        experiment_dir = '{0}/{1}'.format(self.toa_config_dict['RESULT_DIR'], xlib.get_toa_result_pipeline_dir())
        subdir_list = [subdir for subdir in os.listdir(experiment_dir) if os.path.isdir(os.path.join(experiment_dir, subdir))]
        for subdir in subdir_list:
            pipeline_dataset_name_list.append(subdir)

        # load the pipeline dataset names in the combobox
        self.combobox_pipeline_dataset['values'] = sorted(pipeline_dataset_name_list)

    #---------------

    def populate_combobox_namespace(self):
        '''
        Populate data in "combobox_namespace".
        '''

        # clear the value selected in the combobox
        self.wrapper_namespace.set('all')

        # load the list of the read dataset names in the combobox
        self.combobox_namespace['values'] =['all', 'biological process', 'cellular component', 'molecular function']

    #---------------

    def populate_combobox_alignment_count_level(self):
        '''
        Populate data in "combobox_alignment_count_level".
        '''

        # clear the value selected in the combobox
        self.wrapper_alignment_count_level.set('minimum e-value count')

        # load the list of the read dataset names in the combobox
        self.combobox_alignment_count_level['values'] =['all count', 'first HSP count', 'minimum e-value count']

    #---------------

    def populate_combobox_image_format(self):
        '''
        Populate data in "combobox_image_format".
        '''

        # clear the value selected in the combobox
        self.wrapper_image_format.set('JPEG')

        # load the list of the read dataset names in the combobox
        self.combobox_image_format['values'] =['EPS', 'JPEG', 'PDF', 'PNG', 'PS', 'SVG', 'TIFF']

    #---------------

    def select_dir(self):
        '''
        Select a directory and assign it to "entry_local_dir".
        '''

        # select the directory
        directory = tkinter.filedialog.askdirectory(parent=self, initialdir=".", title='Please select the image directory')

        # assign the directory to "entry_local_dir"
        if directory != '':
            self.wrapper_image_dir.set(directory)

    #---------------

    def combobox_experiment_id_selected_item(self, event=None):
        '''
        Process the event when an item of "combobox_experiment_id" has been selected
        '''

        # set cursor to show busy status
        self.main.config(cursor='watch')
        self.main.update()

        # load data in "combobox_pipeline_dataset"
        self.populate_combobox_pipeline_dataset()

        # set cursor to show normal status
        self.main.config(cursor='')
        self.main.update()

    #---------------

    def combobox_pipeline_dataset_selected_item(self, event=None):
        '''
        Process the event when an item of "combobox_pipeline_dataset" has been selected
        '''

        pass

    #---------------

    def combobox_namespace_selected_item(self, event=None):
        '''
        Process the event when an item of "combobox_namespace" has been selected
        '''

        pass

    #---------------

    def combobox_alignment_count_level_selected_item(self, event=None):
        '''
        Process the event when an item of "combobox_alignment_count_level" has been selected
        '''

        pass

    #---------------

    def combobox_image_format_selected_item(self, event=None):
        '''
        Process the event when an item of "combobox_image_format" has been selected
        '''

        if self.wrapper_image_name.get() != '':
            file_name, file_extension = os.path.splitext(self.wrapper_image_name.get())
            self.wrapper_image_name.set('{0}.{1}'.format(file_name, self.wrapper_image_format.get().lower()))

    #---------------

    def check_inputs(self, *args):
        '''
        Check the content of each input of "FormPlotStats" and do the actions linked to its value
        '''

        # initialize the control variable
        OK = True

        # check the content of "entry_dpi"
        if not self.check_entry_dpi():
            OK = False

        # check the content of "entry_image_name"
        if not self.check_entry_image_name():
            OK = False

        # check if "button_execute" has to be enabled or disabled
        if self.stats_code in ['species', 'family', 'phylum', 'namespace', 'ec', 'interpro', 'kegg', 'mapman', 'metacyc']:
            if self.wrapper_experiment_id.get() != ''  and self.wrapper_pipeline_dataset.get() != '' and  self.wrapper_alignment_count_level.get() != '' and  self.wrapper_image_format.get() != '' and self.wrapper_dpi.get() != '' and self.wrapper_image_dir.get() != '' and self.wrapper_image_name.get() != '':
                self.button_execute['state'] = 'enable'
            else:
                self.button_execute['state'] = 'disabled'
        elif self.stats_code == 'go':
            if self.wrapper_experiment_id.get() != ''  and self.wrapper_pipeline_dataset.get() != '' and  self.wrapper_namespace.get() != '' and  self.wrapper_alignment_count_level.get() != '' and  self.wrapper_image_format.get() != '' and self.wrapper_dpi.get() != '' and self.wrapper_image_dir.get() != '' and self.wrapper_image_name.get() != '':
                self.button_execute['state'] = 'enable'
            else:
                self.button_execute['state'] = 'disabled'
        else:
            if self.wrapper_experiment_id.get() != ''  and self.wrapper_pipeline_dataset.get() != '' and  self.wrapper_image_format.get() != '' and self.wrapper_dpi.get() != '' and self.wrapper_image_dir.get() != '' and self.wrapper_image_name.get() != '':
                self.button_execute['state'] = 'enable'
            else:
                self.button_execute['state'] = 'disabled'

        # return the control variable
        return OK

    #---------------

    def check_entry_dpi(self):
        '''
        Check the content of "entry_dpi"
        '''

        # initialize the control variable
        OK = True

        # check that "entry_dpi" is an integer value
        if not xlib.check_int(self.wrapper_dpi.get(), minimum=100):
            self.label_dpi_warning['text'] = 'The value is not an integer number >= 100.'
            self.label_dpi_warning['foreground'] = 'red'
            OK = False
        else:
            self.label_dpi_warning['text'] = ''
            self.label_dpi_warning['foreground'] = 'black'

        # return the control variable
        return OK

    #---------------

    def check_entry_image_name(self):
        '''
        Check the content of "entry_image_name"
        '''

        # initialize the control variable
        OK = True

        # check that "entry_image_name" has the appropriate extension
        if self.wrapper_image_name.get() != '' and  self.wrapper_image_format.get() != '' and not self.wrapper_image_name.get().lower().endswith('.{0}'.format(self.wrapper_image_format.get().lower())):
            self.label_image_name_warning['text'] = 'The extension does not correspond with the format.'
            self.label_image_name_warning['foreground'] = 'red'
            OK = False
        else:
            self.label_image_name_warning['text'] = ''
            self.label_image_name_warning['foreground'] = 'black'

        # return the control variable
        return OK

    #---------------

    def execute(self):
        '''
        Run TOA process.
        '''

        # check inputs
        OK = self.check_inputs()
        if not OK:
            message = 'Some input values are not OK.'
            tkinter.messagebox.showerror('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # check if the image file exists
        if OK:
            image_file = '{0}/{1}'.format(self.wrapper_image_dir.get(), self.wrapper_image_name.get())
            if os.path.isfile(image_file):
                message = 'The image file is going to be overwritten. Are you sure to continue?'
                if not tkinter.messagebox.askyesno('{0} - Plot statistics'.format(xlib.get_short_project_name()), message):
                    OK = False

        # execute the corresponding process
        if OK:
            if self.stats_code in ['hit_per_hsp', 'seq_per_go', 'seq_per_ec', 'seq_per_interpro', 'seq_per_kegg', 'seq_per_mapman', 'seq_per_metacyc']:
                self.plot_x_per_y()
            elif self.stats_code in ['dataset', 'species', 'family', 'phylum', 'go', 'namespace', 'interpro', 'mapman', 'ec', 'kegg', 'metacyc']:
                self.plot_frecuency_distribution()

        # close the form
        if OK:
            self.close()

    #---------------

    def plot_x_per_y(self):
        '''
        Plot x count per y count.
        '''

        # set cursor to show busy status
        self.main.config(cursor='watch')
        self.main.update()

        # initialize the control variable
        OK = True

        # initialize the lists associated to the distribution dictionary
        x_count_list = []
        y_count_list = []

        # get the statistics file path
        stats_file = '{0}/{1}/{2}/{3}/{4}-{5}.csv'.format(self.toa_config_dict['RESULT_DIR'], self.wrapper_experiment_id.get(), self.combobox_pipeline_dataset.get(), self.toa_config_dict['STATS_SUBDIR_NAME'], self.stats_code, self.toa_config_dict['STATS_BASE_NAME'])

        # set the graphics file path
        image_file = '{0}/{1}'.format(self.wrapper_image_dir.get(), self.wrapper_image_name.get())

        # open the statistics file
        if stats_file.endswith('.gz'):
            try:
                stats_file_id = gzip.open(stats_file, mode='rt', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F002', stats_file)
        else:
            try:
                stats_file_id = open(stats_file, mode='r', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F001', stats_file)

        # initialize the record counter
        record_counter = 0

        # initialize the header record control
        header_record = True

        # read the first record
        record = stats_file_id.readline()

        # while there are records
        while record != '':

            # add 1 to the record counter
            record_counter += 1

            # process the header record
            if header_record:
                header_record = False

            # process data records
            else:

                # extract data
                # record format: "x_count";"y_count"
                data_list = []
                begin = 0
                for end in [i for i, chr in enumerate(record) if chr == ';']:
                    data_list.append(record[begin:end].strip('"'))
                    begin = end + 1
                data_list.append(record[begin:].strip('\n').strip('"'))
                try:
                    x_count_list.append(int(data_list[0]))
                    y_count_list.append(int(data_list[1]))
                except Exception as e:
                    raise xlib.ProgramException('F006', os.path.basename(stats_file), record_counter)

            # read the next record
            record = stats_file_id.readline()

        # check if there are any stats
        if len(x_count_list) == 0:
            message = 'There is not any stats data.'
            tkinter.messagebox.showwarning('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)
            OK = False

        # there are data
        else:

            # build distribution dictionary
            distribution_dict = {'x_count': x_count_list, 'y_count': y_count_list}

            # load data in a Pandas DataFrame
            distribution_df = pandas.DataFrame(distribution_dict)

            # set the title, caption and labels
            title = self.name
            caption = ''
            if self.stats_code == 'hit_per_hsp':
                label_x = '# HSPs'
                label_y = '# HITs'
            elif self.stats_code == 'seq_per_go':
                label_x = '# GO terms'
                label_y = '# sequences'
            elif self.stats_code == 'seq_per_ec':
                label_x = '# EC ids'
                label_y = '# sequences'
            elif self.stats_code == 'seq_per_interpro':
                label_x = '# InterPro ids'
                label_y = '# sequences'
            elif self.stats_code == 'seq_per_kegg':
                label_x = '# KEGG ids'
                label_y = '# sequences'
            elif self.stats_code == 'seq_per_mapman':
                label_x = '# MapMan ids'
                label_y = '# sequences'
            elif self.stats_code == 'seq_per_metacyc':
                label_x = '# MetaCyc ids'
                label_y = '# sequences'

            # build the plot
            plot = (plotnine.ggplot(data=distribution_df) +
                        plotnine.aes(x='x_count', y='y_count') +
                        plotnine.geom_bar(stat='identity', color='red', fill='red') +
                        plotnine.labs(title=title, caption=caption, x=label_x, y=label_y) +
                        plotnine.theme_grey() +
                        plotnine.theme(plot_title=plotnine.element_text(color='blue', margin={'b':15})) +
                        plotnine.theme(axis_title_x=plotnine.element_text(color='black')) +
                        plotnine.theme(axis_title_y=plotnine.element_text(color='black'))
            )
            plot.save(filename=image_file, height=4.8, width=6.4, dpi=int(self.wrapper_dpi.get()), verbose=False)

            # show the plot
            webbrowser.open_new('file://{0}'.format(image_file))

        # set cursor to show normal status
        self.main.config(cursor='')
        self.main.update()

    #---------------

    def plot_frecuency_distribution(self):
        '''
        Plot a bar plot when x is a interger number and y is a literal.
        '''

        # set cursor to show busy status
        self.main.config(cursor='watch')
        self.main.update()

        # initialize the control variable
        OK = True

        # initialize the data dictionary
        data_dict = {}

        # get the statistics file path
        stats_file = '{0}/{1}/{2}/{3}/{4}-{5}.csv'.format(self.toa_config_dict['RESULT_DIR'], self.wrapper_experiment_id.get(), self.combobox_pipeline_dataset.get(), self.toa_config_dict['STATS_SUBDIR_NAME'], self.stats_code, self.toa_config_dict['STATS_BASE_NAME'])

        # set the graphics file path
        image_file = '{0}/{1}'.format(self.wrapper_image_dir.get(), self.wrapper_image_name.get())

        # open the statistics file
        if stats_file.endswith('.gz'):
            try:
                stats_file_id = gzip.open(stats_file, mode='rt', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F002', stats_file)
        else:
            try:
                stats_file_id = open(stats_file, mode='r', encoding='iso-8859-1', newline='\n')
            except Exception as e:
                raise xlib.ProgramException('F001', stats_file)

        # initialize the record counter
        record_counter = 0

        # initialize the header record control
        header_record = True

        # read the first record
        record = stats_file_id.readline()

        # while there are records
        while record != '':

            # add 1 to the record counter
            record_counter += 1

            # process the header record
            if header_record:
                header_record = False

            # process data records
            else:

                # extract data and add item to the data dictionary
                data_list = []
                begin = 0
                for end in [i for i, chr in enumerate(record) if chr == ';']:
                    data_list.append(record[begin:end].strip('"'))
                    begin = end + 1
                data_list.append(record[begin:].strip('\n').strip('"'))
                try:
                    # record format: "dataset_name";"annotated_seq_count";"remained_seq_count"
                    if self.stats_code == 'dataset':
                        key = data_list[0]
                        value = int(data_list[1]) if xlib.check_int(data_list[1]) else 0
                        if value > 0:
                            data_dict[key] = value
                    # record format: "stats_code_id";"all_count";"first_hsp_count";"min_evalue_count"
                    elif self.stats_code in ['species', 'family', 'phylum', 'namespace']:
                        # format: "id";"all_count";"first_hsp_countT";"min_evalue_count"
                        key = data_list[0]
                        if self.wrapper_alignment_count_level.get() == 'all count':
                            value = int(data_list[1])
                        elif self.wrapper_alignment_count_level.get() == 'first HSP count':
                            value = int(data_list[2])
                        elif self.wrapper_alignment_count_level.get() == 'minimum e-value count':
                            value = int(data_list[3])
                        if value > 0:
                            data_dict[key] = value
                    # record format: "go_id";"description";"namespace";"all_count";"first_hsp_count";"min_evalue_count"
                    elif self.stats_code == 'go':
                        if self.wrapper_namespace.get() == 'all' or self.wrapper_namespace.get() == data_list[2]:
                            key = '{0} ({1})'.format(data_list[0], data_list[1])
                            if self.wrapper_alignment_count_level.get() == 'all count':
                                value = int(data_list[3])
                            elif self.wrapper_alignment_count_level.get() == 'first HSP count':
                                value = int(data_list[4])
                            elif self.wrapper_alignment_count_level.get() == 'minimum e-value count':
                                value = int(data_list[5])
                            if value > 0:
                                data_dict[key] = value
                    # record format: "stats_code_id";"description";"all_count";"first_hsp_count";"min_evalue_count"
                    elif self.stats_code == 'ec':
                        key = 'EC {0} ({1})'.format(data_list[0], data_list[1]) if data_list[1] != 'N/A' else 'EC {0}'.format(data_list[0])
                        if self.wrapper_alignment_count_level.get() == 'all count':
                            value = int(data_list[2])
                        elif self.wrapper_alignment_count_level.get() == 'first HSP count':
                            value = int(data_list[3])
                        elif self.wrapper_alignment_count_level.get() == 'minimum e-value count':
                            value = int(data_list[4])
                        if value > 0:
                            data_dict[key] = value
                    # record format: "stats_code_id";"description";"all_count";"first_hsp_count";"min_evalue_count"
                    elif self.stats_code in ['interpro', 'mapman', 'kegg']:
                        key = '{0} ({1})'.format(data_list[0], data_list[1])
                        if self.wrapper_alignment_count_level.get() == 'all count':
                            value = int(data_list[2])
                        elif self.wrapper_alignment_count_level.get() == 'first HSP count':
                            value = int(data_list[3])
                        elif self.wrapper_alignment_count_level.get() == 'minimum e-value count':
                            value = int(data_list[4])
                        if value > 0:
                            data_dict[key] = value
                    # record format: "metacyc_id";"description";"all_count";"first_hsp_count";"min_evalue_count"
                    elif self.stats_code == 'metacyc':
                        key = data_list[0]
                        if self.wrapper_alignment_count_level.get() == 'all count':
                            value = int(data_list[2])
                        elif self.wrapper_alignment_count_level.get() == 'first HSP count':
                            value = int(data_list[3])
                        elif self.wrapper_alignment_count_level.get() == 'minimum e-value count':
                            value = int(data_list[4])
                        if value > 0:
                            data_dict[key] = value
                except Exception as e:
                    raise xlib.ProgramException('F006', os.path.basename(stats_file), record_counter)

            # read the next record
            record = stats_file_id.readline()

        # check if there are any stats
        if data_dict == {}:
            message = 'There is not any stats data.'
            tkinter.messagebox.showwarning('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)
            OK = False

        # there are data
        else:

            # initialize the lists associated to the distribution dictionary
            text_list = []
            value_list = []

            # initialize the item counter
            item_counter = 0

            # initialize the value sum of remainder items
            remainder_sum = 0

            # sort the data dictionary by value
            for (key, value) in sorted(data_dict.items(), reverse=True, key=lambda x: x[1]):

                # check if item counter is less than the maximum of items to show
                if item_counter < 10:
                    text_list.append(key)
                    value_list.append(value)

                # if it not is less
                else:
                    remainder_sum += value

                # add 1 to the item counter
                item_counter += 1

            # build distribution dictionary
            text_list = list(reversed(text_list))
            value_list = list(reversed(value_list))
            distribution_dict = {'text_list': text_list, 'value_list': value_list}

            # load data in a Pandas DataFrame
            distribution_df = pandas.DataFrame(distribution_dict)
            distribution_df['text_list'] = pandas.Categorical(distribution_df['text_list'], categories=text_list, ordered=False)

            # set the title, caption and labels
            title = '{0} - Namespace: {1}'.format(self.name, self.wrapper_namespace.get()) if self.stats_code == 'go' else self.name
            caption = '' if self.stats_code == 'dataset' else 'Alignment count level: {0}'.format(self.wrapper_alignment_count_level.get())
            label_y = '# sequences' if self.stats_code == 'dataset' else '# alignments'

            # build the "plot"
            if self.stats_code == 'namespace':
                # pie chart
                explode = [0.01] * len(value_list)
                (fig1, ax1) = matplotlib.pyplot.subplots()
                (patches, texts, autotexts) = ax1.pie(value_list, explode=explode, labels=text_list, autopct='%1.1f%%', shadow=False, startangle=270)
                ax1.axis('equal')
                for text in texts:
                    text.set_color('grey')
                matplotlib.pyplot.title(title, color='blue')
                matplotlib.pyplot.savefig(image_file, dpi=int(self.wrapper_dpi.get()))
            else:
                # bar plot
                plot = (plotnine.ggplot(data=distribution_df) +
                            plotnine.aes(x='text_list', y='value_list') +
                            plotnine.geom_bar(stat='identity', size=0.1, color='green', fill='green') +
                            plotnine.geom_text(plotnine.aes(label='value_list'), va='center') +
                            plotnine.coord_flip() +
                            plotnine.labs(title=title, caption=caption, x='', y=label_y) +
                            plotnine.theme_grey() +
                            plotnine.theme(plot_title=plotnine.element_text(color='blue', margin={'b':15})) +
                            plotnine.theme(axis_title_x=plotnine.element_text(color='black')) +
                            plotnine.theme(axis_title_y=plotnine.element_text(color='black'))
                )
                plot.save(filename=image_file, height=6, width=10, dpi=int(self.wrapper_dpi.get()), verbose=False)

            # show the plot
            webbrowser.open_new('file://{0}'.format(image_file))

        # set cursor to show normal status
        self.main.config(cursor='')
        self.main.update()

    #---------------

    def close(self):
        '''
        Close "FormPlotStats".
        '''

        # clear the label of the current process name
        self.main.label_process['text'] = ''

        # close the current form
        self.main.close_current_form()

    #---------------

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print('This file contains the classes related to forms corresponding to menu items in gui mode.')
    sys.exit(0)

#-------------------------------------------------------------------------------
