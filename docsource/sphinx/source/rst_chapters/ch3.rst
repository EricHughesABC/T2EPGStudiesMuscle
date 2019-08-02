Creating the Study Directory Structure
======================================

Once the study description file has been created, the directory
structure of the sttudy can be created by issuing the following command.

::

   -> python create_study_directory_structure.py

This script will create the following study directory structure and also
create ROI template files

::

   .
   └── testStudy
       ├── HC-001
       │   └── sess-1
       │       └── forearm
       │           ├── dicom
       │           ├── rois
       │           │   └── EH
       │           │       ├── EH_HC-001_sess-1_forearm_fat.zip
       │           │       ├── EH_HC-001_sess-1_forearm_muscle.zip
       │           │       └── EH_HC-001_sess-1_forearm_outline.zip
       │           └── T2
       └── study_description_file.yml
