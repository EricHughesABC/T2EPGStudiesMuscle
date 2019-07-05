# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 13:35:52 2018

@author: neh69
"""

import numpy as np
import scipy.io as spio
from matplotlib import pyplot as plt

class  PulseProfileM(object):

    def __init__(self, pulseProfileFilename=None, ):

        self.pulseProfileFilename = pulseProfileFilename

        self.mxyz = None
        self.epg_slice_xxx = None
        self.offset = 130
        self.step   = 10

        self.readPulseProfileFile( self.pulseProfileFilename )


    def readPulseProfileFile(self, pulseProfileFilename ):
        """Ascii file consisting of five columns separated by space
           column   Description
           1        -slice width/2 to +slice_width/2
           2        Mx profile  -1 to 1
           3        My profile  -1 to 1
           4        Mz profile  -1 to 1
           5        Profile     0 - 360 degrees
        """

        self.mxyz = np.fromfile(pulseProfileFilename, sep= ' ')
        self.npts = self.mxyz.size
        self.mxyz = self.mxyz.reshape(5, self.npts//5)



    def profile(self, offset=None, step=None):

        if offset is not None:
            self.offset = offset
        if step is not None:
            self.step = step

        return self.mxyz[-1][self.offset:-self.offset+self.step:self.step]


    def dx(self):
        if self.mxyz is None:
            return None
        else:
            self.epg_slice_xxx =self.mxyz[0][self.offset:-self.offset+self.step:self.step]
            return self.epg_slice_xxx[1]-self.epg_slice_xxx[0]



    def xcoords(self):

        if self.epg_slice_xxx is None:
            self.epg_slice_xxx =self.mxyz[0][self.offset:-self.offset+self.step:self.step]

        return self.epg_slice_xxx


    def plot(self):
        plt.plot( self.xcoords(), self.profile(), '.-');
        plt.xlabel('slice [mm]');
        plt.ylabel('rotation angle ($^0$)')


class  PulseProfile(object):

    def __init__(self, pulseProfileFilename=None, slice_width=30, step=10 ):

        self.pulseProfileFilename = pulseProfileFilename

        self.mxyz = None
        self.epg_slice_xxx = None
        self.slice_width = slice_width
        self.step   = step

        self.pxxx  = None
        self.pulsearray = None

        self.matp  = self.readPulseProfileFile( self.pulseProfileFilename )
        # print('type(self.matp)',type(self.matp))
        self.pxxx, self.pulsearray = self.return_halfprofiles(self.matp, self.slice_width, self.step)


    def readPulseProfileFile(self, pulseProfileFilename ):


#         self.mxyz = np.fromfile(pulseProfileFilename, sep= ' ')
#         self.npts = self.mxyz.size
#         self.mxyz = self.mxyz.reshape(5, self.npts//5)

        return spio.loadmat(pulseProfileFilename, squeeze_me=True)




    def return_halfprofiles(self, m90, slice_width=30, step=10):

        xxx=m90[ 'xxx_axis_mm']
        p90 = m90['flip_angle180']


        sw_half = slice_width/2

        e = np.abs(xxx).argmin()

        s = ((np.abs(xxx-sw_half).argmin()))


        xxx1 = xxx[e:s:step]
        p901 = p90[e:s:step]


        if len(xxx1)%2 == 0:
            return xxx1[:-1], p901[:-1]
        else:
            return xxx1, p901



    def profile(self):

       return self.pulsearray


    def dx(self):

        return self.pxxx[1]-self.pxxx[0]



    def xcoords(self):

#         if self.epg_slice_xxx is None:
#             self.epg_slice_xxx =self.mxyz[0][self.offset:-self.offset+self.step:self.step]

        return self.pxxx


    def plot(self):
        plt.plot( self.xcoords(), self.profile(), '.-');
        plt.xlabel('slice [mm]');
        plt.ylabel('rotation angle ($^0$)')




