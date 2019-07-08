


import yaml
import json
import ijroieh
import os
import sys
import pulseProfile
import nibabel

from skimage.draw import ( polygon,ellipse)


import numpy as np
from scipy import integrate

import pandas as pd
from matplotlib import pyplot as plt


from multiprocessing import Pool

import lmfit as lm
from epg import cpmg_epg_b1 as cpmg_epg_b1_c



import guidata
_app = guidata.qapplication() # not required if a QApplication has already been created

import guidata.dataset.datatypes as dt
import guidata.dataset.dataitems as di


def plot_results( pixel_index, roi_index, roi_name, fit_model, results, fitModel):
    """plots a fit for a specific pixel giving the intial guess and final result
    in two xy plots

    Parameters
    ----------

    pixel_index: int
    roi_index: int
    roi_name: str
    fit_model: str
    results: lmfit.minimizer
    fitModel: lmfit.fitModel

    Returns
    -------

    None
    """

    nechos =fitModel.userargs[-1].shape[0]
    echo = fitModel.params['echo'].value

    paramsInitGuess = fitModel.params.copy()
    paramsFinalResult = results.params.copy()

    T2m = paramsFinalResult['t2_m'].value

    paramsInitGuessMuscle = paramsInitGuess.copy()
    paramsInitGuessMuscle['A_f'].value=0.0

    paramsInitGuessFatTotal = paramsInitGuess.copy()
    paramsInitGuessFatTotal['A_m'].value=0.0

    paramsInitGuessFatLong = paramsInitGuess.copy()
    paramsInitGuessFatLong['A_m'].value=0.0
    paramsInitGuessFatLong['c_s'].value=0.0

    paramsInitGuessFatShort = paramsInitGuess.copy()
    paramsInitGuessFatShort['A_m'].value=0.0
    paramsInitGuessFatShort['c_l'].value=0.0

    paramsFinalResultMuscle = paramsFinalResult.copy()
    paramsFinalResultMuscle['A_f'].value=0.0

    paramsFinalResultFatTotal = paramsFinalResult.copy()
    paramsFinalResultFatTotal['A_m'].value=0.0

    paramsFinalResultFatLong = paramsFinalResult.copy()
    paramsFinalResultFatLong['A_m'].value=0.0
    paramsFinalResultFatLong['c_s'].value=0.0

    paramsFinalResultFatShort = paramsFinalResult.copy()
    paramsFinalResultFatShort['A_m'].value=0.0
    paramsFinalResultFatShort['c_l'].value=0.0

    yyy_InitGuessAll = fitModel.userfcn( paramsInitGuess,   *(fitModel.userargs[:-1]))
    yyy_InitGuessMuscle = fitModel.userfcn( paramsInitGuessMuscle,   *(fitModel.userargs[:-1]))
    yyy_InitGuessFatTotal  = fitModel.userfcn( paramsInitGuessFatTotal, *(fitModel.userargs[:-1]))
    yyy_InitGuessFatLong   = fitModel.userfcn( paramsInitGuessFatLong,  *(fitModel.userargs[:-1]))
    yyy_InitGuessFatShort  = fitModel.userfcn( paramsInitGuessFatShort, *(fitModel.userargs[:-1]))

    yyy_FinalResultAll       = fitModel.userfcn( paramsFinalResult,   *(fitModel.userargs[:-1]))
    yyy_FinalResultMuscle    = fitModel.userfcn( paramsFinalResultMuscle,   *(fitModel.userargs[:-1]))
    yyy_FinalResultFatTotal  = fitModel.userfcn( paramsFinalResultFatTotal, *(fitModel.userargs[:-1]))
    yyy_FinalResultFatLong   = fitModel.userfcn( paramsFinalResultFatLong,  *(fitModel.userargs[:-1]))
    yyy_FinalResultFatShort  = fitModel.userfcn( paramsFinalResultFatShort, *(fitModel.userargs[:-1]))

    ttt = np.linspace(echo,echo*nechos,nechos)

    fig,ax = plt.subplots(1,2, figsize=(12,5), sharey=False)
    ax = ax.flatten()
    ax[0].plot(ttt, fitModel.userargs[-1],'o', label='data')
    ax[1].plot(ttt, fitModel.userargs[-1],'o', label='data')

    if fit_model.lower() != "azzabou":
        ttt1 = ttt
    else:
        ttt1 = ttt[2:]

    ax[0].plot(ttt1, yyy_InitGuessAll,'-', label='fit')
    ax[0].plot(ttt1, yyy_InitGuessMuscle,'-', label='t2_m')
    ax[0].plot(ttt1, yyy_InitGuessFatTotal,'-', label='Af(c_l+c_s)')
    ax[0].plot(ttt1, yyy_InitGuessFatLong,'-', label='c_l')
    ax[0].plot(ttt1, yyy_InitGuessFatShort,'-', label='c_s')
    ax[0].legend()
    ax[0].set_title("Initial Guess")

    ax[1].plot(ttt1, yyy_FinalResultAll,'-', label='fit')
    ax[1].plot(ttt1, yyy_FinalResultMuscle,'-', label='t2_m')
    ax[1].plot(ttt1, yyy_FinalResultFatTotal,'-', label='Af(c_l+c_s)')
    ax[1].plot(ttt1, yyy_FinalResultFatLong,'-', label='c_l')
    ax[1].plot(ttt1, yyy_FinalResultFatShort,'-', label='c_s')
    ax[1].legend()

    if fit_model in ["AzzEPG","muscleEPG1","muscleEPG2","Azzabou"]:
        Am100 = 100*paramsFinalResult['A_m'].value/(paramsFinalResult['A_m'].value+paramsFinalResult['A_f'].value)
        Af100 = 100-Am100
        ax[1].set_title("Final Result {}\n\nmuscle % {:.1f}, fat % {:.1f},  T2 muscle {:.1f} ms".format(fit_model, Am100, Af100, T2m))
    elif fit_model in ["phantomEPG1", "phantomEPG2"]:
        Am100 = 100*paramsFinalResult['A_m'].value/(paramsFinalResult['A_m'].value+paramsFinalResult['A_f'].value)
        Af100 = 100-Am100
        ax[1].set_title("Final Result {}\n\ncomponent 1 % {:.1f}, component 2 % {:.1f},  T2 muscle {:.1f} ms".format(fit_model, Am100, Af100, T2m))
    elif fit_model in ["fatEPG1", "fatEPG2"]:
        cl100 = 100*paramsFinalResult['c_l'].value/(paramsFinalResult['c_l'].value+paramsFinalResult['c_s'].value)
        cs100 = 100-cl100
        T2fl = paramsFinalResult['t2_fl'].value
        T2fs = paramsFinalResult['t2_fs'].value
        ax[1].set_title("Final Result {}\n\nfat long % {:.1f}, fat short % {:.1f},  fat long {:.1f} fat short {:.1f}ms".format(fit_model, cl100, cs100, T2fl,T2fs))


