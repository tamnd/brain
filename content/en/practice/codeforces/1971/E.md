---
title: "CF 1971E - Find the Car"
description: "We are given a car moving along a straight line from position 0 to position n. We know the exact times at which the car passes several checkpoints. These checkpoints are sorted by position: 0, a1, a2, ..., ak, and the corresponding times are also strictly increasing: 0, b1, b2, ."
date: "2026-06-08T17:21:49+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1971
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 944 (Div. 4)"
rating: 1500
weight: 1971
solve_time_s: 141
verified: true
draft: false
---

[CF 1971E - Find the Car](https://codeforces.com/problemset/problem/1971/E)

**Rating:** 1500  
**Tags:** binary search, math, sortings  
**Solve time:** 2m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a car moving along a straight line from position `0` to position `n`. We know the exact times at which the car passes several checkpoints. These checkpoints are sorted by position: `0, a1, a2, ..., ak`, and the corresponding times are also strictly increasing: `0, b1, b2, ..., bk`, with the final checkpoint at position `n`.

Between any two consecutive known checkpoints, the car moves at a constant speed. That means the motion is piecewise linear in time: position increases linearly with time inside each segment, but the speed can change at the boundaries of the given points.

For each query position `d`, we must compute the time when the car reaches `d`, and output the integer part of that time.

The main difficulty is that `n`, the coordinates, can be as large as 1e9, so we cannot simulate movement step by step. However, the number of known segments `k` is at most 1e5 per test, and the total across tests is also 1e5, so we can afford logarithmic or linear preprocessing per test case.

A naive mistake comes from misunderstanding how interpolation works between known points. The time is not proportional to index, but proportional to distance inside a segment.

For example, if we have points `(0, 0)` and `(10, 10)` and a query `d = 5`, the answer is `5`. But if we change the second point to `(10, 20)`, the speed doubles, so `d = 5` corresponds to time `10`. Any solution assuming constant global speed will fail.

Another subtle edge case is querying exactly at a known checkpoint. If `d = a[i]`, the answer must be exactly `b[i]`. Any interpolation formula must preserve boundary consistency.

Finally, queries can land before the first checkpoint after zero or inside any segment, so we must correctly locate the segment for each query.

## Approaches

A brute-force approach processes each query independently. For a query position `d`, we scan through the segments `[a[i], a[i+1]]`, find where `d` lies, and compute time using linear interpolation.

Inside a segment, if the car moves from `(a[i], b[i])` to `(a[i+1], b[i+1])`, then the speed is `(a[i+1] - a[i]) / (b[i+1] - b[i])`. We invert this to compute time at `d`:

```
t = b[i] + (d - a[i]) * (b[i+1] - b[i]) / (a[i+1] - a[i])
```

This is correct, but for each query we may scan up to `k` segments, making the complexity `O(kq)` per test case. With `k, q` up to 1e5, this becomes 1e10 operations in the worst case, which is too slow.

The key observation is that both `a` and `b` are sorted, and the mapping from position to time is monotonic and piecewise linear. Once we locate the correct segment for a query position `d`, the answer is deterministic. This reduces the problem to efficient segment location.

We can binary search on the `a` array to find the last checkpoint `a[i] ≤ d`. After that, we compute the answer using the interpolation formula in constant time.

Thus, each query becomes `O(log k)` instead of `O(k)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Scan | O(kq) | O(k) | Too slow |
| Binary Search + Interpolation | O(q log k) | O(k) | Accepted |

## Algorithm Walkthrough

We preprocess each test case by storing arrays `a` and `b`.

1. Read arrays `a` and `b` representing position-time checkpoints. These define a piecewise linear function from position to time.
2. For each query `d`, we locate the largest index `i` such that `a[i] ≤ d`. This identifies the segment containing `d` because the function is monotonic in position.
3. If `d` equals a checkpoint `a[i]`, we directly return `b[i]`. This avoids floating-point error and preserves exact values at known points.
4. Otherwise, we compute the fraction of distance traveled inside the segment:

the relative position inside the segment is `(d - a[i]) / (a[i+1] - a[i])`.
5. We map that fraction into time space using linear interpolation:

`t = b[i] + (d - a[i]) * (b[i+1] - b[i]) // (a[i+1] - a[i])`.

Integer division is used because the output requires the floor of the time.
6. Print the computed time.

### Why it works

Within each segment, position is a linear function of time because speed is constant. That implies the inverse mapping from position to time is also linear on the same interval. Since `a` is strictly increasing, every position `d` lies in exactly one segment, and binary search correctly identifies that segment. The interpolation formula exactly reconstructs the inverse linear function restricted to that segment, so the computed time matches the true continuous time and flooring it yields the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k, q = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        for _ in range(q):
            d = int(input())

            if d <= a[0]:
                if a[0] == 0:
                    print(0)
                else:
                    # segment from 0 to a[0]
                    dt = b[0] * d // a[0]
                    print(dt)
                continue

            if d >= a[-1]:
                print(b[-1])
                continue

            lo, hi = 0, k - 1
            while lo < hi:
                mid = (lo + hi) // 2
                if a[mid] <= d:
                    lo = mid + 1
                else:
                    hi = mid
            i = lo - 1

            if a[i] == d:
                print(b[i])
            else:
                dt = (b[i+1] - b[i]) * (d - a[i]) // (a[i+1] - a[i])
                print(b[i] + dt)

solve()
```

The implementation relies on binary search to find the correct segment efficiently. The edge case `d <= a[0]` is handled separately because the first segment starts at zero implicitly. For queries beyond the last checkpoint, the answer is directly `b[k-1]` since the car has already reached the destination.

The interpolation is done entirely with integers, and the multiplication is performed before division to preserve precision.

## Worked Examples

We trace a small constructed case:

Input:

```
n=10, k=2
a = [4, 10]
b = [4, 7]
queries: d = 6, 4, 2, 7
```

### Query trace

| d | segment index i | computation | result |
| --- | --- | --- | --- |
| 6 | 0 | 4 + (2 * 3 // 6) | 5 |
| 4 | 0 | exact match | 4 |
| 2 | before first | 2 * 4 // 4 | 2 |
| 7 | 0 | 4 + (3 * 3 // 6) | 5 |

The trace shows how different regions behave: inside segment interpolation, exact checkpoint hits, and extrapolation before the first known segment.

This confirms that binary search consistently selects the correct segment and that linear interpolation matches the motion model.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log k) per test case | each query uses binary search over checkpoints |
| Space | O(k) | storage for checkpoint arrays |

The total constraints sum to 1e5 over all test cases, so this complexity is easily fast enough. Each operation is logarithmic over at most 1e5 elements, keeping total operations within a few million.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from typing import List

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n, k, q = map(int, input().split())
            a = list(map(int, input().split()))
            b = list(map(int, input().split()))

            for _ in range(q):
                d = int(input())

                if d <= a[0]:
                    if a[0] == 0:
                        out.append("0")
                    else:
                        out.append(str(b[0] * d // a[0]))
                    continue

                if d >= a[-1]:
                    out.append(str(b[-1]))
                    continue

                lo, hi = 0, k - 1
                while lo < hi:
                    mid = (lo + hi) // 2
                    if a[mid] <= d:
                        lo = mid + 1
                    else:
                        hi = mid
                i = lo - 1

                if a[i] == d:
                    out.append(str(b[i]))
                else:
                    dt = (b[i+1] - b[i]) * (d - a[i]) // (a[i+1] - a[i])
                    out.append(str(b[i] + dt))

        return "\n".join(out)

    return solve()

# provided sample (abbreviated format check only)
assert run("1\n10 1 3\n10\n10\n0\n6\n7\n") == "0\n6\n7"

# custom: single segment linear
assert run("1\n10 1 3\n10\n10\n2\n5\n9\n") == "2\n5\n9"

# custom: two segments
assert run("1\n10 2 4\n4 10\n4 7\n6\n4\n2\n7\n") == "5\n4\n2\n5"

# custom: boundary
assert run("1\n100 1 2\n100\n100\n0\n100\n") == "0\n100"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single segment | linear mapping | basic interpolation correctness |
| two segments | mixed queries | segment switching |
| boundary | endpoints | correct handling of edges |

## Edge Cases

One important edge case is when the query lies before the first known checkpoint. In that region, we effectively interpolate from `(0, 0)` to `(a[0], b[0])`. For example, if `a[0] = 10` and `b[0] = 5`, then `d = 2` gives `t = 5 * 2 // 10 = 1`. The implementation explicitly handles this without entering binary search because there is no previous segment.

Another edge case is exact matching at a checkpoint. If `d = a[i]`, interpolation would still work numerically, but it risks rounding errors and unnecessary computation. Directly returning `b[i]` ensures correctness and avoids division artifacts.

A final edge case is querying beyond the last checkpoint. Since `a[k-1] = n`, any `d ≥ n` must return `b[k-1]`. The solution handles this directly, reflecting that the motion does not continue past the final known time point.
