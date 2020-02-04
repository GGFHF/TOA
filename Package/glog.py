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
This file contains the classes related to log forms in gui mode.
'''

#-------------------------------------------------------------------------------

import os
import re
import sys
import tkinter
import tkinter.ttk
import subprocess

import gdialogs
import xlib
import xtoa

#-------------------------------------------------------------------------------

class FormViewSubmissionLogs(tkinter.Frame):

    #---------------

    def __init__(self, parent, main):
        '''
        Execute actions correspending to the creation of a "FormViewSubmissionLogs" instance.
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
        self.head = 'Logs - View submission logs'

        # create the wrappers to track changes in the inputs
        self.wrapper_submission_process_text = tkinter.StringVar()
        self.wrapper_submission_process_text.trace('w', self.check_inputs)

        # build the graphical user interface
        self.build_gui()

        # initialize the cluster name previously selected
        self.cluster_name_ant = None

        # load initial data in inputs
        self.initialize_inputs()

        # set cursor to show normal status
        self.main.config(cursor='')
        self.main.update()

    #---------------

    def build_gui(self):
        '''
        Build the graphical user interface of "FormViewSubmissionLogs".
        '''

        # assign the text to the label of the current process name
        self.main.label_process['text'] = self.head

        # create "label_submission_process_text" and register it with the grid geometry manager
        self.label_submission_process_text = tkinter.Label(self, text='Submission process')
        self.label_submission_process_text.grid(row=0, column=0, padx=(15,5), pady=(75,5), sticky='e')

        # create "combobox_submission_process_text" and register it with the grid geometry manager
        self.combobox_submission_process_text = tkinter.ttk.Combobox(self, width=50, height=4, state='readonly', textvariable=self.wrapper_submission_process_text)
        self.combobox_submission_process_text.grid(row=0, column=1, padx=(5,5), pady=(75,5), sticky='w')

        # create "label_fit" and register it with the grid geometry manager
        self.label_fit = tkinter.Label(self, text=' '*(25+xlib.get_os_size_fix()))
        self.label_fit.grid(row=2, column=2, padx=(0,0), pady=(45,5), sticky='e')

        # create "button_execute" and register it with the grid geometry manager
        self.button_execute = tkinter.ttk.Button(self, text='Execute', command=self.execute, state='disabled')
        self.button_execute.grid(row=2, column=3, padx=(5,5), pady=(45,5), sticky='e')

        # create "button_close" and register it with the grid geometry manager
        self.button_close = tkinter.ttk.Button(self, text='Close', command=self.close)
        self.button_close.grid(row=2, column=4, padx=(5,5), pady=(45,5), sticky='w')

        # link a handler to events
        self.combobox_submission_process_text.bind('<<ComboboxSelected>>', self.combobox_submission_process_text_selected_item)

    #---------------

    def initialize_inputs(self):
        '''
        Load initial data in inputs.
        '''

        # load initial data in inputs
        self.submission_process_id = None

        # populate data in comboboxes
        self.populate_combobox_submission_process_text()

    #---------------

    def populate_combobox_submission_process_text(self):
        '''
        Populate data in "combobox_submission_process_text".
        '''

        # clear the value selected in the combobox
        self.wrapper_submission_process_text.set('')

        # get the submission process dictionary
        submission_process_dict = xlib.get_submission_process_dict()

        # build the submission process text list
        submission_process_text_list = []
        for submission_process_id in submission_process_dict.keys():
            submission_process_text_list.append(submission_process_dict[submission_process_id]['text'])

        # add item 'all' to submission process text list
        submission_process_text_list.sort()

        # load the names of submission processes
        self.combobox_submission_process_text['values'] = ['all'] + submission_process_text_list

    #---------------

    def combobox_submission_process_text_selected_item(self, event=None):
        '''
        Process the event when an item of "combobox_submission_process_text" has been selected
        '''

        # get the submission process identification
        self.submission_process_id = xlib.get_submission_process_id(self.wrapper_submission_process_text.get())

    #---------------

    def check_inputs(self, *args):
        '''
        Check the content of each input of "FormViewSubmissionLogs" and do the actions linked to its value
        '''

        # initialize the control variable
        OK = True

        # check if "button_execute" has to be enabled or disabled
        if self.wrapper_submission_process_text.get() != '':
            self.button_execute['state'] = 'enable'
        else:
            self.button_execute['state'] = 'disabled'

        # return the control variable
        return OK

    #---------------

    def execute(self):
        '''
        Execute the list the submission logs.
        '''

        # check inputs
        OK = self.check_inputs()
        if not OK:
            message = 'Some input values are not OK.'
            tkinter.messagebox.showerror('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # get the submission process dictionary
        submission_process_dict = xlib.get_submission_process_dict()

        # build the log dictionary
        if OK:
            log_dict = {}
            if self.wrapper_submission_process_text.get() == 'all':
                command = xlib.list_log_files_command('all')
            else:
                command = xlib.list_log_files_command(self.submission_process_id)
            output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            for line in output.stdout.split('\n'):
                if line != '':
                    line = os.path.basename(line)
                    run_id = line
                    try:
                        pattern = r'^(.+)\-(.+)\-(.+).txt$'
                        mo = re.search(pattern, line)
                        submission_process_id = mo.group(1).strip()
                        yymmdd = mo.group(2)
                        hhmmss = mo.group(3)
                        process_text = submission_process_dict[submission_process_id]['text']
                        date = '20{0}-{1}-{2}'.format(yymmdd[:2], yymmdd[2:4], yymmdd[4:])
                        time = '{0}:{1}:{2}'.format(hhmmss[:2], hhmmss[2:4], hhmmss[4:])
                    except Exception as e:
                        process_text = 'unknown process'
                        date = '0000-00-00'
                        time = '00:00:00'
                    key = '{0}-{1}'.format(process_text, run_id)
                    log_dict[key] = {'process_text': process_text, 'run_id': run_id, 'date': date, 'time': time}

        # check if there are any submission logs
        if OK:
            if log_dict == {}:
                message = 'There is not any submission process log.'
                tkinter.messagebox.showwarning('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)
                OK = False

        # build the data list
        if OK:
            data_list = ['process_text', 'run_id', 'date', 'time']

        # build the data dictionary
        if OK:
            data_dict = {}
            data_dict['process_text'] = {'text': 'Process', 'width': 300, 'alignment': 'left'}
            data_dict['run_id'] = {'text': 'Run id', 'width': 400, 'alignment': 'left'}
            data_dict['date'] = {'text': 'Date', 'width': 95, 'alignment': 'right'}
            data_dict['time'] = {'text': 'Time', 'width': 75, 'alignment': 'right'}

        # create the dialog Table to list the submission process logs
        if OK:
            dialog_table = gdialogs.DialogTable(self, 'Submission process log', 400, 900, data_list, data_dict, log_dict, sorted(log_dict.keys()), 'view_submission_logs')
            self.wait_window(dialog_table)

        # close the form
        if OK:
            self.close()

    #---------------

    def close(self):
        '''
        Close "FormViewSubmissionLogs".
        '''

        # clear the label of the current process name
        self.main.label_process['text'] = ''

        # close the current form
        self.main.close_current_form()

   #---------------

#-------------------------------------------------------------------------------

class FormViewResultLogs(tkinter.Frame):

    #---------------

    def __init__(self, parent, main):
        '''
        Execute actions correspending to the creation of a "FormViewResultLogs" instance.
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
        self.head = 'Logs - View result logs'

        # create the wrappers to track changes in the inputs
        self.wrapper_experiment_id = tkinter.StringVar()
        self.wrapper_experiment_id.trace('w', self.check_inputs)

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
        Build the graphical user interface of "FormViewResultLogs".
        '''

        # assign the text to the label of the current process name
        self.main.label_process['text'] = self.head

        # create "label_experiment_id" and register it with the grid geometry manager
        self.label_experiment_id = tkinter.Label(self, text='Experiment/process')
        self.label_experiment_id.grid(row=0, column=0, padx=(15,5), pady=(75,5), sticky='e')

        # create "combobox_experiment_id" and register it with the grid geometry manager
        self.combobox_experiment_id = tkinter.ttk.Combobox(self, width=30, height=4, state='readonly', textvariable=self.wrapper_experiment_id)
        self.combobox_experiment_id.grid(row=0, column=1, padx=(5,5), pady=(75,5), sticky='w')

        # create "label_fit" and register it with the grid geometry manager
        self.label_fit = tkinter.Label(self, text=' '*(65+xlib.get_os_size_fix()))
        self.label_fit.grid(row=1, column=2, padx=(0,0), pady=(45,5), sticky='e')

        # create "button_execute" and register it with the grid geometry manager
        self.button_execute = tkinter.ttk.Button(self, text='Execute', command=self.execute, state='disabled')
        self.button_execute.grid(row=1, column=3, padx=(5,5), pady=(45,5), sticky='e')

        # create "button_close" and register it with the grid geometry manager
        self.button_close = tkinter.ttk.Button(self, text='Close', command=self.close)
        self.button_close.grid(row=1, column=4, padx=(5,5), pady=(45,5), sticky='w')

        # link a handler to events
        self.combobox_experiment_id.bind('<<ComboboxSelected>>', self.combobox_experiment_id_selected_item)

    #---------------

    def initialize_inputs(self):
        '''
        Load initial data in inputs.
        '''

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
        experiment_id_list = []

        # get the dictionary of TOA configuration.
        toa_config_dict = xtoa.get_toa_config_dict()

        # get the experiment identifications
        subdir_list = [subdir for subdir in os.listdir(toa_config_dict['RESULT_DIR']) if os.path.isdir(os.path.join(toa_config_dict['RESULT_DIR'], subdir))]
        for subdir in subdir_list:
            experiment_id_list.append(subdir)

        # check if there are any experimment identifications
        if experiment_id_list == []:
            message = 'There is not any experiment/process run.'
            tkinter.messagebox.showwarning('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)
            return

        # load the names of clusters which are running in the combobox
        self.combobox_experiment_id['values'] = experiment_id_list

    #---------------

    def combobox_experiment_id_selected_item(self, event=None):
        '''
        Process the event when an item of "combobox_experiment_id" has been selected
        '''

        pass

    #---------------

    def check_inputs(self, *args):
        '''
        Check the content of each input of "FormViewResultLogs" and do the actions linked to its value
        '''

        # initialize the control variable
        OK = True

        # check if "button_execute" has to be enabled or disabled
        if self.wrapper_experiment_id.get() != '':
            self.button_execute['state'] = 'enable'
        else:
            self.button_execute['state'] = 'disabled'

        # return the control variable
        return OK

    #---------------

    def execute(self):
        '''
        Execute the list the result logs in the cluster.
        '''

        # check inputs
        OK = self.check_inputs()
        if not OK:
            message = 'Some input values are not OK.'
            tkinter.messagebox.showerror('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # get the dictionary of TOA configuration.
        if OK:
            toa_config_dict = xtoa.get_toa_config_dict()

        # get the run dictionary of the experiment
        if OK:
            experiment_dir = '{0}/{1}'.format(toa_config_dict['RESULT_DIR'], self.wrapper_experiment_id.get())
            subdir_list = [subdir for subdir in os.listdir(experiment_dir) if os.path.isdir(os.path.join(experiment_dir, subdir))]
            result_dataset_dict = {}
            for subdir in subdir_list:
                result_dataset_id = subdir
                try:
                    pattern = r'^(.+)\-(.+)\-(.+)$'
                    mo = re.search(pattern, result_dataset_id)
                    bioinfo_app_code = mo.group(1).strip()
                    yymmdd = mo.group(2)
                    hhmmss = mo.group(3)
                    date = '20{0}-{1}-{2}'.format(yymmdd[:2], yymmdd[2:4], yymmdd[4:])
                    time = '{0}:{1}:{2}'.format(hhmmss[:2], hhmmss[2:4], hhmmss[4:])
                except Exception as e:
                    bioinfo_app_code = 'xxx'
                    date = '0000-00-00'
                    time = '00:00:00'
                if result_dataset_id.startswith(xlib.get_blastplus_code()+'-'):
                    bioinfo_app_name = xlib.get_blastplus_name()
                elif result_dataset_id.startswith(xlib.get_entrez_direct_code()+'-'):
                    bioinfo_app_name = xlib.get_entrez_direct_name()
                elif result_dataset_id.startswith(xlib.get_miniconda3_code()+'-'):
                    bioinfo_app_name = xlib.get_miniconda3_name()
                elif result_dataset_id.startswith(xlib.get_r_code()+'-'):
                    bioinfo_app_name = xlib.get_r_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_blastdb_nr_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_blastdb_nr_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_blastdb_nt_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_blastdb_nt_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_download_basic_data_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_download_basic_data_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_download_dicots_04_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_download_dicots_04_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_download_gene_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_download_gene_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_download_go_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_download_go_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_download_gymno_01_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_download_gymno_01_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_download_interpro_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_download_interpro_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_download_monocots_04_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_download_monocots_04_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_gilist_viridiplantae_nucleotide_gi_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_gilist_viridiplantae_nucleotide_gi_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_gilist_viridiplantae_protein_gi_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_gilist_viridiplantae_protein_gi_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_load_basic_data_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_load_basic_data_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_load_dicots_04_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_load_dicots_04_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_load_gene_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_load_gene_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_load_go_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_load_go_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_load_gymno_01_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_load_gymno_01_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_load_interpro_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_load_interpro_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_load_monocots_04_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_load_monocots_04_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_pipeline_aminoacid_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_pipeline_aminoacid_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_pipeline_nucleotide_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_pipeline_nucleotide_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_proteome_dicots_04_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_proteome_dicots_04_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_proteome_gymno_01_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_proteome_gymno_01_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_proteome_monocots_04_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_proteome_monocots_04_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_proteome_refseq_plant_code()+'-'):
                    bioinfo_app_name = xlib.get_toa_process_proteome_refseq_plant_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_rebuild_toa_database_code()+'-'):
                    bioinfo_app_name = xlib.get_get_toa_process_rebuild_toa_database_name()
                elif result_dataset_id.startswith(xlib.get_toa_process_recreate_toa_database_code()+'-'):
                    bioinfo_app_name = xlib.get_get_toa_process_recreate_toa_database_name()
                elif result_dataset_id.startswith(xlib.get_transdecoder_code()+'-'):
                    bioinfo_app_name = xlib.get_transdecoder_name()
                else:
                    bioinfo_app_name = 'xxx'
                status_ok = os.path.isfile(xlib.get_status_ok(os.path.join(experiment_dir, subdir)))
                status_wrong = os.path.isfile(xlib.get_status_wrong(os.path.join(experiment_dir, subdir)))
                if status_ok and not status_wrong:
                    status = 'OK'
                elif not status_ok and status_wrong:
                    status = 'wrong'
                elif not status_ok and not status_wrong:
                    status = 'not finished'
                elif status_ok and status_wrong:
                    status = 'undetermined'
                key = '{0}-{1}'.format(bioinfo_app_name, result_dataset_id)
                result_dataset_dict[key] = {'experiment_id': self.wrapper_experiment_id.get(), 'bioinfo_app': bioinfo_app_name, 'result_dataset_id': result_dataset_id, 'date': date, 'time': time, 'status': status}

        # check if there are any nodes running
        if OK:
            if result_dataset_dict == {}:
                message = 'There is not any run.'
                tkinter.messagebox.showwarning('{0} - {1}'.format(xlib.get_short_project_name(), self.head), message)

        # build the data list
        if OK:
            data_list = ['experiment_id', 'bioinfo_app', 'result_dataset_id', 'date', 'time', 'status']

        # build the data dictionary
        if OK:
            data_dict = {}
            data_dict['experiment_id']= {'text': 'Experiment id./Process', 'width': 180, 'alignment': 'left'}
            data_dict['bioinfo_app'] = {'text': 'Bioinfo app / Utility', 'width': 340, 'alignment': 'left'}
            data_dict['result_dataset_id'] = {'text': 'Result dataset', 'width': 225, 'alignment': 'left'}
            data_dict['date'] = {'text': 'Date', 'width': 95, 'alignment': 'right'}
            data_dict['time'] = {'text': 'Time', 'width': 75, 'alignment': 'right'}
            data_dict['status'] = {'text': 'Status', 'width': 90, 'alignment': 'left'}

        # create the dialog Table to show the nodes running
        if OK:
            dialog_table = gdialogs.DialogTable(self, 'Experiment/Process runs in {0}/{1}'.format(xlib.get_result_dir(), self.wrapper_experiment_id.get()), 400, 1030, data_list, data_dict, result_dataset_dict, sorted(result_dataset_dict.keys()), 'view_result_logs', ['revisar'])
            self.wait_window(dialog_table)

        # close the form
        if OK:
            self.close()

    #---------------

    def close(self):
        '''
        Close "FormViewResultLogs".
        '''

        # clear the label of the current process name
        self.main.label_process['text'] = ''

        # close the current form
        self.main.close_current_form()

   #---------------

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print('This file contains the classes related to log form in gui mode.')
    sys.exit(0)

#-------------------------------------------------------------------------------
