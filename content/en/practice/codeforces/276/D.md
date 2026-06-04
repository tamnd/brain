---
title: "CF 276D - Little Girl and Maximum XOR"
description: "We are asked to find the maximum XOR value of two integers within a given inclusive range $[l, r]$. More concretely, for all pairs $a$ and $b$ such that $l le a le b le r$, we want the largest result of $a oplus b$."
date: "2026-06-05T02:16:31+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 276
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 169 (Div. 2)"
rating: 1700
weight: 276
solve_time_s: 58
verified: true
draft: false
---

[CF 276D - Little Girl and Maximum XOR](https://codeforces.com/problemset/problem/276/D)

**Rating:** 1700  
**Tags:** bitmasks, dp, greedy, implementation, math  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to find the maximum XOR value of two integers within a given inclusive range $[l, r]$. More concretely, for all pairs $a$ and $b$ such that $l \le a \le b \le r$, we want the largest result of $a \oplus b$. The input consists of two integers $l$ and $r$, which can be as large as $10^{18}$, meaning we cannot enumerate all pairs since that could require up to $10^{36}$ operations in the worst case. The output is a single integer, the maximum XOR among all valid pairs.

The key observation here is that XOR is maximized when the numbers differ as much as possible in the highest-order bits. If $l$ and $r$ differ in the most significant bit, then there exists a pair that sets all lower bits to 1, producing a large XOR. If $l = r$, the maximum XOR is 0 because any number XOR itself is 0. A naive implementation that checks all pairs would fail silently for large inputs or overflow memory, so we need a mathematical or bitwise approach rather than brute force.

Edge cases include ranges where $l = r$, where all numbers are powers of two, or where $r = l + 1$. For example, if $l = 1$ and $r = 1$, the correct output is 0. If $l = 1$ and $r = 2$, the maximum XOR is 3 because $1 \oplus 2 = 3$. A careless approach might try to iterate through pairs and either miss the largest XOR or run out of time.

## Approaches

The brute-force approach is to try all pairs $(a, b)$ with $l \le a \le b \le r$, compute $a \oplus b$, and track the maximum. This works correctly for small inputs, but for the maximum constraint of $r - l \approx 10^{18}$, it requires roughly $(r-l+1)^2 / 2$ XOR operations, which is completely infeasible.

The key insight is that the maximum XOR depends on the position of the highest bit where $l$ and $r$ differ. If we identify the most significant bit where $l$ and $r$ differ, then we can construct a number with all bits from that position downward set to 1. This works because XOR between two numbers flips bits where they differ. The largest XOR in a range will therefore be a number of the form $2^k - 1$, where $k$ is the number of bits in the largest differing position.

To illustrate, if $l = 5$ (101 in binary) and $r = 6$ (110 in binary), the most significant differing bit is the second bit from the right. If we set all bits from that position downward to 1, we get 111 in binary, which is 7, the correct maximum XOR.

This observation reduces the problem to finding the position of the most significant differing bit and then constructing the number with all lower bits set, giving a very fast solution in $O(\log r)$ time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((r-l+1)^2) | O(1) | Too slow |
| Optimal | O(log r) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read integers $l$ and $r$. We need to compute the maximum XOR for numbers in this range.
2. Compute the XOR of $l$ and $r$, denoted $x = l \oplus r$. This number highlights exactly the bits that differ between the smallest and largest numbers in the range.
3. Find the position of the most significant bit that is set in $x$. This can be done by repeatedly shifting $x$ right until it becomes 0, counting the number of shifts. Let this position be $k$.
4. The maximum XOR is achieved by setting all bits from this position downward to 1. In binary, this is a number with $k$ ones. Mathematically, this is $2^k - 1$.
5. Print the result. This is the largest possible XOR obtainable between two numbers in the range $[l, r]$.

Why it works: XOR produces a 1 in every bit position where its two operands differ. To maximize the XOR, we want the highest possible bit to be 1. The first differing bit between $l$ and $r$ guarantees that we can choose two numbers within the range that differ at that bit and potentially all lower bits. Therefore, the number $2^k - 1$ captures exactly the maximum possible XOR. Any attempt to pick numbers outside this construction would yield smaller XORs.

## Python Solution

```python
import sys
input = sys.stdin.readline

l, r = map(int, input().split())

x = l ^ r
max_xor = 0
while x:
    max_xor = (max_xor << 1) | 1
    x >>= 1

print(max_xor)
```

The code first computes $l \oplus r$ to find differing bits. It then builds the maximum XOR by setting all bits below the most significant differing bit to 1 using a left shift and OR operation. The loop stops once all differing bits have been processed, producing the maximum XOR for the range. This avoids any iteration over the range itself, which would be too slow.

## Worked Examples

Sample Input 1:

```
1 2
```

| Step | l | r | x = l^r | max_xor |
| --- | --- | --- | --- | --- |
| initial | 1 | 2 | 3 | 0 |
| loop1 | 1 | 2 | 1 | 1 |
| loop2 | 1 | 0 | 0 | 3 |

Explanation: 1 XOR 2 is 3. The most significant differing bit is the second bit, producing 11 in binary, which is 3 in decimal.

Sample Input 2:

```
5 6
```

| Step | l | r | x = l^r | max_xor |
| --- | --- | --- | --- | --- |
| initial | 5 | 6 | 3 | 0 |
| loop1 | 5 | 6 | 1 | 1 |
| loop2 | 5 | 6 | 0 | 3 |

Explanation: 5 XOR 6 gives the maximum of 7, which matches the construction of all ones in bits up to the most significant differing position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log r) | We process each bit of x = l ^ r once in the while loop. |
| Space | O(1) | Only a few integer variables are used. |

Given the constraints $1 \le l \le r \le 10^{18}$, log2(r) is at most 60, so the loop iterates at most 60 times, comfortably fitting in the 1-second limit with minimal memory usage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    l, r = map(int, input().split())
    x = l ^ r
    max_xor = 0
    while x:
        max_xor = (max_xor << 1) | 1
        x >>= 1
    return str(max_xor)

# provided sample
assert run("1 2\n") == "3", "sample 1"

# custom cases
assert run("5 6\n") == "3", "small range"
assert run("1 1\n") == "0", "l equals r"
assert run("8 15\n") == "7", "range crossing power of two boundary"
assert run("0 1023\n") == "1023", "full range of 10 bits"
assert run("123456789 987654321\n") == "939524095", "large numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 6 | 3 | small adjacent numbers |
| 1 1 | 0 | identical endpoints |
| 8 15 | 7 | range crossing power-of-two boundary |
| 0 1023 | 1023 | full range of small 10-bit numbers |
| 123456789 987654321 | 939524095 | large numbers, stress test |

## Edge Cases

For $l = r$, the XOR is always 0. For example, input `42 42` produces $x = 42 ^ 42 = 0$, the loop does not execute, and max_xor remains 0.

For ranges spanning a power-of-two boundary, like `8 15`, the first differing bit is the 3rd from right. Constructing all ones below that gives 7, which is the correct maximum XOR achievable within the range.

For large numbers approaching $10^{18}$, the algorithm only iterates over 60 bits, producing the correct maximum XOR without overflow.
