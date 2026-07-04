---
title: "CF 102956E - Brief Statements Union"
description: "The Twelvefold Way classifies placements of $n$ balls into $m$ urns according to whether balls and urns are labeled or unlabeled, and whether each urn is unrestricted, required to contain at most one ball, or required to contain at least one ball."
date: "2026-07-04T07:09:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102956
codeforces_index: "E"
codeforces_contest_name: "2020-2021 Winter Petrozavodsk Camp, Belarusian SU Contest (XXI Open Cup, Grand Prix of Belarus)"
rating: 0
weight: 102956
solve_time_s: 150
verified: false
draft: false
---

[CF 102956E - Brief Statements Union](https://codeforces.com/problemset/problem/102956/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 30s  
**Verified:** no  

## Solution
## Solution

The Twelvefold Way classifies placements of $n$ balls into $m$ urns according to whether balls and urns are labeled or unlabeled, and whether each urn is unrestricted, required to contain at most one ball, or required to contain at least one ball.

Each entry is a standard counting problem whose answer must remain correct when $m=0$ or $n=0$. In those boundary cases, the defining constraints determine whether the count is $0$ or $1$.

### 1. $n$ labeled balls, $m$ labeled urns

Each ball independently chooses one of $m$ urns, giving $m$ choices per ball. The total number of functions from an $n$-element set to an $m$-element set is therefore

$$m^n.$$

When $m=0$, no function exists unless $n=0$, in which case the empty function contributes $1$. Thus the formula $0^0=1$ is consistent in this context.

### 2. $n$ labeled balls, $m$ labeled urns, at most one ball per urn

This counts injections from an $n$-element set into an $m$-element set. If $n>m$, no injection exists. For $n\le m$, the number is

$$m(m-1)\cdots(m-n+1)=\frac{m!}{(m-n)!}.$$

If $n=0$, there is exactly one empty injection, so the value is $1$ for all $m$. If $m=0$, the value is $1$ when $n=0$ and $0$ otherwise.

### 3. $n$ labeled balls, $m$ labeled urns, at least one ball per urn

This counts surjections from an $n$-set onto an $m$-set. The number is given by inclusion-exclusion:

$$\sum_{k=0}^m (-1)^k \binom{m}{k}(m-k)^n.$$

When $m=0$, this equals $1$ if $n=0$ and $0$ otherwise, since the empty function is the only surjection onto the empty set.

### 4. $n$ unlabeled balls, $m$ labeled urns

This is the number of multisets of size $n$ drawn from an $m$-element set, equivalently weak compositions of $n$ into $m$ parts. The formula is

$$\binom{n+m-1}{m-1}=\binom{n+m-1}{n}.$$

When $m=0$, the only valid case is $n=0$, giving $1$. When $n=0$, all urns are empty, giving $1$ for every $m$.

### 5. $n$ unlabeled balls, $m$ labeled urns, at most one ball per urn

Each urn contains either $0$ or $1$ ball, so we choose $n$ urns from $m$. The number is

$$\binom{m}{n}.$$

This is $0$ when $n>m$, and equals $1$ when $n=0$ or $m=0$ with $n=0$.

### 6. $n$ unlabeled balls, $m$ labeled urns, at least one ball per urn

This counts compositions of $n$ into $m$ positive parts. The number is

$$\binom{n-1}{m-1}$$

for $n\ge m\ge 1$, and $0$ otherwise.

When $m=0$, the value is $1$ if $n=0$ and $0$ otherwise. When $n=0$, no positive parts exist unless $m=0$.

### 7. $n$ labeled balls, $m$ unlabeled urns

This counts partitions of an $n$-element set into at most $m$ blocks. The number is the restricted Bell number

$$\sum_{k=0}^m S(n,k),$$

where $S(n,k)$ is a Stirling number of the second kind.

When $m\ge n$, this becomes the Bell number $B_n$. When $n=0$, the value is $1$ for all $m$. When $m=0$, it is $1$ only if $n=0$.

### 8. $n$ labeled balls, $m$ unlabeled urns, at most one ball per urn

Each configuration corresponds to choosing a subset of balls of size at most $m$, since each occupied urn contains exactly one ball and urns are indistinguishable. Thus the number is

$$\sum_{k=0}^{\min(n,m)} \binom{n}{k}.$$

When $m\ge n$, this equals $2^n$. When $n=0$, it is $1$.

### 9. $n$ labeled balls, $m$ unlabeled urns, at least one ball per urn

This counts partitions of an $n$-set into exactly $m$ blocks:

$$S(n,m).$$

When $m>n$, the value is $0$. When $n=0$, it is $1$ if $m=0$ and $0$ otherwise.

### 10. $n$ unlabeled balls, $m$ unlabeled urns

This counts integer partitions of $n$ into at most $m$ parts:

$$p(n,\le m),$$

the number of partitions of $n$ with largest part count at most $m$.

When $m\ge n$, this equals the ordinary partition number $p(n)$. When $n=0$, the value is $1$ for all $m$.

### 11. $n$ unlabeled balls, $m$ unlabeled urns, at most one ball per urn

Since balls are identical and urns are identical, only the number of occupied urns matters, but occupancy is restricted to $0$ or $1$. A configuration exists only if $n\le m$, and in that case there is exactly one configuration. Hence the value is

$$[n\le m],$$

where $[P]$ is $1$ if $P$ is true and $0$ otherwise.

### 12. $n$ unlabeled balls, $m$ unlabeled urns, at least one ball per urn

This counts partitions of $n$ into exactly $m$ parts:

$$p(n,m),$$

the number of integer partitions of $n$ with exactly $m$ positive summands. It is $0$ unless $n\ge m$. When $n=0$, it equals $1$ if $m=0$ and $0$ otherwise.

### Final consistency

Each formula respects the boundary conditions $n=0$ and $m=0$ by either producing a single empty configuration or forbidding any configuration, matching the combinatorial interpretations in all twelve cases.

This completes the solution. ∎
