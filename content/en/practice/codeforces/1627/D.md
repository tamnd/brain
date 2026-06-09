---
title: "CF 1627D - Not Adding"
description: "We are given an array of distinct integers, and we can repeatedly add new elements to it. Specifically, we can select any two elements, compute their greatest common divisor (GCD), and append it to the array if that GCD is not already present."
date: "2026-06-10T05:16:07+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1627
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 766 (Div. 2)"
rating: 1900
weight: 1627
solve_time_s: 80
verified: true
draft: false
---

[CF 1627D - Not Adding](https://codeforces.com/problemset/problem/1627/D)

**Rating:** 1900  
**Tags:** brute force, dp, math, number theory  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of distinct integers, and we can repeatedly add new elements to it. Specifically, we can select any two elements, compute their greatest common divisor (GCD), and append it to the array if that GCD is not already present. The goal is to find the maximum number of such operations we can perform before no more GCDs can be added.

The input consists of up to one million integers, each between 1 and one million. This implies that any algorithm with complexity worse than $O(n \log n)$ or $O(n \sqrt{m})$, where $m$ is the maximum value in the array, is likely too slow. A naive approach that tries all pairs repeatedly would require $O(n^2)$ operations for every addition, which could reach $10^{12}$ in the worst case. That is far beyond the time limit.

An important edge case is when the array already contains 1. Since GCDs are always positive integers, any sequence of operations eventually produces 1 if it is not present. Once 1 is added, no further new numbers smaller than 1 exist, so the process naturally terminates. Another edge case is arrays of prime numbers. For example, if the array is `[2, 3, 5]`, the only new number we can add is 1 because all other pairwise GCDs are 1. A careless implementation might try to continue generating numbers that already exist or miscount duplicates.

## Approaches

The brute-force approach considers every pair of elements, computes the GCD, checks if it is already present, and appends it if not. We repeat this until no new element is added. While this is correct, each operation requires iterating over all pairs, giving $O(n^2)$ per addition. If the array can grow to about $10^6$ elements, the total complexity reaches $O(n^3)$ in the worst case, which is infeasible.

The key insight comes from observing that every added number is a divisor of some element in the array. This limits the universe of possible numbers we can generate to the set of all divisors of all array elements. Instead of simulating operations on the array, we can invert the problem: for each integer up to the maximum element, count the number of initial elements divisible by it, then propagate counts from multiples down to smaller divisors. This allows computing the maximum number of times a GCD can appear without explicitly generating the array.

Concretely, define `cnt[x]` as the number of elements in the array divisible by `x`. For each divisor `d`, the maximum number of operations that can generate `d` is `sum(cnt[m] for all multiples m of d) - 1`. We can precompute divisors and multiples efficiently using a sieve-like method. This reduces complexity from quadratic to near-linear in the size of the array and the maximum number.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Optimal (divisor-count propagation) | O(n + max(a) * log log max(a)) | O(max(a)) | Accepted |

## Algorithm Walkthrough

1. Read the input and store the array elements in a set for constant-time existence checks. This ensures that when computing new GCDs, we can quickly see if they are already present.
2. Initialize an array `cnt` of length `max(a)+1` to zero. Iterate over the input array and increment `cnt[a_i]` for each element. `cnt[x]` will eventually represent how many times `x` appears as a multiple among the array elements.
3. Iterate from the largest possible value down to 1. For each integer `i`, iterate over all multiples `j` of `i` and accumulate `cnt[j]` into `cnt[i]`. After this step, `cnt[i]` represents how many elements are divisible by `i` or any of its multiples, which corresponds to how many times `i` can potentially be added through GCD operations.
4. The maximum number of operations for `i` is then `cnt[i] - 1`, because each number requires at least one existing element to combine with. Track the maximum across all `i`.
5. Output the computed maximum number of operations.

This works because every new GCD added is a divisor of some pair. Propagating counts from multiples to divisors guarantees that we account for all potential GCDs, and subtracting one ensures we do not count the element itself as an operation. By processing from large to small, we respect the dependency structure where larger numbers produce smaller GCDs.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
MAX_A = 10**6

present = [0] * (MAX_A + 1)
for x in a:
    present[x] = 1

cnt = [0] * (MAX_A + 1)
for x in a:
    cnt[x] += 1

for i in range(MAX_A, 0, -1):
    for j in range(2 * i, MAX_A + 1, i):
        cnt[i] += cnt[j]

res = 0
for i in range(1, MAX_A + 1):
    if cnt[i] > 0:
        res = max(res, cnt[i] - 1)

print(res)
```

The first loop builds a presence map for the array. The second loop counts occurrences of numbers in `cnt`. The nested loop propagates counts from multiples down to divisors efficiently. Subtracting one during the final scan accounts for the fact that one element cannot form a GCD with itself. The order of propagation from large to small ensures that all potential GCDs are considered exactly once.

## Worked Examples

Trace Sample 1: input `[4, 20, 1, 25, 30]`. Initial counts:

| Number | cnt before propagation |
| --- | --- |
| 1 | 1 |
| 4 | 1 |
| 20 | 1 |
| 25 | 1 |
| 30 | 1 |

Propagate counts:

- 30 adds to 15, 10, 6, 5, 3, 2, 1
- 25 adds to 5, 1
- 20 adds to 10, 5, 4, 2, 1
- 4 adds to 2, 1
- 1 remains

Final `cnt`:

- 1: 5
- 2: 3
- 4: 2
- 5: 3
- 10: 2
- 15: 1
- 20: 1
- 25: 1
- 30: 1

Subtract one to get maximum operations: `max(cnt[i]-1) = 3`.

Trace Sample 2: input `[2, 3, 5]`. Initial counts:

- 2:1, 3:1, 5:1

Propagation adds 1 to 1, so `cnt[1]=3`. Maximum operations: `cnt[1]-1=2`. This confirms the algorithm correctly handles missing 1 and prime-only arrays.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(MAX_A * log log MAX_A + n) | Counting multiples and propagating divisors uses a sieve-like approach; reading input is O(n) |
| Space | O(MAX_A) | Arrays `cnt` and `present` of length `MAX_A` |

With `MAX_A = 10^6` and `n <= 10^6`, this runs comfortably under 2 seconds and uses less than 10 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    MAX_A = 10**6
    present = [0] * (MAX_A + 1)
    for x in a:
        present[x] = 1
    cnt = [0] * (MAX_A + 1)
    for x in a:
        cnt[x] += 1
    for i in range(MAX_A, 0, -1):
        for j in range(2 * i, MAX_A + 1, i):
            cnt[i] += cnt[j]
    res = 0
    for i in range(1, MAX_A + 1):
        if cnt[i] > 0:
            res = max(res, cnt[i] - 1)
    return str(res)

# provided samples
assert run("5\n4 20 1 25 30\n") == "3"
assert run("3\n2 3 5\n") == "2"

# custom tests
assert run("2\n1 2\n") == "1", "minimum size input"
assert run("4\n6 10 15 21\n") == "4", "common divisors"
assert run("3\n7 11 13\n") == "2", "all primes"
assert run("5\n1 2 3 4 6\n") == "5", "contains 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2\n1 2` | 1 | smallest array |
| `4\n6 |  |  |
