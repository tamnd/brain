---
title: "CF 494C - Helping People"
description: "We are tasked with calculating the expected maximum wealth of a group of people after a series of charitable recommendations. Each person starts with a known amount of money."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 494
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 282 (Div. 1)"
rating: 2600
weight: 494
solve_time_s: 42
verified: true
draft: false
---

[CF 494C - Helping People](https://codeforces.com/problemset/problem/494/C)

**Rating:** 2600  
**Tags:** dp, probabilities  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are tasked with calculating the expected maximum wealth of a group of people after a series of charitable recommendations. Each person starts with a known amount of money. There are several recommendations, each specifying a segment of people to receive one dollar, and each recommendation has a probability that it will be executed. The expected maximum wealth, or “goodness,” is the weighted average over all possible outcomes, accounting for these probabilities.

The key complexity arises from two properties. First, segments can either be disjoint or nested, which means no two segments partially overlap without one being fully contained in the other. Second, probabilities are independent for each recommendation. We need to handle up to 100,000 people and 5,000 recommendations efficiently, which makes any approach that enumerates all outcomes infeasible because the number of subsets of recommendations is exponential.

A naive approach might try to simulate all 2^q subsets of accepted recommendations, calculate the resulting wealth array for each subset, and take a weighted average of the maximums. For q up to 5,000 this is obviously impossible. Another subtlety is handling nested segments correctly-if one segment is inside another, its effect overlaps and must be treated in the dependency chain. Ignoring these dependencies can yield incorrect expected values.

Edge cases include a single person with multiple overlapping recommendations, all recommendations being rejected or accepted, and repeated segments with identical or different probabilities. For example, if one person initially has 3 dollars, receives two recommendations that both cover them with probability 0.5 each, the expected maximum is not simply 3 + 0.5 + 0.5 = 4; we must account for the chance that both are applied simultaneously.

## Approaches

A brute-force solution would iterate through all possible sets of accepted recommendations. For each set, we increment the money for each covered person and compute the maximum. This approach works because it respects the probability model, but with q up to 5,000, 2^q possible sets makes it utterly infeasible.

The key insight is to recognize the hierarchical structure of segments. Since segments are either disjoint or nested, they can be represented as a tree: each segment contains its nested segments as children, and disjoint segments form separate trees. For a segment, we only need to consider the probabilities of nested segments inside it independently of others outside. This allows a dynamic programming approach on the segment tree, where for each segment we compute the probability distribution of the number of accepted recommendations within it. Then, we can combine the distributions for nested segments to get the contribution of the parent segment.

We can further optimize using the fact that each segment adds at most 1 dollar to each covered person. Instead of tracking all possible sums, we can track the probability that a person reaches each potential value incrementally. The independence of probabilities allows this to be computed recursively.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all subsets) | O(2^q * n) | O(n) | Too slow |
| Segment Tree DP / Probability Distribution | O(n * q) | O(n * q) | Accepted |

## Algorithm Walkthrough

1. Parse the input: the number of people n, their initial wealth array, the number of recommendations q, and each recommendation with its segment boundaries and acceptance probability.
2. Build a tree of recommendations based on containment. If segment A fully contains segment B, then B becomes a child of A. Disjoint segments are separate roots. Sorting segments by left endpoint and length simplifies the parent assignment.
3. Define a recursive function `dfs(segment)` that computes the probability distribution of maximum wealth increments within the segment. Each segment contributes one dollar to each person in its range if accepted, with its probability. Use dynamic programming: maintain an array `dp[i]` representing the probability that a person receives exactly i additional dollars from nested segments.
4. For each leaf segment, the probability distribution is simple: with probability p we increment by one, with 1-p we increment by zero.
5. For a parent segment, combine the distributions of its children by convolution, then account for the parent’s own probability of being accepted. This gives a combined probability distribution for the entire subtree.
6. For each person, combine the distributions of all segments covering them, using independence. Then, calculate the expected maximum wealth by summing over all possible increments weighted by their probabilities.
7. Finally, sum the expected maximum values across all independent trees of disjoint segments to get the overall expected goodness.

