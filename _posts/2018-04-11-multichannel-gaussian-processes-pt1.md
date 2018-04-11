---
layout: post
title: "Multi-channel gaussian processes (part1: introduction)"
date: 2018-04-11
---

## [> {{ page.title}}](https://caesoma.github.io/archive/standalone/2018-03-07-multichannel-gaussian-processes)

Machine learning is all the rage these days, it is hard to hear about some new cool thing that doesn't involve the term, somewhat replacing the more vague and [Altered Carbon](https://motherboard.vice.com/en_us/article/a34dxe/altered-carbon-netflix-review) -invoking term AI (in trying to avoid clichés I should at least attempt to stay away from _Blade Runner_ references), and now-already-outdated ones like data mining, which these days sounds like something from the 1980s.
Apparently, most applications still seem to use neural networks, which can be very good at the job, but are actually stuff from the 80s as pointed out by people like [Ben Vigoda](https://tedxboston.org/speaker/vigoda).

Alternatives to that approach include methods like gaussian processes; there are formal connection between the approaches (as there often are to many others) but the most basic connection is probably that they are all just statistics and inference with different flavors of linear algebra to glue everything together -- i.e. "machine learning" is not a separate, more sophisticated class of methods in any real way.
Gaussian processes (GPs) are no exception; coming from the side of traditional statistics they are basically linear regression formulated in a clever way that is able to explore useful properties of basis functions and the gaussian distribution to be more flexible than fitting a straight line or an unknowable polynomial.
Therefore, besides its representation as jointly normal variables with correlations specified by a kernel, gaussian processes can be formalized as a traditional linear regression, and this is called _dual-representation_.

While linear models, and/or others based on normally-distributed data are still widely used in experimental science, normally not even the scientists believe their process of interest really conforms to that kind of model.
Non-linear parametric models are more sophisticated alternatives, and can be formulated as coupled differential equations (ODEs) that (somewhat) mechanistically represent the processes of interest, and often require numerical approaches to both obtain an output and infer their parameters.
Although only a few fields [(like epidemiology) have a basic model](http://mathworld.wolfram.com/SIRModel.html) of that serves as basis for almost every other extension, I believe this kind of models should be the ultimate goal of modeling any system.

Gaussian processes are somewhat non-parametric models (they do have parameters, but they are quite flexible and therefore do not have a very predefined shape of the outputs), and can in some cases be seen as in-between inflexible linear models, and computationally-intensive, complex parametric models.
Nevertheless, there are several shortcomings of the regular GP-regression that need to be addressed to make it useful for inference, and prevent scientists from incurring in the same errors of using linear models indiscriminately.
One of the limitations is that observations are assumed to be normally distributed; for traditional linear models this is dealt with by extending them to have non-gaussian likelihoods, converting them into what is called generalized linear models (GLMs) -- GPs can also be extended in a somewhat similar way, which I should discuss sometime soon.
Another thing is that GPs normally describe a univariate function, which does not capture interaction between processes like many models of coupled ODEs -- this is what I am going to start to address in this post and its part-two follow-up.

While it is technically possible to have independent functions describing the different observed processes, for many systems the main interest is in determining the interaction parameters: for [predator-prey](http://mathworld.wolfram.com/Lotka-VolterraEquations.html) models that would be the predation rate; for epidemiological models the transmission rate between infected and healthy individuals([Ross](http://rspa.royalsocietypublishing.org/content/92/638/204)); or for host-microbe interactions it would be the rate of clearing pathogens by the immune system
([Souto-Maior _et al._](http://journals.plos.org/plosntds/article?id=10.1371/journal.pntd.0006339)).
So apart from assuming independence, there may be different ways of coupling gaussian processes; I am going to describe a formulation that can be made with essentially the same constructs used for single-channel processes.

There are plenty of good references that describe the basics of gaussian processes formally (see [Rasmussen, Williams](http://www.gaussianprocess.org/gpml/), whose notation we follow when applicable). More casual explanations can be found, like that in [Kat Bailey's blog](http://katbailey.github.io/post/gaussian-processes-for-dummies/), with some code in Python that I found quite useful for a practical implementation.
I recommend getting familiarized with some of the theory and computational implementations of gaussian processes before moving on to multi-channel versions of the method.

Some of the features I will describe in the next post are outlined in two papers from [Bonilla et al.](https://papers.nips.cc/paper/3189-multi-task-gaussian-process-prediction.pdf), and [Melkumyan and Ramos](https://www.ijcai.org/Proceedings/11/Papers/238.pdf). The result are interacting processes with kernels between the different tasks, and a covariance matrix that defines the intensity of the interactions between the channels. That may be useful to improve inference, and especially to identify the magnitude of the interactions between channels, which can be informative about the mechanisms of the system.
l\Like any other statistical method there are situations where machine learning applies and others where it doesn't; claiming to use machine learning is a fast way to associate to the state-of-the-art, but these days it is more often a red flag than a sign of wisdom.



1. [Carl Edward Rasmussen, Christopher K.I. Williams Gaussian. Processes for Machine Learning. MIT Press. 2006.](http://www.gaussianprocess.org/gpml/)
