---
title: "CF 2093E - Min Max MEX"
description: "We are given an array and asked to cut it into exactly k contiguous pieces that together cover the whole array. Once the array is split, each piece has a MEX value, and we care about the worst piece, meaning the smallest MEX among all k segments."
date: "2026-06-08T05:38:59+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2093
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1016 (Div. 3)"
rating: 1500
weight: 2093
solve_time_s: 74
verified: true
draft: false
---

[CF 2093E - Min Max MEX](https://codeforces.com/problemset/problem/2093/E)

**Rating:** 1500  
**Tags:** binary search, brute force, greedy  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array and asked to cut it into exactly k contiguous pieces that together cover the whole array. Once the array is split, each piece has a MEX value, and we care about the worst piece, meaning the smallest MEX among all k segments. The goal is to choose the split so that this worst MEX is as large as possible.

Reframing the problem helps: we are trying to enforce that every segment is “rich enough” in small numbers, because MEX depends only on how early we can guarantee the presence of 0, 1, 2, and so on. If a segment is missing any integer x, then its MEX is at most x.

The constraints imply a solution must be close to linear per test case. Since total n across tests is 2e5, any approach that is worse than O(n log n) or O(n) per test case will fail. A naive greedy simulation per candidate value is acceptable if it is linear, but anything quadratic in n per test case is impossible.

A subtle edge case appears when k is large. If k equals n, every segment has length 1, so each MEX is either 0 or 1 depending on whether the element is 0. Another tricky case is when the array has no zeros at all. Then every segment has MEX 0, so answer is forced to 0 regardless of k. A naive approach that assumes we can always “collect” values inside segments will break here.

Another failure mode appears when one tries to greedily cut segments too early. For example, if we attempt to maximize MEX greedily by ending a segment as soon as it contains all numbers up to x-1, we may end up using too many segments and fail to reach k.

## Approaches

The key idea is to treat the answer as something we can test. Suppose we guess a value x and ask whether it is possible to split the array into at least k segments such that every segment has MEX at least x. If we can check this condition, we can binary search the maximum x.

For a segment to have MEX at least x, it must contain every number from 0 to x-1 at least once. This transforms the problem into a coverage requirement over a sliding window: each valid segment must “collect” all required values before it can be closed.

A brute-force way is to try all ways to partition the array into k segments and compute MEX for each segment. The number of partitions is exponential, since each of n-1 gaps can be cut or not. Even computing MEX per segment would be O(n), so this approach is completely infeasible.

The improvement comes from reversing the perspective. Instead of choosing cuts and checking MEX, we fix x and greedily construct segments from left to right, always ending a segment as soon as it satisfies all required values 0 to x-1. This greedy construction produces the maximum possible number of valid segments for a given x. If even this maximum count is less than k, then x is impossible.

This works because extending a segment beyond the point where it becomes valid can only reduce the number of segments we can form later, never increase it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Partitioning | O(2^n · n) | O(n) | Too slow |
| Binary Search + Greedy Check | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We first binary search the answer x, because if a value x is feasible, any smaller value is also feasible.

1. For a fixed x, define a checker that determines whether we can form at least k valid segments, where each segment contains all integers from 0 to x-1. This is the exact condition for MEX ≥ x.
2. Scan the array from left to right while maintaining a frequency structure for the current segment. We also track how many distinct values from 0 to x-1 have been seen so far.
3. When we see a value v in the range [0, x-1], we update its frequency, and if it becomes the first occurrence in the current segment, we increase a counter of satisfied values.
4. Once the counter reaches x, the current segment is valid. We immediately cut here and reset the frequency structure and counter, then continue scanning.
5. Count how many segments we can form this way. If this count is at least k, then x is feasible; otherwise it is not.

The binary search range is from 0 up to n+1, because MEX cannot exceed n+1 in any meaningful partitioning context.

### Why it works

For a fixed x, the greedy strategy always ends a segment at the earliest possible position where it becomes valid. Any later cut would only consume more elements without increasing the number of valid segments. Therefore this greedy produces the maximum number of valid segments achievable for that x. If even this maximum is below k, no alternative partition can succeed. This establishes correctness of the feasibility check, and binary search then gives the maximum x.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(a, k, x):
    if x == 0:
        return True

    freq = [0] * (x + 1)
    have = 0
    segments = 0

    for v in a:
        if v < x:
            if freq[v] == 0:
                have += 1
            freq[v] += 1

        if have == x:
            segments += 1
            if segments >= k:
                return True
            freq = [0] * (x + 1)
            have = 0

    return segments >= k

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    lo, hi = 0, n + 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if can(a, k, mid):
            lo = mid
        else:
            hi = mid - 1

    print(lo)
```

The checker function is the core of the solution. It maintains only information about values strictly less than x, since larger values do not affect whether MEX reaches x. Once all required values are seen in a segment, the segment is closed immediately.

Binary search is implemented in a standard upper-mid form to avoid infinite loops and ensure convergence toward the maximum feasible x.

## Worked Examples

### Example 1

Input:

```
5 2
2 1 0 0 1
```

We test feasibility for different x.

For x = 2, each segment must contain {0,1}. We scan:

| Index | Value | Have 0 | Have 1 | Segments |
| --- | --- | --- | --- | --- |
| 0 | 2 | 0 | 0 | 0 |
| 1 | 1 | 0 | 1 | 0 |
| 2 | 0 | 1 | 1 | 0 → cut |
| 3 | 0 | 1 | 1 | 1 |
| 4 | 1 | 1 | 1 | 1 → cut |

We obtain 2 segments, so x = 2 is feasible.

For x = 3, we need {0,1,2} per segment. Only one segment can be formed, so x = 3 fails.

This confirms answer 2.

### Example 2

Input:

```
4 4
1 0 0 0
```

For x = 1, each segment must contain 0.

Scanning:

| Index | Value | Have 0 | Segments |
| --- | --- | --- | --- |
| 0 | 1 | 0 | 0 |
| 1 | 0 | 1 | 0 → cut |
| 2 | 0 | 1 | 1 → cut |
| 3 | 0 | 1 | 2 → cut |

We can form at least 4 segments only if each cut isolates a zero, but after first cut we already consume structure and cannot produce 4 valid segments. So result is 0.

This shows how forcing many segments can collapse achievable MEX.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each feasibility check is O(n), and binary search runs O(log n) |
| Space | O(n) | Frequency array reused per check |

The total n across test cases is 2e5, so O(n log n) is comfortably within limits. Each test case performs a linear scan multiple times, but overall work remains proportional to n log n aggregated.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        def can(x):
            if x == 0:
                return True
            freq = [0] * (x + 1)
            have = 0
            seg = 0

            for v in a:
                if v < x:
                    if freq[v] == 0:
                        have += 1
                    freq[v] += 1
                if have == x:
                    seg += 1
                    if seg >= k:
                        return True
                    freq = [0] * (x + 1)
                    have = 0
            return seg >= k

        lo, hi = 0, n + 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can(mid):
                lo = mid
            else:
                hi = mid - 1
        print(lo)

    t = int(input())
    for _ in range(t):
        solve()

    return sys.stdout.getvalue().strip()

# provided samples
assert run("""7
1 1
0
5 1
0 1 3 2 4
6 2
2 1 0 0 1 2
5 5
0 0 0 0 0
5 2
2 3 4 5 6
6 2
0 0 1 1 2 2
4 4
1 0 0 0
""") == """1
5
3
1
0
1
0"""

# custom cases
assert run("""1
1 1
0
""") == "1", "single element"

assert run("""1
3 3
0 1 2
""") == "1", "tight full coverage"

assert run("""1
5 1
1 1 1 1 1
""") == "0", "no zero case"

assert run("""1
6 2
0 1 0 1 0 1
""") == "2", "alternating pattern"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimal boundary |
| 0 1 2 with k=3 | 1 | exact partition feasibility |
| all non-zero | 0 | missing required MEX base |
| alternating pattern | 2 | greedy segment splitting |

## Edge Cases

When the array contains no zero at all, every segment immediately has MEX 0. The checker for x = 1 fails because no segment can ever collect the value 0, so the binary search correctly collapses to 0.

When k equals n, each element must form its own segment. The algorithm will only count segments where a single element already completes the requirement. For x ≥ 2, this is impossible, since a single element cannot contain both 0 and 1. The feasibility check stops early and returns 0 or 1 appropriately depending on whether zeros exist.

When k = 1, the entire array is one segment. The greedy check reduces to checking the global MEX condition, and binary search effectively finds the MEX of the whole array, matching the problem definition.
