---
title: "CF 104618G - Ice Cream Gambling"
description: "We are given two independent collections that interact through a trading process. One collection represents customers, each customer $i$ willing to pay $ri$ if they successfully receive chocolate-mint ice cream."
date: "2026-06-29T17:30:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104618
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 09-22-23 Div. 1"
rating: 0
weight: 104618
solve_time_s: 33
verified: false
draft: false
---

[CF 104618G - Ice Cream Gambling](https://codeforces.com/problemset/problem/104618/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two independent collections that interact through a trading process. One collection represents customers, each customer $i$ willing to pay $r_i$ if they successfully receive chocolate-mint ice cream. The other collection represents cones Greg found, where each cone $j$ has a purchase cost $c_j$. We must decide which cones to buy and which customers to serve with them.

The twist is that cones are “unknown”: a cone might or might not be chocolate-mint. If we assign a cone to a customer, we always serve it, but profit depends on whether that cone turns out to be valid. Alex’s gambling introduces the ability to bet on whether a cone is chocolate-mint, which effectively allows us to neutralize uncertainty optimally, but not for free. The end result is that each assignment contributes a deterministic guaranteed value derived from the pairing of customer value and cone cost.

The task is to maximize guaranteed profit, and among all ways achieving that maximum profit, maximize the number of customers served. We also must count how many assignment configurations achieve both objectives.

The constraints $N, M \le 10^5$ immediately rule out any quadratic matching or flow-based solution over the full bipartite graph. Any approach that considers all customer-cone pairs explicitly would require $10^{10}$ operations, which is infeasible. This pushes us toward sorting, greedy pairing, and combinatorial counting.

A subtle edge case appears when all costs are high relative to values. A naive greedy might decide to avoid matching entirely, but the problem guarantees that doing nothing yields a valid zero-profit baseline. Another edge case is when multiple cones or customers share identical values or costs, which affects counting of optimal assignments because permutations among equal elements still produce distinct ways.

## Approaches

If we try brute force, we would assign each customer either no cone or one of the available cones, and each cone at most once. For each assignment set, we would compute the guaranteed profit, then track the best result. The number of subsets of pairings is combinatorial in both $N$ and $M$, growing faster than $2^{100000}$, so this is completely impossible.

The key structural observation is that only relative ordering matters. Each customer contributes independently based on whether we assign them a cone and which cone we choose. Since cones are interchangeable except for their costs, and customers are interchangeable except for their rewards, optimal structure emerges after sorting both arrays.

The critical idea is that we are effectively pairing high-value customers with low-cost cones. Any deviation that pairs a high-value customer with a more expensive cone while leaving a better pairing unused can only reduce guaranteed profit. This transforms the problem into a matching between sorted sequences where optimal solutions respect order: largest $r_i$ should be matched with smallest $c_j$ in a controlled prefix.

Once we sort both arrays, we can consider taking exactly $k$ customers and $k$ cones. For a fixed $k$, the best guaranteed structure is pairing the $k$ largest $r_i$ with the $k$ smallest $c_j$. This reduces the problem to evaluating a function over $k$, maximizing profit, and among ties maximizing $k$, then counting permutations that realize the same optimal structure.

Counting arises because within equal-valued blocks, multiple assignments yield identical profit. We must multiply choices of identical cones and identical customers using combinatorial coefficients.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(N + M) | Too slow |
| Optimal Sorting + Greedy Pairing + Combinatorics | $O(N \log N + M \log M)$ | O(N + M) | Accepted |

## Algorithm Walkthrough

### 1. Sort both arrays

Sort customer values $r$ in descending order and cone costs $c$ in ascending order. This aligns the best customers with the cheapest available cones in any optimal matching.

### 2. Precompute prefix sums

Build prefix sums for both arrays so we can quickly evaluate total profit contributions for any prefix length $k$.

### 3. Evaluate all possible match sizes

For each $k$ from $0$ to $\min(N, M)$, compute the candidate profit of matching the top $k$ customers with the cheapest $k$ cones. The structure ensures that any optimal solution of size $k$ must look like this, because swapping any pair of mismatched order would increase cost or decrease reward.

The profit for a fixed $k$ is computed from prefix sums as:

$$\text{profit}(k) = \sum_{i=1}^{k} r_i^{(desc)} - \sum_{j=1}^{k} c_j^{(asc)}$$

### 4. Track best profit and best size

Maintain the maximum profit seen so far. If a larger profit is found, reset the best size. If the same profit is found, prefer larger $k$.

### 5. Count optimal assignments

For the chosen optimal $k$, we count how many ways we can select which $k$ customers and $k$ cones form the optimal pairing structure.

This depends on multiplicities. Suppose among the top $k$ customers there are repeated values; any permutation of identical values does not change the outcome. Similarly for cones.

Thus the number of valid matchings is:

$$\frac{k!}{\prod \text{freq of equal } r} \times \frac{k!}{\prod \text{freq of equal } c}$$

modulo $10^9+7$, adjusted carefully for identical-value symmetries.

### Why it works

The core invariant is that in any optimal solution, the matched pairs must respect sorted order. If there exists a pair where a larger reward is matched to a more expensive cone than another unused pair, swapping them strictly improves or preserves profit. Repeating this exchange argument eliminates all inversions, forcing the optimal struc
