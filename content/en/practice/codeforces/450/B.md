---
title: "CF 450B - Jzzhu and Sequences"
description: "The problem defines a linear sequence $fn$ with two initial values $x = f1$ and $y = f2$, and a recurrence that repeats every six terms: $f{n} = f{n-1} - f{n-2}$."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 450
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 257 (Div. 2)"
rating: 1300
weight: 450
solve_time_s: 51
verified: true
draft: false
---

[CF 450B - Jzzhu and Sequences](https://codeforces.com/problemset/problem/450/B)

**Rating:** 1300  
**Tags:** implementation, math  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem defines a linear sequence $f_n$ with two initial values $x = f_1$ and $y = f_2$, and a recurrence that repeats every six terms: $f_{n} = f_{n-1} - f_{n-2}$. Effectively, this creates a sequence with the following cycle:

- $f_1 = x$
- $f_2 = y$
- $f_3 = y - x$
- $f_4 = -x$
- $f_5 = -y$
- $f_6 = x - y$
- $f_7 = f_1 = x$
- And so on, repeating every 6 terms.

The input provides integers $x$, $y$, and $n$, and we are asked to compute $f_n$ modulo $10^9 + 7$.

Constraints indicate that $x$ and $y$ can be very large (up to $\pm 10^9$), and $n$ can reach $2 \times 10^9$. This implies that computing the sequence iteratively from 1 to $n$ would be infeasible because it could require billions of operations. Therefore, a direct formula leveraging the 6-term repeating pattern is necessary.

A subtle edge case involves negative numbers. Since we must return the result modulo $10^9 + 7$, negative results must be properly converted to the corresponding positive modulus.

## Approaches

A brute-force approach would iterate from 1 to $n$ using the recurrence $f_n = f_{n-1} - f_{n-2}$ to compute each term. While this approach is logically correct, it is not practical for large $n$, because $n$ can be as large as 2 billion, resulting in billions of arithmetic operations.

The key insight is to recognize the sequence's 6-term cyclic behavior. Once the cycle is identified, any $f_n$ can be computed directly using the remainder $n \mod 6$. This reduces the problem from $O(n)$ operations to a constant $O(1)$ lookup and arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow for large n |
| Cycle-Based Formula | O(1) | O(1) | Accepted and efficient |

## Algorithm Walkthrough

1. First, compute the 6-term cycle based on the initial values $x$ and $y$. The sequence is $[x, y, y - x, -x, -y, x - y]$.
2. Compute $n \mod 6$ to determine the position within the cycle. Since the sequence is 1-indexed, adjust the index by subtracting 1: $index = (n-1) \mod 6$.
3. Retrieve the value from the cycle corresponding to this index.
4. Convert the result to the range $[0, 10^9 + 6]$ using modulo arithmetic. If the number is negative, add $10^9 + 7$ before taking the modulo.
5. Return the final value.

Why it works: The sequence's recurrence ensures that every 6 consecutive terms repeat exactly, so computing $n \mod 6$ provides the correct term regardless of how large $n$ is. Handling negative values with modulo guarantees the output meets the problem's constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

x, y = map(int, input().split())
n = int(input())

seq = [x, y, y - x, -x, -y, x - y]
result = seq[(n - 1) % 6] % MOD
print(result if result >= 0 else result + MOD)
```

This code first reads input values for $x$, $y$, and $n$. The 6-term cycle `seq` is constructed, and the appropriate term is accessed via `(n - 1) % 6` to account for 1-based indexing. The modulo operation ensures the result is in the correct range, handling any negative values.

## Worked Examples

For input:

```
2 3
3
```

Compute the sequence: `[2, 3, 1, -2, -3, -1]`. The 3rd term (0-indexed: 2) is `1`. Modulo operation is trivial here, so the output is `1`.

For input:

```
2 3
8
```

Index in the cycle: `(8 - 1) % 6 = 1`. The 2nd term in the sequence is `3`. Output modulo $10^9 + 7$ is `3`.

For input with negative result:

```
2 3
5
```

Index: `(5 - 1) % 6 = 4`. 5th term is `-3`. Modulo conversion: `-3 % (10^9 + 7) = 1000000004`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant-time arithmetic and indexing operations are performed |
| Space | O(1) | Stores only a fixed-length list of 6 elements and a few variables |

The algorithm is extremely efficient and works within the problem constraints even for the maximum $n$ of 2 billion.

## Test Cases

```
# sample inputs
assert run("2 3\n3\n") == "1", "sample 1"
assert run("2 3\n5\n") == "1000000004", "sample 2 negative mod"
# minimum n
assert run("1 1\n1\n") == "1", "minimum n"
# maximum n
assert run("1 2\n2000000000\n") == str((2-1) % (10**9+7)), "large n test"
# all negative inputs
assert run("-2 -3\n4\n") == str((-(-2)) % (10**9+7)), "negative x and y"
# cycle repeat
assert run("10 20\n7\n") == "10", "cycle repeat test"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "2 3\n3\n" | 1 | Sample input, normal positive sequence |
| "2 3\n5\n" | 1000000004 | Negative result modulo |
| "1 1\n1\n" | 1 | Minimum n boundary |
| "1 2\n2000000000\n" | 1 | Maximum n boundary |
| "-2 -3\n4\n" | 2 | Negative initial values |
| "10 20\n7\n" | 10 | Sequence repeats after 6 terms |

## Edge Cases

One edge case involves negative numbers. For example, $x = 2$, $y = 3$, $n = 5$. The 5th term is `-3`. Using naive modulo without adjustment might return `-3`, but the correct output is `1000000004`. Our implementation adds $MOD$ if the result is negative, handling this correctly.

Another edge case is when $n$ is very large, for example $n = 2 \times 10^9$. Computing iteratively would be infeasible. Using the cycle-based lookup with modulo reduces it to constant time.

A third edge case is when $n = 1$ or $n = 2$. These correspond directly to the initial values $x$ and $y$. Our modulo indexing `(n-1) % 6` correctly returns the first or second element without any off-by-one errors.
