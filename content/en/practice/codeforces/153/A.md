---
title: "CF 153A - A + B"
description: "We are asked to compute the sum of two integers, but the emphasis is on careful output formatting. Specifically, the input consists of two numbers, each on its own line, and we need to print their sum without any leading zeros."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 153
codeforces_index: "A"
codeforces_contest_name: "Surprise Language Round 5"
rating: 1600
weight: 153
solve_time_s: 59
verified: true
draft: false
---

[CF 153A - A + B](https://codeforces.com/problemset/problem/153/A)

**Rating:** 1600  
**Tags:** *special  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to compute the sum of two integers, but the emphasis is on careful output formatting. Specifically, the input consists of two numbers, each on its own line, and we need to print their sum without any leading zeros. This means that even if the sum is, for example, `00015`, we should output `15`.

The constraints are straightforward: both integers are between 1 and 100,000. These bounds are small enough that we do not need to worry about integer overflow in Python, and the sum will always be less than or equal to 200,000. The input size is tiny, so any reasonable algorithm will run in microseconds; the challenge is correctness, not efficiency.

Non-obvious edge cases arise from potential misinterpretation of input as strings. For instance, if one number were `"00012"` (which is technically outside the input constraint since A and B are positive integers, but could appear in variations of the problem), careless string concatenation or output could produce `"00015"` instead of `"15"`. Another scenario is when the sum itself is exactly `100000` or some boundary value, which again tests that the output is numeric and stripped of leading zeros.

## Approaches

The naive approach treats the numbers as strings, converts them to integers, adds them, and prints the result. This works because Python handles integer arithmetic correctly up to arbitrarily large values. There is no need to manually implement addition digit by digit because the input range is small and Python integers automatically manage carry-over. In a brute-force scenario, one could attempt to iterate through each digit from least significant to most significant and sum manually, but this would be unnecessarily verbose and error-prone.

The key observation is that Python’s built-in `int` type already handles both parsing numbers from strings and removing leading zeros when converting back to string via `print`. Therefore, the optimal approach is simply reading each number, converting it to an integer, summing, and printing the result. There is no need for arrays, loops, or extra checks. The brute-force approach would only be "too slow" in a hypothetical language without big integer support, but here it is effectively optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Manual digit-by-digit addition | O(log(max(A,B))) | O(log(max(A,B))) | Unnecessary, verbose |
| Python built-in arithmetic | O(1) | O(1) | Accepted, simple and correct |

## Algorithm Walkthrough

1. Read the first line of input and convert it to an integer. This ensures that any leading zeros in the input, if present, are ignored automatically.
2. Read the second line of input and convert it to an integer for the same reason.
3. Compute the sum of the two integers.
4. Print the sum directly. The `print` function converts the integer to a string, which by default does not include leading zeros.

Why it works: the invariant here is that at every step we operate on true integer values. By converting from string to integer immediately, we remove any ambiguity from leading zeros. The sum of two positive integers always produces a positive integer, and printing an integer in Python guarantees no leading zeros, which exactly matches the problem requirement.

## Python Solution

```python
import sys
input = sys.stdin.readline

A = int(input())
B = int(input())
print(A + B)
```

The first two lines read the input and convert it to integers. This conversion automatically handles stripping any accidental leading zeros. The last line computes the sum and prints it. There are no loops or conditionals because the problem does not require them. Since the input size is very small, this code runs well within time and memory limits.

## Worked Examples

### Sample 1

Input:

```
12
3
```

| Step | A | B | Sum |
| --- | --- | --- | --- |
| Read A | 12 | - | - |
| Read B | 12 | 3 | - |
| Compute A + B | 12 | 3 | 15 |
| Output | 15 |  |  |

This trace confirms that the conversion from string to integer correctly handles normal numbers and that the sum is computed correctly.

### Sample 2 (constructed)

Input:

```
100000
5
```

| Step | A | B | Sum |
| --- | --- | --- | --- |
| Read A | 100000 | - | - |
| Read B | 100000 | 5 | - |
| Compute A + B | 100000 | 5 | 100005 |
| Output | 100005 |  |  |

This demonstrates that the algorithm handles boundary values without issue.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Reading and converting two integers and summing them is constant time given the small input size. |
| Space | O(1) | Only two integer variables are stored; no arrays or auxiliary structures are required. |

Given the constraints, this solution runs in negligible time and uses minimal memory, fully satisfying the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    A = int(input())
    B = int(input())
    return str(A + B)

# provided sample
assert run("12\n3\n") == "15", "sample 1"

# minimum input
assert run("1\n1\n") == "2", "minimum input"

# maximum input
assert run("100000\n100000\n") == "200000", "maximum input"

# mixed size inputs
assert run("100\n5\n") == "105", "small and small input"

# edge case for output without leading zeros
assert run("00012\n00003\n") == "15", "leading zeros input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 12\n3 | 15 | Normal sum |
| 1\n1 | 2 | Minimum input values |
| 100000\n100000 | 200000 | Maximum input values |
| 100\n5 | 105 | Mixed small values |
| 00012\n00003 | 15 | Input with leading zeros |

## Edge Cases

For input with accidental leading zeros, such as `"00012"` and `"00003"`, the algorithm converts both to integers immediately. Python interprets `"00012"` as 12 and `"00003"` as 3. The sum is computed as 15 and printed without any leading zeros. The internal conversion guarantees correctness even if the input format is unconventional. The boundary values of 1 and 100,000 confirm that neither integer overflow nor misformatting occurs.
