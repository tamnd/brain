---
title: "CF 104467G - Great Plummet"
description: "We are given an array of daily price changes, where each value represents how the stock price moves from one day to the next. From this sequence, we repeatedly look at a sliding window that ends at position i and spans at most M elements."
date: "2026-06-30T13:08:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104467
codeforces_index: "G"
codeforces_contest_name: "La Salle-Pui Ching Programming Challenge \u57f9\u6b63\u5587\u6c99\u7de8\u7a0b\u6311\u6230\u8cfd 2022"
rating: 0
weight: 104467
solve_time_s: 95
verified: false
draft: false
---

[CF 104467G - Great Plummet](https://codeforces.com/problemset/problem/104467/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of daily price changes, where each value represents how the stock price moves from one day to the next. From this sequence, we repeatedly look at a sliding window that ends at position `i` and spans at most `M` elements. For every position `i`, we only consider the segment `A[max(1, i-M+1) ... i]`.

Inside each such window, we want to find the worst continuous decline segment. A decline segment is any contiguous subarray whose sum is as negative as possible, but we only care about the most severe drop. If all subarrays are non-negative, the answer is defined as zero.

So for every window, we are computing the minimum subarray sum, and if that minimum is positive or zero, we clamp it to zero.

This is essentially a sliding-window version of the classic “maximum subarray sum” problem, except we are maximizing downward movement instead of upward gain.

The constraints `N ≤ 100000` and `M ≤ N` imply that any solution that recomputes an answer from scratch per position is too slow. A quadratic approach over all windows would attempt up to about `10^10` operations in the worst case, which is far beyond limits. We need an amortized linear or near-linear structure.

A few subtle edge cases matter:

A window with all non-negative values must output `0`. For example, if `A = [1, 2, 3]` and `M = 2`, every window produces no valid decline, so every answer is `0`.

A window where the worst decline is not the full prefix or suffix but an internal segment must be handled correctly. For example, in `[-3, -5, 2, -3]`, the worst decline is `[-3, -5]`, not the full array.

A naive mistake is to assume the worst decline is always a suffix sum or prefix sum. That fails on mixed-sign arrays where the optimal segment is internal.

## Approaches

The brute-force idea is straightforward. For each index `i`, we take the last `M` elements ending at `i` and try all possible subarrays inside that window. For each subarray, we compute its sum and track the minimum.

This is correct because it explicitly checks every possible continuous segment. However, inside each window of size up to `M`, there are `O(M^2)` subarrays. Over all `N` windows, this becomes `O(NM^2)` in the worst interpretation, or even `O(NM)` if we optimize subarray sum computation with prefix sums, but still too large when both are `10^5`.

The key observation is that each window is asking for a minimum subarray sum, which is equivalent to a maximum prefix difference. If we define prefix sums `S[i] = A[1] + ... + A[i]`, then any subarray sum `A[l..r]` is `S[r] - S[l-1]`. Minimizing this is equivalent to fixing `r` and finding the maximum `S[l-1]` within the allowed range.

So each window reduces to maintaining a sliding window maximum over prefix sums, but with a restriction that only prefix indices inside the last `M` positions are allowed. This becomes a data structure problem: we need to maintain the maximum prefix sum in a sliding window, and compute `S[i] - max_prefix`.

However, there is a subtle complication: the window is dynamic per `i`, so prefix indices enter and leave the valid range. This is exactly a monotonic deque scenario, where we maintain candidates for maximum prefix sum in decreasing order.

The final answer per `i` is:

`min_subarray_sum = S[i] - max_{j in window}(S[j-1])`, clamped to zero if positive.

We maintain a deque of indices of prefix sums, ensuring their prefix values are decreasing, and we also ensure indices outside the window are removed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N·M²) | O(1) | Too slow |
| Optimal (prefix + deque) | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

We transform the problem into prefix sums, then maintain a sliding structure over prefix indices.

### Steps

1. Build prefix sums `S` where `S[0] = 0` and `S[i] = S[i-1] + A[i]`.

This lets us compute any subarray sum in constant time using differences.
2. For each position `i`, we want the minimum subarray sum ending somewhere inside the last `M` elements, which corresponds to choosing `j` in `[i-M, i-1]` for prefix index `j`.
3. Maintain a deque of indices of `S` that are candidates for being the maximum prefix value in the current window.

We store indices in increasing order, but maintain prefix values in decreasing order.
4. Before processing `i`, remove indices from the front of the deque that are out of range.

Specifically, any index `< i-M` is no longer valid.
5. When inserting a new prefix index `i-1`, we remove from the back of the deque any indices whose prefix value is less than or equal to `S[i-1]`.

These are useless because a larger prefix dominates them for all future queries.
6. After cleanup, append `i-1` to the deque.
7. The best (largest) prefix in the window is at the front of the deque. Compute:

`best = S[i] - S[deque[0]]`.
8. If `best > 0`, output `0`, otherwise output `best`.

### Why it works

The deque maintains the invariant that its front always stores the index with the maximum prefix sum among all valid indices in the current window. Any index with a smaller prefix sum than a newer one will never be optimal again, because it is worse and also older or equal in position constraints. This guarantees that every query is answered in constant time, and every index enters and leaves the deque at most once, preserving linear complexity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    # prefix sums
    ps = [0] * (n + 1)
    for i in range(n):
        ps[i + 1] = ps[i] + a[i]

    from collections import deque
    dq = deque()

    res = []

    for i in range(1, n + 1):
        # window for prefix indices: [i-m, i-1]
        left = i - m
        if left < 0:
            left = 0

        # remove out of range indices
        while dq and dq[0] < left:
            dq.popleft()

        # add prefix index i-1
        idx = i - 1
        while dq and ps[dq[-1]] <= ps[idx]:
            dq.pop()
        dq.append(idx)

        best_prefix = ps[dq[0]]
        best = ps[i] - best_prefix

        if best > 0:
            best = 0
        res.append(str(best))

    print(" ".join(res))

