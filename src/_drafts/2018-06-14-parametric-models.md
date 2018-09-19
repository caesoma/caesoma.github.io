---
layout: post
title: "Parametric models of natural processes should be the ultimate goal of quantitative descriptions in science"
date: 2018-04-13
mathjax: true
---

## [> {{ page.title }}](https://caesoma.github.io/archive/standalone/2018-06-14-parametric-models)

Like it or not, the machine learning hype, well, hyped up the interest in statistics and even more basic math-related subjects like linear algebra, differential calculus, and stuff that would made most my little friends in school cringe and decide to become lawyers right there and then, to the detriment of the world at large.
Somewhat like its wiser and less maligned cousin statistics, machine learning is a broad class of methods that aim at describing different kinds of data ranging from scientific experiments to add-clicking on whatever shitty social media site is (directly or indirectly) selling your data today. That is all fine and well, but as a scientist I am interested not in describing the data _per se_ but in associating the observed data to the processes generating them -- there is an apparently subtle difference there that often goes underappreciated.

Linear models, for instance, can be very useful to describe at least a simple trend, but the parameters most likely have no meaning. When fitted to a bacterial growth curve, for instance, the line intercept can be interpreted as the initial number of bacteria, but the slope really means nothing; in contrast the exponential growth parameter can be interpreted as the rate at which they double.
The point applies a lot more broadly; linear models (or their generalized, but still essentially linear versions) are the core of methods to analyze data like gene expression [[1](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-014-0550-8), [2](https://academic.oup.com/nar/article/43/7/e47/2414268)], plus each gene is treated as a linear model independent from all other genes.
There are few things I can think of that are more non-linear and coupled than genetic networks, and yet that is the state-of-the-art of analysis of the transcription of DNA into RNA and further gene products.



<!-- [//]: # (comment) -->

`-- caetano, {{ page.date | date: "%Y-%m-%d" }}`
