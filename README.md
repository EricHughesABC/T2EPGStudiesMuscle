# T2EPGStudiesMuscle
Programs to work on MRI studies that fit T2 Data using EPG and classical approach

### Requirements

The EPG and ijroieh modules need to be installed. These can be found at

https://github.com/EricHughesABC/EPG
https://github.com/EricHughesABC/ijroieh

### Introduction

This repository consists of a number of python programs to set up a CPMG T2 MRI study directory structure and then analyse the data using an EPG or classical T2 approach.

An example of the directory structure created

\---testStudy
    |   study_description_file.yml
    |   
    \---HC-001
        \---sess-1
            \---upperleg
                +---dicom
                +---rois
                |   \---EH
                |           EH_HC-001_sess-1_upperleg_fat.zip
                |           EH_HC-001_sess-1_upperleg_muscle.zip
                |           EH_HC-001_sess-1_upperleg_outline.zip
                |           
                \---T2
                    |   WIP_T2_multiecho_UL_CLEAR.hdr
                    |   WIP_T2_multiecho_UL_CLEAR.img
                    |   
                    \---results
                        +---fat
                        |   +---fatEPG2
                        |           fitStudyDataFatEPG2analyze.yml
                        |           T2_HC-001_sess-1_upperleg_fatEPG2_Agg_summary.csv
                        |           T2_HC-001_sess-1_upperleg_fatEPG2_Agg_summary.xls
                        |           T2_HC-001_sess-1_upperleg_fatEPG2_results.csv
                        |           T2_HC-001_sess-1_upperleg_fatEPG2_results.xls
                        |           T2_HC-001_sess-1_upperleg_fatEPG2_summary.csv
                        |           T2_HC-001_sess-1_upperleg_fatEPG2_summary.xls
                        |           
                        \---muscle
                            +---Azzabou
                            |       fitStudyDataAzzabouAnalyze.yml
                            |       T2_HC-001_sess-1_upperleg_Azzabou_Agg_summary.csv
                            |       T2_HC-001_sess-1_upperleg_Azzabou_Agg_summary.xls
                            |       T2_HC-001_sess-1_upperleg_Azzabou_results.csv
                            |       T2_HC-001_sess-1_upperleg_Azzabou_results.xls
                            |       T2_HC-001_sess-1_upperleg_Azzabou_summary.csv
                            |       T2_HC-001_sess-1_upperleg_Azzabou_summary.xls
                            |       
                            \---AzzEPG
                                    fitStudyDataEPGAzzAnalyze.yml
                                    T2_HC-001_sess-1_upperleg_AzzEPG_Agg_summary.csv
                                    T2_HC-001_sess-1_upperleg_AzzEPG_Agg_summary.xls
                                    T2_HC-001_sess-1_upperleg_AzzEPG_results.csv
                                    T2_HC-001_sess-1_upperleg_AzzEPG_results.xls
                                    T2_HC-001_sess-1_upperleg_AzzEPG_summary.csv
                                    T2_HC-001_sess-1_upperleg_AzzEPG_summary.xls
