
# coding: utf-8




import pandas as pd
#import numpy as np

#from matplotlib import pyplot as plt

import os
import sys

import yaml
import json

#import ipywidgets
#from IPython.display import Markdown, display

#import uncertainties
#import uncertainties as un
#from uncertainties import unumpy

import PySimpleGUI as sg


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


    def __str__(self):
        return yaml.dump(self.data_dict)

    def __repr__(self):

        return (yaml.dump(self.data_dict)).__repr__()


if __name__ == "__main__":

    if len(sys.argv) == 1:
        aggExcelYamlFilename=sg.PopupGetFile("Enter AGG Excel YAML file")
    elif len(sys.argv) == 2:
        aggExcelYamlFilename = sys.argv[-1]
    else:
        print("command line arguments incorrect: ", end=' ')
        for v in sys.argv:
            print(v, end=' ')
        print()
        print("command line should be either :: 'python programName.py  OR python programName.py yamlFileName.yml")
        print("Program quiting")
        sys.exit()


    if (".yml" not in aggExcelYamlFilename) and (".yaml" not in aggExcelYamlFilename):
        print( aggExcelYamlFilename, "not a yaml file program quitting")
        sys.exit()

    if not os.path.exists( aggExcelYamlFilename):
        print(aggExcelYamlFilename, " not Found")
        print("Program quiting")
        sys.exit()

    aggExcelYamlFile = AttrDict.from_file(aggExcelYamlFilename)

    studyDir = aggExcelYamlFile.studyDir
    fn = os.path.join(studyDir,"study_description_file.yml")

    studyDirStructure = AttrDict.from_file(fn)

    print(studyDirStructure)



    # ### Find all summary aggregate files for a given fit model and MRI protocol


    protocol =         aggExcelYamlFile.protocol
    fitModel =         aggExcelYamlFile.fitModel    #"EPGAZZ"
    imagedRegionType = aggExcelYamlFile.imagedRegionType  # "muscle"
    excelParams =      aggExcelYamlFile.excelParams     # ["T2m_mean", "Am100_mean"]


    dataList = []
    for grpNme in studyDirStructure.groupNames:
        print(grpNme)
        for participant in studyDirStructure[ grpNme]['participants']:
            for session in studyDirStructure[ grpNme]['sessions']:
                for imagedRegion in studyDirStructure[ grpNme]['imagedRegions']:
                    dirName = os.path.join(studyDir,participant,session, imagedRegion, protocol, "results", imagedRegionType,fitModel)
                    if os.path.exists(dirName):
                        filesFoundList = [ os.path.join(dirName, fn) for fn in os.listdir(dirName) if (".csv" in fn) and ("Agg" in fn)]
                        if len(filesFoundList)>0:
                            print(os.path.join(dirName,filesFoundList[0]))
                            dataList.append( [grpNme,participant,session, imagedRegion, imagedRegionType, protocol, fitModel,True,os.path.join(dirName,filesFoundList[0])])
                        else:
                            dataList.append( [grpNme,participant,session, imagedRegion, imagedRegionType, protocol, fitModel,False,"empty"])
                    else:
                        dataList.append( [grpNme,participant,session, imagedRegion, imagedRegionType, protocol, fitModel, False, "empty"])


    data_df = pd.DataFrame(dataList, columns=['groupName','subject','session','imagedRegion', 'imagedRegionType','protocol','fitModel','fileFound','resultsFile'])
    # ### Open one Agg file to obtain column names

    print("Total Files Found ::", (data_df.shape)[0])
    print("Total Files Found with Data Present", ((data_df[data_df.fileFound]).shape)[0])

    if ((data_df[data_df.fileFound]).shape)[0] == 0:
        print("############################################")
        print("No Results Files found in Study")
        print("Program quitting")
        sys.exit()

    print(data_df["resultsFile"].head())

    print("###############\ndata_df[data_df.fileFound].resultsFile[0]\n######################")
    print(list(data_df[data_df.fileFound].resultsFile)[0])



    singleAgg_df = pd.read_csv(list(data_df[data_df.fileFound].resultsFile)[0])


