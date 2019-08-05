---
author: caetano
title: "StanCon 2019 -- Multi-channel Gaussian Processes as flexible alternatives to linear models: perspectives and challenges to scaling up Bayesian inference to genomic-scale data"
date: 2019-08-01
layout: post
---

### Abstract

“Omics” data are now routinely produced in labs around the world, but extracting meaningful results from them remains a challenge. The lack of knowledge about the interactions between gene products precludes scientists from formulating mechanistic models of gene network regulations, and the size of the data sets (commonly with thousands of readouts per sample for RNA or protein readouts) hampers exploration of patterns in the data. For transcriptomic data (i.e. RNA transcript counts), a commonly applied pipeline relies on linear model analysis of each gene, where the predictors are experimental conditions such as genotype (e.g. mutant vs wild type), environmental variables (temperature, food availability), or time. This approach solves the problem of data set size by breaking down the problem into thousands of linear regressions with parameters that can be easily estimated; however, it assumes not only that any trends are linear but also independence between genes. Additionally, the coefficients in the model have essentially no biological meaning.

Gaussian processes are flexible models for stochastic processes that can describe nonlinear trends in the data along some dimension, like time, for instance. Their structure also allows the kernel-defined covariance matrix to be extended to multiple channels (e.g. genes) and therefore estimate the degree of interaction between them without need of previous knowledge of which genes actually interact. The caveat of this approach is the number signal covariance parameters – given by the number of pairwise combinations, which is on the order of the square of M, the number of channels – and the size of the covariance matrix itself, a square matrix of size MN which may need to be inverted or decomposed – where N is the number of time points.

Bayesian inference using Hamiltonian Monte Carlo offers a powerful tool to approach this inference problem, but the high dimensionality of the parameter space and the costly computations limit its scalability to a number of channels M in the order of the tens instead of thousands. Here we show the results of a simulation study scaling up a multi-channel Gaussian from M=2 up to M=85 channels, showing the limitations of scaling up this approach in terms of speed, effective number of samples, accuracy and precision of estimation – based on these criteria we assess the feasibility of this joint estimation compared to multiple separate inference for all possible pairs, and discuss the caveats. We also show result of the model applied to transcriptomic data of Drosophila melanogaster artificially selected to be extreme sleepers.

### Methods

#### Gaussian Processes

