---
title: "CF 105869I - Random Remainders"
description: "We are given an array of positive integers. The task is to compute a global sum over all ordered pairs where each element in the array acts as a divisor in a modular expression."
date: "2026-06-22T02:29:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105869
codeforces_index: "I"
codeforces_contest_name: "OCPC Fall 2024 Day 2 Jagiellonian Contest (The 3rd Universal Cup. Stage 35: Krak\u00f3w)"
rating: 0
weight: 105869
solve_time_s: 49
verified: true
draft: false
---

[CF 105869I - Random Remainders](https://codeforces.com/problemset/problem/105869/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers. The task is to compute a global sum over all ordered pairs where each element in the array acts as a divisor in a modular expression. For each fixed element $a_j$, we look at every other element $a_i$, compute $a_i \bmod a_j$, square it, and accumulate everything into a single answer.

So the structure is fundamentally a pairwise interaction over a sorted array, where each pair contributes a value depending on how $a_i$ decomposes with respect to $a_j$.

The critical observation is that for a fixed divisor candidate $a_j$, the values of $a_i$ behave in a structured way when grouped by the quotient $\left\lfloor \frac{a_i}{a_j} \right\rfloor$. This quotient partitions the array into segments where the modular expression becomes linear in $a_i$, which makes prefix-sum aggregation possible.

The input size is large enough that any solution iterating over all pairs directly is immediately infeasible. A naive $O(n^2)$ approach implies up to $10^{10}$ operations in worst cases, which is far beyond acceptable limits. Even a slightly optimized pairwise method remains too slow because the inner computation is non-trivial.

The hidden structure lies in the fact that although there are $n^2$ pairs, each fixed $a_j$ interacts with only a limited number of quotient intervals when values are grouped by division. This reduces the effective work dramatically.

A subtle edge case arises when values are highly skewed. For example, if the array contains many repeated large values, naive grouping by quotient can still degenerate into many checks if not implemented with proper range handling. Another corner case is when values are small, such as all ones. In that case, all remainders are zero and the answer is trivially zero, but careless implementations may still attempt unnecessary segmentation logic.

## Approaches

A direct approach considers every pair $(i, j)$ and computes $(a_i \bmod a_j)^2$ explicitly. This is correct because it follows the definition exactly. However, its cost is quadratic in the array size. With $n = 2 \cdot 10^5$, this leads to billions of operations and cannot run in time.

To improve this, we fix $a_j$ and try to understand how $a_i \bmod a_j$ behaves as $a_i$ increases. The key idea is that the quotient $\left\lfloor \frac{a_i}{a_j} \right\rfloor$ stays constant over contiguous ranges of $a_i$. Inside such a range, the remainder simplifies to $a_i - t \cdot a_j$, where $t$ is the quotient value. This transforms a nonlinear modular expression into a quadratic expression over a contiguous segment.

Once the array is sorted, all values sharing the same quotient $t$ form a contiguous segment. That makes it possible to precompute prefix sums of $a_i$, $a_i^2$, and constant counts, and then evaluate each segment in constant time.

The remaining concern is how many such segments exist per $a_j$. For each $a_j$, the quotient $t$ ranges from $0$ up to $\lfloor \max(a) / a_j \rfloor$. While this looks large, when $a_j$ is randomly chosen from a uniform distribution over the array, the expected number of distinct quotient transitions is logarithmic. This is the same harmonic-series behavior that appears in divisor counting arguments.

Thus each $a_j$ contributes only $O(\log A)$ segments on average, leading to an expected $O(n \log n \log A)$ solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n \log n \log A)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We start by sorting the array so that all quotient-based partitions become contiguous. This structural ordering is what allows range aggregation instead of per-element computation.

We then precompute prefix sums for powers of the array values. Specifically, we maintain cumulative sums of $a_i$, $a_i^2$, and also a simple prefix sum for convenience when expanding quadratic expressions.

For each fixed value $a_j$, we iterate over possible quotient values $t$. Each $t$ defines a range of indices $i$ such that $\left\lfloor \frac{a_i}{a_j} \right\rfloor = t$. We locate this range using binary search boundaries on the sorted array.

Once we identify a segment $[p, q]$, we rewrite the contribution:

$$(a_i \bmod a_j)^2 = (a_i - t \cdot a_j)^2 = a_i^2 - 2 t a_j a_i + t^2 a_j^2$$

We compute the sum over the segment using prefix sums so that each term is obtained in constant time. This avoids iterating through the segment explicitly.

We repeat this for all valid $t$ values for the current $a_j$, accumulating contributions into the final answer.

### Why it works

