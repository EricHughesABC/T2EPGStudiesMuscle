Output from T\ :sub:`2` Fitting Program: fitEPGazz.py
=====================================================

The fitModelData YAML file and three data files are produced from the
fitting program in CSV and Excel format:

-  A results file listing all the fitted data at a pixel level in one
   table based on slices and ROIs. \_results.csv(.xls)

-  A Summary file of the mean and standard deviation for each ROI in
   each slice. \_summary.csv(.xls)

-  An aggregated summary file giving the weighted mean of each parameter
   for each ROI averaged over slices and pixels in each ROI.
   \_summaryAgg.csv(.xls)

The YAML file and the three results files are produced for single data
sources and data present in a study directory structure.

When the data is derived from a study directory structure, the filename
includes the subject, the session, the imaged region, and the model used
together with the appropriate descriptor to indicate the type of data in
the file. The files are best saved in a
*T2/results/imagedRegionType/model* directory at the appropriate point
in study directory structure for the fitted data. This should be set in
the **fitModelData** file.

::

   3       # use a relative directory path when fitting data in study directory structure
   4       # when fitting individual files it can be set to a complete path
   5       
   6       resultsDir: T2/results/muscle/AzzEPG

When data is derived from a single file, the filename includes the model
used and appropriate descriptor for the file. The directory where the
data is stored is given in the fitModelData file. A relative or absolute
path can be used.

When the T\ :sub:`2` fitting program is used on single file data, then
plots of the ROIs overlayed over the imaged region are displayed in in a
single plot (Figure 1) and a representative plot of the fitting results
(Figure 2) for a single pixel data set is displayed in a second
independent plot taken from data from the middle of the data set.

|image0|

Figure 1 Overlay of ROIs on fitted Image

|image1|

Figure 2 Quality of fit to data

.. |image0| image:: images/ch8/media/image1.png
   :width: 3.82292in
   :height: 1.59028in
.. |image1| image:: images/ch8/media/image2.png
   :width: 3.82708in
   :height: 1.90556in
