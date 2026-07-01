---
title: "CF 104426H - Abo Abdo Smoothies"
description: "We are given two sequences of length $n$. The first sequence represents the smoothies Naseem actually bought, and the second sequence represents what each friend would ideally like to receive."
date: "2026-06-30T19:06:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104426
codeforces_index: "H"
codeforces_contest_name: "Syrian Private Universities Collegiate Programming Contest 2023"
rating: 0
weight: 104426
solve_time_s: 82
verified: false
draft: false
---

[CF 104426H - Abo Abdo Smoothies](https://codeforces.com/problemset/problem/104426/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two sequences of length $n$. The first sequence represents the smoothies Naseem actually bought, and the second sequence represents what each friend would ideally like to receive. There is no restriction on which friend receives which smoothie, so we are free to permute the assignment of the purchased smoothies among friends. The goal is to maximize how many friends end up receiving a smoothie type that matches their preference exactly.

Another way to see this is that we have two multisets of size $n$: one coming from purchases and one coming from preferences. We want to match elements from the first multiset to the second one, maximizing the number of equal pairs.

The constraints $n, m \le 10^5$ imply that any solution worse than linear or linearithmic time will not work. A quadratic comparison approach between all pairs would involve up to $10^{10}$ operations in the worst case, which is far beyond the limit. This pushes us toward frequency-based reasoning rather than pairwise matching.

A subtle pitfall appears when duplicates exist heavily on one side but not the other. For example, if all purchased smoothies are type 1 but friends want many different types, a naive greedy assignment that tries to match in order without grouping by type can easily undercount or overcount matches depending on traversal order. Another issue is assuming index alignment matters, when in fact we are allowed to permute arbitrarily.

## Approaches

The brute-force interpretation is to try assigning smoothies to friends in every possible way and count how many matches we can get. This corresponds to generating all permutations of assignments between the two arrays. For each permutation, we compute how many positions match. This is correct because it explores the entire solution space, but it grows factorially, roughly $n!$, which is completely infeasible even for $n = 20$.

A more structured brute-force improvement is to fix an order of friends and, for each friend, try assigning any unused smoothie, recursively maximizing matches. This is still exponential because each step branches into up to $n$ choices.

The key observation is that identity of elements matters only through frequency. For a given smoothie type $x$, suppose it appears $c_a[x]$ times in the purchased list and $c_b[x]$ times in preferences. No matter how we permute, we can match at most $\min(c_a[x], c_b[x])$ friends of type $x$, because each match consumes one smoothie and one preference of that type. Conversely, this bound is achievable by simply pairing greedily within each type.

This reduces the problem from a global assignment problem to independent counting per value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n!)$ | $O(n)$ | Too slow |
| Frequency Matching | $O(n)$ | $O(m)$ | Accepted |

## Algorithm Walkthrough

We solve the problem by counting how many times each smoothie type appears in both arrays and summing the minimum overlaps.

1. Build a frequency map for the purchased smoothies array $a$. This captures how many available items we have of each type.
2. Build a frequency map for the preferences array $b$. This captures how many friends want each type.
3. For every type that appears in either map, compute the number of matches as the minimum of its two frequencies.
4. Accumulate these minima into the final answer and output the result.

Each step is driven by the idea that matches are independent across types. Once a smoothie is assigned, it cannot be reused, so counting per type exactly models resource consumption.

### Why it works

For each value $x$, any valid assignment can only pair at most one smoothie of type $x$ with one friend who wants type $x$. Therefore, the number of valid pairs for that type is upper bounded by both the supply $c_a[x]$ and demand $c_b[x]$. Taking the minimum satisfies both constraints simultaneously. Summing over all types is valid because different types never compete for the same item.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    freq_a = {}
    freq_b = {}

    for x in a:
        freq_a[x] = freq_a.get(x, 0) + 1

    for x in b:
        freq_b[x] = freq_b.get(x, 0) + 1

    ans = 0
    for x in freq_a:
        if x in freq_b:
            ans += min(freq_a[x], freq_b[x])

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution separates counting into two dictionaries. One subtle implementation choice is iterating only over keys of `freq_a` and checking existence in `freq_b`, which avoids iterating over the entire range of possible smoothie types up to $m$, which may include unused values.

Another important detail is using `get` for frequency updates to avoid key errors and keep the code clean and linear.

## Worked Examples

### Example 1

Input:

```
3 2
1 1 2
2 2 1
```

We track frequencies:

| Type | freq_a | freq_b | min |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 1 |
| 2 | 1 | 2 | 1 |

Answer = 2

This demonstrates that even when distributions are skewed, matching is purely frequency-limited, not order-dependent.

### Example 2

Input:

```
5 3
1 1 1 2 3
1 2 2 2 2
```

| Type | freq_a | freq_b | min |
| --- | --- | --- | --- |
| 1 | 3 | 1 | 1 |
| 2 | 1 | 4 | 1 |
| 3 | 1 | 0 | 0 |

Answer = 2

This shows that excess demand or supply in one category does not affect others, reinforcing independence across types.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each array is scanned once, and dictionary iteration is linear in distinct values |
| Space | $O(m)$ | Frequency maps store counts per distinct smoothie type |

The solution fits comfortably within constraints since $n \le 10^5$, and dictionary operations are expected $O(1)$ average.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    freq_a = {}
    freq_b = {}

    for x in a:
        freq_a[x] = freq_a.get(x, 0) + 1
    for x in b:
        freq_b[x] = freq_b.get(x, 0) + 1

    ans = 0
    for x in freq_a:
        if x in freq_b:
            ans += min(freq_a[x], freq_b[x])

    return str(ans).strip()

# provided sample
assert run("3 2\n1 1 2\n2 2 1\n") == "2"

# all equal
assert run("4 1\n1 1 1 1\n1 1 1 1\n") == "4"

# no overlap
assert run("3 3\n1 1 1\n2 2 2\n") == "0"

# partial overlap
assert run("5 5\n1 2 2 3 3\n2 2 3 4 4\n") == "3"

# single element
assert run("1 10\n5\n5\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 4 | full matching saturation |
| no overlap | 0 | disjoint sets |
| partial overlap | 3 | mixed frequency balancing |
| single element | 1 | minimal boundary case |

## Edge Cases

A key edge case is when one type appears only on one side. For example:

Input:

```
3 3
1 1 1
2 2 2
```

The algorithm builds `freq_a = {1: 3}` and `freq_b = {2: 3}`. Since there is no intersection of keys, the loop contributes nothing and the answer is 0, which matches reality because no friend’s preference can be satisfied.

Another edge case is heavy imbalance:

Input:

```
5 5
1 1 1 1 1
1 1 2 2 2
```

Frequencies give:

type 1 contributes min(5, 2) = 2, type 2 contributes min(0, 3) = 0 implicitly, so answer is 2. The algorithm correctly avoids over-assigning extra type 1 smoothies to type 2 preferences, since it never mixes types across keys.

These cases confirm that the frequency-based decomposition preserves correctness even under extreme skew.
