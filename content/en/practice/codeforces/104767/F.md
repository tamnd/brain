---
title: "CF 104767F - Golem Coordinated Derby"
description: "We are given a multiset of up to $10^5$ robots, each labeled by an integer height between 1 and 20. From these robots, we must choose one as a captain and arrange all robots in a line behind the captain in any order we like."
date: "2026-06-28T20:06:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104767
codeforces_index: "F"
codeforces_contest_name: "2023-2024 CTU Open Contest"
rating: 0
weight: 104767
solve_time_s: 28
verified: false
draft: false
---

[CF 104767F - Golem Coordinated Derby](https://codeforces.com/problemset/problem/104767/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a multiset of up to $10^5$ robots, each labeled by an integer height between 1 and 20. From these robots, we must choose one as a captain and arrange all robots in a line behind the captain in any order we like. The captain receives a score equal to the sum of values contributed by each adjacent pair in the line: for every robot in the line, it looks at the robot immediately in front of it and adds the gcd of their heights.

So the problem reduces to this: pick a root element (the captain), arrange all other elements in a sequence starting from it, and maximize the sum of gcd values along directed edges of this path.

The structure is not arbitrary graph traversal. Every arrangement defines a Hamiltonian path over all nodes, rooted at the chosen captain, and the score is the sum of edge weights where weight between two robots depends only on their heights.

The constraint that heights are at most 20 is the key structural restriction. It implies that instead of working with individual robots, we can aggregate them by value. There are only 20 distinct types, but up to $10^5$ occurrences.

From a complexity standpoint, $N = 10^5$ rules out any solution that attempts to permute or DP over subsets of robots. Any $O(N^2)$ or $O(N \cdot 2^N)$ idea is impossible. Even $O(N \log N)$ solutions must avoid dependence on ordering individuals. The solution must compress the problem into a small state space over values 1 through 20.

A subtle edge case is that ordering matters even though gcd is symmetric. For example, if all values are equal, say $[6,6,6]$, every arrangement gives the same contribution $6$ per adjacent edge, but if mixed values exist, the placement of high gcd pairs matters heavily. A naive greedy that always pairs equal or large gcd neighbors locally fails because global structure determines how often each value is used as a predecessor.

Another edge case is when a value appears only once. For instance, if we have a single 1 among many large values, placing it in the middle can reduce contributions significantly because gcd with neighbors is always 1. Any correct solution must handle singleton frequencies naturally rather than assuming pairs.

## Approaches

A brute-force interpretation would be: try every possible choice of captain and every permutation of the remaining robots, compute the sum of gcds along the resulting path, and take the maximum. This is correct because it enumerates all valid configurations. However, the number of permutations alone is $(N-1)!$, which for $N = 10^5$ is astronomically large, making this approach infeasible.

A more structured brute-force would treat each robot individually and attempt dynamic programming over subsets of visited nodes, similar to Hamiltonian path DP. That leads to a state size of $O(N \cdot 2^N)$, again impossible.

The key observation is that the only thing distinguishing robots is their height, and heights lie in a tiny range $[1, 20]$. This allows us to compress the problem into counts of each value. Instead of arranging $N$ labeled objects, we are arranging a multiset of at most 20 types.

Now reinterpret the process. Once the captain is fixed as some value $c$, the contribution depends only on transitions between values. If we know how many times each value appears, we are effectively constructing a sequence that uses each value exactly its frequency, maximizing the sum of edge weights $g(a, b) = \gcd(a, b)$.

This becomes a classic "maximum weighted path over multiset types" problem. We can use dynamic programming over subsets of values and track the last used value. Since there are only 20 values, we define DP states over subsets of these 20 types, but that is still $2^{20}$ states, which is borderline but workable with careful optimization.

However, a sharper observation reduces this further. We do not need to track individual occurrences; we only need counts. We can interpret the process as repeatedly picking the next value type and adding contribution equal to gcd with previous chosen value, multiplied by how many instances are consumed.

We therefore define DP over bitmasks of values 1 to 20, and last chosen value, but we also incorporate multiplicity implicitly by treating each value as repeated identical items and using count-based transitions. Since 20 is small, we can precompute counts and run a DP with complexity roughly $O(2^{20} \cdot 20)$, optimized further by only considering active values.

An equivalent and more practical view is: for each possible ordering of the 20 value types, compute the best contribution assuming we group identical values consecutively. The optimal arrangement will never interleave identical values in a non-beneficial way because all instances of a value are indistinguishable and gcd is symmetric over duplicates.

Thus the solution reduces to ordering the 20 value types, weighted by frequencies, maximizing adjacent gcd contributions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force permutations | $O(N!)$ | $O(N)$ | Too slow |
| Subset DP over value types | $O(2^{20} \cdot 20)$ | $O(2^{20})$ | Accepted |

## Algorithm Walkthrough

We compress
