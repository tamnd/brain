---
title: "CF 188F - Binary Notation"
description: "The task is to take a single positive integer and express it in base 2, meaning we rewrite it using only powers of two with coefficients 0 or 1. Instead of the usual decimal representation, we want the binary string that tells us which powers of two sum up to the number."
date: "2026-06-03T01:07:40+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 188
codeforces_index: "F"
codeforces_contest_name: "Surprise Language Round 6"
rating: 1400
weight: 188
solve_time_s: 60
verified: true
draft: false
---

[CF 188F - Binary Notation](https://codeforces.com/problemset/problem/188/F)

**Rating:** 1400  
**Tags:** *special, implementation  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to take a single positive integer and express it in base 2, meaning we rewrite it using only powers of two with coefficients 0 or 1. Instead of the usual decimal representation, we want the binary string that tells us which powers of two sum up to the number.

For example, the number 5 corresponds to selecting 4 and 1, so its binary representation is `101`. Each position in the binary string represents whether a particular power of two is included in the sum.

The constraint is very small, with n up to 1,000,000. That immediately implies we are never in danger of performance issues even with straightforward bit manipulation or repeated division. Any solution that runs in logarithmic time or even linear in the number of bits is sufficient. Since the binary length of 1,000,000 is at most 20 bits, the output itself is tiny.

There are no hidden corner cases in terms of structure, but a few implementation pitfalls appear frequently. One is accidentally producing leading zeros, for example printing something like `000101` instead of `101`. Another is reversing the binary digits incorrectly if using division by 2 and appending bits in the wrong order. A third is mishandling the value 1, which should directly output `1` without any extra formatting.

## Approaches

The brute-force way to think about this problem is to simulate binary construction by repeatedly checking powers of two. One could start from 1, 2, 4, 8, and so on, testing whether each power fits into the remaining value, subtracting it if it does. This approach is correct because binary representation is fundamentally a greedy decomposition over powers of two. However, it is unnecessarily indirect and requires repeated exponentiation or iteration over all powers up to n, which is still small here but conceptually inefficient.

A more direct brute approach is repeated division by 2. We divide the number by 2, record the remainder each time, and collect bits. This works because division by 2 extracts the least significant bit at each step. The issue is not correctness but output order. The remainders come out from least significant bit to most significant bit, so they must be reversed at the end.

The key observation is that binary representation is exactly the sequence of remainders under repeated division by 2. This reduces the problem to a simple loop of logarithmic length, producing at most about 20 iterations for the maximum input. We do not need any extra data structures beyond a string builder or list of characters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (powers of two scanning) | O(log n) | O(1) | Accepted |
| Optimal (repeated division by 2) | O(log n) | O(log n) | Accepted |

## Algorithm Walkthrough

1. Take the input integer n as the number to convert.
2. Repeatedly divide n by 2 while storing the remainder each time, because the remainder tells us whether the current least significant bit is 0 or 1.
3. After each division, replace n with n // 2 so we move toward more significant bits.
4. Store each remainder in a list because the first remainder corresponds to the least significant bit.
5. Once n becomes 0, stop the loop since all bits have been processed.
6. Reverse the collected remainders because they were generated from least significant to most significant bit.
7. Join them into a single string and output it.

The reason this ordering step is necessary is that binary expansion is positional. Each division extracts information from the current least significant position, so the natural generation order is reversed relative to the final representation.

### Why it works

At every step, the algorithm decomposes n into n = 2q + r, where r is either 0 or 1. That remainder r is exactly the current lowest binary digit. Removing that digit by replacing n with q preserves the invariant that the remaining number still represents the higher-order bits of the original value. Repeating this until n becomes zero ensures that every power of two contribution is extracted exactly once, so the final reversed sequence is the unique binary representation.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())

bits = []

while n > 0:
    bits.append(str(n % 2))
    n //= 2

print(''.join(reversed(bits)))
```

The solution reads the integer, then repeatedly extracts the least significant bit using modulo 2. Each extracted bit is stored as a string. Because these bits are collected in reverse order, we reverse the list at the end before joining.

A subtle but important detail is that we stop when n becomes 0. If we continued further, we would append leading zeros, which are not part of the canonical binary representation. Another detail is converting bits to strings early, which simplifies the final join operation.

## Worked Examples

### Example 1: n = 5

| Step | n | n % 2 | bits |
| --- | --- | --- | --- |
| 1 | 5 | 1 | [1] |
| 2 | 2 | 0 | [1, 0] |
| 3 | 1 | 1 | [1, 0, 1] |
| 4 | 0 | stop | [1, 0, 1] |

After reversing, we get `101`. This confirms that the algorithm correctly reconstructs the binary representation from least significant bit upward.

### Example 2: n = 6

| Step | n | n % 2 | bits |
| --- | --- | --- | --- |
| 1 | 6 | 0 | [0] |
| 2 | 3 | 1 | [0, 1] |
| 3 | 1 | 1 | [0, 1, 1] |
| 4 | 0 | stop | [0, 1, 1] |

Reversing gives `110`, which matches 6 = 4 + 2.

This trace shows that even when the least significant bit is zero, it is still correctly captured and preserved.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | Each iteration halves n, so we process at most the number of bits in n |
| Space | O(log n) | We store one character per bit |

The maximum input size produces at most 20 bits, so both time and memory usage are effectively constant for this problem and well within limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input().strip())

    bits = []
    while n > 0:
        bits.append(str(n % 2))
        n //= 2

    return ''.join(reversed(bits))

# provided sample
assert run("5\n") == "101", "sample 1"

# minimum value
assert run("1\n") == "1", "minimum case"

# power of two
assert run("8\n") == "1000", "power of two"

# all bits set
assert run("7\n") == "111", "all ones case"

# random mid value
assert run("10\n") == "1010", "alternating pattern"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | smallest valid input |
| 8 | 1000 | single high bit |
| 7 | 111 | consecutive ones |
| 10 | 1010 | alternating binary pattern |

## Edge Cases

For input `1`, the algorithm starts with n = 1, appends `1 % 2 = 1`, then reduces n to 0 and stops. The bits list becomes `[1]`, and reversing it still yields `1`. This confirms that the single-bit case is handled without producing empty output or extra padding.

For input `8`, the loop produces remainders `[0, 0, 0, 1]`. Reversing gives `1000`. This demonstrates that trailing zeros in binary form are correctly preserved and not discarded prematurely.
