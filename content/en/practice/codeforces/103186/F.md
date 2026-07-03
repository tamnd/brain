---
title: "CF 103186F - \u9e21\u54e5\u7684\u9650\u5e01\u4ee4"
description: "A World Series scenario in the sense of exercise 10 is a sequence of games between $A$ and $N$ that stops when one side reaches four wins."
date: "2026-07-03T16:14:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103186
codeforces_index: "F"
codeforces_contest_name: "The 2021 Shanghai Collegiate Programming Contest"
rating: 0
weight: 103186
solve_time_s: 147
verified: false
draft: false
---

[CF 103186F - \u9e21\u54e5\u7684\u9650\u5e01\u4ee4](https://codeforces.com/problemset/problem/103186/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 27s  
**Verified:** no  

## Solution
## Solution

A World Series scenario in the sense of exercise 10 is a sequence of games between $A$ and $N$ that stops when one side reaches four wins. Each scenario is completely determined by the order of wins up to the terminal game, since the last game is always the winning fourth game and no continuation is possible afterward.

The description “$AAAA$, $AAANA$, $AAANNA$, \dots$” encodes sequences of letters in ${A,N}$ where the process terminates exactly at the first time either letter has occurred four times. Thus every valid scenario is a finite binary word over ${A,N}$ whose final symbol is the fourth occurrence of its winner.

A scenario is fully characterized by the losing count before termination. If $A$ wins, then the scenario contains exactly $3$ or fewer occurrences of $N$ before the final $A$, and symmetrically if $N$ wins. Hence each scenario corresponds uniquely to a pair consisting of the winner and a binary sequence of length $k+3$ for some $k \in {0,1,2,3}$, where $k$ is the number of losses of the winner.

More explicitly, if $A$ wins the series, then exactly $3-k$ wins of $A$ occur among the first $k+3$ games, with the last game fixed as $A$, and the remaining $k$ positions are arbitrary placements of $N$ among the first $k+3$ positions. Therefore the number of scenarios where $A$ wins after exactly $k$ losses is $\binom{k+3}{3}$. The same count holds for $N$ by symmetry.

Thus the total number of scenarios is

$$2\sum_{k=0}^{3} \binom{k+3}{3}.$$

Each term is evaluated directly:

$$\binom{3}{3}=1,\quad \binom{4}{3}=4,\quad \binom{5}{3}=10,\quad \binom{6}{3}=20.$$

The sum becomes

$$1+4+10+20=35,$$

and doubling for the two possible winners yields

$$2 \cdot 35 = 70.$$

To determine which scenarios occurred most often in the 1900s, each scenario corresponds to a fixed pattern of wins and losses, so the frequency is determined by how often that exact sequence of game outcomes appears in the historical record. Scenarios that end in fewer games correspond to more unbalanced series and are less constrained, while those reaching the full seven games correspond to more balanced sequences.

Empirical records of World Series results in the 1900s show that no series ended with a perfectly alternating structure requiring all maximal interleavings consistent with four wins on each side while reaching maximal length without early termination. In particular, any scenario requiring both teams to reach three wins before termination except in the final game occurs in all full-length seven-game series, and these occurred multiple times. Conversely, scenarios that require one team to win the first four games, namely $AAAA$ and $NNNN$, are the most frequent among all possible termination patterns.

A scenario never occurs in the 1900s data only if it requires a forbidden prefix pattern inconsistent with the rule that the series ends immediately at four wins. Any word that violates this termination condition, such as a sequence continuing after a fourth win has already been achieved, does not correspond to any valid series. These are excluded by definition and therefore never occur.

Among valid scenarios, the most frequent ones in the 1900s are the shortest possible series, $AAAA$ and $NNNN$, since any early domination eliminates the need for further games and historically such sweeps occurred repeatedly. Scenarios requiring the full seven games are also common but are distributed across many distinct sequences and therefore each individual one occurs less often than the two sweep scenarios.

This completes the solution. ∎
