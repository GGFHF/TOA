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
This source contains the class Main corresponding to the graphical user interface of
the TOA (Taxonomy-oriented Annotation) software package.
'''

#-------------------------------------------------------------------------------

import os
import PIL.Image
import PIL.ImageTk
import tkinter
import tkinter.messagebox
import tkinter.ttk
import sys
import webbrowser

import gbioinfoapp
import gdialogs
import glog
import gtoa
import xlib
import xtoa

#-------------------------------------------------------------------------------

class Main():

    #---------------

    if sys.platform.startswith('linux'):
        WINDOW_HEIGHT = 620
        WINDOW_WIDTH = 875
    elif sys.platform.startswith('darwin'):
        WINDOW_HEIGHT = 650
        WINDOW_WIDTH = 980
    elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
        WINDOW_HEIGHT = 585
        WINDOW_WIDTH = 800

    #---------------

    def __init__(self):
        '''
        Execute actions correspending to the creation of a "Main" instance.
        '''

        # call the init method of the parent class
        self.root = tkinter.Tk()

        # create the window
        self.create_window()

        # build the graphical user interface
        self.build_gui()
        # self.root.grid()

        # initialize the forms dictionary
        self.forms_dict = {}

        # create "form_welcome" and register it in "container" with the grid geometry manager
        self.form_welcome = FormWelcome(self)
        self.form_welcome.grid(row=0, column=0, sticky='nsew')

        # set "form_welcome" as current form and add it in the forms dictionary
        self.current_form = 'form_welcome'
        self.forms_dict[self.current_form] = self.form_welcome

        # raise "form_set_environment" to front
        self.form_welcome.tkraise()

    #---------------

    def create_window(self):
        '''
        Create the window of "Main".
        '''

        # define the dimensions
        x = round((self.root.winfo_screenwidth() - self.WINDOW_WIDTH) / 2)
        y = round((self.root.winfo_screenheight() - self.WINDOW_HEIGHT) / 2)
        self.root.geometry('{}x{}+{}+{}'.format(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, x, y))
        self.root.minsize(height=self.WINDOW_HEIGHT, width=self.WINDOW_WIDTH)
        self.root.maxsize(height=self.WINDOW_HEIGHT, width=self.WINDOW_WIDTH)

        # set default fondt
        self.root.option_add("*Font", "Verdana 10")

        # set default language of MessageBox
        self.root.tk.eval('::msgcat::mclocale en')

        # set the title
        self.root.title(xlib.get_long_project_name())

        # set the icon
        image_app = PIL.Image.open(xlib.get_project_image_file())
        self.photoimage_app = PIL.ImageTk.PhotoImage(image_app)
        self.root.tk.call('wm', 'iconphoto', self.root._w, self.photoimage_app)

    #---------------

    def build_gui(self):
        '''
        Build the graphical user interface of "Main".
        '''

        # create "imagetk_exit"
        image_exit = PIL.Image.open('./image_exit.png')
        imagetk_exit = PIL.ImageTk.PhotoImage(image_exit)  

        # maximize the width of column 0
        self.root.grid_columnconfigure(0, weight=1)

        # create "menu_bar"
        self.menu_bar = tkinter.Menu(self.root)

        # create "menu_system" and add its menu items
        self.menu_system = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_system.add_command(label='Exit', command=self.exit, accelerator='Alt+F4', compound='left', image=imagetk_exit)

        # link "menu_system" to "menu_bar"
        self.menu_bar.add_cascade(label='System', menu=self.menu_system)

        # create "menu_bioinfo_software_installation" add add its menu items
        self.menu_bioinfo_software_installation = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_bioinfo_software_installation.add_command(label=f'{xlib.get_miniconda3_name()} (Conda infrastructure)', command=self.install_miniconda3)
        self.menu_bioinfo_software_installation.add_separator()
        self.menu_bioinfo_software_installation.add_command(label=xlib.get_blastplus_name(), command=self.install_blastplus)
        self.menu_bioinfo_software_installation.add_command(label=xlib.get_diamond_name(), command=self.install_diamond)
        self.menu_bioinfo_software_installation.add_command(label=xlib.get_entrez_direct_name(), command=self.install_entrez_direct)
        self.menu_bioinfo_software_installation.add_command(label=xlib.get_transdecoder_name(), command=self.install_transdecoder)
        # -- self.menu_bioinfo_software_installation.add_separator()
        # -- self.menu_bioinfo_software_installation.add_command(label=f'{xlib.get_r_name()} & analysis packages', command=self.install_r)

        # create "menu_toa_configuration" and add its menu items
        self.menu_toa_configuration = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_configuration.add_command(label=f'Recreate {xlib.get_toa_name()} config file', command=self.recreate_toa_config_file)
        self.menu_toa_configuration.add_command(label=f'View {xlib.get_toa_name()} config file', command=self.view_toa_config_file)
        self.menu_toa_configuration.add_separator()
        self.menu_toa_configuration.add_command(label=f'Recreate {xlib.get_toa_name()} database', command=self.recreate_toa_database)
        self.menu_toa_configuration.add_command(label=f'Rebuild {xlib.get_toa_name()} database', command=self.rebuild_toa_database)
        self.menu_toa_configuration.add_separator()
        self.menu_toa_configuration.add_cascade(label='Bioinfo software installation', menu=self.menu_bioinfo_software_installation)

        # link "menu_toa_configuration" to "menu_bar"
        self.menu_bar.add_cascade(label='Configuration', menu=self.menu_toa_configuration)

        # create "menu_toa_basic_data" and add its menu items
        self.menu_toa_basic_data = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_basic_data.add_command(label='Recreate genomic dataset file', command=self.recreate_dataset_file)
        self.menu_toa_basic_data.add_command(label='Edit genomic dataset file', command=self.edit_dataset_file)
        self.menu_toa_basic_data.add_separator()
        self.menu_toa_basic_data.add_command(label='Recreate species file', command=self.recreate_species_file)
        self.menu_toa_basic_data.add_command(label='Edit species file', command=self.edit_species_file)
        self.menu_toa_basic_data.add_separator()
        self.menu_toa_basic_data.add_command(label='Download other basic data', command=self.download_basic_data)
        self.menu_toa_basic_data.add_separator()
        self.menu_toa_basic_data.add_command(label=f'Load data into {xlib.get_toa_name()} database', command=self.load_basic_data)

        # create "menu_toa_gymno_01" and add its menu items
        self.menu_toa_gymno_01 = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_gymno_01.add_command(label='Build proteome', command=self.build_gymno_01_proteome)
        self.menu_toa_gymno_01.add_separator()
        self.menu_toa_gymno_01.add_command(label='Download functional annotations from PLAZA server', command=self.download_gymno_01_data)
        self.menu_toa_gymno_01.add_command(label=f'Load data into {xlib.get_toa_name()} database', command=self.load_gymno_01_data)

        # create "menu_toa_dicots_04" and add its menu items
        self.menu_toa_dicots_04 = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_dicots_04.add_command(label='Build proteome', command=self.build_dicots_04_proteome)
        self.menu_toa_dicots_04.add_separator()
        self.menu_toa_dicots_04.add_command(label='Download functional annotations from PLAZA server', command=self.download_dicots_04_data)
        self.menu_toa_dicots_04.add_command(label=f'Load data into {xlib.get_toa_name()} database', command=self.load_dicots_04_data)

        # create "menu_toa_monocots_04" and add its menu items
        self.menu_toa_monocots_04 = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_monocots_04.add_command(label='Build proteome', command=self.build_monocots_04_proteome)
        self.menu_toa_monocots_04.add_separator()
        self.menu_toa_monocots_04.add_command(label='Download functional annotations from PLAZA server', command=self.download_monocots_04_data)
        self.menu_toa_monocots_04.add_command(label=f'Load data into {xlib.get_toa_name()} database', command=self.load_monocots_04_data)

        # create "menu_toa_refseq_plant" and add its menu items
        self.menu_toa_refseq_plant = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_refseq_plant.add_command(label='Build proteome', command=self.build_refseq_plant_proteome)

        # create "menu_toa_taxonomy" and add its menu items
        self.menu_toa_taxonomy = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_taxonomy.add_command(label='Download taxonomy data from NCBI server', command=self.download_taxonomy_data)

        # create "menu_toa_nt" and add its menu items
        self.menu_toa_nt = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_nt.add_command(label='Build database for BLAST+', command=self.build_blastplus_nt_db)

        # create "menu_toa_nucleotide_gi" and add its menu items
        self.menu_toa_nucleotide_gi = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_nucleotide_gi.add_command(label='Build identifier list using NCBI server', command=self.build_viridiplantae_nucleotide_gi_gilist)

        # create "menu_toa_nr" and add its menu items
        self.menu_toa_nr = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_nr.add_command(label='Build database for BLAST+', command=self.build_blastplus_nr_db)
        self.menu_toa_nr.add_command(label='Build database for DIAMOND', command=self.build_diamond_nr_db)

        # create "menu_toa_protein_gi" and add its menu items
        self.menu_toa_protein_gi = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_protein_gi.add_command(label='Build identifier list using NCBI server', command=self.build_viridiplantae_protein_gi_gilist)

        # create "menu_toa_gene" and add its menu items
        self.menu_toa_gene = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_gene.add_command(label='Download functional annotations from NCBI server', command=self.download_gene_data)
        self.menu_toa_gene.add_command(label=f'Load data into {xlib.get_toa_name()} database', command=self.load_gene_data)

        # create "menu_toa_interpro" and add its menu items
        self.menu_toa_interpro = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_interpro.add_command(label='Download functional annotations from InterPro server', command=self.download_interpro_data)
        self.menu_toa_interpro.add_command(label=f'Load data into {xlib.get_toa_name()} database', command=self.load_interpro_data)

        # create "menu_toa_go" and add its menu items
        self.menu_toa_go = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_go.add_command(label='Download functional annotations from Gene Ontology server', command=self.download_go_data)
        self.menu_toa_go.add_command(label=f'Load data into {xlib.get_toa_name()} database', command=self.load_go_data)

        # create "menu_toa_databases" and add its menu items
        self.menu_toa_databases = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_databases.add_cascade(label=xlib.get_toa_data_basic_data_name(), menu=self.menu_toa_basic_data)
        self.menu_toa_databases.add_separator()
        self.menu_toa_databases.add_cascade(label=xlib.get_toa_data_gymno_01_name(), menu=self.menu_toa_gymno_01)
        self.menu_toa_databases.add_cascade(label=xlib.get_toa_data_dicots_04_name(), menu=self.menu_toa_dicots_04)
        self.menu_toa_databases.add_cascade(label=xlib.get_toa_data_monocots_04_name(), menu=self.menu_toa_monocots_04)
        self.menu_toa_databases.add_separator()
        self.menu_toa_databases.add_cascade(label=xlib.get_toa_data_refseq_plant_name(), menu=self.menu_toa_refseq_plant)
        # -- self.menu_toa_databases.add_cascade(label=xlib.get_toa_data_taxonomy_name(), menu=self.menu_toa_taxonomy)
        self.menu_toa_databases.add_cascade(label=xlib.get_toa_data_nt_name(), menu=self.menu_toa_nt)
        # -- self.menu_toa_databases.add_cascade(label=xlib.get_toa_data_viridiplantae_nucleotide_gi_name(), menu=self.menu_toa_nucleotide_gi)
        self.menu_toa_databases.add_cascade(label=xlib.get_toa_data_nr_name(), menu=self.menu_toa_nr)
        # -- self.menu_toa_databases.add_cascade(label=xlib.get_toa_data_viridiplantae_protein_gi_name(), menu=self.menu_toa_protein_gi)
        self.menu_toa_databases.add_cascade(label=xlib.get_toa_data_gene_name(), menu=self.menu_toa_gene)
        self.menu_toa_databases.add_separator()
        self.menu_toa_databases.add_cascade(label=xlib.get_toa_data_interpro_name(), menu=self.menu_toa_interpro)
        self.menu_toa_databases.add_separator()
        self.menu_toa_databases.add_cascade(label=xlib.get_toa_data_go_name(), menu=self.menu_toa_go)

        # link "menu_toa_databases" to "menu_bar"
        self.menu_bar.add_cascade(label='Genomic databases', menu=self.menu_toa_databases)

        # create "menu_toa_nucleotide_pipeline" and add its menu items
        self.menu_toa_nucleotide_pipeline = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_nucleotide_pipeline.add_command(label='Recreate config file', command=self.recreate_nucleotide_pipeline_config_file)
        self.menu_toa_nucleotide_pipeline.add_command(label='Edit config file', command=self.edit_nucleotide_pipeline_config_file)
        self.menu_toa_nucleotide_pipeline.add_separator()
        self.menu_toa_nucleotide_pipeline.add_command(label='Run pipeline', command=self.run_nucleotide_pipeline_process)
        self.menu_toa_nucleotide_pipeline.add_command(label='Restart pipeline', command=self.restart_nucleotide_pipeline_process)

        # create "menu_toa_aminoacid_pipeline" and add its menu items
        self.menu_toa_aminoacid_pipeline = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_aminoacid_pipeline.add_command(label='Recreate config file', command=self.recreate_aminoacid_pipeline_config_file)
        self.menu_toa_aminoacid_pipeline.add_command(label='Edit config file', command=self.edit_aminoacid_pipeline_config_file)
        self.menu_toa_aminoacid_pipeline.add_separator()
        self.menu_toa_aminoacid_pipeline.add_command(label='Run pipeline', command=self.run_aminoacid_pipeline_process)
        self.menu_toa_aminoacid_pipeline.add_command(label='Restart pipeline', command=self.restart_aminoacid_pipeline_process)

        # create "menu_toa_annotation_merger" and add its menu items
        self.menu_toa_annotation_merger = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_annotation_merger.add_command(label='Recreate config file', command=self.recreate_annotation_merger_config_file)
        self.menu_toa_annotation_merger.add_command(label='Edit config file', command=self.edit_annotation_merger_config_file)
        self.menu_toa_annotation_merger.add_separator()
        self.menu_toa_annotation_merger.add_command(label='Run process', command=self.run_annotation_merger_process)

        # create "menu_toa_pipelines" and add its menu items
        self.menu_toa_pipelines = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_pipelines.add_cascade(label=f'{xlib.get_toa_name()} {xlib.get_toa_process_pipeline_nucleotide_name()}', menu=self.menu_toa_nucleotide_pipeline)
        self.menu_toa_pipelines.add_cascade(label=f'{xlib.get_toa_name()} {xlib.get_toa_process_pipeline_aminoacid_name()}', menu=self.menu_toa_aminoacid_pipeline)
        self.menu_toa_pipelines.add_separator()
        self.menu_toa_pipelines.add_cascade(label=f'Annotation merger of {xlib.get_toa_name()} pipelines', menu=self.menu_toa_annotation_merger)

        # link "menu_toa_pipelines" to "menu_bar"
        self.menu_bar.add_cascade(label='Annotation pipelines', menu=self.menu_toa_pipelines)

        # create "menu_toa_alignment_stats" and add its menu items
        self.menu_toa_alignment_stats = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_alignment_stats.add_command(label='# HITs per # HSPs data', command=self.view_hit_per_hsp_data)
        if os.getcwd() != xlib.get_docker_toa_dir():
            self.menu_toa_alignment_stats.add_command(label='# HITs per # HSPs plot', command=self.plot_hit_per_hsp_data)

        # create "menu_toa_annotation_dataset_stats" and add its menu items
        self.menu_toa_annotation_dataset_stats = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_annotation_dataset_stats.add_command(label='Frequency distribution data', command=self.view_annotation_dataset_frequency)
        if os.getcwd() != xlib.get_docker_toa_dir():
            self.menu_toa_annotation_dataset_stats.add_command(label='Frequency distribution plot', command=self.plot_annotation_dataset_frequency)

        # create "menu_toa_species_stats" and add its menu items
        self.menu_toa_species_stats = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_species_stats.add_command(label='Frequency distribution data', command=self.view_species_frequency)
        if os.getcwd() != xlib.get_docker_toa_dir():
            self.menu_toa_species_stats.add_command(label='Frequency distribution plot', command=self.plot_species_frequency)

        # create "menu_toa_family_stats" and add its menu items
        self.menu_toa_family_stats = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_family_stats.add_command(label='Frequency distribution data', command=self.view_family_frequency)
        if os.getcwd() != xlib.get_docker_toa_dir():
            self.menu_toa_family_stats.add_command(label='Frequency distribution plot', command=self.plot_family_frequency)

        # create "menu_toa_phylum_stats" and add its menu items
        self.menu_toa_phylum_stats = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_phylum_stats.add_command(label='Frequency distribution data', command=self.view_phylum_frequency)
        if os.getcwd() != xlib.get_docker_toa_dir():
            self.menu_toa_phylum_stats.add_command(label='Frequency distribution plot', command=self.plot_phylum_frequency)

        # create "menu_toa_ec_stats" and add its menu items
        self.menu_toa_ec_stats = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_ec_stats.add_command(label='Frequency distribution data', command=self.view_ec_frequency)
        if os.getcwd() != xlib.get_docker_toa_dir():
            self.menu_toa_ec_stats.add_command(label='Frequency distribution plot', command=self.plot_ec_frequency)
        self.menu_toa_ec_stats.add_separator()
        self.menu_toa_ec_stats.add_command(label='# sequences per # ids data', command=self.view_seq_per_ec_data)
        if os.getcwd() != xlib.get_docker_toa_dir():
            self.menu_toa_ec_stats.add_command(label='# sequences per # ids plot', command=self.plot_seq_per_ec_data)

        # create "menu_toa_go_stats" and add its menu items
        self.menu_toa_go_stats = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_go_stats.add_command(label='Frequency distribution per term data', command=self.view_go_frequency)
        if os.getcwd() != xlib.get_docker_toa_dir():
            self.menu_toa_go_stats.add_command(label='Frequency distribution per term plot', command=self.plot_go_frequency)
        self.menu_toa_go_stats.add_separator()
        self.menu_toa_go_stats.add_command(label='Frequency distribution per namespace data', command=self.view_namespace_frequency)
        if os.getcwd() != xlib.get_docker_toa_dir():
            self.menu_toa_go_stats.add_command(label='Frequency distribution per namespace plot', command=self.plot_namespace_frequency)
        self.menu_toa_go_stats.add_separator()
        self.menu_toa_go_stats.add_command(label='# sequences per # terms data', command=self.view_seq_per_go_data)
        if os.getcwd() != xlib.get_docker_toa_dir():
            self.menu_toa_go_stats.add_command(label='# sequences per # terms plot', command=self.plot_seq_per_go_data)

        # create "menu_toa_interpro_stats" and add its menu items
        self.menu_toa_interpro_stats = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_interpro_stats.add_command(label='Frequency distribution data', command=self.view_interpro_frequency)
        if os.getcwd() != xlib.get_docker_toa_dir():
            self.menu_toa_interpro_stats.add_command(label='Frequency distribution plot', command=self.plot_interpro_frequency)
        self.menu_toa_interpro_stats.add_separator()
        self.menu_toa_interpro_stats.add_command(label='# sequences per # ids data', command=self.view_seq_per_interpro_data)
        if os.getcwd() != xlib.get_docker_toa_dir():
            self.menu_toa_interpro_stats.add_command(label='# sequences per # ids plot', command=self.plot_seq_per_interpro_data)

        # create "menu_toa_kegg_stats" and add its menu items
        self.menu_toa_kegg_stats = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_kegg_stats.add_command(label='Frequency distribution data', command=self.view_kegg_frequency)
        if os.getcwd() != xlib.get_docker_toa_dir():
            self.menu_toa_kegg_stats.add_command(label='Frequency distribution plot', command=self.plot_kegg_frequency)
        self.menu_toa_kegg_stats.add_separator()
        self.menu_toa_kegg_stats.add_command(label='# sequences per # ids data', command=self.view_seq_per_kegg_data)
        if os.getcwd() != xlib.get_docker_toa_dir():
            self.menu_toa_kegg_stats.add_command(label='# sequences per # ids plot', command=self.plot_seq_per_kegg_data)

        # create "menu_toa_mapman_stats" and add its menu items
        self.menu_toa_mapman_stats = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_mapman_stats.add_command(label='Frequency distribution data', command=self.view_mapman_frequency)
        if os.getcwd() != xlib.get_docker_toa_dir():
            self.menu_toa_mapman_stats.add_command(label='Frequency distribution plot', command=self.plot_mapman_frequency)
        self.menu_toa_mapman_stats.add_separator()
        self.menu_toa_mapman_stats.add_command(label='# sequences per # ids data', command=self.view_seq_per_mapman_data)
        if os.getcwd() != xlib.get_docker_toa_dir():
            self.menu_toa_mapman_stats.add_command(label='# sequences per # ids plot', command=self.plot_seq_per_mapman_data)

        # create "menu_toa_metacyc_stats" and add its menu items
        self.menu_toa_metacyc_stats = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_metacyc_stats.add_command(label='Distribution data', command=self.view_metacyc_frequency)
        if os.getcwd() != xlib.get_docker_toa_dir():
            self.menu_toa_metacyc_stats.add_command(label='Distribution plot', command=self.plot_metacyc_frequency)
        self.menu_toa_metacyc_stats.add_separator()
        self.menu_toa_metacyc_stats.add_command(label='# sequences per # ids data', command=self.view_seq_per_metacyc_data)
        if os.getcwd() != xlib.get_docker_toa_dir():
            self.menu_toa_metacyc_stats.add_command(label='# sequences per # ids plot', command=self.plot_seq_per_metacyc_data)

        # create "menu_toa_stats" and add its menu items
        self.menu_toa_stats = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_toa_stats.add_cascade(label='Alignment', menu=self.menu_toa_alignment_stats)
        self.menu_toa_stats.add_separator()
        self.menu_toa_stats.add_cascade(label='Annotation datasets', menu=self.menu_toa_annotation_dataset_stats)
        self.menu_toa_stats.add_separator()
        self.menu_toa_stats.add_cascade(label='Species', menu=self.menu_toa_species_stats)
        self.menu_toa_stats.add_cascade(label='Family', menu=self.menu_toa_family_stats)
        self.menu_toa_stats.add_cascade(label='Phylum', menu=self.menu_toa_phylum_stats)
        self.menu_toa_stats.add_separator()
        self.menu_toa_stats.add_cascade(label='EC', menu=self.menu_toa_ec_stats)
        self.menu_toa_stats.add_cascade(label='Gene Ontology', menu=self.menu_toa_go_stats)
        self.menu_toa_stats.add_cascade(label='InterPro', menu=self.menu_toa_interpro_stats)
        self.menu_toa_stats.add_cascade(label='KEGG', menu=self.menu_toa_kegg_stats)
        self.menu_toa_stats.add_cascade(label='MapMan', menu=self.menu_toa_mapman_stats)
        self.menu_toa_stats.add_cascade(label='MetaCyc', menu=self.menu_toa_metacyc_stats)

        # link "menu_toa_statistics" to "menu_bar"
        self.menu_bar.add_cascade(label='Statistics', menu=self.menu_toa_stats)

        # create "menu_logs" add add its menu items
        self.menu_logs = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_logs.add_command(label='View submission logs', command=self.view_submission_logs)
        self.menu_logs.add_separator()
        self.menu_logs.add_command(label='View result logs', command=self.view_result_logs)

        # link "menu_toa_pipelines" to "menu_bar"
        self.menu_bar.add_cascade(label='Logs', menu=self.menu_logs)

        # create "menu_help" add add its menu items
        self.initial_menu_help = tkinter.Menu(self.menu_bar, tearoff=0)
        self.initial_menu_help.add_command(label='View help', command=self.open_help, accelerator='F1')
        self.initial_menu_help.add_separator()
        self.initial_menu_help.add_command(label='About...', command=self.show_dialog_about)

        # link "menu_help" with "menu_bar"
        self.menu_bar.add_cascade(label='Help', menu=self.initial_menu_help)

        #  assign "initial_menu_bar" as the window menu
        self.root.config(menu=self.menu_bar)

        # create "frame_toolbar" and register it in "Main" with the grid geometry manager
        self.frame_toolbar = tkinter.Frame(self.root, borderwidth=1, relief='raised')
        self.frame_toolbar.grid(row=0, column=0, sticky='ew')

        # create and register "button_exit" in "frame_toolbar" with the pack geometry manager
        self.button_exit = tkinter.Button(self.frame_toolbar, command=self.exit, relief='flat', image=imagetk_exit)
        self.button_exit.image = imagetk_exit
        self.button_exit.pack(side='left', padx=2, pady=5)

        # create "frame_information" and register it in "Main" with the grid geometry manager
        self.frame_information = tkinter.Frame(self.root, borderwidth=1, relief='raised')
        self.frame_information.grid(row=1, column=0, sticky='ew')

        # create "label_process" and register it in "frame_information" with the pack geometry manager
        self.label_process = tkinter.Label(self.frame_information, text='')
        self.label_process.pack(side='right', padx=(0,10))

        # create "container" and register it in "Main" with the grid geometry manager
        self.container = tkinter.Frame(self.root)
        self.container.grid(row=2, column=0, sticky='nsew')

        # link a handler to events
        self.root.bind('<F1>', self.open_help)
        self.root.bind('<Alt-F4>', self.exit)

        # link a handler to interactions between the application and the window manager
        self.root.protocol('WM_DELETE_WINDOW', self.exit)

    #---------------

    def install_miniconda3(self):
        '''
        Install the Miniconda3 in the cluster.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_install_miniconda3" in "container" with the grid geometry manager
        form_install_miniconda3 = gbioinfoapp.FormInstallBioinfoApp(self, app=xlib.get_miniconda3_code())
        form_install_miniconda3.grid(row=0, column=0, sticky='nsew')

        # set "form_install_miniconda3" as current form and add it in the forms dictionary
        self.current_form = 'form_install_miniconda3'
        self.forms_dict[self.current_form] = form_install_miniconda3

        # raise "form_install_miniconda3" to front
        form_install_miniconda3.tkraise()

    #---------------

    def install_blastplus(self):
        '''
        Install the BLAST+ in the cluster.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_install_blastplus" in "container" with the grid geometry manager
        form_install_blastplus = gbioinfoapp.FormInstallBioinfoApp(self, app=xlib.get_blastplus_code())
        form_install_blastplus.grid(row=0, column=0, sticky='nsew')

        # set "form_install_blastplus" as current form and add it in the forms dictionary
        self.current_form = 'form_install_blastplus'
        self.forms_dict[self.current_form] = form_install_blastplus

        # raise "form_install_blastplus" to front
        form_install_blastplus.tkraise()

    #---------------

    def install_diamond(self):
        '''
        Install the DIAMOND in the cluster.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_install_diamond" in "container" with the grid geometry manager
        form_install_diamond = gbioinfoapp.FormInstallBioinfoApp(self, app=xlib.get_diamond_code())
        form_install_diamond.grid(row=0, column=0, sticky='nsew')

        # set "form_install_diamond" as current form and add it in the forms dictionary
        self.current_form = 'form_install_diamond'
        self.forms_dict[self.current_form] = form_install_diamond

        # raise "form_install_diamond" to front
        form_install_diamond.tkraise()

    #---------------

    def install_entrez_direct(self):
        '''
        Install the Entrez Direct software in the cluster.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_install_entrez_direct" in "container" with the grid geometry manager
        form_install_entrez_direct = gbioinfoapp.FormInstallBioinfoApp(self, app=xlib.get_entrez_direct_code())
        form_install_entrez_direct.grid(row=0, column=0, sticky='nsew')

        # set "form_install_entrez_direct" as current form and add it in the forms dictionary
        self.current_form = 'form_install_entrez_direct'
        self.forms_dict[self.current_form] = form_install_entrez_direct

        # raise "form_install_entrez_direct" to front
        form_install_entrez_direct.tkraise()

    #---------------

    def install_r(self):
        '''
        Install the R in the cluster.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_install_r" in "container" with the grid geometry manager
        form_install_r = gbioinfoapp.FormInstallBioinfoApp(self, app=xlib.get_r_code())
        form_install_r.grid(row=0, column=0, sticky='nsew')

        # set "form_install_r" as current form and add it in the forms dictionary
        self.current_form = 'form_install_r'
        self.forms_dict[self.current_form] = form_install_r

        # raise "form_install_r" to front
        form_install_r.tkraise()

    #---------------

    def install_transdecoder(self):
        '''
        Install the TransDecoder software in the cluster.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_install_transdecoder" in "container" with the grid geometry manager
        form_install_transdecoder = gbioinfoapp.FormInstallBioinfoApp(self, app=xlib.get_transdecoder_code())
        form_install_transdecoder.grid(row=0, column=0, sticky='nsew')

        # set "form_install_transdecoder" as current form and add it in the forms dictionary
        self.current_form = 'form_install_transdecoder'
        self.forms_dict[self.current_form] = form_install_transdecoder

        # raise "form_install_transdecoder" to front
        form_install_transdecoder.tkraise()

    #---------------

    def recreate_toa_config_file(self):
        '''
        Recreate the TOA config file.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_recreate_toa_config_file" in "container" with the grid geometry manager
        form_recreate_toa_config_file = gtoa.FormRecreateToaConfigFile(self)
        form_recreate_toa_config_file.grid(row=0, column=0, sticky='nsew')

        # set "form_recreate_toa_config_file" as current form and add it in the forms dictionary
        self.current_form = 'form_create_toa_config_file'
        self.forms_dict[self.current_form] = form_recreate_toa_config_file

        # raise "form_recreate_toa_config_file" to front
        form_recreate_toa_config_file.tkraise()

    #---------------

    def view_toa_config_file(self):
        '''
        List the TOA config file.
        '''

        # close the current form
        self.close_current_form()

        # get the TOA config file
        toa_config_file = xtoa.get_toa_config_file()

        # create and show a instance DialogViewer to view the TOA config file
        dialog_viewer = gdialogs.DialogViewer(self.root, toa_config_file)
        self.root.wait_window(dialog_viewer)

    #---------------

    def recreate_toa_database(self):
        '''
        Recreate the TOA database.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_recreate_toa_database" in "container" with the grid geometry manager
        form_recreate_toa_database = gtoa.FormManageToaDatabase(self, process_type=xlib.get_toa_type_recreate())
        form_recreate_toa_database.grid(row=0, column=0, sticky='nsew')

        # set "form_recreate_toa_database" as current form and add it in the forms dictionary
        self.current_form = 'form_create_toa_config_file'
        self.forms_dict[self.current_form] = form_recreate_toa_database

        # raise "form_recreate_toa_database" to front
        form_recreate_toa_database.tkraise()

    #---------------

    def rebuild_toa_database(self):
        '''
        Rebuild the TOA database.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_rebuild_toa_database" in "container" with the grid geometry manager
        form_rebuild_toa_database = gtoa.FormManageToaDatabase(self, process_type=xlib.get_toa_type_rebuild())
        form_rebuild_toa_database.grid(row=0, column=0, sticky='nsew')

        # set "form_rebuild_toa_database" as current form and add it in the forms dictionary
        self.current_form = 'form_create_toa_config_file'
        self.forms_dict[self.current_form] = form_rebuild_toa_database

        # raise "form_rebuild_toa_database" to front
        form_rebuild_toa_database.tkraise()

    #---------------

    def recreate_dataset_file(self):
        '''
        Recreate the file of datasets.
        '''

        # initialize the control variable
        OK = True

        # close the current form
        self.close_current_form()

        # set the head
        head = f'{xlib.get_toa_name()} - Recreate file of datasets'

        # confirm the creation of the file of datasets
        message = f'The file {xtoa.get_dataset_file()} is going to be recreated. The previous file will be lost.\n\nAre you sure to continue?'
        OK = tkinter.messagebox.askyesno(f'{xlib.get_short_project_name()} - {head}', message)

        # recreate the file of datasets
        if OK:
            (OK, error_list) = xtoa.create_dataset_file()
            if not OK:
                message = ''
                for error in error_list:
                    message = f'{message}{error}\n'
                tkinter.messagebox.showerror(f'{xlib.get_short_project_name()} - {head}', message)

        # edit the file of datasets
        if OK:

            # edit the data file using "DialogEditor" 
            dialog_editor = gdialogs.DialogEditor(self.root, xtoa.get_dataset_file())
            self.root.wait_window(dialog_editor)

            # check the data file
            (OK, error_list) = xtoa.check_dataset_file(strict=False)
            if OK:
                message = f'The file {xtoa.get_dataset_file()} is OK.'
                tkinter.messagebox.showinfo(f'{xlib.get_short_project_name()} - {head}', message)
            else:
                message = 'Detected errors:\n\n'
                for error in error_list:
                    message = f'{message}{error}\n'
                tkinter.messagebox.showerror(f'{xlib.get_short_project_name()} - {head}', message)

    #---------------

    def edit_dataset_file(self):
        '''
        Edit the file of datasets.
        '''

        # initialize the control variable
        OK = True

        # close the current form
        self.close_current_form()

        # set the head
        head = f'{xlib.get_toa_name()} - Edit file of datasets'

        # edit the file of datasets using "DialogEditor" 
        dialog_editor = gdialogs.DialogEditor(self.root, xtoa.get_dataset_file())
        self.root.wait_window(dialog_editor)

        # check the file of datasets
        (OK, error_list) = xtoa.check_dataset_file(strict=False)
        if OK:
            message = f'The file {xtoa.get_dataset_file()} is OK.'
            tkinter.messagebox.showinfo(f'{xlib.get_short_project_name()} - {head}', message)
        else:
            message = 'Detected errors:\n\n'
            for error in error_list:
                message = f'{message}{error}\n'
            tkinter.messagebox.showerror(f'{xlib.get_short_project_name()} - {head}', message)

    #---------------

    def recreate_species_file(self):
        '''
        Recreate the file of species.
        '''

        # initialize the control variable
        OK = True

        # close the current form
        self.close_current_form()

        # set the head
        head = f'{xlib.get_toa_name()} - Recreate file of species'

        # confirm the creation of the file of species
        message = f'The file {xtoa.get_species_file()} is going to be recreated. The previous file will be lost.\n\nAre you sure to continue?'
        OK = tkinter.messagebox.askyesno(f'{xlib.get_short_project_name()} - {head}', message)

        # recreate the file of species
        if OK:
            (OK, error_list) = xtoa.create_species_file()
            if not OK:
                message = ''
                for error in error_list:
                    message = f'{message}{error}\n'
                tkinter.messagebox.showerror(f'{xlib.get_short_project_name()} - {head}', message)

        # edit the file of species
        if OK:

            # edit the data file using "DialogEditor" 
            dialog_editor = gdialogs.DialogEditor(self.root, xtoa.get_species_file())
            self.root.wait_window(dialog_editor)

            # check the data file
            (OK, error_list) = xtoa.check_species_file(strict=False)
            if OK:
                message = f'The file {xtoa.get_species_file()} is OK.'
                tkinter.messagebox.showinfo(f'{xlib.get_short_project_name()} - {head}', message)
            else:
                message = 'Detected errors:\n\n'
                for error in error_list:
                    message = f'{message}{error}\n' 
                tkinter.messagebox.showerror(f'{xlib.get_short_project_name()} - {head}', message)

    #---------------

    def edit_species_file(self):
        '''
        Edit the file of species.
        '''

        # initialize the control variable
        OK = True

        # close the current form
        self.close_current_form()

        # set the head
        head = f'{xlib.get_toa_name()} - Edit file of species'.format()

        # edit the file of species using "DialogEditor" 
        dialog_editor = gdialogs.DialogEditor(self.root, xtoa.get_species_file())
        self.root.wait_window(dialog_editor)

        # check the file of species
        (OK, error_list) = xtoa.check_species_file(strict=False)
        if OK:
            message = f'The file {xtoa.get_species_file()} is OK.'
            tkinter.messagebox.showinfo(f'{xlib.get_short_project_name()} - {head}', message)
        else:
            message = 'Detected errors:\n\n'
            for error in error_list:
                message = f'{message}{error}\n' 
            tkinter.messagebox.showerror(f'{xlib.get_short_project_name()} - {head}', message)

    #---------------

    def download_basic_data(self):
        '''
        Download other basic data.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_download_basic_data" in "container" with the grid geometry manager
        form_download_basic_data = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_download_data(), genomic_database=xlib.get_toa_data_basic_data_code())
        form_download_basic_data.grid(row=0, column=0, sticky='nsew')

        # set "form_download_basic_data" as current form and add it in the forms dictionary
        self.current_form = 'form_download_basic_data'
        self.forms_dict[self.current_form] = form_download_basic_data

        # raise "form_download_basic_data" to front
        form_download_basic_data.tkraise()

    #---------------

    def load_basic_data(self):
        '''
        Load basic data into TOA database.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_load_basic_data" in "container" with the grid geometry manager
        form_load_basic_data = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_load_data(), genomic_database=xlib.get_toa_data_basic_data_code())
        form_load_basic_data.grid(row=0, column=0, sticky='nsew')

        # set "form_load_basic_data" as current form and add it in the forms dictionary
        self.current_form = 'form_load_basic_data'
        self.forms_dict[self.current_form] = form_load_basic_data

        # raise "form_load_basic_data" to front
        form_load_basic_data.tkraise()

    #---------------

    def build_gymno_01_proteome(self):
        '''
        Build the Gymno PLAZA 1.0 proteome.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_build_gymno_01_proteome" in "container" with the grid geometry manager
        form_build_gymno_01_proteome = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_build_proteome(), genomic_database=xlib.get_toa_data_gymno_01_code())
        form_build_gymno_01_proteome.grid(row=0, column=0, sticky='nsew')

        # set "form_build_gymno_01_proteome" as current form and add it in the forms dictionary
        self.current_form = 'form_build_gymno_01_proteome'
        self.forms_dict[self.current_form] = form_build_gymno_01_proteome

        # raise "form_build_gymno_01_proteome" to front
        form_build_gymno_01_proteome.tkraise()

    #---------------

    def download_gymno_01_data(self):
        '''
        Download Gymno PLAZA 1.0 functional annotation.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_download_gymno_01_data" in "container" with the grid geometry manager
        form_download_gymno_01_data = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_download_data(), genomic_database=xlib.get_toa_data_gymno_01_code())
        form_download_gymno_01_data.grid(row=0, column=0, sticky='nsew')

        # set "form_download_gymno_01_data" as current form and add it in the forms dictionary
        self.current_form = 'form_download_gymno_01_data'
        self.forms_dict[self.current_form] = form_download_gymno_01_data

        # raise "form_download_gymno_01_data" to front
        form_download_gymno_01_data.tkraise()

    #---------------

    def load_gymno_01_data(self):
        '''
        Load Gymno PLAZA 1.0 data into TOA database.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_load_gymno_01_data" in "container" with the grid geometry manager
        form_load_gymno_01_data = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_load_data(), genomic_database=xlib.get_toa_data_gymno_01_code())
        form_load_gymno_01_data.grid(row=0, column=0, sticky='nsew')

        # set "form_load_gymno_01_data" as current form and add it in the forms dictionary
        self.current_form = 'form_load_gymno_01_data'
        self.forms_dict[self.current_form] = form_load_gymno_01_data

        # raise "form_load_gymno_01_data" to front
        form_load_gymno_01_data.tkraise()

    #---------------

    def build_dicots_04_proteome(self):
        '''
        Build the Dicots PLAZA 4.0 proteome.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_build_dicots_04_proteome" in "container" with the grid geometry manager
        form_build_dicots_04_proteome = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_build_proteome(), genomic_database=xlib.get_toa_data_dicots_04_code())
        form_build_dicots_04_proteome.grid(row=0, column=0, sticky='nsew')

        # set "form_build_dicots_04_proteome" as current form and add it in the forms dictionary
        self.current_form = 'form_build_dicots_04_proteome'
        self.forms_dict[self.current_form] = form_build_dicots_04_proteome

        # raise "form_build_dicots_04_proteome" to front
        form_build_dicots_04_proteome.tkraise()

    #---------------

    def download_dicots_04_data(self):
        '''
        Download Dicots PLAZA 4.0 functional annotation.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_download_dicots_04_data" in "container" with the grid geometry manager
        form_download_dicots_04_data = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_download_data(), genomic_database=xlib.get_toa_data_dicots_04_code())
        form_download_dicots_04_data.grid(row=0, column=0, sticky='nsew')

        # set "form_download_dicots_04_data" as current form and add it in the forms dictionary
        self.current_form = 'form_download_dicots_04_data'
        self.forms_dict[self.current_form] = form_download_dicots_04_data

        # raise "form_download_dicots_04_data" to front
        form_download_dicots_04_data.tkraise()

    #---------------

    def load_dicots_04_data(self):
        '''
        Load Dicots PLAZA 4.0 data into TOA database.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_load_dicots_04_data" in "container" with the grid geometry manager
        form_load_dicots_04_data = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_load_data(), genomic_database=xlib.get_toa_data_dicots_04_code())
        form_load_dicots_04_data.grid(row=0, column=0, sticky='nsew')

        # set "form_load_dicots_04_data" as current form and add it in the forms dictionary
        self.current_form = 'form_load_dicots_04_data'
        self.forms_dict[self.current_form] = form_load_dicots_04_data

        # raise "form_load_dicots_04_data" to front
        form_load_dicots_04_data.tkraise()

    #---------------

    def build_monocots_04_proteome(self):
        '''
        Build the Monocots PLAZA 4.0 proteome.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_build_monocots_04_proteome" in "container" with the grid geometry manager
        form_build_monocots_04_proteome = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_build_proteome(), genomic_database=xlib.get_toa_data_monocots_04_code())
        form_build_monocots_04_proteome.grid(row=0, column=0, sticky='nsew')

        # set "form_build_monocots_04_proteome" as current form and add it in the forms dictionary
        self.current_form = 'form_build_monocots_04_proteome'
        self.forms_dict[self.current_form] = form_build_monocots_04_proteome

        # raise "form_build_monocots_04_proteome" to front
        form_build_monocots_04_proteome.tkraise()

    #---------------

    def download_monocots_04_data(self):
        '''
        Download Monocots PLAZA 4.0 functional annotation.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_download_monocots_04_data" in "container" with the grid geometry manager
        form_download_monocots_04_data = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_download_data(), genomic_database=xlib.get_toa_data_monocots_04_code())
        form_download_monocots_04_data.grid(row=0, column=0, sticky='nsew')

        # set "form_download_monocots_04_data" as current form and add it in the forms dictionary
        self.current_form = 'form_download_monocots_04_data'
        self.forms_dict[self.current_form] = form_download_monocots_04_data

        # raise "form_download_monocots_04_data" to front
        form_download_monocots_04_data.tkraise()

    #---------------

    def load_monocots_04_data(self):
        '''
        Load Monocots PLAZA 4.0 data into TOA database.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_load_monocots_04_data" in "container" with the grid geometry manager
        form_load_monocots_04_data = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_load_data(), genomic_database=xlib.get_toa_data_monocots_04_code())
        form_load_monocots_04_data.grid(row=0, column=0, sticky='nsew')

        # set "form_load_monocots_04_data" as current form and add it in the forms dictionary
        self.current_form = 'form_load_monocots_04_data'
        self.forms_dict[self.current_form] = form_load_monocots_04_data

        # raise "form_load_monocots_04_data" to front
        form_load_monocots_04_data.tkraise()

    #---------------

    def build_refseq_plant_proteome(self):
        '''
        Build the NCBI RefSeq Plant proteome.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_build_refseq_plant_proteome" in "container" with the grid geometry manager
        form_build_refseq_plant_proteome = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_build_proteome(), genomic_database=xlib.get_toa_data_refseq_plant_code())
        form_build_refseq_plant_proteome.grid(row=0, column=0, sticky='nsew')

        # set "form_build_refseq_plant_proteome" as current form and add it in the forms dictionary
        self.current_form = 'form_build_refseq_plant_proteome'
        self.forms_dict[self.current_form] = form_build_refseq_plant_proteome

        # raise "form_build_refseq_plant_proteome" to front
        form_build_refseq_plant_proteome.tkraise()

    #---------------

    def download_taxonomy_data(self):
        '''
        Download NCBI Taxonomy data.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_download_taxonomy_data" in "container" with the grid geometry manager
        form_download_taxonomy_data = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_download_data(), genomic_database=xlib.get_toa_data_taxonomy_code())
        form_download_taxonomy_data.grid(row=0, column=0, sticky='nsew')

        # set "form_download_taxonomy_data" as current form and add it in the forms dictionary
        self.current_form = 'form_download_taxonomy_data'
        self.forms_dict[self.current_form] = form_download_taxonomy_data

        # raise "form_download_taxonomy_data" to front
        form_download_taxonomy_data.tkraise()

    #---------------

    def build_blastplus_nt_db(self):
        '''
        Build the NCBI BLAST database NT for BLAST+.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_build_blastplus_nt_db" in "container" with the grid geometry manager
        form_build_blastplus_nt_db = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_build_blastplus_db(), genomic_database=xlib.get_toa_data_nt_code())
        form_build_blastplus_nt_db.grid(row=0, column=0, sticky='nsew')

        # set "form_build_blastplus_nt_db" as current form and add it in the forms dictionary
        self.current_form = 'form_build_blastplus_nt_db'
        self.forms_dict[self.current_form] = form_build_blastplus_nt_db

        # raise "form_build_blastplus_nt_db" to front
        form_build_blastplus_nt_db.tkraise()

    #---------------

    def build_viridiplantae_nucleotide_gi_gilist(self):
        '''
        Build the NCBI Nucleotide GenInfo viridiplantae identifier list.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_build_viridiplantae_nucleotide_gi_gilist" in "container" with the grid geometry manager
        form_build_viridiplantae_nucleotide_gi_gilist = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_build_gilist(), genomic_database=xlib.get_toa_data_viridiplantae_nucleotide_gi_code())
        form_build_viridiplantae_nucleotide_gi_gilist.grid(row=0, column=0, sticky='nsew')

        # set "form_build_viridiplantae_nucleotide_gi_gilist" as current form and add it in the forms dictionary
        self.current_form = 'form_build_viridiplantae_nucleotide_gi_gilist'
        self.forms_dict[self.current_form] = form_build_viridiplantae_nucleotide_gi_gilist

        # raise "form_build_viridiplantae_nucleotide_gi_gilist" to front
        form_build_viridiplantae_nucleotide_gi_gilist.tkraise()

    #---------------

    def build_blastplus_nr_db(self):
        '''
        Build the NCBI BLAST database NR for BLAST+.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_build_blastplus_nr_db" in "container" with the grid geometry manager
        form_build_blastplus_nr_db = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_build_blastplus_db(), genomic_database=xlib.get_toa_data_nr_code())
        form_build_blastplus_nr_db.grid(row=0, column=0, sticky='nsew')

        # set "form_build_blastplus_nr_db" as current form and add it in the forms dictionary
        self.current_form = 'form_build_blastplus_nr_db'
        self.forms_dict[self.current_form] = form_build_blastplus_nr_db

        # raise "form_build_blastplus_nr_db" to front
        form_build_blastplus_nr_db.tkraise()

    #---------------

    def build_diamond_nr_db(self):
        '''
        Build the NCBI BLAST database NR for DIAMOND.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_build_diamond_nr_db" in "container" with the grid geometry manager
        form_build_diamond_nr_db = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_build_diamond_db(), genomic_database=xlib.get_toa_data_nr_code())
        form_build_diamond_nr_db.grid(row=0, column=0, sticky='nsew')

        # set "form_build_diamond_nr_db" as current form and add it in the forms dictionary
        self.current_form = 'form_build_diamond_nr_db'
        self.forms_dict[self.current_form] = form_build_diamond_nr_db

        # raise "form_build_diamond_nr_db" to front
        form_build_diamond_nr_db.tkraise()

    #---------------

    def build_viridiplantae_protein_gi_gilist(self):
        '''
        Build the NCBI Protein GenInfo viridiplantae identifier list.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_build_viridiplantae_protein_gi_gilist" in "container" with the grid geometry manager
        form_build_viridiplantae_protein_gi_gilist = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_build_gilist(), genomic_database=xlib.get_toa_data_viridiplantae_protein_gi_code())
        form_build_viridiplantae_protein_gi_gilist.grid(row=0, column=0, sticky='nsew')

        # set "form_build_viridiplantae_protein_gi_gilist" as current form and add it in the forms dictionary
        self.current_form = 'form_build_viridiplantae_protein_gi_gilist'
        self.forms_dict[self.current_form] = form_build_viridiplantae_protein_gi_gilist

        # raise "form_build_viridiplantae_protein_gi_gilist" to front
        form_build_viridiplantae_protein_gi_gilist.tkraise()

    #---------------

    def download_gene_data(self):
        '''
        Download NCBI Gene functional annotation.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_download_gene_data" in "container" with the grid geometry manager
        form_download_gene_data = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_download_data(), genomic_database=xlib.get_toa_data_gene_code())
        form_download_gene_data.grid(row=0, column=0, sticky='nsew')

        # set "form_download_gene_data" as current form and add it in the forms dictionary
        self.current_form = 'form_download_gene_data'
        self.forms_dict[self.current_form] = form_download_gene_data

        # raise "form_download_gene_data" to front
        form_download_gene_data.tkraise()

    #---------------

    def load_gene_data(self):
        '''
        Load NCBI Gene data into TOA database.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_load_gene_data" in "container" with the grid geometry manager
        form_load_gene_data = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_load_data(), genomic_database=xlib.get_toa_data_gene_code())
        form_load_gene_data.grid(row=0, column=0, sticky='nsew')

        # set "form_load_gene_data" as current form and add it in the forms dictionary
        self.current_form = 'form_load_gene_data'
        self.forms_dict[self.current_form] = form_load_gene_data

        # raise "form_load_gene_data" to front
        form_load_gene_data.tkraise()

    #---------------

    def download_interpro_data(self):
        '''
        Download InterPro functional annotation.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_download_interpro_data" in "container" with the grid geometry manager
        form_download_interpro_data = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_download_data(), genomic_database=xlib.get_toa_data_interpro_code())
        form_download_interpro_data.grid(row=0, column=0, sticky='nsew')

        # set "form_download_interpro_data" as current form and add it in the forms dictionary
        self.current_form = 'form_download_interpro_data'
        self.forms_dict[self.current_form] = form_download_interpro_data

        # raise "form_download_interpro_data" to front
        form_download_interpro_data.tkraise()

    #---------------

    def load_interpro_data(self):
        '''
        Load InterPro data into TOA database.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_load_interpro_data" in "container" with the grid geometry manager
        form_load_interpro_data = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_load_data(), genomic_database=xlib.get_toa_data_interpro_code())
        form_load_interpro_data.grid(row=0, column=0, sticky='nsew')

        # set "form_load_interpro_data" as current form and add it in the forms dictionary
        self.current_form = 'form_load_interpro_data'
        self.forms_dict[self.current_form] = form_load_interpro_data

        # raise "form_load_interpro_data" to front
        form_load_interpro_data.tkraise()

    #---------------

    def download_go_data(self):
        '''
        Download Gene Ontology functional annotation.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_download_go_data" in "container" with the grid geometry manager
        form_download_go_data = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_download_data(), genomic_database=xlib.get_toa_data_go_code())
        form_download_go_data.grid(row=0, column=0, sticky='nsew')

        # set "form_download_go_data" as current form and add it in the forms dictionary
        self.current_form = 'form_download_go_data'
        self.forms_dict[self.current_form] = form_download_go_data

        # raise "form_download_go_data" to front
        form_download_go_data.tkraise()

    #---------------

    def load_go_data(self):
        '''
        Load NCBI Gene Ontology into TOA database.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_load_go_data" in "container" with the grid geometry manager
        form_load_go_data = gtoa.FormManageGenomicDatabase(self, process_type=xlib.get_toa_type_load_data(), genomic_database=xlib.get_toa_data_go_code())
        form_load_go_data.grid(row=0, column=0, sticky='nsew')

        # set "form_load_go_data" as current form and add it in the forms dictionary
        self.current_form = 'form_load_go_data'
        self.forms_dict[self.current_form] = form_load_go_data

        # raise "form_load_go_data" to front
        form_load_go_data.tkraise()

    #---------------

    def recreate_nucleotide_pipeline_config_file(self):
        '''
        Recreate the nucleotide pipeline config file with the default options. It is necessary
        update the options in each process run.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_recreate_nucleotide_pipeline_config_file" in "container" with the grid geometry manager
        form_recreate_nucleotide_pipeline_config_file = gtoa.FormRecreatePipelineConfigFile(self, pipeline_type=xlib.get_toa_process_pipeline_nucleotide_code())
        form_recreate_nucleotide_pipeline_config_file.grid(row=0, column=0, sticky='nsew')

        # set "form_recreate_nucleotide_pipeline_config_file" as current form and add it in the forms dictionary
        self.current_form = 'form_recreate_nucleotide_pipeline_config_file'
        self.forms_dict[self.current_form] = form_recreate_nucleotide_pipeline_config_file

        # raise "form_recreate_nucleotide_pipeline_config_file" to front
        form_recreate_nucleotide_pipeline_config_file.tkraise()

    #---------------

    def edit_nucleotide_pipeline_config_file(self):
        '''
        Edit the nucleotide pipeline config file to change the parameters of process run.
        '''

        # initialize the control variable
        OK = True

        # close the current form
        self.close_current_form()

        # set the head
        head = f'{xlib.get_toa_process_pipeline_nucleotide_name()} - Edit config file'

        # edit the nucleotide pipeline config file using "DialogEditor" 
        dialog_editor = gdialogs.DialogEditor(self.root, xtoa.get_nucleotide_pipeline_config_file())
        self.root.wait_window(dialog_editor)

        # check the nucleotide pipeline config file
        (OK, error_list) = xtoa.check_pipeline_config_file(pipeline_type=xlib.get_toa_process_pipeline_nucleotide_code(), strict=False)
        if OK:
            message = f'The {xlib.get_toa_process_pipeline_nucleotide_name()} config file is OK.'
            tkinter.messagebox.showinfo(f'{xlib.get_short_project_name()} - {head}', message)
        else:
            message = 'Detected errors:\n\n'
            for error in error_list:
                message = f'{message}{error}\n' 
            tkinter.messagebox.showerror(f'{xlib.get_short_project_name()} - {head}', message)

    #---------------

    def run_nucleotide_pipeline_process(self):
        '''
        Run a nucleotide pipeline process corresponding to the options in nucleotide pipeline config file.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_run_nucleotide_pipeline_process" in "container" with the grid geometry manager
        form_run_nucleotide_pipeline_process = gtoa.FormRunPipelineProcess(self, pipeline_type=xlib.get_toa_process_pipeline_nucleotide_code())
        form_run_nucleotide_pipeline_process.grid(row=0, column=0, sticky='nsew')

        # set "form_run_nucleotide_pipeline_process" as current form and add it in the forms dictionary
        self.current_form = 'form_run_nucleotide_pipeline_process'
        self.forms_dict[self.current_form] = form_run_nucleotide_pipeline_process

        # raise "form_run_nucleotide_pipeline_process" to front
        form_run_nucleotide_pipeline_process.tkraise()

    #---------------

    def restart_nucleotide_pipeline_process(self):
        '''
        Restart a nucleotide pipeline process from the last step ended OK.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_restart_nucleotide_pipeline_process" in "container" with the grid geometry manager
        form_restart_nucleotide_pipeline_process = gtoa.FormRestartPipelineProcess(self, pipeline_type=xlib.get_toa_process_pipeline_nucleotide_code())
        form_restart_nucleotide_pipeline_process.grid(row=0, column=0, sticky='nsew')

        # set "form_restart_nucleotide_pipeline_process" as current form and add it in the forms dictionary
        self.current_form = 'form_restart_nucleotide_pipeline_process'
        self.forms_dict[self.current_form] = form_restart_nucleotide_pipeline_process

        # raise "form_restart_nucleotide_pipeline_process" to front
        form_restart_nucleotide_pipeline_process.tkraise()

    #---------------

    def recreate_aminoacid_pipeline_config_file(self):
        '''
        Recreate the amino acid pipeline config file with the default options. It is necessary
        update the options in each process run.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_recreate_aminoacid_pipeline_config_file" in "container" with the grid geometry manager
        form_recreate_aminoacid_pipeline_config_file = gtoa.FormRecreatePipelineConfigFile(self, pipeline_type=xlib.get_toa_process_pipeline_aminoacid_code())
        form_recreate_aminoacid_pipeline_config_file.grid(row=0, column=0, sticky='nsew')

        # set "form_recreate_aminoacid_pipeline_config_file" as current form and add it in the forms dictionary
        self.current_form = 'form_recreate_aminoacid_pipeline_config_file'
        self.forms_dict[self.current_form] = form_recreate_aminoacid_pipeline_config_file

        # raise "form_recreate_aminoacid_pipeline_config_file" to front
        form_recreate_aminoacid_pipeline_config_file.tkraise()

    #---------------

    def edit_aminoacid_pipeline_config_file(self):
        '''
        Edit the amino acid pipeline config file to change the parameters of process run.
        '''

        # initialize the control variable
        OK = True

        # close the current form
        self.close_current_form()

        # set the head
        head = f'{xlib.get_toa_process_pipeline_aminoacid_name()} - Edit config file'

        # edit the amino acid pipeline config file using "DialogEditor" 
        dialog_editor = gdialogs.DialogEditor(self.root, xtoa.get_aminoacid_pipeline_config_file())
        self.root.wait_window(dialog_editor)

        # check the amino acid pipeline config file
        (OK, error_list) = xtoa.check_pipeline_config_file(pipeline_type=xlib.get_toa_process_pipeline_aminoacid_code(), strict=False)
        if OK:
            message = f'The {xlib.get_toa_process_pipeline_aminoacid_name()} config file is OK.'
            tkinter.messagebox.showinfo(f'{xlib.get_short_project_name()} - {head}', message)
        else:
            message = 'Detected errors:\n\n'
            for error in error_list:
                message = f'{message}{error}\n' 
            tkinter.messagebox.showerror(f'{xlib.get_short_project_name()} - {head}', message)

    #---------------

    def run_aminoacid_pipeline_process(self):
        '''
        Run a amino acid pipeline process corresponding to the options in amino acid pipeline config file.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_run_aminoacid_pipeline_process" in "container" with the grid geometry manager
        form_run_aminoacid_pipeline_process = gtoa.FormRunPipelineProcess(self, pipeline_type=xlib.get_toa_process_pipeline_aminoacid_code())
        form_run_aminoacid_pipeline_process.grid(row=0, column=0, sticky='nsew')

        # set "form_run_aminoacid_pipeline_process" as current form and add it in the forms dictionary
        self.current_form = 'form_run_aminoacid_pipeline_process'
        self.forms_dict[self.current_form] = form_run_aminoacid_pipeline_process

        # raise "form_run_aminoacid_pipeline_process" to front
        form_run_aminoacid_pipeline_process.tkraise()

    #---------------

    def restart_aminoacid_pipeline_process(self):
        '''
        Restart a amino acid pipeline process from the last step ended OK.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_restart_aminoacid_pipeline_process" in "container" with the grid geometry manager
        form_restart_aminoacid_pipeline_process = gtoa.FormRestartPipelineProcess(self, pipeline_type=xlib.get_toa_process_pipeline_aminoacid_code())
        form_restart_aminoacid_pipeline_process.grid(row=0, column=0, sticky='nsew')

        # set "form_restart_aminoacid_pipeline_process" as current form and add it in the forms dictionary
        self.current_form = 'form_restart_aminoacid_pipeline_process'
        self.forms_dict[self.current_form] = form_restart_aminoacid_pipeline_process

        # raise "form_restart_aminoacid_pipeline_process" to front
        form_restart_aminoacid_pipeline_process.tkraise()

    #---------------

    def recreate_annotation_merger_config_file(self):
        '''
        Recreate the pipeline merger config file with the default options. It is necessary
        update the options in each process run.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_recreate_annotation_merger_config_file" in "container" with the grid geometry manager
        form_recreate_annotation_merger_config_file = gtoa.FormRecreateAnnotatioMergerConfigFile(self)
        form_recreate_annotation_merger_config_file.grid(row=0, column=0, sticky='nsew')

        # set "form_recreate_annotation_merger_config_file" as current form and add it in the forms dictionary
        self.current_form = 'form_recreate_annotation_merger_config_file'
        self.forms_dict[self.current_form] = form_recreate_annotation_merger_config_file

        # raise "form_recreate_annotation_merger_config_file" to front
        form_recreate_annotation_merger_config_file.tkraise()

    #---------------

    def edit_annotation_merger_config_file(self):
        '''
        Edit the pipeline merger config file to change the parameters of process run.
        '''

        # initialize the control variable
        OK = True

        # close the current form
        self.close_current_form()

        # set the head
        head = f'{xlib.get_toa_process_merge_annotations_name()} - Edit config file'

        # edit the pipeline merger config file using "DialogEditor" 
        dialog_editor = gdialogs.DialogEditor(self.root, xtoa.get_annotation_merger_config_file())
        self.root.wait_window(dialog_editor)

        # check the nucleotide pipeline config file
        (OK, error_list) = xtoa.check_annotation_merger_config_file(strict=False)
        if OK:
            message = f'The {xlib.get_toa_process_merge_annotations_name()} config file is OK.'
            tkinter.messagebox.showinfo(f'{xlib.get_short_project_name()} - {head}', message)
        else:
            message = 'Detected errors:\n\n'
            for error in error_list:
                message = f'{message}{error}\n' 
            tkinter.messagebox.showerror(f'{xlib.get_short_project_name()} - {head}', message)

    #---------------

    def run_annotation_merger_process(self):
        '''
        Run an annotation merger process corresponding to the options in nucleotide pipeline config file.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_run_annotation_merger_process" in "container" with the grid geometry manager
        form_run_annotation_merger_process = gtoa.FormRunPipelineProcess(self, pipeline_type=xlib.get_toa_process_merge_annotations_code())
        form_run_annotation_merger_process.grid(row=0, column=0, sticky='nsew')

        # set "form_run_annotation_merger_process" as current form and add it in the forms dictionary
        self.current_form = 'form_run_annotation_merger_process'
        self.forms_dict[self.current_form] = form_run_annotation_merger_process

        # raise "form_run_annotation_merger_process" to front
        form_run_annotation_merger_process.tkraise()

    #---------------

    def view_hit_per_hsp_data(self):
        '''
        View the # HITs per # HSPs data of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_view_hit_per_hsp_data" in "container" with the grid geometry manager
        form_view_hit_per_hsp_data = gtoa.FormViewStats(self, stats_code='hit_per_hsp')
        form_view_hit_per_hsp_data.grid(row=0, column=0, sticky='nsew')

        # set "form_view_hit_per_hsp_data" as current form and add it in the forms dictionary
        self.current_form = 'form_view_hit_per_hsp_data'
        self.forms_dict[self.current_form] = form_view_hit_per_hsp_data

        # raise "form_view_hit_per_hsp_data" to front
        form_view_hit_per_hsp_data.tkraise()

    #---------------

    def plot_hit_per_hsp_data(self):
        '''
        Plot the # HITs per # HSPs data of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_plot_dataset_frequency" in "container" with the grid geometry manager
        form_plot_dataset_frequency = gtoa.FormPlotStats(self, stats_code='hit_per_hsp')
        form_plot_dataset_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_plot_dataset_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_plot_dataset_frequency'
        self.forms_dict[self.current_form] = form_plot_dataset_frequency

        # raise "form_plot_dataset_frequency" to front
        form_plot_dataset_frequency.tkraise()

    #---------------

    def view_annotation_dataset_frequency(self):
        '''
        View the dataset frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_view_dataset_frequency" in "container" with the grid geometry manager
        form_view_dataset_frequency = gtoa.FormViewStats(self, stats_code='dataset')
        form_view_dataset_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_view_dataset_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_view_dataset_frequency'
        self.forms_dict[self.current_form] = form_view_dataset_frequency

        # raise "form_view_dataset_frequency" to front
        form_view_dataset_frequency.tkraise()

    #---------------

    def plot_annotation_dataset_frequency(self):
        '''
        Plot the dataset frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_plot_dataset_frequency" in "container" with the grid geometry manager
        form_plot_dataset_frequency = gtoa.FormPlotStats(self, stats_code='dataset')
        form_plot_dataset_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_plot_dataset_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_plot_dataset_frequency'
        self.forms_dict[self.current_form] = form_plot_dataset_frequency

        # raise "form_plot_dataset_frequency" to front
        form_plot_dataset_frequency.tkraise()

    #---------------

    def view_species_frequency(self):
        '''
        View the species frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_view_species_frequency" in "container" with the grid geometry manager
        form_view_species_frequency = gtoa.FormViewStats(self, stats_code='species')
        form_view_species_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_view_species_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_view_species_frequency'
        self.forms_dict[self.current_form] = form_view_species_frequency

        # raise "form_view_species_frequency" to front
        form_view_species_frequency.tkraise()

    #---------------

    def plot_species_frequency(self):
        '''
        Plot the species frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_plot_species_frequency" in "container" with the grid geometry manager
        form_plot_species_frequency = gtoa.FormPlotStats(self, stats_code='species')
        form_plot_species_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_plot_species_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_plot_species_frequency'
        self.forms_dict[self.current_form] = form_plot_species_frequency

        # raise "form_plot_species_frequency" to front
        form_plot_species_frequency.tkraise()

    #---------------

    def view_family_frequency(self):
        '''
        View the family frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_view_family_frequency" in "container" with the grid geometry manager
        form_view_family_frequency = gtoa.FormViewStats(self, stats_code='family')
        form_view_family_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_view_family_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_view_family_frequency'
        self.forms_dict[self.current_form] = form_view_family_frequency

        # raise "form_view_family_frequency" to front
        form_view_family_frequency.tkraise()

    #---------------

    def plot_family_frequency(self):
        '''
        Plot the family frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_plot_family_frequency" in "container" with the grid geometry manager
        form_plot_family_frequency = gtoa.FormPlotStats(self, stats_code='family')
        form_plot_family_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_plot_family_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_plot_family_frequency'
        self.forms_dict[self.current_form] = form_plot_family_frequency

        # raise "form_plot_family_frequency" to front
        form_plot_family_frequency.tkraise()

    #---------------

    def view_phylum_frequency(self):
        '''
        View the phylum frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_view_phylum_frequency" in "container" with the grid geometry manager
        form_view_phylum_frequency = gtoa.FormViewStats(self, stats_code='phylum')
        form_view_phylum_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_view_phylum_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_view_phylum_frequency'
        self.forms_dict[self.current_form] = form_view_phylum_frequency

        # raise "form_view_phylum_frequency" to front
        form_view_phylum_frequency.tkraise()

    #---------------

    def plot_phylum_frequency(self):
        '''
        Plot the phylum frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_plot_phylum_frequency" in "container" with the grid geometry manager
        form_plot_phylum_frequency = gtoa.FormPlotStats(self, stats_code='phylum')
        form_plot_phylum_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_plot_phylum_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_plot_phylum_frequency'
        self.forms_dict[self.current_form] = form_plot_phylum_frequency

        # raise "form_plot_phylum_frequency" to front
        form_plot_phylum_frequency.tkraise()

    #---------------

    def view_ec_frequency(self):
        '''
        View the EC frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_view_ec_frequency" in "container" with the grid geometry manager
        form_view_ec_frequency = gtoa.FormViewStats(self, stats_code='ec')
        form_view_ec_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_view_ec_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_view_ec_frequency'
        self.forms_dict[self.current_form] = form_view_ec_frequency

        # raise "form_view_ec_frequency" to front
        form_view_ec_frequency.tkraise()

    #---------------

    def plot_ec_frequency(self):
        '''
        Plot the EC frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_plot_ec_frequency" in "container" with the grid geometry manager
        form_plot_ec_frequency = gtoa.FormPlotStats(self, stats_code='ec')
        form_plot_ec_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_plot_ec_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_plot_ec_frequency'
        self.forms_dict[self.current_form] = form_plot_ec_frequency

        # raise "form_plot_ec_frequency" to front
        form_plot_ec_frequency.tkraise()

    #---------------

    def view_seq_per_ec_data(self):
        '''
        View the # sequences per # EC ids data of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_view_seq_per_ec_data" in "container" with the grid geometry manager
        form_view_seq_per_ec_data = gtoa.FormViewStats(self, stats_code='seq_per_ec')
        form_view_seq_per_ec_data.grid(row=0, column=0, sticky='nsew')

        # set "form_view_seq_per_ec_data" as current form and add it in the forms dictionary
        self.current_form = 'form_view_seq_per_ec_data'
        self.forms_dict[self.current_form] = form_view_seq_per_ec_data

        # raise "form_view_seq_per_ec_data" to front
        form_view_seq_per_ec_data.tkraise()

    #---------------

    def plot_seq_per_ec_data(self):
        '''
        Plot the # sequences per # EC ids data of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_plot_seq_per_ec_data" in "container" with the grid geometry manager
        form_plot_seq_per_ec_data = gtoa.FormPlotStats(self, stats_code='seq_per_ec')
        form_plot_seq_per_ec_data.grid(row=0, column=0, sticky='nsew')

        # set "form_plot_seq_per_ec_data" as current form and add it in the forms dictionary
        self.current_form = 'form_plot_seq_per_ec_data'
        self.forms_dict[self.current_form] = form_plot_seq_per_ec_data

        # raise "form_plot_seq_per_ec_data" to front
        form_plot_seq_per_ec_data.tkraise()

    #---------------

    def view_go_frequency(self):
        '''
        View the GO frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_view_go_frequency" in "container" with the grid geometry manager
        form_view_go_frequency = gtoa.FormViewStats(self, stats_code='go')
        form_view_go_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_view_go_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_view_go_frequency'
        self.forms_dict[self.current_form] = form_view_go_frequency

        # raise "form_view_go_frequency" to front
        form_view_go_frequency.tkraise()

    #---------------

    def plot_go_frequency(self):
        '''
        Plot the GO frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_plot_go_frequency" in "container" with the grid geometry manager
        form_plot_go_frequency = gtoa.FormPlotStats(self, stats_code='go')
        form_plot_go_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_plot_go_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_plot_go_frequency'
        self.forms_dict[self.current_form] = form_plot_go_frequency

        # raise "form_plot_go_frequency" to front
        form_plot_go_frequency.tkraise()

    #---------------

    def view_namespace_frequency(self):
        '''
        View the namespace frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_view_namespace_frequency" in "container" with the grid geometry manager
        form_view_namespace_frequency = gtoa.FormViewStats(self, stats_code='namespace')
        form_view_namespace_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_view_namespace_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_view_namespace_frequency'
        self.forms_dict[self.current_form] = form_view_namespace_frequency

        # raise "form_view_namespace_frequency" to front
        form_view_namespace_frequency.tkraise()

    #---------------

    def plot_namespace_frequency(self):
        '''
        Plot the GO frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_plot_namespace_frequency" in "container" with the grid geometry manager
        form_plot_namespace_frequency = gtoa.FormPlotStats(self, stats_code='namespace')
        form_plot_namespace_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_plot_namespace_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_plot_namespace_frequency'
        self.forms_dict[self.current_form] = form_plot_namespace_frequency

        # raise "form_plot_namespace_frequency" to front
        form_plot_namespace_frequency.tkraise()

    #---------------

    def view_seq_per_go_data(self):
        '''
        View the # sequences per # GO ids data of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_view_seq_per_go_data" in "container" with the grid geometry manager
        form_view_seq_per_go_data = gtoa.FormViewStats(self, stats_code='seq_per_go')
        form_view_seq_per_go_data.grid(row=0, column=0, sticky='nsew')

        # set "form_view_seq_per_go_data" as current form and add it in the forms dictionary
        self.current_form = 'form_view_seq_per_go_data'
        self.forms_dict[self.current_form] = form_view_seq_per_go_data

        # raise "form_view_seq_per_go_data" to front
        form_view_seq_per_go_data.tkraise()

    #---------------

    def plot_seq_per_go_data(self):
        '''
        Plot the # sequences per # GO ids data of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_plot_seq_per_go_data" in "container" with the grid geometry manager
        form_plot_seq_per_go_data = gtoa.FormPlotStats(self, stats_code='seq_per_go')
        form_plot_seq_per_go_data.grid(row=0, column=0, sticky='nsew')

        # set "form_plot_seq_per_go_data" as current form and add it in the forms dictionary
        self.current_form = 'form_plot_seq_per_go_data'
        self.forms_dict[self.current_form] = form_plot_seq_per_go_data

        # raise "form_plot_seq_per_go_data" to front
        form_plot_seq_per_go_data.tkraise()

    #---------------

    def view_interpro_frequency(self):
        '''
        View the InterPro frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_view_interpro_frequency" in "container" with the grid geometry manager
        form_view_interpro_frequency = gtoa.FormViewStats(self, stats_code='interpro')
        form_view_interpro_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_view_interpro_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_view_interpro_frequency'
        self.forms_dict[self.current_form] = form_view_interpro_frequency

        # raise "form_view_interpro_frequency" to front
        form_view_interpro_frequency.tkraise()

    #---------------

    def plot_interpro_frequency(self):
        '''
        Plot the InterPro frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_plot_interpro_frequency" in "container" with the grid geometry manager
        form_plot_interpro_frequency = gtoa.FormPlotStats(self, stats_code='interpro')
        form_plot_interpro_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_plot_interpro_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_plot_interpro_frequency'
        self.forms_dict[self.current_form] = form_plot_interpro_frequency

        # raise "form_plot_interpro_frequency" to front
        form_plot_interpro_frequency.tkraise()

    #---------------

    def view_seq_per_interpro_data(self):
        '''
        View the # sequences per # InterPro ids data of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_view_seq_per_interpro_data" in "container" with the grid geometry manager
        form_view_seq_per_interpro_data = gtoa.FormViewStats(self, stats_code='seq_per_interpro')
        form_view_seq_per_interpro_data.grid(row=0, column=0, sticky='nsew')

        # set "form_view_seq_per_interpro_data" as current form and add it in the forms dictionary
        self.current_form = 'form_view_seq_per_interpro_data'
        self.forms_dict[self.current_form] = form_view_seq_per_interpro_data

        # raise "form_view_seq_per_interpro_data" to front
        form_view_seq_per_interpro_data.tkraise()

    #---------------

    def plot_seq_per_interpro_data(self):
        '''
        Plot the # sequences per # InterPro ids data of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_plot_seq_per_interpro_data" in "container" with the grid geometry manager
        form_plot_seq_per_interpro_data = gtoa.FormPlotStats(self, stats_code='seq_per_interpro')
        form_plot_seq_per_interpro_data.grid(row=0, column=0, sticky='nsew')

        # set "form_plot_seq_per_interpro_data" as current form and add it in the forms dictionary
        self.current_form = 'form_plot_seq_per_interpro_data'
        self.forms_dict[self.current_form] = form_plot_seq_per_interpro_data

        # raise "form_plot_seq_per_interpro_data" to front
        form_plot_seq_per_interpro_data.tkraise()

    #---------------

    def view_kegg_frequency(self):
        '''
        View the KEGG frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_view_kegg_frequency" in "container" with the grid geometry manager
        form_view_kegg_frequency = gtoa.FormViewStats(self, stats_code='kegg')
        form_view_kegg_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_view_kegg_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_view_kegg_frequency'
        self.forms_dict[self.current_form] = form_view_kegg_frequency

        # raise "form_view_kegg_frequency" to front
        form_view_kegg_frequency.tkraise()

    #---------------

    def plot_kegg_frequency(self):
        '''
        Plot the KEGG frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_plot_kegg_frequency" in "container" with the grid geometry manager
        form_plot_kegg_frequency = gtoa.FormPlotStats(self, stats_code='kegg')
        form_plot_kegg_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_plot_kegg_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_plot_kegg_frequency'
        self.forms_dict[self.current_form] = form_plot_kegg_frequency

        # raise "form_plot_kegg_frequency" to front
        form_plot_kegg_frequency.tkraise()

    #---------------

    def view_seq_per_kegg_data(self):
        '''
        View the # sequences per # KEGG ids data of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_view_seq_per_kegg_data" in "container" with the grid geometry manager
        form_view_seq_per_kegg_data = gtoa.FormViewStats(self, stats_code='seq_per_kegg')
        form_view_seq_per_kegg_data.grid(row=0, column=0, sticky='nsew')

        # set "form_view_seq_per_kegg_data" as current form and add it in the forms dictionary
        self.current_form = 'form_view_seq_per_kegg_data'
        self.forms_dict[self.current_form] = form_view_seq_per_kegg_data

        # raise "form_view_seq_per_kegg_data" to front
        form_view_seq_per_kegg_data.tkraise()

    #---------------

    def plot_seq_per_kegg_data(self):
        '''
        Plot the # sequences per # KEGG ids data of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_plot_seq_per_kegg_data" in "container" with the grid geometry manager
        form_plot_seq_per_kegg_data = gtoa.FormPlotStats(self, stats_code='seq_per_kegg')
        form_plot_seq_per_kegg_data.grid(row=0, column=0, sticky='nsew')

        # set "form_plot_seq_per_kegg_data" as current form and add it in the forms dictionary
        self.current_form = 'form_plot_seq_per_kegg_data'
        self.forms_dict[self.current_form] = form_plot_seq_per_kegg_data

        # raise "form_plot_seq_per_kegg_data" to front
        form_plot_seq_per_kegg_data.tkraise()

    #---------------

    def view_mapman_frequency(self):
        '''
        View the MapMan frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_view_mapman_frequency" in "container" with the grid geometry manager
        form_view_mapman_frequency = gtoa.FormViewStats(self, stats_code='mapman')
        form_view_mapman_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_view_mapman_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_view_mapman_frequency'
        self.forms_dict[self.current_form] = form_view_mapman_frequency

        # raise "form_view_mapman_frequency" to front
        form_view_mapman_frequency.tkraise()

    #---------------

    def plot_mapman_frequency(self):
        '''
        Plot the MapMan frequency distribution of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_plot_mapman_frequency" in "container" with the grid geometry manager
        form_plot_mapman_frequency = gtoa.FormPlotStats(self, stats_code='mapman')
        form_plot_mapman_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_plot_mapman_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_plot_mapman_frequency'
        self.forms_dict[self.current_form] = form_plot_mapman_frequency

        # raise "form_plot_mapman_frequency" to front
        form_plot_mapman_frequency.tkraise()

    #---------------

    def view_seq_per_mapman_data(self):
        '''
        View the # sequences per # MapMan ids data of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_view_seq_per_mapman_data" in "container" with the grid geometry manager
        form_view_seq_per_mapman_data = gtoa.FormViewStats(self, stats_code='seq_per_mapman')
        form_view_seq_per_mapman_data.grid(row=0, column=0, sticky='nsew')

        # set "form_view_seq_per_mapman_data" as current form and add it in the forms dictionary
        self.current_form = 'form_view_seq_per_mapman_data'
        self.forms_dict[self.current_form] = form_view_seq_per_mapman_data

        # raise "form_view_seq_per_mapman_data" to front
        form_view_seq_per_mapman_data.tkraise()

    #---------------

    def plot_seq_per_mapman_data(self):
        '''
        Plot the # sequences per # MapMan ids data of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_plot_seq_per_mapman_data" in "container" with the grid geometry manager
        form_plot_seq_per_mapman_data = gtoa.FormPlotStats(self, stats_code='seq_per_mapman')
        form_plot_seq_per_mapman_data.grid(row=0, column=0, sticky='nsew')

        # set "form_plot_seq_per_mapman_data" as current form and add it in the forms dictionary
        self.current_form = 'form_plot_seq_per_mapman_data'
        self.forms_dict[self.current_form] = form_plot_seq_per_mapman_data

        # raise "form_plot_seq_per_mapman_data" to front
        form_plot_seq_per_mapman_data.tkraise()

    #---------------

    def view_metacyc_frequency(self):
        '''
        View the MetaCyc frequency of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_view_metacyc_frequency" in "container" with the grid geometry manager
        form_view_metacyc_frequency = gtoa.FormViewStats(self, stats_code='metacyc')
        form_view_metacyc_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_view_metacyc_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_view_metacyc_frequency'
        self.forms_dict[self.current_form] = form_view_metacyc_frequency

        # raise "form_view_metacyc_frequency" to front
        form_view_metacyc_frequency.tkraise()

    #---------------

    def plot_metacyc_frequency(self):
        '''
        Plot the MetaCyc frequency of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_plot_metacyc_frequency" in "container" with the grid geometry manager
        form_plot_metacyc_frequency = gtoa.FormPlotStats(self, stats_code='metacyc')
        form_plot_metacyc_frequency.grid(row=0, column=0, sticky='nsew')

        # set "form_plot_metacyc_frequency" as current form and add it in the forms dictionary
        self.current_form = 'form_plot_metacyc_frequency'
        self.forms_dict[self.current_form] = form_plot_metacyc_frequency

        # raise "form_plot_metacyc_frequency" to front
        form_plot_metacyc_frequency.tkraise()

    #---------------

    def view_seq_per_metacyc_data(self):
        '''
        View the # sequences per # MetaCyc ids data of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_view_seq_per_metacyc_data" in "container" with the grid geometry manager
        form_view_seq_per_metacyc_data = gtoa.FormViewStats(self, stats_code='seq_per_metacyc')
        form_view_seq_per_metacyc_data.grid(row=0, column=0, sticky='nsew')

        # set "form_view_seq_per_metacyc_data" as current form and add it in the forms dictionary
        self.current_form = 'form_view_seq_per_metacyc_data'
        self.forms_dict[self.current_form] = form_view_seq_per_metacyc_data

        # raise "form_view_seq_per_metacyc_data" to front
        form_view_seq_per_metacyc_data.tkraise()

    #---------------

    def plot_seq_per_metacyc_data(self):
        '''
        Plot the # sequences per # MetaCyc data of an annotation pipeline.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_plot_seq_per_metacyc_data" in "container" with the grid geometry manager
        form_plot_seq_per_metacyc_data = gtoa.FormPlotStats(self, stats_code='seq_per_metacyc')
        form_plot_seq_per_metacyc_data.grid(row=0, column=0, sticky='nsew')

        # set "form_plot_seq_per_metacyc_data" as current form and add it in the forms dictionary
        self.current_form = 'form_plot_seq_per_metacyc_data'
        self.forms_dict[self.current_form] = form_plot_seq_per_metacyc_data

        # raise "form_plot_seq_per_metacyc_data" to front
        form_plot_seq_per_metacyc_data.tkraise()

    #---------------

    def view_submission_logs(self):
        '''
        List logs of process submission in local computer.
        '''

        # close the current form
        self.close_current_form()

        # create and register "form_view_submission_logs" in container with the grid geometry manager
        form_view_submission_logs = glog.FormViewSubmissionLogs(self)
        form_view_submission_logs.grid(row=0, column=0, sticky='nsew')

        # set "form_view_submission_logs" as current form and add it in the forms dictionary
        self.current_form = 'form_view_submission_logs'
        self.forms_dict[self.current_form] = form_view_submission_logs

        # raise "form_view_submission_logs" to front
        form_view_submission_logs.tkraise()

    #---------------

    def view_result_logs(self):
        '''
        List logs of results in a cluster.
        '''

        # close the current form
        self.close_current_form()

        # create and register "view_result_logs" in container with the grid geometry manager
        form_view_result_logs = glog.FormViewResultLogs(self)
        form_view_result_logs.grid(row=0, column=0, sticky='nsew')

        # set "form_view_result_logs" as current form and add it in the forms dictionary
        self.current_form = 'form_view_result_logs'
        self.forms_dict[self.current_form] = form_view_result_logs

        # raise "form_view_result_logs" to front
        form_view_result_logs.tkraise()

    #---------------

    def open_help(self, event=None):
        '''
        Open the help file.
        '''

        try:
            manual = os.path.abspath(xlib.get_project_manual_file())
            webbrowser.open_new(f'file://{manual}')
        except Exception:
            message = f'The document {manual}\n is not available.'
            tkinter.messagebox.showerror(f'{xlib.get_short_project_name()} - Open help', message)

    #---------------

    def show_dialog_about(self):
        '''
        Show the application information.
        '''

        dialog_about = gdialogs.DialogAbout(self.root)
        self.root.wait_window(dialog_about)

    #---------------

    def warn_unavailable_process(self):

        message = 'This process is been built.\nIt is coming soon!'
        tkinter.messagebox.showwarning(tkinter.messagebox.showerror(f'{xlib.get_short_project_name()} - {self.root.head}', message), message)

    #---------------

    def close_current_form(self):
        '''
        Close the current form.
        '''

        # clear the label of the current process name
        self.label_process['text'] = ''

        # destroy the current form
        if self.current_form != 'form_welcome':
            self.forms_dict[self.current_form].destroy()
            self.forms_dict['form_welcome'].tkraise()

    #---------------

    def exit(self, event=None):
        '''
        Exit the application.
        '''

        message = f'Are you sure to exit {xlib.get_short_project_name()}?'
        if tkinter.messagebox.askyesno(f'{xlib.get_short_project_name()} - Exit', message):
            self.close_current_form()
            self.root.quit()
            self.root.destroy()
            exit()

   #---------------

