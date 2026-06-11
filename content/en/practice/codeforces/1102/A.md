---
title: "CF 1102A - Integer Sequence Dividing"
description: "We are given the sequence of integers from 1 to $n$. The task is to divide this sequence into two disjoint sets $A$ and $B$ so that the absolute difference between their sums, $ Since $n$ can be as large as $2 cdot 10^9$, explicitly constructing the sequence or trying all…"
date: "2026-06-12T05:35:13+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1102
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 531 (Div. 3)"
rating: 800
weight: 1102
solve_time_s: 72
verified: true
draft: false
---

[CF 1102A - Integer Sequence Dividing](https://codeforces.com/problemset/problem/1102/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the sequence of integers from 1 to $n$. The task is to divide this sequence into two disjoint sets $A$ and $B$ so that the absolute difference between their sums, $|sum(A) - sum(B)|$, is as small as possible. The input is a single integer $n$ and the output is a single integer representing this minimal difference.

Since $n$ can be as large as $2 \cdot 10^9$, explicitly constructing the sequence or trying all partitions is impossible. This constraint implies that any solution must run in constant time with respect to $n$. We cannot iterate through $n$ elements or subsets because even $O(n)$ time would be too slow, and any solution requiring $O(n^2)$ or more is entirely infeasible.

The non-obvious edge cases arise from the parity of the sum of numbers from 1 to $n$. The sum of the first $n$ natural numbers is $S = n(n+1)/2$. If $S$ is even, it is theoretically possible to split the sequence into two sets with equal sums, yielding a minimum difference of 0. If $S$ is odd, the minimum difference must be 1, since the sums of the two sets cannot both be integers that sum to an odd total. A naive solution that ignores parity might attempt to construct sets manually, which would be too slow for large $n$.

## Approaches

A brute-force approach would try to generate all subsets of the sequence and calculate the difference of sums for each pair of disjoint sets. This approach works in principle because checking all partitions guarantees finding the minimum difference. However, the number of subsets of a set of size $n$ is $2^n$. For even modest $n$, say $n = 30$, this is already over a billion possibilities. For $n$ up to $2 \cdot 10^9$, this is completely infeasible.

The key insight is that the sequence is consecutive integers starting at 1. The sum of the first $n$ numbers is a simple formula: $S = n(n+1)/2$. The absolute difference between two partitions can only be 0 if $S$ is even, or 1 if $S$ is odd. This observation eliminates the need for constructing sets or iterating: it reduces the problem to computing $S$ and checking its parity. The brute-force reasoning validates the correctness of this shortcut: the minimum difference is solely determined by whether the total sum is even or odd.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the sum of the sequence from 1 to $n$ using the formula $S = n(n+1)/2$. This formula is derived from the arithmetic series formula and does not require iteration, which makes it feasible even for large $n$.
2. Check the parity of $S$. If $S$ is divisible by 2, the sum is even. Otherwise, the sum is odd.
3. Return 0 if $S$ is even, or 1 if $S$ is odd. This is the minimal possible absolute difference. The reasoning is that an even total sum can be split exactly in half, whereas an odd sum will always leave a remainder of 1 when divided into integer sums.

Why it works: the formula for the sum guarantees that we capture the total sum exactly, and the parity check ensures that we choose the correct minimal difference. Since the sequence is strictly increasing consecutive integers, no other configuration of splits can produce a smaller difference than the one implied by the total sum’s parity.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
total_sum = n * (n + 1) // 2
if total_sum % 2 == 0:
    print(0)
else:
    print(1)
```

The code reads a single integer $n$, computes the total sum using integer division to avoid floating-point errors, and then checks parity using the modulo operator. The use of integer division ensures correctness for very large $n$ without risk of rounding errors. The conditional prints the minimum difference directly.

## Worked Examples

Sample Input 1: `3`

| Step | Calculation | total_sum | total_sum % 2 | Output |
| --- | --- | --- | --- | --- |
| 1 | n = 3 | 6 | 0 | 0 |

The sum $1 + 2 + 3 = 6$ is even, so we can split as $\{1,2\}$ and $\{3\}$ or other combinations to get a difference of 0.

Sample Input 2: `4`

| Step | Calculation | total_sum | total_sum % 2 | Output |
| --- | --- | --- | --- | --- |
| 1 | n = 4 | 10 | 0 | 0 |

The sum $1 + 2 + 3 + 4 = 10$ is even, so the difference is 0.

Sample Input 3: `5`

| Step | Calculation | total_sum | total_sum % 2 | Output |
| --- | --- | --- | --- | --- |
| 1 | n = 5 | 15 | 1 | 1 |

The sum $1 + 2 + 3 + 4 + 5 = 15$ is odd, so the difference must be 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic operations and a modulo check are performed. |
| Space | O(1) | No data structures grow with $n$. |

Given $n \le 2 \cdot 10^9$, these operations complete in microseconds. The solution is fully feasible under 1-second time and 256 MB memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    total_sum = n * (n + 1) // 2
    return str(0 if total_sum % 2 == 0 else 1)

# Provided samples
assert run("3\n") == "0", "sample 1"
assert run("4\n") == "0", "sample 2"
assert run("5\n") == "1", "sample 3"

# Custom cases
assert run("1\n") == "1", "minimum input"
assert run("2\n") == "1", "small even n"
assert run("1000000000\n") == "0", "large n, even total sum"
assert run("2000000001\n") == "1", "large n, odd total sum"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | minimum input, odd total sum |
| 2 | 1 | small n where split cannot be zero |
| 1000000000 | 0 | very large n, even total sum |
| 2000000001 | 1 | very large n, odd total sum |

## Edge Cases

For $n = 1$, the total sum is 1, which is odd. The algorithm correctly outputs 1. For $n = 2$, the sum is 3, also odd, so the algorithm returns 1. For very large $n$, the formula $n(n+1)/2$ handles integer overflow safely in Python, and the modulo check works identically. These cases confirm that the solution scales correctly and handles boundary conditions accurately.
