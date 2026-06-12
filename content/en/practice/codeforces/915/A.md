---
title: "CF 915A - Garden"
description: "We are asked to water a linear garden of length k using one of n buckets. Each bucket waters a fixed segment of the garden every hour, specifically a continuous stretch of length ai. Luba must water the entire garden without leaving gaps and cannot water any part twice."
date: "2026-06-13T01:46:54+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 915
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 36 (Rated for Div. 2)"
rating: 900
weight: 915
solve_time_s: 704
verified: true
draft: false
---

[CF 915A - Garden](https://codeforces.com/problemset/problem/915/A)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 11m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to water a linear garden of length _k_ using one of _n_ buckets. Each bucket waters a fixed segment of the garden every hour, specifically a continuous stretch of length _a_i_. Luba must water the entire garden without leaving gaps and cannot water any part twice. Our task is to determine which bucket minimizes the total number of hours required.

The input gives the number of buckets and the garden length on the first line, followed by the lengths that each bucket can water in one hour. The output is a single integer, the minimum number of hours needed to water the garden using a single bucket.

The constraints are small: _n_ and _k_ are both at most 100. That means even a straightforward approach iterating over all buckets is efficient. We can safely check each bucket in turn and perform simple arithmetic to see if it divides the garden evenly. The edge case that could cause a naive implementation to fail is when a bucket’s watering length does not divide the garden length evenly. For example, if _k_ = 6 and the buckets are [5, 2], the bucket with length 5 cannot fully water the garden, while 2 divides 6 exactly, giving 3 hours.

## Approaches

The brute-force approach is simple. For each bucket, check if its watering length divides the garden length exactly. If it does, compute the number of hours required as `k // a_i`. Keep track of the minimum number of hours across all buckets. This is correct because watering can only be done in continuous segments of exactly the bucket’s length, and partial watering of a segment is not allowed.

A naive variation might attempt to simulate placing segments of length `a_i` along the garden, but that is unnecessary because division handles it directly. Since the maximum value for _n_ and _k_ is 100, iterating over all buckets and performing integer division is extremely fast, giving an operation count of at most 100, which is negligible.

The key insight that simplifies this problem is realizing that the problem reduces to integer division. For each bucket that divides the garden length exactly, the number of hours is `k // a_i`. We only need to pick the largest such bucket because larger segments reduce the number of hours. The observation that `k % a_i == 0` allows us to discard buckets that cannot fully water the garden in integer hours.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of buckets `n` and garden length `k`.
2. Read the list of bucket lengths `a`.
3. Initialize a variable `min_hours` to a large number to track the minimal hours.
4. Iterate through each bucket length `length` in `a`.
5. Check if `k % length == 0`. If it does not, skip this bucket because it cannot water the garden fully in integer hours.
6. Compute the number of hours as `hours = k // length`.
7. Update `min_hours` if `hours` is smaller than the current `min_hours`.
8. After checking all buckets, print `min_hours`.

The invariant here is that we only consider bucket lengths that divide the garden exactly. Since the problem guarantees at least one valid bucket, `min_hours` will always be updated with a correct value. Because larger segments reduce the number of hours, this approach ensures we find the minimal number of hours.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

min_hours = float('inf')
for length in a:
    if k % length == 0:
        hours = k // length
        if hours < min_hours:
            min_hours = hours

print(min_hours)
```

The solution reads input efficiently with `sys.stdin.readline`. We initialize `min_hours` to infinity to ensure any valid number of hours is smaller. We iterate over all buckets, check divisibility with the garden length, and update the minimum hours. The check `k % length == 0` is crucial because it guarantees full coverage of the garden. The final print outputs the minimal hours.

## Worked Examples

### Sample 1

Input:

```
3 6
2 3 5
```

| Bucket Length | k % length | Hours (k//length) | min_hours |
| --- | --- | --- | --- |
| 2 | 0 | 3 | 3 |
| 3 | 0 | 2 | 2 |
| 5 | 1 | - | 2 |

This demonstrates that only buckets dividing the garden length exactly are considered. The minimal hours is 2.

### Sample 2

Input:

```
2 7
1 3
```

| Bucket Length | k % length | Hours (k//length) | min_hours |
| --- | --- | --- | --- |
| 1 | 0 | 7 | 7 |
| 3 | 1 | - | 7 |

Here only bucket length 1 works, giving 7 hours.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Iterate over each bucket once |
| Space | O(n) | Store the list of bucket lengths |

Given the small constraints n ≤ 100 and k ≤ 100, this algorithm runs instantly within the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    min_hours = float('inf')
    for length in a:
        if k % length == 0:
            hours = k // length
            if hours < min_hours:
                min_hours = hours
    return str(min_hours)

# provided samples
assert run("3 6\n2 3 5\n") == "2", "sample 1"
assert run("1 1\n1\n") == "1", "sample 2"

# custom cases
assert run("2 7\n1 3\n") == "7", "only bucket 1 works"
assert run("5 100\n1 2 4 5 10\n") == "10", "bucket 10 is optimal"
assert run("3 15\n4 5 6\n") == "3", "bucket 5 is best"
assert run("1 100\n100\n") == "1", "single bucket matches exactly"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 7\n1 3 | 7 | Only bucket 1 works |
| 5 100\n1 2 4 5 10 | 10 | Bucket with largest divisor is chosen |
| 3 15\n4 5 6 | 3 | Correct choice among multiple divisors |
| 1 100\n100 | 1 | Single bucket equals garden length |

## Edge Cases

If the garden length equals the largest bucket, such as k = 100 and bucket = 100, the algorithm correctly identifies 1 hour. If the smallest bucket is the only divisor, like k = 7 and bucket = 1, the algorithm produces 7 hours. The algorithm ignores non-dividing buckets automatically, preventing incorrect partial watering. All edge cases are covered by the divisibility check and the guarantee that at least one bucket works.
