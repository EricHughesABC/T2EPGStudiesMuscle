# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 09:32:44 2019

@author: neh69
"""

#
# Summarize Dixon Data based on ROIs
#
# Use summarizeDixonData YAML file to work either on single files or
# data held in study directory strucure
#
import numpy as np

import pandas as pd
import os
import sys
from skimage.draw import ( polygon,ellipse)
import ijroieh

import yaml
import json

import guidata
_app = guidata.qapplication() # not required if a QApplication has already been created

import guidata.dataset.datatypes as dt
import guidata.dataset.dataitems as di

import nibabel


class AttrDict(dict):
    """class to access a dictionary as class.key"""

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
        self.data_dict = args[0]


    @classmethod
    def from_jsonFile(cls, filename):
        fp = open(filename,'r')
        data_dict = json.load(fp)
        fp.close()
        return cls(data_dict)

    @classmethod
    def from_yamlFile(cls, filename):
        fp = open(filename,'r')
        data_dict = yaml.load(fp)
        fp.close()
        return cls(data_dict)

    @classmethod
    def from_file(cls,filename):
        fp = open(filename,'r')
        if ".yml" in filename:
            data_dict = yaml.load(fp)
        else:
            data_dict = json.load(fp)

        fp.close()
        return cls(data_dict)

    def dump(self, fn):
        if ".yml" in fn:
            fp = open(fn,"w")
            yaml.dump(self.data_dict,fp)
            fp.close()
        elif ".json" in fn:
            fp = open(fn,"w")
            json.dump(self.data_dict,fp)
            fp.close()
        else:
            print("Saved file type is not  YAML or JSON ::", fn)


class studyDirectory(dt.DataSet):
    """Study Root Directory

    Enter Study Directory"""

    directory = di.DirectoryItem("Study Dir:")


class dixonModelFile(dt.DataSet):
    """Dixon Model File

    Enter Dixon model file"""

    dixonFileName = di.FileOpenItem("Dixon Model:")



def return_masks_individual( dataSet, islice,  roi_set):
    """Used to calculate a mask for a single slice given that the zipped
    ROI is made up of individual ROIs

    Parameters
    ----------

    dataSet: dictionary
        contains information on dimensions of image
    islice: int
        index number of slice based on rois

    roi_set: list
        rois read in from imageJ formatted roi set

    Returns
    -------

    mask: 2-D np.ndarray of type boolean
        boolean mask of all the ROIS found for the slice
    mask_id: 2-D np.ndarray of type int
        integer mask of all the ROIS found in the slice,
        each pixel associated with a specific ROI is set to a number starting
        at 1 and incremented if more than one ROI present
    roi_names: list of str
        list of ROI names associated with the image slice
    """

    mask = np.zeros((dataSet['numRows'],dataSet['numCols']), dtype=np.bool)
    mask_id = np.zeros((dataSet['numRows'],dataSet['numCols']), dtype=np.int8)

    roi_names = []

    roi_ii = 1
    for rois in roi_set:
        (roi_name,roiShape, coords) = rois

        print(  islice, roi_name, roi_ii)
        if "slice-{}".format(islice) in roi_name:
            print( "found", islice, roi_name, roi_ii)
            roi_names.append(roi_name)

            if roiShape == 'polygon':
                coords=coords.transpose()
                print(coords[0],coords[1])
                mask[polygon(coords[0],coords[1])] = True
                mask_id[polygon(coords[0],coords[1])] = roi_ii

            elif roiShape == 'rect':
                coords=coords.transpose()
                mask[polygon(coords[0],coords[1])] = True
                mask_id[polygon(coords[0],coords[1])] = roi_ii

            elif roiShape == 'oval':
                xc = coords[0][0]
                yc = coords[0][1]
                xr = coords[1][0]
                yr = coords[1][1]
                mask[ellipse(yc,xc,yr,xr)] = True
                mask_id[ellipse(yc,xc,yr,xr)] = roi_ii

            roi_ii += 1

    return mask, mask_id, roi_names



def decide_what_todo():

    command_line_args_string = """

The program can be called in the following manner

