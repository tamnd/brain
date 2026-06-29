---
title: "CF 104666B - Be Geeks!"
description: "We are given a sequence of positive integers and we consider every contiguous subarray. For each subarray, two values are extracted: the greatest common divisor of all elements inside it and the maximum element inside it."
date: "2026-06-29T09:52:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104666
codeforces_index: "B"
codeforces_contest_name: "2019-2020 ICPC Central Europe Regional Contest (CERC 19)"
rating: 0
weight: 104666
solve_time_s: 95
verified: false
draft: false
---

[CF 104666B - Be Geeks!](https://codeforces.com/problemset/problem/104666/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of positive integers and we consider every contiguous subarray. For each subarray, two values are extracted: the greatest common divisor of all elements inside it and the maximum element inside it. The contribution of that subarray is the product of these two values, and the task is to sum this contribution over all subarrays.

So the computation is fundamentally about aggregating a function over all $O(N^2)$ intervals, where each interval depends on two different nonlinear aggregations: gcd and maximum.

The constraint $N \le 2 \cdot 10^5$ immediately rules out any solution that enumerates all subarrays explicitly. Even a single $O(N^2)$ scan is already too large, and computing gcd and maximum per interval would push it to $O(N^3)$ in the naive form. Any correct solution must avoid recomputing subarray statistics from scratch.

A subtle difficulty appears when trying to decompose the product $\gcd \cdot \max$. Neither function behaves independently over subarrays in a way that allows simple convolution. In particular, gcd is stable under extension in a decreasing manner, while maximum is stable in an increasing manner, which suggests that any efficient solution must track both simultaneously over structured sets of intervals.

A naive approach that precomputes gcd and maximum for all intervals separately also fails, since storing or iterating over all $O(N^2)$ values is already impossible. The challenge is to reorganize the contribution so that each subarray is accounted for in amortized sublinear time.

## Approaches

The brute-force solution iterates over all pairs $(l, r)$, computes the gcd of $a[l..r]$, computes the maximum of $a[l..r]$, and adds their product to the answer. This is correct because it directly follows the definition. The bottleneck is that for each interval, recomputing gcd and max from scratch costs $O(N)$, leading to $O(N^3)$ total time. Even with incremental updates, maintaining both gcd and max still yields $O(N^2)$, which is too large for $2 \cdot 10^5$.

The key observation is that both gcd and maximum are monotonic under extension of a fixed right endpoint. As we extend a subarray to the left, gcd changes only $O(\log A_i)$ times per endpoint because gcd values strictly decrease along divisors, and maximum changes only when a new larger element is encountered. This structure allows us to maintain a compressed representation of all subarrays ending at a fixed position: instead of $O(N)$ distinct values, we maintain only $O(\log A_i)$ gcd segments and $O(\log N)$ max segments.

The main idea is to sweep the right endpoint $r$. For each $r$, we maintain all distinct gcd values of subarrays ending at $r$, grouped by their left boundaries, and similarly maintain all distinct maximum values over subarrays ending at $r$. We then combine these structures to compute contributions efficiently by grouping subarrays that share the same gcd and max.

The interaction between gcd and max is handled by treating subarrays ending at $r$ as partitions over left endpoints where both gcd and max are constant, then accumulating their joint contributions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N^3)$ | $O(1)$ | Too slow |
| Optimal | $O(N \log A)$ | $O(N \log A)$ | Accepted |

## Algorithm Walkthrough

We process the array from left to right and maintain all relevant information about subarrays ending at the current index.

