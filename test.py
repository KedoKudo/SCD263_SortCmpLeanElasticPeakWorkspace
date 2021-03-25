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
