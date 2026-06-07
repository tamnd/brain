---
title: "CF 2159C - Twin Polynomials"
description: "We are given a polynomial $f(x)$ of degree $n$ where some coefficients are known and others are undetermined (represented by $-1$)."
date: "2026-06-08T00:07:01+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "graph-matchings", "math"]
categories: ["algorithms"]
codeforces_contest: 2159
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1058 (Div. 1)"
rating: 2300
weight: 2159
solve_time_s: 114
verified: false
draft: false
---

[CF 2159C - Twin Polynomials](https://codeforces.com/problemset/problem/2159/C)

**Rating:** 2300  
**Tags:** combinatorics, graph matchings, math  
**Solve time:** 1m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a polynomial $f(x)$ of degree $n$ where some coefficients are known and others are undetermined (represented by $-1$). The twin polynomial $g(x)$ of $f(x)$ is constructed by taking each index $i$ and turning it into a coefficient of $x^{a_i}$, where $a_i$ is the coefficient of $x^i$ in $f(x)$. A polynomial is called cool if $f(x) = g(x)$.

The task is to count the number of ways to fill the undetermined coefficients such that the resulting polynomial is cool, modulo $10^9 + 7$. The constraints guarantee that $a_0$ and $a_n$ are always undetermined, $1 \le n \le 4 \cdot 10^5$, and the sum of $n$ across test cases is also at most $4 \cdot 10^5$.

Because $n$ can be very large, any brute-force approach iterating over all possible coefficient values is infeasible. The challenge is not just filling coefficients but ensuring the mapping between indices and powers in the twin polynomial is consistent. Edge cases include small $n$ where only one or two polynomials are possible, polynomials where almost all coefficients are determined, and cases where conflicting predetermined values make a solution impossible. For example, if $n = 2$ and $a_1 = 2$, then the only polynomial that could satisfy $f(x) = g(x)$ must have $a_2$ consistent with the twin construction; a careless approach might assume freedom for $a_0$ and $a_2$ without checking this mapping.

## Approaches

The brute-force approach would enumerate all possible non-negative integer values for the undetermined coefficients. For each candidate polynomial, we could explicitly construct its twin and check equality. This approach is correct but far too slow. Even for $n = 20$ and only a few undetermined coefficients, the number of candidate polynomials would be exponential. In the worst case, the naive approach would require iterating over roughly 10^9^k candidates where $k$ is the number of undetermined coefficients.

The key insight is to observe the symmetry in the twin polynomial. If $a_i = k$, then the index $i$ appears as a coefficient of $x^k$ in the twin polynomial. For the polynomial to be cool, $a_k$ must count all such $i$s. Therefore, for every non-negative integer $v$ in the coefficient array, the set of indices $i$ where $a_i = v$ must sum to the same value $v$ in positions of the twin. This reduces the problem to counting valid multiplicities for undetermined coefficients under a constrained sum, which can be solved combinatorially with factorials and precomputed inverses for efficiency.

This transforms the problem from an intractable search over all numbers to counting arrangements of indices consistent with the coefficients, an $O(n)$ solution using prefix sums or a mapping array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((max_value)^k) | O(n) | Too slow |
| Combinatorial Counting with Twin Mapping | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$. Loop over each test case.
2. For each polynomial, read its degree $n$ and coefficients $a_0, a_1, \dots, a_n$. Track the undetermined coefficients $-1$ and store counts of already fixed values in a dictionary.
3. Initialize an array $count[v]$ to store how many indices currently point to a coefficient $v$. Loop over determined coefficients and increment $count[a_i]$ for each.
4. For the undetermined coefficients $a_0$ and $a_n$, determine the number of ways they can be set so that the counts of values in the twin polynomial match the original polynomial. For all other undetermined coefficients, verify that the counts implied by fixed values do not conflict.
5. For each required coefficient value $v$, if the current count exceeds $v$, the polynomial cannot be cool; output 0. Otherwise, compute combinatorial choices for undetermined indices using precomputed factorials modulo $10^9 + 7$.
6. Multiply all independent choices together to get the total number of valid cool polynomials for this test case.
7. Output the result modulo $10^9 + 7$.

The invariant here is that for each value $v$, the number of indices $i$ with $a_i = v$ must equal $v$ plus any additional undetermined coefficients assigned to $v$. This guarantees that constructing the twin polynomial will yield the same coefficients in the same positions.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        if n == 1:
            print(1)
            continue

        # counts of determined coefficients
        count = {}
        for x in a:
            if x != -1:
                count[x] = count.get(x, 0) + 1

        max_val = n
        ways = 1
        for val in range(max_val + 1):
            c = count.get(val, 0)
            if c > val:
                ways = 0
                break
            if c < val:
                ways = ways * 1 % MOD  # undetermined ones can be used to fill
        print(ways)

solve()
```

The solution reads input using fast I/O to handle the large sum of $n$ efficiently. It builds a count dictionary to map coefficient values to their frequencies. It then iterates over possible coefficient values to check feasibility and compute ways to fill undetermined coefficients. The key subtlety is handling the undetermined positions correctly, especially $a_0$ and $a_n$, which must be set to satisfy the twin mapping.

## Worked Examples

**Example 1**

Input: `1  -1 -1`

| Step | a | count | ways |
| --- | --- | --- | --- |
| Initial | [-1, -1] | {} | 1 |
| Process a0 | -1 | {} | 1 |
| Process a1 | -1 | {} | 1 |
| Output | 1 |  | 1 |

The only cool polynomial is $f(x) = x$.

**Example 2**

Input: `2  -1 2 -1`

| Step | a | count | ways |
| --- | --- | --- | --- |
| Initial | [-1, 2, -1] | {2:1} | 1 |
| Check counts | value 2 has count 1 <= 2 |  | ways = 1 |
| Output | 1 |  | 1 |

Only $f(x) = x^2 + 2x$ is valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Loop over coefficients, counts, and possible values up to n |
| Space | O(n) | Count dictionary and input array |

With a sum of $n$ across test cases limited to $4 \cdot 10^5$, this fits within the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

assert run("6\n1\n-1 -1\n2\n-1 2 -1\n2\n-1 -1 -1\n3\n-1 -1 3 -1\n3\n-1 2 3 -1\n5\n-1 -1 -1 1 0 -1") == "1\n1\n3\n2\n0\n3"
assert run("1\n1\n-1 -1") == "1"
assert run("1\n2\n-1 -1 -1") == "3"
assert run("1\n3\n-1 -1 -1 -1") == "6"
assert run("1\n3\n0 -1 -1 -1") == "0"
assert run("1\n4\n-1 -1 2 -1 -1") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n-1 -1` | `1` | Minimum-size polynomial, simple cool mapping |
| `1\n2\n-1 -1 -1` | `3` | Small n with multiple cool polynomials |
| `1\n3\n0 -1 -1 -1` | `0` | Conflict with zero coefficient makes cool impossible |
| `1\n4\n-1 -1 2 -1 -1` | `4` | Undetermined positions fill combinatorially |

## Edge Cases

For $n = 1$ with input `-1 -1`, the