def return_dataframe(ddd, fitT2, islice):
    """takes fit results from map/pool output and creates a pandas dataframe

    Parameters
    ----------

    ddd: list
        list of results
        [[pixel_index: int,
          roi_index: int,
          roi_name: str,
          fit_modelName: str,
          results: structure returned from lm.minimize(),
          fitModel: structure],]

    fitT2: dictatrs object
        parameters of fit

    islice: int
        slice index of image data set being processed

    Returns
    -------

    dff: Pandas dataframe
        table of fit results from all voxels in pandas dataframe format
    """


    results=[]

    for d in ddd:
        res = d[4]
        try:
            t1_f =res.params['T1_f'].value
        except:
            t1_f = 1.0
        try:
            t1_m =res.params['T1_m'].value
        except:
            t1_m = 1.0
        try:
            b1 = res.params['B1'].value
        except:
            b1= 1.0

        results.append([d[0],
                        d[1],
                        d[2],
                        d[3],
                        res.params['t2_m'].value,
                        res.params['t2_fl'].value,
                        res.params['t2_fs'].value,
                        t1_f,
                        t1_m,
                        res.params['A_f'].value,
                        res.params['A_m'].value,
                        res.params['c_l'].value,
                        res.params['c_s'].value,


                        b1,
                        res.params['echo'].value,
                        res.chisqr,
                        res.redchi,
                        res.aic,
                        res.bic,
                        fitT2['dx']
                        ])

    dff = pd.DataFrame(results, columns=('pixel_index',
                                         'roi_index',
                                         'roi_name',
                                         'fit_model',
                                         'T2m',
                                         'T2fl',
                                         'T2fs',
                                         'T1f',
                                         'T1m',
                                         'Af',
                                         'Am',
                                         'cl',
                                         'cs',
                                         'B1',
                                         'echo',
                                         'rss',
                                         'rchi',
                                         'AIC',
                                         'BIC',
                                         'dx'))

    dff['Am100']=100.0*dff.Am/(dff.Am+dff.Af)
    dff['Af100']=100.0-dff.Am100


    dff['cl100']=100.0*dff.cl/(dff.cl+dff.cs)
    dff['cs100']=100.0-dff.cl100

    dff['slice']=islice
    return dff




def fit_T2EPGCPMG(pool_params):
    """Function that fits a dataset

    Parameters
    ----------

    pool_params: List
        Contains information needed to fit data

        m: int
            pixel index
        yyy: np.ndarray float
            1-D experimental T2 data of size Nechos
        m_id: int
            index into roiName identifying roi used
        roiName: list of str
            list of stings identifying the roi used to obtain experimental data
        ppp: lm.Parameters
            strucure holding information about the parameters in the fit which
            are varied and which are not
        Nechos: int
            Number of points in experimental data
        dx: float
            Scaling factor used druing integration across puls profile
        p90_array: np.ndarray
            profile of 90 degree excitation pulse
        p180_array: np.ndarray
            profile of 180 degreerefocussing pulse
        fit_modelName: str
            name of model used in the fit

    Returns
    -------

    m: int
        pixel index
    m_id: int
        roiName index
    roiName[m_id]: str
        string identifying ROI used
    fit_modelName: str
        name of model used in fit
    results: lmfit object
        results from calling lmfit.minimize()
    fitModel: lmfit object
        model structure used by lmfit module
    """

    m, yyy, m_id, roiName, ppp, Nechos, dx,   p90_array, p180_array, fit_modelName = pool_params

    yyy = yyy/yyy.max()
    fitModel = lm.Minimizer(cpmg_epg_genint, ppp, fcn_args=( fit_modelName, Nechos, dx,  p90_array, p180_array, yyy))
    results  = fitModel.minimize()

    return(m, m_id, roiName[m_id-1], fit_modelName, results, fitModel)


