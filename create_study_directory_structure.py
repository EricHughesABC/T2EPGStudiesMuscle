# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 10:22:18 2018

@author: neh69
"""

#import json
import yaml
import os
import sys

import zipfile
import ijroieh

import guidata
_app = guidata.qapplication() # not required if a QApplication has already been created

import guidata.dataset.datatypes as dt
import guidata.dataset.dataitems as di

class studyDirectory(dt.DataSet):
    """Define Study Root Directory

    Enter Study Directory  in dialog"""

    directory = di.DirectoryItem("Study Dir:")



if __name__ == "__main__":

    if "win" not in sys.platform:

        print("Only works on windows for the minute")
        sys.exit()

    studyDirDialog= studyDirectory()
    okay=studyDirDialog.edit()


    cancelExplanation = """

+--------------------------------------------+
|                                            |
|  Cancel Button Pressed in StudyDir Dialog  |
|                                            |
|  Program Quiting                           |
|                                            |
+--------------------------------------------+

"""
    if not okay:
        print( cancelExplanation)
        sys.exit()

    # read in json study description file

    ymlStudyDescriptionFile = os.path.join(studyDirDialog.directory,"study_description_file.yml")

    fp = open(ymlStudyDescriptionFile, 'r')

    study = yaml.load(fp)

    fp.close()

    print(study)

    # find study root directory

#    if "win" in sys.platform:
#        rootDir = study['rootDirectory']['windows']
#    else:
#        rootDir = study['rootDirectory']['linux']
#    print("rootDir\n",rootDir)

    # find study directory from json study description file

#    studyDir = os.path.join(rootDir,os.path.sep,study['studyName'])
    studyDir = studyDirDialog.directory

    if study['studyName'] not in studyDir:
        print( "miss-match in study directory chosen and study name in study description file")
        print( "Program quitting")
        sys.exit()

    # make directory structure

    #
    # For study participants
    #

    for  groupName in study['groupNames']:
        for participant in study[groupName]['participants']:
            for session in study[groupName]['sessions']:


#
                for  imagedRegion in study[groupName][ 'imagedRegions']:
                    print(groupName, participant, session, imagedRegion)

                    os.makedirs(os.path.join(studyDir,participant,session,imagedRegion), exist_ok=True)
                    os.makedirs(os.path.join(studyDir,participant,session,imagedRegion,'rois'), exist_ok=True)
                    os.makedirs(os.path.join(studyDir,participant,session,imagedRegion,'dicom'), exist_ok=True)

                    for protocol in study['protocols']:
                        os.makedirs(os.path.join(studyDir,participant,session,imagedRegion,protocol), exist_ok=True)

                    for roiAuthor in study['roiAuthors']:
                        os.makedirs(os.path.join(studyDir,participant,session,imagedRegion,'rois',roiAuthor), exist_ok=True)



    for  groupName in study['groupNames']:
        for participant in study[groupName]['participants']:
            for session in study[groupName]['sessions']:
                for  imagedRegion in study[groupName]['rois'].keys():
                    for imagedRegionType, roiLabels in study[groupName]['rois'][imagedRegion].items():
                        for author in study['roiAuthors']:
                            zipName = "{}_{}_{}_{}_{}.zip".format(author,participant,session,imagedRegion, imagedRegionType,'T2' )
                            print("\t",zipName)

                            roiPath=os.path.join(studyDir,participant, session, imagedRegion, 'rois', author)

                            print(roiPath, os.path.exists(roiPath))
                            if not os.path.exists(os.path.join(roiPath,zipName)):

                                zf = zipfile.ZipFile(os.path.join(roiPath,zipName), mode='w')

                                for islice in study[groupName]['slices'][imagedRegion][imagedRegionType]['T2']:

                                    for roiLabel in roiLabels:
                                        roiName = "{}_slice-{}_{}_{}_{}_{}_{}_{}.roi".format(author,islice,participant,session,imagedRegion, imagedRegionType,'T2',roiLabel )


                                        print(roiName)
                                        zf.writestr(roiName, ijroieh.polygon_roi)
                                zf.close()


    #
    # Create ROI templates for T2 only
    #
#    for dirPath, listOfDirs, listOfFiles in os.walk(studyDir):
#
#        dirPathList = dirPath.split( os.path.sep)
#        if len(dirPathList)==1:
#            dirPathList = dirPath.split( os.path.altsep)
#
#
#        if 'rois' in dirPathList[-2]:
#            print( "dirPathList", dirPathList)
#
#            roiAuthor = dirPathList[-1]
#            rois = dirPathList[-2]
#            imagedRegion=dirPathList[-3]
#            session=dirPathList[-4]
#            participant=dirPathList[-5]
#            studyName = dirPathList[-6]
#
#            for groupName in study['groupNames']:


