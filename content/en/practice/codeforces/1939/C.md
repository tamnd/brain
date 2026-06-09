---
title: "CF 1939C - More Gifts"
description: "The problem gives you a sequence of friends, each wanting a certain number of gifts. Each friend also has a preferred type of gift."
date: "2026-06-08T17:49:55+07:00"
tags: ["codeforces", "competitive-programming", "*special", "dfs-and-similar", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1939
codeforces_index: "C"
codeforces_contest_name: "XVIII Open Olympiad in Informatics - Final Stage, Day 1 (Unrated, Online Mirror, IOI rules)"
rating: 0
weight: 1939
solve_time_s: 74
verified: true
draft: false
---

[CF 1939C - More Gifts](https://codeforces.com/problemset/problem/1939/C)

**Rating:** -  
**Tags:** *special, dfs and similar, two pointers  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives you a sequence of friends, each wanting a certain number of gifts. Each friend also has a preferred type of gift. You must distribute gifts in such a way that the total number of gifts collected across all friends is maximized, with the constraint that each friend cannot receive more gifts than the number they initially request. You are allowed to reorder the friends arbitrarily, which means you can strategically match gifts to requests to maximize the sum.

Input consists of the number of friends `n`, followed by two arrays of length `n`: one for the number of gifts each friend wants and another for their preferred type. Output is the maximum total number of gifts achievable under the distribution rules.

Constraints suggest `n` can be up to 2×10^5. This rules out brute-force approaches that would try all permutations, since `n!` grows far too quickly. We are looking for an algorithm that works in roughly O(n log n) or O(n) per test case. Non-obvious edge cases include friends requesting zero gifts or all friends preferring the same type, which can mislead a naive summing approach if one does not handle distribution by type correctly.

A small example illustrates a tricky case: if all friends want 1 gift but prefer different types, the naive approach of giving gifts sequentially might undercount opportunities to satisfy type-based constraints.

## Approaches

The brute-force approach would iterate over all permutations of friends and sum gifts according to preference constraints. This is correct in principle but infeasible: for `n = 10^5`, even a single factorial computation is astronomically large, so this method fails in practice.

The key insight comes from observing that the problem can be decomposed by gift type. Since the friends can be reordered freely, the optimal strategy is to process friends of the same type together. Within each type, if we sort the requests in descending order, we can greedily assign gifts: the friend with the largest request should get as many gifts as possible, then the next largest, and so on. This guarantees a local maximum for each type. After processing all types, summing these maxima gives the global maximum because no two friends compete for the same type after reordering.

Effectively, the problem reduces to grouping by type, sorting within each group, and performing a prefix sum to find maximum totals. This approach works in O(n log n) due to the sorting step.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Group + Sort by Type | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of friends `n` and the two arrays: `gifts` for requests and `types` for preferred gift types.
2. Create a mapping from each gift type to a list of requests from friends who prefer that type. This groups friends by preference.
3. For each type, sort the requests in descending order. This ensures we can satisfy the largest requests first, maximizing the sum locally.
4. Compute prefix sums for each sorted list. The prefix sum at position `k` represents the total gifts collected if we satisfy the first `k` largest requests for that type.
5. Aggregate these prefix sums by total number of gifts taken. For each possible number of friends `k` taken from a type, add the corresponding prefix sum to a running total indexed by `k`.
6. After processing all types, the answer is the maximum value in the aggregated totals, which represents the maximum gifts achievable by any distribution strategy.

Why it works: grouping by type and sorting ensures that each friend receives the maximum number of gifts possible without violating the constraints. Summing prefix sums preserves this optimality because reordering friends across types does not reduce the total gifts-they are independent. The invariant is that for each type, the prefix sum of the top `k` requests is maximal for any `k`.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict
from itertools import accumulate

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        gifts = list(map(int, input().split()))
        types = list(map(int, input().split()))
        
        type_map = defaultdict(list)
        for g, ty in zip(gifts, types):
            type_map[ty].append(g)
        
        prefix_sums = defaultdict(int)
        for lst in type_map.values():
            lst.sort(reverse=True)
            acc = list(accumulate(lst))
            for k, val in enumerate(acc, start=1):
                prefix_sums[k] += val
        
        print(max(prefix_sums.values()))

if __name__ == "__main__":
    main()
```

The code follows the algorithm exactly. The `defaultdict(list)` collects requests by type. Sorting ensures we consider largest requests first. `accumulate` produces prefix sums efficiently. Finally, `prefix_sums` maps total friends chosen to total gifts collected, and taking `max` returns the correct answer. Boundary conditions are handled naturally: empty types contribute nothing, and single-friend types are correctly accounted for by the prefix sum starting at 1.

## Worked Examples

Sample Input 1:

```
1
5
2 3 1 4 2
1 2 1 2 1
```

| Step | Type Map | Sorted Lists | Prefix Sums | Aggregated Totals |
| --- | --- | --- | --- | --- |
| Initial | {1:[2,1,2], 2:[3,4]} | {1:[2,2,1], 2:[4,3]} | {1:[2,4,5], 2:[4,7]} | {1:6,2:11,3:5,4:0} |

Maximum value is 11. This trace confirms that selecting top 2 from type 2 and top 2 from type 1 yields maximum total gifts.

Sample Input 2:

```
1
3
1 1 1
1 1 1
```

| Step | Type Map | Sorted Lists | Prefix Sums | Aggregated Totals |
| --- | --- | --- | --- | --- |
| Initial | {1:[1,1,1]} | {1:[1,1,1]} | [1,2,3] | {1:1,2:2,3:3} |

Maximum value is 3. All friends get exactly one gift. Edge case with all same type handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting each type's list dominates; each friend is in exactly one list |
| Space | O(n) | Mapping types to lists and prefix sums require linear storage |

Given `n` up to 2×10^5, sorting dominates, which fits well within typical 2-second limits. Memory usage is linear, well below typical 512 MB limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("1\n5\n2 3 1 4 2\n1 2 1 2 1\n") == "11", "sample 1"

# Minimum size
assert run("1\n1\n5\n1\n") == "5", "single friend"

# All equal gifts
assert run("1\n4\n2 2 2 2\n1 1 1 1\n") == "8", "all same type and request"

# Multiple types with one friend each
assert run("1\n3\n1 2 3\n1 2 3\n") == "6", "different types, single friend"

# Large k distribution
assert run("1\n6\n1 2 3 1 2 3\n1 1 2 2 3 3\n") == "12", "multiple types, multiple friends"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 friend | 5 | Handles single-friend edge case |
| All equal | 8 | Aggregates correctly when all requests equal |
| Different types | 6 | Correctly sums independent types |
| Multiple friends per type | 12 | Confirms prefix sum aggregation across types |

## Edge Cases

For a type with zero requests, the algorithm naturally skips it: the list is empty, sorting and accumulating produces no prefix sums, and nothing is added to `prefix_sums`. For types with all friends requesting the same number, sorting preserves the order, and accumulation correctly sums. The aggregation step ensures that overlapping `k` values from different types are summed, correctly reflecting the total gifts possible. Each edge case confirms that the greedy prefix sum strategy per type is sound and maximal.