#-------------------------------------------------------------------------------

class FormWelcome(tkinter.Frame):

    #---------------

    def __init__(self, main):
        '''
        Execute actions correspending to the creation of a "FormWelcome" instance.
        '''

        # save initial parameters in instance variables
        self.main = main
        self.root = main.root
        self.container = main.container

        # call the init method of the parent class
        tkinter.Frame.__init__(self, self.container)

        # build the graphical user interface
        self.build_gui()

    #---------------

    def build_gui(self):
        '''
        Build the graphical user interface of "FormWelcome".
        '''

        # create "image_penota"
        image_penota = PIL.Image.open('./image_penota.jpg')
        image_penota.thumbnail((self.main.WINDOW_WIDTH,self.main.WINDOW_HEIGHT), PIL.Image.ANTIALIAS)

        # create "photoimage_penota"
        self.photoimage_penota = PIL.ImageTk.PhotoImage(image_penota)  

        # create "canvas_photoimage_perrault" and register it with the grid geometry manager
        self.canvas_photoimage_penota = tkinter.Canvas(self, width=self.main.WINDOW_WIDTH, height=self.main.WINDOW_HEIGHT)
        self.canvas_photoimage_penota.create_image(round(self.main.WINDOW_WIDTH / 2), round(self.main.WINDOW_HEIGHT / 2 - 45), image=self.photoimage_penota, anchor='center')
        if sys.platform.startswith('linux'):
            x_coordinate = 10
            y_coordinate = self.main.WINDOW_HEIGHT - 100
        elif sys.platform.startswith('darwin'):
            x_coordinate = 10
            y_coordinate = self.main.WINDOW_HEIGHT - 85
        elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
            x_coordinate = 10
            y_coordinate = self.main.WINDOW_HEIGHT - 70
        self.canvas_photoimage_penota.create_text(x_coordinate, y_coordinate, anchor='w', text = 'La Peñota - Sierra de Guadarrama National Park (Madrid, Spain)') 
        self.canvas_photoimage_penota.pack(side='left', fill='both', expand=True)

    #---------------

    def close(self):
        '''
        Close "FormWelcome".
        '''

        # close the current form
        self.main.close_current_form()

   #---------------

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    print(f'This file contains the class Main corresponding to the graphical user interface of the {xlib.get_long_project_name()} software package.')
    sys.exit(0)

#-------------------------------------------------------------------------------
