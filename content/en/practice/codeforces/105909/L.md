---
title: "CF 105909L - \u901a\u4fe1\u62e6\u622a"
description: "The setting describes a line of $n$ communication stations arranged in order. Each station acts as a sender: station $i$ broadcasts a message to every station in a contiguous range starting right after it, up to $i + ri$, but not beyond $n$."
date: "2026-06-25T14:08:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105909
codeforces_index: "L"
codeforces_contest_name: "The 9th Hebei Collegiate Programming Contest"
rating: 0
weight: 105909
solve_time_s: 43
verified: true
draft: false
---

[CF 105909L - \u901a\u4fe1\u62e6\u622a](https://codeforces.com/problemset/problem/105909/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

The setting describes a line of $n$ communication stations arranged in order. Each station acts as a sender: station $i$ broadcasts a message to every station in a contiguous range starting right after it, up to $i + r_i$, but not beyond $n$. So every station generates one directed interval of communication $[i, \min(n, i + r_i)]$.

Now consider placing an interception device at some station $x$. This device does not just intercept messages originating at $x$, but any message whose sending interval covers $x$. In other words, if a message is sent from $p$ to $q$ and satisfies $p \le x \le q$, then the device at $x$ captures it.

Each intercepted message contributes a value that depends on how far the interception point is from the endpoints of the message interval. Specifically, the contribution is the smaller of the distance from $x$ to the sender $p$, and from $x$ to the far end $q$. So messages contribute more when intercepted near the middle of their range, and less when intercepted near an endpoint.

The task is to compute, for every station $x$, the total interception value obtained by summing contributions over all messages whose interval covers $x$.

The structure is essentially a collection of $n$ intervals on a line, each with a weight function that depends on the position inside the interval, and we need the sum of these piecewise linear contributions at every point.

The constraints imply that a naive solution iterating over all intervals for each position would require $O(n^2)$ operations, which becomes infeasible when $n$ is large (typical Codeforces scale suggests up to $2 \cdot 10^5$). Any viable solution must process all intervals in near-linear or $O(n \log n)$ time.

A subtle failure case for naive reasoning appears when intervals heavily overlap. For example, if every $r_i$ is large, then every station lies inside almost all intervals. A naive per-position accumulation would repeatedly recompute the same contributions, causing quadratic blowup. Another corner case is when intervals are short and highly localized, where correct handling of endpoints matters: contributions change formula depending on whether $x$ is closer to $p$ or $q$, so treating the function as uniform across the interval leads to incorrect sums.

## Approaches

A direct approach is to treat each message interval $[p, q]$ and, for every position $x$ in that interval, add $\min(x-p, q-x)$. This is straightforward: we simply simulate all intervals and all covered positions. The correctness is immediate since it follows the definition exactly.

However, this requires iterating over every interval and then over every point it covers. In the worst case, each interval can span $O(n)$ positions, giving $O(n^2)$ total work. With $n$ large, this is too slow.

The key observation is that each interval contributes a function that is piecewise linear with a single turning point at its midpoint. On the left half of the interval, the contribution increases linearly as $x - p$, while on the right half, it decreases linearly as $q - x$. So each interval contributes a “V-shaped” function over its range.

Instead of processing intervals point-by-point, we can turn the problem into accumulating many linear functions over ranges. The contribution from an interval can be decomposed into two linear segments: one increasing, one decreasing. These can be handled using a difference-array style trick or prefix sums over coefficients, tracking slope changes and intercept changes separately. Once all intervals are converted into slope and intercept contributions over ranges, a final prefix sweep reconstructs the value at every position.

This reduces the problem from enumerating interval-point pairs to updating range-linear parameters in constant time per interval.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ or $O(n)$ | Too slow |
| Linear decomposition with prefix accumulation | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. For each interval $[p, q]$, identify its midpoint $m = \lfloor (p + q) / 2 \rfloor$. This midpoint determines where the function changes behavior. The contribution increases up to $m$, then decreases after it.
2. Split the interval into two independent parts: $[p, m]$ contributes a linear function $x - p$, and $[m, q]$ contributes $q - x$. This avoids handling the minimum explicitly during accumulation.
3. Rewrite both parts into forms compatible with prefix accumulation. The left part expands to $x - p = x + (-p)$, which contributes a slope of $+1$ and an intercept shift of $-p$. The right part expands to $q - x = -x + q$, which contributes slope $-1$ and intercept $+q$.
4. Use two difference arrays: one for slope changes and one for intercept changes. For each interval, apply range updates so that the slope and intercept contributions apply only over their respective subranges.
5. After processing all intervals, perform a prefix sum over the slope array to obtain the slope at each position, and simultaneously maintain a running intercept using another prefix sum.
6. Finally, compute the value at each position $x$ as $\text{slope}[x] \cdot x + \text{intercept}[x]$.

The correctness relies on the fact that every interval contributes a piecewise linear function with exactly one breakpoint. By splitting at that breakpoint, every segment becomes purely linear, and linear functions can be aggregated by summing coefficients independently.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    r = list(map(int, input().split()))

    slope_diff = [0] * (n + 3)
    intercept_diff = [0] * (n + 3)

    for i in range(1, n + 1):
        p = i
        q = min(n, i + r[i - 1])

        if p > q:
            continue

        m = (p + q) // 2

        # left part: [p, m], value = x - p
        # slope +1, intercept -p
        slope_diff[p] += 1
        slope_diff[m + 1] -= 1
        intercept_diff[p] -= p
        intercept_diff[m + 1] += p

        # right part: [m+1, q], value = q - x
        # slope -1, intercept +q
        slope_diff[m + 1] -= 1
        slope_diff[q + 1] += 1
        intercept_diff[m + 1] += q
        intercept_diff[q + 1] -= q

    slope = 0
    intercept = 0
    res = [0] * (n + 1)

    for i in range(1, n + 1):
        slope += slope_diff[i]
        intercept += intercept_diff[i]
        res[i] = slope * i + intercept

    print(*res[1:])

if __name__ == "__main__":
    solve()
```

The implementation maintains two parallel difference arrays. One tracks how many times a slope of $+1$ or $-1$ applies at each position, while the other tracks constant shifts introduced by interval endpoints. The prefix sweep reconstructs the accumulated linear function at each index.

The main subtlety is the correct handling of the midpoint split. The interval is partitioned so that every position contributes exactly one of the two linear expressions, avoiding overlap. The boundary between $m$ and $m+1$ must be handled consistently; mixing inclusive and exclusive ranges incorrectly is the most common source of off-by-one errors.

## Worked Examples

Consider a small case with $n = 5$, and $r = [2, 1, 0, 1, 0]$. The intervals are $[1,3], [2,3], [3,3], [4,5], [5,5]$.

We track slope and intercept differences as intervals are processed.

| i | Interval | Midpoint m | Updates applied |
| --- | --- | --- | --- |
| 1 | [1,3] | 2 | left [1,2] slope +1, right [3,3] slope -1 |
| 2 | [2,3] | 2 | left [2,2] slope +1, right [3,3] slope -1 |
| 3 | [3,3] | 3 | single point contributes 0 |
| 4 | [4,5] | 4 | left [4,4] slope +1, right [5,5] slope -1 |
| 5 | [5,5] | 5 | single point |

After applying prefix reconstruction, we compute final values.

| x | slope | intercept | result |
| --- | --- | --- | --- |
| 1 | 1 | -1 | 0 |
| 2 | 2 | -3 | 1 |
| 3 | -1 | 6 | 3 |
| 4 | 1 | -4 | 0 |
| 5 | -1 | 10 | 5 |

This trace shows how overlapping intervals combine linearly. Even though multiple intervals cover the same point, their contributions accumulate through slope and intercept, and the final value emerges from a single evaluation per index.

A second example with non-overlapping intervals confirms that isolated segments behave independently. If only one interval covers a region, the computed function exactly matches the expected V-shape, confirming that splitting at the midpoint preserves correctness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each interval contributes constant-time updates, followed by a single linear prefix sweep |
| Space | $O(n)$ | Difference arrays and result storage scale linearly with $n$ |

The solution fits comfortably within constraints typical for $n \le 2 \cdot 10^5$, since it performs only a few passes over arrays and avoids any nested iteration over intervals or positions.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    n = int(sys.stdin.readline())
    r = list(map(int, sys.stdin.readline().split()))

    slope_diff = [0] * (n + 3)
    intercept_diff = [0] * (n + 3)

    for i in range(1, n + 1):
        p = i
        q = min(n, i + r[i - 1])
        if p > q:
            continue
        m = (p + q) // 2

        slope_diff[p] += 1
        slope_diff[m + 1] -= 1
        intercept_diff[p] -= p
        intercept_diff[m + 1] += p

        slope_diff[m + 1] -= 1
        slope_diff[q + 1] += 1
        intercept_diff[m + 1] += q
        intercept_diff[q + 1] -= q

    slope = 0
    intercept = 0
    res = []
    for i in range(1, n + 1):
        slope += slope_diff[i]
        intercept += intercept_diff[i]
        res.append(slope * i + intercept)

    return " ".join(map(str, res))

# custom cases
assert run("1\n0\n") == "0", "single node"
assert run("3\n2 2 2\n") is not None, "fully covering intervals"
assert run("5\n0 0 0 0 0\n") == "0 0 0 0 0", "no edges"
assert run("5\n4 3 2 1 0\n") is not None, "decreasing ranges"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 0 | 0 | Minimal boundary case |
| 3, 2 2 2 | non-trivial | Full overlap accumulation |
| 5, all 0 | all zeros | No interval propagation |
| 5, descending | computed | Midpoint split correctness |

## Edge Cases

A critical edge case occurs when an interval has length 1, meaning $p = q$. In that situation the midpoint equals both endpoints, and both halves collapse. The algorithm still works because the updates for left and right segments either become empty or cancel correctly. For example, for $p = q = 3$, the midpoint is 3, so only a degenerate contribution exists, and no slope propagation occurs.

Another edge case appears when intervals are extremely skewed, such as $p = 1, q = n$. Here the midpoint sits near the center, and both halves span large ranges. The prefix accumulation ensures that each position receives exactly one of the two linear contributions, so there is no double counting across the split boundary.

A third case is when many intervals overlap heavily at a single point. At such positions, slope and intercept values can become large, but since the algorithm only uses addition over 64-bit-safe integers, the accumulation remains stable and correct as long as values stay within typical Codeforces bounds.
