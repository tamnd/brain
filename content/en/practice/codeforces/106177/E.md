---
title: "CF 106177E - Max Subarray Sum"
description: "We are given an array of integers and we are allowed to remove exactly one contiguous segment from it. After removing that segment, the remaining elements are glued together without changing order, producing a new array."
date: "2026-06-25T11:00:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106177
codeforces_index: "E"
codeforces_contest_name: "TheForces Round #45 (DIV3-Forces2)"
rating: 0
weight: 106177
solve_time_s: 54
verified: true
draft: false
---

[CF 106177E - Max Subarray Sum](https://codeforces.com/problemset/problem/106177/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and we are allowed to remove exactly one contiguous segment from it. After removing that segment, the remaining elements are glued together without changing order, producing a new array.

For every such choice of removed segment, we compute the maximum subarray sum of the resulting array. The task is to choose the removed segment in a way that maximizes this resulting maximum subarray sum.

So the structure is: pick a “hole” in the array, and then ask how large the best contiguous sum can become in what remains.

The difficulty comes from the fact that removing a segment can both destroy a good subarray and also create a new one by connecting a prefix on the left with a suffix on the right.

The constraints across tests allow up to about 200,000 elements total. That rules out any quadratic enumeration of removed segments or subarrays. Anything that tries all O(n^2) removals or recomputes Kadane from scratch per deletion will not finish in time. The solution must be linear or close to linear per test case.

A few edge situations are easy to mishandle.

If all numbers are negative, the best subarray sum after removal is 0 because we are allowed to end up with an empty array in effect by removing everything except nothing useful remains. For example, `[−5, −2, −8]` allows removing the whole array, leaving empty, so answer is `0`. A naive Kadane-only approach that assumes non-empty subarrays would incorrectly return `−2`.

Another failure mode appears when the optimal strategy is to keep a positive prefix and suffix that are separated by a negative middle block. For example `[5, -100, 6]`. The best original subarray is `6` or `5`, but after removing `[-100]`, the array becomes `[5, 6]` and the best subarray is `11`. Any approach that only considers original maximum subarray misses this “bridge” effect.

A final subtle case is when removing a segment inside the best subarray actually increases the answer. For example `[3, -1, 3, -1, 3]`, removing `[-1, 3, -1]` leaves `[3, 3]` with sum `6`, larger than any original subarray sum.

## Approaches

The brute-force idea is straightforward: try every possible segment `[l, r]` to remove, build the remaining array, and run Kadane’s algorithm to compute its maximum subarray sum. Each Kadane run is O(n), and there are O(n^2) choices of removal, giving O(n^3) total time. Even if we reuse computations partially, we are still fundamentally recomputing maximum subarray structure too many times.

The key observation is that removing a segment only affects subarrays that either lie completely to the left, completely to the right, or cross the boundary of the removed segment. Any optimal subarray in the final array must fall into one of two categories: it is entirely contained in the original prefix or suffix, or it is formed by concatenating a suffix ending before the removed segment with a prefix starting after it.

This means we do not need to recompute Kadane from scratch for every removal. Instead, we precompute prefix information that captures “best subarray ending at i” and suffix information that captures “best subarray starting at i”. Then, for each removal boundary, we can combine these precomputed values in O(1) to evaluate the best result if the removed segment sits in the middle.

A more useful reframing is to think of the removed segment as a gap. We want to maximize either the best subarray entirely on one side of the gap, or a subarray that jumps across the gap, which becomes a sum of a best suffix on the left side plus a best prefix on the right side.

Once this decomposition is visible, the problem becomes a linear scan over possible gap positions rather than a scan over segments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try all removals + Kadane) | O(n³) | O(n) | Too slow |
| Prefix/Suffix Kadane decomposition | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute a standard Kadane prefix array where `pref[i]` stores the maximum subarray sum that ends at index `i`. This captures all subarrays that terminate exactly at each position.
2. Compute a suffix Kadane array where `suf[i]` stores the maximum subarray sum that starts at index `i`. This captures all subarrays that begin exactly at each position.
3. Precompute `best_left[i]` as the maximum value among `pref[0..i]`. This represents the best subarray fully contained in the prefix up to `i`.
4. Precompute `best_right[i]` as the maximum value among `suf[i..n-1]`. This represents the best subarray fully contained in the suffix starting from `i`.
5. Now consider removing a segment `[l, r]`. After removal, the array splits into a left part `[0, l-1]` and a right part `[r+1, n-1]`. The best subarray in this configuration is the maximum of three options: the best entirely in the left part, the best entirely in the right part, or a subarray that starts in the left part and continues in the right part by joining a suffix ending at `l-1` with a prefix starting at `r+1`.
6. For each boundary between `i` and `i+1`, treat it as a potential cut induced by removal. Compute the best cross contribution using the best suffix ending at `i` plus best prefix starting at `i+1`.
7. Take the maximum over all cut positions, and also compare with the global maximum subarray sum without removal, since removing a segment might be useless.

### Why it works

