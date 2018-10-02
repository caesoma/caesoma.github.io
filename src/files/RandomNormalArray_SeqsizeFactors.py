#!/usr/bin/python3

import os
import numpy, pandas
from numpy.random import normal as rnormal, poisson as rpoisson, randint
import matplotlib, matplotlib.pyplot as pyplot
from matplotlib.pyplot import figure, plot, show
import seaborn

os.chdir(os.path.expanduser("~/git/evorna"));
import estimateSizeFactors

seq = randint(1, 10, 10)/10  # rpoisson(10, size=10)/10;
randomNormalArray = pandas.DataFrame((seq*rpoisson(100, size=(10, 10000)).T).T, index=["smpl #"+str(i) for i in range(10)], columns=["gn#"+str(i) for i in range(10000)]);

sizeFactors = estimateSizeFactors.esf(randomNormalArray.T);
normRNAseq = (randomNormalArray.T/sizeFactors).T

seaborn.clustermap(normRNAseq, cmap=matplotlib.cm.coolwarm, pivot_kws=None, method='average', metric='euclidean', z_score=1, standard_scale=None, figsize=(8,4), row_cluster=False, col_cluster=False);

seaborn.clustermap(normRNAseq, cmap=matplotlib.cm.coolwarm, pivot_kws=None, method='average', metric='euclidean', z_score=1, standard_scale=None, figsize=(8,4), cbar_kws=None, row_cluster=False, col_cluster=True, row_linkage=None, col_linkage=None, row_colors=None, col_colors=None, mask=None);
show();
