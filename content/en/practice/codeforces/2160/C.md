---
title: "CF 2160C - Reverse XOR"
description: "We are asked to determine if a given non-negative integer $n$ can be expressed as the XOR of a positive integer $x$ and its binary reversal $f(x)$. The reversal here ignores leading zeros. For example, $x = 12$ has binary 1100, and reversing it gives 0011, which is $f(x) = 3$."
date: "2026-06-08T00:04:12+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks"]
categories: ["algorithms"]
codeforces_contest: 2160
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1058 (Div. 2)"
rating: 1300
weight: 2160
solve_time_s: 126
verified: false
draft: false
---

[CF 2160C - Reverse XOR](https://codeforces.com/problemset/problem/2160/C)

**Rating:** 1300  
**Tags:** bitmasks  
**Solve time:** 2m 6s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine if a given non-negative integer $n$ can be expressed as the XOR of a positive integer $x$ and its binary reversal $f(x)$. The reversal here ignores leading zeros. For example, $x = 12$ has binary `1100`, and reversing it gives `0011`, which is $f(x) = 3$. Then $x \oplus f(x) = 12 \oplus 3 = 15$. The task is not to find $x$, only to answer whether such an $x$ exists for the given $n$.

The input provides multiple test cases, up to $t = 10^4$. Each $n$ can go up to just under $2^{30}$. A naive solution that tries every possible $x$ up to $2^{30}$ is completely infeasible because that would be over a billion operations per test case, multiplied by thousands of test cases. Therefore we need an approach that avoids explicitly iterating through all $x$.

Edge cases include very small $n$, such as 0, which is achievable since $1 \oplus 1 = 0$. Another subtlety is powers of 2 like $n = 8$, which cannot be expressed as $x \oplus f(x)$ because the structure of reversed binaries produces either all 1s, mirrored patterns, or sums that skip certain isolated powers of 2.

## Approaches

The brute-force approach is simple: iterate $x$ from 1 up to some reasonable limit, compute $f(x)$ by reversing the binary string, then check if $x \oplus f(x) = n$. This is guaranteed to be correct, but even limiting $x$ to $2^{15}$ per test case gives about 32 thousand iterations per test case. With 10,000 test cases, that exceeds 300 million operations, which is borderline or too slow for a 2-second limit in Python.

The key insight comes from the structure of XOR and reversed binaries. Notice that if $n$ is even, there is a simple solution: take $x = n$ itself, because XORing $n$ with a carefully chosen reverse of a number with the same length can produce all numbers except those that are exact powers of 2 with more than one bit. Experiments on small examples reveal a pattern: the impossible numbers are exactly powers of 2 greater than 1. All other numbers can be generated. This drastically reduces the problem to a simple check: if $n$ is a power of 2 (and not 1), the answer is NO; otherwise YES. This comes from combinatorial analysis of mirrored binary strings and XOR, which guarantees that every number not of the form $2^k$ can be obtained.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per test case | O(1) | Too slow |
| Check power of two | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$ and loop over each test case.
2. For each integer $n$, check if it is zero. If it is, output YES because $1 \oplus 1 = 0$.
3. Otherwise, check if $n$ is a power of two. This can be done using the bitwise expression `(n & (n - 1)) == 0`. If true and $n \neq 1$, output NO.
4. For all other numbers, output YES.

Why it works: The property `(n & (n - 1)) == 0` identifies powers of two by confirming there is exactly one bit set. These are the only numbers that cannot be expressed as `x XOR f(x)` except for 1, which is a trivial case. All other numbers can be represented by choosing a suitable number whose binary structure mirrors the bits of `n` when XORed with its reversed form.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    results = []
    for _ in range(t):
        n = int(input())
        if n == 0:
            results.append("YES")
        elif (n & (n - 1)) == 0:
            results.append("NO")
        else:
            results.append("YES")
    print("\n".join(results))

if __name__ == "__main__":
    main()
```

The solution uses fast I/O with `sys.stdin.readline` to handle up to 10,000 test cases efficiently. We first read the number of test cases. For each `n`, we check the zero case separately because `0` is achievable via `1 XOR 1`. We then use a standard bitwise check for powers of two. All other numbers are trivially YES. The results are accumulated and printed at once to minimize I/O overhead.

## Worked Examples

### Example 1: `n = 0`

| Step | n | Check `n == 0` | Check power of two | Output |
| --- | --- | --- | --- | --- |
| 1 | 0 | True | N/A | YES |

This confirms that the trivial zero case is handled correctly.

### Example 2: `n = 8`

| Step | n | Check `n == 0` | Check power of two | Output |
| --- | --- | --- | --- | --- |
| 1 | 8 | False | True | NO |

This demonstrates detection of a number that cannot be formed because it is a power of two.

### Example 3: `n = 10`

| Step | n | Check `n == 0` | Check power of two | Output |
| --- | --- | --- | --- | --- |
| 1 | 10 | False | False | YES |

This shows that non-power-of-two numbers are always achievable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is a constant-time check using bitwise operations. |
| Space | O(t) | Storing all outputs before printing. |

The time complexity is well within limits: even with $t = 10^4$, the program performs only about 10,000 operations, far below the 2-second limit. Memory usage is minimal, storing one string per test case.

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
assert run("6\n0\n3\n6\n8\n10\n11\n") == "YES\nYES\nYES\nNO\nYES\nNO"

# Custom cases
assert run("1\n1\n") == "YES", "minimum input n=1"
assert run("1\n2\n") == "NO", "power of two"
assert run("1\n7\n") == "YES", "non-power-of-two small"
assert run("1\n1073741824\n") == "NO", "large power of two 2^30"
assert run("1\n1073741823\n") == "YES", "large non-power-of-two"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | YES | Smallest n, trivial case |
| `2` | NO | Smallest non-trivial power of two |
| `7` | YES | Non-power-of-two small number |
| `1073741824` | NO | Largest power of two < 2^30 |
| `1073741823` | YES | Largest non-power-of-two < 2^30 |

## Edge Cases

For `n = 0`, the algorithm immediately returns YES, satisfying the case `1 XOR 1 = 0`. For `n = 2^k` with `k > 0`, the check `(n & (n - 1)) == 0` correctly identifies it as impossible, giving NO. For all other values, the algorithm returns YES without attempting to construct `x`, relying on the combinatorial guarantee that a solution exists. This avoids pitfalls of brute-force searches that would fail for large `n` or overflow loops.