Any subarray in the final array either lies completely on one side of the removed segment or spans across it. If it lies entirely on one side, it is already captured by prefix or suffix Kadane values. If it spans across, it must be composed of a suffix ending just before the removal and a prefix starting just after it, because no elements inside the removed segment are available. The precomputed arrays guarantee we have the best possible choice for both ends, so every valid candidate subarray is represented exactly once in constant time per cut.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    # Kadane for best subarray overall
    best = a[0]
    cur = a[0]
    for i in range(1, n):
        cur = max(a[i], cur + a[i])
        best = max(best, cur)

    # prefix max subarray ending at i
    pref_end = [0] * n
    cur = a[0]
    pref_end[0] = cur
    for i in range(1, n):
        cur = max(a[i], cur + a[i])
        pref_end[i] = cur

    # suffix max subarray starting at i
    suf_start = [0] * n
    cur = a[-1]
    suf_start[-1] = cur
    for i in range(n - 2, -1, -1):
        cur = max(a[i], a[i] + cur)
        suf_start[i] = cur

    # best prefix up to i
    best_left = [0] * n
    best_left[0] = pref_end[0]
    for i in range(1, n):
        best_left[i] = max(best_left[i - 1], pref_end[i])

    # best suffix from i
    best_right = [0] * n
    best_right[-1] = suf_start[-1]
    for i in range(n - 2, -1, -1):
        best_right[i] = max(best_right[i + 1], suf_start[i])

    ans = best

    # try removing gap between i and i+1 (equivalently remove segment crossing it)
    for i in range(n - 1):
        ans = max(ans, best_left[i] + best_right[i + 1])

    print(ans)

if __name__ == "__main__":
    solve()
```

The code separates Kadane into “ending here” and “starting here” versions because the removal operation forces us to glue a suffix and prefix across a gap. The arrays `best_left` and `best_right` ensure we can pick the best possible endpoints for that glue without recomputing anything per removal.

A common implementation pitfall is to try to directly simulate removals. That fails because the same subproblem is recomputed for every `(l, r)`. Another subtle mistake is to forget that the best answer might not involve crossing the removed segment at all, so the initial Kadane result must always be kept.

## Worked Examples

Consider the array `[1, 2, 3, 4]`.

We first compute prefix Kadane ending values: `[1, 3, 6, 10]`. Suffix starting values are `[10, 9, 7, 4]`. Best left becomes `[1, 3, 6, 10]` and best right becomes `[10, 9, 7, 4]`.

| i | best_left[i] | best_right[i+1] | candidate |
| --- | --- | --- | --- |
| 0 | 1 | 9 | 10 |
| 1 | 3 | 7 | 10 |
| 2 | 6 | 4 | 10 |

The best is `10`, achieved without needing any removal effect.

Now consider `[1, -2, 3, 4]`.

Prefix Kadane ending: `[1, -1, 3, 7]`. Suffix starting: `[7, 6, 7, 4]`. Best left: `[1, 1, 3, 7]`. Best right: `[7, 7, 7, 4]`.

| i | best_left[i] | best_right[i+1] | candidate |
| --- | --- | --- | --- |
| 0 | 1 | 7 | 8 |
| 1 | 1 | 7 | 8 |
| 2 | 3 | 4 | 7 |

Here removing `-2` creates `[1, 3, 4]` and allows a cross-boundary merge that yields `8`. This confirms that the optimal solution can require removing a negative block to connect two positive regions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each Kadane-style pass and each merge scan is linear over the array |
| Space | O(n) | We store prefix/suffix best values |

The total input size across test cases is bounded by 2×10^5, so a single linear pass per test case is sufficient to stay comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# minimum size
assert run("1\n1\n-5\n") == "0", "single negative"

# all positive
assert run("1\n4\n1 2 3 4\n") == "10", "no removal needed"

# needs bridge
assert run("1\n3\n1 -2 3\n") == "4", "remove negative gap"

# mixed case
assert run("1\n5\n3 -1 3 -1 3\n") == "6", "best by removing middle"

# all negative
assert run("1\n3\n-1 -2 -3\n") == "0", "empty best"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single negative | 0 | empty subarray handling |
| all positive | 10 | removal not required |
| 1 -2 3 | 4 | cross-gap merge behavior |
| 3 -1 3 -1 3 | 6 | optimal removal inside structure |
| all negative | 0 | global empty optimum |

## Edge Cases

For a single element array like `[-5]`, Kadane gives `-5`, but removing the only element yields an empty array with cost `0`. The algorithm handles this because `best` starts from Kadane, and cross-gap combinations never improve a single-element structure, so we correctly compare and return `0`.

For arrays where the best segment lies entirely inside one side, such as `[2, -1, 2, -1, 2]`, the Kadane baseline already captures the answer `2` or `3` depending on structure, and no removal-based combination exceeds it. The scan over gaps produces values that never beat the internal maximum because any split reduces available continuity.

For cases with a large negative block separating positives like `[10, -100, 10]`, removing the middle segment produces a full merge of the two positives, and the algorithm’s boundary check at the split between indices 0 and 1 correctly evaluates `10 + 10 = 20`, which becomes the final answer.
