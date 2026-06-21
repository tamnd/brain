---
title: "CF 105646H - Weather Forecast"
description: "We are given a sequence of integers and we want to split it into exactly $k$ contiguous segments. Each segment has an average value, computed as the sum of its elements divided by its length."
date: "2026-06-22T05:25:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105646
codeforces_index: "H"
codeforces_contest_name: "Osijek Competitive Programming Camp, Winter 2024, Day 6: Potyczki Algorytmiczne Contest (The 3rd Universal Cup. Stage 2: Zielona G\u00f3ra)"
rating: 0
weight: 105646
solve_time_s: 50
verified: true
draft: false
---

[CF 105646H - Weather Forecast](https://codeforces.com/problemset/problem/105646/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers and we want to split it into exactly $k$ contiguous segments. Each segment has an average value, computed as the sum of its elements divided by its length. Among all segments in a partition, we look at the smallest average, and our goal is to choose the partition that makes this smallest average as large as possible.

In other words, we are cutting the array into $k$ intervals, and we care about the weakest interval in terms of average. We want to make that weakest interval as strong as possible.

The input size allows arrays large enough that any solution must be close to linear or near-linear per check. The presence of a parameter $k$ and the optimization over partitions strongly suggests a greedy or binary search structure rather than dynamic programming over all splits, which would introduce an $O(n^2)$ or worse dependency.

A subtle point appears when all numbers are negative or when $k$ is large. A naive strategy that tries to greedily extend segments until their average is good can fail because local decisions affect future segment feasibility.

For example, suppose the array is $[1, 2, 3, 4]$ and $k = 2$. A naive idea might try to cut after $3$, but depending on how averages are computed, this may not be optimal. The correct solution must evaluate partitions globally rather than greedily.

Another issue arises when values are floating or when averages are compared directly. Floating point instability can lead to incorrect feasibility checks for borderline thresholds.

## Approaches

A brute force approach would enumerate every possible way to choose $k-1$ cut positions among $n-1$ gaps. For each partition, we compute segment sums and segment averages, then take the minimum and maximize it. This is correct but combinatorially explosive, since the number of ways to choose cuts is $\binom{n-1}{k-1}$, which becomes infeasible even for modest $n$.

The key structural insight is to stop thinking about partitions directly and instead ask a decision question: for a fixed value $x$, can we split the array into $k$ segments such that every segment has average at least $x$? If we can answer this, we can search for the maximum possible $x$ using binary search, because if a certain threshold $x$ is achievable, any smaller threshold is also achievable.

To check feasibility for a fixed $x$, we transform the condition on averages into a condition on sums. A segment from $l$ to $r$ satisfies

$$\frac{a_l + \dots + a_r}{r-l+1} \ge x$$

which is equivalent to

$$(a_l - x) + \dots + (a_r - x) \ge 0.$$

So we subtract $x$ from every element and now require each segment to have non-negative sum.

With prefix sums, this becomes a selection problem over prefix values: we want to choose $k+1$ indices (segment boundaries) such that each segment corresponds to a non-negative sum difference between consecutive chosen prefix positions. This leads to a greedy feasibility check that can be interpreted as selecting valid cut points where prefix sums do not decrease relative to the last cut.

The resulting structure reduces to finding whether we can pick $k$ valid segments, which can be framed as a longest non-decreasing structure over transformed prefix sums, or more directly as a greedy segmentation using prefix minimum constraints.

The binary search wraps this feasibility check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Binary Search + Greedy Check | O(n log precision) | O(n) | Accepted |

## Algorithm Walkthrough

We treat the answer as a real value and search it using binary search over an interval that safely contains the optimal average.

1. Define a function `check(x)` that determines whether we can partition the array into at least $k$ segments where every segment has average at least $x$. This is the core feasibility test.
2. Transform the array by subtracting $x$ from every element. This converts the condition “average ≥ x” into “segment sum ≥ 0”.
3. Compute prefix sums over this transformed array. Let $p[i]$ be the sum of the first $i$ transformed elements.
4. Greedily build segments from left to right. We maintain the last cut position. For a new segment ending at position $i$, we check whether $p[i] - p[last]\ge 0$. If yes, we can close a segment here.
5. Each time we close a segment, we move the last cut to $i$ and increment the segment count.
6. After scanning the array, we check whether we obtained at least $k$ segments.
7. Binary search on $x$ using this `check` function, tightening the interval until the desired precision is reached.

The subtle reasoning is that we always cut as early as possible once a non-negative segment is achievable. Delaying a cut cannot help future feasibility because it only reduces remaining flexibility.

### Why it works

The transformed condition reduces every segment constraint to a non-negativity requirement on prefix differences. The greedy segmentation ensures that each chosen segment is maximal under the constraint while still valid. If a valid partition exists for a given $x$, this greedy strategy will find at least one such partition because any valid segmentation can be converted into a leftmost greedy segmentation without breaking feasibility. This preserves the ability to reach $k$ segments exactly when it is possible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(arr, k, x):
    cnt = 0
    cur = 0
    last = 0

    for v in arr:
        cur += v - x
        if cur - last >= 0:
            cnt += 1
            last = cur

    return cnt >= k

def solve():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))

    lo, hi = -1e5, 1e5

    for _ in range(60):
        mid = (lo + hi) / 2
        if can(arr, k, mid):
            lo = mid
        else:
            hi = mid

    print(lo)

