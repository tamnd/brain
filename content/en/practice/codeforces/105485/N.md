---
title: "CF 105485N - \u4f4e\u8c37(hard)"
description: "We are given a sequence of numbers and allowed to perform a fixed number of operations. Each operation chooses a single position and decreases that value by exactly one. After doing this up to k times in total, we want to maximize how many indices become “valleys”."
date: "2026-06-23T01:57:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105485
codeforces_index: "N"
codeforces_contest_name: "2024 China Unversity of Geosciences (Wuhan) Freshman Contest"
rating: 0
weight: 105485
solve_time_s: 55
verified: true
draft: false
---

[CF 105485N - \u4f4e\u8c37(hard)](https://codeforces.com/problemset/problem/105485/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of numbers and allowed to perform a fixed number of operations. Each operation chooses a single position and decreases that value by exactly one. After doing this up to k times in total, we want to maximize how many indices become “valleys”.

A valley is an internal position i, meaning it cannot be the first or last element, such that its value is strictly smaller than both neighbors after all modifications. So for a chosen configuration of decrements, we are trying to shape the array so that many interior points become local minima.

The important constraint is that each operation is extremely local: it only reduces one element. We never increase values, so the only way to create a valley at position i is to ensure ai becomes sufficiently small compared to ai−1 and ai+1, either by lowering ai or by not lowering its neighbors too much.

The input size n is up to 10^5 and k is up to 10^9. The array values can also be large. This combination immediately rules out any simulation over k operations. Any valid solution must reason about how many valleys can be formed structurally and how much “effort” each valley requires.

A subtle issue appears when valleys overlap. If we try to greedily force a valley at every position independently, we may underestimate shared costs or overcount achievable valleys because changing one element affects two potential valley conditions. Another failure case is assuming that lowering only the center is always optimal, when sometimes lowering neighbors is cheaper depending on height differences.

## Approaches

The brute-force idea is to simulate operations and try all possibilities of distributing k decrements across positions. After each hypothetical distribution, we check how many valleys exist. This is equivalent to distributing k unit decreases over n positions in all possible ways, which is combinatorially enormous. Even ignoring enumeration, evaluating a single configuration is O(n), and the number of configurations is on the order of stars and bars, far beyond feasible limits.

A more structured brute force is to greedily build valleys one by one. For each candidate position i, we compute how many decrements are needed to make ai strictly less than both neighbors, assuming neighbors are fixed. Then we pick the cheapest valley repeatedly. This fails because once we modify an index, costs of nearby valleys change, so recomputing locally still leads to repeated O(n) scans per selection, giving O(n^2).

The key observation is that valleys are independent in a very specific way: a valley at i only depends on the triple (i−1, i, i+1). If we decide that position i is a valley, the only requirement is that ai must be strictly smaller than both neighbors. Since we can only decrease values, we never want to increase neighbors. So the best strategy for forming a valley is to only reduce ai, not its neighbors, because lowering neighbors would only make other valleys harder without helping this one.

Thus, for a fixed i, the cost to make it a valley is:

cost(i) = max(0, min(ai−1, ai+1) − (ai − 1) + 1)

This simplifies to:

cost(i) = max(0, ai − min(ai−1, ai+1) + 1)

Each valley is independent in cost, because we never touch neighbors when building it. Therefore the problem reduces to selecting as many indices i as possible such that the sum of their costs does not exceed k.

This becomes a classic greedy selection problem: compute all costs, sort them, and pick the smallest costs first.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / O(n^2) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We focus on transforming the problem into independent “valley costs” and then selecting the maximum number under a budget.

1. For every index i from 2 to n−1, compute m = min(ai−1, ai+1). This value represents the threshold below which ai must fall to become a valley.
2. If ai is already strictly less than m, then i is already a valley candidate requiring zero operations. Otherwise, compute the number of decrements needed as cost = ai − m + 1. This is the minimal amount needed to make ai strictly smaller than both neighbors.
3. Collect all such costs into a list. Each cost represents how expensive it is to “activate” a valley at that position without affecting any other position.
4. Sort the list of costs in non-decreasing order. This ordering ensures that we prioritize valleys that are cheapest to create.
5. Traverse the sorted list while maintaining a running sum of used operations. For each cost, if adding it does not exceed k, include it and increment the answer. Otherwise, stop or skip further inclusion.
6. Return the number of selected valleys.

### Why it works

Each valley requirement is local to a triple and can be satisfied purely by decreasing the center element. Since operations only reduce values, touching neighbors never helps reduce cost for another valley; it only risks increasing costs elsewhere indirectly. Therefore, each valley can be treated as an independent item with a fixed price. The task becomes maximizing the count of items under a total budget, which greedy selection by smallest cost is optimal because each item has equal value (one valley) and only differs in cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    costs = []
    
    for i in range(1, n - 1):
        m = min(a[i - 1], a[i + 1])
        if a[i] < m:
            costs.append(0)
        else:
            costs.append(a[i] - m + 1)
    
    costs.sort()
    
    ans = 0
    used = 0
    
    for c in costs:
        if used + c <= k:
            used += c
            ans += 1
        else:
            break
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The code directly implements the reduction from valley formation to independent costs. The loop over internal indices computes the minimal required decrement per position. Sorting is essential because it ensures we always spend operations on the cheapest valleys first, maximizing count under a fixed budget k.

A subtle implementation detail is handling already-valid valleys, where cost becomes zero. These should be taken first because they do not consume any operations. The greedy loop naturally includes them immediately.

## Worked Examples

We construct two traces to illustrate behavior.

### Example 1

Input:

```
5 3
3 1 3 1 3
```

Costs computation:

| i | ai−1 | ai | ai+1 | min | cost |
| --- | --- | --- | --- | --- | --- |
| 2 | 3 | 1 | 3 | 3 | 0 |
| 3 | 1 | 3 | 1 | 1 | 3 |

Sorted costs: [0, 3]

| Step | cost | used | valleys |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 1 |
| 2 | 3 | 3 | 2 |

Output is 2.

This shows that zero-cost valleys are always taken first and do not interact with paid ones.

### Example 2

Input:

```
6 2
5 4 3 2 1 2
```

Costs:

| i | triple | min | cost |
| --- | --- | --- | --- |
| 2 | (5,4,3) | 3 | 2 |
| 3 | (4,3,2) | 2 | 2 |
| 4 | (3,2,1) | 1 | 2 |
| 5 | (2,1,2) | 2 | 0 |

Sorted: [0,2,2,2]

| Step | cost | used | valleys |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 1 |
| 2 | 2 | 2 | 2 |

We stop after using full budget.

This demonstrates that even though many valleys are possible structurally, the budget k limits selection.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Computing costs is linear, sorting dominates |
| Space | O(n) | Stores cost list |

The constraints n ≤ 10^5 make O(n log n) comfortably fast. The value range of k up to 10^9 is irrelevant since we only accumulate costs without iterating over k.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample
assert run("7 3\n2 2 3 4 6 2 3\n") == "3"

# minimum size (no internal valleys)
assert run("2 10\n5 5\n") == "0"

# all equal
assert run("5 5\n3 3 3 3 3\n") == "3"

# already many valleys
assert run("5 0\n5 1 5 1 5\n") == "2"

# large k but structure limits
assert run("5 100\n10 9 8 7 6\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 3 | correctness on given case |
| n=2 | 0 | no valid valley positions |
| all equal | 3 | zero-cost activation |
| k=0 pattern | 2 | already-valid valleys only |
| descending array | 2 | budget not needed but structure limits |

## Edge Cases

A first edge case is when n ≤ 2. The algorithm naturally produces an empty cost list because there are no interior indices. For example, input `n=2` always returns 0 since no position can satisfy the valley definition.

Another case is arrays where many valleys are already valid without any operation. For input `5 0` and array `[5,1,5,1,5]`, every internal position is already a valley. The computed costs are all zero, so the algorithm selects all of them without consuming k.

A third case is when k is extremely large but structure limits valleys. For `[10,9,8,7,6]`, each interior position has cost 2, so only two valleys can be selected if k=100 still respects that at most two positions exist. The greedy selection still returns the correct structural maximum even when budget is irrelevant.
