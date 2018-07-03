# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
# MDAnalysis --- https://www.mdanalysis.org
# Copyright (c) 2006-2017 The MDAnalysis Development Team and contributors
# (see the file AUTHORS for the full list of names)
#
# Released under the GNU Public Licence, v2 or any higher version
#
# Please cite your use of MDAnalysis in published work:
#
# R. J. Gowers, M. Linke, J. Barnoud, T. J. E. Reddy, M. N. Melo, S. L. Seyler,
# D. L. Dotson, J. Domanski, S. Buchoux, I. M. Kenney, and O. Beckstein.
# MDAnalysis: A Python package for the rapid analysis of molecular dynamics
# simulations. In S. Benthall and S. Rostrup editors, Proceedings of the 15th
# Python in Science Conference, pages 102-109, Austin, TX, 2016. SciPy.
#
# N. Michaud-Agrawal, E. J. Denning, T. B. Woolf, and O. Beckstein.
# MDAnalysis: A Toolkit for the Analysis of Molecular Dynamics Simulations.
# J. Comput. Chem. 32 (2011), 2319--2327, doi:10.1002/jcc.21787
#

"""Water dynamics analysis --- :mod:`MDAnalysis.analysis.waterdynamics`
=======================================================================

:Author: Alejandro Bernardin
:Year: 2014-2015
:Copyright: GNU Public License v3

.. versionadded:: 0.11.0

This module provides functions to analize water dynamics trajectories and water
interactions with other molecules.  The functions in this module are: water
orientational relaxation (WOR) [Yeh1999]_, hydrogen bond lifetimes (HBL)
[Rapaport1983]_, angular distribution (AD) [Grigera1995]_, mean square
displacement (MSD) [Brodka1994]_ and survival probability (SP) [Liu2004]_.

For more information about this type of analysis please refer to
[Araya-Secchi2014]_ (water in a protein cavity) and [Milischuk2011]_ (water in
a nanopore).

.. rubric:: References

.. [Rapaport1983] D.C. Rapaport (1983): Hydrogen bonds in water, Molecular
            Physics: An International Journal at the Interface Between
            Chemistry and Physics, 50:5, 1151-1162.

.. [Yeh1999] Yu-ling Yeh and Chung-Yuan Mou (1999).  Orientational Relaxation
             Dynamics of Liquid Water Studied by Molecular Dynamics Simulation,
             J. Phys. Chem. B 1999, 103, 3699-3705.

.. [Grigera1995] Raul Grigera, Susana G. Kalko and Jorge Fischbarg
                 (1995). Wall-Water Interface.  A Molecular Dynamics Study,
                 Langmuir 1996,12,154-158

.. [Liu2004] Pu Liu, Edward Harder, and B. J. Berne (2004).On the Calculation
             of Diffusion Coefficients in Confined Fluids and Interfaces with
             an Application to the Liquid-Vapor Interface of Water,
             J. Phys. Chem. B 2004, 108, 6595-6602.

.. [Brodka1994] Aleksander Brodka (1994). Diffusion in restricted volume,
                Molecular Physics, 1994, Vol.  82, No. 5, 1075-1078.

.. [Araya-Secchi2014] Araya-Secchi, R., Tomas Perez-Acle, Seung-gu Kang, Tien
                      Huynh, Alejandro Bernardin, Yerko Escalona, Jose-Antonio
                      Garate, Agustin D. Martinez, Isaac E. Garcia, Juan
                      C. Saez, Ruhong Zhou (2014). Characterization of a novel
                      water pocket inside the human Cx26 hemichannel
                      structure. Biophysical journal, 107(3), 599-612.

.. [Milischuk2011] Anatoli A. Milischuk and Branka M. Ladanyi. Structure and
                   dynamics of water confined in silica
                   nanopores. J. Chem. Phys. 135, 174709 (2011); doi:
                   10.1063/1.3657408


Example use of the analysis classes
-----------------------------------

HydrogenBondLifetimes
~~~~~~~~~~~~~~~~~~~~~

Analyzing hydrogen bond lifetimes (HBL) :class:`HydrogenBondLifetimes`, both
continuos and intermittent. In this case we are analyzing how residue 38
interact with a water sphere of radius 6.0 centered on the geometric center of
protein and residue 42. If the hydrogen bond lifetimes are very stable, we can
assume that residue 38 is hydrophilic, on the other hand, if the are very
unstable, we can assume that residue 38 is hydrophobic::

  import MDAnalysis
  from MDAnalysis.analysis.waterdynamics import HydrogenBondLifetimes as HBL

  u = MDAnalysis.Universe(pdb, trajectory)
  selection1 = "byres name OH2 and sphzone 6.0 protein and resid 42"
  selection2 = "resid 38"
  HBL_analysis = HBL(universe, selection1, selection2, 0, 2000, 30)
  HBL_analysis.run()
  time = 0
  #now we print the data ready to plot. The first two columns are the HBLc vs t
  #plot and the second two columns are the HBLi vs t graph
  for HBLc, HBLi in HBL_analysis.timeseries:
      print("{time} {HBLc} {time} {HBLi}".format(time=time, HBLc=HBLc, HBLi=HBLi))
      time += 1

  #we can also plot our data
  plt.figure(1,figsize=(18, 6))

  #HBL continuos
  plt.subplot(121)
  plt.xlabel('time')
  plt.ylabel('HBLc')
  plt.title('HBL Continuos')
  plt.plot(range(0,time),[column[0] for column in HBL_analysis.timeseries])

  #HBL intermitent
  plt.subplot(122)
  plt.xlabel('time')
  plt.ylabel('HBLi')
  plt.title('HBL Intermitent')
  plt.plot(range(0,time),[column[1] for column in HBL_analysis.timeseries])

  plt.show()

where HBLc is the value for the continuos hydrogen bond lifetimes and HBLi is
the value for the intermittent hydrogen bond lifetime, t0 = 0, tf = 2000 and
dtmax = 30. In this way we create 30 windows timestep (30 values in x
axis). The continuos hydrogen bond lifetimes should decay faster than
intermittent.


WaterOrientationalRelaxation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Analyzing water orientational relaxation (WOR)
:class:`WaterOrientationalRelaxation`. In this case we are analyzing "how fast"
water molecules are rotating/changing direction. If WOR is very stable we can
assume that water molecules are rotating/changing direction very slow, on the
other hand, if WOR decay very fast, we can assume that water molecules are
rotating/changing direction very fast::

  import MDAnalysis
  from MDAnalysis.analysis.waterdynamics import WaterOrientationalRelaxation as WOR

  u = MDAnalysis.Universe(pdb, trajectory)
  selection = "byres name OH2 and sphzone 6.0 protein and resid 42"
  WOR_analysis = WOR(universe, selection, 0, 1000, 20)
  WOR_analysis.run()
  time = 0
  #now we print the data ready to plot. The first two columns are WOR_OH vs t plot,
  #the second two columns are WOR_HH vs t graph and the third two columns are WOR_dip vs t graph
  for WOR_OH, WOR_HH, WOR_dip in WOR_analysis.timeseries:
        print("{time} {WOR_OH} {time} {WOR_HH} {time} {WOR_dip}".format(time=time, WOR_OH=WOR_OH, WOR_HH=WOR_HH,WOR_dip=WOR_dip))
        time += 1

  #now, if we want, we can plot our data
  plt.figure(1,figsize=(18, 6))

  #WOR OH
  plt.subplot(131)
  plt.xlabel('time')
  plt.ylabel('WOR')
  plt.title('WOR OH')
  plt.plot(range(0,time),[column[0] for column in WOR_analysis.timeseries])

  #WOR HH
  plt.subplot(132)
  plt.xlabel('time')
  plt.ylabel('WOR')
  plt.title('WOR HH')
  plt.plot(range(0,time),[column[1] for column in WOR_analysis.timeseries])

  #WOR dip
  plt.subplot(133)
  plt.xlabel('time')
  plt.ylabel('WOR')
  plt.title('WOR dip')
  plt.plot(range(0,time),[column[2] for column in WOR_analysis.timeseries])

  plt.show()

where t0 = 0, tf = 1000 and dtmax = 20. In this way we create 20 windows
timesteps (20 values in the x axis), the first window is created with 1000
timestep average (1000/1), the second window is created with 500 timestep
average(1000/2), the third window is created with 333 timestep average (1000/3)
and so on.

AngularDistribution
~~~~~~~~~~~~~~~~~~~

Analyzing angular distribution (AD) :class:`AngularDistribution` for OH vector,
HH vector and dipole vector. It returns a line histogram with vector
orientation preference. A straight line in the output plot means no
preferential orientation in water molecules. In this case we are analyzing if
water molecules have some orientational preference, in this way we can see if
water molecules are under an electric field or if they are interacting with
something (residue, protein, etc)::

  import MDAnalysis
  from MDAnalysis.analysis.waterdynamics import AngularDistribution as AD

  u = MDAnalysis.Universe(pdb, trajectory)
  selection = "byres name OH2 and sphzone 6.0 (protein and (resid 42 or resid 26) )"
  bins = 30
  AD_analysis = AD(universe,selection,bins)
  AD_analysis.run()
  #now we print data ready to graph. The first two columns are P(cos(theta)) vs cos(theta) for OH vector ,
  #the seconds two columns are P(cos(theta)) vs cos(theta) for HH vector and thirds two columns
  #are P(cos(theta)) vs cos(theta) for dipole vector
  for bin in range(bins):
        print("{AD_analysisOH} {AD_analysisHH} {AD_analysisDip}".format(AD_analysis.graph0=AD_analysis.graph[0][bin], AD_analysis.graph1=AD_analysis.graph[1][bin],AD_analysis.graph2=AD_analysis.graph[2][bin]))

  #and if we want to graph our results
  plt.figure(1,figsize=(18, 6))

  #AD OH
  plt.subplot(131)
  plt.xlabel('cos theta')
  plt.ylabel('P(cos theta)')
  plt.title('PDF cos theta for OH')
  plt.plot([float(column.split()[0]) for column in AD_analysis.graph[0][:-1]],[float(column.split()[1]) for column in AD_analysis.graph[0][:-1]])

  #AD HH
  plt.subplot(132)
  plt.xlabel('cos theta')
  plt.ylabel('P(cos theta)')
  plt.title('PDF cos theta for HH')
  plt.plot([float(column.split()[0]) for column in AD_analysis.graph[1][:-1]],[float(column.split()[1]) for column in AD_analysis.graph[1][:-1]])

  #AD dip
  plt.subplot(133)
  plt.xlabel('cos theta')
  plt.ylabel('P(cos theta)')
  plt.title('PDF cos theta for dipole')
  plt.plot([float(column.split()[0]) for column in AD_analysis.graph[2][:-1]],[float(column.split()[1]) for column in AD_analysis.graph[2][:-1]])

  plt.show()


where `P(cos(theta))` is the angular distribution or angular probabilities.


MeanSquareDisplacement
~~~~~~~~~~~~~~~~~~~~~~

Analyzing mean square displacement (MSD) :class:`MeanSquareDisplacement` for
water molecules. In this case we are analyzing the average distance that water
molecules travels inside protein in XYZ direction (cylindric zone of radius
11[nm], Zmax 4.0[nm] and Zmin -8.0[nm]). A strong rise mean a fast movement of
water molecules, a weak rise mean slow movement of particles::

  import MDAnalysis
  from MDAnalysis.analysis.waterdynamics import MeanSquareDisplacement as MSD

  u = MDAnalysis.Universe(pdb, trajectory)
  selection = "byres name OH2 and cyzone 11.0 4.0 -8.0 protein"
  MSD_analysis = MSD(universe, selection, 0, 1000, 20)
  MSD_analysis.run()
  #now we print data ready to graph. The graph
  #represents MSD vs t
  time = 0
  for msd in MSD_analysis.timeseries:
        print("{time} {msd}".format(time=time, msd=msd))
        time += 1

  #Plot
  plt.xlabel('time')
  plt.ylabel('MSD')
  plt.title('MSD')
  plt.plot(range(0,time),MSD_analysis.timeseries)
  plt.show()


.. _SP-examples:

SurvivalProbability
~~~~~~~~~~~~~~~~~~~

Analyzing survival probability (SP) :class:`SurvivalProbability` for water
molecules. In this case we are analyzing how long water molecules remain in a
sphere of radius 12.3 centered in the geometrical center of resid 42, 26, 34
and 80.  A slow decay of SP means a long permanence time of water molecules in
the zone, on the other hand, a fast decay means a short permanence time::

  import MDAnalysis
  from MDAnalysis.analysis.waterdynamics import SurvivalProbability as SP

  u = MDAnalysis.Universe(pdb, trajectory)
  selection = "byres name OH2 and sphzone 12.3 (resid 42 or resid 26 or resid 34 or resid 80) "
  SP_analysis = SP(universe, selection, 0, 100, 20)
  SP_analysis.run()
  #now we print data ready to graph. The graph
  #represents SP vs t
  time = 0
  for sp in SP_analysis.timeseries:
        print("{time} {sp}".format(time=time, sp=sp))
        time += 1

  #Plot
  plt.xlabel('time')
  plt.ylabel('SP')
  plt.title('Survival Probability')
  plt.plot(range(0,time),MSD_analysis.timeseries)
  plt.show()


.. _Output:

Output
------

HydrogenBondLifetimes
~~~~~~~~~~~~~~~~~~~~~

Hydrogen bond lifetimes (HBL) data is returned per window timestep, which is
stored in :attr:`HydrogenBondLifetimes.timeseries` (in all the following
descriptions, # indicates comments that are not part of the output)::

    results = [
        [ # time t0
            <HBL_c>, <HBL_i>
        ],
        [ # time t1
            <HBL_c>, <HBL_i>
        ],
        ...
     ]

WaterOrientationalRelaxation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Water orientational relaxation (WOR) data is returned per window timestep,
which is stored in :attr:`WaterOrientationalRelaxation.timeseries`::

    results = [
        [ # time t0
            <WOR_OH>, <WOR_HH>, <WOR_dip>
        ],
        [ # time t1
            <WOR_OH>, <WOR_HH>, <WOR_dip>
        ],
        ...
     ]

AngularDistribution
~~~~~~~~~~~~~~~~~~~

Angular distribution (AD) data is returned per vector, which is stored in
:attr:`AngularDistribution.graph`. In fact, AngularDistribution returns a
histogram::

    results = [
        [ # OH vector values
          # the values are order in this way: <x_axis  y_axis>
            <cos_theta0 ang_distr0>, <cos_theta1 ang_distr1>, ...
        ],
        [ # HH vector values
            <cos_theta0 ang_distr0>, <cos_theta1 ang_distr1>, ...
        ],
        [ # dip vector values
           <cos_theta0 ang_distr0>, <cos_theta1 ang_distr1>, ...
        ],
     ]

MeanSquareDisplacement
~~~~~~~~~~~~~~~~~~~~~~

Mean Square Displacement (MSD) data is returned in a list, which each element
represents a MSD value in its respective window timestep. Data is stored in
:attr:`MeanSquareDisplacement.timeseries`::

    results = [
         #MSD values orders by window timestep
            <MSD_t0>, <MSD_t1>, ...
     ]

SurvivalProbability
~~~~~~~~~~~~~~~~~~~

Survival Probability (SP) data is returned in a list, which each element
represents a SP value in its respective window timestep. Data is stored in
:attr:`SurvivalProbability.timeseries`::

    results = [
         # SP values order by window timestep
            <SP_t0>, <SP_t1>, ...
     ]



Classes
--------

.. autoclass:: HydrogenBondLifetimes
   :members:
   :inherited-members:

.. autoclass:: WaterOrientationalRelaxation
   :members:
   :inherited-members:

.. autoclass:: AngularDistribution
   :members:
   :inherited-members:

.. autoclass:: MeanSquareDisplacement
   :members:
   :inherited-members:

.. autoclass:: SurvivalProbability
   :members:
   :inherited-members:

"""
from __future__ import print_function, division, absolute_import

