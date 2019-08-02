T2EPGStudiesMuscle
##################

Programs to work on MRI studies that fit T2 Data using EPG and classical approach

Requirements
------------

The EPG and ijroieh modules need to be installed. These can be found at

   https://github.com/EricHughesABC/EPG
   
   https://github.com/EricHughesABC/ijroieh

Introduction
------------

This repository consists of a number of python programs to set up a CPMG T2 MRI study directory structure and then analyse the data using an EPG or classical T2 approach. The purpose of the programs is to automate the setting up of a CPMG T2 MRI study in terms of directory structure and file name conventions for region of interest files. It takes inspiration from the BIDS initiative https://bids.neuroimaging.io/. The programs that automate the set up of the study are general and couldbe used for other MRI studies

Programs
--------

- **studyDescriptionGUI.py**
   - This program is run first to create a yaml file describing the study and capturing all relevant information
      
- **create_study_directory_structure.py** 
   - This program creates the study directory structure and region of interest files that are used to analyze the MRI data
    
- **fitEPGazz.py**
   - This program fits the T2 CPMG MRI data.
    
    
Further documentation can be found in the docs directory in terms of a word document and pdf file    

An example of the directory structure created for a simple MRI study
--------------------------------------------------------------------

::

    └── testStudy
        ├── study_description_file.yml
        │  
        └── HC-001
            └── sess-1
                └── upperleg
                    ├── dicom
                    ├── rois
                    │   └── EH
                    │        ├──── EH_HC-001_sess-1_upperleg_fat.zip
                    │        ├──── EH_HC-001_sess-1_upperleg_muscle.zip
                    │        └──── EH_HC-001_sess-1_upperleg_outline.zip
                    │           
                    └──T2
                        ├── WIP_T2_multiecho_UL_CLEAR.hdr
                        ├── WIP_T2_multiecho_UL_CLEAR.img
                        │   
                        └─ results
                            ├─ fat
                            │   └── fatEPG2
                            │         ├────  fitStudyDataFatEPG2analyze.yml
                            │         ├──── T2_HC-001_sess-1_upperleg_fatEPG2_Agg_summary.csv
                            │         ├──── T2_HC-001_sess-1_upperleg_fatEPG2_Agg_summary.xls
                            │         ├──── T2_HC-001_sess-1_upperleg_fatEPG2_results.csv
                            │         ├──── T2_HC-001_sess-1_upperleg_fatEPG2_results.xls
                            │         ├──── T2_HC-001_sess-1_upperleg_fatEPG2_summary.csv
                            │           T2_HC-001_sess-1_upperleg_fatEPG2_summary.xls
                            │           
                            └─ muscle
                                ├── Azzabou
                                │     ├──── fitStudyDataAzzabouAnalyze.yml
                                │     ├──── T2_HC-001_sess-1_upperleg_Azzabou_Agg_summary.csv
                                │     ├──── T2_HC-001_sess-1_upperleg_Azzabou_Agg_summary.xls
                                │     ├──── T2_HC-001_sess-1_upperleg_Azzabou_results.csv
                                │     ├──── T2_HC-001_sess-1_upperleg_Azzabou_results.xls
                                │     ├──── T2_HC-001_sess-1_upperleg_Azzabou_summary.csv
                                │       T2_HC-001_sess-1_upperleg_Azzabou_summary.xls
                                │       
                                └── AzzEPG
                                      ├──── fitStudyDataEPGAzzAnalyze.yml
                                      ├──── T2_HC-001_sess-1_upperleg_AzzEPG_Agg_summary.csv
                                      ├──── T2_HC-001_sess-1_upperleg_AzzEPG_Agg_summary.xls
                                      ├──── T2_HC-001_sess-1_upperleg_AzzEPG_results.csv
                                      ├──── T2_HC-001_sess-1_upperleg_AzzEPG_results.xls
                                      ├──── T2_HC-001_sess-1_upperleg_AzzEPG_summary.csv
                                      └──── T2_HC-001_sess-1_upperleg_AzzEPG_summary.xls