Gaussian processes (GPs) describe a series of observations correlated along some dimension (e.g. time); this correlation is given by a matrix specified by a kernel, which in turn can be a function for instance of the distance between time points (specified by the data), and a couple of free parameters or "hyperparameters" (which depends on the actual form of the kernel chosen) [Rasmussen and Williams Gaussian](http://www.gaussianprocess.org/gpml/).

Therefore, a gaussian process is fully specified by a multivariate gaussian distribution \\( y \\sim \\mathcal{N}(\\mu, K) \\), where \\( \\mu \\) is the mean of the observation series, and \\( K \\) is its covariance matrix with entries \\( k_{ij} \\) specified by a kernel instead of independently specified for every pair of gaussian observations as is common otherwise. If there are \\( N \\) observations the matrix \\( K \\) has dimension \\( N \\times N \\).

For an exponential quadratic kernel, the covariance of two entris of the matrix is given by:
$$ k_{ij} = k(x_i,x_j) = \sigma^{2}_f exp \left( \frac{-|x_i-x_j|^2}{2\ell^2} \right) $$ and the gaussian process is given by \\(\\mathcal{GP} \\sim \\mathcal{N}(\\mu, K) \\). Here \\( \\ell \\) modulates the bandwidth of correlation between time points (hereafter "bandwidth hyperparameter") and \\( \\sigma^{2}_f \\) determines the variance of the observations (hereafter "signal variance hyperparameter").

This can also be written as \\( k_{ij} = \\sigma_f^{2} c_{ij} \\), where \\( c_{ij} \\) is the correlation structure (as opposed to covariance).

The Gaussian Process observations are therefore a draw from the multivariate normal distribution \\( \\mathcal{GP} \\sim \\mathcal{N}(\\mu, K) \\).


#### Multi-channel Gaussian Processes

The description above is for a process, or "channel", that does not interact with other observations. If more than one channel is present, interactions between them can be modeled by a correlation structure that takes any "between-channel" covariance into account.

This can be achieved by a Matrix Normal distribution, which is equivalent to a Kronecker product of a matrix of signal variances for all channel combinations and the correlation matrix \\( c_{ij} \\) [Bonilla _et al._](https://papers.nips.cc/paper/3189-multi-task-gaussian-process-prediction); however, this formulation assumes the parameters that specify \\( c_{ij} \\) are the same of all channels and channel combinations. This can be relaxed, and even different kernels may be combined [Melkumyan and Ramos](https://www.ijcai.org/Proceedings/11/Papers/238.pdf), but this means the gaussian process can no longer be written as a Matrix Normal, and instead each channel combination needs to be specified individually.

For multiple channels , for instance, still using the exponential quadratic kernel, each channel has its own bandwidth parameter \\( \\ell_m \\), and each combination of channels their signal variance parameters \\( \\sigma^{2}_{mp} \\) (where the subscript _f_ was omitted for clarity), and each entry in the covariance matrix for this Gaussian Process is now given by:

$$ k_{mp}(x_{i},x_{j}) = \sigma^{2}_{mp} exp \left( \frac{-|x_{mi}-x_{pj}|^2}{\ell_m^2 + \ell_p^2} \right) $$

For two channels (uncreatively called channels \\(1\\) and \\(2\\) ), for instance, \\( \\ell_m, m=1,2 \\),  \\( \\sigma^{2}_{mp}, m,p=(1,1),(1,2),(2,1), (2,2) \\), and two observations for each channel ( \\( N_1=2, N_2=2\\) ), the square \\( K \\) matrix has dimension \\( 4 \\) (the sum \\( (N_1 + N_2)\\) of the number of time points of both channels), and is given by:

$$ K = \begin{bmatrix} \sigma^2_{11} \begin{bmatrix} k_{11}(x_{11},x_{11}) & k_{11}(x_{11},x_{12}) \\ k_{11}(x_{12},x_{11}) & k_{11}(x_{12},x_{12}) \end{bmatrix} \sigma^2_{12} \begin{bmatrix} k_{12}(x_{11},x_{21}) & k_{12}(x_{11},x_{22}) \\ k_{12}(x_{12},x_{21}) & k_{12}(x_{12},x_{22}) \end{bmatrix} \\ \sigma^2_{21} \begin{bmatrix} k_{21}(x_{21},x_{11}) & k_{21}(x_{21},x_{12}) \\ k_{21}(x_{22},x_{11}) & k_{21}(x_{22},x_{12}) \end{bmatrix} \sigma^2_{22} \begin{bmatrix} k_{22}(x_{21},x_{21}) & k_{22}(x_{21},x_{22}) \\ k_{22}(x_{22},x_{21}) & k_{22}(x_{22},x_{22}) \end{bmatrix} \end{bmatrix} $$

More generally, for \\( M \\) channels the dimension of the matrix is \\( \\sum_i^M N_i \\) (if all channels have the same number of observations the matrix will have size \\( MN \\times MN \\) ).

To complete the multivariate gaussian distribution, the means are given by a concatenation of the means for each observation for each channel \\(n, \\mu = vec(Y) = [\\mu_1, \\mu_2, ..., \\mu_n]^T\\).


#### Likelihood of non-gaussian observations

Normally distributed observations of a Gaussian Process with variance \\( \\sigma_n^2 \\) have log-likelihood given by the following expression:


$$ log\ p(\mathbf{y}|X) = -\frac{1}{2} \mathbf{y}^T(K+\sigma_n^2I)^{-1}\mathbf{y} - \frac{1}{2}log|K+\sigma_n^2I| - \frac{n}{2}log 2\pi $$

which is simply the logarithm of the probability density from the multivariate normal distribution.

For non-gaussian observations the likelihood cannot be computed directly, since the Gaussian Process function depends on the gaussian observations drawn, which are not available. Instead the latter must be approximated or, under a Bayesian framework, sampled -- this is sometimes called Gaussian Process Classification (GPC) because it is often applied to categorical variables, but it actually applies to any distribution other than the normal, whether discrete or continuous.

Therefore, given an approximation or sample of the unobserved gaussian observations, the GP function can be computed, and from that point on any likelihood distribution can be used on top of it to infer parameters based on the data that is actually observed.


#### Stan implementation
The model described above was implemented in Stan with the \\( \\ell_m \\) and \\( \\sigma^2_{mp} \\) parameters being sampled via _MCMC_, and the \\( K \\) matrix of size \\(MN \\times MN \\) matrix being assembled as described above. Standard gaussian variables, \\( \\tilde{f} \\) were also sampled, and the samples from the multivariate gaussian were computed by talking the Cholesky decomposition of \\(  K \\) (\\(  L \\)), and multiplying the vector of standard normal variables, the mean of the Gaussian Process was computed as \\( f = exp(\\mu + L \\cdot \\tilde{f}) \\). A negative binomial distribution was used, parameterized with the mean \\( f \\), and a free parameter \\( \\alpha \\) for the distribution's dispersion, or \\( y \\sim NegBinom2(f, \\alpha)\\) .

Inference was run for \\( 10^5\\) iterations using the HMC sampler with No U-Turn Sampling method and dense Euclidian metric.

1. [Carl Edward Rasmussen, Christopher K.I. Williams Gaussian. Processes for Machine Learning. MIT Press. 2006.](http://www.gaussianprocess.org/gpml/)
2. [Edwin V. Bonilla, Kian M. Chai, Christopher Williams](https://papers.nips.cc/paper/3189-multi-task-gaussian-process-prediction)
3. [Arman Melkumyan, Fabio Ramos, IJCAI 2011, Proceedings of the 22nd International Joint Conference on Artificial Intelligence, Barcelona, Catalonia, Spain, July 16-22, 2011](https://www.ijcai.org/Proceedings/11/Papers/238.pdf)

<!-- [//]: # (comment) -->
<!-- `-- caetano, {{ page.date | date: "%Y-%m-%d" }}` -->
