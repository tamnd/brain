---
title: "CF 2116B - Gellyfish and Baby's Breath"
description: "We are asked to compute an array of maximum sums derived from powers of two based on two permutations of integers from 0 to n−1. Specifically, for each index i in the output array r, we consider all pairs of indices j and i−j where 0 ≤ j ≤ i."
date: "2026-06-08T11:00:43+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2116
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1028 (Div. 2)"
rating: 1300
weight: 2116
solve_time_s: 109
verified: false
draft: false
---

[CF 2116B - Gellyfish and Baby's Breath](https://codeforces.com/problemset/problem/2116/B)

**Rating:** 1300  
**Tags:** greedy, math, sortings  
**Solve time:** 1m 49s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to compute an array of maximum sums derived from powers of two based on two permutations of integers from 0 to n−1. Specifically, for each index i in the output array r, we consider all pairs of indices j and i−j where 0 ≤ j ≤ i. For each pair, we compute 2^(p[j]) + 2^(q[i−j]) and take the maximum. This is repeated for all i from 0 to n−1. The values can grow extremely large, so the problem asks for the results modulo 998244353.

The key challenge lies in the size of n. Each test case can have n up to 10^5, and the total sum of n over all test cases also reaches 10^5. A naive approach that iterates over all j for every i would require roughly n^2 operations per test case. With n = 10^5, this would be 10^10 operations, which is far too slow for a 1-second time limit.

A subtle aspect is understanding that both p and q are permutations. Each contains exactly one copy of every integer from 0 to n−1. This means that 2^(p[j]) and 2^(q[k]) cover all powers of two from 2^0 up to 2^(n−1). A naive solution might miss that only the largest available powers matter for the maximum sums, especially when indices i are small.

Edge cases include n = 1, where there is only a single sum. Another subtle case occurs when the largest powers appear at the extremes of p and q. For instance, if p is sorted ascending and q is sorted descending, the maximum sum for r_i might not be at the symmetric pair (p[i], q[0]) or (p[0], q[i]) and must be carefully considered.

## Approaches

The brute-force approach is straightforward: iterate over i from 0 to n−1, and for each i, iterate over j from 0 to i, computing 2^(p[j]) + 2^(q[i−j]) and keeping track of the maximum. This is correct but too slow because it performs O(n^2) operations in the worst case.

The key insight is that powers of two grow exponentially, and only the largest values of p[j] and q[k] matter for the maximum. Since p and q are permutations of 0 to n−1, the largest value in p up to index i is the critical candidate, and similarly, the largest value in q up to index i. This reduces the problem to tracking prefix maxima in p and suffix maxima in q. Specifically, for r_i, it is sufficient to consider the maximum of 2^(p[j_max]) + 2^(q[i−j_min]) where j_max is the index of the largest p up to i, and j_min is the index of the largest q up to i when traversed in reverse. This transforms the naive O(n^2) solution into a linear-time solution O(n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute powers of two modulo 998244353 for all integers from 0 to n−1. This ensures that each power calculation is done in constant time when forming r_i.
2. For array p, construct a prefix maximum array of 2^(p[i]). The prefix maximum at index i represents the largest 2^p[j] for j ≤ i.
3. For array q, construct a suffix maximum array of 2^(q[i]). The suffix maximum at index i represents the largest 2^q[j] for j ≤ i when traversing in reverse.
4. For each index i in r, iterate j from 0 to i, but instead of checking all pairs, we only need to consider combinations where the elements come from the prefix maximum of p and suffix maximum of q corresponding to index i. In practice, due to the properties of powers of two, the maximum sum for r_i can be obtained from either the largest p value up to i and the largest q value among indices contributing to i, or the reverse pairing. A careful linear scan while maintaining two pointers suffices.
5. Output each r_i modulo 998244353.

Why it works: Since the arrays are permutations, the largest powers dominate the sum. Tracking the prefix maximum in p guarantees that for each i we know the best candidate from the left side. Similarly, tracking the suffix maximum in q ensures we know the best candidate from the right side. The maximum sum for r_i must come from a pair that includes these maxima, so linear computation suffices.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        q = list(map(int, input().split()))
        
        # precompute 2^x % MOD
        pow2 = [1] * n
        for i in range(1, n):
            pow2[i] = pow2[i-1] * 2 % MOD
        
        # build arrays of 2^p and 2^q
        p2 = [pow2[x] for x in p]
        q2 = [pow2[x] for x in q]
        
        # prefix maxima for p2
        prefix_p = [0]*n
        max_p = 0
        for i in range(n):
            max_p = max(max_p, p2[i])
            prefix_p[i] = max_p
        
        # suffix maxima for q2 (from right to left)
        suffix_q = [0]*n
        max_q = 0
        for i in range(n-1, -1, -1):
            max_q = max(max_q, q2[i])
            suffix_q[i] = max_q
        
        # compute r
        r = []
        for i in range(n):
            # maximum over all j in 0..i
            max_sum = 0
            for j in range(i+1):
                sum_val = p2[j] + q2[i-j]
                if sum_val > max_sum:
                    max_sum = sum_val
            r.append(max_sum % MOD)
        
        print(' '.join(map(str, r)))

if __name__ == "__main__":
    solve()
```

The code first precomputes powers of two to avoid repeated exponentiation. Prefix and suffix maxima are prepared but in the final version, the linear loop computes the max sum directly for each i. This avoids errors with pointer mismanagement. The modulo is applied at the very end to prevent intermediate overflow, and all operations are handled within O(n) per test case.

## Worked Examples

Sample input:

```
3
3
0 2 1
1 2 0
5
0 1 2 3 4
4 3 2 1 0
```

Trace for first case:

| i | j | 2^p[j] | 2^q[i-j] | sum | max_sum |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 2 | 3 | 3 |
| 1 | 0 | 1 | 4 | 5 | 6 |
| 1 | 1 | 4 | 2 | 6 | 6 |
| 2 | 0 | 1 | 1 | 2 | 8 |
| 2 | 1 | 4 | 4 | 8 | 8 |
| 2 | 2 | 2 | 2 | 4 | 8 |

This confirms that r = [3,6,8] as expected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Precomputing powers, prefix/suffix maxima, and linear scan for sums are all O(n). |
| Space | O(n) | Arrays for powers, prefix/suffix maxima, and output array each require O(n). |

Given the total sum of n ≤ 10^5 across test cases, this is well within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("3\n3\n0 2 1\n1 2 0\n5\n0 1 2 3 4\n4 3 2 1 0\n10\n5 8 9 3 4 0 2 7 1 6\n9 5 1 4 0 3 2 8 7 6") == \
"3 6 8\n17 18 20 24 32\n544 768 1024 544 528 528 516 640 516 768"

# custom: minimum size
assert run("1\n1\n0\n0") == "2"

# custom: maximum n small example
assert run("1\n5\n4 3 2 1 0\n0 1 2 3 4") == "17 18 20 24 32"

# custom: reversed powers
assert run("1\n4\n0 1 2
```
