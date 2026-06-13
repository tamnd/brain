---
title: "CF 1512F - Education"
description: "Method 1b already provides the key idea. If $(umldots u1u0)3$ is a ternary integer, its decimal value is obtained from the nested form $$(cdots((umcdot3+u{m-1})cdot3+u{m-2})cdots)cdot3+u0.$$ For pencil-and-paper work this means: Start with the leading digit."
date: "2026-06-10T18:54:43+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1512
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 713 (Div. 3)"
rating: 1900
weight: 1512
solve_time_s: 168
verified: false
draft: false
---

[CF 1512F - Education](https://codeforces.com/problemset/problem/1512/F)

**Rating:** 1900  
**Tags:** brute force, dp, greedy, implementation  
**Solve time:** 2m 48s  
**Verified:** no  

## Solution
## Solution

Method 1b already provides the key idea. If

$(u_m\ldots u_1u_0)_3$

is a ternary integer, its decimal value is obtained from the nested form

$$(\cdots((u_m\cdot3+u_{m-1})\cdot3+u_{m-2})\cdots)\cdot3+u_0.$$

For pencil-and-paper work this means:

Start with the leading digit. Repeatedly multiply the current result by $3$ and add the next ternary digit.

Only multiplication by $3$ and addition of $0$, $1$, or $2$ are required.

For

$$(12120112120210)_3,$$

the computation proceeds as follows:

$$\begin{array}{rcl} 1 &\to& 1\cdot3+2=5,\\ 5 &\to& 5\cdot3+1=16,\\ 16 &\to& 16\cdot3+2=50,\\ 50 &\to& 50\cdot3+0=150,\\ 150 &\to& 150\cdot3+1=451,\\ 451 &\to& 451\cdot3+1=1354,\\ 1354 &\to& 1354\cdot3+2=4064,\\ 4064 &\to& 4064\cdot3+1=12193,\\ 12193 &\to& 12193\cdot3+2=36581,\\ 36581 &\to& 36581\cdot3+0=109743,\\ 109743 &\to& 109743\cdot3+2=329231,\\ 329231 &\to& 329231\cdot3+1=987694,\\ 987694 &\to& 987694\cdot3+0=2963082. \end{array}$$

Hence

$$(12120112120210)_3=(2963082)_{10}.$$

Therefore the decimal value is

$$\boxed{2963082}.$$

To convert in the opposite direction, from decimal to ternary, use Method 1a with $B=3$. Repeatedly divide by $3$ and record the remainders.

For an integer $u$,

$$u=3q_0+r_0,\qquad 0\le r_0<3,$$

then

$$q_0=3q_1+r_1,$$

and so on until the quotient becomes $0$. The ternary digits are the remainders read in reverse order:

$$u=(\ldots r_2r_1r_0)_3.$$

Thus a rapid ternary-to-decimal method is repeated multiplication by $3$ and addition of the next digit; a rapid decimal-to-ternary method is repeated division by $3$ with remainders.

∎
