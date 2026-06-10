---
title: "CF 1421A - XORwice"
description: "The problem asks for the minimum sum of two XOR operations for a pair of integers a and b when XORed with the same number x. Concretely, given a and b, we must choose x such that the expression (a XOR x) + (b XOR x) is as small as possible."
date: "2026-06-11T06:36:15+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1421
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 676 (Div. 2)"
rating: 800
weight: 1421
solve_time_s: 616
verified: true
draft: false
---

[CF 1421A - XORwice](https://codeforces.com/problemset/problem/1421/A)

**Rating:** 800  
**Tags:** bitmasks, greedy, math  
**Solve time:** 10m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks for the minimum sum of two XOR operations for a pair of integers `a` and `b` when XORed with the same number `x`. Concretely, given `a` and `b`, we must choose `x` such that the expression `(a XOR x) + (b XOR x)` is as small as possible. The input provides multiple such pairs of integers, and the output is the minimum sum for each pair.

Given the constraints, `1 ≤ a, b ≤ 10^9` and up to `10^4` test cases, a brute-force search over all possible `x` values is impossible, because iterating over numbers up to `10^9` for each test case would require trillions of operations. This forces us to reason about the XOR operation itself rather than trying every `x`.

A non-obvious edge case arises when `a` equals `b`. Choosing `x = a` results in both `a XOR x` and `b XOR x` becoming zero. A careless approach that tries `x = 0` or some other arbitrary number could fail this case. Another subtlety is that each bit of `x` can independently minimize the contribution of that bit in `a XOR x + b XOR x`. Mismanaging bitwise logic can lead to incorrect results.

## Approaches

The brute-force approach would attempt all `x` values from `0` to some upper limit, compute `(a XOR x) + (b XOR x)` for each, and pick the minimum. This works in principle, but the complexity is `O(max(a, b))` per test case, which is too slow for the upper constraints.

The key insight is to consider the XOR operation at the bit level. For each bit position, we can independently determine whether `x` should have a `0` or `1` to minimize the sum of `a XOR x + b XOR x`. The contribution of a single bit is as follows: if the bit is `0` in both `a` and `b`, any `x` bit will leave the sum unchanged. If one of them is `1`, choosing `x` to match the `1` bit reduces the total sum for that bit. Working this through carefully leads to the simple observation: choosing `x = a AND b` minimizes the sum for all bits. With this choice, `(a XOR x) + (b XOR x)` becomes `a + b - 2 * (a & b)`. This formula is derived from the identity `a XOR b = a + b - 2*(a & b)`.

This transforms the problem from trying all `x` to computing a single formula in constant time per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(max(a, b)) per test | O(1) | Too slow |
| Optimal | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read integers `a` and `b`.
3. Compute `x = a & b`. This choice guarantees minimal sum because it preserves all common `1` bits and avoids adding extra ones.
4. Compute the minimum sum using the formula `(a XOR x) + (b XOR x)`. Equivalently, this is `a + b - 2 * x`.
5. Output the result.

Why it works: Choosing `x = a & b` ensures that every bit that is `1` in both `a` and `b` contributes `0` to the sum, while any differing bits are handled optimally. The invariant is that for every bit position, the sum of the XORs is minimized independently, so the total sum is globally minimized.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b = map(int, input().split())
    x = a & b
    result = (a ^ x) + (b ^ x)
    print(result)
```

The code reads input efficiently, computes `x` using the bitwise AND operator, and calculates the result using XOR. Using `a & b` directly avoids iterative bit manipulations and prevents off-by-one errors.

## Worked Examples

Sample 1:

| a | b | x = a & b | a^x | b^x | (a^x)+(b^x) |
| --- | --- | --- | --- | --- | --- |
| 6 | 12 | 4 | 2 | 8 | 10 |

The table shows that choosing `x = 4` (which is `6 & 12`) minimizes the sum. Any other `x` would produce a larger sum.

Sample 2:

| a | b | x = a & b | a^x | b^x | (a^x)+(b^x) |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 0 | 0 |

This demonstrates the edge case where `a = b`. The minimum sum is `0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case takes constant time, only bitwise operations and arithmetic. |
| Space | O(1) | No extra memory beyond input variables. |

Given `t ≤ 10^4`, this solution easily fits in the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())
        x = a & b
        output.append(str((a ^ x) + (b ^ x)))
    return "\n".join(output)

# provided samples
assert run("6\n6 12\n4 9\n59 832\n28 14\n4925 2912\n1 1\n") == "10\n13\n891\n18\n6237\n0", "sample 1"

# custom cases
assert run("3\n1 2\n7 7\n0 15\n") == "3\n0\n15", "custom cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 | 3 | minimal sum for small integers |
| 7 7 | 0 | identical numbers edge case |
| 0 15 | 15 | zero and large number edge case |

## Edge Cases

When `a = b`, choosing `x = a & b` correctly produces zero because `(a XOR a) + (b XOR b) = 0`. When `a` or `b` is zero, the formula still works because `(0 XOR x) = x`, and `(b XOR x)` complements it, yielding `b` as the minimum sum when `x = 0`.

For `a = 0, b = 15`:

| a | b | x = a & b | a^x | b^x | sum |
| --- | --- | --- | --- | --- | --- |
| 0 | 15 | 0 | 0 | 15 | 15 |

The algorithm handles all single-bit differences correctly, demonstrating its correctness across the full domain.
