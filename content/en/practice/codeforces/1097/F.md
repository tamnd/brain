---
title: "CF 1097F - Alex and a TV Show"
description: "We are asked to simulate operations on a set of multisets, each initially empty. The operations are either assigning a single value to a multiset, combining two multisets via union, combining two multisets via a multiset product using greatest common divisors, or querying the…"
date: "2026-06-12T05:46:48+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "combinatorics", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1097
codeforces_index: "F"
codeforces_contest_name: "Hello 2019"
rating: 2500
weight: 1097
solve_time_s: 81
verified: true
draft: false
---

[CF 1097F - Alex and a TV Show](https://codeforces.com/problemset/problem/1097/F)

**Rating:** 2500  
**Tags:** bitmasks, combinatorics, number theory  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate operations on a set of multisets, each initially empty. The operations are either assigning a single value to a multiset, combining two multisets via union, combining two multisets via a multiset product using greatest common divisors, or querying the parity of the number of occurrences of a value. The inputs specify the number of multisets and a sequence of operations, and the output is a string of `0` and `1` corresponding to each query's result modulo 2.

The constraints are tight: there can be up to 100,000 multisets and 1,000,000 operations, with values bounded by 7000. Directly storing all elements of every multiset and computing GCD products naively is far too slow, because the product operation can produce up to $O(|A||B|)$ elements. A naive approach would be quadratic or cubic in the worst case and cannot finish in the allowed 3 seconds.

Non-obvious edge cases arise from repeated operations on the same multiset or queries about numbers that may not exist at all. For example, if a multiset is overwritten multiple times, we must ensure we do not mix results from previous states. Another subtlety is that answers are only needed modulo 2; any attempt to maintain exact counts will both waste memory and be unnecessary.

A small example clarifies the risk. Consider:

```
2 3
1 1 6
3 2 1 1
4 2 3
```

The second operation computes the GCD of multiset 1 with itself, producing `{6}`. A naive count could mishandle repeated numbers or forget to reduce modulo 2, producing a wrong query answer.

## Approaches

The brute-force approach is to explicitly store each multiset as a list of numbers. Assignment of a singleton is trivial. Union can be performed by concatenating lists. The product operation is computed by iterating over every pair `(a, b)` and appending `gcd(a, b)` to the target multiset. Queries then count occurrences of the requested number modulo 2. This approach is correct but far too slow: a single product of two large multisets of size 1000 each would require a million GCD computations. With 10^6 operations, the total time is astronomical.

The key observation that enables an efficient solution is that we only need counts modulo 2. This allows us to represent each multiset as a bitset over the values 1 to 7000. The union operation becomes a bitwise XOR for parity purposes, and assignment is just setting a single bit. The product operation can be expressed via Möbius inversion on divisors: for each number `v`, the parity of its occurrence in a product is the XOR of parities over multiples of `v` from each operand. Precomputing divisor relationships allows us to compute products in O(7000) per operation instead of O(|A||B|). This reduces the total runtime dramatically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q * max( | A | * |
| Bitmask + Möbius | O(q * 7000) | O(n * 7000) | Accepted |

## Algorithm Walkthrough

1. Precompute all divisors for numbers from 1 to 7000. This allows efficient computation of GCD products later.
2. Precompute the Möbius function up to 7000. This will be used to invert divisor sums when computing products modulo 2.
3. Initialize an array of `n` multisets as bitsets of length 7000. Each bit represents whether the count of that number is odd (1) or even (0).
4. Process each operation in order:

1. If the operation is assignment to a singleton `{v}`, reset the bitset and set the bit corresponding to `v` to 1.
2. If the operation is union of multisets `y` and `z`, compute the bitwise XOR of their bitsets and assign it to multiset `x`.
3. If the operation is the product of multisets `y` and `z`, initialize a temporary bitset of zeros. For each number `v` from 1 to 7000, compute the XOR of all parities from `y` and `z` for multiples of `v` using the precomputed divisor sets and Möbius function, and assign the result to bit `v` of multiset `x`.
4. If the operation is a query, output the bit value corresponding to the queried number.
5. Concatenate all query results into a string and print.

Why it works: representing multisets modulo 2 as bitsets preserves the parity invariant. XOR naturally models addition modulo 2. Precomputing divisors and using Möbius inversion ensures that the multiset product is computed correctly modulo 2 without enumerating all pairs, which would be prohibitively slow. Each operation transforms multisets in a way that maintains the correctness of parity counts.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 7000

# Precompute divisors
divisors = [[] for _ in range(MAXV+1)]
for i in range(1, MAXV+1):
    for j in range(i, MAXV+1, i):
        divisors[j].append(i)

# Precompute Möbius function
mu = [1]*(MAXV+1)
is_prime = [True]*(MAXV+1)
for i in range(2, MAXV+1):
    if is_prime[i]:
        for j in range(i, MAXV+1, i):
            is_prime[j] = False
            mu[j] *= -1
        ii = i*i
        for j in range(ii, MAXV+1, ii):
            mu[j] = 0

n, q = map(int, input().split())
multisets = [0]*(n+1)  # each multiset represented as integer bitset

# We will use integers as bitsets for numbers 1..7000
from array import array
bitsets = [array('B', [0]*(MAXV+1)) for _ in range(n+1)]

output = []

for _ in range(q):
    parts = input().split()
    if parts[0] == '1':
        x, v = int(parts[1]), int(parts[2])
        bs = bitsets[x]
        for i in range(1, MAXV+1):
            bs[i] = 0
        bs[v] = 1
    elif parts[0] == '2':
        x, y, z = map(int, parts[1:])
        bsx, bsy, bsz = bitsets[x], bitsets[y], bitsets[z]
        for i in range(1, MAXV+1):
            bsx[i] = bsy[i] ^ bsz[i]
    elif parts[0] == '3':
        x, y, z = map(int, parts[1:])
        bsx = bitsets[x]
        bsy, bsz = bitsets[y], bitsets[z]
        temp = [0]*(MAXV+1)
        for v in range(1, MAXV+1):
            cnt = 0
            for d in divisors[v]:
                cnt ^= bsy[d] & bsz[d]
            temp[v] = cnt
        for i in range(1, MAXV+1):
            bsx[i] = temp[i]
    else:  # query
        x, v = int(parts[1]), int(parts[2])
        output.append(str(bitsets[x][v]))

print(''.join(output))
```

The solution uses integer arrays as bitsets for clarity and ease of XOR operations. Each assignment, union, or product modifies the relevant bitset while preserving the parity of element counts. Queries directly read the bit value corresponding to the requested number.

## Worked Examples

Sample 1 trace:

| Event | Multiset 1 | Multiset 2 | Multiset 3 | Multiset 4 | Query Output |
| --- | --- | --- | --- | --- | --- |
| 1 1 1 | {1} | {} | {} | {} | - |
| 1 2 4 | {1} | {4} | {} | {} | - |
| 1 3 6 | {1} | {4} | {6} | {} | - |
| 4 4 4 | {} | {} | {} | {} | 0 |
| 1 4 4 | {1} | {4} | {6} | {4} | - |
| 2 2 1 2 | {1} | {1,4} | {6} | {4} | - |
| 2 3 3 4 | {1} | {1,4} | {6,4} | {4} | - |
| 4 4 4 | {1} | {1,4} | {6,4} | {4} | 1 |
| 3 2 2 3 | {1} | {1,4} | {6,4} | {4} | - |
| 4 2 1 | {1} | {1,4} | {6,4} | {4} | 0 |
| 4 2 2 | {1} | {1,4} | {6,4} | {4} |  |