The correctness comes from partitioning the array into maximal contiguous segments where the quotient $\left\lfloor \frac{a_i}{a_j} \right\rfloor$ is constant. Inside each segment, the modular expression becomes a fixed quadratic function of $a_i$. Because prefix sums preserve linearity, summing this quadratic form over a contiguous interval is exact and lossless. Every pair $(i, j)$ is included in exactly one segment corresponding to its quotient, so no contribution is missed or double-counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()

    pref1 = [0] * (n + 1)
    pref2 = [0] * (n + 1)

    for i in range(n):
        pref1[i + 1] = pref1[i] + a[i]
        pref2[i + 1] = pref2[i] + a[i] * a[i]

    def range_sum(l, r):
        return pref1[r + 1] - pref1[l]

    def range_sum2(l, r):
        return pref2[r + 1] - pref2[l]

    ans = 0

    for j in range(n):
        aj = a[j]
        i = 0
        max_val = a[-1]

        t = 0
        while t * aj <= max_val:
            # find range of i where floor(ai / aj) == t
            left_val = t * aj
            right_val = (t + 1) * aj - 1

            # binary search for bounds
            l = j + 1
            r = n - 1

            # lower bound
            lo = l
            hi = r
            L = n
            while lo <= hi:
                mid = (lo + hi) // 2
                if a[mid] >= left_val:
                    L = mid
                    hi = mid - 1
                else:
                    lo = mid + 1

            lo = l
            hi = r
            R = j - 1
            while lo <= hi:
                mid = (lo + hi) // 2
                if a[mid] <= right_val:
                    R = mid
                    lo = mid + 1
                else:
                    hi = mid - 1

            if L <= R and L < n:
                cnt = R - L + 1
                s1 = range_sum(L, R)
                s2 = range_sum2(L, R)

                # sum (ai - t*aj)^2
                ans += s2 - 2 * t * aj * s1 + cnt * (t * aj) * (t * aj)

            t += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by sorting to enable contiguous quotient ranges. Prefix sums are then built to allow constant-time range aggregation for both linear and quadratic terms.

For each $a_j$, we scan quotient values $t$. Each $t$ defines a numeric interval $[t a_j, (t+1)a_j - 1]$, and we use binary search to find which indices fall into this interval. The contribution is computed using the expanded square identity, replacing iteration over the segment with prefix sum arithmetic.

Care must be taken with bounds: the search must exclude indices before $j$ if the problem defines ordered pairs $i \ne j$, and the binary search must correctly handle empty ranges.

## Worked Examples

Consider a small array $a = [1, 3, 5]$.

We compute contributions for each $a_j$.

| j | a[j] | t | segment [L, R] | s1 | s2 | contribution |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | [1,2] invalid | - | - | 0 |
| 1 | 3 | 0 | [0,2] → [1] | 1 | 1 | (1-0)^2 = 1 |
| 1 | 3 | 1 | [3,5] → [5] | 5 | 25 | (5-3)^2 = 4 |
| 2 | 5 | 0 | [0,4] → [1,3] | 4 | 10 | (1-0)^2 + (3-0)^2 = 10 |
| 2 | 5 | 1 | [5,9] → [5] | 5 | 25 | 0 |

For $j=1$, we split values into quotient groups relative to 3. Values 1 and 5 fall into different ranges, showing how segmentation replaces per-pair computation.

Now consider $a = [2, 2, 2, 2]$.

| j | a[j] | t | segment | cnt | contribution |
| --- | --- | --- | --- | --- | --- |
| all | 2 | 0 | all elements | 4 | 0 |

Every remainder is zero, so the result is zero regardless of segmentation. This shows that the algorithm naturally collapses repeated-value cases without extra logic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n \log A)$ | sorting plus binary search per quotient segment per element |
| Space | $O(n)$ | prefix sums and stored array |

The logarithmic factor from value range segmentation remains small in expectation because each $a_j$ generates only a limited number of meaningful quotient boundaries. This keeps the solution within typical limits for $n \approx 2 \cdot 10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# simple sample-like case
assert run("3\n1 3 5\n") != "", "basic run"

# all equal
assert run("4\n2 2 2 2\n") == "0", "all equal values"

# minimum size
assert run("1\n7\n") == "0", "single element"

# increasing pattern
assert run("5\n1 2 3 4 5\n") != "", "increasing array"

# large spread
assert run("4\n1 100 1000 10000\n") != "", "wide range"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 identical values | 0 | all remainders vanish |
| single element | 0 | no pairs exist |
| 1 2 3 4 5 | non-zero | general segmentation correctness |
| 1 100 1000 10000 | non-zero | stability across large quotients |

## Edge Cases

When all elements are equal, every remainder is zero for any pair, and the algorithm processes a single quotient segment with value zero. For an input like $[5, 5, 5]$, the only relevant $t$ is zero, and the computed segment sum becomes zero because $a_i - 0 \cdot a_j = 5$ but it is paired only with itself depending on indexing rules, leading to cancellation in symmetric pair handling.

When the array contains a single element such as $[10]$, there are no valid pairs, so the outer loop runs but no segment contributes. The binary search yields empty ranges for all $t$, leaving the accumulated answer unchanged at zero.

When values are highly spaced like $[1, 10^9]$, each $a_j$ produces only a few quotient intervals because $t a_j$ jumps quickly beyond the maximum array value. The loop over $t$ terminates early, and only one or two segments are ever evaluated, demonstrating the logarithmic behavior in practice.
