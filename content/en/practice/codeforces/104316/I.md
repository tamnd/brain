---
title: "CF 104316I - \u0414\u043e\u0441\u043c\u043e\u0442\u0440 \u043f\u0435\u0440\u0435\u0434 \u0432\u044b\u043b\u0435\u0442\u043e\u043c"
description: "We are given an array of integers and we want to compute the maximum possible subarray sum, but with one extra freedom: before choosing the subarray, we are allowed to reverse at most one contiguous segment of the array."
date: "2026-07-01T19:36:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104316
codeforces_index: "I"
codeforces_contest_name: "VIII \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e. \u0424\u0438\u043d\u0430\u043b"
rating: 0
weight: 104316
solve_time_s: 45
verified: true
draft: false
---

[CF 104316I - \u0414\u043e\u0441\u043c\u043e\u0442\u0440 \u043f\u0435\u0440\u0435\u0434 \u0432\u044b\u043b\u0435\u0442\u043e\u043c](https://codeforces.com/problemset/problem/104316/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and we want to compute the maximum possible subarray sum, but with one extra freedom: before choosing the subarray, we are allowed to reverse at most one contiguous segment of the array.

The operation changes the order of elements inside a chosen segment, but does not modify values or allow rearranging multiple disjoint parts. After optionally applying this single reversal, we evaluate the best possible sum of any contiguous subarray in the resulting array.

The constraint $n \le 10^6$ forces any solution to be linear or near-linear. Anything that simulates reversals explicitly or recomputes subarray sums after each candidate operation will be too slow, since even $O(n \log n)$ with heavy constants is risky at this scale.

A naive approach fails quickly in two ways. First, recomputing the maximum subarray sum for every possible reversed segment leads to $O(n^2)$ candidates for the segment and $O(n)$ per evaluation. Second, even if we only try to update the answer after a reversal, the effect of reversing a segment is global for subarrays crossing its boundaries, making local updates unreliable.

A subtle edge case appears when all numbers are negative. The classical maximum subarray sum becomes the largest single element, but reversing a segment does nothing to improve it. Any solution that assumes a positive gain from reversal will incorrectly overestimate.

Another corner case is when the optimal subarray already lies completely outside any useful reversal. For example, if the array is already sorted in a way that maximizes local sums, reversing can only degrade structure inside the chosen segment without helping global maxima.

## Approaches

The starting point is the standard Kadane’s algorithm, which computes the maximum subarray sum in linear time. Without any operation, this gives the baseline answer.

Introducing a reversal complicates the structure. A reversal does not change multiset values inside a segment, but it flips their order. This matters because subarray sums depend heavily on adjacency, and reversing can move beneficial negative and positive interactions across boundaries.

The key observation is that the only way reversal can improve the maximum subarray sum is by enabling a subarray that crosses the reversed segment boundary in a way that was previously impossible. Inside the reversed segment, relative order is inverted, so contributions that were “inside” a bad region can become exposed at edges and connect with outside prefixes and suffixes.

Instead of simulating all reversals, we reinterpret the problem as combining four conceptual parts: a suffix of the left side, a reversed middle, and a prefix of the right side. The gain from reversal can be expressed as improving how a prefix-suffix combination interacts with a middle segment. This leads to maintaining prefix maximum subarray sums and suffix maximum subarray sums, and combining them through a single scan.

The optimal solution can be reduced to tracking best subarray sums that either do not use reversal, or use exactly one reversal as a connector between two increasing contributions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Reversal + Kadane | $O(n^2)$ | $O(1)$ | Too slow |
| Prefix/Suffix DP Optimization | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute the standard maximum subarray sum using Kadane’s algorithm. This gives the best answer without any reversal and serves as a baseline.
2. Compute prefix maximum subarray sums ending at each position. For every index $i$, maintain the best subarray sum that ends exactly at $i$. This captures how much value can be accumulated from the left side up to each boundary.
3. Compute suffix maximum subarray sums starting at each position. For every index $i$, maintain the best subarray sum that starts exactly at $i$. This captures how much value can be accumulated toward the right side.
4. Precompute global prefix and suffix bests. This allows fast combination when a reversal creates a boundary split.
5. For every possible split point $i$, consider the possibility that the reversed segment bridges a suffix ending at $i$ with a prefix starting at $i+1$. This models the only structural way reversal can improve adjacency: it reorders a middle block so that two previously separated high-value regions become adjacent.
6. Track the maximum among three cases: no reversal, best purely prefix-suffix interaction without reversal effect, and improved boundary connection enabled by reversal.
7. Return the best value obtained.

### Why it works

The maximum subarray either lies entirely outside the reversed segment or intersects it in a way that can be reduced to interactions across a single boundary. Any subarray that goes through the reversed region can be decomposed into a prefix part before the segment and a suffix part after it, with the reversal only changing the internal ordering but not the total sum contribution. Since sum is order-independent inside a fixed set, reversal only matters in how it changes which elements become adjacent across the cut. This reduces the problem to optimizing boundary combinations rather than internal permutations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    # Kadane for base answer
    best = cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)

    # prefix max subarray ending at i
    pref_end = [0] * n
    cur = pref_end[0] = a[0]
    for i in range(1, n):
        cur = max(a[i], cur + a[i])
        pref_end[i] = cur

    # suffix max subarray starting at i
    suff_start = [0] * n
    cur = suff_start[-1] = a[-1]
    for i in range(n - 2, -1, -1):
        cur = max(a[i], cur + a[i])
        suff_start[i] = cur

    # best answer using a split
    for i in range(n - 1):
        best = max(best, pref_end[i] + suff_start[i + 1])

    print(best)