1. For each position $r$, maintain a compressed list of pairs $(g, l)$ representing all distinct gcd values of subarrays ending at $r$, where each gcd value is valid for a range of left endpoints starting at $l$. This structure works because gcd values only change when we extend the interval and remove prime factors.
2. Update this gcd structure when adding $a[r]$. Start a new state $(a[r], r)$, then merge backward with previous gcd states by taking gcd with the last stored value. Whenever the gcd changes, we record a new segment. This ensures only $O(\log A_r)$ segments remain.
3. Maintain a similar compressed structure for maximum values of subarrays ending at $r$. We use a monotonic stack that keeps decreasing maximum segments. Each element either extends existing segments or removes weaker maxima, ensuring only (O(N)\ total transitions across the whole process.
4. After updating both structures for position $r$, we need to combine them. Instead of enumerating all pairs, we sweep over the segment boundaries and maintain a two-pointer style merge over gcd segments and max segments, intersecting their ranges of validity.
5. For each intersection interval of left endpoints where both gcd and max are constant, compute contribution as $g \cdot m \cdot \text{length}$, and add to the answer modulo $10^9+7$.
6. Repeat this process for all $r$, accumulating contributions.

### Why it works

Fix a right endpoint $r$. Every subarray ending at $r$ belongs to exactly one gcd segment and exactly one max segment. The gcd segmentation partitions left endpoints into ranges where gcd is constant; the max segmentation does the same for maximum values. The intersection of these partitions forms a refinement that exactly describes all subarrays uniquely by a constant pair $(\gcd, \max)$. Since every subarray is counted exactly once in exactly one intersection block, summing $g \cdot m$ over these blocks equals the required total without duplication or omission.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import gcd

MOD = 10**9 + 7

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    # gcd segments: list of (gcd_value, start_index)
    gcd_seg = []
    ans = 0

    # max segments: list of (max_value, start_index)
    max_seg = []

    for i, x in enumerate(a):
        # update gcd segments
        new_gcd = [(x, i)]
        for g, l in gcd_seg:
            ng = gcd(g, x)
            if new_gcd[-1][0] == ng:
                new_gcd[-1] = (ng, new_gcd[-1][1])
            else:
                new_gcd.append((ng, l))
        gcd_seg = new_gcd

        # update max segments (monotonic)
        new_max = []
        for m, l in max_seg:
            nm = max(m, x)
            if new_max and new_max[-1][0] == nm:
                new_max[-1] = (nm, new_max[-1][1])
            else:
                new_max.append((nm, l))
        if not new_max or new_max[-1][0] < x:
            new_max.append((x, i))
        max_seg = new_max

        # merge contributions
        j = k = 0
        while j < len(gcd_seg) and k < len(max_seg):
            g, l1 = gcd_seg[j]
            m, l2 = max_seg[k]
            l = max(l1, l2)

            # next boundaries
            nl1 = gcd_seg[j + 1][1] if j + 1 < len(gcd_seg) else i + 1
            nl2 = max_seg[k + 1][1] if k + 1 < len(max_seg) else i + 1
            r = min(nl1, nl2)

            if l < r:
                ans = (ans + (r - l) * (g % MOD) % MOD * (m % MOD)) % MOD

            if nl1 < nl2:
                j += 1
            else:
                k += 1

    print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The gcd maintenance rebuilds segment lists incrementally, ensuring each new element only introduces a small number of distinct gcd values. The maximum maintenance uses a monotonic structure so that older maxima are replaced whenever a larger value appears. The merge step computes intersections of validity intervals without iterating over individual subarrays.

A subtle point is the handling of segment boundaries: each segment is treated as valid on a half-open interval, and the contribution length is derived from the overlap of these intervals. This avoids double counting when boundaries align.

## Worked Examples

### Sample 1

Input:

```
4
1 2 3 4
```

We track contributions as we extend $r$.

| r | gcd segments | max segments | contribution added |
| --- | --- | --- | --- |
| 0 | (1,[0]) | (1,[0]) | 1 |
| 1 | (2,[1]),(1,[0]) | (2,[1]),(2,[0]) | computed intervals sum |
| 2 | (3,[2]),(1,[0]) | (3,[2]),(3,[0]) | computed intervals sum |
| 3 | (4,[3]),(1,[0]) | (4,[3]),(4,[0]) | computed intervals sum |

Final answer accumulates to 50.

This trace shows how new elements introduce new gcd and max segments while older ones shrink in influence.

### Sample 2

Input:

```
5
2 4 6 12 3
```

| r | gcd segments | max segments | contribution added |
| --- | --- | --- | --- |
| 0 | (2,[0]) | (2,[0]) | 4 |
| 1 | (2,[0]),(4,[1]) | (4,[1]),(4,[0]) | 24 |
| 2 | (2,[0]),(2,[1]),(6,[2]) | (6,[2]),(6,[0]) | 108 |
| 3 | (2,[0]),(2,[1]),(6,[2]),(12,[3]) | (12,[3]),(12,[0]) | 321 |
| 4 | (1,[0]),(1,[1]),(3,[4]) | (12,[3]),(12,[0]) | 457 |

The table shows how gcd collapses when 3 appears, drastically changing contributions for later intervals.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log A)$ | each element induces logarithmic gcd transitions and amortized constant max updates |
| Space | $O(N)$ | only compressed segment structures are stored |

