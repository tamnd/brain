---
title: "CF 104518F - Vacation"
description: "We are given a sequence of monthly sales values and a fixed window size $K$. For every contiguous segment of length $K$, we compute its average sales. Since all windows have the same length, comparing averages is equivalent to comparing sums."
date: "2026-06-30T10:38:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104518
codeforces_index: "F"
codeforces_contest_name: "UNICAMP Selection Contest 2023"
rating: 0
weight: 104518
solve_time_s: 60
verified: true
draft: false
---

[CF 104518F - Vacation](https://codeforces.com/problemset/problem/104518/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of monthly sales values and a fixed window size $K$. For every contiguous segment of length $K$, we compute its average sales. Since all windows have the same length, comparing averages is equivalent to comparing sums.

The task is to identify two positions: the earliest starting index of a window with the minimum sum, and the earliest starting index of a window with the maximum sum.

The key structure here is that we are not selecting a single best window by value alone, but also enforcing a tie-breaking rule based on earliest occurrence. That changes how we treat equal sums: we must not overwrite an earlier index when we see the same value again.

The constraints reach up to $10^5$ elements, which rules out recomputing sums for every window from scratch. A naive approach that sums each window independently would take $O(NK)$, which becomes too large when both $N$ and $K$ are big.

Edge cases arise when multiple windows share the same minimum or maximum sum. A careless implementation that updates indices on `<=` or `>=` instead of strict `<` or `>` will incorrectly pick later positions instead of the first occurrence.

Another subtle case is when $K = 1$. Then every element is its own window, and the answer reduces to the first occurrence of minimum and maximum array values.

## Approaches

The brute-force method computes the sum of every window by iterating over its $K$ elements. This is correct but repeats work heavily: each of the $N-K+1$ windows costs $O(K)$, leading to $O(NK)$. At $10^5$, this is far too slow.

The improvement comes from observing overlap. Adjacent windows share $K-1$ elements, so we can update the sum in constant time by subtracting the outgoing element and adding the incoming one. This sliding window technique reduces the complexity to linear time.

Once we have each window sum in $O(1)$, tracking minimum and maximum becomes a single pass with careful tie-breaking.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(NK)$ | $O(1)$ | Too slow |
| Sliding Window | $O(N)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We maintain the sum of the first window, then slide it across the array while updating minimum and maximum.

1. Compute the sum of the first $K$ elements. This initializes both the current window and the baseline for comparisons.
2. Set both best minimum and best maximum to this first sum, and record index 1 for both.
3. Move the window one step at a time from left to right.
4. For each step, update the current sum by subtracting the element leaving the window and adding the new element entering.
5. If the new sum is strictly smaller than the best minimum, update the minimum value and store the current index.
6. If the new sum is strictly larger than the best maximum, update the maximum value and store the current index.

The strict comparison is essential. If we use non-strict comparisons, we would overwrite earlier valid answers and violate the requirement of returning the first occurrence.

### Why it works

Every possible window is examined exactly once in order. The sliding sum ensures correctness of each window value, and monotonic updates ensure that only strictly better candidates replace the current best. Since we never overwrite on ties, the first occurrence is preserved by construction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    v = list(map(int, input().split()))

    window_sum = sum(v[:k])

    min_sum = window_sum
    max_sum = window_sum
    min_idx = 1
    max_idx = 1

    for i in range(k, n):
        window_sum += v[i] - v[i - k]
        start_idx = i - k + 2

        if window_sum < min_sum:
            min_sum = window_sum
            min_idx = start_idx

        if window_sum > max_sum:
            max_sum = window_sum
            max_idx = start_idx

    print(min_idx, max_idx)

if __name__ == "__main__":
    solve()
```

The implementation begins by reading the input and computing the first window sum explicitly. The loop then maintains the sliding window invariant. The index calculation `i - k + 2` converts a zero-based right endpoint into a one-based window start.

The comparisons use strict inequality to preserve the earliest occurrence requirement. This is the most common source of bugs in this problem: using `<=` or `>=` silently breaks correctness on ties.

## Worked Examples

### Example 1

Input:

```
5 2
1 1 1 2 3
```

We track the sliding window sums.

| Step | Window | Sum | Min | Max |
| --- | --- | --- | --- | --- |
| initial | (1,1) | 2 | 1 | 1 |
| i=2 | (1,1) | 2 | 1 | 1 |
| i=3 | (1,2) | 3 | 1 | 2 |
| i=4 | (2,3) | 5 | 1 | 4 |

The minimum occurs at index 1, maximum at index 4.

### Example 2

Input:

```
6 4
1000 1 2 3 4 100
```

| Step | Window | Sum | Min | Max |
| --- | --- | --- | --- | --- |
| initial | (1000,1,2,3) | 1006 | 2 | 2 |
| i=5 | (1,2,3,4) | 10 | 2 | 5 |
| i=6 | (2,3,4,100) | 109 | 2 | 6 |

Minimum starts at index 2, maximum at index 1.

These traces show that once a window sum is computed, it is never recomputed or reconsidered out of order, preserving correct tie-breaking.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | One initial sum and one pass over the array |
| Space | $O(1)$ | Only running sums and indices are stored |

The solution fits easily within constraints since even $2 \cdot 10^5$ operations are trivial in linear time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("5 2\n1 1 1 2 3\n") == "1 4"

# minimum window size
assert run("5 1\n5 4 3 2 1\n") == "5 1"

# all equal
assert run("4 2\n7 7 7 7\n") == "1 1"

# increasing sequence
assert run("5 3\n1 2 3 4 5\n") == "1 3"

# decreasing sequence
assert run("5 2\n5 4 3 2 1\n") == "4 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 1 1 | tie handling correctness |
| K=1 | last and first indices | boundary behavior |
| monotonic increasing | correct max at end | sliding correctness |
| monotonic decreasing | correct min at end | index updates |

## Edge Cases

When all windows have the same sum, the algorithm must preserve the first index for both minimum and maximum. This is guaranteed because updates only occur on strict improvement, so the initial index remains untouched.

When $K = 1$, each element is its own window. The sliding mechanism still works: each update replaces the previous sum with the new element, and comparisons correctly identify first occurrences of min and max values.

When all values are equal, every window sum is identical, so no update ever triggers. The output remains `(1, 1)`, which matches the requirement of first occurrence selection.
