---
title: "CF 103652G - Cosmic Cleaner"
description: "Let $G$ be the Cayley graph of the symmetric group $Sn$ with generators $(alpha1,dots,alphak)$, and assume that each generator satisfies $$alphaj(x)=y$$ for fixed distinct symbols $x,y in {1,dots,n}$."
date: "2026-07-02T22:01:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103652
codeforces_index: "G"
codeforces_contest_name: "2019 Summer Petrozavodsk Camp, Day 8: XIX Open Cup Onsite"
rating: 0
weight: 103652
solve_time_s: 126
verified: false
draft: false
---

[CF 103652G - Cosmic Cleaner](https://codeforces.com/problemset/problem/103652/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 6s  
**Verified:** no  

## Solution
## Solution

Let $G$ be the Cayley graph of the symmetric group $S_n$ with generators $(\alpha_1,\dots,\alpha_k)$, and assume that each generator satisfies

$$\alpha_j(x)=y$$

for fixed distinct symbols $x,y \in {1,\dots,n}$.

Let a Hamiltonian path in $G$ starting at the identity permutation $e=12\cdots n$ be given:

$$v_0=e,\ v_1,\dots,v_{N-1}, \quad N=n!.$$

For each step, there exists an index $j_i$ such that

$$v_{i+1}=v_i \alpha_{j_i}.$$

Define

$$a_i = v_i(x), \quad b_i = v_i(y).$$

From the transition rule and the assumption $\alpha_{j}(x)=y$, we obtain

$$v_{i+1}(x)=v_i(\alpha_{j_i}(x))=v_i(y),$$

hence

$$a_{i+1}=b_i \quad \text{for } 0 \le i \le N-2.$$

This identity links consecutive values of the sequences $(a_i)$ and $(b_i)$ by a shift:

$$b_i=a_{i+1}.$$

The sequence $(a_i)$ is the list of values taken by the function $g \mapsto g(x)$ along the Hamiltonian path. Since each vertex of $S_n$ appears exactly once, $(a_0,a_1,\dots,a_{N-1})$ is a permutation of ${1,\dots,n}$.

From $b_i=a_{i+1}$ for $0 \le i \le N-2$, the sequence $(b_0,\dots,b_{N-2})$ is exactly the subsequence

$$(a_1,a_2,\dots,a_{N-1}).$$

Therefore $(b_0,\dots,b_{N-2})$ contains every element of ${1,\dots,n}$ except $a_0$.

At the initial vertex $v_0=e$, we have $a_0=e(x)=x$. Hence the value $x$ does not appear in $(b_0,\dots,b_{N-2})$. Since $(b_0,\dots,b_{N-1})$ is also a permutation of ${1,\dots,n}$, the missing value must occur at the final position:

$$b_{N-1}=x.$$

Thus

$$v_{N-1}(y)=x.$$

This completes the proof. ∎
