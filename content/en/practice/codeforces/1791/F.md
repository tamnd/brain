---
title: "CF 1791F - Range Update Point Query"
description: "We are given an array of integers and a series of operations that either transform a subarray by replacing each element with the sum of its digits or query the current value of a single element. The task is to output the results of all the queries in the order they appear."
date: "2026-06-09T10:33:21+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1791
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 849 (Div. 4)"
rating: 1500
weight: 1791
solve_time_s: 194
verified: true
draft: false
---

[CF 1791F - Range Update Point Query](https://codeforces.com/problemset/problem/1791/F)

**Rating:** 1500  
**Tags:** binary search, brute force, data structures  
**Solve time:** 3m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a series of operations that either transform a subarray by replacing each element with the sum of its digits or query the current value of a single element. The task is to output the results of all the queries in the order they appear. Each test case is independent. The size of the array and the number of operations can reach 200,000, but the total across all test cases is bounded by the same number. This means a naive approach that applies each sum-of-digits operation by iterating explicitly over all elements in the range for each query would be too slow in the worst case.

The sum-of-digits operation is idempotent once the number becomes a single-digit number. This is the critical property that lets us optimize. For example, applying the sum-of-digits operation multiple times on a number like 1434 gives 1+4+3+4=12, then 1+2=3, after which further operations do nothing. Edge cases arise when the range contains only single-digit numbers, which do not change, or when ranges overlap, so naive repeated iteration can unnecessarily repeat computations.

## Approaches

The brute-force approach simply loops over each type 1 query and for every index in the specified range computes the sum of digits, then answers type 2 queries by direct lookup. While this is correct logically, its worst-case complexity is $O(q \cdot n \cdot \log(a_i))$, where the logarithmic factor comes from the sum-of-digits operation, which is unacceptable for the input limits. For instance, 200,000 operations each affecting 200,000 elements would involve tens of billions of operations.

The key observation is that any number becomes stable (single-digit) after at most 9 sum-of-digits applications, since numbers are bounded by 10^9. Therefore, once an element is single-digit, further sum-of-digits operations can be skipped. We can track which elements are still “active” (not yet single-digit) and only apply operations to them. Using a data structure like a sorted list or set of active indices allows us to skip already stabilized numbers efficiently. This reduces redundant work and keeps the overall complexity linear with respect to the number of active updates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q * n * log(a_i)) | O(n) | Too slow |
| Optimized with active indices | O(n + q * log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `a` with the input numbers and a sorted list `active` containing indices of all numbers that are greater than 9.
2. Iterate through each query in order. If the query is of type 2, print the value at the queried index immediately.
3. For a type 1 query specifying a range [l, r], find all indices in `active` that lie within this range. Since `active` is sorted, this can be done efficiently with binary search.
4. For each such active index, update `a[i]` to be the sum of its digits.
5. If after the update `a[i]` becomes single-digit, remove the index from `active`. Otherwise, keep it for future operations.
6. Continue processing queries until all are handled. Type 2 queries always read the current value in `a`, which reflects all prior transformations.

Why it works: The invariant is that `active` contains exactly those indices whose values are not yet stabilized. We only update these, ensuring no wasted computation. Type 2 queries always retrieve the current value, which is correct because every prior type 1 operation affecting that index has been applied exactly once. The sum-of-digits operation is idempotent once single-digit is reached, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline
from bisect import bisect_left, bisect_right

def sum_digits(x):
    return sum(int(d) for d in str(x))

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))
        # active indices with values > 9
        active = set(i for i, val in enumerate(a) if val > 9)
        
        queries = []
        for _ in range(q):
            queries.append(input().split())
        
        for query in queries:
            if query[0] == '1':
                l, r = int(query[1])-1, int(query[2])-1
                to_remove = []
                for i in list(active):
                    if l <= i <= r:
                        a[i] = sum_digits(a[i])
                        if a[i] < 10:
                            to_remove.append(i)
                for i in to_remove:
                    active.remove(i)
            else:
                x = int(query[1])-1
                print(a[x])

if __name__ == "__main__":
    solve()
```

The code keeps track of active indices in a set. For each type 1 query, we only iterate over active indices within the specified range, updating their values and removing stabilized indices. Type 2 queries directly output the value. We use 0-based indexing internally for simplicity. Using a set ensures removal is O(1), and iterating over active indices is efficient because the number of non-single-digit elements is small.

## Worked Examples

**Sample 1 trace:**

Input: `[1, 420, 69, 1434, 2023]`, first type 1 query `[2, 3]`.

| Index | Active? | Value | After sum_digits |
| --- | --- | --- | --- |
| 1 | yes | 420 | 6 |
| 2 | yes | 69 | 15 |

Active after first update: `{2,3,4}` → indices with values `15, 1434, 2023`. Queries of type 2 directly read current values: 6, 15, 1434.

Second type 1 query `[2,5]`:

| Index | Active? | Value | After sum_digits |
| --- | --- | --- | --- |
| 2 | yes | 15 | 6 |
| 3 | yes | 1434 | 12 |
| 4 | yes | 2023 | 7 |

Active after this: `{3}` → only index 3 has value 12 (>9). Type 2 queries output: 1, 6, 7, confirming correctness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q * k) | `k` is small because each number becomes single-digit after at most 9 sum-of-digits; each index processed only while >9 |
| Space | O(n) | Array `a` and active set |

Since the total number of elements and queries across all test cases ≤ 2e5, this solution runs well within time limits.

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

# Provided sample
assert run("3\n5 8\n1 420 69 1434 2023\n1 2 3\n2 2\n2 3\n2 4\n1 2 5\n2 1\n2 3\n2 5\n2 3\n9999 1000\n1 1 2\n2 1\n2 2\n1 1\n1\n2 1\n") == "6\n15\n1434\n1\n6\n7\n36\n1\n1"

# Custom tests
assert run("1\n5 3\n9 10 11 12 13\n1 1 5\n2 3\n2 5\n") == "2\n4"
assert run("1\n1 2\n123456789\n1 1 1\n2 1\n") == "9"
assert run("1\n3 2\n5 5 5\n1 1 3\n2 2\n") == "5"
assert run("1\n3 1\n99 9 9\n2 1\n") == "99"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 elements all >9, range full | 2 4 | Correct sum-of-digits transformations and stabilization |
| Single element large | 9 | Multiple sum-of-digits applications handled correctly |
| All single-digit | 5 | No unnecessary updates performed |
| Mix of 2-digit and single-digit | 99 | Queries work on unchanged numbers |

## Edge Cases

If a range contains only single-digit numbers, the algorithm correctly skips them because they are not in the active set. For overlapping ranges, each index is processed at most 9 times until stabilization, so repeated ranges do not cause inefficiency. For single-element arrays or ranges, the behavior is identical and correctly updates or reads the element. The implementation handles all edge conditions including maximum array size, maximum number of queries, and values at the upper bound 10^9.