def cpmg_epg_genint( params,  fit_modelName, Nechos,  dx, p90_array, p180_array, yyy_exp=None):
    """
    Function that generates fitting data depending on the model passed into it

    Parameters
    ----------

    params: lm.Parameters
        strucure holding information about the parameters in the fit which
        are varied and which are not
    fit_modelName: str
        name of model used in fit
    Nechos: int
        Number of points in experimental data
    dx: float
        Scaling factor used druing integration across puls profile
    p90_array: 1-D np.ndarray
        profile of 90 degree excitation pulse
    p180_array: 1-D np.ndarray
        profile of 180 degreerefocussing pulse
    yyy_exp=None: 1-D np.ndarray
        experimental T2 data of size Nechos


    Returns
    -------

    int_signal: 1-D np.ndarray of floats of length Nechos
        if yyy_exp == None
    int_signal-yyy_exp: 1-D np.ndarray of floats of length Nechos
        if yyy_exp != None
    """

    parvals  = params.valuesdict()

    if fit_modelName.lower() == "azzabou":

        echo  = parvals[ 'echo' ]
        t2_m  = parvals[ 't2_m' ]
        t2_fl = parvals['t2_fl' ]
        t2_fs = parvals['t2_fs' ]
        A_f   = parvals[ 'A_f'  ]
        A_m   = parvals['A_m'   ]
        c_s   = parvals['c_s'   ]
        c_l   = parvals['c_l'   ]
    else:

        t1_f  = parvals[ 'T1_f' ]
        t1_m  = parvals[ 'T1_m' ]
        echo  = parvals[ 'echo' ]
        t2_m  = parvals[ 't2_m' ]
        t2_fl = parvals['t2_fl' ]
        t2_fs = parvals['t2_fs' ]
        A_f   = parvals[ 'A_f'  ]
        A_m   = parvals['A_m'   ]
        c_s   = parvals['c_s'   ]
        c_l   = parvals['c_l'   ]
        B1    = parvals['B1'    ]

    Ngauss = p90_array.shape[0]
    xxx = np.linspace(echo,echo*Nechos, Nechos)
    signal        = np.zeros([Ngauss,Nechos])
    signal_muscle    = np.zeros(Nechos)
    signal_fatlong = np.zeros(Nechos)
    signal_fatshort = np.zeros(Nechos)

    for i,(p90,p180) in enumerate(zip(p90_array,p180_array)):

        if fit_modelName.lower() == "azzepg":
            cpmg_epg_b1_c( signal_fatshort,   p90, p180, t1_f,    t2_fs,    echo, B1 )
            cpmg_epg_b1_c( signal_fatlong,    p90, p180, t1_f,    t2_fl,    echo, B1 )
            cpmg_epg_b1_c( signal_muscle,     p90, p180, t1_m,    t2_m,     echo, B1 )
            signal[i] = A_f*(c_l*signal_fatlong+c_s*signal_fatshort)+A_m*signal_muscle

        elif (fit_modelName.lower() == "muscleEPG1".lower() or
             fit_modelName.lower() == "muscleEPG2".lower() or
             fit_modelName.lower() == "phantomEPG2".lower()):

            cpmg_epg_b1_c( signal_fatlong,    p90, p180, t1_f,    t2_fl,    echo, B1 )
            cpmg_epg_b1_c( signal_muscle,     p90, p180, t1_m,    t2_m,     echo, B1 )
            signal[i] = A_f*signal_fatlong+A_m*signal_muscle

        elif fit_modelName.lower() == "fatEPG1".lower():
            cpmg_epg_b1_c( signal_fatlong,    p90, p180, t1_f,    t2_fl,    echo, B1 )
            signal[i] = c_l*signal_fatlong

        elif fit_modelName.lower() == "fatEPG2".lower():
            cpmg_epg_b1_c( signal_fatlong,    p90, p180, t1_f,    t2_fl,    echo, B1 )
            cpmg_epg_b1_c( signal_fatshort,   p90, p180, t1_f,    t2_fs,    echo, B1 )
            signal[i] = c_l*signal_fatlong+c_s*signal_fatshort

        elif fit_modelName.lower() == "phantomEPG1".lower():
            cpmg_epg_b1_c( signal_muscle,     p90, p180, t1_m,    t2_m,     echo, B1 )
            signal[i] = A_m*signal_muscle

        elif fit_modelName.lower() == "Azzabou".lower():
            azz_signal = A_f * (c_l*np.exp(-xxx/t2_fl)+c_s*np.exp(-xxx/t2_fs)) + A_m * (np.exp(-xxx/t2_m))


        else:
            print("{} fit model unknown".format(fit_modelName))
            print("Quiting program")
            sys.exit()

    if fit_modelName.lower() == "Azzabou".lower():
        int_signal = azz_signal
    else:
        int_signal = integrate.simps(signal, dx=dx,axis=0)


    if isinstance(yyy_exp, np.ndarray):
        if fit_modelName.lower() == "Azzabou".lower():
            return(int_signal[2:]-yyy_exp[2:])
        else:
            return( int_signal-yyy_exp)
    else:
        if fit_modelName.lower() == "Azzabou".lower():
            return(int_signal[2:])
        else:
            return(int_signal)



def return_masks_individual( dataSet, islice, isliceZero, roi_set):
    """Used to calculate a mask for a single slice given that the zipped
    ROI is made up of individual ROIs

    Parameters
    ----------

    dataSet: dictionary
        contains information on dimensions of image
    islice: int
        index number of slice
    isliceZero: int
        index number based Zero offset
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





#def return_mask_outline( dataSet, islice, isliceZero, roi_set):
#    """Returns a single ROI mask that encompasses the outline of the imaged object
#
#    Parameters
#    ----------
#
#    dataSet: dictionary
#        contains information on dimensions of image
#    islice: int
#        index number of slice
#    isliceZero: int
#        index number based on 0 start
#    roi_set: list
#        rois read in from imageJ formatted roi set
#
#    Returns
#    -------
#
#    mask: 2-D np.ndarray of type boolean
#        boolean mask of all the ROIS found for the slice
#    mask_id: 2-D np.ndarray of type int
#        integer mask of all the ROIS found in the slice,
#        each pixel associated with a specific ROI is set to a number starting
#        at 1 and incremented if more than one ROI present
#    roi_names: list of str
#        list of ROI names associated with the image slice
#    """
#
#    mask = np.zeros((dataSet['numRows'],dataSet['numCols']), dtype=np.bool)
#    mask_id = np.zeros((dataSet['numRows'],dataSet['numCols']), dtype=np.int8)
#
#    roi_names = []
#
#    roi_ii = 1
#
#    print("islice, isliceZero, len(roi_set)", "islice, isliceZero, len(roi_set)")
#
#    roi_set_chosen = [ rs for rs in roi_set if "slice-{}".format(islice) in rs[0]]
#
#    (roi_name,roiShape, coords) = roi_set_chosen[0]
#
#    print("islice, roi_name", islice, roi_name)
#
##    roi_names.append(os.path.splitext(roi_name)[0].split('_')[-2])
#    roi_names.append(roi_name)
#
#    if roiShape == 'polygon':
#        coords=coords.transpose()
#        mask[polygon(coords[0],coords[1])] = True
#        mask_id[polygon(coords[0],coords[1])] = roi_ii
#
#    elif roiShape == 'rect':
#        coords=coords.transpose()
#        mask[polygon(coords[0],coords[1])] = True
#        mask_id[polygon(coords[0],coords[1])] = roi_ii
#
#    elif roiShape == 'oval':
#        xc = coords[0][0]
#        yc = coords[0][1]
#        xr = coords[1][0]
#        yr = coords[1][1]
#        mask[ellipse(yc,xc,yr,xr)] = True
#        mask_id[ellipse(yc,xc,yr,xr)] = roi_ii
#
#    return mask, mask_id, roi_names



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

class fitModelFile(dt.DataSet):
    """fit Model File

    Enter fit model file"""

    fitModelFileName = di.FileOpenItem("Fit Model:")


def return_groupName( subject, fitModelData, studyDescription):

    for groupName  in studyDescription.groupNames:
        if subject in studyDescription[groupName]['participants']:
            return groupName

def fitEPGAZZ_inStudyStructure(fitModelData=None, studyDir=None, yamlfileName=None):

    print("sys.argv ::", sys.argv)

    progDir, pyprog = os.path.split(sys.argv[0])

    print("progDir ::", progDir)

    if studyDir==None:

        studyDirDialog= studyDirectory()
        okcancel=studyDirDialog.edit()
        studyDir_directory = studyDirDialog.directory

        studyDescription = AttrDict.from_file( os.path.join(studyDir_directory,
                                                            "study_description_file.yml"))

    else:
        studyDir_directory = studyDir
        studyDescription = AttrDict.from_file( os.path.join(studyDir_directory,
                                                            "study_description_file.yml"))


    # ## Open fit study file name

    if fitModelData == None:
        fitModelFileDialog = fitModelFile()
        fitModelFileDialog.edit()
        fitModelFileDialog.fitModelFileName
        fitModelData =  AttrDict.from_file(fitModelFileDialog.fitModelFileName)
        yamlfileName = (os.path.split(fitModelFileDialog.fitModelFileName))[1]


    print(fitModelData)

    ################################
    #
    # Read in pulse profile data
    #
    #################################

    if os.path.isfile(fitModelData.p90pulseProfile):
        p90 = fitModelData.p90pulseProfile
    else:
        p90 = os.path.join(progDir, fitModelData.p90pulseProfile)

    if os.path.isfile(fitModelData.p180pulseProfile):
        p180 = fitModelData.p180pulseProfile
    else:
        p180 = os.path.join(progDir, fitModelData.p180pulseProfile)

    p90cw_profile = pulseProfile.PulseProfile(p90,step=fitModelData.pulseProfileSteps)
    p180cw_profile = pulseProfile.PulseProfile(p180,step=fitModelData.pulseProfileSteps)

    ######################################################
    #
    # Read in lmfit parameters file associated with model
    # Update parameter values from model yml file
    #
    ######################################################

    fp = open(fitModelData.paramsModelName[fitModelData.fitModel], 'r')
    params = lm.Parameters().load(fp)
    fp.close()


    print(params)


    analyzeDirectory = ["T2"]
    roiDirectory = ["rois"]
