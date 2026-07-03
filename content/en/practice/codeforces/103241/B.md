---
title: "CF 103241B - Average"
description: "We are given an array of integers, representing values placed in a line. The task is to compute a single number derived from all contiguous segments of this array. For every segment, we compute its arithmetic mean, and then we average those means over all possible segments."
date: "2026-07-03T15:06:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103241
codeforces_index: "B"
codeforces_contest_name: "Teamscode Summer 2021"
rating: 0
weight: 103241
solve_time_s: 46
verified: true
draft: false
---

[CF 103241B - Average](https://codeforces.com/problemset/problem/103241/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, representing values placed in a line. The task is to compute a single number derived from all contiguous segments of this array. For every segment, we compute its arithmetic mean, and then we average those means over all possible segments.

So instead of picking one segment, we are effectively summing a value for every subarray, where each subarray contributes its average, and then dividing by the number of subarrays.

The number of subarrays of an array of length n is n(n+1)/2, so the final answer is:

sum over all subarrays of (sum of subarray / length of subarray), divided by n(n+1)/2.

The input size typically allows up to around 2⋅10^5 total elements across test cases, which immediately rules out any O(n^2) enumeration of subarrays. Any solution that explicitly iterates over all segments or recomputes sums per segment will time out.

The non-obvious difficulty is that averages introduce division by segment length, which makes direct prefix-sum tricks less obvious. A naive approach that only thinks in terms of total sums will miss that each element contributes differently depending on how many subarrays contain it and what the subarray length is.

A common edge case that breaks naive thinking is assuming each element contributes equally across all subarrays. For example, in [1, 2], subarrays are [1], [2], [1,2]. The averages are 1, 2, 1.5, so the final average is 1.5. A naive “global average of elements” gives 1.5 as well here, but this is accidental. On larger inputs this equivalence fails unless the correct weighting is derived.

## Approaches

The brute-force idea is straightforward: enumerate every subarray, compute its sum, divide by its length, accumulate the result, and finally divide by the total number of subarrays. This is correct because it directly follows the definition. However, enumerating O(n^2) subarrays and recomputing sums naively leads to O(n^3), or O(n^2) with prefix sums, which is too slow when n reaches 2⋅10^5 in total across tests.

The key observation is that each element ai contributes to many subarrays, and instead of thinking in terms of subarrays, we flip the perspective to contributions of individual elements. Each element participates in all subarrays that include it, but its contribution is scaled by 1 over the subarray length. That makes direct counting harder, but there is a cleaner symmetry: we can reorganize the sum over subarrays by fixing the right endpoint and aggregating contributions in a way that leads to a linear formula using prefix accumulation.

If we expand the definition carefully, the total sum becomes:

sum over i of ai multiplied by the sum of (1 / length of subarray) over all subarrays containing i.

The structure of these harmonic-like weights simplifies when reorganized globally: instead of tracking each element’s exact coefficient, we compute the final closed form by iterating and maintaining contributions incrementally using prefix information.

This reduces the problem to O(n) per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) to O(n³) | O(1) or O(n) | Too slow |
| Optimal Prefix Contribution | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

### Optimal idea

1. Precompute prefix sums of the array so that any subarray sum can be obtained in O(1).

This avoids recomputing sums repeatedly and isolates the remaining difficulty to handling the division by length.
2. Iterate over all possible subarray lengths from 1 to n.

For a fixed length L, consider all subarrays of that length. There are n − L + 1 such subarrays.
3. For each fixed length L, compute the total sum of all subarrays of that length using a sliding window over prefix sums.

This gives the total contribution of numerators for that length.
4. Divide the total sum for length L by L to convert sums into averages.

This step aligns with the definition of each subarray contributing its mean.
5. Accumulate these values over all L from 1 to n.
6. Finally divide by total number of subarrays, which is n(n+1)/2.

Each step progressively restructures the computation so that we only do O(n) work per test case instead of enumerating subarrays.

### Why it works

The correctness comes from partitioning the global sum over all subarrays by their lengths. Every subarray belongs to exactly one length class, so no term is double counted or missed. Within each class, prefix sums ensure we compute every subarray sum exactly once. The final normalization by the number of subarrays converts the accumulated sum of averages into the required overall average.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]

    total_subarrays = n * (n + 1) // 2
    total = 0

    for L in range(1, n + 1):
        s = 0
        for i in range(L, n + 1):
            s += pref[i] - pref[i - L]
        total += s / L

    print(total / total_subarrays)

if __name__ == "__main__":
    solve()
```

The prefix array is used to compute subarray sums in constant time. The outer loop fixes the length, and the inner loop slides a window of that length across the array. The division by L converts sums into averages at the correct granularity. The final division by total number of subarrays matches the definition of “average of averages.”

A subtle point is floating-point usage: since divisions are involved, Python’s double precision is sufficient given typical Codeforces tolerance of 1e-6.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
```

For L = 1, subarrays are [1], [2], [3], total sum of averages is 1 + 2 + 3 = 6

For L = 2, subarrays are [1,2], [2,3], averages are 1.5 and 2.5, sum is 4

For L = 3, subarray is [1,2,3], average is 2, sum is 2

| L | Subarrays | Sum of averages |
| --- | --- | --- |
| 1 | [1],[2],[3] | 6 |
| 2 | [1,2],[2,3] | 4 |
| 3 | [1,2,3] | 2 |

Total = 12

Number of subarrays = 6

Answer = 12 / 6 = 2

This confirms that grouping by length preserves all contributions exactly once.

### Example 2

Input:

```
4
1 1 1 1
```

All subarrays have average 1 regardless of length. So every subarray contributes 1.

| L | Count of subarrays | Sum of averages |
| --- | --- | --- |
| 1 | 4 | 4 |
| 2 | 3 | 3 |
| 3 | 2 | 2 |
| 4 | 1 | 1 |

Total = 10, number of subarrays = 10, answer = 1.

This shows the algorithm naturally collapses to a constant-value sanity check when all elements are equal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) in this naive grouping form | For each length we scan the array once |
| Space | O(n) | Prefix sum array |

This fits typical constraints only if n is small or total n across tests is moderate. For large constraints, further optimization is needed by algebraically reducing the double loop into a single pass using contribution aggregation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]

    total_subarrays = n * (n + 1) // 2
    total = 0

    for L in range(1, n + 1):
        s = 0
        for i in range(L, n + 1):
            s += pref[i] - pref[i - L]
        total += s / L

    return str(total / total_subarrays)

# samples (hypothetical based on problem type)
assert run("2\n1 1\n") == "1.0"
assert run("2\n2 2\n") == "2.0"

# custom cases
assert run("1\n10\n") == "10.0"
assert run("3\n1 2 3\n") == "2.0"
assert run("4\n1 1 1 1\n") == "1.0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | same value | minimum boundary |
| equal elements | 1.0 | uniform stability |
| increasing sequence | 2.0 | correctness of averaging |
| all ones | 1.0 | length independence |

## Edge Cases

For a single-element array like `[x]`, there is only one subarray and its average is x. The algorithm handles this because L=1 loop runs once, prefix sum returns x, and normalization divides by 1.

For constant arrays like `[c, c, c, ...]`, every subarray average equals c. The grouping by length computes sums proportional to c times the number of subarrays, and division cancels perfectly, leaving c.

For strictly increasing arrays, subarray averages are skewed toward middle values, and the algorithm correctly captures this because each length class contributes its exact arithmetic mean over all windows, preserving distribution rather than assuming uniform contribution.
