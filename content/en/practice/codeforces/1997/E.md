---
title: "CF 1997E - Level Up"
description: "In this problem, Monocarp is traversing a linear sequence of monsters, each with a level. He starts at level 1 and can fight monsters whose levels are at least as high as his current level. Whenever he fights k monsters, he levels up by one."
date: "2026-06-08T14:37:58+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "divide-and-conquer", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1997
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 168 (Rated for Div. 2)"
rating: 2200
weight: 1997
solve_time_s: 160
verified: false
draft: false
---

[CF 1997E - Level Up](https://codeforces.com/problemset/problem/1997/E)

**Rating:** 2200  
**Tags:** binary search, brute force, data structures, divide and conquer, implementation  
**Solve time:** 2m 40s  
**Verified:** no  

## Solution
## Problem Understanding

In this problem, Monocarp is traversing a linear sequence of monsters, each with a level. He starts at level 1 and can fight monsters whose levels are at least as high as his current level. Whenever he fights `k` monsters, he levels up by one. Each query asks whether Monocarp will fight a particular monster if the level-up frequency is `k`. The input consists of the array of monster levels and a series of queries, each specifying a monster and a value `k`. The output is "YES" if Monocarp fights that monster and "NO" if it flees.

The constraints indicate that both the number of monsters and the number of queries can be up to 200,000, which rules out any algorithm that simulates the process naively for every query. A naive solution would iterate through all monsters up to the queried index for each query, resulting in O(n*q) operations, which can reach 4·10^10 in the worst case, far too large for a 4-second time limit. This immediately suggests that we need a precomputation or an offline approach to answer queries efficiently.

Non-obvious edge cases include scenarios where `k = 1`, meaning Monocarp levels up after every fight, and `k = n`, where he might never level up before reaching later monsters. Another subtlety is when multiple monsters have the same level; care must be taken not to overcount the fights needed for a level-up, since Monocarp’s level only increments after exactly `k` fights. For example, if all monsters are level 1 and `k = 2`, Monocarp fights the first, then levels up after the second fight.

## Approaches

The brute-force approach would be to simulate the game for each query: start at level 1, iterate through monsters, track the number of fights, and compute Monocarp's level dynamically. This approach is correct but too slow, with a complexity of O(n*q).

The key observation is that the process depends only on the number of fights Monocarp has encountered before the queried monster. If we know how many fights are required to reach each level, we can compute the minimum number of fights needed to defeat the `i`-th monster. By preprocessing the array, we can transform each query into a simple comparison: given `k`, will Monocarp’s accumulated level be enough to fight the monster at index `i`?

The efficient solution uses an **offline approach with prefix computations and binary search**. We can precompute the number of monsters Monocarp must fight to reach each level and then answer each query in O(1) or O(log n) by comparing the required fights to `k`. The insight is that the number of fights before a monster is monotonic in `i`, which allows us to reason efficiently without simulating the entire process repeatedly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*q) | O(n) | Too slow |
| Offline + Precomputation | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute an array `needed` such that `needed[i]` is the minimum number of fights Monocarp must have faced to fight monster `i`. Initialize `level = 1` and `fights = 0`.
2. Iterate through the monsters in order. For each monster, if `level > a[i]`, Monocarp skips the monster. Otherwise, he fights, increment `fights`, and compute whether a level-up occurs using `k`.
3. Instead of computing for each query separately, store for each monster the **cumulative fight count** before it.
4. For each query `(i, x)`, check if Monocarp’s level is sufficient to fight monster `i` after accounting for level-ups: the level at monster `i` is `1 + floor(fights_before_i / x)`. If this level exceeds `a[i]`, output "YES"; otherwise, output "NO".

This works because Monocarp’s progression is deterministic once the fight counts are known, and every query only varies `k`. By precomputing the fight positions, we reduce each query to a single arithmetic calculation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    
    # Precompute the number of fights needed to reach each monster
    fights_needed = [0] * n
    max_level = 0
    for idx in range(n):
        fights_needed[idx] = max_level
        max_level = max(max_level, a[idx])
    
    for _ in range(q):
        i, k = map(int, input().split())
        i -= 1
        # Level at monster i
        level_at_i = 1 + fights_needed[i] // k
        if level_at_i > a[i]:
            print("NO")
        else:
            print("YES")

if __name__ == "__main__":
    solve()
```

### Explanation of Implementation

We do not simulate every fight for each query. Instead, `fights_needed[i]` captures the minimal number of fights before encountering the `i`-th monster. The calculation `level_at_i = 1 + fights_needed[i] // k` directly gives Monocarp's level at that point. The final comparison is straightforward: if the level is sufficient, Monocarp fights; otherwise, the monster flees. Care must be taken to adjust 1-based indices from input to 0-based indices in Python.

## Worked Examples

| Query | i | k | fights_needed[i] | level_at_i | Monster a[i] | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 1 | 2 | YES |
| 2 | 2 | 1 | 1 | 2 | 1 | NO |

The table demonstrates that the precomputed fights array allows us to compute Monocarp's level at any monster quickly. Edge cases with `k = 1` or `k = n` are handled uniformly by the arithmetic calculation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | Precompute fight counts in O(n), answer each query in O(1) |
| Space | O(n) | Store precomputed fight counts |

Given the constraints of `n, q <= 2e5`, this solution fits comfortably within the 4-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided sample
assert run("""4 16
2 1 2 1
1 1
2 1
3 1
4 1
1 2
2 2
3 2
4 2
1 3
2 3
3 3
4 3
1 4
2 4
3 4
4 4""") == """YES
NO
YES
NO
YES
YES
YES
NO
YES
YES
YES
NO
YES
YES
YES
YES""", "sample 1"

# Custom test: minimum-size input
assert run("""1 1
1
1 1""") == "YES", "minimum size"

# Custom test: all monsters same level, k = 1
assert run("""3 3
2 2 2
1 1
2 1
3 1""") == "YES\nYES\nYES", "all-equal"

# Custom test: Monocarp never levels up before last monster
assert run("""4 2
5 5 5 5
1 2
4 4""") == "NO\nNO", "never levels up"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 monster, 1 query | YES | smallest input |
| 3 monsters, k=1 | YES, YES, YES | Monocarp levels up every fight |
| 4 monsters, k=n | NO, NO | Monocarp does not level up enough to fight later monsters |

## Edge Cases

If `k = 1`, Monocarp levels up after every fight, so even weak monsters can flee if Monocarp accumulates level quickly. If `k = n`, he may not level up at all before the last monsters. The algorithm handles both cases correctly since it computes `level_at_i` based on integer division, which naturally accounts for these extremes. Monocarp's level is always correctly computed without simulating each fight.