#    if fitModelData.fitModel in [ 'AzzEPG', 'muscleEPG2']:
#        fatDirectory = ["T2","results","fat","fatEPG2"]
#    elif fitModelData.fitModel in ["azzabou", "muscleEPG1"]:
#        fatDirectory = ["T2","results","fat","fatEPG1"]



    for subject in fitModelData.fitSubject:
        groupName = return_groupName( subject, fitModelData, studyDescription)
        for session in fitModelData.fitSession:
            for imagedRegion in fitModelData.fitImagedRegions:

                if not os.path.exists( os.path.join( studyDir_directory, subject, session, imagedRegion)):
                    print("path does not exist")
                    print(os.path.join( studyDir_directory, subject, session, imagedRegion))
                    continue

                ###################################################################
                # Read in extra parameters
                ###################################################################

                print("fitModelData.setParamValsIndividually",fitModelData.setParamValsIndividually)
                if fitModelData.setParamValsIndividually:
                    
                    if fitModelData.fitModel == "AzzEPG":

                        # read in fat paremeters
                        directory = os.path.join(studyDir_directory, subject, session, imagedRegion,fitModelData.fatResultsDir)

                        csv =[os.path.join(directory,fn) for fn in os.listdir(directory) if "results.csv" in fn ]

                        twofatEPG_df = pd.read_csv(csv[0])
                        print(csv)
            

                        fitModelData.ParamVals['t2_fl']={}
                        t2_fl_mean = twofatEPG_df.T2fl.mean()
                        print("t2_fl_mean",t2_fl_mean)
                        fitModelData.ParamVals['t2_fl']['min']=t2_fl_mean-1.0
                        fitModelData.ParamVals['t2_fl']['max']=t2_fl_mean+1.0
                        fitModelData.ParamVals['t2_fl']['value']=t2_fl_mean



                        fitModelData.ParamVals['t2_fs']={}
                        t2_fs_mean = twofatEPG_df.T2fs.mean()
                        fitModelData.ParamVals['t2_fs']['min']=t2_fs_mean-1.0
                        fitModelData.ParamVals['t2_fs']['max']=t2_fs_mean+1.0
                        fitModelData.ParamVals['t2_fs']['value']=t2_fs_mean

                        fitModelData.ParamVals['c_l']={}
                        cl_mean = twofatEPG_df.cl.mean()/(twofatEPG_df.cl.mean()+twofatEPG_df.cs.mean())
                        fitModelData.ParamVals['c_l']['min']=cl_mean-1.0
                        fitModelData.ParamVals['c_l']['max']=cl_mean+1.0
                        fitModelData.ParamVals['c_l']['value']=cl_mean

                        fitModelData.ParamVals['c_s']={}
                        cs_mean = twofatEPG_df.cs.mean()/(twofatEPG_df.cl.mean()+twofatEPG_df.cs.mean())
                        fitModelData.ParamVals['c_s']['min']=cs_mean-1.0
                        fitModelData.ParamVals['c_s']['max']=cs_mean+1.0
                        fitModelData.ParamVals['c_s']['value']=cs_mean

                    elif fitModelData.fitModel in ["muscleEPG2", "azzabou", "muscleEPG1"]:

                        # read in fat paremeters
                        directory = os.path.join(studyDir_directory, subject, session, imagedRegion,fitModelData.fatResultsDir)

                        csv =[os.path.join(directory,fn) for fn in os.listdir(directory) if "results.csv" in fn ]
                        print(csv)

                        onefatEPG_df = pd.read_csv(csv[0])

                        fitModelData.ParamVals['T2_fl']={}
                        t2_fl_mean = onefatEPG_df.T2fl.mean()
                        print("t2_fl_mean", t2_fl_mean )
                        fitModelData.ParamVals['T2_fl']['min']=t2_fl_mean-1.0
                        fitModelData.ParamVals['T2_fl']['max']=t2_fl_mean+1.0
                        fitModelData.ParamVals['T2_fl']['value']=t2_fl_mean

                #####################################################
                #
                # Update lmfit params data structure
                #
                #####################################################

                for paramName,attrs in fitModelData.ParamVals.items():
                    for k,v in attrs.items():
                        if k == "value":
                            params[paramName].value=v
                        elif k == "vary":
                            params[paramName].vary=v
                        elif k == "min":
                            params[paramName].min=v
                        elif k == "max":
                            params[paramName].max=v

                ###################################################################
                # Read in ROI files
                ###################################################################

                for roiAuthor in fitModelData.roiAuthorPreference:

                    directory = os.path.join(studyDir_directory, subject, session, imagedRegion,*roiDirectory, roiAuthor)
                    print("roi directory", directory)
                    if os.path.exists(directory):
                        break


                roiFilesList = [os.path.join(directory,fn) for fn in os.listdir(directory) if ".zip" in fn ]



                if fitModelData.useRoiOutline:

                    roiOutlineFileList = [fn for fn in roiFilesList if  "outline" in fn ]
                    roiFile = roiOutlineFileList[0]
                    print(fitModelData.useRoiOutline, roiFile)

                else:

                    roiIndvidualFileList = [fn for fn in roiFilesList if fitModelData.roiFitModel[fitModelData.fitModel] in fn]
                    roiFile = roiIndvidualFileList[0]
                    print(fitModelData.useRoiOutline,roiIndvidualFileList)

                roi_set = ijroieh.read_roi_zip(roiFile)

                ###########################################################
                #
                # Read in image data which can be in analyze format or
                # nifti, nifti can be a single file or a directory of files
                #
                ###########################################################

                directory = os.path.join(studyDir_directory, subject, session, imagedRegion,*analyzeDirectory)

                if fitModelData.imageDataFormat.lower() == "analyze":
                    # read in analyze data
                    print("read in analyze data")
                    AnalyzeImageFilesList = [os.path.join(directory,fn) for fn in os.listdir(directory) if ".img" in fn ]


                    img = nibabel.load(AnalyzeImageFilesList[0])
                    imageDataT2 = img.get_data()
                    imageDataT2 =np.flipud(imageDataT2.swapaxes(1,0))

                elif fitModelData.imageDataFormat.lower() == "nifti":
                    niftiImageFilesList = [os.path.join(directory,fn) for fn in os.listdir(directory) if ".nii" in fn ]

                    print( "niftiImageFilesList",  niftiImageFilesList)

                    if len(niftiImageFilesList)==1:
                        # read in nifti as a single file
                        print("read in nifti as a single file")

                        img = nibabel.load(niftiImageFilesList[0])
                        imageDataT2 = img.get_data()
                        imageDataT2 =np.flipud(imageDataT2.swapaxes(1,0))
                    elif len(niftiImageFilesList)>1:
                        # read in files as a series and stick them together
                        print("read in files as a series and stick them together")

                        fn_list = niftiImageFilesList
                        fn_list.sort()
                        niilist = []
                        for fn in fn_list:
                            niilist.append( nibabel.load(fn) )
                        nrows,ncols, nslices, nechos = niilist[0].shape
                        ddd = np.zeros((nrows,ncols, nslices, nechos))

                        for i in range(nechos):
                            ddd[:,:,:,i]= niilist[i].get_data()
                        imageDataT2 =np.flipud(ddd.swapaxes(1,0))
                    else:
                        # search in directory for any nifti files

                        print("read in nifti files from directories found in  directory")

                        niftiImageDirList = [os.path.join(directory,fn) for fn in os.listdir(directory) if os.path.isdir(os.path.join(directory,fn)) ]

                        for niftiDir in niftiImageDirList:
                            niftiImageFilesList = [os.path.join(niftiDir,fn) for fn in os.listdir(niftiDir) if ".nii" in fn ]

                            if len(niftiImageFilesList)==0:
                                continue
                            elif len(niftiImageFilesList)==1:
                                # read in nifti as a single file

                                img = nibabel.load(niftiImageFilesList[0])
                                imageDataT2 = img.get_data()
                                imageDataT2 =np.flipud(imageDataT2.swapaxes(1,0))

                            elif len(niftiImageFilesList)>1:
                                # read in files as a series and stick them together

                                fn_list = niftiImageFilesList
                                fn_list.sort()
                                niilist = []
                                for fn in fn_list:
                                    niilist.append( nibabel.load(fn) )
                                nrows,ncols, nslices = niilist[0].shape
                                nechos=len(fn_list)
                                ddd = np.zeros((nrows,ncols, nslices, nechos))

                                for i in range(nechos):
                                    ddd[:,:,:,i]= niilist[i].get_data()
                                imageDataT2 =np.flipud(ddd.swapaxes(1,0))





                nrows, ncols, nslices,nechos = imageDataT2.shape

                dataSet = { 'numRows':nrows, 'numCols':ncols, 'numSlices': nslices, 'numEchoes':nechos }

                dff_list = []

                ################################################################
                #
                # Loop over slices and fit data to model covered by ROIs
                #
                ################################################################

                for islice in fitModelData.fitSlices:

                    isliceZero=int(islice)-1
                    print("islice, isliceZero", islice, isliceZero)


                    t2mask_index = np.arange(dataSet['numRows']*dataSet['numCols']).reshape(dataSet['numRows'],dataSet['numCols'])

                    ##########################################
                    #
                    # Return ROI mask information
                    #
                    ###########################################

