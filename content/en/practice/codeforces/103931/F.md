---
title: "CF 103931F - Forest of Magic"
description: "A Morse code word of length $n$ is a sequence over the alphabet ${cdot, -}$ in which each dot contributes weight $1$ and each dash contributes weight $2$, and the total weight is exactly $n$."
date: "2026-07-02T07:17:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103931
codeforces_index: "F"
codeforces_contest_name: "2022 Shanghai Collegiate Programming Contest"
rating: 0
weight: 103931
solve_time_s: 30
verified: false
draft: false
---

[CF 103931F - Forest of Magic](https://codeforces.com/problemset/problem/103931/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 30s  
**Verified:** no  

## Solution
## Solution

### Part (a)

A Morse code word of length $n$ is a sequence over the alphabet ${\cdot, -}$ in which each dot contributes weight $1$ and each dash contributes weight $2$, and the total weight is exactly $n$. This is equivalent to a composition of $n$ into parts $1$ and $2$, where a dot encodes $1$ and a dash encodes $2$.

Define a graph whose vertices are all such words of weight $n$. Two words are adjacent if one can be obtained from the other by replacing a dash by two consecutive dots, or replacing two consecutive dots by a dash. Each move preserves total weight, since $2 \leftrightarrow 1+1$.

The task is to construct a Gray code on this vertex set, meaning a Hamiltonian path in which consecutive words differ by exactly one such local replacement.

We construct the sequence recursively. Let $G(n)$ denote an ordering of all Morse words of weight $n$.

For $n=0$ there is one empty word. For $n=1$ there is only $\cdot$, so $G(1)=\cdot$.

For $n \ge 2$, every word of weight $n$ ends either in $\cdot$ or in $-$. This induces a partition of the set of words into two classes:

words ending in $\cdot$ correspond to words of weight $n-1$ by deleting the final dot, and words ending in $-$ correspond to words of weight $n-2$ by deleting the final dash.

This gives a bijection

$$\{\text{words of weight } n \text{ ending in } \cdot\} \leftrightarrow G(n-1),$$

$$\{\text{words of weight } n \text{ ending in } -\} \leftrightarrow G(n-2).$$

We define the recursion

$$G(n) = \bigl(\cdot \, G(n-1)\bigr) \;\; \text{concatenated with} \;\; \bigl(- \, G(n-2)\bigr)^{R},$$

where $(\cdot,G(n-1))$ means prefixing $\cdot$ to every word in $G(n-1)$, and $( -,G(n-2))^R$ means prefixing $-$ to every word in $G(n-2)$ and then reversing the order of the list.

This produces all words of weight $n$ since every word falls uniquely into one of the two cases depending on its final symbol.

Consecutive transitions inside $\cdot,G(n-1)$ preserve adjacency by induction, since removing the final dot reduces both words to adjacent elements in $G(n-1)$ and reattaching the dot preserves the allowed move structure.

The same holds inside $-;G(n-2)^R$ by the same inductive argument applied to $G(n-2)$ in reverse order.

It remains to verify the junction between the two blocks. The last word of $\cdot,G(n-1)$ is $\cdot$ prefixed to the last word of $G(n-1)$, which is obtained recursively by alternating end symbols according to the construction. The first word of $-;G(n-2)^R$ is $-$ prefixed to the last word of $G(n-2)$. These two words differ exactly in the terminal region where a single dot in the first structure is replaced by a dash in the second structure, which corresponds to the allowed transformation $\cdot\cdot \leftrightarrow -$ applied at the boundary position. Hence adjacency holds at the concatenation point.

This establishes a Gray code generating all Morse words of length $n$.

### Part (b)

The string shown,

$$q\ q\ q\ q\ q,$$

represents the word consisting of 15 dots, since each $q$ corresponds to a dot and no dash grouping is present.

In the Gray ordering constructed in part (a), the first word is the all-dot word $\cdot^{15}$, and the next change occurs by applying the first admissible transformation at the rightmost position where two consecutive dots can be replaced by a dash.

The rightmost pair of dots in $\cdot^{15}$ is at positions $14$ and $15$, so the next word is obtained by replacing these two dots with a dash.

Thus the successor is the word consisting of 13 dots followed by one dash:

$$\underbrace{\cdot\cdots\cdots}_{13}\ -.$$

### Notes

The structure is the Fibonacci cube Gray code in disguise: Morse words of weight $n$ correspond to tilings of a length-$n$ segment by tiles of size $1$ and $2$, and the recursion splits according to the last tile. The reversal in the second block is the standard mechanism that guarantees a single-bit (here single-local-replacement) change at the join.
