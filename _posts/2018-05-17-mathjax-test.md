---
layout: post
title: "Mathematical symbols and equations with MathJax rendering of \\( \LaTeX \\) symbols"
date: 2018-05-17
mathjax: true
---

## [> {{ page.title }} ](https://caesoma.github.io/archive/standalone/2018-05-17-mathjax-test.md)

  I  wanted (and still want) to keep this page/blog as simple as possible, which meant not including any JavaScript at all or anything "fancy". So I'd have text, figures, and any mathematical symbols or equations would just be figures as well from the very handy [LaTeXiT](https://www.chachatelier.fr/latexit/).
However, being a regular \\( \LaTeX \\) user it would be very convenient to be able to just write equations _inline_ and _display_ style so when googling I found out about [MathJax](https://www.mathjax.org/). There are many howtos on google for how to incorporate the MathJax scripts into GitHub pages, and you can just copy a [snippet](https://github.com/caesoma/caesoma.github.io/blob/master/_includes/mathjax.html) into your default layout page, but it took me a little more work with the liquid tags to load the scripts only for [posts where I set the mathjax flag](https://github.com/caesoma/caesoma.github.io/blob/master/index.html), so there's an example of trying to keep that simple.
So it's nice to be able to write simpler equations inline like this: \\( e^{i\pi} + 1= 0 \\), or longer ones like that:

\\begin{equation}
    i \frac{h}{2\pi} \frac{\partial}{\partial t} \Psi (x,t) = = \frac{h}{4m\pi}\frac{\partial^2}{\partialx^2} \Psi (x,t) + V(x)\Psi (x,t) 
\\end{equation}

so anyway, since I had a test post to include the scripts and write some equations I'm going to leave this here in case it is helpful for someone trying to blog with some pretty math.

<!-- [//]: # (comment) -->

<!-- `-- caetano, {{ page.date | date: "%Y-%m-%d" }}` -->
