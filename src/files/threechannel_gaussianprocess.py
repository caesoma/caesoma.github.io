#!/usr/bin/python3

import numpy
from numpy.random import normal as rnormal
from matplotlib.pyplot import figure, plot, show
import matplotlib.pyplot as pyplot


# Define the kernel functions
def se_kernel_pt(xp, xq, la, lb):
    """squared exponential kernel for a pair of points """
    corr = numpy.exp(-(numpy.abs(xp-xq)**2)/((la**2)+(lb**2)))
    return corr

# functions to compute the 'K' matrices of the gaussian processes
def compute_multi_kss_matrix(xTest, params, Kf):
    """ Computes the covariance matrix for test points of multiple channels, multiple bandwidths, and  a positive semi-definite matrix with process and "cross-process" variance. M matrices are produced. """

    M = xTest.shape[0] # channels
    N = xTest.shape[1] # number of data points for all channels (assumes they are equal)

    # empty matrix with terms computed on the loop below
    Kss = numpy.full([M,N, N], -numpy.Infinity)

    # compute each K_l,k matrix terms of the K** matrix
    for l in range(0,M):
        for k in range(0,M):

            la, lb = params[l], params[l]
            for xpq in range(0,N):
                Kss[l][xpq][xpq] = Kf[l][l]*1 # computes values on the diagonal, with correlation equal to unity

            for xp in range(0,N):
                for xq in range(xp+1,N):
                    Kss[l][xp][xq] = Kf[l][l]*se_kernel_pt(xTest[l][xp], xTest[l][xq], la, lb)
                    Kss[l][xq][xp] = Kss[l][xp][xq] # computes terms off of the diagonal, and their symmetric values ont he opposite side of the diagonal

    return Kss


def compute_multi_k_matrix(xTrain, params, Kf):
    """ computes the covariance matrix for training points of multiple channels, multiple bandwidths, and a positive semi-definite matrix with process and "cross-process" variance """

    M = xTrain.shape[0]
    N = xTrain.shape[1]

    ylen = M*N

    K = numpy.full([M*N, M*N], -numpy.Infinity)

    for l in range(0,M):
        subl = l*N

        for k in range(0,M):
            subk = k*N
            la, lb = params[l], params[k]

            for xp in range(0,N):
                for xq in range(xp, N):
                    K[subl+xp][subk+xq] = Kf[l][k]*se_kernel_pt(xTrain[l][xp], xTrain[k][xq], la, lb)
                    K[subk+xq][subl+xp] = K[subl+xp][subk+xq]

    return K


def compute_multi_ks_matrix(xTrain, xTest, params, Kf):
    """ computes the coavariance matrix between training and test points of multiple channels, with the appropriate cross-channel parameters """

    M = xTrain.shape[0]
    N = xTrain.shape[1]

    testN = xTest.shape[1]

    ylen = M*N

    Ks = numpy.full([M, testN, M*N], -numpy.Infinity)

    for l in range(0,M):
        lb = params[l]
        for xp in range(0,testN):
            for trn in range(0,M):
                la = params[trn]
                subtrn = trn*N
                for xq in range(N):
                    Ks[l][xp][subtrn+xq] = Kf[l][trn]*se_kernel_pt(xTest[l][xp],xTrain[trn][xq], la, lb)

    return Ks


# Training data
mu = 0 # mean is assumed to be zero, but does not have to be

sigman = 1 # standard deviation value from the real function values

# x training points values for each channel
xTrain1 = numpy.arange(2.05, 9.05, 1)
xTrain2 = xTrain1
xTrain3 = xTrain1

# array with training data points of all channels
xTrain = numpy.array([xTrain1, xTrain2, xTrain3])

# number of channels and training data points
M = xTrain.shape[0]
N = xTrain.shape[1]

# noisy observed values for the x training points
y1 = mu+xTrain1*numpy.sin(xTrain1) + rnormal(0, sigman, xTrain.shape[1])
y2 = mu+xTrain2*numpy.cos(xTrain2) + rnormal(0, sigman, xTrain.shape[1])
y3 = mu+(10-xTrain3)*numpy.sin(xTrain3) + rnormal(0, sigman, xTrain.shape[1])

y = numpy.array([y1, y2, y3]) # array with the multiple channels
yVec = y.reshape([1,-1])[0] # concatenated form of data

# test points
xTest1 = numpy.arange(0, 10.1, 0.1)
xTest2 = xTest1
xTest3 = xTest1
xTest = numpy.array([xTest1, xTest2, xTest3])

# "hyperparameters", a.k.a. parameters
params = numpy.sqrt([0.2, 0.1, 0.3]) # kernel 'bandwidth' parameters

Kf = numpy.array([[5, 0.7, 0.4],[0.7, 4, 0.5],[0.4, 0.5, 3]])  # signal variance matrix

# compute covariance matrices
Kss = compute_multi_kss_matrix(xTest, params, Kf)
K = compute_multi_k_matrix(xTrain, params, Kf)
Ks = compute_multi_ks_matrix(xTrain, xTest, params, Kf)

# get cholesky decomposition of the covariance matrix
L = numpy.linalg.cholesky(K + (sigman**2)*numpy.eye(M*N))

# compute solutions for mean channel values, following algorithm in Rasmussen and Williams, adapted for multiple channels
alpha = numpy.linalg.solve(L.T, numpy.linalg.solve(L, yVec.T))
fs = numpy.array([numpy.dot(Ks[l], alpha) for l in range(M)])

# compute variances for the channels
vee = numpy.array([numpy.linalg.solve(L, Ks[l].T) for l in range(M)])
Var = numpy.array([Kss[l] - numpy.dot(vee[l].T, vee[l]) for l in range(M)])
sd = numpy.array([numpy.sqrt(numpy.diag(Var[l])) for l in range(M)])


# the functions generating the 'true' values
fully1 = mu+xTest1*numpy.sin(xTest1)
fully2 = mu+xTest2*numpy.cos(xTest2)
fully3 = mu+(xTest3[-1]-xTest3)*numpy.sin(xTest3)

fully = numpy.array([fully1, fully2, fully3])

# plot results
channelcolor = ["CornFlowerBlue", "Crimson", "DarkOrange"]

pyplot.figure()
for l in range(M):
    pyplot.plot(xTest[l].T, fully[l], color=channelcolor[l])
    pyplot.plot(xTrain[l].T, y[l].T, 'o', color=channelcolor[l])
    pyplot.axis([0, 10, 2*y.min(), 2*y.max()])
    pyplot.title('True model')


for l in range(M):
    pyplot.figure()
    pyplot.plot(xTest[l], fully[l], color="Black", alpha=0.9-l*0.2)
    pyplot.plot(xTest[l].T, fs[l], color=channelcolor[l])
    pyplot.fill_between(xTest[l], fs[l]-2*sd[l], fs[l]+2*sd[l], color=channelcolor[l], alpha=0.2)
    pyplot.plot(xTrain[l].T, y[l].T, 'o', color=channelcolor[l])
    pyplot.axis([0, 10, 2*y.min(), y.max()*2])
    pyplot.title('Samples from the GP posterior')

pyplot.show()

# exec(open("./threechannel_gaussianprocess.py").read())
