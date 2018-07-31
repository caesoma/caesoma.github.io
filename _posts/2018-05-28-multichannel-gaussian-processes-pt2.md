---
layout: post
title: "Multi-channel gaussian processes (part 2: mathematical description)"
date: 2018-05-28
mathjax: true
---

## [> {{ page.title }} ](https://caesoma.github.io/archive/standalone/2018-05-28-multichannel-gaussian-processes-pt2)

  Most applications of the gaussian processes, whether it's regression or classification, have one channel (or task) with a set of observations \\( (y = f(x) + \varepsilon) \\) for some values of an independent variable \\( x \\) (the _training data_), and possibly a set of unobserved values \\( x_\star \\) for which we may like to predict the values.
Alternatively, we may want to infer the kernel parameters (or _hyperparameters_ as the machine learnists like to call it, \\( \sigma_f^2 \\), the signal variance, and \\( \ell \\), the bandwidth, in the "squared exponential kernel") that have higher probability of having generated the observed values.
<!-- As described by [Rasmussen and Williams Gaussian](http://www.gaussianprocess.org/gpml/) -- and apparently in -->

[Bonilla _et al._](https://papers.nips.cc/paper/3189-multi-task-gaussian-process-prediction) and [Melkumyan and Ramos](https://www.ijcai.org/Proceedings/11/Papers/238.pdf) describe multi channel, or multi task, gaussian processes; in some aspects they are complementary, so I will draw on both and on the thorough description of single channel GPs in [Rasmussen and Williams](http://www.gaussianprocess.org/gpml/), because that is how I managed to piece together everything I needed -- a [GitHub gist](https://gist.github.com/caesoma) implements an example of the description below.

Loosely speaking, gaussian processes are based on computing a matrix with the correlation between different data points, and multi-channel GPs extend that to include correlations between data of different channels, so while the matrix of training points correlations for \\( N \\) training points in a single channels results in a \\(N \times N\\) "\\( K \\) matrix" for a multiple channels results in a square matrix with the total number of training points, e.g. \\((N_1+N_2)\timesN_1+N_2)\\) for two channels.
Furthermore, the kernel parameters may depend on which channel the training point belongs to [[Melkumyan and Ramos](https://www.ijcai.org/Proceedings/11/Papers/238.pdf)]; normally the parameters of the squared exponential kernel, for instance, include the square of the bandwidth \\( 2\ell^2 \\), which arises from both data points coming from the same process.
In the case of covariance between different channels these parameters may differ, resulting in \\( \ell_1^2 + \ell_2^2 \\) instead of \\( \ell^2 + \ell^2 = 2\ell^2\\), indicated by the subscripts in \\( k_{lk} \\).

  Melkumyan and Ramos showed how to obtain these covariance functions for different kernels (also having a different kind of kernel for each channel).
The same applies to the signal variance of the process that multiplies the covariance matrix, instead of a single \\( \sigma_f^2 \\) for each channel that is extended to being a symmetric matrix of size \\(M \times M\\) for \\( M \\) channels giving the signal variance for each channel on the signal covariance between channels off of diagonal, that is what is described by [Bonilla _et al._](https://papers.nips.cc/paper/3189-multi-task-gaussian-process-prediction).
For instance, the entry of the matrix corresponding to the correlation between the \\( i^{th} \\) training point of channel \\( l \\) and the \\( j^{th} \\) of channel \\( k \\) has signal covariance (where we dropped the subscript \\( f\\) ) \\( \sigma_{kl}^2 \\) and bandwidth parameters \\( \ell_l \\) and \\( \ell_k \\), given then by

$$ k_{lk}(x_{li},x_{kj}) = \sigma^2_{lk} exp \left( \frac{-|x_{li}-x_{kj}|^2}{\ell_l^2 + \ell_k^2} \right) $$

<!-- where  \\(r = x_{11}-x_{21}\\). -->
To illustrate that, given two training points for channel 1 and two for channel 2, we have a covariance matrix of the following form:

$$ K = \begin{bmatrix} \sigma^2_{11} \begin{bmatrix} k_{11}(x_{11},x_{11}) & k_{11}(x_{11},x_{12}) \\ k_{11}(x_{12},x_{11}) & k_{11}(x_{12},x_{12}) \end{bmatrix} \sigma^2_{12} \begin{bmatrix} k_{12}(x_{11},x_{21}) & k_{12}(x_{11},x_{22}) \\ k_{12}(x_{12},x_{21}) & k_{12}(x_{12},x_{22}) \end{bmatrix} \\ \sigma^2_{21} \begin{bmatrix} k_{21}(x_{21},x_{11}) & k_{21}(x_{21},x_{12}) \\ k_{21}(x_{22},x_{11}) & k_{21}(x_{22},x_{12}) \end{bmatrix} \sigma^2_{22} \begin{bmatrix} k_{22}(x_{21},x_{21}) & k_{22}(x_{21},x_{22}) \\ k_{22}(x_{22},x_{21}) & k_{22}(x_{22},x_{22}) \end{bmatrix} \end{bmatrix} $$

<!-- ![Kmatrix](/images/latexit/Kmatrix.png) -->

<!-- [//]: # (K = \\\begin{bmatrix} k_{11}(x_{11},x_{11}) & k_{11}(x_{11},x_{12}) & k_{12}(x_{11},x_{21}) & k_{12}(x_{11},x_{22}) \\ k_{11}(x_{12},x_{11}) & k_{11}(x_{12},x_{12}) & k_{12}(x_{12},x_{21}) & k_{12}(x_{12},x_{22}) \\ k_{21}(x_{21},x_{11}) & k_{21}(x_{21},x_{12}) & k_{22}(x_{21},x_{21}) & k_{22}(x_{21},x_{22}) \\ k_{21}(x_{22},x_{11}) & k_{21}(x_{22},x_{12}) & k_{22}(x_{22},x_{21}) & k_{22}(x_{22},x_{22}) \\end{bmatrix}) -->

  So basically the covariance matrix for the training points is built the same way as for a single channel, with the blocks in the diagonal being the same as for a single channel model, and the blocks off the diagonal having a signal covariance and combining the kernels of the pairs of channels.

  Conceptually it is pretty simple, but actually trying to write it down and implementing it as code can be confusing at times, so it takes some staring at its repetitive structure to internalize it.

  From here there are at least two ways we can go: you may want to predict the values at other values of \\( x \\) that were not observed, and you can estimate the _hyperparameters_.
In the first case, given the \\( K \\) matrix and the concatenated one-dimensional vector of the observations \\( y = [y_1 y_2]\\) the mean and variance of an unobserved data point from a channel _l_ can be predicted with the following expressions:


$$ \bar{f}_{l\star} = \mathbf{k_{l\star}}^T(K+\sigma_n^2I)^{-1}\mathbf{y} \\
Var[\bar{f}_{l\star}] = \mathbf{k_{l\star\star}} - \mathbf{k_{l\star}}^T(K+\sigma_n^2I)^{-1}\mathbf{k_{l\star}} $$

Those expressions are entirely analogous to the single channel ones described by Rasmussen and Williams, just observing the combination of hyperparameters between channels.

  Bringing together that formulation with what's described in the papers I cite, Bonilla _et al._ write the _covariance_ matrix as a kronecker product \\( K = K_f \otimes K^x \\), where \\( K_f \\) is the positive semidefinite matrix with the variance intensity of each single channel, and the covariance between channels, and \\( K^x \\) are the correlation matrix blocks for each channel and between channels. To write this as this kronecker product the correlation blocks (\\(K^x\\)) must be assumed to be the same, and if there is no noise added to the correlation matrix, the gaussian process can be written as an expression independent of the (\\(K_f\\)) matrix:

\begin{align} \\bar{f}(\\mathbf{x_\star}) &= (K_f \\otimes \\mathbf{k_\star^x})^T (K_f \\otimes K^x)^{-1}\\mathbf{y} \\\\ &= (K_f(Kf)^{-1}) \\otimes ((\\mathbf{k_\star^x})^T (K^x)^{-1})\\mathbf{y} \\\\ &= I \\otimes ((\\mathbf{k_\star^x})^T (K^x)^{-1})\\mathbf{y} \end{align}

  Therefore, the authors argue that in a noiseless process there is no transfer between the channels, but that is only the case if the matrix can be written as that kronecker product, i.e. the submatrices making it up are the same. For the formulation where we have different hyperparameters (here \\( \ell \\)), the blocks are different even in the absence of added noise, so there is transfer regardless.

  That whole formulation is implemented in Python in [this GitHub gist](https://gist.github.com/caesoma/ee16f5fbcca8c9dfb9eb03cf34837896); the implementation uses for loops to set up all matrices; if you want to stick to Python that can be sped up by using numpy arrays for some operations, but I wanted to put it like that to make the function structure simpler to read (if you have any comments about the implementation, feel free to comment on the gist).
The true values are drawn from independent sinusoidal functions, so they don't represent actual interactions between the channels. For any useful modeling of, say, a biological system we would need to estimate the parameters to get an estimate of the interactions between channels.

  Estimating the hyperparameters requires computing the likelihood, which for gaussian noise has a closed form with \\( y \sim \mathcal{N}(\mu, K+\sigma_n^2I)\\). From there with the expression for the normal distribution the log likelihood can be explicitly written as:

$$ log\ p(\mathbf{y}|X) = -\frac{1}{2} \mathbf{y}^T(K+\sigma_n^2I)^{-1}\mathbf{y} - \frac{1}{2}log|K+\sigma_n^2I| - \frac{n}{2}log 2\pi $$

Beyond this, I'm not going into inference in this post to try and keep things separate, but will probably address it later on when discussing non-gaussian likelihoods (in my opinion somewhat misleadingly called gaussian process classification, or _GPC_).
Let me know if you have any more questions by commenting on the gist or via twitter.

**References**
1. [Carl Edward Rasmussen, Christopher K.I. Williams Gaussian. Processes for Machine Learning. MIT Press. 2006.](http://www.gaussianprocess.org/gpml/)
2. [Edwin V. Bonilla, Kian M. Chai, Christopher Williams](https://papers.nips.cc/paper/3189-multi-task-gaussian-process-prediction)
3. [Arman Melkumyan, Fabio Ramos, IJCAI 2011, Proceedings of the 22nd International Joint Conference on Artificial Intelligence, Barcelona, Catalonia, Spain, July 16-22, 2011](https://www.ijcai.org/Proceedings/11/Papers/238.pdf)

<!-- `-- caetano, {{ page.date | date: "%Y-%m-%d" }}` -->

<!-- [//]: # ()
4. [David J.C. MacKay. Introduction to Gaussian Processes. In Bishop, C.M. editor, Neural Networks and Machine Learning. pp 84-92. Springer-Verlag. 1998.](http://www.inference.org.uk/mackay/gpB.pdf)
5. [Christopher Bishop. Pattern Recognition and Machine Learning. pp 311. Springer. 2006.](http://users.isr.ist.utl.pt/~wurmd/Livros/school/Bishop%20-%20Pattern%20Recognition%20And%20Machine%20Learning%20-%20Springer%20%202006.pdf)
-->