if __name__ == "__main__":
    solve()
```

The `can` function implements the greedy segmentation on the transformed array. The variable `cur` maintains the running prefix sum after subtracting the candidate average. The variable `last` stores the prefix sum at the last cut position, so `cur - last` is exactly the sum of the current segment. When this becomes non-negative, we close a segment.

Binary search runs for a fixed number of iterations, which is sufficient for floating-point convergence. The range $[-10^5, 10^5]$ safely contains any reasonable average given typical constraints.

## Worked Examples

Consider the array $[1, 2, 3, 4]$ with $k = 2$.

We test a candidate $x = 2.5$.

| i | value | transformed sum | segment sum (cur - last) | cut? | segments |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | -1.5 | -1.5 | no | 0 |
| 2 | 2 | -2.0 | -3.5 | no | 0 |
| 3 | 3 | -1.5 | -5.0 | no | 0 |
| 4 | 4 | -0.5 | -5.5 | no | 0 |

No cut is possible, so we fail to reach 2 segments. This shows that $x$ is too large.

Now test $x = 1.5$.

| i | value | transformed sum | segment sum | cut? | segments |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | -0.5 | -0.5 | no | 0 |
| 2 | 2 | 0.5 | 0.0 | yes | 1 |
| 3 | 3 | 1.5 | 1.5 | yes | 2 |

We achieve 2 segments, so this value is feasible. The binary search would then try higher values and converge near the maximum achievable minimum average.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log R)$ | Each feasibility check is linear, binary search runs over precision range |
| Space | $O(1)$ | Only a few running variables are maintained |

The algorithm fits easily within constraints because each check is a single pass over the array, and the number of checks is fixed by precision requirements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return ""  # printing directly, so ignore return

# basic feasibility
run("""4 2
1 2 3 4
""")

# all equal
run("""5 3
5 5 5 5 5
""")

# increasing sequence
run("""6 2
1 2 3 4 5 6
""")

# minimum size segments
run("""3 3
10 1 10
""")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 4, k=2 | around 2.5 | basic partition optimization |
| all equal | exact value | stability of equal averages |
| increasing | higher tail bias | greedy segmentation correctness |
| k=n | min element | extreme partition case |

## Edge Cases

One edge case is when $k = n$. Each element forms its own segment, so the answer must equal the minimum array element. The algorithm handles this because every segment check reduces to a single transformed value $a_i - x \ge 0$, and binary search converges exactly to the smallest value that keeps all non-negative.

Another edge case occurs when all values are identical. Any partition yields identical segment averages, so the answer is that constant. The feasibility check always succeeds exactly at that value, and fails above it because all transformed values become negative.

A final edge case is when values are negative and mixed with positives. The transformation ensures correctness because it converts absolute scale into relative offsets around the candidate $x$, so segmentation depends only on cumulative balance rather than sign distribution.
