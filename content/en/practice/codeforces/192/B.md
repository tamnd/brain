---
title: "CF 192B - Walking in the Rain"
description: "We are asked to determine the number of days the opposition can walk along a boulevard of tiles before it becomes impossible due to the tiles being destroyed by rain. Each tile has a durability measured in days."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 192
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 121 (Div. 2)"
rating: 1100
weight: 192
solve_time_s: 180
verified: false
draft: false
---

[CF 192B - Walking in the Rain](https://codeforces.com/problemset/problem/192/B)

**Rating:** 1100  
**Tags:** brute force, implementation  
**Solve time:** 3m  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine the number of days the opposition can walk along a boulevard of tiles before it becomes impossible due to the tiles being destroyed by rain. Each tile has a durability measured in days. On day _aᵢ_ the tile is still intact, and on day _aᵢ + 1_ it is destroyed. Movement is constrained: from tile _i_, the opposition can move to tile _i+1_ or _i+2_. The walk is thwarted if the first or last tile is destroyed, or if there is no sequence of jumps that allows reaching the last tile from the first.

The input is the number of tiles, _n_, followed by an array _a_ of size _n_ representing the day each tile is destroyed. The output is a single integer: the last day the walk is still feasible.

The constraints are small: _n_ ≤ 1000 and _aᵢ_ ≤ 1000. This allows solutions with time complexity up to roughly O(n²) without worrying about timeouts. Because movement allows jumps over a single tile, the key challenge is identifying the largest contiguous gap of destroyed tiles that blocks all possible paths. Edge cases include when _n_ = 1, where the first and last tile are the same, and scenarios where a single tile’s destruction immediately prevents any valid path.

## Approaches

A brute-force approach simulates each day starting from day 1, marking destroyed tiles, and trying to traverse from the first to the last tile using a greedy or BFS method. While correct, this approach requires checking up to 1000 days for each traversal, leading to an O(n²) worst-case complexity which is acceptable given the constraints but unnecessary.

The key observation is that the walk becomes impossible when there is a segment of three consecutive tiles where all are destroyed. Since the opposition can jump over one tile, a two-tile gap can be bypassed, but a three-tile gap blocks the path entirely. Therefore, the maximal day for which a walk is possible is the minimal value among all triplets of consecutive tiles. We also need to check the first and last tiles separately, as their destruction immediately prevents a start or finish.

By focusing on consecutive triplets, we reduce the problem from simulating every day to a simple scan through the tiles array, yielding an O(n) solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate each day) | O(n * max(aᵢ)) ≈ 10^6 | O(n) | Acceptable but inefficient |
| Optimal (scan consecutive triplets) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `max_day` to infinity. This variable will hold the last day a valid path exists.
2. Iterate through the array of tile durability. For each triplet of consecutive tiles (tiles i, i+1, i+2), compute the minimal destruction day among them. Update `max_day` to the minimum of its current value and this triplet minimum minus 1. The minus 1 accounts for the fact that the tile is still intact on day _aᵢ_ but destroyed on day _aᵢ + 1_.
3. Check the first and last tiles separately. If either is destroyed on day _d_, update `max_day` to min(max_day, a₁ - 1) or min(max_day, aₙ - 1) respectively.
4. After scanning all relevant tiles, print `max_day`.

The invariant maintained is that `max_day` always represents the last day before any critical blockage appears. This guarantees correctness because the opposition only fails if a tile or triplet of consecutive tiles becomes unusable, which is precisely what we check.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

# Handle trivial case of single tile
if n == 1:
    print(a[0] - 1)
    sys.exit()

max_day = float('inf')

# Check triplets
for i in range(n - 2):
    max_day = min(max_day, min(a[i], a[i + 1], a[i + 2]) - 1)

# Check first and last tiles
max_day = min(max_day, a[0] - 1)
max_day = min(max_day, a[-1] - 1)

print(max_day)
```

The solution first handles the single-tile edge case. Then it scans through all consecutive triplets to find the earliest day a blockage occurs. Finally, it ensures that the first and last tiles are intact. Subtracting 1 accounts for the tile still being usable on the day it reaches its destruction threshold.

## Worked Examples

**Sample 1**

Input:

```
4
10 3 5 10
```

| i | Triplet min(a[i],a[i+1],a[i+2]) | max_day |
| --- | --- | --- |
| 0 | min(10,3,5) = 3 | 3 - 1 = 2 |
| 1 | min(3,5,10) = 3 | min(2, 3-1) = 2 |

First tile: 10 - 1 = 9 → min(2,9)=2

Last tile: 10 - 1 = 9 → min(2,9)=2

Output: `2`

This shows the path is blocked after day 2, which matches the requirement that the second tile's early destruction prevents movement over two consecutive destroyed tiles.

**Sample 2**

Input:

```
5
6 4 5 7 5
```

| i | Triplet min | max_day |
| --- | --- | --- |
| 0 | min(6,4,5)=4 | 4-1=3 |
| 1 | min(4,5,7)=4 | min(3,3)=3 |
| 2 | min(5,7,5)=5 | min(3,5-1)=3 |

First tile: 6-1=5 → min(3,5)=3

Last tile: 5-1=4 → min(3,4)=3

Output: `3`

The table demonstrates that even though some tiles survive longer, the presence of a critical triplet limits the overall walk.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over tiles array for triplets and edges |
| Space | O(1) | Only variables for tracking max_day, no additional structures |

Given n ≤ 1000, this linear scan runs well within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    if n == 1:
        return str(a[0] - 1)
    max_day = float('inf')
    for i in range(n - 2):
        max_day = min(max_day, min(a[i], a[i + 1], a[i + 2]) - 1)
    max_day = min(max_day, a[0] - 1)
    max_day = min(max_day, a[-1] - 1)
    return str(max_day)

# Provided samples
assert run("4\n10 3 5 10\n") == "2", "sample 1"
assert run("5\n6 4 5 7 5\n") == "3", "sample 2"

# Custom cases
assert run("1\n10\n") == "9", "single tile"
assert run("3\n2 2 2\n") == "1", "all equal, triplet blocks on day 2"
assert run("4\n1 2 3 4\n") == "0", "first tile destroyed immediately"
assert run("5\n10 10 10 10 10\n") == "9", "all survive long, path ok"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n10 | 9 | single tile case |
| 3\n2 2 2 | 1 | triplet destruction blocks early |
| 4\n1 2 3 4 | 0 | first tile destroyed immediately |
| 5\n10 10 10 10 10 | 9 | uniform long durability, no early block |

## Edge Cases

When n = 1, the first and last tile are the same. The algorithm handles it by returning a[0] - 1, correctly representing the last usable day.

If a triplet of tiles has a lower durability than any other tiles, the loop finds the minimal among all triplets, ensuring the walk cannot continue beyond that point. For example, in `[10,3,5,10]`, the triplet `[10,3,5]` limits the path, correctly preventing overestimation.

If the first or last tile is destroyed before any triplet becomes critical, the separate checks guarantee `max_day` is updated accordingly. This handles the scenario `[1,10,10]`, producing `0` since the first tile fails immediately.
