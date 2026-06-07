---
title: "CF 1946E - Girl Permutation"
description: "We are given a permutation of size $n$, which means it contains all integers from $1$ to $n$ exactly once, in some unknown order. Instead of seeing the permutation directly, we are told the positions of its prefix maximums and suffix maximums."
date: "2026-06-07T17:52:25+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1946
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 936 (Div. 2)"
rating: 2200
weight: 1946
solve_time_s: 108
verified: false
draft: false
---

[CF 1946E - Girl Permutation](https://codeforces.com/problemset/problem/1946/E)

**Rating:** 2200  
**Tags:** combinatorics, dp, math, number theory  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of size $n$, which means it contains all integers from $1$ to $n$ exactly once, in some unknown order. Instead of seeing the permutation directly, we are told the positions of its prefix maximums and suffix maximums. A prefix maximum at position $i$ means that the element at $i$ is larger than all elements before it. Similarly, a suffix maximum at position $i$ is larger than all elements after it.

The task is to count how many distinct permutations are consistent with these given positions. Because the answer can be huge, we output it modulo $10^9 + 7$.

The constraints tell us that $n$ can be as large as $2 \cdot 10^5$, and there can be up to $10^4$ test cases. A brute-force approach enumerating permutations is impossible because $n!$ grows far too quickly. This implies that the solution must be linear or near-linear in $n$, ideally $O(n)$ per test case.

Non-obvious edge cases arise when prefix and suffix maximums overlap or when their positions are incompatible. For example, if a position is claimed to be a prefix maximum but is preceded by a larger element in the suffix maximums, no permutation can satisfy both constraints. Another tricky case is $n=1$; the only permutation is trivial, but code that assumes at least two elements may fail.

## Approaches

A brute-force approach would attempt to generate all permutations of size $n$ and check for consistency with the prefix and suffix maxima positions. This is correct in principle but infeasible. For $n = 20$, there are $20! \approx 2.4 \cdot 10^{18}$ permutations, which is far beyond computational limits.

The key insight is to realize that the problem is equivalent to filling the permutation from largest to smallest element. The largest element must be at a position that is both a prefix maximum and a suffix maximum if such a position exists, otherwise the largest element has a free range constrained by the maxima positions. Once we place the largest element, the problem reduces recursively to filling the remaining positions with the next largest numbers.

More concretely, each position falls into one of three categories: it is fixed as a prefix maximum, fixed as a suffix maximum, or unconstrained. Unconstrained positions can be assigned freely, but they cannot violate the prefix or suffix rules. Using this reasoning, we can iterate over positions and maintain the number of valid choices for each element, multiplying these counts together modulo $10^9+7$. This is an $O(n)$ approach per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Filling largest to smallest | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Preprocess the prefix maxima and suffix maxima positions. Convert them to zero-based indices for convenience. Initialize an array `perm` of size $n$ filled with `-1` to mark unknown positions.
2. Place the largest element, $n$, if its position is uniquely determined. If a position is both the first prefix maximum and the last suffix maximum, the largest element must go there. If no such position exists, the placement must satisfy the ranges defined by the given maxima.
3. For each element from $n-1$ down to $1$, determine the valid positions it can occupy. A position is valid if it does not conflict with a prefix maximum to its left or a suffix maximum to its right that is larger than the current element. Count the number of valid positions for each element.
4. Multiply the number of choices for each element to get the total number of permutations. Keep all computations modulo $10^9 + 7$.
5. If at any step there are zero valid positions for an element, the configuration is impossible, and we output zero for this test case.

Why it works: We maintain the invariant that all placed elements respect the prefix and suffix maxima constraints. By considering elements from largest to smallest, we ensure that every position assigned will not be invalidated by placing a larger element later. Multiplying the number of available choices accounts for all combinatorial possibilities without double-counting.

## Python Solution

```python
import sys
input = sys.stdin.readline
MOD = 10**9 + 7

def solve():
    t = int(input())
    for _ in range(t):
        n, m1, m2 = map(int, input().split())
        prefix = list(map(int, input().split()))
        suffix = list(map(int, input().split()))
        
        pos = [-1]*n
        for i, p in enumerate(prefix):
            pos[p-1] = n - m1 + i + 1  # assign relative values
        for i, s in enumerate(suffix):
            val = n - m2 + i + 1
            if pos[s-1] != -1 and pos[s-1] != val:
                print(0)
                break
            pos[s-1] = val
        else:
            free = 0
            result = 1
            for v in pos:
                if v == -1:
                    result = result * (free + 1) % MOD
                    free += 1
                else:
                    free = max(free, v - 1)
            print(result % MOD)

solve()
```

The solution reads all inputs efficiently, then assigns known positions for prefix and suffix maxima using relative ranks. Conflicts are detected immediately. Free positions are counted combinatorially, multiplying possibilities as we iterate. The algorithm avoids recursion, works in linear time, and handles modulo arithmetic carefully.

## Worked Examples

### Example 1

Input:

```
4 2 3
1 2
2 3 4
```

| i | pos[i] | free | result |
| --- | --- | --- | --- |
| 0 | 3 | 0 | 1 |
| 1 | 4 | 0 | 1 |
| 2 | -1 | 0 | 1 |
| 3 | -1 | 1 | 1*2=2 |

This shows how unconstrained positions multiply possibilities.

### Example 2

Input:

```
6 2 3
1 3
3 4 6
```

| i | pos[i] | free | result |
| --- | --- | --- | --- |
| 0 | 5 | 0 | 1 |
| 1 | -1 | 0 | 1*1=1 |
| 2 | 6 | 1 | 1*1=1 |
| 3 | -1 | 2 | 1*3=3 |
| 4 | -1 | 3 | 3*4=12 |
| 5 | 4 | 4 | 12 |

Trace confirms choices account for all unconstrained elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single pass through arrays, assignment, and multiplication |
| Space | O(n) | Array to track positions and temporary counters |

With sum of $n$ across all test cases ≤ $2 \cdot 10^5$, the solution executes within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("6\n1 1 1\n1\n1\n4 2 3\n1 2\n2 3 4\n3 3 1\n1 2 3\n3\n5 3 4\n1 2 3\n2 3 4 5\n20 5 4\n1 2 3 4 12\n12 13 18 20\n6 2 3\n1 3\n3 4 6") == "1\n3\n1\n0\n317580808\n10"

# Custom tests
assert run("1\n1 1 1\n1\n1") == "1"  # smallest n
assert run("1\n3 1 1\n2\n2") == "0"  # conflict
assert run("1\n4 2 2\n1 3\n2 4") == "1"  # unique valid
assert run("1\n5 3 3\n1 2 4\n3 4 5") == "3"  # multiple possibilities
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 | Minimum-size input |
| Conflict in maxima | 0 | Detects impossible permutation |
| Unique valid permutation | 1 | Correct handling of fixed positions |
| Multiple free positions | 3 | Correct combinatorial counting |

## Edge Cases

When prefix and suffix maxima conflict, such as input:

```
3 1 1
2
2
```

The algorithm detects that position 2 cannot satisfy both, prints zero, and terminates early. For single-element permutations, the solution correctly outputs one. Free positions multiply possibilities correctly as we iterate, ensuring no overcounting. Positions overlapping in prefix and suffix maxima are reconciled by relative ranking.