#                    if fitModelData.useRoiOutline:
#                        mask,mask_id,roi_names = return_mask_outline( dataSet, islice, isliceZero, roi_set)
#                    else:
#                        mask,mask_id,roi_names = return_masks_individual( dataSet, islice, isliceZero, roi_set)

                    mask,mask_id,roi_names = return_masks_individual( dataSet, islice, isliceZero, roi_set)
                    print("after masks")

                    ##############################################################
                    #
                    # Initiate fitting information based on the ROI masks for use
                    # in Pool/Map operation
                    #
                    ##############################################################

                    mask_id_pool      = mask_id[mask]
                    t2mask_index_pool = t2mask_index[mask]
                    t2imageData_pool  = imageDataT2[:,:,isliceZero,:][mask]
                    nvals_mask        = t2mask_index_pool.shape[0]

                    print("nvals_mask",nvals_mask)

                    pool_params =zip(t2mask_index_pool,
                                     t2imageData_pool,
                                     mask_id_pool,
                                     [roi_names]*nvals_mask,
                                     [params]*nvals_mask,
                                     [dataSet['numEchoes']]*nvals_mask,
                                     [fitModelData['dx']]*nvals_mask,
                                     [p90cw_profile.profile()]*nvals_mask,
                                     [p180cw_profile.profile()]*nvals_mask,
                                     [fitModelData['fitModel']]*nvals_mask)

                    ###############################################################
                    #
                    # Fit data using pool/map method to ustilize all processors
                    #
                    ###############################################################

                    pool = Pool()
                    ddd = pool.map(fit_T2EPGCPMG, pool_params)
                    pool.close()

                    ##################################################################
                    #
                    # Create a pandas datafram from all the results from the slice
                    # and store dataframe in a list
                    #
                    ##################################################################

                    dff = return_dataframe(ddd, fitModelData, islice)
                    dff['nrows']=nrows
                    dff['ncols']=ncols
                    dff['groupName']=groupName
                    dff['subject']=subject
                    dff['session']=session
                    dff['imagedRegion']=imagedRegion
                    dff['imagedRegionType']=fitModelData["roiFitModel"][fitModelData["fitModel"]]

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
                                         fitModelData.resultsDir)

                roi_names_all = (dff_all.roi_name.str.split('_'))

                roi_key = []
                for sss in roi_names_all:
                    roi_key.append(sss[-1].split('.')[0])

#                dff_all['roi_key']=roi_key
                dff_all['roi']=roi_key

                if not os.path.exists(resultsDir):
                    os.makedirs(resultsDir)

                dff_all.to_csv(os.path.join(resultsDir,'T2_{}_{}_{}_{}_results.csv'.format(subject,session,imagedRegion,fitModelData.fitModel)))
                dff_all.to_excel(os.path.join(resultsDir,'T2_{}_{}_{}_{}_results.xls'.format(subject,session,imagedRegion,fitModelData.fitModel)))

                #####################################################
                #
                # create a summary based on ROIs and slices
                #
                #####################################################



                ccc = [ 'T2m', 'Am100',  'Af100','T2fl', 'T2fs',  'T1f', 'T1m', 'Af', 'Am', 'cl', 'cs', 'B1',
                       'echo', 'rss', 'rchi', 'AIC', 'BIC',  'cl100',
                       'cs100']

                hdr = ['roi','slice','numPixels','subject','session','imagedRegion','fitModel', 'groupName', 'imagedRegionType']


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

                        p_list.append(rk)  # roi
                        p_list.append(s)   # slice
                        p_list.append(data_slice.echo.count()) #numPixels
                        p_list.append(subject)  # subject
                        p_list.append(session)  # session
                        p_list.append(imagedRegion)  # imagedRegion
                        p_list.append(fitModelData.fitModel)  # fitModel
                        p_list.append(data_slice.groupName.unique()[0])  # groupName
                        p_list.append(data_slice.imagedRegionType.unique()[0])  # imagedRegionType

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
                    s_data['fitModel']=fitModelData.fitModel
                    s_data['groupName']=data_rk.groupName.unique()[0]
                    s_data['imagedRegionType']=data_rk.imagedRegionType.unique()[0]

                    roiAggList.append(s_data)

                roiAgg_df = pd.DataFrame(roiAggList, columns=roiAggList[0].index)

                if not os.path.exists(fitModelData.resultsDir):
                    os.makedirs(fitModelData.resultsDir)
                summary_df.to_csv(os.path.join(resultsDir,'T2_{}_{}_{}_{}_summary.csv'.format(subject,session,imagedRegion,fitModelData.fitModel)))
                roiAgg_df.to_csv(os.path.join(resultsDir,'T2_{}_{}_{}_{}_Agg_summary.csv'.format(subject,session,imagedRegion,fitModelData.fitModel)))
                summary_df.to_excel(os.path.join(resultsDir,'T2_{}_{}_{}_{}_summary.xls'.format(subject,session,imagedRegion,fitModelData.fitModel)))
                roiAgg_df.to_excel(os.path.join(resultsDir,'T2_{}_{}_{}_{}_Agg_summary.xls'.format(subject,session,imagedRegion,fitModelData.fitModel)))

                fitModelData.dump(os.path.join(resultsDir,yamlfileName))

                del dff_list
                del dff_all
                del summary_df
                del summary




def fitEPGAZZ_singledata(fitModelData, yamlfileName):

    progDir, pyprog = os.path.split(sys.argv[0])

    print("progDir", progDir)

    ###########################################################
    #
    # Read in image data which needs to be in analyze format
    #
    ###########################################################

    if fitModelData.imageDataFormat == "nifti":

        if os.path.isdir(fitModelData.niftiData):

            fn_list = [ fn for fn in os.listdir(fitModelData.niftiData) if 'nii' in fn ]
            fn_list.sort()
            niilist = []
            for fn in fn_list:
                niilist.append( nibabel.load(os.path.join(fitModelData.niftiData, fn)) )

            nrows,ncols,nslices = niilist[0].shape
            nechos = len(niilist)

            ddd = np.zeros((nrows,ncols,nslices,nechos))

            for i in range(nechos):
                ddd[:,:,:,i]= niilist[i].get_data()

            imageDataT2=np.flipud(ddd.swapaxes(1,0))


        elif os.path.isfile(fitModelData.niftiData):
            img = nibabel.load(fitModelData.niftiData)
            imageDataT2 = img.get_data()
            imageDataT2=np.flipud(imageDataT2.swapaxes(1,0))

    elif fitModelData.imageDataFormat == "Analyze":

