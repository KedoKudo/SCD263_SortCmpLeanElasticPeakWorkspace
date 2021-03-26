from mantid.simpleapi import *
from mantid.geometry import OrientedLattice
from itertools import permutations
import numpy as np

ol=OrientedLattice(5,7,12,90,90,120)
ub=ol.getUB()
print(ub)

peaks = CreatePeaksWorkspace(NumberOfPeaks=0)

for hkl in set(permutations([1,1,1,0,0,0,-1,-1,-1],3)):
    p = peaks.createPeakQSample(2*np.pi*np.dot(ub,hkl))
    peaks.addPeak(p)

sorted_peaks = SortPeaksWorkspace(peaks, ColumnNameToSortBy='DSpacing')

CompareWorkspaces("peaks", "sorted_peaks")

# TOPAZ example
simulationWorkspace = CreateSimulationWorkspace(
    Instrument='TOPAZ_Definition_2015-01-01.xml',
    BinParams='0,1,2',
    UnitX='TOF',
    )
SetUB(simulationWorkspace, a=5.5, b=6.5, c=8.1, u='12,1,1', v='0,4,9')
peaks_topaz = PredictPeaks(
    simulationWorkspace,
    WavelengthMin=0.5, WavelengthMax=6,
    MinDSpacing=0.5, MaxDSpacing=10,
    )
SaveNexus(
    InputWorkspace='peaks_topaz',
    Filename='data/predict_peaks_test_random_ub_topaz.nxs',
    )
LoadNexus(
    Filename='data/predict_peaks_test_random_ub_topaz.nxs', OutputWorkspace='peaks_topaz_ref')
CompareWorkspaces("peaks_topaz", "peaks_topaz_ref")
