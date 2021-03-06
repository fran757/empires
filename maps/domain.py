"""Domain module

This module contains classes to represent the integration domain, the pops and the resources
"""

import matplotlib.pyplot as plt
import numpy as np
import json
from matplotlib.animation import FuncAnimation, PillowWriter
from PIL import Image


class Domain:
    """The domain of integration"""

    def __init__(self, name):
        """Constructor of the domain

        name -- a string with the name of the domain files
        """

        f = open(name+'/specs.json',)
        specs = json.load(f)

        # Reading all the images
        self.I = plt.imread(name+'/bound.png')
        self.I_topo = (1-plt.imread(name+'/topo.png'))
        terrain = (plt.imread(name+'/terrain.png')*255).astype(np.uint8)

        # Building the ressource base regeneration map
        self.I_r = np.zeros(self.I.shape)
        for t in specs["terrain"]:
            self.I_r[np.where(np.all(terrain == np.array(t["color"]), axis=-1))] = t["prosperity"]

        self.dx = specs["dx"] #km
        self.area = np.sum(self.I)*(self.dx**2)
        self.shape = self.I.shape

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

    def __init__(self,c0,Rdem,chi,n0,Nstart,Nmax):
        """Population constructor

        Consumption parameters:
            c0 -- maximum consumption rate per person (pop^-1.year^-1)
            Rdem -- R needed to reach half of maximum consumption rate (res)
            chi -- population generated by max consumption (pop)
        Demography:
            n0 -- pop natural death rate (year^-1)
            Nstart -- founding pop (pop)
            Nmax -- carrying capacity (pop)
        """

        self.c0 = c0
        self.Rdem = Rdem
        self.chi = chi
        self.n0 = n0
        self.Nstart = Nstart
        self.Nmax = Nmax
