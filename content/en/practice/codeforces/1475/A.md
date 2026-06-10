---
title: "CF 1475A - Odd Divisor"
description: "We are asked to determine if a given integer $n$ has an odd divisor greater than one. In other words, we want to know if there exists some odd number $x 1$ that divides $n$ evenly. If $n$ is divisible by such a number, the answer is \"YES\"; otherwise, it is \"NO\"."
date: "2026-06-11T00:06:48+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1475
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 697 (Div. 3)"
rating: 900
weight: 1475
solve_time_s: 113
verified: true
draft: false
---

[CF 1475A - Odd Divisor](https://codeforces.com/problemset/problem/1475/A)

**Rating:** 900  
**Tags:** math, number theory  
**Solve time:** 1m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine if a given integer $n$ has an odd divisor greater than one. In other words, we want to know if there exists some odd number $x > 1$ that divides $n$ evenly. If $n$ is divisible by such a number, the answer is "YES"; otherwise, it is "NO".

The input consists of multiple test cases, each with a single integer $n$. The largest possible $n$ can reach $10^{14}$, which is far beyond the limits of a naive approach that tries every number up to $n$ as a potential divisor. Given that there can be up to $10^4$ test cases, any approach that is linear in $n$ will be far too slow. We need something that works in logarithmic or constant time per query.

Edge cases include small numbers and powers of two. For example, if $n = 2$, there are no odd divisors greater than one, so the answer must be "NO". If $n = 3$, it is itself an odd number greater than one, so the answer is "YES". For powers of two, such as $n = 16$, all divisors are also powers of two and therefore even; these should return "NO". Misidentifying a power of two as having an odd divisor is a common mistake in a naive implementation.

## Approaches

The brute-force approach would be to check each integer from 3 to $n$ (skipping even numbers) to see if it divides $n$. This works because if any number divides $n$, it is an odd divisor. However, the worst case occurs for $n = 10^{14}$, requiring roughly $5 \cdot 10^{13}$ division checks, which is completely infeasible. This clearly fails the time limits.

The key observation is that an integer $n$ has no odd divisor greater than one if and only if it is a power of two. Powers of two are numbers of the form $2^k$, and all of their divisors are themselves powers of two, meaning they are all even except for 1. Any other number $n$ either has an odd factor itself or can be factored into an odd number multiplied by a power of two. This insight reduces the problem to checking whether $n$ is a power of two.

Checking if a number is a power of two can be done efficiently using a bitwise trick. For a positive integer $n$, if $n \& (n-1) == 0$, then $n$ is a power of two. This works because powers of two have exactly one bit set in binary. Otherwise, the number has an odd factor greater than one, and we return "YES".

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Bitwise Power-of-Two Check | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$. This defines how many numbers we need to process sequentially.
2. For each test case, read the integer $n$. We will examine whether $n$ has an odd divisor greater than one.
3. Apply the bitwise power-of-two test: compute $n \& (n-1)$. If this equals zero, $n$ is a power of two, and we output "NO" because it has no odd divisor greater than one.
4. If $n \& (n-1)$ is not zero, output "YES". This indicates that $n$ is not a pure power of two, meaning it has an odd divisor greater than one.

Why it works: powers of two are the only integers where all nontrivial divisors are even. By checking the binary representation, the bitwise trick directly identifies this property. Any number that fails the check must contain an odd factor, which guarantees an odd divisor greater than one.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        if n & (n - 1) == 0:
            print("NO")
        else:
            print("YES")

if __name__ == "__main__":
    main()
```

The code starts by reading all inputs efficiently using `sys.stdin.readline`. We loop through each test case and apply the bitwise check. Using `n & (n-1)` is critical; a naive modulo approach like `n % 2` or iterating divisors would fail the time constraints. The code handles very large numbers correctly because Python integers are arbitrary-precision.

## Worked Examples

**Example 1:** $n = 2$

| n | n & (n-1) | Output |
| --- | --- | --- |
| 2 | 2 & 1 = 0 | NO |

The number 2 is a power of two, so no odd divisor greater than one exists.

**Example 2:** $n = 3$

| n | n & (n-1) | Output |
| --- | --- | --- |
| 3 | 3 & 2 = 2 | YES |

The number 3 is not a power of two, so it has an odd divisor greater than one, which is 3 itself.

**Example 3:** $n = 16$

| n | n & (n-1) | Output |
| --- | --- | --- |
| 16 | 16 & 15 = 0 | NO |

16 is a power of two, all divisors are even except 1, so "NO" is correct.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is processed in constant time using a single bitwise operation. |
| Space | O(1) | No additional data structures are used beyond input storage. |

Given the constraints $t \le 10^4$ and $n \le 10^{14}$, the solution fits comfortably within the time and memory limits. Each operation is minimal, so even the largest inputs complete instantly.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# Provided samples
assert run("6\n2\n3\n4\n5\n998244353\n1099511627776\n") == "NO\nYES\nNO\nYES\nYES\nNO", "sample 1"

# Custom tests
assert run("2\n1\n8\n") == "NO\nNO", "minimum and power of two"
assert run("3\n9\n10\n15\n") == "YES\nYES\nYES", "odd numbers and non-powers-of-two"
assert run("2\n1024\n2048\n") == "NO\nNO", "large powers of two"
assert run("1\n99999999999999\n") == "YES", "large non-power-of-two"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 8 | NO, NO | smallest n and a small power of two |
| 9, 10, 15 | YES, YES, YES | non-powers-of-two numbers, some odd |
| 1024, 2048 | NO, NO | large powers of two |
| 99999999999999 | YES | very large number that is not a power of two |

## Edge Cases

The algorithm handles the smallest possible numbers correctly. For $n = 2$, the bitwise test returns zero, producing "NO". For odd numbers like $n = 3$ or $n = 9$, the test fails, correctly identifying that an odd divisor greater than one exists. For powers of two, even very large ones like $n = 2^{40}$, the check scales without looping or recursion, ensuring both speed and correctness. No off-by-one errors exist because the bitwise operation precisely detects the one-bit pattern of powers of two.
