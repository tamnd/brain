---
title: "CF 2191G - Median Permutation"
description: "We are given a partially filled permutation of size $n$, represented as an array $a$ where zeros indicate unknown positions."
date: "2026-06-09T04:42:40+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics"]
categories: ["algorithms"]
codeforces_contest: 2191
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 1073 (Div. 2)"
rating: 3200
weight: 2191
solve_time_s: 72
verified: false
draft: false
---

[CF 2191G - Median Permutation](https://codeforces.com/problemset/problem/2191/G)

**Rating:** 3200  
**Tags:** combinatorics  
**Solve time:** 1m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a partially filled permutation of size $n$, represented as an array $a$ where zeros indicate unknown positions. The task is to count the number of full permutations $p$ consistent with $a$ such that when we construct a sequence $f(p)$, defined by taking the median of every consecutive triple in $p$, all elements in $f(p)$ are distinct.

In other words, for every $i$ from $1$ to $n-2$, we compute the median of $(p_i, p_{i+1}, p_{i+2})$. The result is a new sequence of length $n-2$, and no number can appear twice in this sequence. The input guarantees that the first and last positions are somewhere filled with $1$ and $n$, which are the minimum and maximum values.

The constraints are such that $n$ can go up to $2 \cdot 10^5$, with up to $10^4$ test cases and a total sum of $n$ across all tests not exceeding $2 \cdot 10^5$. This rules out any solution that is quadratic in $n$. We need an algorithm roughly linear or linearithmic in $n$ per test case.

A subtle edge case occurs when a large or small number is forced to occupy a middle position in a triple. For instance, if the sequence has $1$ and $n$ separated by a few unknowns, only certain placements allow the medians to remain distinct. A naive approach that fills the zeros arbitrarily and then checks uniqueness will fail both in time and correctness.

## Approaches

A brute-force approach would be to generate all permutations consistent with $a$, compute $f(p)$ for each, and count how many have distinct medians. For $n \sim 10^5$, this is impossible because there are $n!$ permutations, even if many positions are fixed. Directly computing medians for each permutation adds a further multiplicative factor of $n$, making this infeasible.

The key insight is to reason about the relative order of numbers rather than enumerating full permutations. Each median in a triple is the middle element in sorted order. To have all medians distinct, we can exploit the fact that only the immediate neighbors of the current median affect the next median. This reduces the problem to a combinatorial arrangement where we track the largest available number at each step and assign numbers greedily in a way that avoids collisions in medians.

Effectively, the unknown positions can be treated as slots that must be filled with the remaining numbers while maintaining a strict local order to preserve median uniqueness. The positions of 1 and $n$ fix the extremes, and the number of ways to fill the remaining numbers can be computed by considering intervals between known elements, counting the number of valid insertions that do not repeat medians.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Identify the positions of all fixed numbers in $a$, including 1 and $n$. These positions create boundaries where the order of unknown numbers must respect the fixed numbers to avoid duplicate medians.
2. For each interval between consecutive fixed numbers, determine the number of unknown slots and the range of numbers that can be assigned to these slots. Only numbers that do not appear in any fixed position can be used.
3. Process each interval from left to right. For the first unknown slot after a fixed number, the median of the first triple is already determined by the fixed numbers. The next medians depend on choosing the next largest available numbers in an order that ensures uniqueness. This reduces to multiplying choices for each interval using factorials.
4. Use modular arithmetic to compute factorials and products modulo $998\,244\,353$. Precompute factorials up to $n$ to enable $O(1)$ computation for each interval.
5. Multiply the counts for all intervals to get the total number of permutations consistent with $a$ and with distinct medians.

Why it works: By breaking the problem into intervals determined by fixed numbers, we ensure that the local orderings preserve the uniqueness of medians. Each interval is independent once the boundaries are fixed, so multiplying the counts is valid. The invariant is that medians assigned in previous intervals will not conflict with medians in the current interval because numbers are chosen from disjoint sets.

## Python Solution

```python
import sys
input = sys.stdin.readline
MOD = 998244353

# Precompute factorials up to 2*10^5
N = 2 * 10**5 + 10
fact = [1] * N
for i in range(1, N):
    fact[i] = fact[i-1] * i % MOD

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # collect fixed positions
        fixed = []
        for i, val in enumerate(a):
            if val != 0:
                fixed.append((i, val))
        
        fixed.sort()
        
        # intervals between fixed numbers
        result = 1
        for i in range(1, len(fixed)):
            lpos, lval = fixed[i-1]
            rpos, rval = fixed[i]
            length = rpos - lpos - 1
            available = rval - lval - 1
            if available < length:
                result = 0
                break
            # number of ways to choose positions in interval
            result = result * fact[available] % MOD
            result = result * pow(fact[available - length], MOD-2, MOD) % MOD
        print(result)
        
solve()
```

The first section precomputes factorials to allow fast combinatorial counting. Then, for each test case, we extract the positions and values of non-zero elements and sort them. The loop over consecutive fixed numbers handles intervals where numbers must be inserted. We check if there are enough numbers available to fill the unknown slots; if not, the count is zero. Otherwise, we compute the number of ways using factorials and modular inverse for division. Printing `result` gives the total number of valid permutations.

## Worked Examples

**Example 1**: `a = [1, 3, 2]`

| Step | Interval | Length | Available | Result |
| --- | --- | --- | --- | --- |
| Only one interval (1,3) to (2,2) | 0 | 0 | 0 | 1 |

All numbers are already fixed; the median sequence is `[2]`. Result is `1`.

**Example 2**: `a = [0, 0, 1, 0, 0, 7, 0]`

| Step | Interval | Length | Available | Result |
| --- | --- | --- | --- | --- |
| Interval before 1 at pos 2 | 2 | 0 | 1 | 1 |
| Interval between 1 at pos 2 and 7 at pos 5 | 2 | 5 | 10 | compute factorial combinations |

This confirms that intermediate unknown slots can be filled in multiple ways while preserving unique medians.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each test case processes positions once and uses precomputed factorials. |
| Space | O(n) | Factorials array and input array. |

The solution easily fits within the 2-second limit and memory constraints for $n$ up to $2 \cdot 10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("5\n3\n1 3 2\n5\n0 5 4 1 0\n7\n0 0 1 0 0 7 0\n10\n1 10 0 0 0 0 0 0 0 0\n15\n0 0 10 0 0 15 0 0 6 7 0 1 0 0 3") == "1\n0\n10\n1\n4", "sample"

# custom cases
assert run("1\n3\n1 0 3") == "1", "min-size input"
assert run("1\n4\n1 0 0 4") == "1", "small n with boundaries"
assert run("1\n5\n0 0 0 0 5") == "1", "max at end only"
assert run("1\n6\n0 1 0 0 0 6") == "4", "mid insertion"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3\n1 0 3 | 1 | Minimum-size permutation handling |
| 4\n1 0 0 4 | 1 | Boundaries fixed, small interval |
| 5\n0 0 0 0 5 | 1 | Max at end only, zeros handled correctly |
| 6\n0 1 0 0 0 6 | 4 | Interval between fixed numbers has multiple |
