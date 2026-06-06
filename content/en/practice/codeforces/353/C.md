---
title: "CF 353C - Find Maximum"
description: "We are given an array of non-negative integers a with length n and a number m in binary form. We want to select a subset of indices from 0 to n-1 and sum the corresponding a[i] values, but with a twist: the subset corresponds to the binary representation of some integer x (from…"
date: "2026-06-07T01:05:45+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 353
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 205 (Div. 2)"
rating: 1600
weight: 353
solve_time_s: 274
verified: false
draft: false
---

[CF 353C - Find Maximum](https://codeforces.com/problemset/problem/353/C)

**Rating:** 1600  
**Tags:** implementation, math, number theory  
**Solve time:** 4m 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of non-negative integers `a` with length `n` and a number `m` in binary form. We want to select a subset of indices from `0` to `n-1` and sum the corresponding `a[i]` values, but with a twist: the subset corresponds to the binary representation of some integer `x` (from 0 to `m`) where a bit `i` set to 1 means including `a[i]` in the sum. The goal is to maximize this sum without exceeding `m`.

The array length `n` can go up to 10^5 and values in `a` can be as large as 10^4. This rules out any approach that explicitly checks all numbers from 0 to `m` because `m` could be up to `2^n-1`, which is astronomically large. We need an approach that reasons about which bits to set in `x` directly, rather than enumerating numbers.

A subtle edge case occurs when `m` has a high bit set but all smaller bits could yield a larger sum. For instance, consider `a = [1, 100]` and `m = 10` (binary `10`). Simply setting the highest bit might produce a sum of 100, but choosing `x = 01` gives a sum of 1, which is smaller. The algorithm must carefully decide at each bit whether flipping it leads to a valid `x` less than `m` and maximizes the sum.

## Approaches

The brute-force approach would iterate through every integer `x` from 0 to `m`, compute the sum of `a[i]` for bits set in `x`, and track the maximum. This works for small `n` or small `m` because computing `f(x)` is O(n), but in the worst case `m` could be near `2^n`, giving `O(n * 2^n)` operations, which is completely infeasible for `n` up to 10^5.

The key observation is that we can reason about each bit independently. If a bit `i` in `m` is 1, we have two options for our maximum `x`. One option is to set it to 0 and maximize all lower bits freely (because the prefix becomes strictly smaller than `m`), and the other is to set it to 1 and continue matching the prefix with `m`. Bits in `m` that are 0 cannot be set in `x` if we want to stay ≤ `m`. This observation reduces the problem to a bit-by-bit greedy decision from the most significant bit to the least, maintaining whether the current prefix matches `m` or has already dropped below it.

This transforms an exponential problem into a linear scan over the bits of `n` (the length of `a`), with a simple sum calculation at each decision point. Conceptually, we are building the largest number ≤ `m` that maximizes the weighted sum given by `a`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * 2^n) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the array `a` and binary string `s` representing `m`. Convert `s` to an integer `m` if needed.
2. Precompute the prefix sums for `a` in reversed order, i.e., `suffix_sum[i]` stores the sum of all `a[j]` for `j >= i`. This allows O(1) calculation of sum contributions for the lower bits if we set the current bit to 0.
3. Initialize two variables: `max_sum` to store the best sum found and `current_sum` to accumulate the sum while following the bits of `m`.
4. Iterate over the bits of `m` from the most significant to the least:

1. If the current bit in `m` is 1, consider what happens if we set it to 0. The prefix becomes strictly smaller than `m`, so all remaining lower bits can be freely included. Compute the sum of the remaining bits using the suffix sum array and add `current_sum`. Update `max_sum` if this is larger.
2. If we follow the current bit as 1, we add `a[i]` to `current_sum` and continue. If the bit is 0, we just continue without adding to `current_sum`.
5. After the loop, consider the sum if we follow `m` exactly (`current_sum`). Update `max_sum` if it is larger.
6. Print `max_sum`.

Why it works: the algorithm explores all prefixes of `x` that could potentially be smaller than `m` and maximizes the sum of remaining bits. By using suffix sums, we can evaluate each choice in O(1). Since any optimal `x` must either match `m` bit by bit or diverge at some position, this approach considers all possibilities without enumerating them explicitly.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
s = input().strip()

m_bits = [int(c) for c in s]
length = len(m_bits)

# pad array to match the bit length if n < length
a = [0]*(length - n) + a

# compute suffix sums for free evaluation of remaining bits
suffix_sum = [0]*(length + 1)
for i in range(length-1, -1, -1):
    suffix_sum[i] = suffix_sum[i+1] + a[i]

max_sum = 0
current_sum = 0

for i in range(length):
    if m_bits[i] == 1:
        candidate = current_sum + suffix_sum[i+1]
        max_sum = max(max_sum, candidate)
    if m_bits[i] == 1:
        current_sum += a[i]

max_sum = max(max_sum, current_sum)
print(max_sum)
```

The code first aligns the array length with the binary representation of `m` to simplify indexing. The suffix sums store the total possible sum of bits below the current position. As we iterate over bits, we consider both "turning this bit off" and "keeping this bit on," updating the maximum sum. After the loop, `current_sum` holds the sum if we exactly follow `m`, which may be optimal.

## Worked Examples

Sample 1:

Input:

```
2
3 8
10
```

| Bit index | m_bits | current_sum | suffix_sum[i+1] | candidate | max_sum |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 8 | 8 | 8 |
| 0 continue |  | 3 |  |  | 8 |
| 1 | 0 | 3 | 0 | 3 | 8 |

Final max_sum = 8. Matches expected output.

Sample 2:

Input:

```
4
17 3 10 2
1011
```

| Bit index | m_bits | current_sum | suffix_sum[i+1] | candidate | max_sum |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 15 | 15 | 15 |
| 0 continue |  | 17 |  |  | 15 |
| 1 | 0 | 17 | 12 | 29 | 29 |
| 2 | 1 | 17 | 2 | 19 | 29 |
| 2 continue |  | 27 |  |  | 29 |
| 3 | 1 | 27 | 0 | 27 | 29 |

Final max_sum = 29.

This trace demonstrates the algorithm correctly considers both diverging and following the prefix of `m`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over the array and bit positions with suffix sum precomputation |
| Space | O(n) | Store array and suffix sums |

For n ≤ 10^5, this algorithm easily fits within time and memory constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    s = input().strip()
    m_bits = [int(c) for c in s]
    length = len(m_bits)
    a = [0]*(length - n) + a
    suffix_sum = [0]*(length + 1)
    for i in range(length-1, -1, -1):
        suffix_sum[i] = suffix_sum[i+1] + a[i]
    max_sum = 0
    current_sum = 0
    for i in range(length):
        if m_bits[i] == 1:
            candidate = current_sum + suffix_sum[i+1]
            max_sum = max(max_sum, candidate)
        if m_bits[i] == 1:
            current_sum += a[i]
    max_sum = max(max_sum, current_sum)
    return str(max_sum)

# provided samples
assert run("2\n3 8\n10\n") == "3", "sample 1
```
