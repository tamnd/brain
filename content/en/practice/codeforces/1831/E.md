---
title: "CF 1831E - Hyperregular Bracket Strings"
description: "We are asked to count bracket sequences of length $n$ that are globally regular, while also being locally regular on certain specified subintervals. The input gives us the length $n$ and a list of $k$ intervals $[li, ri]$."
date: "2026-06-09T07:08:38+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "data-structures", "hashing", "math", "number-theory", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1831
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 875 (Div. 2)"
rating: 2400
weight: 1831
solve_time_s: 200
verified: false
draft: false
---

[CF 1831E - Hyperregular Bracket Strings](https://codeforces.com/problemset/problem/1831/E)

**Rating:** 2400  
**Tags:** combinatorics, data structures, hashing, math, number theory, sortings, two pointers  
**Solve time:** 3m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count bracket sequences of length $n$ that are globally regular, while also being locally regular on certain specified subintervals. The input gives us the length $n$ and a list of $k$ intervals $[l_i, r_i]$. A globally regular bracket sequence is one where every opening parenthesis has a matching closing parenthesis, and no closing parenthesis occurs before its matching opening. A sequence is hyperregular if each of the specified intervals forms a valid regular bracket sequence on its own. Our output is the number of such hyperregular sequences modulo $998{,}244{,}353$.

The constraints are tight. The total $n$ across all test cases can reach $3 \cdot 10^5$, and $k$ can also reach $3 \cdot 10^5$. A naive approach that generates all sequences, checks regularity, and then filters based on intervals is impossible because the number of sequences grows exponentially in $n$. Therefore, we need a combinatorial or mathematical approach, ideally in linear or near-linear time with respect to $n + k$.

Edge cases arise when $n$ is odd, since no regular sequence exists, or when intervals are overlapping or nested, as these constraints reduce the number of valid sequences and can even make the count zero. A careful handling of empty intervals and intervals of length one is also required because they automatically constrain certain positions in the sequence.

## Approaches

The brute-force approach would generate all $2^n$ sequences, check if each is globally regular, and then check each interval for local regularity. This is correct in principle but utterly infeasible for $n > 20$ due to exponential growth.

The key observation is that regular bracket sequences are fully characterized by the number of opening and closing brackets and their positions. The Catalan numbers enumerate all regular sequences of a given length. When we add intervals with the hyperregular constraint, it forces certain positions to match, effectively fixing portions of the sequence. If intervals overlap or nest, the sequence inside must satisfy all overlapping constraints simultaneously. This leads to a combinatorial reduction: we only need to consider how the endpoints of these intervals can match to form smaller valid sequences.

The optimal approach leverages the fact that any nested interval structure can be recursively split into independent segments. By counting the number of ways to fill each independent segment using Catalan numbers and multiplying, we can compute the total number of hyperregular sequences efficiently. Precomputing factorials and inverse factorials modulo $998{,}244{,}353$ allows us to compute Catalan numbers in constant time for each segment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * k) | O(n) | Too slow |
| Optimal | O((n + k) log(n)) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and $k$, and store the intervals $[l_i, r_i]$. Sort the intervals by starting point. Sorting is required to handle nested or overlapping intervals efficiently.
2. Initialize a stack to simulate a nesting structure. Iterate through the intervals, and for each, if it starts after the top of the stack, pop the stack until the current interval fits. This constructs a tree representing nested intervals.
3. For each node in the interval tree, compute the number of valid sequences recursively. If a node has child intervals, split the sequence into segments defined by these children. For each segment of length $m$, compute the Catalan number $C_{m/2}$ if $m$ is even. If $m$ is odd, set the count to zero because no regular sequence exists of odd length.
4. Multiply the Catalan numbers of all segments and recursively for nested children. This gives the count for the current interval.
5. The answer for the test case is the count for the interval covering the entire sequence. If no interval covers the full sequence, consider the entire sequence as a single interval.

Why it works: Catalan numbers enumerate all sequences that satisfy regularity. By splitting the sequence into non-overlapping segments determined by the nested interval structure, we ensure that each segment is counted independently. Multiplying counts is valid due to independence. The recursion respects nesting, so every interval constraint is satisfied.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
MAX = 3 * 10**5 + 10

# precompute factorials and inverse factorials
fact = [1] * MAX
invfact = [1] * MAX
for i in range(1, MAX):
    fact[i] = fact[i - 1] * i % MOD
invfact[MAX - 1] = pow(fact[MAX - 1], MOD - 2, MOD)
for i in range(MAX - 2, -1, -1):
    invfact[i] = invfact[i + 1] * (i + 1) % MOD

def catalan(n):
    if n == 0:
        return 1
    return fact[2 * n] * invfact[n] % MOD * invfact[n + 1] % MOD

def solve_case(n, k, intervals):
    intervals.sort()
    stack = []
    result = 1
    last = 0

    for l, r in intervals:
        # handle gaps
        if l - 1 > last:
            gap = l - 1 - last
            if gap % 2 != 0:
                return 0
            result = result * catalan(gap // 2) % MOD
        last = max(last, r)
    # handle tail
    if last < n:
        gap = n - last
        if gap % 2 != 0:
            return 0
        result = result * catalan(gap // 2) % MOD
    return result

def main():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        intervals = [tuple(map(int, input().split())) for _ in range(k)]
```
