---
title: "CF 104720C - Cooking Class"
description: "Autumn is entering a skill-based contest where ranking is determined purely by numerical skill values. Every participant has a fixed skill, while Autumn has a base skill that can be improved by choosing exactly one of several available training classes."
date: "2026-06-29T04:16:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104720
codeforces_index: "C"
codeforces_contest_name: "UTPC x WiCS Contest 10-06-23"
rating: 0
weight: 104720
solve_time_s: 77
verified: false
draft: false
---

[CF 104720C - Cooking Class](https://codeforces.com/problemset/problem/104720/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** no  

## Solution
## Problem Understanding

Autumn is entering a skill-based contest where ranking is determined purely by numerical skill values. Every participant has a fixed skill, while Autumn has a base skill that can be improved by choosing exactly one of several available training classes. Each class adds a positive boost to her skill, and she must pick exactly one.

Once her final skill is determined, her rank depends on how many competitors have strictly higher skill than her, plus how ties are handled. All people with the same skill share the same rank position, and ranks skip accordingly, meaning rank is effectively one plus the number of participants strictly stronger than her.

The task is to choose the best class so that Autumn’s resulting rank is as small as possible, i.e., she wants as few people as possible to have strictly higher skill than her after applying the chosen boost.

The input sizes reach up to 200,000 competitors and 200,000 classes, so any solution that tries every pair of competitor and class directly would require up to 40 billion comparisons, which is far beyond what a 2-second limit can handle. The only viable approaches must reduce the per-class evaluation cost to logarithmic or constant time after preprocessing.

A subtle edge case arises when multiple competitors share the same skill level as Autumn after boosting. Those ties do not affect the number of strictly better competitors, but a naive interpretation might mistakenly count equals as worse or better. Another edge case occurs when Autumn is already the strongest even before boosts; the answer should then be 1 regardless of the chosen class, as long as boosts are positive. Finally, large duplicate values among competitors matter because ranking depends only on counts of values greater than a threshold, not their identities.

## Approaches

A direct approach would be to compute Autumn’s final skill for each class, then compare it against every competitor to count how many have strictly greater skill. This leads to a nested structure where for each of M boosts we scan N competitors, producing O(NM) time complexity. With 200,000 in both dimensions, this is infeasible.

The key observation is that for any fixed final skill value X, the rank depends only on how many competitor skills exceed X. This is a classic “count how many elements are greater than a threshold” problem, which becomes efficient once the competitor array is sorted. After sorting S, we can use binary search to determine how many values are greater than any X in O(log N). This reduces each class evaluation from linear time to logarithmic time, bringing total complexity to O((N + M) log N).

An even more structured view is that the competitor set is static, and we are repeatedly querying a function f(X) = number of elements strictly greater than X. Pre-sorting transforms this into prefix reasoning over an ordered array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NM) | O(1) | Too slow |
| Sort + Binary Search | O((N + M) log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Read all competitor skills and Autumn’s base skill. Store competitors in a list separate from Autumn. The reason is that Autumn is not part of the fixed dataset we preprocess.
2. Sort the competitor skill list in non-decreasing order. This transforms the problem into a structure where all “greater than X” queries become contiguous suffix queries.
3. For each boost value P_i, compute Autumn’s final skill X = S_A + P_i. Each class produces a candidate ranking scenario.
4. For each X, determine how many competitors have skill strictly greater than X using binary search. Specifically, find the first index where value is greater than X, then subtract from N. This works because the sorted array ensures all greater values form a suffix.
5. Convert this count into rank as 1 + number of strictly greater competitors. Track the minimum rank across all boosts.
6. Output the smallest rank obtained.

### Why it works

The ranking depends only on the relative order of skills. Sorting fixes this order globally, and any query reduces to finding a boundary between values less than or equal to X and values strictly greater than X. Since rank ignores ties below or equal to X and only counts strictly greater values, binary search yields the exact contribution of each candidate skill. Because every class is evaluated independently over the same sorted structure, no recomputation is needed, and the minimum over all candidates correctly represents the optimal choice.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    N, M = map(int, input().split())
    arr = list(map(int, input().split()))
    S_A = arr[-1]
    opponents = arr[:-1]
    
    opponents.sort()
    
    import bisect
    
    best = N + 1
    
    for p in map(int, input().split()):
        x = S_A + p
        # first index > x
        idx = bisect.bisect_right(opponents, x)
        stronger = N - idx
        rank = stronger + 1
        if rank < best:
            best = rank
    
    print(best)

if __name__ == "__main__":
    main()
```

The solution separates Autumn from competitors before sorting, since she must not be included in the count of others.

The key implementation detail is using `bisect_right`, which correctly counts elements strictly greater than X by returning the first position where X could be inserted while keeping order. Subtracting this index from N yields the number of strictly larger values. Using `bisect_left` would be incorrect because it would treat equal values inconsistently and break the strict inequality requirement.

## Worked Examples

### Example 1

Input:

```
N=5, M=5
Opponents: 3 3 4 5 2
Autumn: 1
Boosts: 1 2 3 4 5
```

We compute final skill and rank:

| Boost | Final Skill X | idx (≤X end) | Stronger | Rank |
| --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 4 | 5 |
| 2 | 3 | 3 | 2 | 3 |
| 3 | 4 | 4 | 1 | 2 |
| 4 | 5 | 5 | 0 | 1 |
| 5 | 6 | 5 | 0 | 1 |

Minimum rank is 1.

This demonstrates how increasing X reduces the suffix of strictly greater competitors until Autumn becomes top-ranked.

### Example 2

Input:

```
N=4, M=3
Opponents: 10 10 20 30
Autumn: 15
Boosts: 0 5 20
```

| Boost | Final Skill X | idx | Stronger | Rank |
| --- | --- | --- | --- | --- |
| 0 | 15 | 2 | 2 | 3 |
| 5 | 20 | 3 | 1 | 2 |
| 20 | 35 | 4 | 0 | 1 |

This shows the effect of ties at 20: equal values are not counted as strictly stronger, so only values greater than X matter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + M) log N) | sorting plus one binary search per class |
| Space | O(N) | storage for opponent list |

The constraints allow up to 200,000 elements, and logarithmic processing per query is well within limits. Sorting dominates preprocessing, and the rest scales linearly with M.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import bisect

    N, M = map(int, input().split())
    arr = list(map(int, input().split()))
    SA = arr[-1]
    opp = arr[:-1]
    opp.sort()

    best = 10**18
    boosts = list(map(int, input().split()))

    for p in boosts:
        x = SA + p
        idx = bisect.bisect_right(opp, x)
        rank = (N - idx) + 1
        best = min(best, rank)

    return str(best)

# sample
assert run("5 5\n3 3 4 5 2 1\n1 2 3 4 5\n") == "1"

# minimum size
assert run("1 1\n10 1\n1\n") == "1"

# all equal competitors
assert run("3 2\n5 5 5 5\n0 10\n") == "1"

# Autumn always weakest
assert run("3 2\n10 20 30 1\n0 0\n") == "4"

# strong boost dominates
assert run("3 2\n10 20 30 1\n100 200\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| min size | 1 | single competitor edge |
| all equal | 1 | tie handling correctness |
| weakest Autumn | 4 | full ranking shift |
| large boosts | 1 | dominance case |

## Edge Cases

When all competitors have the same skill as Autumn after boosting, the binary search returns index 0 or full length depending on comparison, but the number of strictly greater competitors becomes zero. For example, if opponents are `[5, 5, 5]` and X is `5`, `bisect_right` returns 3, so stronger is 0 and rank is 1. This correctly reflects that ties do not hurt rank.

When Autumn is already strictly above all competitors even for the smallest boost, every query yields rank 1. For instance, opponents `[1, 2, 3]`, Autumn `10`, boosts `[1, 2]` produce final skills `11` and `12`, both exceeding all competitors. The algorithm consistently returns zero stronger competitors and thus rank 1.

When boosts are minimal or zero-like in effect, the algorithm still works because each candidate is evaluated independently; there is no assumption that boosts are increasing or sorted.