python createDixonSummaries.py

python createDixonSummaries.py  directory\\to\\input_file\\dixonDataFile.yml

python createDixonSummaries.py directory\\directory\\to\\input_file\\dixonDataFile.yml directory\\to\\study_directory\\testStudy"""


    studyDir = None

    if len(sys.argv) == 1: ## no command arguments
        #
        # Ask for fit Model data yaml file

        dixonModelFileDialog = dixonModelFile()
        dixonModelFileDialog.edit()
        yamlfile = dixonModelFileDialog.dixonFileName



    elif len(sys.argv) == 2: # one cammand line argument that is a yaml file

        yamlfile = sys.argv[1]



    elif len(sys.argv) == 3: # two command line arguments, yaml file and study directory

        if ("yml" in sys.argv[1]) or ("yaml" in sys.argv[1]):
            yamlfile = sys.argv[1]
            studyDir = sys.argv[2]
        else:
            yamlfile = sys.argv[2]
            studyDir = sys.argv[1]

    if (("yml" in yamlfile) or ("yaml" in yamlfile)) and os.path.exists(yamlfile):

        dixonModelData =  AttrDict.from_file(yamlfile)
        yamlfileName = (os.path.split(yamlfile))[1]

        summarizeDixonData(dixonModelData,  yamlfileName, studyDir)
    else:

        print("\n\n", yamlfile, ":: is not a yaml file or path does not exist")
        print(command_line_args_string)



def return_groupName( subject, fitModelData, studyDescription):

    for groupName  in studyDescription.groupNames:
        if subject in studyDescription[groupName]['participants']:
            return groupName


def summarizeDixonData(dixonModelData,  yamlfileName, studyDir):

    if dixonModelData.fitSubject == []:
        useStudyDir = False
    else:
        useStudyDir = True

        if studyDir==None:

            studyDirDialog= studyDirectory()
            studyDirDialog.edit()
            studyDir_directory = studyDirDialog.directory

            studyDescription = AttrDict.from_file( os.path.join(studyDir_directory,
                                                                "study_description_file.yml"))

        else:
            studyDir_directory = studyDir
            studyDescription = AttrDict.from_file( os.path.join(studyDir_directory,
                                                                "study_description_file.yml"))

    analyzeDirectory = ["dixon"]
    roiDirectory = ["rois"]

    if useStudyDir:

        for subject in dixonModelData.fitSubject:
            groupName = return_groupName( subject, dixonModelData, studyDescription)
            for session in dixonModelData.fitSession:
                for imagedRegion in dixonModelData.fitImagedRegions:

                    if not os.path.exists( os.path.join( studyDir_directory, subject, session, imagedRegion)):
                        print(os.path.join( studyDir_directory, subject, session, imagedRegion))
                        continue


                    ###################################################################
                    # Read in ROI files
                    ###################################################################

                    for roiAuthor in dixonModelData.roiAuthorPreference:

                        directory = os.path.join(studyDir_directory, subject, session, imagedRegion,*roiDirectory, roiAuthor)
                        print("roi directory", directory)
                        if os.path.exists(directory):
                            break

                    roiFilesList = [os.path.join(directory,fn) for fn in os.listdir(directory) if ".zip" in fn ]



                    if dixonModelData.useRoiOutline:

                        roiOutlineFileList = [fn for fn in roiFilesList if  "outline" in fn ]
                        roiFile = roiOutlineFileList[0]
                        print(dixonModelData.useRoiOutline, roiFile)

                    else:

                        roiIndvidualFileList = [fn for fn in roiFilesList if dixonModelData.roiFitModel[dixonModelData.fitModel] in fn]
                        roiFile = roiIndvidualFileList[0]
                        print(dixonModelData.useRoiOutline,roiIndvidualFileList)

                    roi_set = ijroieh.read_roi_zip(roiFile)

                    ###########################################################
                    #
                    # Read in image data which can be in analyze format s
                    #
                    ###########################################################

                    directory = os.path.join(studyDir_directory, subject, session, imagedRegion,*analyzeDirectory)


                    # read in analyze data
                    print("read in analyze data")
                    AnalyzeImageFilesList = [os.path.join(directory,fn) for fn in os.listdir(directory) if (".img" in fn) and ("fatPC" in fn) ]


                    img = nibabel.load(AnalyzeImageFilesList[0])
                    imageDataDixon = img.get_data()
                    imageDataDixon =np.flipud(imageDataDixon.swapaxes(1,0))

                    nrows, ncols, nslices = imageDataDixon.shape

                    dataSet = { 'numRows':nrows, 'numCols':ncols, 'numSlices': nslices}

                    dff_list = []

                    ################################################################
                    #
                    # Loop over slices and extract Dixon data  covered by ROIs
                    #
                    ################################################################

                    for islice, roislice in zip(dixonModelData.fitSlices,dixonModelData.roiSlices):

                        dff_dict = {}

                        isliceZero=int(islice)-1
                        print("islice, isliceZero", islice, isliceZero)


                        dixonmask_index = np.arange(dataSet['numRows']*dataSet['numCols']).reshape(dataSet['numRows'],dataSet['numCols'])

                        ##########################################
                        #
                        # Return ROI mask information
                        #
                        ###########################################

    #                    if fitModelData.useRoiOutline:
    #                        mask,mask_id,roi_names = return_mask_outline( dataSet, islice, isliceZero, roi_set)
    #                    else:
    #                        mask,mask_id,roi_names = return_masks_individual( dataSet, islice, isliceZero, roi_set)

                        mask,mask_id,roi_names = return_masks_individual( dataSet, roislice,  roi_set)

                        print("roi_names", roi_names)

                        print("after masks")

                        dff_dict['roi_id'] =  mask_id[mask]
                        dff_dict['pixel_index']= dixonmask_index[mask]

                        dff_dict['fatPC']  = imageDataDixon[:,:,isliceZero][mask]


                        dff = pd.DataFrame(dff_dict)
                        dff['slice']=islice
                        dff['nrows']=dataSet['numRows']
                        dff['ncols']=dataSet['numCols']
                        dff['groupName']=groupName
                        dff['subject']=subject
                        dff['session']=session
                        dff['imagedRegion']=imagedRegion
                        dff['imagedRegionType']=dixonModelData["roiFitModel"][dixonModelData["fitModel"]]

                        roi_all_list = []

                        for i in dff.roi_id:
                            roi_all_list.append(roi_names[i-1])

                        dff['roi_name']=roi_all_list

                        dff_list.append(dff)

                    ####################################################
                    #
                    # Combine all slice pandas dataframes and save
                    #
                    #####################################################

                    dff_all = pd.concat(dff_list)
                    resultsDir = os.path.join( studyDir_directory,
                                             subject,
                                             session,
                                             imagedRegion,
                                             dixonModelData.resultsDir)

                    print("dff_all.roi_name.unique()", dff_all.roi_name.unique())

                    roi_names_all = (dff_all.roi_name.str.split('_'))

                    roi_key = []
                    for sss in roi_names_all:
                        roi_key.append(sss[-1].split('.')[0])

                    dff_all['roi']=roi_key

                    if not os.path.exists(resultsDir):
                        os.makedirs(resultsDir)

                    dff_all.to_csv(os.path.join(resultsDir,'dixon_{}_{}_{}_{}_results.csv'.format(subject,session,imagedRegion,dixonModelData.fitModel)))
                    dff_all.to_excel(os.path.join(resultsDir,'dixon_{}_{}_{}_{}_results.xls'.format(subject,session,imagedRegion,dixonModelData.fitModel)))


                    #####################################################
                    #
                    # create a summary based on ROIs and slices
                    #
                    #####################################################



                    ccc = [ 'fatPC']

                    hdr = ['roi','slice','numPixels','subject','session','imagedRegion','fitModel',  'groupName', 'imagedRegionType']


                    ccc_mean_std = []

                    for c in ccc:
                        hdr.append(c+'_mean')
                        hdr.append(c+'_std')
                        ccc_mean_std.append(c+'_mean')
                        ccc_mean_std.append(c+'_std')
                    summary = []


                    for rk in  dff_all.roi.unique():
                        data_rk =  dff_all[dff_all.roi == rk]
                        for s in data_rk.slice.unique():
                            data_slice = data_rk[data_rk.slice == s]
                            p_list=[]

                            p_list.append(rk)
                            p_list.append(s)
                            p_list.append(data_slice.slice.count())
                            p_list.append(subject)
                            p_list.append(session)
                            p_list.append(imagedRegion)
                            p_list.append(dixonModelData.fitModel)
                            p_list.append(data_slice.groupName.unique()[0])
                            p_list.append(data_slice.imagedRegionType.unique()[0])
                            for p in ccc:
                                p_list.append(data_slice[p].mean())
                                p_list.append(data_slice[p].std())

                            summary.append(p_list)

                    summary_df = pd.DataFrame(summary, columns=hdr)


                    roiAggList = []

                    for rk in  summary_df.roi.unique():

                        data_rk =  summary_df[summary_df.roi == rk]
                        s_data = (data_rk[ccc_mean_std].multiply(data_rk['numPixels'], axis="index")).sum()/data_rk['numPixels'].sum()
                        s_data['roi']=rk
                        s_data['subject']=subject
                        s_data['session']=session
                        s_data['imagedRegion']=imagedRegion
                        s_data['fitModel']=dixonModelData.fitModel
                        s_data['groupName']=data_rk.groupName.unique()[0]
                        s_data['imagedRegionType']=data_rk.imagedRegionType.unique()[0]
                        roiAggList.append(s_data)

                    roiAgg_df = pd.DataFrame(roiAggList, columns=roiAggList[0].index)

                    if not os.path.exists(dixonModelData.resultsDir):
                        os.makedirs(dixonModelData.resultsDir)
                    summary_df.to_csv(os.path.join(resultsDir,'dixon_{}_{}_{}_{}_summary.csv'.format(subject,session,imagedRegion,dixonModelData.fitModel)))
                    roiAgg_df.to_csv(os.path.join(resultsDir,'dixon_{}_{}_{}_{}_Agg_summary.csv'.format(subject,session,imagedRegion,dixonModelData.fitModel)))
                    summary_df.to_excel(os.path.join(resultsDir,'dixon_{}_{}_{}_{}_summary.xls'.format(subject,session,imagedRegion,dixonModelData.fitModel)))
                    roiAgg_df.to_excel(os.path.join(resultsDir,'dixon_{}_{}_{}_{}_Agg_summary.xls'.format(subject,session,imagedRegion,dixonModelData.fitModel)))

                    dixonModelData.dump(os.path.join(resultsDir,yamlfileName))

                    del dff_list
                    del dff_all
                    del summary_df
                    del summary

    else:

        ###################################################################
        # Read in ROI files
        ###################################################################
        if dixonModelData.useRoiOutline:
            roi_set = ijroieh.read_roi_zip(dixonModelData.roisOutline)
        else:
            roi_set = ijroieh.read_roi_zip(dixonModelData.roisIndividual)

        ###########################################################
        #
        # Read in image data which can be in analyze format s
        #
        ###########################################################



        img = nibabel.load(dixonModelData.dixonImageFile)
        imageDataDixon = img.get_data()
        imageDataDixon =np.flipud(imageDataDixon.swapaxes(1,0))

        nrows, ncols, nslices = imageDataDixon.shape

        dataSet = { 'numRows':nrows, 'numCols':ncols, 'numSlices': nslices}

        dff_list = []

        ################################################################
        #
        # Loop over slices and extract Dixon data  covered by ROIs
        #
        ################################################################

        for islice, roislice in zip(dixonModelData.fitSlices,dixonModelData.roiSlices):

            dff_dict = {}

            isliceZero=int(islice)-1
            print("islice, isliceZero", islice, isliceZero)


            dixonmask_index = np.arange(dataSet['numRows']*dataSet['numCols']).reshape(dataSet['numRows'],dataSet['numCols'])

            ##########################################
            #
            # Return ROI mask information
            #
            ###########################################

#                    if fitModelData.useRoiOutline:
#                        mask,mask_id,roi_names = return_mask_outline( dataSet, islice, isliceZero, roi_set)
#                    else:
#                        mask,mask_id,roi_names = return_masks_individual( dataSet, islice, isliceZero, roi_set)

            mask,mask_id,roi_names = return_masks_individual( dataSet, roislice,  roi_set)

            print("roi_names", roi_names)

            print("after masks")

            dff_dict['roi_id'] =  mask_id[mask]
            dff_dict['pixel_index']= dixonmask_index[mask]

            dff_dict['fatPC']  = imageDataDixon[:,:,isliceZero][mask]


            dff = pd.DataFrame(dff_dict)
            dff['slice']=islice
            dff['nrows']=dataSet['numRows']
            dff['ncols']=dataSet['numCols']

            roi_all_list = []

            for i in dff.roi_id:
                roi_all_list.append(roi_names[i-1])

            dff['roi_name']=roi_all_list

            dff_list.append(dff)

        ####################################################
        #
        # Combine all slice pandas dataframes and save
        #
        #####################################################

        dff_all = pd.concat(dff_list)
        resultsDir =  dixonModelData.resultsDir

        print("dff_all.roi_name.unique()", dff_all.roi_name.unique())

        roi_names_all = (dff_all.roi_name.str.split('_'))

        roi_key = []
        for sss in roi_names_all:
            roi_key.append(sss[-1].split('.')[0])

        dff_all['roi']=roi_key

        if not os.path.exists(resultsDir):
            os.makedirs(resultsDir)

        dff_all.to_csv(os.path.join(resultsDir,'dixon_{}_results.csv'.format(dixonModelData.fitModel)))
        dff_all.to_excel(os.path.join(resultsDir,'dixon_{}_results.xls'.format(dixonModelData.fitModel)))


        #####################################################
        #
        # create a summary based on ROIs and slices
        #
        #####################################################



        ccc = [ 'fatPC']

        hdr = ['roi','slice','numPixels','fitModel']


        ccc_mean_std = []

        for c in ccc:
            hdr.append(c+'_mean')
            hdr.append(c+'_std')
            ccc_mean_std.append(c+'_mean')
            ccc_mean_std.append(c+'_std')
        summary = []


        for rk in  dff_all.roi.unique():
            data_rk =  dff_all[dff_all.roi == rk]
            for s in data_rk.slice.unique():
                data_slice = data_rk[data_rk.slice == s]
                p_list=[]

                p_list.append(rk)
                p_list.append(s)
                p_list.append(data_slice.slice.count())
                p_list.append(dixonModelData.fitModel)
                for p in ccc:
                    p_list.append(data_slice[p].mean())
                    p_list.append(data_slice[p].std())

                summary.append(p_list)

        summary_df = pd.DataFrame(summary, columns=hdr)


        roiAggList = []

        for rk in  summary_df.roi.unique():

            data_rk =  summary_df[summary_df.roi == rk]
            s_data = (data_rk[ccc_mean_std].multiply(data_rk['numPixels'], axis="index")).sum()/data_rk['numPixels'].sum()
            s_data['roi']=rk
            roiAggList.append(s_data)

        roiAgg_df = pd.DataFrame(roiAggList, columns=roiAggList[0].index)

        if not os.path.exists(dixonModelData.resultsDir):
            os.makedirs(dixonModelData.resultsDir)
        summary_df.to_csv(os.path.join(resultsDir,'dixon_{}_summary.csv'.format(dixonModelData.fitModel)))
        roiAgg_df.to_csv(os.path.join(resultsDir,'dixon_{}_Agg_summary.csv'.format(dixonModelData.fitModel)))
        summary_df.to_excel(os.path.join(resultsDir,'dixon_{}_summary.xls'.format(dixonModelData.fitModel)))
        roiAgg_df.to_excel(os.path.join(resultsDir,'dixon_{}__Agg_summary.xls'.format(dixonModelData.fitModel)))

        dixonModelData.dump(os.path.join(resultsDir,yamlfileName))

        del dff_list
        del dff_all
        del summary_df
        del summary


if __name__ == "__main__":

    decide_what_todo()

