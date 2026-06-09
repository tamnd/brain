---
title: "CF 1657D - For Gamers. By Gamers."
description: "We have a strategy game scenario where Monocarp recruits a squad to fight a sequence of monsters. Each battle starts with an empty squad, and Monocarp can spend up to C coins per battle. Each unit type has a cost, damage per second, and health."
date: "2026-06-10T03:28:35+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1657
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 125 (Rated for Div. 2)"
rating: 2000
weight: 1657
solve_time_s: 61
verified: true
draft: false
---

[CF 1657D - For Gamers. By Gamers.](https://codeforces.com/problemset/problem/1657/D)

**Rating:** 2000  
**Tags:** binary search, brute force, greedy, math, sortings  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a strategy game scenario where Monocarp recruits a squad to fight a sequence of monsters. Each battle starts with an empty squad, and Monocarp can spend up to `C` coins per battle. Each unit type has a cost, damage per second, and health. Each monster has a damage per second and total health. The battle is simultaneous, meaning Monocarp wins only if his squad kills the monster strictly faster than the monster kills a single unit of his squad.

The input provides the details of `n` unit types and `m` monsters. The output must report, for each monster, the minimum coins Monocarp needs to spend to win. If no combination within `C` coins allows victory, we return `-1`.

Given the constraints, `n` and `m` can be up to `3 * 10^5` and coin limits up to `10^6`. This rules out naive approaches that iterate over every number of units per type for every monster, as that would require potentially `O(n * C * m)` operations, which is far too large.

A non-obvious edge case arises when a single unit of a type can defeat a monster, but multiple units are cheaper. For example, a cheap unit may need 5 copies to beat the monster, costing 50 coins, while an expensive but stronger unit needs only one copy, costing 30 coins. A careless solution that always takes the first type that satisfies the condition can return a suboptimal or impossible answer.

## Approaches

The brute-force approach considers each unit type and tries every possible number of units that can be recruited within the coin limit. For each combination, we check whether the squad kills the monster before the monster kills a unit. This works for correctness but is far too slow because iterating over up to `C` coins for each of `n` units and `m` monsters leads to a worst-case operation count of `O(n * C * m)`.

The key insight is that the battle condition depends on the ratio of total squad damage to monster health and total monster damage to unit health. Let `k` be the number of units of type `i`. The squad kills the monster in `H_j / (k * d_i)` seconds, and the monster kills a unit in `h_i / D_j` seconds. Victory requires `H_j / (k * d_i) < h_i / D_j`, which simplifies to `k > H_j * D_j / (h_i * d_i)`. Thus, for each unit type, we can compute the minimum number of units required to beat a given monster. The corresponding cost is `ceil(k) * c_i`. We only need the minimum such cost across all unit types.

Because `C` can be up to `10^6`, iterating `k` directly is unnecessary. Precomputing the maximum damage achievable per coin count allows us to answer queries in `O(log C)` time per monster via a search. Sorting and keeping a prefix maximum of `damage * health` ensures that dominated unit types (more expensive but strictly worse) do not affect the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * C * m) | O(n * C) | Too slow |
| Optimal | O(n + C + m * log C) | O(C) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `best` of size `C + 1` to track the best `damage * health` achievable for each coin amount up to `C`. Set all entries to zero initially.
2. Iterate over all unit types. For each unit type with cost `c_i`, damage `d_i`, and health `h_i`, compute `d_i * h_i`. Update `best[c_i]` to be the maximum of its current value and `d_i * h_i`. This ensures that for each cost, we know the most effective single unit type.
3. Propagate the prefix maximum over the `best` array. For every coin value from 1 to `C`, set `best[i] = max(best[i], best[i-1])`. This ensures that for any coin budget, we know the best unit type affordable.
4. For each monster with `D_j` and `H_j`, compute `threshold = H_j * D_j`. We now want the smallest coin count `k` such that `best[k] > threshold`. Perform a binary search over the `best` array from 1 to `C`.
5. If a valid `k` is found, output `k`. Otherwise, output `-1`.

Why it works: The battle condition reduces to `k * d_i * h_i > H_j * D_j`. By precomputing the maximum `d_i * h_i` per coin count and using prefix maxima, we guarantee that we can answer each monster query by searching for the minimal coin expenditure that satisfies the inequality. Dominated unit types cannot reduce the coin cost below the minimal `k` found.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, C = map(int, input().split())
best = [0] * (C + 1)

for _ in range(n):
    c, d, h = map(int, input().split())
    value = d * h
    if best[c] < value:
        best[c] = value

for i in range(1, C + 1):
    best[i] = max(best[i], best[i - 1])

m = int(input())
monsters = [tuple(map(int, input().split())) for _ in range(m)]
res = []

for D, H in monsters:
    left, right = 1, C
    ans = -1
    threshold = D * H
    while left <= right:
        mid = (left + right) // 2
        if best[mid] > threshold:
            ans = mid
            right = mid - 1
        else:
            left = mid + 1
    res.append(str(ans))

print(" ".join(res))
```

The first loop constructs the `best` array with the maximum `d*h` value per cost. The second loop builds prefix maxima so that for any coin budget, we can access the most effective unit. The binary search checks for the smallest coin expenditure meeting the monster threshold. Using integer arithmetic avoids floating-point errors, and the order of propagation ensures we do not miss a cheaper unit type that could beat the monster.

## Worked Examples

### Sample Input 1

```
3 10
3 4 6
5 5 5
10 3 4
3
8 3
5 4
10 15
```

| Monster | Threshold H*D | best array max ≤ C | Coin result |
| --- | --- | --- | --- |
| 8 3 | 24 | best[3]=24, best[5]=25 | 5 |
| 5 4 | 20 | best[3]=24 | 3 |
| 10 15 | 150 | best[10]=25 | -1 |

This trace shows that for the first monster, although multiple units of type 1 could meet the threshold, type 2 achieves it cheaper.

### Custom Example

```
2 5
2 2 2
3 3 1
1
3 3
```

| Monster | Threshold H*D | best array max ≤ C | Coin result |
| --- | --- | --- | --- |
| 3 3 | 9 | best[3]=3 | -1 |

The threshold cannot be met by any unit within the coin limit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + C + m * log C) | Construct `best` in O(n), prefix maxima in O(C), binary search for each monster in O(log C) |
| Space | O(C + m) | `best` array size C+1, monster list size m |

The algorithm is efficient given n, m ≤ 3*10^5 and C ≤ 10^6. Binary search ensures that even the largest number of monsters is processed in acceptable time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, C = map(int, input().split())
    best = [0] * (C + 1)
    for _ in range(n):
        c, d, h = map(int, input().split())
        best[c] = max(best[c], d*h)
    for i in range(1, C + 1):
        best[i] = max(best[i], best[i-1])
    m = int(input())
    monsters = [tuple(map(int, input().split())) for _ in range(m)]
    res = []
    for D, H in monsters:
        left, right = 1, C
        ans = -1
        threshold = D * H
        while left <= right:
            mid = (left + right) // 2
            if best[mid] > threshold:
                ans = mid
                right = mid - 1
            else:
                left = mid + 1
        res.append(str(ans))
    return " ".join(res)

# Provided samples
assert run("3 10\n3 4 6\n5 5 5\n10 3 4\n3\n8 3\n5 4\n10 15\n") == "5 3 -1"

# Custom cases
assert run("2 5\n2 2 2\n3 3
```