from numpy.core.multiarray import ndarray
from six.moves import range, zip_longest

import numpy as np
import multiprocessing

import MDAnalysis.analysis.hbonds
from MDAnalysis.lib.log import _set_verbose, ProgressMeter


class HydrogenBondLifetimes(object):
    r"""Hydrogen bond lifetime analysis

    This is a autocorrelation function that gives the "Hydrogen Bond Lifetimes"
    (HBL) proposed by D.C. Rapaport [Rapaport1983]_. From this function we can
    obtain the continuous and intermittent behavior of hydrogen bonds in
    time. A fast decay in these parameters indicate a fast change in HBs
    connectivity. A slow decay indicate very stables hydrogen bonds, like in
    ice. The HBL is also know as "Hydrogen Bond Population Relaxation"
    (HBPR). In the continuos case we have:

    .. math::
       C_{HB}^c(\tau) = \frac{\sum_{ij}h_{ij}(t_0)h'_{ij}(t_0+\tau)}{\sum_{ij}h_{ij}(t_0)}

    where :math:`h'_{ij}(t_0+\tau)=1` if there is a H-bond between a pair
    :math:`ij` during time interval :math:`t_0+\tau` (continuos) and
    :math:`h'_{ij}(t_0+\tau)=0` otherwise. In the intermittent case we have:

    .. math::
       C_{HB}^i(\tau) = \frac{\sum_{ij}h_{ij}(t_0)h_{ij}(t_0+\tau)}{\sum_{ij}h_{ij}(t_0)}

    where :math:`h_{ij}(t_0+\tau)=1` if there is a H-bond between a pair
    :math:`ij` at time :math:`t_0+\tau` (intermittent) and
    :math:`h_{ij}(t_0+\tau)=0` otherwise.


    Parameters
    ----------
    universe : Universe
      Universe object
    selection1 : str
      Selection string for first selection [‘byres name OH2’].
      It could be any selection available in MDAnalysis, not just water.
    selection2 : str
      Selection string to analize its HBL against selection1
    t0 : int
      frame  where analysis begins
    tf : int
      frame where analysis ends
    dtmax : int
      Maximum dt size, `dtmax` < `tf` or it will crash.
    nproc : int
      Number of processors to use, by default is 1.


    .. versionadded:: 0.11.0
    """

    def __init__(self, universe, selection1, selection2, t0, tf, dtmax,
                 nproc=1):
        self.universe = universe
        self.selection1 = selection1
        self.selection2 = selection2
        self.t0 = t0
        self.tf = tf - 1
        self.dtmax = dtmax
        self.nproc = nproc
        self.timeseries = None

    def _getC_i(self, HBP, t0, t):
        """
        This function give the intermitent Hydrogen Bond Lifetime
        C_i = <h(t0)h(t)>/<h(t0)> between t0 and t
        """
        C_i = 0
        for i in range(len(HBP[t0])):
            for j in range(len(HBP[t])):
                if (HBP[t0][i][0] == HBP[t][j][0] and HBP[t0][i][1] == HBP[t][j][1]):
                    C_i += 1
                    break
        if len(HBP[t0]) == 0:
            return 0.0
        else:
            return float(C_i) / len(HBP[t0])

    def _getC_c(self, HBP, t0, t):
        """
        This function give the continous Hydrogen Bond Lifetime
        C_c = <h(t0)h'(t)>/<h(t0)> between t0 and t
        """
        C_c = 0
        dt = 1
        begt0 = t0
        HBP_cp = HBP
        HBP_t0 = HBP[t0]
        newHBP = []
        if t0 == t:
            return 1.0
        while t0 + dt <= t:
            for i in range(len(HBP_t0)):
                for j in range(len(HBP_cp[t0 + dt])):
                    if (HBP_t0[i][0] == HBP_cp[t0 + dt][j][0] and
                        HBP_t0[i][1] == HBP_cp[t0 + dt][j][1]):
                        newHBP.append(HBP_t0[i])
                        break
            C_c = len(newHBP)
            t0 += dt
            HBP_t0 = newHBP
            newHBP = []
        if len(HBP[begt0]) == 0:
            return 0
        else:
            return C_c / float(len(HBP[begt0]))

    def _intervC_c(self, HBP, t0, tf, dt):
        """
        This function gets all the data for the h(t0)h(t0+dt)', where
        t0 = 1,2,3,...,tf. This function give us one point of the final plot
        HBL vs t
        """
        a = 0
        count = 0
        for i in range(len(HBP)):
            if (t0 + dt <= tf):
                if t0 == t0 + dt:
                    b = self._getC_c(HBP, t0, t0)
                    break
                b = self._getC_c(HBP, t0, t0 + dt)
                t0 += dt
                a += b
                count += 1
        if count == 0:
            return 1.0
        return a / count

    def _intervC_i(self, HBP, t0, tf, dt):
        """
        This function gets all the data for the h(t0)h(t0+dt), where
        t0 = 1,2,3,...,tf. This function give us a point of the final plot
        HBL vs t
        """
        a = 0
        count = 0
        for i in range(len(HBP)):
            if (t0 + dt <= tf):
                b = self._getC_i(HBP, t0, t0 + dt)
                t0 += dt
                a += b
                count += 1
        return a / count

    def _finalGraphGetC_i(self, HBP, t0, tf, maxdt):
        """
        This function gets the final data of the C_i graph.
        """
        output = []
        for dt in range(maxdt):
            a = self._intervC_i(HBP, t0, tf, dt)
            output.append(a)
        return output

    def _finalGraphGetC_c(self, HBP, t0, tf, maxdt):
        """
        This function gets the final data of the C_c graph.
        """
        output = []
        for dt in range(maxdt):
            a = self._intervC_c(HBP, t0, tf, dt)
            output.append(a)
        return output

    def _getGraphics(self, HBP, t0, tf, maxdt):
        """
        Function that join all the results into a plot.
        """
        a = []
        cont = self._finalGraphGetC_c(HBP, t0, tf, maxdt)
        inte = self._finalGraphGetC_i(HBP, t0, tf, maxdt)
        for i in range(len(cont)):
            fix = [cont[i], inte[i]]
            a.append(fix)
        return a

    def _HBA(self, ts, conn, universe, selAtom1, selAtom2,
             verbose=None, quiet=None):
        """
        Main function for calculate C_i and C_c in parallel.
        """
        verbose = _set_verbose(verbose, quiet, default=False)
        finalGetResidue1 = selAtom1
        finalGetResidue2 = selAtom2
        frame = ts.frame
        h = MDAnalysis.analysis.hbonds.HydrogenBondAnalysis(universe,
                                                            finalGetResidue1,
                                                            finalGetResidue2,
                                                            distance=3.5,
                                                            angle=120.0,
                                                            start=frame - 1,
                                                            stop=frame)
        while True:
            try:
                h.run(verbose=verbose)
                break
            except:
                print("error")
                print("trying again")
                sys.stdout.flush()
        sys.stdout.flush()
        conn.send(h.timeseries[0])
        conn.close()

    def run(self, **kwargs):
        """Analyze trajectory and produce timeseries"""
        h_list = []
        i = 0
        if (self.nproc > 1):
            while i < len(self.universe.trajectory):
                jobs = []
                k = i
                for j in range(self.nproc):
                        # start
                    print("ts=", i + 1)
                    if i >= len(self.universe.trajectory):
                        break
                    conn_parent, conn_child = multiprocessing.Pipe(False)
                    while True:
                        try:
                            # new thread
                            jobs.append(
                                (multiprocessing.Process(
                                    target=self._HBA,
                                    args=(self.universe.trajectory[i],
                                          conn_child, self.universe,
                                          self.selection1, self.selection2,)),
                                 conn_parent))
                            break
                        except:
                            print("error in jobs.append")
                    jobs[j][0].start()
                    i = i + 1

                for j in range(self.nproc):
                    if k >= len(self.universe.trajectory):
                        break
                    rec01 = jobs[j][1]
                    received = rec01.recv()
                    h_list.append(received)
                    jobs[j][0].join()
                    k += 1
            self.timeseries = self._getGraphics(
                h_list, 0, self.tf - 1, self.dtmax)
        else:
            h_list = MDAnalysis.analysis.hbonds.HydrogenBondAnalysis(self.universe,
                                                                     self.selection1,
                                                                     self.selection2,
                                                                     distance=3.5,
                                                                     angle=120.0)
            h_list.run(**kwargs)
            self.timeseries = self._getGraphics(
                h_list.timeseries, self.t0, self.tf, self.dtmax)


