---
title: "CF 105948G - \u8ff7\u5bab (II)"
description: "We are given a square grid whose side length is $2n$. Inside this grid, there is a fixed procedure described in a previous part of the problem (迷宫 I) that allows us to add edges between cells according to certain local rules."
date: "2026-06-22T16:06:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105948
codeforces_index: "G"
codeforces_contest_name: "CCF CAT NAEC 2025 (Provincial)"
rating: 0
weight: 105948
solve_time_s: 64
verified: true
draft: false
---

[CF 105948G - \u8ff7\u5bab (II)](https://codeforces.com/problemset/problem/105948/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a square grid whose side length is $2n$. Inside this grid, there is a fixed procedure described in a previous part of the problem (迷宫 I) that allows us to add edges between cells according to certain local rules. By repeatedly applying this procedure, different final graphs can be produced on the same $2n \times 2n$ board.

The task is to count how many distinct final edge configurations can be obtained in this way. Two configurations are considered different if there exists at least one adjacency edge that is present in one configuration but absent in the other. Since this count grows extremely quickly, the answer must be reported modulo $m$.

Each test case provides a pair $(n, m)$, and the goal is to compute the number of reachable configurations for that size parameter.

The constraints allow up to $10^4$ test cases, with $n$ and $m$ as large as $10^9$. This immediately rules out any solution that depends on iterating over the grid, simulating the construction, or using dynamic programming over $n$. Even $O(n)$ per test case is impossible, since $n$ itself can be $10^9$.

The structure of the input suggests that the answer depends only on $n$, not on the grid contents or individual queries. Each test case is independent, so any preprocessing must be done in constant or logarithmic time per query.

A common failure mode in problems of this type is attempting to simulate the construction rules locally. Even if each operation looks simple, the number of possible sequences of operations typically explodes exponentially with $n$, making simulation infeasible.

Another subtle edge case is when $n = 1$. In that case the grid is only $2 \times 2$, and the number of possible configurations is very small. Any formula must correctly handle this base case without relying on asymptotic approximations.

## Approaches

If we try to think directly about the process, every configuration comes from repeatedly applying the allowed connection operation in the $2n \times 2n$ grid. A brute-force approach would enumerate all possible sequences of operations, construct the resulting graph each time, and insert it into a set.

This is conceptually correct because it explores the full state space of the process. However, the number of possible operation sequences grows exponentially with the size of the grid. Even for moderate $n$, the number of states becomes far beyond computational limits. The bottleneck is not just time per construction, but the sheer number of distinct constructions that must be explored.

The key structural observation is that the construction decomposes independently across $n$ layers of the grid. Each layer contributes an independent binary decision: a local structural choice that does not constrain the other layers. Once this decomposition is recognized, the global configuration is fully determined by making $n$ independent choices, each with exactly two possibilities.

This reduces the problem from exploring a complex combinatorial object to counting the number of binary strings of length $n$. Each configuration corresponds uniquely to such a string, so the total number of configurations is $2^n$.

The modulo $m$ requirement then turns the task into modular exponentiation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration of Configurations | Exponential | Exponential | Too slow |
| Independent Layer Decomposition | $O(\log n)$ per test case | $O(1)$ | Accepted |

## Algorithm Walkthrough

The solution relies on computing $2^n \bmod m$ efficiently for each test case.

1. Read $n$ and $m$. The modulus $m$ is specific to each query, so computations cannot be reused across test cases in a straightforward way.
2. If $m = 1$, immediately return 0. Any number modulo 1 is zero, so further computation is unnecessary.
3. Compute $2^n \bmod m$ using binary exponentiation. This works by repeatedly squaring the base and reducing the exponent by half at each step, while applying modulo $m$ at every multiplication.
4. Output the result.

The important point is that the exponent $n$ can be as large as $10^9$, so linear multiplication is impossible. Binary exponentiation ensures that only $O(\log n)$ multiplications are required.

### Why it works

The correctness comes from the decomposition of the configuration space into $n$ independent binary decisions. Each layer of the grid contributes exactly two possible structural states, and choices across layers do not interact. This creates a one-to-one mapping between configurations and binary strings of length $n$. Counting configurations therefore reduces exactly to counting such strings, which is $2^n$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def mod_pow(a, e, mod):
    res = 1 % mod
    a %= mod
    while e > 0:
        if e & 1:
            res = (res * a) % mod
        a = (a * a) % mod
        e >>= 1
    return res

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    if m == 1:
        print(0)
        continue
    print(mod_pow(2, n, m))
```

The code isolates modular exponentiation into a helper function. The iterative binary exponentiation avoids recursion depth issues and keeps memory usage constant.

A subtle implementation detail is the initialization `res = 1 % mod`, which ensures correctness even if `mod` is 1, although that case is already handled explicitly. The base `a` is reduced modulo `m` once at the beginning to prevent unnecessary growth in intermediate multiplications.

## Worked Examples

Consider a small instance where $n = 3$, $m = 10$.

We compute $2^3 \bmod 10$.

| Step | exponent (e) | base (a) | result (res) | action |
| --- | --- | --- | --- | --- |
| start | 3 | 2 | 1 | initial state |
| 1 | 3 | 2 | 2 | multiply res by a |
| 2 | 1 | 4 | 2 | square base |
| 3 | 1 | 4 | 8 | multiply res by a |
| end | 0 | - | 8 | finished |

The result is 8, matching $2^3$.

Now consider $n = 5$, $m = 6$.

We compute $2^5 \bmod 6$.

| Step | exponent (e) | base (a) | result (res) | action |
| --- | --- | --- | --- | --- |
| start | 5 | 2 | 1 | initial state |
| 1 | 5 | 2 | 2 | multiply res by a |
| 2 | 2 | 4 | 2 | square base |
| 3 | 2 | 4 | 2 | skip (even exponent) |
| 4 | 1 | 4 | 2 | square base then multiply |
| end | 0 | - | 2 | finished |

The final result is 2, which matches $32 \bmod 6$.

These traces show how exponentiation reduces repeated multiplication into a logarithmic sequence of squaring and conditional accumulation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T \log n)$ | each test case uses binary exponentiation on exponent $n$ |
| Space | $O(1)$ | only a fixed number of variables are used |

The solution comfortably handles $T = 10^4$ and $n \le 10^9$ because each test case performs at most about 30 multiplications.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def mod_pow(a, e, mod):
        res = 1 % mod
        a %= mod
        while e > 0:
            if e & 1:
                res = (res * a) % mod
            a = (a * a) % mod
            e >>= 1
        return res

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        if m == 1:
            out.append("0")
        else:
            out.append(str(mod_pow(2, n, m)))
    return "\n".join(out)

def run(inp: str) -> str:
    return solve(inp)

# sample-like checks
assert run("1\n1 10\n") == "2"
assert run("1\n3 10\n") == "8"

# custom cases
assert run("1\n0 7\n") == "1", "n=0 base case"
assert run("1\n10 1\n") == "0", "mod 1 case"
assert run("1\n5 6\n") == "2", "mod wrap case"
assert run("2\n1 2\n2 2\n") == "0\n0", "small modulus consistency"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n = 0 case | 1 | empty configuration count |
| m = 1 | 0 | modulo collapse |
| small cycle mod 6 | 2 | non-trivial modular reduction |
| multiple queries | 0 0 | independence of test cases |

## Edge Cases

When $n = 0$, the grid degenerates to an empty construction with exactly one configuration. The algorithm returns $2^0 = 1$, which follows directly from the exponentiation logic since the loop does not execute and the result remains 1.

When $m = 1$, every intermediate value becomes irrelevant because all integers are equivalent modulo 1. The early return avoids unnecessary computation and ensures correctness even though binary exponentiation would still produce 0 in the end.

When $n$ is large, such as $10^9$, repeated multiplication would overflow time limits. Binary exponentiation maintains correctness by preserving the identity $a^{2k} = (a^k)^2$, allowing the computation to remain logarithmic regardless of magnitude.
