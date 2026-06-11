---
title: "CF 1333D - Challenges in school \u211641"
description: "The reviewer is correct. The displayed sequences are not addition chains, because the quantities $2^g,2^h,2^k,2^m$ were used as summands without first appearing as chain elements. The argument must be rebuilt from the definition of a star chain."
date: "2026-06-11T16:03:40+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "games", "graphs", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1333
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 632 (Div. 2)"
rating: 2100
weight: 1333
solve_time_s: 70
verified: false
draft: false
---

[CF 1333D - Challenges in school \u211641](https://codeforces.com/problemset/problem/1333/D)

**Rating:** 2100  
**Tags:** brute force, constructive algorithms, games, graphs, greedy, implementation, sortings  
**Solve time:** 1m 10s  
**Verified:** no  

## Solution
The reviewer is correct. The displayed sequences are not addition chains, because the quantities $2^g,2^h,2^k,2^m$ were used as summands without first appearing as chain elements. The argument must be rebuilt from the definition of a star chain.

Let the four cases of Theorem C be

$$n=2^m+1,$$

$$n=2^m+2^k+1 \qquad (m>k\ge 0),$$

$$n=2^m+2^k+2^h+1 \qquad (m>k>h\ge 0),$$

$$n=2^m+2^k+2^h+2^g+1
\qquad (m>k>h>g\ge 0).$$

In each case $A$ is the number of powers of $2$ occurring in $n-1$. We must exhibit a star chain of length $A+2$.

Recall that a star chain satisfies

$$a_r=a_{r-1}+a_j,
\qquad j<r.$$

Hence every new term must be obtained from the immediately preceding term by adding an earlier chain element.

The key observation is that the powers of two themselves already form a star chain:

$$1,2,4,\ldots,2^m.$$

Once $2^m$ has been reached, each smaller power of two appearing in the binary expansion of $n-1$ is already available as an earlier chain element. We may then add those powers successively to the current value.

### Case 1

Let

$$n=2^m+1.$$

Consider the chain

$$1,2,4,\ldots,2^m,2^m+1.$$

The first $m$ steps are doublings,

$$2^r=2^{r-1}+2^{r-1},$$

so they are star steps.

The final step is

$$2^m+1=2^m+1,$$

where $1$ is the first element of the chain.

Thus this is a star chain.

Its length is

$$m+1.$$

In Theorem C, for this case,

$$A=m-1,$$

hence

$$A+2=m+1.$$

Therefore the required length is achieved.

### Case 2

Let

$$n=2^m+2^k+1,
\qquad m>k\ge0.$$

Take

$$1,2,4,\ldots,2^m,
\quad
2^m+2^k,
\quad
2^m+2^k+1.$$

After reaching $2^m$, the element $2^k$ already occurs earlier in the chain. Hence

$$2^m+2^k
=
2^m+2^k$$

is a star step.

Since $1$ is also an earlier chain element,

$$2^m+2^k+1
=
(2^m+2^k)+1$$

is another star step.

Therefore the whole chain is a star chain.

Its length is

$$m+2.$$

For this case of Theorem C,

$$A=m,$$

so

$$A+2=m+2.$$

### Case 3

Let

$$n=2^m+2^k+2^h+1,
\qquad m>k>h\ge0.$$

Consider

$$1,2,4,\ldots,2^m,
\quad
2^m+2^k,
\quad
2^m+2^k+2^h,
\quad
2^m+2^k+2^h+1.$$

The powers $2^k$ and $2^h$ already appear earlier in the chain, so

$$2^m+2^k
=
2^m+2^k,$$

and

$$2^m+2^k+2^h
=
(2^m+2^k)+2^h$$

are star steps.

Finally,

$$2^m+2^k+2^h+1
=
(2^m+2^k+2^h)+1,$$

and $1$ is an earlier chain element.

Hence the chain is a star chain.

Its length is

$$m+3.$$

For this case,

$$A=m+1,$$

therefore

$$A+2=m+3.$$

### Case 4

Let

$$n=2^m+2^k+2^h+2^g+1,
\qquad m>k>h>g\ge0.$$

Take

$$1,2,4,\ldots,2^m,$$

followed by

$$2^m+2^k,$$

$$2^m+2^k+2^h,$$

$$2^m+2^k+2^h+2^g,$$

$$2^m+2^k+2^h+2^g+1.$$

Each of the powers

$$2^k,\quad 2^h,\quad 2^g,$$

already occurs earlier in the chain, and $1$ is the initial element. Hence every one of the final four steps has the form

$$a_r=a_{r-1}+a_j$$

with $j<r$.

Thus the chain is a star chain.

Its length is

$$m+4.$$

For this case,

$$A=m+2,$$

so

$$A+2=m+4.$$

In all four cases we have constructed explicit star chains whose lengths are exactly $A+2$. Consequently the statement of Theorem C remains true when $l$ is replaced by $l^*$. ∎