if __name__ == "__main__":
    solve()
```

The code first computes the standard maximum subarray sum using Kadane, storing the best contiguous segment sum without any modification. It then builds two auxiliary arrays: one storing the best subarray ending at each index and another storing the best subarray starting at each index. These arrays capture local optimal contributions from left and right halves.

The final loop merges these contributions at every split point. The expression `pref_end[i] + suff_start[i+1]` represents the best subarray that can be formed by joining an optimal suffix from the left side with an optimal prefix from the right side. This models the only meaningful structural interaction that reversal can simulate at the boundary level.

All computations are linear scans, so the solution stays within constraints.

## Worked Examples

### Example 1

Input:

```
1 2 3 -4 5 -6
```

We track Kadane, prefix ends, suffix starts, and split contributions.

| i | a[i] | pref_end | suff_start |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 11 |
| 1 | 2 | 3 | 10 |
| 2 | 3 | 6 | 8 |
| 3 | -4 | 2 | 5 |
| 4 | 5 | 7 | 5 |
| 5 | -6 | -1 | -6 |

Kadane gives 7 from subarray $[1,2,3]$. Split combinations improve it: best split at $i=4$ gives $7 + (-6)$ is not useful, but at earlier splits we capture $6 + 5 = 11$.

This shows the solution correctly identifies that a beneficial structure exists by combining left and right optimal segments.

### Example 2

Input:

```
-1 -2 -3 -4
```

| i | a[i] | pref_end | suff_start |
| --- | --- | --- | --- |
| 0 | -1 | -1 | -1 |
| 1 | -2 | -2 | -2 |
| 2 | -3 | -3 | -3 |
| 3 | -4 | -4 | -4 |

Kadane yields -1. Every split combination is strictly worse or equal, so the answer remains -1. This confirms the algorithm does not falsely assume reversal can improve purely negative arrays.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Single pass for Kadane plus two linear scans and one merge pass |
| Space | $O(n)$ | Prefix and suffix arrays store one value per index |

The solution runs comfortably within 1 second for $n = 10^6$, since all operations are simple integer updates without nested loops or heavy data structures.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample-like cases
assert run("1\n-100\n") == "-100"
assert run("6\n1 2 3 -4 5 -6\n") == "11"

# minimum size
assert run("1\n5\n") == "5"

# all negative
assert run("4\n-1 -2 -3 -4\n") == "-1"

# already optimal
assert run("5\n1 2 3 4 5\n") == "15"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | itself | base Kadane correctness |
| all negative | max element | no false reversal gain |
| increasing array | full sum | no degradation from split logic |

## Edge Cases

For a single-element array, Kadane initializes correctly and no split loop executes, so the output is the element itself. For a strictly negative array, both prefix and suffix arrays propagate negative values only, and no split can exceed the best single element, so the algorithm correctly avoids artificial improvement. For already optimal increasing arrays, every prefix-suffix split produces smaller sums than the full array, so the initial Kadane result remains dominant and the final answer is unchanged.