#    fitResults = {}
#    for colName in singleAgg_df.columns:
#        if '_mean' in colName:
#            paramName, paramType = colName.split('_')
#            fitResults[paramName]=[colName, paramName+'_std']


    fitParamResults = {}
    fitMetaParams = []
    for colName in singleAgg_df.columns:
        if '_mean' in colName:
            paramName, paramType = colName.split('_')
            fitParamResults[paramName]=[colName, paramName+'_std']
        elif '_std' not in colName:
            if "Unnamed" in colName:
                continue
            print(colName)
            fitMetaParams.append(colName)

    print("fitMetaParams",fitMetaParams)
    # ### Read in Data from Agg summary files inserting zeros for missing data so we can have a complete table




    df_list = []
    for index, row in data_df.iterrows():

        print()
        print(index, end = ' ')
        if row.fileFound:
            resultsDir, resultsName = os.path.split(row.resultsFile)
            df_agg = pd.read_csv(row.resultsFile)

            for indexAgg,rowAgg in df_agg.iterrows():
                rowList=[]
                for metaParam in fitMetaParams:
                    rowList.append(rowAgg[metaParam])
#                rowList = [rowAgg.roi,
#                           rowAgg.subject,
#                           rowAgg.session,
#                           rowAgg.imagedRegion,
#                           rowAgg.fitModel,
#                           rowAgg.groupName]
                for p in fitParamResults.keys():
                    rowList.append(rowAgg[fitParamResults[p][0]])
                    rowList.append(rowAgg[fitParamResults[p][1]])
                print(len(rowList), row.fileFound, end=' ')
                df_list.append(rowList)

        else:

            for roi in studyDirStructure[row.groupName]['rois'][row.imagedRegion][imagedRegionType]:
                rowList = []
                rowList.append(roi)
                for metaParam in fitMetaParams:
                    if metaParam == 'roi':
                        pass
#                    elif metaParam == 'subject':
#                        rowList.append(row.participant)
                    else:
                        rowList.append(row[metaParam])
#                rowList = [roi,
#                           row.groupName,
#                           row.participant,
#                           row.session,
#                           row.imagedRegion,
#                           row.fitModel,
#                           ]
                print(len(rowList), row.fileFound, end=' ')
                for p in fitParamResults.keys():
                    rowList.append(0.0)
                    rowList.append(0.0)
                print(len(rowList), row.fileFound, end=' ')
                df_list.append(rowList)





    columnsList = fitMetaParams.copy()
    for p in fitParamResults.keys():
        columnsList.append(fitParamResults[p][0])
        columnsList.append(fitParamResults[p][1])

    print("columnsList ::",columnsList)
    agg_df = pd.DataFrame(df_list, columns=columnsList)


    # ### Create Excel data sheets in terms of sessions and subjects

    print("agg_df.shape",agg_df.shape)

    print()

    with pd.ExcelWriter(aggExcelYamlFile.outputFile) as writer:

        for grpNme in studyDirStructure.groupNames:

            agg_participants_df = agg_df[agg_df['groupName']==grpNme]

            print("agg_participants_df.shape",agg_participants_df.shape)


            for imagedRegion in studyDirStructure[ grpNme]['imagedRegions']:
                for roi in studyDirStructure[ grpNme]['rois'][imagedRegion][imagedRegionType]:

                    session_df =agg_participants_df.query("imagedRegion=='{}' and roi=='{}'".format(imagedRegion, roi))
#                    pivot_df = session_df.pivot(index='subject',columns='session', values=['T2m_mean', 'T2m_std', 'Am100_mean'])
                    pivot_df = session_df.pivot(index='subject',columns='session', values=excelParams)
    #                     print(pivot_df.round(2))

                    sheetname = "{}_{}_{}".format(grpNme, imagedRegion, roi)
                    print(sheetname, pivot_df.shape)
                    pivot_df.round(2).to_excel(writer, sheet_name=sheetname)




#    import PySimpleGUI as sg

#
#    ret = sg.PopupYesNo('This is my first Popup')
#    print(ret)
#
#
#
#
#    sg.PopupScrolled(studyDirStructure)