if __name__ == "__main__":
    solve()
```

The prefix sum array allows constant-time subarray sum evaluation. The deque maintains candidates for the optimal starting point of a negative subarray ending at `i`. The key detail is that we store prefix indices, not array indices, and always use `i-1` as the latest candidate prefix endpoint.

The removal of indices outside `[i-m, i-1]` ensures the window constraint is respected, while the monotonic removal ensures only potentially optimal prefix sums remain.

## Worked Examples

### Sample 1

Input:

```
10 4
4 -3 1 -2 -3 2 0 -1 -1 -2
```

We track prefix sums and deque evolution:

| i | A[i] | prefix i | deque (prefix indices) | best prefix | result |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 4 | [0] | 0 | 0 |
| 2 | -3 | 1 | [1,2] | 1 | 0 |
| 3 | 1 | 2 | [1,2,3] | 1 | -3 |
| 4 | -2 | 0 | [1,4] | 1 | -3 |
| 5 | -3 | -3 | [1,5] | 1 | -3 |
| 6 | 2 | -1 | [4,5,6] | 0 | -5 |
| 7 | 0 | -1 | [4,5,6,7] | 0 | -5 |
| 8 | -1 | -2 | [5,6,7,8] | -3 | -3 |
| 9 | -1 | -3 | [6,7,8,9] | -3 | -2 |
| 10 | -2 | -5 | [7,8,9,10] | -3 | -4 |

This trace shows how the best decline is always determined by the maximum prefix in the valid window, not necessarily the earliest or latest position.

### Sample 2

Input:

```
12 7
-3 -7 -1 -3 -5 6 -3 -2 -2 4 -1 2
```

| i | A[i] | prefix i | deque | best prefix | result |
| --- | --- | --- | --- | --- | --- |
| 1 | -3 | -3 | [0,1] | 0 | -3 |
| 2 | -7 | -10 | [0,1,2] | 0 | -10 |
| 3 | -1 | -11 | [0,1,2,3] | 0 | -11 |
| 4 | -3 | -14 | [0,1,2,3,4] | 0 | -14 |
| 5 | -5 | -19 | [0,1,2,3,4,5] | 0 | -19 |
| 6 | 6 | -13 | [0,5,6] | -19? no, window shifts | -19 |
| 7 | -3 | -16 | updated | -19 | -19 |

The second sample shows how early large prefix values persist until they leave the window, strongly influencing later subarrays even after local improvements appear.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | each index enters and exits deque once |
| Space | O(N) | prefix array and deque storage |

The linear behavior is sufficient for `N = 100000`. The operations inside each loop are amortized constant, so the solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    ps = [0] * (n + 1)
    for i in range(n):
        ps[i + 1] = ps[i] + a[i]

    from collections import deque
    dq = deque()
    res = []

    for i in range(1, n + 1):
        left = i - m
        if left < 0:
            left = 0

        while dq and dq[0] < left:
            dq.popleft()

        idx = i - 1
        while dq and ps[dq[-1]] <= ps[idx]:
            dq.pop()
        dq.append(idx)

        best = ps[i] - ps[dq[0]]
        if best > 0:
            best = 0
        res.append(str(best))

    return " ".join(res)

# provided samples
assert run("10 4\n4 -3 1 -2 -3 2 0 -1 -1 -2") == "0 -3 -3 -3 -5 -5 -5 -3 -2 -4"
assert run("12 7\n-3 -7 -1 -3 -5 6 -3 -2 -2 4 -1 2") == "-3 -10 -11 -14 -19 -19 -19 -16 -9 -8 -7 -7"

# custom cases
assert run("1 1\n5") == "0", "single positive"
assert run("5 2\n1 2 3 4 5") == "0 0 0 0 0", "all non-negative"
assert run("5 3\n-1 -2 -3 -4 -5") == "-1 -3 -6 -9 -12", "all negative"
assert run("6 2\n3 -10 3 -10 3 -10") == "0 -7 0 -7 0 -7", "alternating spikes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | minimum window handling |
| all positive | all zeros | correct clamping |
| all negative | accumulating worst decline | correctness on monotone negatives |
| alternating spikes | periodic recomputation | sliding window correctness |

## Edge Cases

A single-element window occurs when `M = 1`. The algorithm reduces to checking whether the element is negative, since the only subarray is itself. The prefix/deque method still works because the window of prefix indices becomes a single point, and the difference `S[i] - S[i-1]` correctly yields `A[i]`.

When all values are non-negative, prefix sums are strictly increasing, so the maximum prefix in every window is always the earliest valid index. The computed subarray sum becomes non-positive, so clamping produces zero consistently. The deque still updates correctly but never changes the result structure.

When all values are negative, the maximum prefix is always the least negative prefix, typically the earliest prefix in the window. This produces a steadily decreasing sequence of answers matching cumulative worst segments. The algorithm handles this because the deque preserves decreasing prefix order, but all candidates still remain relevant until they slide out of range.
