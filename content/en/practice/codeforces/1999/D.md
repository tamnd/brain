---
title: "CF 1999D - Slavic's Exam"
description: "The task asks for the sum of the digits of a two-digit number for multiple test cases. Each input number $n$ is guaranteed to be between 10 and 99 inclusive, so the first digit is always nonzero."
date: "2026-06-08T14:22:08+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1999
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 964 (Div. 4)"
rating: 1100
weight: 1999
solve_time_s: 164
verified: false
draft: false
---

[CF 1999D - Slavic's Exam](https://codeforces.com/problemset/problem/1999/D)

**Rating:** 1100  
**Tags:** greedy, implementation, strings  
**Solve time:** 2m 44s  
**Verified:** no  

## Solution
## Problem Understanding

The task asks for the sum of the digits of a two-digit number for multiple test cases. Each input number $n$ is guaranteed to be between 10 and 99 inclusive, so the first digit is always nonzero. The input begins with $t$, the number of test cases, followed by $t$ lines each containing a single two-digit integer. The output for each test case is a single integer representing the sum of the tens and units digits.

Given the constraints, the number of test cases $t$ is small, up to 90, and each $n$ is fixed in size. There is no need for complex algorithms or data structures because even a straightforward approach that computes the sum for each number individually is sufficiently fast. Edge cases are straightforward: the smallest two-digit number is 10, which has a digit sum of 1, and the largest is 99, with a digit sum of 18. A careless approach might attempt to convert numbers to strings unnecessarily or mishandle 10, but a simple arithmetic approach using division and modulo avoids these pitfalls.

## Approaches

The brute-force approach is to convert each number to a string, split it into characters, convert those characters back to integers, and sum them. This works correctly because each number is guaranteed to have exactly two digits. The downside is that it involves string operations, which are unnecessary for numbers of this size.

The optimal approach is purely arithmetic. For a two-digit number $n$, the tens digit can be computed as $n // 10$ and the units digit as $n % 10$. Summing these two values gives the digit sum directly, avoiding any string manipulation and operating in constant time per test case. Given that $t$ is at most 90, this approach will complete in well under one second.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Convert to string and sum digits | O(t) | O(1) | Accepted |
| Arithmetic digit extraction | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer $t$ from input, which represents the number of test cases.
2. Loop over each test case from 1 to $t$.
3. For the current test case, read the integer $n$.
4. Compute the tens digit as $n // 10$.
5. Compute the units digit as $n % 10$.
6. Sum the tens and units digits to obtain the answer.
7. Print the sum.

This works because every number is guaranteed to be two digits, so integer division and modulo operations correctly isolate the tens and units. There are no cases where the number has fewer than two digits or more than two digits, so these operations are safe.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        print(n // 10 + n % 10)

if __name__ == "__main__":
    solve()
```

The solution reads the number of test cases, then loops through each number, computes the sum of digits using integer division and modulo, and prints the result. Using `sys.stdin.readline` ensures fast input handling even if the number of test cases is near the upper bound. There are no off-by-one errors because integer division and modulo for two-digit numbers are straightforward.

## Worked Examples

For the first sample input 77, the tens digit is 7 and the units digit is 7. Summing these gives 14. For the input 10, the tens digit is 1 and the units digit is 0, giving a sum of 1.

| n | tens (n // 10) | units (n % 10) | sum |
| --- | --- | --- | --- |
| 77 | 7 | 7 | 14 |
| 21 | 2 | 1 | 3 |
| 40 | 4 | 0 | 4 |
| 10 | 1 | 0 | 1 |
| 99 | 9 | 9 | 18 |

This trace confirms that the algorithm correctly computes the sum for both minimal and maximal two-digit inputs, and handles numbers where the units digit is zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case involves a constant number of arithmetic operations. |
| Space | O(1) | No additional data structures are needed beyond storing the input integer. |

With $t \le 90$, this solution runs in negligible time and uses minimal memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided sample
assert run("8\n77\n21\n40\n34\n19\n84\n10\n99\n") == "14\n3\n4\n7\n10\n12\n1\n18", "sample 1"

# Custom cases
assert run("3\n10\n99\n55\n") == "1\n18\n10", "edge digit sums"
assert run("2\n11\n20\n") == "2\n2", "leading or trailing zero"
assert run("1\n88\n") == "16", "equal digits"
assert run("1\n15\n") == "6", "arbitrary mid-range"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10, 99, 55 | 1, 18, 10 | Minimum and maximum digit sums, and equal tens and units digits |
| 11, 20 | 2, 2 | Correct handling when units digit is zero or both digits are small |
| 88 | 16 | Both digits equal and sum > 15 |
| 15 | 6 | General two-digit number sum |

## Edge Cases

The smallest two-digit number 10 produces a sum of 1. The largest 99 produces a sum of 18. Numbers like 20 or 30 test whether the algorithm handles zeros correctly; integer division and modulo correctly extract tens and units in these cases. Numbers with identical digits, such as 55 or 88, also work correctly because the sum is simply twice the repeated digit. This confirms the algorithm handles all two-digit numbers in the allowed range.
