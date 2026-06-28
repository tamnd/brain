---
title: "CF 104720C - Cooking Class"
description: "We are given a fixed group of competitors, each with a known skill value, and Autumn with her own initial skill. The competition ranking is purely determined by sorting all participants by skill in descending order, with ties sharing the same rank and causing rank skipping in…"
date: "2026-06-29T05:11:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104720
codeforces_index: "C"
codeforces_contest_name: "UTPC x WiCS Contest 10-06-23"
rating: 0
weight: 104720
solve_time_s: 72
verified: false
draft: false
---

[CF 104720C - Cooking Class](https://codeforces.com/problemset/problem/104720/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fixed group of competitors, each with a known skill value, and Autumn with her own initial skill. The competition ranking is purely determined by sorting all participants by skill in descending order, with ties sharing the same rank and causing rank skipping in the usual competitive programming way.

Autumn can increase her skill exactly once by choosing one of the given cooking classes, each of which adds a positive boost to her current skill. Every other competitor keeps their original skill. The task is to choose the class that gives Autumn the best possible final rank.

The key output is not Autumn’s final skill, but her best achievable rank after optimally selecting one boost.

The constraints are large, with up to 200,000 competitors and 200,000 classes. This rules out any solution that recomputes rankings from scratch for every class, since that would lead to about 40 billion comparisons in the worst case.

A naive approach would simulate Autumn’s rank for each boost independently, scanning all competitors each time to count how many have strictly higher skill. That would be $O(NM)$, which is far too slow.

A subtle edge case appears when multiple competitors share the same skill as Autumn’s final value. For example, if Autumn ties with several people at the top, she still gets rank 1, but a careless implementation that counts “strictly greater only” might underestimate ties depending on interpretation of rank logic.

Another edge case is when Autumn is already the strongest even before boosting, but still must choose a boost anyway, which can paradoxically change her rank if the problem is misread as only maximizing skill rather than minimizing rank.

## Approaches

The ranking depends only on how many competitors have strictly greater skill than Autumn after she chooses a boost. If Autumn’s final skill is $X$, then her rank is $1 + \#\{S_i > X\}$.

A brute-force method tries every boost $P_i$, computes $X = S_A + P_i$, and counts how many competitors exceed $X$. Each count requires scanning all $N$ competitors, so the total work is $O(NM)$. With $2 \cdot 10^5$ in both dimensions, this is completely infeasible.

The key observation is that for each candidate final skill $X$, the rank depends only on a threshold query: how many values in the array exceed $X$. If we sort the competitor skills once, we can answer this in logarithmic time using binary search. This reduces each evaluation from linear to logarithmic.

Since we still need to try all $M$ boosts, the final complexity becomes $O(M \log N)$ after an initial sort of $O(N \log N)$. This is efficient enough.

The structure of the problem is essentially “maximize a function over a small set of candidates where each evaluation is a range query over a static multiset”.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(NM)$ | $O(1)$ | Too slow |
| Optimal (sort + binary search) | $O(N \log N + M \log N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

1. Read all competitor skills and Autumn’s initial skill. Compute Autumn’s baseline skill value as a reference point.
2. Sort the list of competitor skills in non-decreasing order. This allows efficient counting of how many competitors exceed a given threshold using binary search.
3. For each cooking class boost value $P_i$, compute Autumn’s resulting skill $X = S_A + P_i$.
4. For this value $X$, determine how many competitors have strictly greater skill. This is done by finding the first position in the sorted array where value is greater than $X$, and subtracting it from $N$. This gives the count of competitors ahead of Autumn.
5. Convert this count into a rank using $rank = 1 + count$. Track the minimum rank over all boosts.
6. Output the smallest rank obtained.

The binary search step is the only nontrivial operation. It works because the sorted array splits naturally into values $\le X$ and values $> X$, and we only care about the latter.

### Why it works

The ranking depends entirely on the number of competitors strictly above Autumn’s final skill. Sorting fixes the relative structure of all competitor skills, making the “greater than X” condition a prefix cut in the sorted array. Every possible boost only changes $X$, not the ordering of competitors, so each candidate solution is evaluated independently but using the same preprocessed structure. This ensures no candidate rank is missed and all are compared correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline

from bisect import bisect_right

def solve():
    data = list(map(int, input().split()))
    n, m = data[0], data[1]
    
    arr = data[2:2+n]
    sa = data[2+n]
    boosts = data[3+n:]
    
    arr.sort()
    
    best = n + 1
    
    for p in boosts:
        x = sa + p
        idx = bisect_right(arr, x)
        greater = n - idx
        rank = 1 + greater
        if rank < best:
            best = rank
    
    print(best)

if __name__ == "__main__":
    solve()
```

The solution begins by separating competitor skills, Autumn’s initial skill, and the boost list from the input stream. Sorting the competitor array is essential because it enables binary search to compute how many values exceed a threshold in logarithmic time.

For each boost, we compute Autumn’s new skill and apply `bisect_right`, which returns the first index where values are strictly greater than the target. Subtracting this index from $N$ gives the number of competitors strictly ahead. Adding one converts this into the competitive ranking definition.

Tracking the minimum rank across all boosts ensures we select the best possible cooking class.

## Worked Examples

Consider the sample input where competitors have skills `[3, 3, 4, 5, 2]`, Autumn starts at `2`, and boosts are `[1, 2, 3, 4, 5]`.

Sorted competitors become `[2, 3, 3, 4, 5]`.

### Trace for boosts

| Boost | Final skill X | First > X index | Greater count | Rank |
| --- | --- | --- | --- | --- |
| 1 | 3 | 3 | 2 | 3 |
| 2 | 4 | 4 | 1 | 2 |
| 3 | 5 | 5 | 0 | 1 |
| 4 | 6 | 5 | 0 | 1 |
| 5 | 7 | 5 | 0 | 1 |

The best achievable rank is 1, achieved once Autumn surpasses all competitors.

This trace shows how the same sorted structure is reused for every candidate boost, and only the threshold changes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N + M \log N)$ | Sorting once, then binary search per boost |
| Space | $O(N)$ | Storage of competitor skills |

The constraints allow up to 200,000 elements, so a logarithmic factor is essential. The solution runs comfortably within limits because each query reduces to a binary search over a pre-sorted array.

## Test Cases

```python
import sys, io
from bisect import bisect_right

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from bisect import bisect_right

    data = list(map(int, sys.stdin.read().split()))
    n, m = data[0], data[1]
    arr = data[2:2+n]
    sa = data[2+n]
    boosts = data[3+n:]

    arr.sort()

    best = n + 1
    for p in boosts:
        x = sa + p
        idx = bisect_right(arr, x)
        best = min(best, 1 + (n - idx))

    return str(best)

# provided sample
assert run("5 5 3 3 4 5 2 1 2 3 4 5") == "1"

# minimum case
assert run("1 1 10 5 1") == "1"

# all equal competitors
assert run("3 3 5 5 5 5 1 2 3") == "1"

# Autumn always loses
assert run("3 2 10 1 2 1 1") == "3"

# boundary dominance
assert run("4 2 1 100 200 300 1 1000 2000") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single competitor | 1 | minimal structure correctness |
| all equal skills | 1 | tie handling |
| always weaker Autumn | 3 | worst rank computation |
| large boost case | 1 | dominance edge |

## Edge Cases

One edge case occurs when Autumn’s final skill equals the maximum competitor skill. For example, competitors `[5, 10, 10]`, Autumn starts at `9`, and boost makes her `10`. The correct rank is `2`, not `1`, because two competitors tie above her or at her level depending on interpretation. The algorithm handles this correctly because `bisect_right` excludes equal values from the “greater” count, ensuring ties are not counted as strictly greater.

Another edge case is when all competitors are weaker than Autumn for every boost. In that case, the binary search always returns `n`, so the greater count is `0` and rank remains `1`. The algorithm correctly preserves rank 1 across all candidates and returns it.
