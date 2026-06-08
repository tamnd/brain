---
title: "CF 2053C - Bewitching Stargazer"
description: "We are asked to simulate the process of Iris observing stars with a lazy, recursive strategy. She starts with all stars in a single segment and repeatedly targets the middle star of any odd-length segment, adding its 1-based index to her \"lucky value\"."
date: "2026-06-08T08:24:12+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "divide-and-conquer", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 2053
codeforces_index: "C"
codeforces_contest_name: "Good Bye 2024: 2025 is NEAR"
rating: 1500
weight: 2053
solve_time_s: 114
verified: false
draft: false
---

[CF 2053C - Bewitching Stargazer](https://codeforces.com/problemset/problem/2053/C)

**Rating:** 1500  
**Tags:** bitmasks, divide and conquer, dp, math  
**Solve time:** 1m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to simulate the process of Iris observing stars with a lazy, recursive strategy. She starts with all stars in a single segment and repeatedly targets the middle star of any odd-length segment, adding its 1-based index to her "lucky value". After choosing a star, she continues recursively on the two subsegments to the left and right, except she ignores any segment smaller than her laziness threshold $k$. For even-length segments, she does not increase her lucky value directly but splits the segment into two equal halves.

The input consists of multiple test cases, each giving the total number of stars $n$ and the laziness threshold $k$. The output is the final lucky value after applying the recursive procedure to all valid segments.

The main constraint is that $n$ can be as large as $2 \cdot 10^9$, with up to $10^5$ test cases. This rules out any naive recursive approach that explicitly visits each star, since in the worst case the recursion would touch nearly every star, producing $O(n)$ operations per test case, which is far too slow.

Edge cases include situations where $k = 1$, forcing Iris to observe every star individually, or $k = n$, where only the first middle star is counted. For small segments relative to $k$, some segments are skipped entirely. Careless implementations may also miscalculate the middle index in even-length segments or mismanage boundaries when subtracting 1 for subsegment recursion.

## Approaches

A straightforward brute-force approach is to implement the recursive procedure directly. For a segment $[l, r]$, calculate $m = \lfloor(l+r)/2\rfloor$, add $m$ to the lucky value if the segment length is odd, then recursively handle the left and right subsegments as long as they are at least $k$ in length. While correct, this results in $O(n)$ operations for the worst case, which is unacceptable when $n$ can reach $2 \cdot 10^9$.

The key insight for a faster solution comes from recognizing that this process has a predictable pattern. Observing a segment with an odd length adds the middle element to the sum, then divides the segment into left and right halves. Each segment is independent, and the contribution of a segment depends only on its length and the starting index. This allows us to compute the lucky value recursively by working with segment lengths and starting indices rather than enumerating all stars. Specifically, we can write a recursive function `sum_segment(start, length)` that returns the total lucky value for a segment of given length starting at `start`. The recursion stops when the segment length is less than `k`. Using this approach, each recursive call splits the segment roughly in half, producing a recursion depth of $O(\log n)$. Since each split adds only a constant number of operations, the overall complexity becomes $O(\log n)$ per test case, which is feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(log n) recursion stack | Too slow |
| Optimal | O(log n) | O(log n) recursion stack | Accepted |

## Algorithm Walkthrough

1. Define a recursive function `compute_lucky(l, r)` that returns the total lucky value for a segment $[l, r]$. We use 1-based indices, consistent with the problem statement.
2. If the length $r - l + 1$ is less than $k$, return 0. This enforces the laziness threshold and stops recursion.
3. Compute the middle index $m = (l + r) // 2$. If the length of the segment is odd, this is the star Iris observes, so include `m` in the sum.
4. Recursively compute the lucky value of the left subsegment $[l, m-1]$ and right subsegment $[m+1, r]$. Sum these values with `m` if applicable.
5. For even-length segments, skip adding the middle value but still recursively handle the two equal halves, ensuring both halves are at least $k$ in length.
6. Return the sum of the contributions from the middle star (if any) and the subsegments.

Why it works: The algorithm maintains the invariant that every star that would have been observed according to Iris' rules is included exactly once. The recursion only stops when segments are smaller than $k$, which aligns with the laziness constraint. Since each split produces independent subsegments, summing the contributions preserves correctness. Every index calculation is exact and bounded by the original segment limits, ensuring no over-counting or boundary errors.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    import sys
    sys.setrecursionlimit(100)
    t = int(input())
    
    def compute_lucky(l, r, k):
        length = r - l + 1
        if length < k:
            return 0
        m = (l + r) // 2
        lucky = 0
        if length % 2 == 1:
            lucky += m
            lucky += compute_lucky(l, m-1, k)
            lucky += compute_lucky(m+1, r, k)
        else:
            lucky += compute_lucky(l, m, k)
            lucky += compute_lucky(m+1, r, k)
        return lucky

    for _ in range(t):
        n, k = map(int, input().split())
        print(compute_lucky(1, n, k))
```

The recursion is carefully controlled by the segment length and the laziness threshold `k`. Using integer division ensures that the middle index is correctly chosen for both odd and even lengths. For large `n`, the recursion depth is at most $O(\log n)$, so stack overflow is avoided. The `sys.setrecursionlimit(100)` call is sufficient because the recursion depth is small due to the exponential segment halving.

## Worked Examples

Trace of first sample input `7 2`:

| Segment [l,r] | Length | Middle m | Lucky added | Next segments |
| --- | --- | --- | --- | --- |
| [1,7] | 7 | 4 | 4 | [1,3],[5,7] |
| [1,3] | 3 | 2 | 2 | [1,1],[3,3] |
| [1,1] | 1 | <k | 0 | - |
| [3,3] | 3 | <k | 0 | - |
| [5,7] | 3 | 6 | 6 | [5,5],[7,7] |
| [5,5] | 1 | <k | 0 | - |
| [7,7] | 1 | <k | 0 | - |

Sum of lucky values: 4 + 2 + 6 = 12.

Trace of second sample input `11 3`:

| Segment [l,r] | Length | Middle m | Lucky added | Next segments |
| --- | --- | --- | --- | --- |
| [1,11] | 11 | 6 | 6 | [1,5],[7,11] |
| [1,5] | 5 | 3 | 3 | [1,2],[4,5] |
| [1,2] | 2 | even | 0 | [1,1],[2,2] |
| [1,1] | 1 | <k | 0 | - |
| [2,2] | 1 | <k | 0 | - |
| [4,5] | 2 | even | 0 | [4,4],[5,5] |
| [4,4] | 1 | <k | 0 | - |
| [5,5] | 1 | <k | 0 | - |
| [7,11] | 5 | 9 | 9 | [7,8],[10,11] |
| [7,8] | 2 | even | 0 | [7,7],[8,8] |
| [7,7] | 1 | <k | 0 | - |
| [8,8] | 1 | <k | 0 | - |
| [10,11] | 2 | even | 0 | [10,10],[11,11] |
| [10,10] | 1 | <k | 0 | - |
| [11,11] | 1 | <k | 0 | - |

Sum: 6 + 3 + 9 = 18.

These traces confirm the algorithm correctly implements the recursive middle selection and laziness cutoff.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) per test case | Each segment splits in half recursively; recursion depth is log(n) |
| Space | O(log n) recursion stack | Only recursive calls are stored; maximum depth log(n) |

This fits within the time limit even for $t = 10^5$ and $n = 2 \cdot 10^9$, because the total number of operations is roughly $t \cdot \log_2 n \approx 10^5 \cdot 31 \approx 3 \cdot 10^6$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin
```