#        hdr = nibabel.load(fitModelData.analyzeHdr)
        img = nibabel.load(fitModelData.analyzeImg)
        imageDataT2 = img.get_data()
        imageDataT2 =np.flipud(imageDataT2.swapaxes(1,0))

    nrows, ncols, nslices,nechos = imageDataT2.shape

    ######################################################
    #
    # Read in lmfit parameters file associated with model
    # Update parameter values from model yml file
    #
    ######################################################

    fp = open(fitModelData.paramsModelName[fitModelData.fitModel], 'r')
    params = lm.Parameters().load(fp)
    fp.close()

    for paramName,attrs in fitModelData.ParamVals.items():
        for k,v in attrs.items():
            if k == "value":
                params[paramName].value=v
            elif k == "vary":
                params[paramName].vary=v
            elif k == "min":
                params[paramName].min=v
            elif k == "max":
                params[paramName].max=v

    params.pretty_print()


    ################################
    #
    # Read in pulse profile data
    #
    #################################

    if os.path.isfile(fitModelData.p90pulseProfile):
        p90 = fitModelData.p90pulseProfile
    else:
        p90 = os.path.join(progDir, fitModelData.p90pulseProfile)

    if os.path.isfile(fitModelData.p180pulseProfile):
        p180 = fitModelData.p180pulseProfile
    else:
        p180 = os.path.join(progDir, fitModelData.p180pulseProfile)

    print("p90",p90)
    print("p180",p180)

#    p90 = os.path.join("simpleModelData", fitModelData.p90pulseProfile)
#
#    p180 = os.path.join("simpleModelData", fitModelData.p180pulseProfile)

    p90cw_profile = pulseProfile.PulseProfile(p90,step=fitModelData.pulseProfileSteps)
    p180cw_profile = pulseProfile.PulseProfile(p180,step=fitModelData.pulseProfileSteps)

    ######################################
    #
    # Choose ROI file to read in
    #
    #######################################

    if fitModelData.useRoiOutline:
        roi_set = ijroieh.read_roi_zip(fitModelData.roiOutline)
    else:
        print("fitModelData.roisIndividual",fitModelData.roisIndividual)
        roi_set = ijroieh.read_roi_zip(fitModelData.roisIndividual)

    dataSet = { 'numRows':nrows, 'numCols':ncols, 'numSlices': nslices, 'numEchoes':nechos }

    dff_list = []

    ##################################################
    #
    #  Create figure forto ROIS on slice images
    #
    ##################################################

    fig,ax = plt.subplots(1,len(fitModelData['fitSlices']),  figsize=(4*len(fitModelData['fitSlices']),4), sharey=True, sharex=True)
    if len(fitModelData['fitSlices']) > 1:
        ax = ax.flatten()

    ################################################################
    #
    # Loop over slices and fit data to model covered by ROIs
    #
    ################################################################

    i=0 # index for plotting slices images

    for islice in fitModelData['fitSlices']:

        isliceZero = islice-1

        t2mask_index = np.arange(dataSet['numRows']*dataSet['numCols']).reshape(dataSet['numRows'],dataSet['numCols'])

        ##########################################
        #
        # Return ROI mask information
        #
        ###########################################


        mask, mask_id,roi_names = return_masks_individual( dataSet, islice, isliceZero, roi_set)

        ##############################################################
        #
        # Initiate fitting information based on the ROI masks for use
        # in Pool/Map operation
        #
        ##############################################################

        mask_id_pool      = mask_id[mask]
        t2mask_index_pool = t2mask_index[mask]
        t2imageData_pool  = imageDataT2[:,:,isliceZero,:][mask]
        nvals_mask        = t2mask_index_pool.shape[0]

        pool_params =zip(t2mask_index_pool,
                         t2imageData_pool,
                         mask_id_pool,
                         [roi_names]*nvals_mask,
                         [params]*nvals_mask,
                         [dataSet['numEchoes']]*nvals_mask,
                         [fitModelData['dx']]*nvals_mask,
                         [p90cw_profile.profile()]*nvals_mask,
                         [p180cw_profile.profile()]*nvals_mask,
                         [fitModelData['fitModel']]*nvals_mask)

        ###############################################################
        #
        # Fit data using pool/map method to ustilize all processors
        #
        ###############################################################

        pool = Pool()
        ddd = pool.map(fit_T2EPGCPMG, pool_params)

        ##################################################################
        #
        # Create a pandas datafram from all the results from the slice
        # and store dataframe in a list
        #
        ##################################################################

        dff = return_dataframe(ddd, fitModelData, islice)
        dff['nrows']=nrows
        dff['ncols']=ncols

        dff_list.append(dff)

        #############################
        #
        # Plot image slice and Roi
        #
        #############################

        if len(fitModelData['fitSlices']) > 1:
            ax[i].imshow(imageDataT2[:,:,isliceZero,0])
            ax[i].imshow(mask_id, alpha=0.5)
        else:
            ax.imshow(imageDataT2[:,:,isliceZero,0])
            ax.imshow(mask_id, alpha=0.5)
        i +=1

    ####################################################
    #
    # Combine all slice pandas dataframes and save
    #
    #####################################################

    dff_all = pd.concat(dff_list)

    # add a roi key field to data

    roi_names_all = dff_all.roi_name.str.split('_')
    roi_key = []
    for sss in roi_names_all:
        roi_key.append(sss[-1].split('.')[0])

    dff_all['roi']=roi_key

    print(dff_all['roi'])

    if not os.path.exists(fitModelData.resultsDir):
        os.makedirs(fitModelData.resultsDir)
    dff_all.to_csv(os.path.join(fitModelData.resultsDir,'T2_'+fitModelData.fitModel+'_results.csv'))
    dff_all.to_excel(os.path.join(fitModelData.resultsDir,'T2_'+fitModelData.fitModel+'_results.xls'))
    fitModelData.dump(os.path.join(fitModelData.resultsDir,yamlfileName))

    #####################################################
    #
    # create a summary based on ROIs and slices
    #
    #####################################################
