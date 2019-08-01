Set-up of the fitModeldata yaml file
====================================

Information to process the data in the study is provided to the fitting
program by a fitmodelData yaml file. Examples of these files can be
found in the **fitModelDataYAMLfiles** directory for fitting single data
sets and in the **examples/fitModelDataYAMLfiles** directory for fitting
data in a study directory structure.

-  fitStudyDataEPGAzz

-  fitStudyDataFatEPG2

-  fitStudyDataMuscleEPG1

The fitting program is capable of fitting a number of different models
to the T\ :sub:`2` image data based on the model structure found in the
Azzabou paper. Muscle, fat and phantom data can be fit by the program
using a simple exponential decay model or an extended phase graph model
(EPG). This document will focus on fitting the T\ :sub:`2` image data
using the EPG model.

The example taken will be to fit the T\ :sub:`2` image data using the
**fitStudyDataEPGAzzAnalyze** yaml file.

The contents of the file are given below. Line numbers have been added
to help with the explanation of the file, but the user should be aware
that the sequential order of the different groups within the file is not
important. The example YAML file has been set up to be used on the study
directory structure defined earlier. The YAML input file has been
designed to be used on data in a study directory structure or on
individual files which have been defined within the file. In the
following paragraphs the different parts of the file will be discussed.

::

   1       fitModel: AzzEPG
   2       
   3       # use a relative directory path when fitting data in study directory structure
   4       # when fitting individual files it can be set to a complete path
   5       
   6       resultsDir: T2/results/muscle/AzzEPG
   7       
   8       # Can only be used when fitting data in study directory structure
   9       # must be set as a relative directory path
   10      
   11      fatResultsDir: T2/results/fat/fatEPG2
   12      setParamValsIndividually: True
   13      
   14      # EPGAZZ model parameters to update
   15      # Always include the echo value
   16      
   17      ParamVals:
   18          echo:
   19              value: 8
   20              min: 0
   21              max: 10
   22              vary: False
   23      
   24      paramsModelName:
   25          AzzEPG:      fitModelParameterJsonFiles/azz_fatmuscle_epg_model_params.json
   26          fatEPG2:     fitModelParameterJsonFiles/two_fat_epg2_model_params.json
   27          fatEPG1:     fitModelParameterJsonFiles/one_fat_epg1_model_params.json
   28          muscleEPG1:  fitModelParameterJsonFiles/one_fatmuscle_epg1_model_params.json
   29          muscleEPG2 : fitModelParameterJsonFiles/two_fatmuscle_epg2_model_params.json
   30          phantomEPG1: fitModelParameterJsonFiles/oneParamEPGphantom_model_params.json
   31          phantomEPG2: fitModelParameterJsonFiles/twoParamEPGphantom_model_params.json
   32          Azzabou:     fitModelParameterJsonFiles/azz_params.json
   33      
   34      roiFitModel:
   35          AzzEPG:      muscle
   36          fatEPG2:     fat
   37          fatEPG1:     fat
   38          muscleEPG1:  muscle
   39          muscleEPG2 : muscle
   40          phantomEPG1: phantom
   41          phantomEPG2: phantom
   42          Azzabou:     muscle
   43      
   44      fitSubject: [HC-001]
   45      fitSession: [sess-1]
   46      fitImagedRegions: [forearm]
   47      fitSlices: [1,2,3]
   48      
   49      useRoiOutline: False
   50      
   51      roiAuthorPreference: [EH]
   52      imageDataFormat: Analyze
   53      
   54      #roisIndividual: simpleModelData/DMD_001_FOREARM_RoiSet.zip
   55      
   56      roiOutline:     simpleModelData/EH_DMDT_001_1_foreArm_outline.zip
   57      
   58      analyzeHdr: simpleModelData/WIP_Forearm_T2_CLEAR.hdr
   59      analyzeImg: simpleModelData/WIP_Forearm_T2_CLEAR.img
   60      
   61      # minimum step size across profile =  1
   62      # maximum step size across profile = 19
   63      
   64      pulseProfileSteps: 10
   65      
   66      # pulse profile should correspond to the protocol that was used to collect
   67      # the data
   68      
   69      p90pulseProfile: simpleModelData/flip_angle90_clairewood.mat
   70      p180pulseProfile: simpleModelData/flip_angle180_clairewood.mat
   71      
   72      # integration factor, might need to be altered based on value of
   73      # pulseProfileSteps and fit model being used
   74      
   75      dx: 0.45
