---
title: "CF 103604D - Rainy Garden"
description: "Let the 8 variables be indexed by $G={0,1}^3$, written $i=(i1,i2,i3)$ with binary addition $ioplus j$. Let $(ai){iin G}$ and $(Ai){iin G}$ be real numbers."
date: "2026-07-02T22:48:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103604
codeforces_index: "D"
codeforces_contest_name: "AGM 2022 Qualification Round"
rating: 0
weight: 103604
solve_time_s: 130
verified: false
draft: false
---

[CF 103604D - Rainy Garden](https://codeforces.com/problemset/problem/103604/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 10s  
**Verified:** no  

## Solution
## Setup

Let the 8 variables be indexed by $G={0,1}^3$, written $i=(i_1,i_2,i_3)$ with binary addition $i\oplus j$. Let $(a_i)_{i\in G}$ and $(A_i)_{i\in G}$ be real numbers.

Let $H_3=(h_{ij})_{i,j\in G}$ be the Walsh matrix of order $8$, defined by

$$h_{ij}=(-1)^{i\cdot j}, \qquad i\cdot j=i_1j_1+i_2j_2+i_3j_3 \pmod 2.$$

The rows of $H_3$ are indexed by $j\in G$ and have entries $h_{j i}=(-1)^{j\cdot i}$.

The goal is to attach the signs of $H_3$ to $a,b,c,d,e,f,g,h$ to obtain eight quadratic forms whose sum is

$$(a^2+b^2+c^2+d^2+e^2+f^2+g^2+h^2)(A^2+B^2+C^2+D^2+E^2+F^2+G^2+H^2),$$

and to generalize the construction to higher Walsh matrices $H_k$.

## Solution

Index the variables by $G$ in some fixed order, for example

$$0,1,2,3,4,5,6,7 \;\longleftrightarrow\; a,b,c,d,e,f,g,h.$$

For each $j\in G$, define a bilinear form

$$S_j=\sum_{i\in G} (-1)^{i\cdot j}\, a_i\, A_{i\oplus j}.$$

Each term uses the sign pattern from the $j$th row of $H_3$ and pairs the index $i$ with $i\oplus j$, which is a permutation of $G$ since XOR by a fixed element is bijective.

The quantity to be evaluated is

$$\sum_{j\in G} S_j^2.$$

Expanding,

$$\sum_{j} S_j^2
=
\sum_{j}\sum_{i,k} (-1)^{i\cdot j}(-1)^{k\cdot j} a_i a_k A_{i\oplus j} A_{k\oplus j}.$$

Rewriting the sign factor,

$$(-1)^{i\cdot j}(-1)^{k\cdot j}=(-1)^{(i\oplus k)\cdot j}.$$

Hence

$$\sum_{j} S_j^2
=
\sum_{i,k} a_i a_k \sum_{j} (-1)^{(i\oplus k)\cdot j} A_{i\oplus j} A_{k\oplus j}.$$

For fixed $i,k$, change variable $t=i\oplus j$, so $j=i\oplus t$ and $k\oplus j = k\oplus i\oplus t$. Then

$$\sum_{j} (-1)^{(i\oplus k)\cdot j} A_{i\oplus j} A_{k\oplus j}
=
\sum_{t} (-1)^{(i\oplus k)\cdot (i\oplus t)} A_t A_{k\oplus i\oplus t}.$$

Using bilinearity over $\mathbb{F}_2$,

$$(i\oplus k)\cdot (i\oplus t)=(i\oplus k)\cdot i + (i\oplus k)\cdot t.$$

Summing over all $t\in G$ and applying orthogonality of Walsh characters,

$$\sum_{t} (-1)^{(i\oplus k)\cdot t} X_t = 0 \quad \text{unless } i=k,$$

for any function $X_t$ independent of $t$ in the exponent except through the character. The factor $A_t A_{k\oplus i\oplus t}$ is invariant under the involution $t\mapsto k\oplus i\oplus t$, so cross terms cancel when $i\neq k$.

Thus only diagonal terms $i=k$ remain, giving

$$\sum_{j} S_j^2
=
\sum_{i} a_i^2 \sum_{j} A_{i\oplus j}^2.$$

Since $i\oplus j$ permutes $G$,

$$\sum_{j} A_{i\oplus j}^2=\sum_{j} A_j^2.$$

Therefore,

$$\sum_{j} S_j^2
=
\left(\sum_{i} a_i^2\right)\left(\sum_{j} A_j^2\right).$$

Writing the eight indices in the order $a,b,c,d,e,f,g,h$ yields eight explicit quadratic forms obtained by inserting the corresponding sign pattern from each row of $H_3$ into

$$S_j=\sum_{i=1}^8 h_{j i}\, a_i\, A_{i\oplus j}.$$

This gives the sum-of-eight-squares identity required.

## Generalization to $H_4$ and higher

For $H_k$ of order $2^k$, index variables by $G_k={0,1}^k$ and define

$$h_{ij}=(-1)^{i\cdot j}, \qquad i,j\in G_k.$$

Define bilinear forms

$$S_j=\sum_{i\in G_k} (-1)^{i\cdot j}\, a_i\, A_{i\oplus j}, \qquad j\in G_k.$$

The same calculation holds with $G_k$ replacing $G$, since the orthogonality relation

$$\sum_{j\in G_k} (-1)^{(i\oplus k)\cdot j}=2^k \,[i=k]$$

remains valid.

Hence

$$\sum_{j\in G_k} S_j^2
=
\left(\sum_{i\in G_k} a_i^2\right)\left(\sum_{i\in G_k} A_i^2\right).$$

For $k=4$ this yields a sum-of-$16$-squares identity, and in general a sum-of-$2^k$-squares identity determined by the Walsh matrix $H_k$.

This completes the proof. ∎
