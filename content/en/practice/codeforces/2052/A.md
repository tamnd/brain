---
title: "CF 2052A - Adrenaline Rush"
description: "The race starts with cars ordered by their labels: $$1,2,3,dots,n.$$ During the race, an overtake is an adjacent swap. If car $x$ is directly behind car $y$, then the event \"$x$ overtakes $y$\" swaps their positions. At the end of the race we know only the final ordering $c$."
date: "2026-06-08T08:34:04+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 2052
codeforces_index: "A"
codeforces_contest_name: "2024-2025 ICPC, NERC, Northern Eurasia Finals (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 1600
weight: 2052
solve_time_s: 204
verified: false
draft: false
---

[CF 2052A - Adrenaline Rush](https://codeforces.com/problemset/problem/2052/A)

**Rating:** 1600  
**Tags:** constructive algorithms  
**Solve time:** 3m 24s  
**Verified:** no  

## Solution
## Problem Understanding

The race starts with cars ordered by their labels:

$$1,2,3,\dots,n.$$

During the race, an overtake is an adjacent swap. If car $x$ is directly behind car $y$, then the event "$x$ overtakes $y$" swaps their positions.

At the end of the race we know only the final ordering $c$. We must reconstruct a race containing as many overtakes as possible, under one restriction: for every pair of cars $(x,y)$, the event "$x$ overtakes $y$" may happen at most once, and the event "$y$ overtakes $x$" may happen at most once.

We need to output both the maximum possible number of overtakes and one sequence of overtakes achieving it.

The constraint $n \le 1000$ is small. The number of pairs of cars is at most

$$\frac{1000\cdot999}{2}=499500.$$

Since the answer itself can contain $O(n^2)$ overtakes, any accepted solution will also be at least quadratic in the worst case. An $O(n^2)$ construction is completely safe.

A subtle point is that maximizing the number of overtakes is not the same as minimizing or matching the final permutation. For a pair of cars whose relative order is unchanged in the final ranking, we can let them exchange positions twice during the race and still finish in the original order. A solution that only performs the overtakes strictly necessary to obtain the final permutation misses many valid extra overtakes.

Consider:

```
n = 2
final = [1, 2]
```

The final order is already the initial order. A naive solution would output zero overtakes.

The optimal race is:

```
2 overtakes 1
1 overtakes 2
```

The final order is again $[1,2]$, but now we have two overtakes.

Another easy-to-miss case is:

```
n = 3
final = [3,2,1]
```

Every pair is reversed. No pair can contribute two overtakes, because ending reversed requires a net change of relative order. The maximum is exactly three overtakes, one for each pair.

## Approaches

A brute force view starts from considering every pair of cars independently.

Take a pair $(x,y)$ with $x<y$. Initially, $x$ is ahead of $y$.

If the final ranking also places $x$ ahead of $y$, then the pair can contribute two overtakes:

```
y overtakes x
x overtakes y
```

The relative order ends unchanged.

If the final ranking places $y$ ahead of $x$, then the pair can contribute at most one overtake:

```
y overtakes x
```

Performing both directions would restore the original order, which is not allowed.

This immediately gives an upper bound. Let $P$ be the number of pairs and let $I$ be the inversion count of the final permutation relative to the initial order.

Every non-inversion pair contributes at most two overta
