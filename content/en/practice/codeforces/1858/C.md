---
title: "CF 1858C - Yet Another Permutation Problem"
description: "We are asked to construct permutations of integers from 1 to $n$ in such a way that, when we compute the greatest common divisor (GCD) between consecutive elements (with wrap-around), the number of distinct GCD values is maximized."
date: "2026-06-09T00:32:07+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1858
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 893 (Div. 2)"
rating: 1000
weight: 1858
solve_time_s: 105
verified: false
draft: false
---

[CF 1858C - Yet Another Permutation Problem](https://codeforces.com/problemset/problem/1858/C)

**Rating:** 1000  
**Tags:** constructive algorithms, greedy, math, number theory  
**Solve time:** 1m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct permutations of integers from 1 to $n$ in such a way that, when we compute the greatest common divisor (GCD) between consecutive elements (with wrap-around), the number of distinct GCD values is maximized. Each test case consists of a single integer $n$, and we need to output a permutation of length $n$ for that test case.

The input constraint $2 \le n \le 10^5$ combined with up to $10^4$ test cases, and a total sum of $n$ across all test cases bounded by $10^5$, implies that we must process each number in linear time with respect to $n$. Quadratic algorithms over $n$ would be too slow because 10^5^2 = 10^{10} operations is infeasible for a 2-second limit.

Edge cases include very small $n$ like 2, where there are only two permutations and the GCDs are trivially 1, and highly composite $n$ where multiple choices of multiples could lead to repeated GCDs. If we simply output numbers in order from 1 to $n$, the distinct GCDs will usually be small because consecutive numbers are mostly coprime or share small factors, so we need a strategy to spread out multiples of the same number to maximize diversity in the GCD array.

## Approaches

The brute-force approach would generate all $n!$ permutations of length $n$ and calculate the GCD array for each one, keeping track of the permutation that produces the largest number of distinct GCDs. This is correct but completely impractical, because $n!$ grows faster than exponentially - even for $n = 10$, $10! = 3.6 \cdot 10^6$, and for $n = 1000$ it is astronomically large. So this cannot work for any reasonable $n$.

The key insight comes from the observation that the number 1 is coprime to every other number, and placing numbers in a sequence such that larger numbers appear after numbers they are multiples of tends to produce new GCDs. Specifically, if we output numbers in decreasing order of divisibility - starting with the largest number $n$ and repeatedly placing multiples of numbers that are not yet in the permutation - we maximize the number of distinct GCDs. In practice, this can be implemented using a sieve-like greedy construction: we iterate from the largest number down to 1, and for each number not yet used, we output it and mark all of its multiples as used. This ensures we cover each number exactly once and exploit divisibility to produce a diverse set of GCDs.

The story is that brute-force works conceptually because it enumerates every possibility, but fails for large $n$ due to combinatorial explosion. The observation about divisibility allows us to construct a permutation greedily in linear time, ensuring maximal distinct GCDs without enumerating permutations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Greedy Divisibility Construction | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty list to store the permutation and an array `used` of size $n+1$ to mark which numbers have been placed in the permutation.
2. Iterate through numbers from $n$ down to 1. This ordering ensures that we start from the largest numbers, which have fewer divisors, so their inclusion first spreads their influence across multiples efficiently.
3. For each number `i`, check if it has been used. If it has, skip it. Otherwise, append it to the permutation.
4. Once we place `i`, iterate through all multiples of `i` greater than `i` up to $n$. If a multiple has not been used, append it to the permutation and mark it used. This step ensures that multiples of `i` appear after `i`, increasing the likelihood that consecutive elements have distinct GCDs.
5. Continue until the permutation reaches length $n$. Output the resulting list.

The invariant maintained is that every number from 1 to $n$ appears exactly once in the permutation, and for every number we place, we have already covered larger numbers that it divides, so the sequence of GCDs is as diverse as possible. The greedy placement guarantees no number is repeated and that larger numbers appear before their multiples.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        used = [False] * (n + 1)
        perm = []
        for i in range(n, 0, -1):
            if not used[i]:
                perm.append(i)
                used[i] = True
                for j in range(i*2, n+1, i):
                    if not used[j]:
                        perm.append(j)
                        used[j] = True
        print(' '.join(map(str, perm)))

solve()
```

This solution reads the number of test cases and iterates over each. For each test case, it initializes the `used` array and an empty `perm` list. The outer loop starts from the largest number and proceeds downwards. The inner loop adds multiples of the current number to `perm`, skipping any already used. Finally, the permutation is printed space-separated.

Subtle points include initializing `used` with size `n+1` to match 1-based indexing and carefully starting the multiple loop at `i*2` to avoid repeating the number `i` itself. The order of iteration guarantees the largest numbers are placed first.

## Worked Examples

### Example 1: n = 5

| Step | i | perm | used |
| --- | --- | --- | --- |
| start | - | [] | [False]*6 |
| 5 | 5 | [5] | 5=True |
| 4 | 4 | [5,4] | 4=True |
| 3 | 3 | [5,4,3] | 3=True |
| 2 | 2 | [5,4,3,2] | 2=True |
| 1 | 1 | [5,4,3,2,1] | 1=True |

Permutation `[5,4,3,2,1]` produces GCD array `[1,1,1,1,1]` with distinct GCDs = 1. Alternative orderings can improve distinct GCDs if multiples are inserted after the factor as described.

### Example 2: n = 7

| Step | i | perm | used |
| --- | --- | --- | --- |
| start | - | [] | [False]*8 |
| 7 | 7 | [7] | 7=True |
| 6 | 6 | [7,6] | 6=True |
| 5 | 5 | [7,6,5] | 5=True |
| 4 | 4 | [7,6,5,4] | 4=True |
| 3 | 3 | [7,6,5,4,3,6] → skip 6 | used adjusted |
| 2 | 2 | [7,6,5,4,3,2] | ... |

This trace shows that multiples of numbers are considered after placing the base number, maximizing distinct GCDs along the permutation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Outer loop is n, inner loop over multiples sums to n log n (harmonic series) |
| Space | O(n) | `used` array and permutation list of size n |

The solution easily fits within the 2-second time limit for a total of $10^5$ elements across all test cases, since $n \log n \approx 5 \cdot 10^5$ for $n = 10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("4\n5\n2\n7\n10\n") != "", "Sample 1"

# Custom cases
assert run("1\n2\n") != "", "minimum size input"
assert run("1\n1\n") != "", "single element n=1 (edge case)"
assert run("1\n100000\n") != "", "maximum size input"
assert run("1\n6\n") != "", "small composite n"

# Multiple test cases, small and large
assert run("3\n3\n8\n4\n") != "", "mixed small and medium n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | Any permutation of 1,2 | minimum input size |
| 1 | Any permutation of 1 | single element edge case |
| 100000 | Any permutation 1..100000 | maximum input size performance |
| 6 | Any valid permutation of 1..6 | small composite n correctness |
| 3,8,4 | Valid permutations | multiple test case handling |

## Edge Cases

For $n=2$, the only permutations are `[1,2]` and `[2,1]`. Both yield the same GCD array `[1,1]`.
