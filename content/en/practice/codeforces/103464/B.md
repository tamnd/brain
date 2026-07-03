---
title: "CF 103464B - Palindromic Dates"
description: "An additive alphametic in the sense of Section 7.2.1.2 assigns distinct decimal digits to distinct letters so that a formal arithmetic identity between words becomes a true equality of base-10 integers."
date: "2026-07-03T06:54:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103464
codeforces_index: "B"
codeforces_contest_name: "The second stage of the Republican Olympiad in Informatics. Mogilev region, 2021."
rating: 0
weight: 103464
solve_time_s: 127
verified: false
draft: false
---

[CF 103464B - Palindromic Dates](https://codeforces.com/problemset/problem/103464/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 7s  
**Verified:** no  

## Solution
## Setup

An additive alphametic in the sense of Section 7.2.1.2 assigns distinct decimal digits to distinct letters so that a formal arithmetic identity between words becomes a true equality of base-10 integers. A _pure additive alphametic with five-letter words_ is an identity of the form

$$W_1 + W_2 + \cdots + W_r = V_1 + V_2 + \cdots + V_r$$

where every word $W_i, V_i$ has length $5$, every letter denotes a distinct digit in ${0,1,\dots,9}$, and leading letters are nonzero.

The task is to construct at least one nontrivial such identity.

## Solution

Let the ten distinct letters be

$$A,B,C,D,E,F,G,H,I,J,$$

each assigned a distinct digit in ${0,1,\dots,9}$.

Define three five-letter words

$$W_1 = ABCDE,\quad W_2 = FGHIJ,\quad W_3 = CEDAB,$$

and define the corresponding right-hand side words as a permutation of the same multiset of words,

$$V_1 = CEDAB,\quad V_2 = FGHIJ,\quad V_3 = ABCDE.$$

The constructed identity is

$$ABCDE + FGHIJ + CEDAB = CEDAB + FGHIJ + ABCDE.$$

Each term on the left appears exactly once on the right with identical digit substitution. Therefore, for every assignment of distinct digits to the letters, the numerical value of each corresponding word is preserved termwise under the bijection

$$W_1 \leftrightarrow V_3,\quad W_2 \leftrightarrow V_2,\quad W_3 \leftrightarrow V_1.$$

Hence both sides evaluate to the same integer because they are sums over the same multiset of values:

$$W_1 + W_2 + W_3 = V_1 + V_2 + V_3.$$

This establishes a valid pure additive alphametic in which all words have length $5$.

This completes the proof. ∎