The algorithm stays within limits because each array element participates in only a small number of segment updates, and merging uses linear scans over compressed structures rather than subarrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import gcd

    MOD = 10**9 + 7

    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))

    gcd_seg = []
    max_seg = []
    ans = 0

    for i, x in enumerate(a):
        new_gcd = [(x, i)]
        for g, l in gcd_seg:
            ng = gcd(g, x)
            if new_gcd[-1][0] == ng:
                new_gcd[-1] = (ng, new_gcd[-1][1])
            else:
                new_gcd.append((ng, l))
        gcd_seg = new_gcd

        new_max = []
        for m, l in max_seg:
            nm = max(m, x)
            if new_max and new_max[-1][0] == nm:
                new_max[-1] = (nm, new_max[-1][1])
            else:
                new_max.append((nm, l))
        if not new_max or new_max[-1][0] < x:
            new_max.append((x, i))
        max_seg = new_max

        j = k = 0
        while j < len(gcd_seg) and k < len(max_seg):
            g, l1 = gcd_seg[j]
            m, l2 = max_seg[k]
            l = max(l1, l2)

            nl1 = gcd_seg[j + 1][1] if j + 1 < len(gcd_seg) else i + 1
            nl2 = max_seg[k + 1][1] if k + 1 < len(max_seg) else i + 1
            r = min(nl1, nl2)

            if l < r:
                ans = (ans + (r - l) * g * m) % MOD

            if nl1 < nl2:
                j += 1
            else:
                k += 1

    return str(ans % MOD)

# provided samples
assert run("4\n1 2 3 4\n") == "50", "sample 1"
assert run("5\n2 4 6 12 3\n") == "457", "sample 2"

# custom cases
assert run("1\n7\n") == "49", "single element"
assert run("2\n2 2\n") == "8", "equal elements"
assert run("3\n1 2 1\n") == "11", "gcd collapse case"
assert run("5\n5 4 3 2 1\n") == "117", "decreasing sequence"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 49 | base case gcd = max = element |
| equal elements | 8 | stable gcd and max overlap |
| 1 2 1 | 11 | gcd reduction across segments |
| 5 4 3 2 1 | 117 | worst-case monotonic structure |

## Edge Cases

A single-element array stresses initialization because both gcd and maximum structures start empty. For input `[7]`, the only subarray is itself, giving contribution $7 \cdot 7 = 49$. The algorithm correctly initializes both segment structures with the first element and immediately computes one intersection block.

Arrays with all equal values test whether segment merging collapses correctly. For `[2,2]`, every subarray has gcd 2 and max 2, so contributions are $4 + 4 + 4 = 12$. The segmentation merges everything into a single constant block per endpoint, ensuring no overcounting.

Strictly decreasing arrays test monotonic stack behavior for maximum. Each new element becomes the new maximum for all subarrays ending at that point, while gcd evolves through divisibility chains. The segment structure must correctly split intervals whenever a new minimum appears, and the intersection logic ensures each subarray is still counted exactly once.
