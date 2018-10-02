#!/usr/bin/python3

import numpy, pandas
from numpy.random import normal as rnormal, poisson as rpoisson
import matplotlib, matplotlib.pyplot as pyplot
from matplotlib.pyplot import figure, plot, show
import seaborn

randomNormalArray = pandas.DataFrame(rnormal(0,1, size=(4, 10000)), index=["smpl #"+str(i) for i in range(4)], columns=["gn#"+str(i) for i in range(10000)]);

#figure(figsize=(8,4));
#pyplot.imshow(randomNormalArray[0], cmap=matplotlib.cm.coolwarm);
seaborn.clustermap(randomNormalArray, cmap=matplotlib.cm.coolwarm, pivot_kws=None, method='average', metric='euclidean', z_score=1, standard_scale=None, figsize=(8,2), cbar_kws=None, row_cluster=False, col_cluster=False, row_linkage=1, col_linkage=None, row_colors=None, col_colors=None, mask=None);

seaborn.clustermap(randomNormalArray, cmap=matplotlib.cm.coolwarm, method='average', metric='euclidean', z_score=1, figsize=(8,2), row_cluster=False, col_cluster=True);
#pyplot.ylabel("pseudo samples")
#pyplot.ylabel("pseudo genes")
show();

"""
for paper in range(10):
    print(">>>run:", paper)
    #seaborn.clustermap(randomNormalArray[i], cmap=matplotlib.cm.coolwarm, z_score=0, figsize=(8,4), row_cluster=False, col_cluster=False);
    seaborn.clustermap(randomNormalArray[paper], cmap=matplotlib.cm.coolwarm, z_score=None, figsize=(8,4), row_cluster=False, col_cluster=True);

show();
"""
