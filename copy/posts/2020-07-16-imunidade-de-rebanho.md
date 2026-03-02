---
author: caetano
title: "Luz no fim da 'imunidade de rebanho'?"
date: 2020-07-20
layout: post
---

Desde que o governo britânico decidiu usar a estratégia de imunidade de rebanho (e desistiu por que alguém que entende alguma coisa do assunto avisou a eles que isso não era estratégia coisa nenhuma) o assunto tem meio parado no ar. Nas últimas semanas o assunto voltou à baila com a publicação na revista [Science](https://www.sciencemag.org/) de um dos preprints que meio começaram essa discussão há mais de dois meses: [Britton et al. 2020](https://arxiv.org/abs/2005.03085), além de [Gomes et al. 2020](https://www.medrxiv.org/content/10.1101/2020.04.27.20081893v3). Pra variar o assunto virou tema de polarização política, e a ciência ficou perdida no meio dos disse-me-disses, então aqui vai um resumo do que isos significa e não significa.

O numero de novas infecções causadas por um indivíduo infectado (\\(R_{eff}\\)) depende do número de pessoas suscetíveis na população (\\(S\\)). À medida que a população se infecta, recupera e fica imune esse número diminui naturalmente.

\\begin{align}
R_{eff} = R_0 \\cdot S
\\end{align}

Quando o número de pessoas suscetíveis é pequeno (a população imune é grande) o suficiente cada infectado transmite o vírus pra somente uma outra pessoa -- esse é "o pico". A partir daí o número de novos casos dimiui e uma hora a epidemia acaba.

A proporção mínima da população que deve ser imune pra que isso aconteça é o limiar de imuniade de rebanho ("herd immunity threshold", _HIT_), que é geralmente usado no contexto de vacinação. Na forulação mais básica, a expressão matemática pra esse limiar é:

\\begin{align}
HIT &= \\frac{R_0-1}{R_0} \\\\
&= 1 - \\frac{1}{R_0}
\\end{align}

Esse valor não é uma definição, é uma consequência da análise da dinâmica de um dos modelos mais básicos de transmissão. Pra um valor de \\(R_0 \\approx 2.4\\) temos \\( HIT \\approx 60\% \\) aproximadamente e como não existe vacina pra SARS-CoV-2 só é possível chegar a esse limiar com infecções reais e gente morrendo.

Esse modelo basicão, como todo modelo, tem premissas que permitem a suas construção e análise (o fazem tratável, na linguagem dos matemáticos). Uma dessas premissas é que todo mundo tem contato com todo mundo, todo mundo é igualmente suscetível -- ou seja, a população é homogênea. No mundo real algumas pessoas tem mais contatos que outras e/ou são mais suscetíveis que outras --  a população é heterogênea. Um modelo menos básico pode descrever isso, e uma das consequências é um pico e um _HIT_ mais baixos (por exemplo os 20-40% que andaram rolando por aí).

Esse é o resumo de alguns artigos recentes: modelo mais realista, HIT mais baixo. A explicação mais simples pra esse fenômeno é que os grupos mais expostos se infectam mais rápido e transmissão diminui mais cedo. Além disso, é importante lembrar que esse limiar é a fração quando a epidemia começa a diminuir, não a fração final infectada. Dependendo das premissas do modelo (olha elas aí de novo, gente) a fração esperada pode bem mais alta, e a mortalidade total também.

Então, com essas ideas tem algumas consequências, por exemplo, o "achatamento da curva" pode ser visto como uma redução no _HIT_, que reduz o pico e a quantidade total de infectados -- essa ideia tá implícita numa matéria recente do [The Atlantic](https://www.theatlantic.com/health/archive/2020/07/herd-immunity-coronavirus/614035/). A segunda onda é o "desachatamento da curva": quando você aumenta o \\(R_0\\) o _HIT_ aumenta e a incidência volta a aumentar. Num modelo heterogêneo isso também acontece, mas é mais complicado por que não temos só um parâmetro que muda (menor distanciamento, maior transmissão), mas uma rede de contatos complexa, e dependendo de como essa rede se reorgnaiza com o relaxamento a população pode voltar a uma situação parecida à de antes ou não.


Resumindo, descrever uma epidemia é uma tarefa complexa, e o papel do modelo matemático não é representar a realidade completa, mas aspectos úteis do processo. Entender esses aspectos premite prever o impacto de diferentes intervenções.
A gente discute essas ideias no [episódio 6](https://ministeriodaciencia.github.io/posts/2020-07-21-cant-touch-this.html) do podcast [Ministério da Ciência](https://ministeriodaciencia.github.io/ouca.html)







<!-- [//]: # (comment) -->
<!-- `-- caetano, {{ page.date | date: "%Y-%m-%d" }}` -->
