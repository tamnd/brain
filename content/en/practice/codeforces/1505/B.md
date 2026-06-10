---
title: "CF 1505B - DMCA"
description: "The task hides the familiar notion of a digital root behind unusual terminology. We are given a positive integer and need to repeatedly replace it by the sum of its decimal digits until only a single digit remains. That final digit is the answer."
date: "2026-06-10T20:28:50+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1505
codeforces_index: "B"
codeforces_contest_name: "April Fools Day Contest 2021"
rating: 1600
weight: 1505
solve_time_s: 340
verified: false
draft: false
---

[CF 1505B - DMCA](https://codeforces.com/problemset/problem/1505/B)

**Rating:** 1600  
**Tags:** *special, implementation, number theory  
**Solve time:** 5m 40s  
**Verified:** no  

## Solution
## Problem Understanding

The task hides the familiar notion of a digital root behind unusual terminology. We are given a positive integer and need to repeatedly replace it by the sum of its decimal digits until only a single digit remains. That final digit is the answer. For example, starting from 81 we get 8 + 1 = 9, so the result is 9. Starting from 999 we get 27, then 2 + 7 = 9.

The input value is at most one million. Even a straightforward simulation performs only a few iterations because each digit sum drastically reduces the number. With such small limits, any reasonable approach runs comfortably within one second.

The main source of mistakes is misunderstanding what kind of "root" is required. A careless solution might compute the square root instead.

Consider the input

```
81
```

The correct output is

```
9
```

because the required operation is digit summation, not √81.

Another subtle case is a number that already consists of a single digit.

For the input

```
1
```

the answer is

```
1
```

A formula based on modulo 9 must treat this case carefully, otherwise it may incorrectly return 0.

A multiple of 9 is another common trap.

For the input

```
18
```

the answer is

```
9
```

Using `a % 9` directly gives 0, which is wrong because the digital root of every positive multiple of 9 equals 9.

## Approaches

The most direct method repeatedly computes the sum of decimal digits until the current value becomes a single digit. This process is correct because it follows the definition exactly. Since the input never exceeds one million, the number has at most seven digits and only a few rounds are needed. Even though the running time is already tiny, there is an even shorter way.

The key observation comes from the well known property of digital roots. Replacing a number by the sum of its digits preserves its remainder modulo 9. Repeating the operation until one digit remains means that the final answer is determined entirely by the remainder modulo 9.

There is one exception. Positive multiples of 9 have remainder 0, but their digital root is 9 rather than 0. Combining these facts gives a constant time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of digits × iterations) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `a`.
2. If `a % 9 != 0`, output `a % 9`. Numbers with the same remainder modulo 9 share the same digital root.
3. Otherwise, distinguish between the value 0 and positive multiples of 9. Since the input is always positive, output 9.

### Why it works

Taking the sum of decimal digits changes a number by a multiple of 9, so the remainder modulo 9 never changes. Repeating the operation eventually produces a single digit between 1 and 9. Among those digits, the only one congruent to 0 modulo 9 is 9 itself. Hence every positive multiple of 9 has digital root 9, and every other number has digital root equal to its remainder modulo 9. The algorithm directly computes that value, so it cannot produce an incorrect answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

a = int(input())

ans = a % 9
if ans == 0:
    ans = 9

print(ans)
```

The program starts by reading the single input number.

The variable `ans` stores the remainder modulo 9. For numbers that are not divisible by 9, this remainder already equals the digital root.

The only special case occurs when the remainder is zero. Since the input is guaranteed to be positive, that means the number is a positive multiple of 9, whose digital root is 9. Replacing 0 by 9 handles this boundary correctly.

No loops or recursion are required.

## Worked Examples

### Example 1

Input:

```
1
```

| a | a % 9 | Final answer |
| --- | --- | --- |
| 1 | 1 | 1 |

The remainder is already nonzero, so it becomes the answer directly. This confirms that single digit numbers remain unchanged.

### Example 2

Input:

```
81
```

| a | a % 9 | Final answer |
| --- | --- | --- |
| 81 | 0 | 9 |

Since 81 is divisible by 9, the remainder is zero. The special rule converts that value to 9. This example demonstrates the only nontrivial boundary case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed |
| Space | O(1) | No extra storage depending on the input size is used |

The solution easily satisfies the limits. Constant time and constant memory are much smaller than what the constraints allow.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    a = int(input())
    ans = a % 9
    if ans == 0:
        ans = 9

    return str(ans) + "\n"

# provided samples
assert run("1\n") == "1\n", "sample 1"

# custom cases
assert run("81\n") == "9\n", "multiple of 9"
assert run("18\n") == "9\n", "boundary remainder 0"
assert run("10\n") == "1\n", "digit sum 1+0"
assert run("1000000\n") == "1\n", "maximum input"
assert run("999999\n") == "9\n", "large multiple of 9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 81 | 9 | Multiple of 9 handling |
| 18 | 9 | Remainder zero special case |
| 10 | 1 | Ordinary nonzero remainder |
| 1000000 | 1 | Maximum input value |
| 999999 | 9 | Large multiple of 9 |

## Edge Cases

A number that already has one digit should remain unchanged.

For the input

```
1
```

the algorithm computes `1 % 9 = 1`, so it prints 1. No special handling is needed.

Positive multiples of 9 require care.

For the input

```
18
```

the execution is:

| a | a % 9 | Output |
| --- | --- | --- |
| 18 | 0 | 9 |

The remainder is zero, so the algorithm replaces it with 9. This matches the sequence 18 → 9 obtained by repeated digit sums.

Large values behave the same way.

For the input

```
1000000
```

the execution is:

| a | a % 9 | Output |
| --- | --- | --- |
| 1000000 | 1 | 1 |

Repeated digit summation gives 1 + 0 + 0 + 0 + 0 + 0 + 0 = 1, which agrees with the modulo computation.
