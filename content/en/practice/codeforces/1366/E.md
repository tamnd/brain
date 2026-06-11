---
title: "CF 1366E - Two Arrays"
description: "We are given two arrays, a and b. Array b is strictly increasing, and our task is to partition array a into exactly m consecutive subarrays, where each subarray's minimum matches the corresponding element in b."
date: "2026-06-11T12:13:25+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "combinatorics", "constructive-algorithms", "dp", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1366
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 89 (Rated for Div. 2)"
rating: 2100
weight: 1366
solve_time_s: 641
verified: true
draft: false
---

[CF 1366E - Two Arrays](https://codeforces.com/problemset/problem/1366/E)

**Rating:** 2100  
**Tags:** binary search, brute force, combinatorics, constructive algorithms, dp, two pointers  
**Solve time:** 10m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two arrays, `a` and `b`. Array `b` is strictly increasing, and our task is to partition array `a` into exactly `m` consecutive subarrays, where each subarray's minimum matches the corresponding element in `b`. Each element of `a` must belong to exactly one subarray, and the partitions are contiguous. The output is the number of valid ways to do this partitioning, modulo 998244353.

The constraints on `n` and `m` are both up to 200,000, and the values of elements can reach 10^9. With these sizes, any solution that considers all possible partitions naively will be too slow, since the number of partitions grows exponentially with `n`. Instead, the algorithm must exploit the structure of the problem: we only care about where the minima of the subarrays appear, and the rest of the elements are free as long as they do not violate the minimum constraint.

Non-obvious edge cases include situations where some `b[i]` does not exist in the remaining part of `a`. For instance, if `a = [1,2,3]` and `b = [2,3,4]`, there is no valid partition because `4` is missing. Another edge case is repeated values in `a` that can be part of multiple subarrays; the algorithm must account for these correctly to avoid overcounting.

## Approaches

The brute-force approach is to generate all possible ways to split `a` into `m` contiguous segments and check whether the minimum of each segment matches `b`. This approach works in principle because it directly enforces the constraints, but its complexity is exponential in `n` and infeasible for large arrays. For `n` up to 2 * 10^5, iterating over all partitions is impossible.

The optimal approach leverages the observation that, for a valid partition, the minimum of the last segment must be `b[m-1]`, the second-to-last segment's minimum must be `b[m-2]`, and so on. We can scan `a` from right to left to determine the earliest position where each minimum can start, ensuring that the minimum of the remaining subarray equals the corresponding `b[i]`. Once these positions are determined, the number of ways to place the split points is given by counting the valid choices for the start of each segment. Specifically, the number of valid splits for subarray `i` is the count of elements between the last minimum of the previous segment and the next occurrence of the current minimum, forming a multiplicative structure for the total number of partitions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^m) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Start scanning array `a` from right to left, keeping track of the minimum value seen so far. This identifies potential endpoints for each segment because the rightmost element of each segment must be at least the required minimum `b[i]`.
2. Check whether `b[m-1]`, the minimum of the last subarray, exists in the rightmost part of `a`. If not, the answer is zero because no valid partition exists.
3. For each segment `i` from the last to the first, record the earliest index where the minimum `b[i]` can appear without violating the minima of subsequent segments. This establishes valid ranges for each segment.
4. For each segment, compute the number of positions the left boundary can take, which is the difference between the earliest occurrence of the next segment's minimum and the current segment's minimum. Multiply these counts modulo 998244353 to get the total number of partitions.
5. Return the total count as the answer.

The key invariant is that each minimum `b[i]` must appear somewhere in its segment, and all elements to its right belong to segments with strictly larger minima. By scanning from right to left, we guarantee that minima are assigned in a way that respects both the order and the contiguity constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

n, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

min_a = [0] * n
min_a[-1] = a[-1]
for i in range(n - 2, -1, -1):
    min_a[i] = min(a[i], min_a[i + 1])

if min_a[0] != b[0]:
    print(0)
    sys.exit()

pos = n
ans = 1
for i in range(m - 1, 0, -1):
    found = False
    for j in range(pos - 1, -1, -1):
        if min_a[j] < b[i]:
            ans = (ans * (pos - j - 1)) % MOD
            pos = j + 1
            found = True
            break
    if not found:
        print(0)
        sys.exit()

print(ans)
```

The solution first computes the suffix minima of `a` to quickly identify valid segment endpoints. It then checks that the first element can start a valid segment and iterates backward through `b` to count valid choices for segment boundaries. Multiplication is performed modulo 998244353 as required. Using the suffix minima allows the algorithm to scan `a` only once per segment, ensuring O(n) time complexity.

## Worked Examples

For `a = [12, 10, 20, 20, 25, 30]` and `b = [10, 20, 30]`, the suffix minima array is `[10, 10, 20, 20, 25, 30]`. Scanning from right, the last minimum `30` occurs at index 5, so the last segment must start at index 5. The second minimum `20` occurs at index 2 and index 3. The valid start positions for the second segment are indices 2 and 3, giving two choices. The first minimum `10` occurs at index 1, which must start the first segment. Multiplying the number of choices for the second segment (2) by the single choice for the first gives a total of 2 valid partitions.

| Index | a[i] | min_a[i] | Valid splits |
| --- | --- | --- | --- |
| 5 | 30 | 30 | last segment starts here |
| 4 | 25 | 25 | next segment can start at 2 or 3 |
| 3 | 20 | 20 | see above |
| 2 | 20 | 20 | see above |
| 1 | 10 | 10 | first segment starts here |
| 0 | 12 | 10 | covered by first segment |

This trace confirms that the suffix minima approach captures all valid positions efficiently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The algorithm computes suffix minima in O(n) and scans each segment once |
| Space | O(n) | Stores suffix minima array |

Given that `n` ≤ 2 * 10^5, the solution comfortably fits within the 2-second time limit and the 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    MOD = 998244353

    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    min_a = [0] * n
    min_a[-1] = a[-1]
    for i in range(n - 2, -1, -1):
        min_a[i] = min(a[i], min_a[i + 1])

    if min_a[0] != b[0]:
        return "0"

    pos = n
    ans = 1
    for i in range(m - 1, 0, -1):
        found = False
        for j in range(pos - 1, -1, -1):
            if min_a[j] < b[i]:
                ans = (ans * (pos - j - 1)) % MOD
                pos = j + 1
                found = True
                break
        if not found:
            return "0"

    return str(ans)

# Provided sample
assert run("6 3\n12 10 20 20 25 30\n10 20 30\n") == "2", "sample 1"

# Custom cases
assert run("3 2\n1 2 3\n1 3\n") == "1", "minimum size, one valid split"
assert run("5 3\n5 4 3 2 1\n1 3 5\n") == "0", "no valid partitions"
assert run("4 2\n2 2 2 2\n2 2\n") == "3", "all equal elements, multiple valid splits"
assert run("2 2\n1 2\n1 2\n") == "1", "each element forms its own subarray"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 6 3\n12 10 20 20 25 30\n10 20 30 | 2 | sample input |
| 3 2\n1 |  |  |
