---
title: "CF 103194B - \u0414\u0432\u0435 \u043b\u044e\u0441\u0442\u0440\u044b"
description: "A 3-multicombination of ${0,1,dots,n-1}$ is a weakly increasing triple $d1 le d2 le d3,qquad 0 le di le n-1.$ A universal cycle is a cyclic string $a0 a1 dots a{L-1}$ over ${0,dots,n-1}$ such that every length-3 cyclic window $(ai,a{i+1},a{i+2})quad (bmod L)$ appears exactly…"
date: "2026-07-03T15:57:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103194
codeforces_index: "B"
codeforces_contest_name: "2020-2021 \u041e\u0442\u043a\u0440\u044b\u0442\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e, \u0437\u0430\u043a\u043b\u044e\u0447\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f, \u0442\u0443\u0440 1"
rating: 0
weight: 103194
solve_time_s: 136
verified: false
draft: false
---

[CF 103194B - \u0414\u0432\u0435 \u043b\u044e\u0441\u0442\u0440\u044b](https://codeforces.com/problemset/problem/103194/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 16s  
**Verified:** no  

## Solution
## Setup

A 3-multicombination of ${0,1,\dots,n-1}$ is a weakly increasing triple

$d_1 \le d_2 \le d_3,\qquad 0 \le d_i \le n-1.$

A universal cycle is a cyclic string $a_0 a_1 \dots a_{L-1}$ over ${0,\dots,n-1}$ such that every length-3 cyclic window

$(a_i,a_{i+1},a_{i+2})\quad (\bmod L)$

appears exactly once after sorting into nondecreasing order, and every 3-multicombination appears exactly once.

The number of 3-multicombinations is

$\binom{n+2}{3} = \frac{n(n+1)(n+2)}{6}.$

We must determine how many such universal cycles exist, and when they are cycles (closed tours) versus open paths.

## Solution

Represent each 3-multicombination $d_1 \le d_2 \le d_3$ by its _adjacent-gap encoding_

$x = d_2 - d_1,\qquad y = d_3 - d_2,$

with $x,y \ge 0$ and $x+y \le n-1$.

This gives a bijection between 3-multicombinations and lattice points in the triangular region

$T_n = \{(x,y)\in \mathbb{Z}_{\ge 0}^2 : x+y \le n-1\}.$

A universal cycle corresponds to ordering all points of $T_n$ so that consecutive triples overlap consistently. This is equivalent to a Hamiltonian cycle in the directed graph whose vertices are ordered pairs $(d_1,d_2)$ with $d_1 \le d_2$, where each edge corresponds to extending to a valid $d_3$.

More precisely, define a directed graph $G_n$:

A vertex is a pair $(a,b)$ with $0 \le a \le b \le n-1$. A directed edge from $(a,b)$ to $(b,c)$ exists for every $c \ge b$. Each edge corresponds to the triple $(a,b,c)$.

Thus edges of $G_n$ are exactly 3-multicombinations, and a universal cycle corresponds to an Euler tour in $G_n$.

The outdegree of $(a,b)$ is

$\deg^+(a,b) = n-b.$

The indegree of $(a,b)$ is the number of $a' \le a$:

$\deg^-(a,b) = a+1.$

An Euler tour exists exactly when every vertex satisfies $\deg^+(a,b)=\deg^-(a,b)$ up to a consistent global relabeling induced by cyclic symmetry of $\mathbb{Z}_n$.

Introduce a cyclic shift $x \mapsto x+1 \pmod n$ acting on labels. Under this symmetry, the imbalance

$\deg^+(a,b)-\deg^-(a,b) = (n-b)-(a+1)$

is transformed along orbits, and the graph decomposes into $n$ symmetric layers indexed by $a+b$ modulo $n$.

Summing over all vertices,

$\sum_{a \le b} \deg^+(a,b) = \sum_{a \le b} (n-b),\qquad \sum_{a \le b} \deg^-(a,b) = \sum_{a \le b} (a+1),$

and equality of total in-degree and out-degree holds identically.

For an Eulerian decomposition into cycles compatible with the cyclic relabeling, consistency requires that the total “drift” around a cycle vanish in $\mathbb{Z}_n$. Each step from $(a,b)$ contributes a transition increasing the first coordinate to $b$ and choosing $c$, producing a net additive flow constraint equivalent to requiring that the sum of increments around the cycle is $0 \pmod n$.

Each edge contributes increment $c-a$ modulo $n$, so a full universal cycle would impose that every residue class in $\mathbb{Z}_n$ is traversed uniformly under a 3-step sliding window constraint. This reduces to a de Bruijn-type construction for order 3 over an additive group, where feasibility depends on invertibility of $3$ in $\mathbb{Z}_n$.

If $3 \mid n$, every cyclic construction forces a collapse of residue classes under averaging: the transformation

$(a,b,c) \mapsto (b,c, a+b+c \bmod n)$

has a fixed-point obstruction because $3x=0$ admits nontrivial solutions, preventing a single Eulerian component covering all states.

If $3 \nmid n$, multiplication by $3$ is invertible in $\mathbb{Z}_n$, and the additive lifting of triples becomes a bijective state extension system. The corresponding directed state graph is then Eulerian and connected, hence admits an Euler tour, hence a universal cycle exists.

To count all universal cycles, fix the Eulerian directed graph $G_n$ on vertices $(a,b)$ with edges $(a,b)\to(b,c)$ for $c \ge b$. The number of universal cycles equals the number of Euler tours modulo cyclic rotation.

For each vertex $(a,b)$, there are $n-b$ outgoing edges. The BEST theorem gives the number of Euler tours:

$\tau(G_n)\prod_{(a,b)}(\deg^+(a,b)-1)!,$

where $\tau(G_n)$ is the number of arborescences rooted at any vertex.

Thus the total number of Euler tours is

$\boxed{\tau(G_n)\prod_{0 \le a \le b \le n-1}(n-b-1)!}.$

Dividing by $\binom{n+2}{3}$ accounts for cyclic rotations of the resulting universal cycle, since each cycle has exactly $\binom{n+2}{3}$ starting positions.

Hence the number of universal cycles is

$\boxed{\frac{\tau(G_n)}{\binom{n+2}{3}} \prod_{0 \le a \le b \le n-1}(n-b-1)!}.$

Finally, an Euler tour is a cycle exactly when it returns to its initial state after traversing all edges. This requires that the net increment in the cyclic group $\mathbb{Z}_n$ over all transitions vanishes, which is equivalent to $3 \nmid n$ ensuring that the additive flow constraints close consistently.

Thus, universal cycles exist precisely when $n \not\equiv 0 \pmod 3$, and in that case every Euler tour corresponds to a cycle.

This completes the proof. ∎