class WaterOrientationalRelaxation(object):
    r"""Water orientation relaxation analysis

    Function to evaluate the Water Orientational Relaxation proposed by Yu-ling
    Yeh and Chung-Yuan Mou [Yeh1999_]. WaterOrientationalRelaxation indicates
    "how fast" water molecules are rotating or changing direction. This is a
    time correlation function given by:

    .. math::
        C_{\hat u}(\tau)=\langle \mathit{P}_2[\mathbf{\hat{u}}(t_0)\cdot\mathbf{\hat{u}}(t_0+\tau)]\rangle

    where :math:`P_2=(3x^2-1)/2` is the second-order Legendre polynomial and :math:`\hat{u}` is
    a unit vector along HH, OH or dipole vector.


    Parameters
    ----------
    universe : Universe
      Universe object
    selection : str
      Selection string for water [‘byres name OH2’].
    t0 : int
      frame  where analysis begins
    tf : int
      frame where analysis ends
    dtmax : int
      Maximum dt size, `dtmax` < `tf` or it will crash.


    .. versionadded:: 0.11.0

    """

    def __init__(self, universe, selection, t0, tf, dtmax, nproc=1):
        self.universe = universe
        self.selection = selection
        self.t0 = t0
        self.tf = tf
        self.dtmax = dtmax
        self.nproc = nproc
        self.timeseries = None

    def _repeatedIndex(self, selection, dt, totalFrames):
        """
        Indicates the comparation between all the t+dt.
        The results is a list of list with all the repeated index per frame
        (or time).
        Ex: dt=1, so compare frames (1,2),(2,3),(3,4)...
        Ex: dt=2, so compare frames (1,3),(3,5),(5,7)...
        Ex: dt=3, so compare frames (1,4),(4,7),(7,10)...
        """
        rep = []
        for i in range(int(round((totalFrames - 1) / float(dt)))):
            if (dt * i + dt < totalFrames):
                rep.append(self._sameMolecTandDT(
                    selection, dt * i, (dt * i) + dt))
        return rep

    def _getOneDeltaPoint(self, universe, repInd, i, t0, dt):
        """
        Gives one point to calculate the mean and gets one point of the plot
        C_vect vs t.
        Ex: t0=1 and tau=1 so calculate the t0-tau=1-2 intervale.
        Ex: t0=5 and tau=3 so calcultate the t0-tau=5-8 intervale.
        i = come from getMeanOnePoint (named j) (int)
        """
        valOH = 0
        valHH = 0
        valdip = 0
        n = 0
        for j in range(len(repInd[i]) // 3):
            begj = 3 * j
            universe.trajectory[t0]
            Ot0 = repInd[i][begj]
            H1t0 = repInd[i][begj + 1]
            H2t0 = repInd[i][begj + 2]
            OHVector0 = H1t0.position - Ot0.position
            HHVector0 = H1t0.position - H2t0.position
            dipVector0 = ((H1t0.position + H2t0.position) * 0.5) - Ot0.position

            universe.trajectory[t0 + dt]
            Otp = repInd[i][begj]
            H1tp = repInd[i][begj + 1]
            H2tp = repInd[i][begj + 2]

            OHVectorp = H1tp.position - Otp.position
            HHVectorp = H1tp.position - H2tp.position
            dipVectorp = ((H1tp.position + H2tp.position) * 0.5) - Otp.position

            normOHVector0 = np.linalg.norm(OHVector0)
            normOHVectorp = np.linalg.norm(OHVectorp)
            normHHVector0 = np.linalg.norm(HHVector0)
            normHHVectorp = np.linalg.norm(HHVectorp)
            normdipVector0 = np.linalg.norm(dipVector0)
            normdipVectorp = np.linalg.norm(dipVectorp)

            unitOHVector0 = [OHVector0[0] / normOHVector0,
                             OHVector0[1] / normOHVector0,
                             OHVector0[2] / normOHVector0]
            unitOHVectorp = [OHVectorp[0] / normOHVectorp,
                             OHVectorp[1] / normOHVectorp,
                             OHVectorp[2] / normOHVectorp]
            unitHHVector0 = [HHVector0[0] / normHHVector0,
                             HHVector0[1] / normHHVector0,
                             HHVector0[2] / normHHVector0]
            unitHHVectorp = [HHVectorp[0] / normHHVectorp,
                             HHVectorp[1] / normHHVectorp,
                             HHVectorp[2] / normHHVectorp]
            unitdipVector0 = [dipVector0[0] / normdipVector0,
                              dipVector0[1] / normdipVector0,
                              dipVector0[2] / normdipVector0]
            unitdipVectorp = [dipVectorp[0] / normdipVectorp,
                              dipVectorp[1] / normdipVectorp,
                              dipVectorp[2] / normdipVectorp]

            valOH += self.lg2(np.dot(unitOHVector0, unitOHVectorp))
            valHH += self.lg2(np.dot(unitHHVector0, unitHHVectorp))
            valdip += self.lg2(np.dot(unitdipVector0, unitdipVectorp))
            n += 1
        return  (valOH/n, valHH/n, valdip/n) if n > 0 else (0, 0, 0)


    def _getMeanOnePoint(self, universe, selection1, selection_str, dt,
                         totalFrames):
        """
        This function gets one point of the plot C_vec vs t. It uses the
        _getOneDeltaPoint() function to calculate the average.

        """
        repInd = self._repeatedIndex(selection1, dt, totalFrames)
        sumsdt = 0
        n = 0.0
        sumDeltaOH = 0.0
        sumDeltaHH = 0.0
        sumDeltadip = 0.0

        for j in range(totalFrames // dt - 1):
            a = self._getOneDeltaPoint(universe, repInd, j, sumsdt, dt)
            sumDeltaOH += a[0]
            sumDeltaHH += a[1]
            sumDeltadip += a[2]
            sumsdt += dt
            n += 1

        # if no water molecules remain in selection, there is nothing to get
        # the mean, so n = 0.
        return (sumDeltaOH / n, sumDeltaHH / n, sumDeltadip / n) if n > 0 else (0, 0, 0)

    def _sameMolecTandDT(self, selection, t0d, tf):
        """
        Compare the molecules in the t0d selection and the t0d+dt selection and
        select only the particles that are repeated in both frame. This is to
        consider only the molecules that remains in the selection after the dt
        time has elapsed.
        The result is a list with the indexs of the atoms.
        """
        a = set(selection[t0d])
        b = set(selection[tf])
        sort = sorted(list(a.intersection(b)))
        return sort

    def _selection_serial(self, universe, selection_str):
        selection = []
        pm = ProgressMeter(universe.trajectory.n_frames,
                           interval=10, verbose=True)
        for ts in universe.trajectory:
            selection.append(universe.select_atoms(selection_str))
            pm.echo(ts.frame)
        return selection

    @staticmethod
    def lg2(x):
        """Second Legendre polynomial"""
        return (3*x*x - 1)/2

    def run(self, **kwargs):
        """Analyze trajectory and produce timeseries"""

        # All the selection to an array, this way is faster than selecting
        # later.
        if self.nproc == 1:
            selection_out = self._selection_serial(
                self.universe, self.selection)
        else:
            # selection_out = self._selection_parallel(self.universe,
            # self.selection, self.nproc)
            # parallel selection to be implemented
            selection_out = self._selection_serial(
                self.universe, self.selection)
        self.timeseries = []
        for dt in list(range(1, self.dtmax + 1)):
            output = self._getMeanOnePoint(
                self.universe, selection_out, self.selection, dt, self.tf)
            self.timeseries.append(output)


class AngularDistribution(object):
    r"""Angular distribution function analysis

    The angular distribution function (AD) is defined as the distribution
    probability of the cosine of the :math:`\theta` angle formed by the OH
    vector, HH vector or dipolar vector of water molecules and a vector
    :math:`\hat n` parallel to chosen axis (z is the default value). The cosine
    is define as :math:`\cos \theta = \hat u \cdot \hat n`, where :math:`\hat
    u` is OH, HH or dipole vector.  It creates a histogram and returns a list
    of lists, see Output_. The AD is also know as Angular Probability (AP).


    Parameters
    ----------
    universe : Universe
        Universe object
    selection : str
        Selection string to evaluate its angular distribution ['byres name OH2']
    bins : int (optional)
        Number of bins to create the histogram by means of :func:`numpy.histogram`
    axis : {'x', 'y', 'z'} (optional)
        Axis to create angle with the vector (HH, OH or dipole) and calculate
        cosine theta ['z'].


    .. versionadded:: 0.11.0
    """

    def __init__(self, universe, selection_str, bins=40, nproc=1, axis="z"):
        self.universe = universe
        self.selection_str = selection_str
        self.bins = bins
        self.nproc = nproc
        self.axis = axis
        self.graph = None

    def _getCosTheta(self, universe, selection, axis):
        valOH = []
        valHH = []
        valdip = []

        i = 0
        while i <= (len(selection) - 1):
            universe.trajectory[i]
            line = selection[i].positions

            Ot0 = line[::3]
            H1t0 = line[1::3]
            H2t0 = line[2::3]

            OHVector0 = H1t0 - Ot0
            HHVector0 = H1t0 - H2t0
            dipVector0 = (H1t0 + H2t0) * 0.5 - Ot0

            unitOHVector0 = OHVector0 / \
                np.linalg.norm(OHVector0, axis=1)[:, None]
            unitHHVector0 = HHVector0 / \
                np.linalg.norm(HHVector0, axis=1)[:, None]
            unitdipVector0 = dipVector0 / \
                np.linalg.norm(dipVector0, axis=1)[:, None]

            j = 0
            while j < len(line) / 3:
                if axis == "z":
                    valOH.append(unitOHVector0[j][2])
                    valHH.append(unitHHVector0[j][2])
                    valdip.append(unitdipVector0[j][2])

                elif axis == "x":
                    valOH.append(unitOHVector0[j][0])
                    valHH.append(unitHHVector0[j][0])
                    valdip.append(unitdipVector0[j][0])

                elif axis == "y":
                    valOH.append(unitOHVector0[j][1])
                    valHH.append(unitHHVector0[j][1])
                    valdip.append(unitdipVector0[j][1])

                j += 1
            i += 1
        return (valOH, valHH, valdip)

    def _getHistogram(self, universe, selection, bins, axis):
        """
        This function gets a normalized histogram of the cos(theta) values. It
        return a list of list.
        """
        a = self._getCosTheta(universe, selection, axis)
        cosThetaOH = a[0]
        cosThetaHH = a[1]
        cosThetadip = a[2]
        lencosThetaOH = len(cosThetaOH)
        lencosThetaHH = len(cosThetaHH)
        lencosThetadip = len(cosThetadip)
        histInterval = bins
        histcosThetaOH = np.histogram(cosThetaOH, histInterval, normed=True)
        histcosThetaHH = np.histogram(cosThetaHH, histInterval, normed=True)
        histcosThetadip = np.histogram(cosThetadip, histInterval, normed=True)

        return (histcosThetaOH, histcosThetaHH, histcosThetadip)

    def _hist2column(self, aList):
        """
        This function transform from the histogram format
        to a column format.
        """
        a = []
        for x in zip_longest(*aList, fillvalue="."):
            a.append(" ".join(str(i) for i in x))
        return a

    def run(self, **kwargs):
        """Function to evaluate the angular distribution of cos(theta)"""

        if self.nproc == 1:
            selection = self._selection_serial(
                self.universe, self.selection_str)
        else:
            # not implemented yet
            # selection = self._selection_parallel(self.universe,
            # self.selection_str,self.nproc)
            selection = self._selection_serial(
                self.universe, self.selection_str)

        self.graph = []
        output = self._getHistogram(
            self.universe, selection, self.bins, self.axis)
        # this is to format the exit of the file
        # maybe this output could be improved
        listOH = [list(output[0][1]), list(output[0][0])]
        listHH = [list(output[1][1]), list(output[1][0])]
        listdip = [list(output[2][1]), list(output[2][0])]

        self.graph.append(self._hist2column(listOH))
        self.graph.append(self._hist2column(listHH))
        self.graph.append(self._hist2column(listdip))

    def _selection_serial(self, universe, selection_str):
        selection = []
        pm = ProgressMeter(universe.trajectory.n_frames,
                           interval=10, verbose=True)
        for ts in universe.trajectory:
            selection.append(universe.select_atoms(selection_str))
            pm.echo(ts.frame)
        return selection


class MeanSquareDisplacement(object):
    r"""Mean square displacement analysis

    Function to evaluate the Mean Square Displacement (MSD_). The MSD gives the
    average distance that particles travels. The MSD is given by:

    .. math::
        \langle\Delta r(t)^2\rangle = 2nDt

    where :math:`r(t)` is the position of particle in time :math:`t`,
    :math:`\Delta r(t)` is the displacement after time lag :math:`t`,
    :math:`n` is the dimensionality, in this case :math:`n=3`,
    :math:`D` is the diffusion coefficient and :math:`t` is the time.

    .. _MSD: http://en.wikipedia.org/wiki/Mean_squared_displacement


    Parameters
    ----------
    universe : Universe
      Universe object
    selection : str
      Selection string for water [‘byres name OH2’].
    t0 : int
      frame  where analysis begins
    tf : int
      frame where analysis ends
    dtmax : int
      Maximum dt size, `dtmax` < `tf` or it will crash.


    .. versionadded:: 0.11.0
    """

    def __init__(self, universe, selection, t0, tf, dtmax, nproc=1):
        self.universe = universe
        self.selection = selection
        self.t0 = t0
        self.tf = tf
        self.dtmax = dtmax
        self.nproc = nproc
        self.timeseries = None

    def _repeatedIndex(self, selection, dt, totalFrames):
        """
        Indicate the comparation between all the t+dt.
        The results is a list of list with all the repeated index per frame
        (or time).

        - Ex: dt=1, so compare frames (1,2),(2,3),(3,4)...
        - Ex: dt=2, so compare frames (1,3),(3,5),(5,7)...
        - Ex: dt=3, so compare frames (1,4),(4,7),(7,10)...
        """
        rep = []
        for i in range(int(round((totalFrames - 1) / float(dt)))):
            if (dt * i + dt < totalFrames):
                rep.append(self._sameMolecTandDT(
                    selection, dt * i, (dt * i) + dt))
        return rep

    def _getOneDeltaPoint(self, universe, repInd, i, t0, dt):
        """
        Gives one point to calculate the mean and gets one point of the plot
        C_vect vs t.

        - Ex: t0=1 and dt=1 so calculate the t0-dt=1-2 interval.
        - Ex: t0=5 and dt=3 so calcultate the t0-dt=5-8 interva

        i = come from getMeanOnePoint (named j) (int)
        """
        valO = 0
        n = 0
        for j in range(len(repInd[i]) // 3):
            begj = 3 * j
            universe.trajectory[t0]
            # Plus zero is to avoid 0to be equal to 0tp
            Ot0 = repInd[i][begj].position + 0

            universe.trajectory[t0 + dt]
            # Plus zero is to avoid 0to be equal to 0tp
            Otp = repInd[i][begj].position + 0

            # position oxygen
            OVector = Ot0 - Otp
            # here it is the difference with
            # waterdynamics.WaterOrientationalRelaxation
            valO += np.dot(OVector, OVector)
            n += 1

        # if no water molecules remain in selection, there is nothing to get
        # the mean, so n = 0.
        return valO/n if n > 0 else 0

    def _getMeanOnePoint(self, universe, selection1, selection_str, dt,
                         totalFrames):
        """
        This function gets one point of the plot C_vec vs t. It's uses the
        _getOneDeltaPoint() function to calculate the average.

        """
        repInd = self._repeatedIndex(selection1, dt, totalFrames)
        sumsdt = 0
        n = 0.0
        sumDeltaO = 0.0
        valOList = []

        for j in range(totalFrames // dt - 1):
            a = self._getOneDeltaPoint(universe, repInd, j, sumsdt, dt)
            sumDeltaO += a
            valOList.append(a)
            sumsdt += dt
            n += 1

        # if no water molecules remain in selection, there is nothing to get
        # the mean, so n = 0.
        return sumDeltaO/n if n > 0 else 0

    def _sameMolecTandDT(self, selection, t0d, tf):
        """
        Compare the molecules in the t0d selection and the t0d+dt selection and
        select only the particles that are repeated in both frame. This is to
        consider only the molecules that remains in the selection after the dt
        time has elapsed. The result is a list with the indexs of the atoms.
        """
        a = set(selection[t0d])
        b = set(selection[tf])
        sort = sorted(list(a.intersection(b)))
        return sort

    def _selection_serial(self, universe, selection_str):
        selection = []
        pm = ProgressMeter(universe.trajectory.n_frames,
                           interval=10, verbose=True)
        for ts in universe.trajectory:
            selection.append(universe.select_atoms(selection_str))
            pm.echo(ts.frame)
        return selection

    def run(self, **kwargs):
        """Analyze trajectory and produce timeseries"""

        # All the selection to an array, this way is faster than selecting
        # later.
        if self.nproc == 1:
            selection_out = self._selection_serial(
                self.universe, self.selection)
        else:
            # parallel not yet implemented
            # selection = selection_parallel(universe, selection_str, nproc)
            selection_out = self._selection_serial(
                self.universe, self.selection)
        self.timeseries = []
        for dt in list(range(1, self.dtmax + 1)):
            output = self._getMeanOnePoint(
                self.universe, selection_out, self.selection, dt, self.tf)
            self.timeseries.append(output)


class SurvivalProbability(object):
    r"""Survival probability analysis

    Function to evaluate the Survival Probability (SP). The SP gives the
    probability for a group of particles to remain in certain region. The SP is
    given by:

    .. math::
        P(\tau) = \frac1T \sum_{t=1}^T \frac{N(t,t+\tau)}{N(t)}

    where :math:`T` is the maximum time of simulation, :math:`\tau` is the
    timestep and :math:`N` the number of particles in certain time.


    Parameters
    ----------
    universe : Universe
      Universe object
    selection : str
      Selection string; any selection is allowed. With this selection you
      define the region/zone where to analyze, e.g.: "selection_a" and "zone"
      (see `SP-examples`_ )
    t0 : int
      frame  where analysis begins
    tf : int
      frame where analysis ends
    tau_max : int
      Maximum dt size, `tau_max` must be < `tf`


    .. versionadded:: 0.11.0

    """

    def __init__(self, universe, selection, t0=0, tf=-1, tau_max=20, verbose=False):
        """
        FIXME - definition explaining each argument
        tf is inclusive

        Return:
        taus, sp_timeseries

        Special:
        :param universe:
        :param selection:
        :param t0: First frame to be analysed
        :param tf: Last frame to be analysed (must be below the max number of frames)
        :param tau_max: The last tau to be calculated (inclusive), starts from 1
        :param verbose: If True, will highlight the starting point, ending point, progress
        """
        self.universe = universe
        self.selection = selection
        self.t0 = t0
        if tf == -1:
            self.tf = len(universe.trajectory) - 1
        elif tf <= len(universe.trajectory):
            self.tf = tf
        else:
            raise ValueError("tf cannot be bigger than the number of frames in the simulation")
        self.tau_max = tau_max
        self.verbose = verbose

        if tf - t0 <= self.tau_max:
            raise ValueError("cannot select fewer frames than tau_max + 1")

    def print(self, *args):
        if self.verbose:
            print(args)

    def run(self):
        """
        Computes and returns the survival probability timeseries
        """
        
        # load all frames to an array of sets
        selected = []
        for _ in self.universe.trajectory[self.t0:self.tf]:
            selected.append(set(self.universe.select_atoms(self.selection)))

        tau_timeseries = np.arange(1, self.tau_max + 1)
        sp_timeseries = [[] for _ in range(self.tau_max)]
        for t in range(len(selected)):
            Nt = len(selected[t])

            if Nt == 0:
                self.print("At t=", t, "the selection did not find any molecule. Moving on to the next frame")
                continue

            for tau in tau_timeseries:
                if t + tau > len(selected):
                    break

                Ntau = len(set.intersection(*selected[t:t + tau + 1]))
                sp_timeseries[tau - 1].append(Ntau / float(Nt) )

        # user can investigate the distribution and sample size
        self.sp_timeseries = sp_timeseries

        return tau_timeseries, [np.mean(sp) for sp in sp_timeseries]

