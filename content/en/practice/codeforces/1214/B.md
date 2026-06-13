---
title: "CF 1214B - Badges"
description: "We are given three integers describing a small combinatorial setup. There are a fixed number of boys and girls in total, and exactly $n$ participants will attend an event, but we do not know how many of them are boys or girls."
date: "2026-06-13T17:26:19+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 1214
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 583 (Div. 1 + Div. 2, based on Olympiad of Metropolises)"
rating: 1100
weight: 1214
solve_time_s: 304
verified: true
draft: false
---

[CF 1214B - Badges](https://codeforces.com/problemset/problem/1214/B)

**Rating:** 1100  
**Tags:** brute force, math  
**Solve time:** 5m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three integers describing a small combinatorial setup. There are a fixed number of boys and girls in total, and exactly $n$ participants will attend an event, but we do not know how many of them are boys or girls. The actual number of boys in the event can range from 0 to $n$, as long as it does not exceed the available population of boys, and similarly the number of girls is determined by the remainder.

For every possible split of the $n$ participants into boys and girls, we need to be able to assign badges correctly. Each possible split requires a specific type of badge deck: if there are $i$ boys, we need a deck containing exactly $i$ blue badges and $n-i$ red badges.

We are given all $n+1$ possible decks, but we are not required to take all of them. The task is to select the smallest subset of these decks such that for every feasible value of $i$ that can actually occur given the constraints on total boys and girls, at least one selected deck matches it.

The input sizes are small, bounded by 300. This removes any pressure for advanced data structures or optimizations; a direct arithmetic or greedy reasoning is sufficient. A quadratic or even linear scan is entirely acceptable.

A subtle edge case appears when some values of $i$ are impossible due to lack of boys or girls. For example, if there are only 2 boys, then any deck requiring 3 or more blue badges is irrelevant even if it exists. A naive approach that always assumes all $0 \ldots n$ values are possible would overcount required decks.

## Approaches

The brute-force viewpoint is to consider every possible number of boys $i$ in the tournament, from 0 to $n$, and check whether that configuration is feasible. A configuration is feasible only if $i \le b$ and $n-i \le g$. For each feasible $i$, we must include the corresponding deck.

This immediately suggests a simple scan: mark all valid $i$, then count them. This already solves the problem correctly because each valid $i$ corresponds to a distinct required deck, and no deck can serve two different values of $i$ since each deck encodes a fixed number of blue badges.

The “optimization” over brute force is mostly conceptual. We do not need to reason about subsets or overlaps because the structure is linear: each $i$ maps to exactly one deck. The only real task is determining the range of valid $i$.

From the inequalities:

$i \le b$ and $n-i \le g \Rightarrow i \ge n-g$.

So valid $i$ lie in the intersection:

$$\max(0, n-g) \le i \le \min(n, b)$$

The answer is simply the size of this interval, if it is non-empty.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O(n) | O(1) | Accepted |
| Interval Computation | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the smallest possible number of boys in the tournament as $L = \max(0, n - g)$. This ensures we do not exceed the available number of girls when forming the remaining participants.
2. Compute the largest possible number of boys as $R = \min(n, b)$, since we cannot exceed total participants or available boys.
3. If $L > R$, no valid configuration exists, meaning no deck is actually required to satisfy a feasible scenario, so the answer is 0.
4. Otherwise, all integer values $i$ in the range $[L, R]$ correspond to feasible scenarios, and each requires a distinct deck.
5. The number of required decks is therefore $R - L + 1$.

### Why it works

Each feasible tournament configuration is uniquely identified by the number of boys $i$. The constraints restrict $i$ to a contiguous interval. Every integer in this interval corresponds to a distinct required badge composition, and each composition is represented by exactly one deck. Because there is no overlap between deck definitions, covering all feasible cases reduces exactly to covering every integer in this interval. No additional selection strategy can reduce the count without missing a valid $i$.

## Python Solution

```
PythonRun
```

The solution directly computes the feasible interval boundaries. The first boundary ensures we have enough girls to fill the remaining $n - i$ slots. The second boundary ensures we do not exceed available boys or total participants.

The key implementation detail is carefully handling the intersection bounds. The `max(0, n - g)` prevents negative lower bounds when there are many girls, and `min(n, b)` caps the upper bound correctly even when the number of boys exceeds $n$. The final check `L > R` is necessary to avoid negative counts when the feasible interval is empty.

## Worked Examples

### Example 1

Input:

```

```

Compute bounds:

| Step | L = max(0, n-g) | R = min(n, b) | Valid interval |
| --- | --- | --- | --- |
| Init | max(0, 3-6)=0 | min(3,5)=3 | [0, 3] |

Answer = 4

This demonstrates a case where all distributions from 0 to 3 boys are possible because both resources are sufficient. Every deck is needed.

### Example 2

Input:

```

```

| Step | L | R | Valid interval |
| --- | --- | --- | --- |
| Init | max(0,3-6)=0 | min(3,3)=3 | [0,3] |

Answer = 4

Now consider a tighter case:

Input:

```

```

| Step | L | R | Valid interval |
| --- | --- | --- | --- |
| Init | max(0,3-2)=1 | min(3,5)=3 | [1,3] |

Answer = 3

This shows that when girls are limited, low values of $i$ become impossible because they would require too many girls.

The trace confirms the key invariant: only feasible splits of participants contribute to the count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed |
| Space | O(1) | No additional storage beyond a few integers |

The constraints allow even naive iteration, but the interval formulation reduces the solution to constant time, which is optimal.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 2 | smallest non-trivial interval |
| 0 5 3 | 0 | impossible configuration |
| 5 2 3 | 3 | tight girl constraint |

## Edge Cases

When girls are abundant and boys are the limiting factor, the lower bound $L = \max(0, n-g)$ becomes 0 and the interval expands upward until $b$. The algorithm correctly includes all feasible $i$ from 0 to $b$.

When boys are abundant but girls are scarce, the upper bound is $R = n$ but the lower bound shifts upward to $n-g$, eliminating impossible small values of $i$. The computed interval still remains contiguous and correctly sized.

When both $b$ and $g$ are too small to form any valid split, the condition $L > R$ triggers, producing 0, which matches the fact that no participant distribution is feasible.
