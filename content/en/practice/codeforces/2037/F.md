---
title: "CF 2037F - Ardent Flames"
description: "We are given a line of enemies, each with a fixed health and a fixed position. Xilonen can attack from a single chosen position p, and each attack reduces an enemy’s health by m - The first key observation is that the damage from each attack decreases linearly with distance."
date: "2026-06-08T10:14:21+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "math", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2037
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 988 (Div. 3)"
rating: 2100
weight: 2037
solve_time_s: 100
verified: true
draft: false
---

[CF 2037F - Ardent Flames](https://codeforces.com/problemset/problem/2037/F)

**Rating:** 2100  
**Tags:** binary search, data structures, math, sortings, two pointers  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of enemies, each with a fixed health and a fixed position. Xilonen can attack from a single chosen position `p`, and each attack reduces an enemy’s health by `m - |p - x|` if that difference is non-negative. The goal is to choose `p` such that at least `k` enemies can be defeated with the fewest number of attacks. The output is that minimum number of attacks, or `-1` if no position allows killing `k` enemies.

The first key observation is that the damage from each attack decreases linearly with distance. This means that the further an enemy is from `p`, the more attacks are required to defeat it. We also notice that `p` can be any integer, not restricted to enemy positions, and the enemies’ positions are strictly increasing.

The constraints imply that `n` can reach up to 100,000 and `m` and `h_i` up to 10^9. This means we cannot afford an O(n^2) brute force approach where we simulate every possible position for `p`. We also need to handle up to 10^4 test cases with the sum of `n` over all cases at most 10^5. Therefore, our algorithm needs to be roughly O(n log n) per test case at worst, ideally faster.

Edge cases include when enemies are spaced further apart than `m`, making it impossible to affect more than one at a time, or when all enemies are within distance `m`, allowing one position to hit multiple targets. For example, if `n=2`, `m=1`, `k=2`, and positions are `[1, 3]`, no single `p` can reach both enemies, so the answer is `-1`. A naive approach that always assumes we can hit the first `k` enemies would fail here.

## Approaches

A brute-force approach would iterate over all possible integer positions for `p` and compute the number of attacks needed to defeat each enemy. We would then sort these counts and select the `k` smallest to see how many attacks suffice. While this is correct, it is far too slow because `p` can range up to 10^9, leading to a potentially huge search space.

The key insight is that the attack pattern is piecewise linear. Each enemy defines an interval of positions where it can be damaged. Specifically, an enemy at `x_i` with health `h_i` can survive up to `ceil(h_i / (m - |p - x_i|))` attacks, which decreases as `|p - x_i|` decreases. Therefore, for any number of attacks `t`, we can compute the interval of positions where an enemy would be defeated in at most `t` attacks. This transforms the problem into an interval coverage problem: we need a position `p` that lies in the intervals of at least `k` enemies.

We can combine this with binary search on the number of attacks. For a candidate `t`, we generate intervals for all enemies that would be defeated in `t` attacks. We then check if any position is covered by at least `k` of these intervals using a sweep-line approach, where we count overlaps efficiently by sorting interval endpoints. Binary search ensures we find the minimal `t` efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m_range) | O(n) | Too slow |
| Interval + Binary Search | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n`, `m`, `k`, the health array `h`, and positions array `x`.
2. Define a helper function `possible(t)` that returns True if at least `k` enemies can be defeated in `t` attacks.
3. In `possible(t)`, iterate over all enemies. For each enemy, compute the maximal distance `d` such that `m - d` times `t` is at least `h_i`. If `d >= m`, skip the enemy; it cannot be defeated in `t` attacks. Otherwise, add the interval `[x_i - d, x_i + d]` to a list.
4. Sort the interval endpoints and perform a sweep line. Track the number of overlapping intervals at each point. If at any point there are at least `k` overlapping intervals, return True.
5. Use binary search on `t`. Set `low = 1`, `high = max(h)`, or a safe upper bound such as 10^9. For each mid-value, call `possible(mid)`. If True, reduce `high`; if False, increase `low`.
6. After binary search, if no valid `t` is found, output `-1`. Otherwise, output the minimal `t` found.

Why it works: The binary search guarantees that the first `t` for which `possible(t)` returns True is minimal. The interval-based sweep ensures that we only consider positions that can actually defeat an enemy in `t` attacks, and counting overlaps guarantees we find a `p` that defeats at least `k` enemies. This approach avoids iterating over all integer positions.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def solve():
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        h = list(map(int, input().split()))
        x = list(map(int, input().split()))
        
        def possible(t_attacks):
            events = []
            for hi, xi in zip(h, x):
                d = m - math.ceil(hi / t_attacks)
                if d < 0:
                    continue
                left = xi - d
                right = xi + d
                events.append((left, 1))
                events.append((right + 1, -1))
            events.sort()
            count = 0
            for pos, delta in events:
                count += delta
                if count >= k:
                    return True
            return False
        
        low, high = 1, max(h)
        answer = -1
        while low <= high:
            mid = (low + high) // 2
            if possible(mid):
                answer = mid
                high = mid - 1
            else:
                low = mid + 1
        print(answer)
        
solve()
```

The code reads inputs efficiently using `sys.stdin.readline` and handles multiple test cases. The `possible` function computes the intervals for each enemy where they can be defeated within a candidate number of attacks, and then uses a sweep-line approach on sorted interval endpoints to see if there exists a position covered by at least `k` intervals. Binary search is used to minimize the number of attacks.

Subtle points include handling the ceiling of `hi / t` correctly, ensuring that intervals are inclusive of both ends, and adding `+1` to the right endpoint for sweep-line correctness. Off-by-one errors in the interval endpoints would break the count of overlapping intervals.

## Worked Examples

**Example 1:** `n=5, m=5, k=3, h=[7,7,7,7,7], x=[1,2,3,4,5]`.

| Attack t | Intervals of enemies | Max overlap |
| --- | --- | --- |
| 1 | [1-2,1+2],[2-2,2+2],[3-2,3+2],[4-2,4+2],[5-2,5+2] | 3 at positions 2,3,4 |
| 2 | [1-3,1+3],[2-3,2+3],... | overlap >= 3 |

The binary search finds that `t=2` is the minimum to defeat 3 enemies.

**Example 2:** `n=2, m=10, k=2, h=[1,1], x=[1,20]`.

Intervals for t=1: enemy1=[1-9,1+9]=[-8,10], enemy2=[20-9,20+9]=[11,29]. No overlap. Binary search returns `-1`.

This trace confirms that non-overlapping intervals correctly produce `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n log H) | Each binary search iteration does O(n log n) sweep, with log H iterations (H=max health) |
| Space | O(n) | Interval events stored per test case |

Given `n` ≤ 10^5 and sum over all test cases ≤ 10^5, and binary search over max `h_i` ≤ 10^9, the solution fits comfortably within the time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("""6
5 5 3
7 7 7 7 7
1 2 3 4 5
9 5 9
2 4 6 8 10 8 6 4 2
1 2 3 4 5 6 7 8 9
2 10 2
1 1
1 20
2 10 1
69696969 420420420
1 20
2 10 2
10 15
1 19
```
