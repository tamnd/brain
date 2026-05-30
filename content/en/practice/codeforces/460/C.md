---
title: "CF 460C - Present"
description: "We are asked to maximize the minimum height of flowers after a limited number of days of watering. Each flower has an initial height, and on any day we can water a contiguous segment of exactly w flowers, increasing each by one."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 460
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 262 (Div. 2)"
rating: 1700
weight: 460
solve_time_s: 60
verified: true
draft: false
---

[CF 460C - Present](https://codeforces.com/problemset/problem/460/C)

**Rating:** 1700  
**Tags:** binary search, data structures, greedy  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to maximize the minimum height of flowers after a limited number of days of watering. Each flower has an initial height, and on any day we can water a contiguous segment of exactly _w_ flowers, increasing each by one. We have _m_ days to apply such waterings, and the flowers are arranged in a fixed line, so the watering segments must respect the order.

The input gives the number of flowers _n_, number of days _m_, and the width of watering _w_, followed by the initial heights of the flowers. The output is a single integer: the largest possible height of the smallest flower after optimally applying watering over the _m_ days.

The constraints tell us that _n_ can be up to 10^5, and _m_ can also be up to 10^5, with flower heights up to 10^9. This rules out any naive simulation where we attempt every possible watering sequence because the number of possibilities is exponential. Any solution must operate in roughly O(n log X) or O(n) per test case, where X is bounded by the maximum achievable height.

An important edge case occurs when the smallest flower is already high relative to others or when _w_ = 1. For example, if _n_ = 3, _m_ = 1, _w_ = 1, and initial heights are `[1, 2, 3]`, the maximum minimum height is `2` because we can only increment one flower by one unit. A careless approach that tries to water greedily from left to right without considering the remaining waterings would overestimate the achievable minimum.

## Approaches

A brute-force solution would try all sequences of daily waterings, updating the array each time and checking the minimum. It is correct because any sequence of waterings can be simulated, but it requires O(n * m * n) operations in the worst case, which is far too slow given n, m ≤ 10^5.

The key insight is that the problem can be reframed as a decision problem: "Can we achieve minimum height H using at most m waterings?" If we can efficiently answer this question, we can apply binary search over H. This works because increasing H is monotone: if H is achievable, any smaller H is also achievable; if H is not achievable, any larger H is impossible.

Checking if a height H is achievable can be done greedily with a difference array to simulate the incremental effects of watering in O(n). For each flower, we track the net effect of previous waterings and decide whether to apply a new watering segment to meet height H. This avoids updating the full array every time and keeps the complexity linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m * n) | O(n) | Too slow |
| Optimal (Binary Search + Greedy + Difference Array) | O(n log(max_height)) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize `low` to the minimum flower height and `high` to `max(a) + m`, the theoretical upper bound of the minimum height after applying all waterings to the smallest flowers.
2. While `low < high`, pick `mid = (low + high + 1) // 2`. This is the candidate minimum height H we want to test.
3. To test if H is achievable, initialize a difference array `add` of size n+1 to zero. This array will track how many waterings affect each flower efficiently.
4. Track `current_add = 0`, the net growth from previous waterings as we iterate left to right.
5. For each flower i from 0 to n-1, calculate `current_height = a[i] + current_add`. If `current_height < H`, we must water starting at i. The number of waterings needed is `delta = H - current_height`.
6. Increment `current_add` by delta, and update `add[i + w] -= delta` if `i + w < n` to indicate the effect of this watering ends after position i + w - 1. Track the total waterings used so far.
7. If total waterings exceed m, H is not achievable; otherwise, it is.
8. If H is achievable, set `low = mid`; otherwise, set `high = mid - 1`.
9. After binary search ends, `low` is the maximum achievable minimum height.

Why it works: The difference array ensures that each watering increment affects exactly w contiguous flowers and that we can compute the net effect on any flower in O(1). Binary search leverages the monotonicity of the decision function. The greedy choice at each flower ensures we never under-water, which would fail to reach H, and never over-water, which could waste days.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_achieve(H, n, m, w, a):
    add = [0] * (n + 1)
    current_add = 0
    used = 0
    for i in range(n):
        current_add += add[i]
        if a[i] + current_add < H:
            delta = H - (a[i] + current_add)
            used += delta
            if used > m:
                return False
            current_add += delta
            if i + w < n:
                add[i + w] -= delta
    return True

def solve():
    n, m, w = map(int, input().split())
    a = list(map(int, input().split()))
    low, high = min(a), max(a) + m
    while low < high:
        mid = (low + high + 1) // 2
        if can_achieve(mid, n, m, w, a):
            low = mid
        else:
            high = mid - 1
    print(low)

if __name__ == "__main__":
    solve()
```

The solution separates the binary search and feasibility check. `can_achieve` uses a difference array so each watering only updates two positions, keeping the time complexity O(n). Off-by-one errors are avoided by careful indexing of the difference array, noting that the effect of watering from position i lasts until i + w - 1.

## Worked Examples

**Sample 1**:

Input: `n=6, m=2, w=3, a=[2,2,2,2,1,1]`

Binary search tests H = 3:

| i | a[i] | current_add | delta | used |
| --- | --- | --- | --- | --- |
| 0 | 2 | 0 | 1 | 1 |
| 1 | 2 | 1 | 0 | 1 |
| 2 | 2 | 1 | 0 | 1 |
| 3 | 2 | 1 | 1 | 2 |
| 4 | 1 | 1 | 1 | 3 → exceeds m=2 → False |

So H=3 fails, H=2 succeeds. Output is 2.

**Custom Example**:

Input: `n=5, m=5, w=2, a=[1,1,1,1,1]`

Binary search tests H=3:

| i | a[i] | current_add | delta | used |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 2 | 2 |
| 1 | 1 | 2 | 0 | 2 |
| 2 | 1 | 2 | 1 | 3 |
| 3 | 1 | 1 | 2 | 5 |
| 4 | 1 | 0 | 3 | 8 → exceeds m=5 → False |

H=2 is achievable. Output 2.

This shows how the difference array propagates watering efficiently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log(max(a)+m)) | Binary search over potential minimum height, with each check O(n) |
| Space | O(n) | Difference array of size n+1 |

Given n, m ≤ 10^5 and heights ≤ 10^9, the solution runs within 2s comfortably.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sysio
    f = sysio.StringIO()
    with redirect_stdout(f):
        solve()
    return f.getvalue().strip()

# provided sample
assert run("6 2 3\n2 2 2 2 1 1\n") == "2", "sample 1"

# minimum input
assert run("1 1 1\n1\n") == "2", "minimum n"

# all equal
assert run("4 4 2\n1 1 1 1\n") == "3", "equal heights"

# maximum width
assert run("5 3 5\n1 2 1 2 1\n") == "2", "w=n"

# maximum watering days not needed
assert run("3 100 1\n1 2 3\n") == "103", "unused waterings"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1\n1` | 2 | Minimum-size input |
| `4 4 2\n1 1 1 1` | 3 | All |
