---
title: "CF 475D - CGCDSSQ"
description: "We are given a list of integers and a set of queries. Each query asks how many contiguous subarrays of the list have a greatest common divisor equal to the query value."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "math"]
categories: ["algorithms"]
codeforces_contest: 475
codeforces_index: "D"
codeforces_contest_name: "Bayan 2015 Contest Warm Up"
rating: 2000
weight: 475
solve_time_s: 71
verified: true
draft: false
---

[CF 475D - CGCDSSQ](https://codeforces.com/problemset/problem/475/D)

**Rating:** 2000  
**Tags:** brute force, data structures, math  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers and a set of queries. Each query asks how many contiguous subarrays of the list have a greatest common divisor equal to the query value. In simpler terms, for each number in the queries, we want to know how many stretches of consecutive elements in the array share that number as their largest shared divisor. For instance, if the array is `[2, 6, 3]` and the query is `2`, the subarrays `[2]` and `[2, 6]` have GCD equal to 2, giving a count of 2.

The array can have up to `10^5` elements, and the number of queries can reach `3 × 10^5`. Each element and each query can be as large as `10^9`. This combination of high `n` and high `q` immediately rules out any solution that considers every subarray individually. A naive approach would require examining O(n^2) subarrays, which with n = 10^5 results in roughly 5 × 10^9 operations, far exceeding a 2-second time limit. Each query also cannot be processed independently by rescanning the array, as that would multiply the work by q.

Non-obvious edge cases appear when elements are repeated, or when the GCD of long stretches reduces quickly. For example, in the array `[4, 8, 16]` and query `2`, naive scanning may miss subarrays like `[8, 16]` whose GCD is 8 rather than 2, or `[16]` whose GCD is 16. Another subtle case occurs when a query asks for a number that is not a divisor of any element; the answer should be 0, not a miscount of near matches.

## Approaches

The brute-force solution would iterate over all possible starting indices, then expand each subarray to the right, computing the GCD incrementally. For every expansion, we would check if the current GCD matches any query. This is correct because it literally counts every subarray, but the worst-case complexity is O(n^2), which fails for n up to 10^5.

The key insight to improve efficiency is that the GCD function is non-increasing when extending a subarray to the right. Once we know the GCD of a subarray ending at position i, extending it by including the next element will only reduce the GCD or leave it unchanged. This means we can maintain a mapping from possible GCDs to the number of subarrays ending at the current position. For each element, we take all previous GCDs, combine them with the current element using GCD, and aggregate counts. This dynamic programming approach produces all possible subarray GCDs in linear time relative to the number of unique GCD values seen at each step. The observation that the number of distinct GCDs at each step is bounded by O(log max(a_i)) ensures efficiency.

This approach converts an O(n^2) problem into something closer to O(n log A) where A is the maximum element. It also allows us to precompute counts for all possible GCDs, making query answering O(1) per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| GCD Aggregation | O(n log A + q) | O(n log A) | Accepted |

## Algorithm Walkthrough

1. Initialize a dictionary `count_gcd` to store cumulative counts of each GCD encountered across all subarrays. This will allow direct query answers after processing the array.
2. Initialize another dictionary `current_gcds` which maps a GCD value to the number of subarrays ending at the current element that have that GCD. Start empty.
3. Iterate over each element `a[i]` in the array. For each step, initialize `next_gcds` as an empty dictionary to store the new GCD counts for subarrays ending at `i`.
4. Include the subarray containing only `a[i]` itself. Set `next_gcds[a[i]] = 1`. This handles single-element subarrays.
5. For each GCD `g` in `current_gcds`, compute `gcd(g, a[i])` and increment `next_gcds[gcd(g, a[i])]` by the count `current_gcds[g]`. This updates counts for all extended subarrays.
6. Merge `next_gcds` into `count_gcd` by adding their counts. This keeps the total counts for every GCD encountered so far.
7. Replace `current_gcds` with `next_gcds` and continue to the next element.
8. After processing the entire array, each query `x` can be answered by looking up `count_gcd.get(x, 0)`.

Why it works: the algorithm maintains the invariant that `current_gcds` correctly counts the number of subarrays ending at the current index for each possible GCD. By iterating this over the array, all possible subarrays are accounted for exactly once. The non-increasing property of GCD ensures no subarray GCD is missed or double-counted.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
q = int(input())
queries = [int(input()) for _ in range(q)]

from collections import defaultdict

count_gcd = defaultdict(int)
current_gcds = {}

for num in a:
    next_gcds = defaultdict(int)
    next_gcds[num] += 1
    for g, cnt in current_gcds.items():
        new_g = math.gcd(g, num)
        next_gcds[new_g] += cnt
    for g, cnt in next_gcds.items():
        count_gcd[g] += cnt
    current_gcds = next_gcds

for x in queries:
    print(count_gcd.get(x, 0))
```

The first block reads the input and prepares query storage. The `count_gcd` dictionary accumulates global counts while `current_gcds` keeps track of subarrays ending at the current position. Using `math.gcd` ensures correctness for every combination, and `defaultdict(int)` prevents KeyErrors. Incrementing counts rather than overwriting is critical to maintain correct counts for subarrays sharing the same GCD. The final loop prints results directly from the precomputed dictionary.

## Worked Examples

Consider the sample input `[2, 6, 3]` with queries `[1, 2, 3, 4, 6]`.

| Step | current_gcds | next_gcds | count_gcd |
| --- | --- | --- | --- |
| 2 | {} | {2:1} | {2:1} |
| 6 | {2:1} | {6:1, 2:1} | {2:2, 6:1} |
| 3 | {6:1, 2:1} | {3:2,1:1} | {2:2,6:1,3:2,1:1} |

This trace shows how each subarray ending at each position contributes to total GCD counts. The counts match expected answers for the queries: 1 maps to 1, 2 maps to 2, 3 maps to 2, 4 maps to 0, 6 maps to 1.

Another example: array `[4, 8, 16]` and query `[4,8,16,2]`.

| Step | current_gcds | next_gcds | count_gcd |
| --- | --- | --- | --- |
| 4 | {} | {4:1} | {4:1} |
| 8 | {4:1} | {8:1,4:1} | {4:2,8:1} |
| 16 | {8:1,4:1} | {16:1,8:1,4:1} | {4:3,8:2,16:1} |

All subarrays are correctly counted, including overlapping GCDs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log A + q) | At each element, we extend up to O(log A) distinct GCDs, with q queries accessed in O(1) each. |
| Space | O(n log A) | The dictionaries store counts of distinct GCDs seen so far; each can be O(log A) per element. |

With `n` up to 10^5 and `A` up to 10^9, log A ≈ 30, so roughly 3 × 10^6 operations, comfortably within 2 seconds.

## Test Cases

```python
import sys, io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())  # assume solution in solution.py
    return output.getvalue().strip()

# Provided sample
assert run("3\n2 6 3\n5\n1\n2\n3\n4\n6\n") == "1\n2\n2\n0\n1"

# Minimum-size input
assert run("1\n7\n3\n1\n7\n10\n") == "0\n1\n0"

# All-equal elements
assert run("3\n5 5 5
```
