# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 10:03:40 2019

@author: ERIC
"""



import yaml
import sys
import os

import guidata
_app = guidata.qapplication() # not required if a QApplication has already been created

import guidata.dataset.datatypes as dt
import guidata.dataset.dataitems as di

class StudyDescriptionName(dt.DataSet):
    """Study Name"""
    studyName = di.DirectoryItem("Study Name", default='ggg')

class NumParticipantGroups(dt.DataSet):
    """Enter the number of participant groups of participants in the study
    This can be patients and volunteers and then split into further groups
    if they participate different number of sessions or have different
    regions imaged"""
    numGroups = di.IntItem("Number of participant groups", default=2)


class StudyProtocolNames( dt.DataSet):

    protocolNames = di.StringItem("Protocol Names", default="T2 dixon")

class RoiAuthorInitials( dt.DataSet):

    authorInitials = di.StringItem("Roi Author Initials", default="KGH EH")

class StudyDescription:

    def __init__(self):

        if os.path.exists("study_description_file.yml"):
            fp = open("study_description_file.yml", "r")
            self.oldStudyDescriptyionDict = yaml.load(fp)
            fp.close()
        else:
            self.oldStudyDescriptyionDict=None
        pass


def create_fillinGroupNames(study):

    data = {}


    print(study.numGroups)
    for i in range(study.numGroups):
        data['g'+str(i)] =  di.StringItem("group {} name ".format(i+1), default="group{}".format(i+1)).set_pos(col=0, colspan=2)
#        data['np'+str(i)] =  di.IntItem("# particpipants ", default=10).set_pos(col=1, colspan=2)

        data['s'+str(i)] =  di.IntItem("Number of Sessions ".format(i+1), default=3).set_pos(col=3, colspan=2)
#        sessions['s'+str(i)]= data['s'+str(i)]
        data['ir'+str(i)] =  di.StringItem("Imaged Regions  ".format(i+1), default='lowerleg   upperleg').set_pos(col=4, colspan=2)
#        imagedRegions['ir'+str(i)]= data['ir'+str(i)]

    clz = type("Dialog", (dt.DataSet,), data)

    dlg = clz()
    okay =dlg.edit()

    if not okay:
        sys.exit()

    study.groups = {}

    for i in range(study.numGroups):
        print(dlg.__dict__['_g'+str(i)])
        study.groups[dlg.__dict__['_g'+str(i)]] = {'name'        : dlg.__dict__['_g'+str(i)],
                                                   'numSessions' : dlg.__dict__['_s'+str(i)],}

        if ',' in dlg.__dict__['_ir'+str(i)]:
            study.groups[dlg.__dict__['_g'+str(i)]]['imagedRegions']= (dlg.__dict__['-ir'+str(i)]).split(',')

        else:
            study.groups[dlg.__dict__['_g'+str(i)]]['imagedRegions']= (dlg.__dict__['_ir'+str(i)]).split()


def create_fillinParticipantNames(study):

    data = {}

    for i,k in enumerate(list(study.groups.keys())):
        print(i,k)

        data[k] = di.TextItem(k, help="add one name per line", default="eric\nbill").set_pos(col=i, colspan=2)

    clz = type("Add partipicipant Names", (dt.DataSet,), data)
    dlg = clz()
    okay =dlg.edit()

    if not okay:
        sys.exit()

    for i,k in enumerate(list(study.groups.keys())):
        print(k, dlg.__dict__['_'+k].splitlines())
        study.groups[k]['participants']=dlg.__dict__['_'+k].splitlines()

        study.groups[k]['participants'] = [v for v in study.groups[k]['participants'] if '' != v ]


def create_fillinRoiTypes(study, groupName):

    data = {}

    help_str = """Add one ROI type name per line
    examples are muscle, fat outline phantom"""

    for i,k in enumerate(study.groups[groupName]['imagedRegions']):
        print(i,k)
        data[k] = di.TextItem(k, help=help_str, default="muscle\nfat\noutline").set_pos(col=i, colspan=2)

    clz = type("Add ROI Types per imaged region for {}".format(groupName), (dt.DataSet,), data)
    dlg = clz()
    okay =dlg.edit()

    if not okay:
        sys.exit()

    print("create_fillinRoiTypes", dlg.__dict__.keys())

    study.groups[groupName]['rois']={}
    for imagedRegion in study.groups[groupName]['imagedRegions']:
        print(imagedRegion, dlg.__dict__['_'+imagedRegion].splitlines())
        study.groups[groupName]['rois'][imagedRegion]={}

        for roiTypes in dlg.__dict__['_'+imagedRegion].splitlines():

            study.groups[groupName]['rois'][imagedRegion][roiTypes]={}




def create_fillinRoiLabels(study):

    data = {}

    for groupName in list(study.groups.keys())[0:1]:
        print("groupName",groupName)
        for imagedRegion in study.groups[groupName]['rois'].keys():
            for roiType in study.groups[groupName]['rois'][imagedRegion].keys():

                idstr = "{}_{}".format(imagedRegion,roiType)

                if roiType=='outline':
                    roiLabelsStr = '1'
                elif roiType=='fat':
                    roiLabelsStr = '1 2 3 4 5'
                else:
                    roiLabelsStr = ""


                data[idstr]=di.StringItem(idstr.replace('_', ' '), help="add Roi name separated by spaces", default=roiLabelsStr).set_pos(col=0, colspan=4)

    clz = type("Add ROI labels per imaged region and Roi type", (dt.DataSet,), data)
    dlg = clz()
    okay =dlg.edit()

    if not okay:
        sys.exit()

    for groupName in study.groups.keys():
        for imagedRegion in study.groups[groupName]['rois'].keys():
            for roiType in study.groups[groupName]['rois'][imagedRegion].keys():
                idstr = "{}_{}".format(imagedRegion,roiType)

                study.groups[groupName]['rois'][imagedRegion][roiType]=dlg.__dict__['_'+idstr].split()



def create_slicesToBeUsed(study):

    data = {}

    for groupName in study.groups.keys():

        study.groups[groupName]['slices']={}

        for imagedRegion in study.groups[groupName]['rois'].keys():

            study.groups[groupName]['slices'][imagedRegion]={}

            for imagedRegionType in study.groups[groupName]['rois'][imagedRegion].keys():

                study.groups[groupName]['slices'][imagedRegion][imagedRegionType]={}

                for protocol in study.protocols:
                    study.groups[groupName]['slices'][imagedRegion][imagedRegionType][protocol]=[]


    for groupName in list(study.groups.keys())[0:1]:
        for imagedRegion in study.groups[groupName]['slices'].keys():
            for imagedRegionType in study.groups[groupName]['slices'][imagedRegion].keys():
                for protocol in study.groups[groupName]['slices'][imagedRegion][imagedRegionType].keys():

                    idstr = "{}_{}_{}".format(imagedRegion,imagedRegionType, protocol)

                    if imagedRegionType=="fat":
                        sliceLabelStr = "2"
                    else:
                        sliceLabelStr = "1 2 3"

                    data[idstr]=di.StringItem(idstr.replace('_', ' '), help="add slice index separated by spaces", default=sliceLabelStr).set_pos(col=0, colspan=4)
#
    clz = type("Add slice index per imaged region, imaged region type and protocol", (dt.DataSet,), data)
    dlg = clz()
    okay =dlg.edit()

    if not okay:
        sys.exit()

    for groupName in study.groups.keys():
        for imagedRegion in study.groups[groupName]['slices'].keys():
            for imagedRegionType in study.groups[groupName]['slices'][imagedRegion].keys():
                for protocol in study.groups[groupName]['slices'][imagedRegion][imagedRegionType].keys():

                    idstr = "{}_{}_{}".format(imagedRegion,imagedRegionType, protocol)

                    study.groups[groupName]['slices'][imagedRegion][imagedRegionType][protocol]=dlg.__dict__['_'+idstr].split()



if __name__ == "__main__":

    study = StudyDescription()



    studyDescriptionNameDialog =StudyDescriptionName()
    okay=studyDescriptionNameDialog.edit()
    if not okay:
        sys.exit()
    print("studyName =", studyDescriptionNameDialog.studyName)

    study.studyName = studyDescriptionNameDialog.studyName

    numParticipantGroupsDialog = NumParticipantGroups()
    okay=numParticipantGroupsDialog.edit()
    if not okay:
        sys.exit()
    print("okay", okay, "numGroups", numParticipantGroupsDialog.numGroups)

    study.numGroups = numParticipantGroupsDialog.numGroups

    studyProtocolNamesDialog = StudyProtocolNames()
    okay=studyProtocolNamesDialog.edit()
    if not okay:
        sys.exit()

    study.protocols = studyProtocolNamesDialog.protocolNames.split()



    roiAuthorInitialsDialog = RoiAuthorInitials()
    okay= roiAuthorInitialsDialog.edit()
    if not okay:
        sys.exit()

    study.roiAuthors = roiAuthorInitialsDialog.authorInitials.split()



    create_fillinGroupNames(study)



    create_fillinParticipantNames(study)

    for groupName in study.groups.keys():

        create_fillinRoiTypes(study,groupName)

    create_fillinRoiLabels(study)

    for groupName in study.groups.keys():

        session_list = []

        for i in range(study.groups[groupName]['numSessions']):
            session_list.append( "sess-{}".format(i+1))

        study.groups[groupName]['sessions']=session_list

    create_slicesToBeUsed(study)



    studyDescriptionDict = {}
    studyDescriptionDict['groupNames']=list(study.groups.keys())
    for k,v in study.groups.items():
        studyDescriptionDict[k]=v

    studyRootDir, studyNameOnly = os.path.split(study.studyName)
    studyDescriptionDict['roiAuthors']= study.roiAuthors
    studyDescriptionDict['studyName']=studyNameOnly
    studyDescriptionDict['studyRootDir']=studyRootDir

    studyDescriptionDict['protocols']=study.protocols
    studyDescriptionDict['principalInvestigators']=[{'name': '', 'email':'', 'address':'', 'initials':''}]
    studyDescriptionDict['researchAssociates']=[{'name': '', 'email':'', 'address':'', 'initials':''}]
    studyDescriptionDict['students']=[{'name': '', 'email':'', 'address':'', 'initials':''}]

    print(yaml.dump(studyDescriptionDict))

    fp = open( os.path.join(studyRootDir, studyNameOnly, 'study_description_file.yml'), 'w')
    yaml.dump(studyDescriptionDict, fp)
    fp.close()








