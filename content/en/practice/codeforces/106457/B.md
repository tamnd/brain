---
title: "CF 106457B - Bespin"
description: "The task is essentially about choosing a non-empty subset of ships, where each ship is distinct, and counting how many of those subsets have an odd size. You are given a single integer $n$, representing how many distinct ships are available."
date: "2026-06-25T09:13:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106457
codeforces_index: "B"
codeforces_contest_name: "UTPC Spring 2026 Open Contest"
rating: 0
weight: 106457
solve_time_s: 38
verified: true
draft: false
---

[CF 106457B - Bespin](https://codeforces.com/problemset/problem/106457/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is essentially about choosing a non-empty subset of ships, where each ship is distinct, and counting how many of those subsets have an odd size.

You are given a single integer $n$, representing how many distinct ships are available. Every subset of ships corresponds to a possible fleet. However, only subsets whose size is odd are considered valid. The empty subset is excluded automatically since a fleet must contain at least one ship.

So the problem reduces to counting how many subsets of a set of size $n$ have odd cardinality.

If we think in terms of raw enumeration, each ship can either be included or excluded, so there are $2^n$ total subsets. Among these, we want exactly those where the number of chosen elements is odd.

A small example clarifies the structure. If $n = 3$, the subsets are:

$\{\}, \{1\}, \{2\}, \{3\}, \{1,2\}, \{1,3\}, \{2,3\}, \{1,2,3\}$.

Odd-sized subsets are the singletons and the full set, giving $3 + 1 = 4$.

The constraints allow $n \le 60$, which immediately rules out any approach that explicitly enumerates subsets. Even $2^{60}$ is far beyond computational reach. Anything exponential in $n$ is too slow unless it reduces to a constant-time formula.

A subtle edge case appears when $n = 1$. The only subset is $\{1\}$, which is valid since its size is 1. The correct answer is 1. A naive implementation that mistakenly includes the empty set or miscounts parity would fail here.

Another case is $n = 2$. The subsets are $\{1\}, \{2\}$, both valid, so the answer is 2. This already suggests a symmetry between odd and even subset counts, which becomes the key structural insight.

## Approaches

A brute-force approach would generate all $2^n$ subsets and count those whose size is odd. Conceptually this is straightforward: iterate over every bitmask from 0 to $2^n - 1$, count set bits, and increment the answer if the parity is odd. This is correct because each subset is represented exactly once and parity is well-defined.

The issue is runtime. Even for $n = 40$, $2^{40}$ is already about $10^{12}$ operations, which is far beyond feasible limits. The problem size up to 60 makes this completely unusable.

The key observation is that subsets of a finite set distribute evenly across parity classes. Each subset can be paired with another subset that differs only by toggling a fixed element. This pairing flips parity, creating a one-to-one correspondence between even-sized and odd-sized subsets.

More concretely, consider all subsets of $n$ elements. If we take any subset $S$, toggling the presence of the first element maps it to a distinct subset $S'$. One of these has even size, the other has odd size. This partitions the entire power set into pairs, meaning exactly half of all subsets are odd-sized.

Since there are $2^n$ total subsets, exactly $2^{n-1}$ of them have odd cardinality.

The empty set does not affect this argument because it is paired with the singleton set containing the chosen element, so it is already accounted for in the pairing structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n 2^n)$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the integer $n$, which represents the number of distinct ships.
2. Recognize that every subset corresponds to a binary choice per ship, giving $2^n$ total subsets. The goal is not to enumerate them but to compute how many have odd size.
3. Use the structural fact that subsets can be paired by flipping membership of a fixed element, which guarantees an equal split between even and odd sizes.
4. Conclude that the number of valid fleets is $2^{n-1}$.
5. Compute this value directly using fast exponentiation or bit shifting.

The only computational work is evaluating a power of two, which can be done in constant or logarithmic time depending on implementation.

### Why it works

The invariant is that toggling a fixed element defines a bijection between subsets of even size and subsets of odd size. Every subset either contains the chosen element or it does not, and flipping that membership changes the parity without creating collisions. Since this mapping is reversible and covers the entire power set, the two parity classes must have equal size, forcing each to contain exactly half of all subsets.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
print(1 << (n - 1))
```

The solution relies on bit shifting instead of `pow(2, n-1)` because it is both simpler and avoids floating-point conversion issues, even though Python’s integers would handle both safely. The shift directly constructs $2^{n-1}$.

The only subtlety is the case $n = 1$, where the shift becomes $1 << 0 = 1$, matching the correct answer.

## Worked Examples

### Example 1: n = 3

We track how subsets split by size parity.

| Subset size | Count |
| --- | --- |
| 0 | 1 |
| 1 | 3 |
| 2 | 3 |
| 3 | 1 |

Odd-sized subsets are those of size 1 and 3.

This confirms the pairing intuition: every even subset has a corresponding odd subset obtained by toggling a fixed element.

Output is $2^{2} = 4$.

### Example 2: n = 4

| Subset size | Count |
| --- | --- |
| 0 | 1 |
| 1 | 4 |
| 2 | 6 |
| 3 | 4 |
| 4 | 1 |

Odd subsets total $4 + 4 = 8$, which matches $2^{3}$.

This example reinforces that the distribution is symmetric regardless of $n$, not dependent on small cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Computing a single power of two via bit shift |
| Space | $O(1)$ | Only one integer is stored |

The constraints allow $n \le 60$, so the result fits easily within a 64-bit integer range, and Python handles it natively without overflow issues.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    n = int(input().strip())
    return str(1 << (n - 1))

# provided samples
assert run("3\n") == "4"

# custom cases
assert run("1\n") == "1", "minimum size"
assert run("2\n") == "2", "small even split"
assert run("4\n") == "8", "basic binomial symmetry"
assert run("60\n") == str(1 << 59), "maximum boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | smallest valid case |
| 2 | 2 | correct split for tiny even n |
| 4 | 8 | general symmetry |
| 60 | 2^59 | upper bound handling |

## Edge Cases

For $n = 1$, there is only one subset: the single ship. The algorithm computes $2^{0} = 1$, which correctly counts it as valid since its size is odd.

For larger values like $n = 60$, the result becomes a very large integer, but Python handles arbitrary precision integers, so no overflow or precision issues occur. The computation remains a single bit shift, so execution is constant time and stable even at the boundary.
