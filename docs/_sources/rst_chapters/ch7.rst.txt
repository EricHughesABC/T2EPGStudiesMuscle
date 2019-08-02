Fitting T\ :sub:`2` Data with fitEPGazz.py
==========================================

The python program has been designed/developed to work within a study
data directory structure or with single files. The program can fit a
number of different models to the data and works with a fitModelData
yaml file for input.

Example fitModelData yaml files can be found in the following
directories

::

   mristudydescription/
   │
   └── examples/
       │
       │
       ├── fitSingleModelDataYAMLfiles/
       │   │
       │   ├── fitSingleDataMuscleEPG1nifti.yml
       │   ├── fitSingleDataMuscleAzzabouNifti.yml
       │   ├── fitSingleDataFatEPG2nifti.yml
       │   ├── fitSingleDataEPGAzzAnalyzeOutline.yml
       │   └── fitSingleDataEPGAzzAnalyzeIndividual.yml
       │
       └── fitStudyModelDataYAMLfiles/
           │
           ├── fitStudyDataEPGAzzAnalyze.yml
           ├── fitStudyDataEPGAzzAnalyze.yml
           ├── fitStudyDataFatEPG2analyze.yml
           ├── fitStudyDataMuscleEPG1analyze.yml
           └── fitStudyDataMuscleEPG1nifti.yml

The files in the **fitSingleModelDataYAMLfiles** directory correspond to
fitModelData example yaml files that work on single specified datasets.

The files in the **fitStudyModelDataYAMLfiles** directory correspond to
fitModelData example yaml files that work on data in a study data
directory structure. In this case, example study data directory
structures that work with the yaml files are found in

::

   mristudydescription/
   │
   └── examples/
       │
       └── studyDirectoyExamples
           │
           ├── testStudyAnalyze
           ├── testStudyNiftDIR
           └── testStudyNiftiFile

Fitting T\ :sub:`2` Data with fitEPGazz.py on named single data files
---------------------------------------------------------------------

To use the program in this manner one would type the following on the
command line after moving to the directory where the fitEPGazz.py is
located.

::

   -> python fitEPGazz.py examples\fitSingleModelDataYAMLfiles\fitSingleDataFatEPG2nifti.yml

or just the program name on its own and enter the yaml file using the
interactive dialog that pops up.

::

   -> python fitEPGazz.py

Fitting T\ :sub:`2` Data with fitEPGazz.py in study directory structures
------------------------------------------------------------------------

The program can fit data from within a study structure directory. This
can be achieved by calling the program from the command line without
arguments and interactive dialogs will pop up to ask for the yaml file
and then the study directory name.

::

   -> python fitEPGazz.py

The fitModelData yaml file can be supplied on the command line. If the
**fitSubject** parameter list is not empty then an interactive dialog
will pop up asking for the path of the study structure directory.

::

   -> python fitEPGazz.py examples\fitStudyModelDataYAMLfiles\fitStudyDataAzzabouAnalyze.yml

Finally, the program can be called with two command line arguments
specifying the yaml fitModelData file and the study directory structure
path.

::

   -> python fitEPGazz.py examples\fitStudyModelDataYAMLfiles\fitStudyDataAzzabouAnalyze.yml 
                          examples\studyDirectoyExamples\testStudyAnalyze