#    roi_names_all = dff_all.roi_name.str.split('_')
#    roi_key = []
#    for sss in roi_names_all:
#        roi_key.append(sss[-1].split('.')[0])
#
#    dff_all['roi_key']=roi_key

#    ccc = [ 'T2m', 'Am100',  'Af100','T2fl', 'T2fs',  'T1f', 'T1m', 'Af', 'Am', 'cl', 'cs', 'B1',
#           'echo', 'rss', 'rchi', 'AIC', 'BIC',  'cl100',
#           'cs100']
#
#    hdr = ['roi','slice','count']
#
#    for c in ccc:
#        hdr.append(c+'_mean')
#        hdr.append(c+'_std')
#    summary = []
#
#
#    for rk in  dff_all.roi_key.unique():
#        data_rk =  dff_all[dff_all.roi_key == rk]
#        for s in data_rk.slice.unique():
#            data_slice = data_rk[data_rk.slice == s]
#            p_list=[]
#
#            p_list.append(rk)
#            p_list.append(s)
#            p_list.append(data_slice.echo.count())
#            for p in ccc:
#                p_list.append(data_slice[p].mean())
#                p_list.append(data_slice[p].std())
#
#            summary.append(p_list)
#
#    summary_df = pd.DataFrame(summary, columns=hdr)

    print("dff_all['roi']", dff_all['roi'])

    summary_df, summaryAgg_df = create_summary_tables(dff_all)

    if not os.path.exists(fitModelData.resultsDir):
        os.makedirs(fitModelData.resultsDir)

    summary_df.to_csv(os.path.join(fitModelData.resultsDir,'T2_'+fitModelData.fitModel+'_summary.csv'))
    summaryAgg_df.to_csv(os.path.join(fitModelData.resultsDir,'T2_'+fitModelData.fitModel+'_summaryAgg.csv'))

    summary_df.to_excel(os.path.join(fitModelData.resultsDir,fitModelData.fitModel+'_summary.xls'))
    summaryAgg_df.to_excel(os.path.join(fitModelData.resultsDir,fitModelData.fitModel+'_summaryAgg.xls'))

    ####################################################
    #
    # Plot an example of the fit
    #
    ####################################################

    half_index = len(ddd)//2
    plot_results(*ddd[half_index])
    plt.show()


def create_summary_tables(dff_all):

    #####################################################
    #
    # create a summary based on ROIs and slices
    #
    #####################################################


    ccc = [ 'T2m', 'Am100',  'Af100','T2fl', 'T2fs',  'T1f', 'T1m', 'Af', 'Am', 'cl', 'cs', 'B1',
           'echo', 'rss', 'rchi', 'AIC', 'BIC',  'cl100',
           'cs100']

    hdr = ['roi','slice','numPixels']

    ccc_mean_std = []

    for c in ccc:
        hdr.append(c+'_mean')
        hdr.append(c+'_std')
        ccc_mean_std.append(c+'_mean')
        ccc_mean_std.append(c+'_std')


    summaryList = []


    for rk in  dff_all.roi.unique():
        data_rk =  dff_all[dff_all.roi == rk]
        for s in data_rk.slice.unique():
            data_slice = data_rk[data_rk.slice == s]
            p_list=[]

            p_list.append(rk)
            p_list.append(s)
            p_list.append(data_slice.echo.count())
            for p in ccc:
                p_list.append(data_slice[p].mean())
                p_list.append(data_slice[p].std())

            summaryList.append(p_list)

    summary_df = pd.DataFrame(summaryList, columns=hdr)

    roiAggList = []

    for rk in  summary_df.roi.unique():

        data_rk =  summary_df[summary_df.roi == rk]
        s_data = (data_rk[ccc_mean_std].multiply(data_rk['numPixels'], axis="index")).sum()/data_rk['numPixels'].sum()
        s_data['roi']=rk
        roiAggList.append(s_data)

    roiAgg_df = pd.DataFrame(roiAggList, columns=roiAggList[0].index)

    return( summary_df, roiAgg_df)







def decide_what_todo():

    command_line_args_string = """

The program can be called in the following manner

python fitEPGazz.py

python fitEPGazz.py  directory\\to\\input_file\\fitModelDataFile.yml

python fitEPGazz.py directory\\directory\\to\\input_file\\fitModelDataFile.yml directory\\to\\study_directory\\testStudy"""


    studyDir = None

    if len(sys.argv) == 1: ## no command arguments
        #
        # Ask for fit Model data yaml file

        fitModelFileDialog = fitModelFile()
        fitModelFileDialog.edit()
        yamlfile = fitModelFileDialog.fitModelFileName



    elif len(sys.argv) == 2: # one cammand line argument that is a yaml file

        yamlfile = sys.argv[1]



    elif len(sys.argv) == 3: # two command line arguments, yaml file and study directory

        if "yml" in sys.argv[1]:
            yamlfile = sys.argv[1]
            studyDir = sys.argv[2]
        else:
            yamlfile = sys.argv[2]
            studyDir = sys.argv[1]

    if "yml" in yamlfile and os.path.exists(yamlfile):

        fitModelData =  AttrDict.from_file(yamlfile)
        yamlfileName = (os.path.split(yamlfile))[1]

        if fitModelData.fitSubject == []:
            fitEPGAZZ_singledata(fitModelData, yamlfileName)
        else:
            fitEPGAZZ_inStudyStructure(fitModelData, studyDir, yamlfileName)
    else:

        print("\n\n", yamlfile, ":: is not a yaml file or path does not exist")


        print(command_line_args_string)






if __name__ == "__main__":

    decide_what_todo()

#    if len(sys.argv) == 2:
#        decide_what_todo(sys.argv[1])
#    elif len(sys.argv) == 1:
#       fitEPGAZZ_inStudyStructure()
#
#    else:
#        print("command line arguments can be: python fitstudyEPGazz.py fitMuscleEPG1.yml or just the program name")

