FitModeldData file main parameters
==================================

Model Definition
----------------

The first line of the file states which model will be used by the
fitting program

::

   1       fitModel: AzzEPG

The model chosen must come from the eight fit models defined in lines 24
to 32. For each model there is a corresponding parameter file defined.
These lines in the file, together with lines 34 to 42 should not be
altered.

::

   24      paramsModelName:
   25          AzzEPG:      fitModelParameterJsonFiles/azz_fatmuscle_epg_model_params.json
   26          fatEPG2:     fitModelParameterJsonFiles/two_fat_epg2_model_params.json
   27          fatEPG1:     fitModelParameterJsonFiles/one_fat_epg1_model_params.json
   28          muscleEPG1:  fitModelParameterJsonFiles/one_fatmuscle_epg1_model_params.json
   29          muscleEPG2 : fitModelParameterJsonFiles/two_fatmuscle_epg2_model_params.json
   30          phantomEPG1: fitModelParameterJsonFiles/oneParamEPGphantom_model_params.json
   31          phantomEPG2: fitModelParameterJsonFiles/twoParamEPGphantom_model_params.json
   32          Azzabou:     fitModelParameterJsonFiles/azz_params.json

Study Data Directory Structure Used or Not.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It was stated earlier that this file can be used to work on data found
in a study directory structure or directly on files in a single
directory. This is achieved by either putting a list of participants in
the **fitSubject** list or setting it to empty.

::

   44      fitSubject: [HC-001]

In this configuration we will use data found in study directory
structure. If the line had been set in the following manner

::

   44      fitSubject: []

then the program would work on named files within the fitModeldata file
defined in lines 54 to 59

::

   54      #roisIndividual: simpleModelData/DMD_001_FOREARM_RoiSet.zip
   55      
   56      roiOutline: simpleModelData/EH_DMDT_001_1_foreArm_outline.zip
   57      
   58      analyzeHdr: simpleModelData/WIP_Forearm_T2_CLEAR.hdr
   59      analyzeImg: simpleModelData/WIP_Forearm_T2_CLEAR.img

Defining sessions, imaged regions and slices
--------------------------------------------

If the fitting program is taking data from the Data Directory Structure
then the sessions and imaged regions to be used are defined as lists in
lines 45 and 47. If defined data is used then the **fitSession** and
**fitImagedRegions** fields are ignored.

::

   45      fitSession: [sess-1]
   46      fitImagedRegions: [forearm]
   47      fitSlices: [1,2,3]

The slices to be used in the fitting are defined in line 47. The slices
defined in this list are also used when the program works on defined
data.

Updating the values in the LMFIT parameter structures.
------------------------------------------------------

Initial starting values for parameters can be set within the file by
updating the fields starting at lines 18 to 22

::

   14      # EPGAZZ model parameters to update
   15      # Always include the echo value
   16      
   17      ParamVals:
   18          echo:
   19              value: 8
   20              min: 0
   21              max: 10
   22              vary: False

As shown in the example the echo spacing time must always be set in the
file. Further parameters within the fitting model can be set in a
similar manner. Parameters that might want to be changed could be the
the T\ :sub:`2` values of the fat in the model, or the initial guess of
the muscle T\ :sub:`2`.

As an example, further items may be added to the file in the following
manner to set the long and short T\ :sub:`2` components of the fat.

::

   ParamVals:
       echo:
           value: 8.0
       t2_l:
           value: 250.0
           min:   0.0
           max:   300.0
           vary:  False
       t2_s:
           value: 80.0
           min:   0.0
           max:   300.0
           vary:  False

In this example all the attributes of the two T\ :sub:`2` fat parameters
are set, i.e. value,minimum, maximum and is it varied in the model. The
minimum and maximum are set so that they cover the new value for the
parameter. If the value is beyond the range present in the original
parameter file then it will be incorrectly set. The vary attribute could
be omitted from the definition. If is is changed from its original
setting within the original parameter file then the model will be
changed as more or less parameters are varied during the fit. It is best
not to change the **vary** attribute from its original setting.

The parameters that can be altered are listed below:

::

   A_f
   A_m
   B1
   T1_f
   T1_m
   c_l
   c_s
   echo
   t2_fl
   t2_fs
   t2_m

The flag **setParamValsIndividually** is set to **True** in the file in
this example. In this case, then fat values are calculated from previous
model data in the study directory structure for each participant in the
**fitSubject** list. This flag can only be set to **True** when data is
being fit from a study directory structure. When this is the case the
path to the fat data should be indicated using the **fatResultsDir**
flag

::

   11      fatResultsDir: T2/results/fat/fatEPG2

When the flag **setParamValsIndividually** is set to **False** then all
the fat parameters for certain models are set from within the file if
they are present, for all participants.

ROI Author Preferences :: roiAuthorPreference
---------------------------------------------

The field **roiAuthorPreferences** at line 51 gives a list of author
initials that are used to choose which ROI files are used.

::

   51      roiAuthorPreference: [EH]

The order of the list gives the priority, if a certain author cannot be
found, then the next author initials will be used to choose the correct
ROI files. This option is only acted upon when the fitting scripts are
used within a study dierctory structure.

Use Roi Outline :: useRoiOutline
--------------------------------

This option is set to **True** when an outline ROI is used to define
which part of the image is to be fit.

::

   38      useRoiOutline: False

Outline ROI filenames must include the word **outline** in their name
for the programs to function correctly

Image Data Format :: imageDataFormat
------------------------------------

The fitting progams can now read in both analyze and nifti data formats.
This must be indicated in the file

::

   52      imageDataFormat: Analyze

For Analyze format the program expects to find the image data as a file,
therefore when the fitting program is fitting individual data then a
file name with a relative or complete path should be given.

::

   58      analyzeHdr: simpleModelData/WIP_Forearm_T2_CLEAR.hdr
   59      analyzeImg: simpleModelData/WIP_Forearm_T2_CLEAR.img

Nifti data can come in the form of a single file, either zipped or not,
or as a series of files, perhaps corresponding to individual echo times
for the T\ :sub:`2` data. If this is the case then the directory where
the data can be found must be entered.

::

   imageDataFormat: nifti

   # when individual files 

   niftiData: C:\Users\NEH69\Dropbox\projects\programming\2019\MRIstudyDescription\simpleModelData\WIP_Forearm_T2_CLEAR.nii.gz

   # when a series of nifti files

   niftiData: C:\Users\NEH69\Dropbox\projects\programming\2019\MRIstudyDescription\simpleModelData\niffti