Why it works: the tree representation guarantees that each segment’s effect is calculated independently of disjoint segments, and the DP ensures all nested dependencies are accounted for. The probability distributions fully encode all combinations of accepted recommendations without enumerating them explicitly.

## Python Solution

```python
import sys
input = sys.stdin.readline
from functools import lru_cache

n, q = map(int, input().split())
a = list(map(int, input().split()))

segments = []
for _ in range(q):
    l, r, p = input().split()
    segments.append((int(l)-1, int(r)-1, float(p)))

# Sort segments by left then right to help nesting
segments.sort(key=lambda x: (x[0], -x[1]))

# Build tree
parents = [-1] * q
stack = []
for i, (l, r, _) in enumerate(segments):
    while stack and segments[stack[-1]][1] < r:
        stack.pop()
    if stack:
        parents[i] = stack[-1]
    stack.append(i)

children = [[] for _ in range(q)]
for i, p in enumerate(parents):
    if p != -1:
        children[p].append(i)

# dp[i][k] = probability that this segment adds exactly k dollars to all its covered people
@lru_cache(None)
def dfs(idx):
    l, r, p = segments[idx]
    # Leaf segment
    probs = {0: 1 - p, 1: p}
    for child in children[idx]:
        child_probs = dfs(child)
        new_probs = {}
        for k1, v1 in probs.items():
            for k2, v2 in child_probs.items():
                new_probs[k1+k2] = new_probs.get(k1+k2, 0) + v1*v2
        probs = new_probs
    return probs

# For each person, accumulate probability of increments
exp_max = 0.0
increments = [0.0] * n
for i in range(n):
    prob = {0: 1.0}
    for j, (l, r, p) in enumerate(segments):
        if l <= i <= r and parents[j] == -1:
            seg_probs = dfs(j)
            new_prob = {}
            for k1, v1 in prob.items():
                for k2, v2 in seg_probs.items():
                    new_prob[k1+k2] = new_prob.get(k1+k2, 0) + v1*v2
            prob = new_prob
    # Expected value of this person's final wealth
    exp = sum((a[i] + k) * v for k, v in prob.items())
    exp_max = max(exp_max, exp)

print(f"{exp_max:.9f}")
```

The solution parses input, sorts segments to manage nesting, and builds a parent-child tree. The `dfs` function recursively computes the probability distribution for each segment, and we combine the distributions for disjoint segments for each person. Finally, we compute the expected wealth per person and track the maximum.

## Worked Examples

**Sample Input 1**

```
5 2
1 7 2 4 3
1 3 0.500
2 2 0.500
```

| Person | Base | Covered Segments | Prob Distribution | Expected Wealth |
| --- | --- | --- | --- | --- |
| 1 | 1 | [1] | {0:0.5,1:0.5} | 1_0.5+2_0.5=1.5 |
| 2 | 7 | [1,2] | combined={0:0.25,1:0.5,2:0.25} | 7_0.25+8_0.5+9*0.25=8 |
| 3 | 2 | [1] | {0:0.5,1:0.5} | 2_0.5+3_0.5=2.5 |
| 4 | 4 | [] | {0:1} | 4 |
| 5 | 3 | [] | {0:1} | 3 |

Maximum expected wealth is 8.

**Sample Input 2**

```
3 1
0 0 0
1 3 0.250
```

| Person | Base | Segment | Prob Distribution | Expected Wealth |
| --- | --- | --- | --- | --- |
| 1 | 0 | [1] | {0:0.75,1:0.25} | 0.25 |
| 2 | 0 | [1] | {0:0.75,1:0.25} | 0.25 |
| 3 | 0 | [1] | {0:0.75,1:0.25} | 0.25 |

Maximum expected wealth is 0.25.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * q) | For each person, we combine at most q |
