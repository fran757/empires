"""Domain module

This module contains classes to represent the integration domain, the pops and the resources
"""

import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.ndimage import gaussian_filter
from matplotlib.animation import FuncAnimation, PillowWriter
from PIL import Image


def restrict(In, dx, new_dx):
    """To project on a coarser grid"""
    step = int(new_dx/dx)
    return In[::step, ::step]


class Domain:
    """The domain of integration"""

    def __init__(self, name):
        """Constructor of the domain

        name -- a string with the name of the domain files
        """

        f = open(name+'/specs.json',)
        specs = json.load(f)

        # Reading all the images
        self.I_start = plt.imread(name+'/bound.png')
        self.I_topo_start = (1-plt.imread(name+'/topo.png'))
        terrain = (plt.imread(name+'/terrain.png')*255).astype(np.uint8)

        # Building the ressource base regeneration map
        self.I_r_start = np.zeros(self.I_start.shape)
        for t in specs["terrain"]:
            self.I_r_start[np.where(np.all(terrain == np.array(t["color"]), axis=-1))] = t["prosperity"]

        self.dx_start = specs["dx"]

        self.I = self.I_start
        self.I_topo = self.I_topo_start
        self.I_r = self.I_r_start

        self.dx = specs["dx"] #km
        self.area = np.sum(self.I)*(self.dx**2)
        self.shape = self.I.shape

    def resize(self, new_dx):
        """To project on a coarser grid

        new_dx -- The new space-step (km)
        """

        if new_dx > self.dx_start:
            self.I = restrict(self.I_start, self.dx_start, new_dx)
            self.I_topo = restrict(self.I_topo_start, self.dx_start, new_dx)
            self.I_r = restrict(self.I_r_start, self.dx_start, new_dx)

            self.dx = new_dx
            self.area = np.sum(self.I)*(self.dx**2)
            self.shape = self.I.shape
        else:
            print("only coarser grid are authorized !")


class Res:
    """Resources class"""
    def __init__(self, r0, Rmax):
        """Constructor of the class

        r0 -- The renewal rate of resources in best conditions (%/year)
        Rmax -- Maximum ressources in the best conditions (res)
        """
        self.r0 = r0
        self.Rmax = Rmax

class Pop:
    """Population class"""

    def __init__(self, start_loc,N_start,c0,Rdem,n0,k0,Nbar,gamma):
        """Population constructor

        Starting:
            start_loc -- array with starting location coordonates
            N_start -- start populations (pop)
        Consumption parameters:
            c0 -- maximum consumption rate per person (res^-1.pop^-1.year^-1)
            Rdem -- R needed to reach half of maximum consumption rate (res)
        Demography:
            n0 -- pop natural growth rate (year^-1)
            k0 -- inflexion of KN
            Nbar -- barbarian population level (pop)
        Migration:
            gamma -- migration inflexion factor (pop^-1)
        """

        self.start_loc = start_loc
        self.N_start = N_start
        self.c0 = c0
        self.Rdem = Rdem
        self.n0 = n0
        self.k0 = k0
        self.Nbar = Nbar
        self.gamma = gamma


class State:
    """State class"""

    def __init__(self, color, idx,c,eps,c1,alpha,sig,h,z):
        """State constructor
        Code caracteristics:
            color -- color (array)
            idx -- state index
        Production parameters:
            c -- production rate (money.resource^-1.year^-1)
            eps -- ressource extraction capacity (%)
        Cultural assimilation:
            c1 -- C growth rate (year^-1)
        Taxes parameters:
            alpha -- production taxation (%.year^-1)
        Asabiya:
            sig -- cohesion ray (km)
        Power:
            h -- power decline speed with distance (km)
            z -- power decline speed with money (money)
        """

        self.color = color
        self.idx = idx
        self.c =c
        self.eps = eps
        self.c1 = c1
        self.alpha = alpha
        self.sig = sig
        self.h = h
        self.z = z
