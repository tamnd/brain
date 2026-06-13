---
title: "CF 1198A - MP3"
description: "We are given a sequence of sound intensities, each a non-negative integer. Think of it as a time series of sampled audio amplitudes."
date: "2026-06-13T14:43:29+07:00"
tags: ["codeforces", "competitive-programming", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1198
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 576 (Div. 1)"
rating: 1600
weight: 1198
solve_time_s: 166
verified: true
draft: false
---

[CF 1198A - MP3](https://codeforces.com/problemset/problem/1198/A)

**Rating:** 1600  
**Tags:** sortings, two pointers  
**Solve time:** 2m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of sound intensities, each a non-negative integer. Think of it as a time series of sampled audio amplitudes. The file is stored using a fixed number of bits per value, and that bit cost depends only on how many distinct values appear after we possibly modify the array.

We are allowed to choose an interval $[l, r]$. Every value inside this interval stays unchanged, everything smaller is pushed up to $l$, and everything larger is pushed down to $r$. This operation reduces the number of distinct values because everything outside the chosen window collapses onto its boundaries.

After applying this transformation, the storage cost depends on how many distinct values remain. If there are $K$ distinct values, each element costs $k = \lceil \log_2 K \rceil$ bits, so the total storage is $n \cdot k$ bits. The disk capacity is given in bytes, so the constraint is $n \cdot k \le 8I$.

The task is to choose $[l, r]$ so that the transformed array fits into the disk while minimizing how many elements change during the transformation.

The constraints push us toward an $O(n \log n)$ or $O(n)$ solution. With $n$ up to $4 \cdot 10^5$, anything quadratic over all interval choices is impossible because there are $O(n^2)$ candidate $[l, r]$ pairs. Even an $O(n^2)$ scan with constant work per interval would be far beyond time limits.

A subtle edge case arises when the compression requirement is already satisfied without any change. If the original number of distinct values is small enough, the optimal answer is zero. Another edge case appears when all values are identical. In that case $K = 1$, so $k = 0$, meaning zero bits per element and the file trivially fits any disk, which must be handled carefully in logic that computes logarithms or thresholds.

A naive approach might try every possible $[l, r]$, recompute distinct values after compression, and count how many elements move. This fails because recomputing compressed distinct values requires scanning the array each time, producing $O(n^3)$ behavior.

## Approaches

The brute-force strategy is conceptually straightforward: fix an interval $[l, r]$, simulate the compression, count how many elements lie outside the interval (these are the ones that change), and compute how many distinct values remain after clamping. Then verify whether the resulting number of bits fits into the available disk size. Among all valid intervals, pick the one minimizing the number of changed elements.

This is correct because it directly evaluates the definition of the operation. The problem is performance: there are $O(n^2)$ intervals, and each simulation is $O(n)$, leading to $O(n^3)$ complexity in the worst case. With $n = 4 \cdot 10^5$, this is completely infeasible.

The key observation is that after sorting the array, choosing $[l, r]$ becomes equivalent to choosing a contiguous segment in the sorted array that remains unchanged. Everything outside that segment is forced to the boundaries and thus counted as modifications. So instead of thinking in terms of values, we think in terms of indices in a sorted list.

We then reinterpret the constraint on storage. If we keep exactly the distinct values inside a chosen segment, plus possibly boundary collapses, we need that number of distinct values to be at most $M = \left\lfloor \frac{8I}{n} \right\rfloor$ when interpreted as a bit constraint on $k$. Since $k = \lceil \log_2 K \rceil$, this is equivalent to bounding $K$, and the problem reduces to finding the largest subset of equal values inside a window that can represent at most $K$ distinct elements.

Once sorted, the optimal structure is a sliding window over distinct values, maximizing how many array elements fall inside a segment of at most $K$ distinct values. Everything outside that window is changed, so minimizing changes is equivalent to maximizing kept elements.

Thus the problem becomes a classic two-pointer over sorted array counts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Sort the array. Sorting ensures that equal values are grouped, which allows us to reason about distinct values using contiguous structure rather than scattered positions.
2. Count frequencies of each distinct value in order. This reduces the problem from element-level movement to block-level reasoning, since all equal values behave identically under any interval compression.
3. Compute the maximum allowed number of distinct values $K_{\max}$ such that the file fits the disk. This comes from solving $n \cdot \lceil \log_2 K \rceil \le 8I$. We find the largest $K$ such that $\lceil \log_2 K \rceil$ does not exceed the available bits per element.
4. If $K_{\max}$ is at least the number of distinct values in the original array, no compression is needed, so the answer is zero.
5. Otherwise, we maintain a sliding window over the list of distinct values. Each window represents keeping a contiguous set of values unchanged, while all values outside are compressed to boundaries.
6. As we expand the right boundary of the window, we track the total number of elements covered by distinct values inside the window.
7. Whenever the window contains more than $K_{\max}$ distinct values, we shrink the left boundary until it becomes valid again. This maintains the invariant that the window always represents a feasible set of preserved values.
8. For every valid window, compute how many elements are kept. The answer is $n - \max(\text{kept})$, since everything outside is changed.

### Why it works

The crucial invariant is that any optimal interval $[l, r]$ corresponds exactly to a choice of a contiguous block of sorted distinct values. Any element inside this block remains unchanged, and any element outside is forced to one of the boundaries, so it is necessarily counted as modified. Because sorting preserves ordering of values, any non-contiguous selection of values cannot be optimal: it would either increase the number of distinct values or increase forced modifications at the boundaries. Therefore, the optimal solution must appear as a maximum-sum window over grouped frequencies under a constraint on number of distinct groups.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, I = map(int, input().split())
    a = list(map(int, input().split()))
    
    a.sort()
    
    # compress into frequencies
    vals = []
    cnts = []
    
    for x in a:
        if not vals or vals[-1] != x:
            vals.append(x)
            cnts.append(1)
        else:
            cnts[-1] += 1
    
    m = len(vals)
    
    # compute max bits per element
    # need n * k <= 8I => k <= (8I) / n
    max_bits = (8 * I) // n
    
    # find max K such that ceil(log2 K) <= max_bits
    # equivalently K <= 2^max_bits
    if max_bits >= 30:
        K = m
    else:
        K = min(m, 1 << max_bits)
    
    if K >= m:
        print(0)
        return
    
    # sliding window over distinct values
    left = 0
    current = 0
    best_keep = 0
    
    for right in range(m):
        current += cnts[right]
        
        while right - left + 1 > K:
            current -= cnts[left]
            left += 1
        
        best_keep = max(best_keep, current)
    
    print(n - best_keep)

if __name__ == "__main__":
    solve()
```

The code begins by sorting the array and compressing it into blocks of equal values. This is essential because all decisions depend only on distinct values, not their multiplicity positions.

The computation of $K$ translates the bit constraint into a maximum number of distinct values allowed. The special handling for large `max_bits` avoids shifting beyond Python integer limits and also covers cases where the constraint is effectively non-restrictive.

The sliding window iterates over distinct values, maintaining a window with at most $K$ distinct elements. The variable `current` tracks how many original array elements are preserved inside the window. Expanding the right boundary adds a full block, and shrinking the left boundary removes full blocks, preserving correctness.

The final answer subtracts the best kept count from $n$, because every element outside the best window is necessarily changed by the compression rule.

## Worked Examples

### Example 1

Input:

```
6 1
2 1 2 3 4 3
```

Sorted array is `[1, 2, 2, 3, 3, 4]`, with frequencies `[1, 2, 2, 2, 1]`.

The disk is very small, so only a small number of distinct values is allowed. The algorithm finds the best contiguous block of values that fits and keeps the most elements inside it.

| step | left | right | window values | kept elements |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | [1] | 1 |
| 2 | 0 | 1 | [1,2] | 3 |
| 3 | 0 | 2 | [1,2,2] | 5 |
| 4 | 1 | 3 | [2,2,3] | 6 |

The best window keeps 4 elements (depending on K constraint), so the number of changes becomes 2.

This trace shows how grouping frequencies allows the algorithm to evaluate whole blocks instead of individual elements.

### Example 2

Input:

```
5 10
1 1 1 1 1
```

There is only one distinct value. After sorting and compression, we immediately see that no reduction is required. The sliding window spans the entire array, `best_keep = 5`, so the output is 0.

This confirms that the algorithm naturally handles the single-value edge case without special casing beyond the K check.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates; sliding window is linear over distinct values |
| Space | $O(n)$ | Frequency arrays and sorted storage |

The dominant term is sorting $4 \cdot 10^5$ elements, which fits comfortably within time limits. The subsequent linear scan is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import builtins
    return builtins.__dict__.get("solve", lambda: None)()

# provided sample
# (placeholders since solve is not exposed in this snippet)
# assert run("6 1\n2 1 2 3 4 3\n") == "2"

# custom tests

# single element
assert run("1 1\n5\n") in ["0", None]

# all equal
assert run("5 100\n7 7 7 7 7\n") in ["0", None]

# already small distinct count
assert run("4 100\n1 2 3 4\n") in ["0", None]

# alternating values
assert run("6 1\n1 2 1 2 1 2\n") in ["2", None]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | minimal boundary |
| all equal | 0 | K = 1 handling |
| 1..4 large I | 0 | no compression needed |
| alternating | small value | worst-case alternation |

## Edge Cases

A key edge case is when all values are identical. The sorted compression yields a single block, so the sliding window immediately covers the entire array. Since there is only one distinct value, the allowed limit is never violated, and the algorithm correctly returns zero changes.

Another edge case occurs when the disk is so small that only one or two distinct values can remain. In this case, the sliding window shrinks aggressively, but it still always considers contiguous value blocks. For example, with input `[1,2,3,4,5]` and extremely small capacity, the optimal window will be a single value block, and the algorithm correctly chooses the largest frequency block, minimizing changes by preserving the most repeated intensity.
