Creating the study Description File using the GUI Program
=========================================================

The study description file contains all the information about the study.
This file can be created by hand, but it is easy to introduce errors, so
a simple GUI program has been written that asks for the information in a
series of dialogs. Below we show the dialog boxes for a simple study
that has a single participant, session, imaged region and ROI file.

The program is started from the command line and has no command-line
arguments

::

   -> python studyDescriptionGUI.py

Step 1. Define the name of the study
------------------------------------

The first step is define the name of the study and where it will be
saved using a directory dialog. If the directory does not already exist,
it can be created using the dialog.

|study name dialog|

Figure 1 Define the name of the study

Step 2. Number of different Groups in the study
-----------------------------------------------

In the study the number of different participant groups is defined. This
is based on simple criteria such as healthy controls and participants
with the condition. Within these groups, sub-groups can be defined based
on the number of visits/sessions, the different protocols that they
have.

|Number of Different Groups|

Figure 2 Number of Different Groups

Step 3. Number of MRI protocols used in the study
-------------------------------------------------

The different MRI protocols that will be performed in the study should
be listed next. Examples could be based on diffusion, T\ :sub:`2`,
T\ :sub:`1`, and Dixon. The MRI protocols are added to the field
separated by a space. In the example one MRI protocol is given.

|Number of MRI protocols|

Figure 3 Names of the protocols used in the study

Step 4. Enter the initials of the people who will have created ROIs
-------------------------------------------------------------------

In the data analysis of a study many people work on the project,
especially with the data analysis. Many projects require regions of
interest to be drawn on the images for use in the analysis. This task is
often performed by different people so it is useful for quality control
reasons to keep track of who created the ROIs and this is done by giving
a list of initials of the different people who will draw the ROIs. This
is added to the ROI name so that this aspect of the data analysis may be
audited. In the dialog one set of initials has been input. Further sets
of initials could be entered separated by a space

|Roi Author Initials|

Figure 4 List of author initials who have created ROIs

Step 5. Enter the names of the groups, number of sessions and a list of imaged regions
--------------------------------------------------------------------------------------

The names of the different groups of participants are entered in this
dialog. The names must be unique. For each group the number of
sessions/visits that the participants in the group attend during the
study is entered. Finally, the imaged regions of the body are entered.
In this field, if a phantom is used throughout the study a place name
for it may be entered.

|groupNameSessionImagedRegions|

Figure 5 For each group defined previously, enter a name for the group
the number of visits/sessions the participants will take part in and the
imaged regions that will be looked at

Step 6. Add the list of participant names/id codes for each defined group
-------------------------------------------------------------------------

For each defined group the participants id-code is entered in this
dialog. The id-code is entered one per line. If more than one group is
defined in the study then then it will appear along side the other
groups in the dialog window.

|participant Names|

Figure 6 List of participant names/ID codes for each defined group

Step 7. Definition of ROI/imaged region types
---------------------------------------------

In this step the ROI/Imaged Region types are entered for each imaged
region, forearm, upperarm,... This dialog is repeated separately for
each group in the study. The group name appears in the dialog title in
the border. Each ROI/Imaged Region type is entered on a separate line.

|image6|

Figure 7 ROI/imaged region types being entered for Healthy volunteers
group and the foream imaged region

Step 8. Definition of the labels for individual ROIs
----------------------------------------------------

The names of the regions of interest for the different ROI/imaged region
types are entered in this dialog. The names can be words or numbers, but
must be unique with the same category

|image7|

Figure 8 ROI labels entered for the different imaged regions and imaged
region types

Step 9. Slice index for the different imaged regions
----------------------------------------------------

The slices used in the study are dependent on the MRI protocol, the
imaged region and imaged region/ROI type. Imaged slices are numbered
based on a starting index of 1.

|image8|

Figure 9 Slices used in the analysis of the data are defined in this
dialog.

Step 10. Saving the study template file
---------------------------------------

When the final dialog is closed the study template file is saved in the
study directory. A number of fields within the study template file
remain blank, these should be filled in by the user, using a text
editor. The fields requiring updating by the user are:

-  principal investigators

-  research associates

-  students

Below is the study description file produced by the previous dialogs

.. code-block :: yaml

   studyName: testStudy
   studyRootDir: MRIstudyDescription/examples

   HealthyVolunteers:
     imagedRegions: [forearm]
     name: HealthyVolunteers
     numSessions: 1
     participants: [HC-001]
     rois:
       forearm:
         fat: ['1', '2', '3', '4', '5']
         muscle: [fg, eg]
         outline: ['1']
     sessions: [sess-1]
     slices:
       forearm:
         fat:
           T2: ['2']
         muscle:
           T2: ['1', '2', '3']
         outline:
           T2: ['1', '2', '3']

   groupNames: [HealthyVolunteers]
   protocols: [T2]
   roiAuthors: [EH]

   principalInvestigators:
   - {address: '', email: '', initials: '', name: ''}

   researchAssociates:
   - {address: '', email: '', initials: '', name: ''}

   students:
   - {address: '', email: '', initials: '', name: ''}

.. |study name dialog| image:: images/ch2/media/image1.png
   :width: 5.83333in
   :height: 1.08819in
.. |Number of Different Groups| image:: images/ch2/media/image2.png
   :width: 5.62083in
   :height: 2.04236in
.. |Number of MRI protocols| image:: images/ch2/media/image3.png
   :width: 2.68403in
   :height: 1.18958in
.. |Roi Author Initials| image:: images/ch2/media/image4.png
   :width: 2.8in
   :height: 1.18958in
.. |groupNameSessionImagedRegions| image:: images/ch2/media/image5.png
   :width: 5.83333in
   :height: 0.87292in
.. |participant Names| image:: images/ch2/media/image6.png
   :width: 4.11597in
   :height: 2.98958in
.. |image6| image:: images/ch2/media/image7.png
   :width: 5.11597in
   :height: 2.98958in
.. |image7| image:: images/ch2/media/image8.png
   :width: 4.2in
   :height: 1.75764in
.. |image8| image:: images/ch2/media/image9.png
   :width: 5.43125in
   :height: 1.82083in
