Naming Conventions for ROI File-names
=====================================

One of the aims of the scripts produced during this work was to minimize
the variation in filenames for such things as ROIs or results files.
This is why it is stressed that researchers should use the stury
directory approach even for small data sets or when a study is in
development and being scoped. However, the authors are aware that on
occasion it may be more convenient to work on single datasets in a less
structured manner. However, for the fitting programs to work, the ROI
files must follow a minimum naming structure. The details are outlined
below.

-  If the ROIs are outline ROIs then this must be present in the zipped
   file-name of the set of ROIs encased in underscores, \_outline_.

-  It is a good idea to add what the imagedType the ROIs are of. For
   example, \_muscle_, \_fat_, \_phantom_, \_brain_.

The individual ROIs within the zipped file should also follow a certain
naming convention. This should include the following:

-  The slice number should be included, starting from an index of one
   and be identified by adding the word slice and connecting the number
   with a hyphon, for example, slice-1_, or \_slice-2\_ and separated
   from other parts of the filename with an underscore.

-  The word or number identifying the ROI should be placed at the end of
   filename before the extension descriptor. For example
   slice-1_muscle_roi1.roi or slice-1_fat_1.roi or
   slice1_muscle_extensor.roi. The ROI identifier must be unique within
   a set of ROIs.

-  It is also a good idea to add the initials of the person who drew the
   ROI. For example, KGH_slice-1_muscle_extensor.roi. This is useful for
   book-keeping purposes.

When data is derived from a single file, the filename includes the model
used and appropriate descriptor for the file. The directory where the
data is stored is given in the fitModelData file. A relative or absolute
path can be used.
