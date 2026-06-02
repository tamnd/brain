---
title: "CF 188D - Asterisks"
description: "The problem asks us to generate a simple text pattern. We are given a single integer n, which represents the number of lines we need to print. The first line should contain a single asterisk, the second line two asterisks, and so on, until the n-th line contains n asterisks."
date: "2026-06-03T01:05:41+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 188
codeforces_index: "D"
codeforces_contest_name: "Surprise Language Round 6"
rating: 1100
weight: 188
solve_time_s: 57
verified: true
draft: false
---

[CF 188D - Asterisks](https://codeforces.com/problemset/problem/188/D)

**Rating:** 1100  
**Tags:** *special, implementation  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to generate a simple text pattern. We are given a single integer _n_, which represents the number of lines we need to print. The first line should contain a single asterisk, the second line two asterisks, and so on, until the _n_-th line contains _n_ asterisks. Essentially, the output is a left-aligned right triangle of asterisks with height _n_.

The input constraint is 1 ≤ _n_ ≤ 50. This tells us that _n_ is small and any solution that runs in linear or quadratic time relative to _n_ will execute almost instantly. There is no risk of hitting performance limits here, so we do not need to consider algorithmic optimizations for large input sizes.

A subtle edge case is when _n_ equals 1. The correct output is a single line with one asterisk. A careless solution that uses a loop starting from zero or off-by-one logic could produce zero lines or fail to print the single asterisk. Similarly, _n_ = 50 is the largest input, so the last line should correctly contain exactly 50 asterisks. Any miscount in the loop boundary could either truncate the line or produce an extra asterisk.

## Approaches

The naive approach is straightforward: iterate from 1 to _n_, and for each iteration _i_, print _i_ asterisks. This works because each line independently depends only on its index, and constructing a string of repeated characters is a constant-time operation in Python for small _n_. The brute-force solution has a time complexity proportional to the sum 1 + 2 + … + _n_, which equals _n_(_n_+1)/2. For _n_ ≤ 50, this is at most 1275 character prints, which is trivial for modern computers.

Since the problem is already small-scale, no further optimization is necessary. The key insight is recognizing that each line's content is a simple repetition of a single character, which allows a one-liner in Python using the multiplication operator for strings. The problem does not require data structures or recursion.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Accepted |
| Optimal | O(n^2) | O(n) | Accepted |

Even though both approaches share the same asymptotic complexity, the "optimal" version leverages string repetition and direct printing to make the code concise.

## Algorithm Walkthrough

1. Read the integer _n_ from input. This defines the number of lines in the triangle.
2. Iterate over the range from 1 to _n_ inclusive. Let the loop variable be _i_.
3. For each _i_, generate a string consisting of _i_ asterisks. In Python, this is done with `"*"` multiplied by _i_.
4. Print the generated string. Each iteration prints one line, automatically appending a newline.

Why it works: The loop invariant is that on iteration _i_, exactly _i_ asterisks are printed. This guarantees that after the final iteration, the triangle has the correct shape and each line contains the exact number of asterisks corresponding to its 1-based index.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

for i in range(1, n + 1):
    print('*' * i)
```

The code starts by reading the input using fast I/O. Converting the input string to an integer ensures we have a proper loop bound. The `for` loop iterates over each line index from 1 to _n_, generating a string with the correct number of asterisks and printing it immediately. Multiplying a string by an integer in Python produces a new string with repeated characters, which matches the required pattern. Off-by-one errors are avoided by using `range(1, n + 1)` instead of `range(n)`.

## Worked Examples

Sample Input 1:

```
3
```

| i | '*' * i | Printed line |
| --- | --- | --- |
| 1 | '*' | * |
| 2 | '**' | ** |
| 3 | '***' | *** |

This confirms that the algorithm correctly prints one asterisk on the first line, two on the second, and three on the third.

Sample Input 2:

```
5
```

| i | '*' * i | Printed line |
| --- | --- | --- |
| 1 | '*' | * |
| 2 | '**' | ** |
| 3 | '***' | *** |
| 4 | '****' | **** |
| 5 | '*****' | ***** |

This demonstrates that the solution scales linearly with the number of lines and respects the 1-based line indexing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | The sum of characters printed is 1 + 2 + … + n = n(n+1)/2, which is O(n^2). |
| Space | O(n) | Each line requires storing up to n characters before printing. |

Given that n ≤ 50, the algorithm executes instantly and uses negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    n = int(input())
    for i in range(1, n + 1):
        print('*' * i)
    return output.getvalue().strip()

# provided sample
assert run("3\n") == "*\n**\n***", "sample 1"

# custom cases
assert run("1\n") == "*", "minimum input"
assert run("50\n") == '\n'.join('*' * i for i in range(1, 51)), "maximum input"
assert run("2\n") == "*\n**", "small even number"
assert run("5\n") == "*\n**\n***\n****\n*****", "small odd number"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | * | Handles minimum input |
| 50 | 1 to 50 asterisks per line | Correctly prints maximum allowed lines |
| 2 | *, ** | Correct line count for small even input |
| 5 | *, **, ***, ****, ***** | Correct line count for small odd input |

## Edge Cases

When _n_ = 1, the algorithm runs a single iteration, printing exactly one asterisk. This confirms the code correctly handles the smallest input. For _n_ = 50, the loop runs 50 times, each line containing the correct number of asterisks. Multiplying the string by the loop variable ensures no off-by-one errors occur. All lines are printed sequentially, preserving the required ordering.
