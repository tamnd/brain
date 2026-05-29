---
title: "CF 345A - Expecting Trouble"
description: "We are given a sequence of recollections of Fridays the 13th. Each day is represented by a character: \"0\" for a normal day, \"1\" for a bad day, and \"?\" for an unknown day. Along with this sequence, we are provided a probability p that a \"?\" corresponds to a bad day."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 345
codeforces_index: "A"
codeforces_contest_name: "Friday the 13th, Programmers Day"
rating: 1500
weight: 345
solve_time_s: 91
verified: true
draft: false
---

[CF 345A - Expecting Trouble](https://codeforces.com/problemset/problem/345/A)

**Rating:** 1500  
**Tags:** *special, probabilities  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of recollections of Fridays the 13th. Each day is represented by a character: `"0"` for a normal day, `"1"` for a bad day, and `"?"` for an unknown day. Along with this sequence, we are provided a probability `p` that a `"?"` corresponds to a bad day. The task is to compute the expected average badness across all days in the sequence. Essentially, we want the mean of a sequence where `"0"` counts as 0, `"1"` counts as 1, and `"?"` counts as `p` in expectation.

The constraints are small: the string length is between 1 and 50, and `p` is a floating-point number with at most two decimal digits. With such a small string, we do not need complex optimizations, and even an O(n) solution is perfectly fast. The main consideration is handling floating-point arithmetic correctly and rounding the final result to five decimal places.

A non-obvious edge case occurs when all characters are `"?"`. For example, if the input is `"???"` and `p = 0.5`, the expected average badness is `0.5` because each day contributes `0.5` in expectation. A careless approach might try to simulate all combinations, which is unnecessary and could lead to floating-point inaccuracies.

## Approaches

The brute-force approach would be to enumerate all possible replacements for `"?"` with `0` or `1`, compute the average badness for each combination, and then compute the mean of these averages. For a string of length `n` with `k` question marks, this results in `2^k` combinations. While this is correct for very small inputs, the worst-case scenario with `n = 50` and all characters being `"?"` would require evaluating `2^50` combinations, which is infeasible.

The key observation is that the expected value of a sum of independent random variables is the sum of their expectations. Each `"0"` contributes `0`, each `"1"` contributes `1`, and each `"?"` contributes `p` to the sum in expectation. Dividing this sum by the total number of days gives the expected average badness directly. This reduces the problem to a simple linear scan of the string and is both conceptually and computationally straightforward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Linear Expectation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `expected_sum` to 0. This will hold the sum of expected badness across all days.
2. Iterate through each character `c` in the input string `s`.

- If `c` is `"1"`, add `1` to `expected_sum`.
- If `c` is `"0"`, add `0`.
- If `c` is `"?"`, add `p`. This handles the uncertainty in expectation without enumerating possibilities.
3. After processing all characters, divide `expected_sum` by the length of the string `n` to compute the expected average badness.
4. Print the result rounded to five decimal places using standard rounding.

Why it works: The linearity of expectation guarantees that summing the expected contributions of individual days gives the correct expected total, and dividing by the number of days correctly gives the expected average. No combination enumeration is needed, and this works regardless of the positions or number of `"?"` characters.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
p = float(input().strip())

expected_sum = 0.0
for c in s:
    if c == '1':
        expected_sum += 1
    elif c == '0':
        expected_sum += 0
    elif c == '?':
        expected_sum += p

expected_avg = expected_sum / len(s)
print(f"{expected_avg:.5f}")
```

The code reads the string and the probability. It initializes a floating-point accumulator `expected_sum`. The loop handles each character, adding `1`, `0`, or `p` as appropriate. Finally, the sum is normalized by dividing by the number of characters and printed with exactly five decimal places. Using Python's `float` is sufficient because `n` is small and `p` has at most two decimal digits, so precision errors are negligible.

## Worked Examples

**Example 1**

Input:

```
?111?1??1
1.0
```

| Character | Contribution | Cumulative Sum |
| --- | --- | --- |
| ? | 1.0 | 1.0 |
| 1 | 1 | 2.0 |
| 1 | 1 | 3.0 |
| 1 | 1 | 4.0 |
| ? | 1.0 | 5.0 |
| 1 | 1 | 6.0 |
| ? | 1.0 | 7.0 |
| ? | 1.0 | 8.0 |
| 1 | 1 | 9.0 |

Expected average = 9 / 9 = 1.00000

**Example 2**

Input:

```
?0?1
0.5
``
```
