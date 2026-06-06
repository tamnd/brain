---
title: "CF 345A - Expecting Trouble"
description: "We are given a string representing Fridays the 13th across some period of time. Each character in the string can be \"0\" for a normal day, \"1\" for a particularly bad day, or \"?\" for a day the user cannot recall."
date: "2026-06-06T17:56:59+07:00"
tags: ["codeforces", "competitive-programming", "*special", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 345
codeforces_index: "A"
codeforces_contest_name: "Friday the 13th, Programmers Day"
rating: 1500
weight: 345
solve_time_s: 96
verified: true
draft: false
---

[CF 345A - Expecting Trouble](https://codeforces.com/problemset/problem/345/A)

**Rating:** 1500  
**Tags:** *special, probabilities  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string representing Fridays the 13th across some period of time. Each character in the string can be `"0"` for a normal day, `"1"` for a particularly bad day, or `"?"` for a day the user cannot recall. Alongside this, we are given a probability `p` which represents the likelihood that an unknown day `"?"` is actually a bad day `"1"`.

The task is to compute the expected value of the average badness over all Fridays. In other words, we want the mean of the random variable representing each day’s badness. Known days contribute their deterministic value (`0` or `1`), and unknown days contribute their expected value, which is just `p` because each `"?"` behaves like a Bernoulli random variable.

The string can be up to 50 characters long, which is very small, so we are not constrained by algorithmic complexity here. We only need a linear pass over the string to compute the expected sum, then divide by the string’s length to get the average.

A subtle edge case occurs when the string contains only `"?"` characters. For example, if the input is `"???"` and `p = 0.6`, a naive implementation might try to generate all possible combinations of `0` and `1` for the unknowns, but the expected value can be calculated directly as `3 * 0.6 / 3 = 0.6`. Another edge case is when `p` is exactly `0` or `1`. If `p = 1`, every `"?"` is treated as `1`; if `p = 0`, every `"?"` is treated as `0`. A careless rounding implementation could also produce `0.99999` instead of `1.00000` if not careful.

## Approaches

The brute-force approach is to enumerate all possible replacements for `"?"` and compute the average badness for each combination. For `n` unknowns, there are `2^n` combinations, each requiring an `O(n)` average computation. This gives `O(n * 2^n)` time complexity. Even for `n = 50`, this becomes astronomically large (`~10^15` operations), which is clearly infeasible.

The key insight is linearity of expectation. The expected value of a sum of independent random variables is the sum of their expected values, regardless of dependencies between the variables. Each known day contributes its deterministic `0` or `1`, and each unknown day `"?"` contributes `p`. This reduces the problem to a single linear pass through the string to sum these values and divide by the length. There is no need for combinatorial enumeration, and the solution is exact.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * 2^n) | O(n) | Too slow |
| Expected Value / Linear Scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the string `s` and the probability `p` from input. `s` contains the history of Fridays and `p` is the likelihood that an unknown day is bad.
2. Initialize a variable `total_badness` to `0`. This will accumulate the expected badness across all days.
3. Iterate over each character `c` in `s`. If `c` is `"1"`, add `1` to `total_badness` because it is deterministically a bad day. If `c` is `"0"`, add `0` since it is a good day. If `c` is `"?"`, add `p` because the expected value of a Bernoulli random variable with probability `p` is exactly `p`.
4. After the loop, compute the expected average by dividing `total_badness` by the length of `s`.
5. Print the result with exactly five decimal places. Use standard rounding rules to avoid off-by-one errors in the last digit.

Why it works: The linearity of expectation guarantees that summing the expected values of individual days gives the exact expected sum. Dividing by the number of days preserves the expectation in the average. There is no loss of precision in treating `"?"` as `p` because expectation does not require generating actual random outcomes.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
p = float(input().strip())

total_badness = 0.0

for c in s:
    if c == '1':
        total_badness += 1.0
    elif c == '?':
        total_badness += p
    # '0' adds 0, so we do nothing

expected_average = total_badness / len(s)
print(f"{expected_average:.5f}")
```

The solution reads input using `sys.stdin.readline` for fast I/O. The loop treats each character according to its meaning. We accumulate the expected badness in a floating-point variable and finally divide by the length. Formatting with `:.5f` ensures exactly five decimal places, rounding according to standard rules. The empty case `"0"` is handled implicitly because adding zero does not affect the sum.

## Worked Examples

**Sample Input 1**

```
?111?1??1
1.0
```

| Character | Contribution | Total Badness |
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

Average = 9.0 / 9 = 1.00000. The trace confirms that every `"?"` contributes `p=1.0` and every `1` contributes `1`, producing a total of 9.

**Sample Input 2**

```
0?0?
0.25
```

| Character | Contribution | Total Badness |
| --- | --- | --- |
| 0 | 0 | 0 |
| ? | 0.25 | 0.25 |
| 0 | 0 | 0.25 |
| ? | 0.25 | 0.50 |

Average = 0.50 / 4 = 0.12500. This trace demonstrates handling of mixed known and unknown days with non-trivial probability.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over the string to sum expected values; n ≤ 50 |
| Space | O(1) | Only one variable needed to store the sum; input size is negligible |

The algorithm is linear in the number of days, which is well within the constraints of n ≤ 50. Memory usage is trivial, fitting the 256 MB limit by several orders of magnitude.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().strip()
    p = float(input().strip())
    total_badness = 0.0
    for c in s:
        if c == '1':
            total_badness += 1.0
        elif c == '?':
            total_badness += p
    expected_average = total_badness / len(s)
    return f"{expected_average:.5f}"

# Provided samples
assert run("?111?1??1\n1.0\n") == "1.00000", "sample 1"
# Custom tests
assert run("0?0?\n0.25\n") == "0.12500", "mix of known and unknown"
assert run("?????\n0.5\n") == "0.50000", "all unknowns"
assert run("11111\n0.75\n") == "1.00000", "all bad days"
assert run("00000\n0.99\n") == "0.00000", "all good days"
assert run("1?0?1?0?1?\n0.5\n") == "0.50000", "alternating known and unknown"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0?0? / 0.25 | 0.12500 | Mixed known and unknown, small p |
| ????? / 0.5 | 0.50000 | All unknowns |
| 11111 / 0.75 | 1.00000 | All known bad |
| 00000 / 0.99 | 0.00000 | All known good |
| 1?0?1?0?1? / 0.5 | 0.50000 | Alternating known and unknown |

## Edge Cases

For a string with only unknowns, `"????"` and `p = 0.3`, each `"?"` contributes `0.3`. Total badness is `1.2`, average is `1.2 / 4 = 0.3`. The algorithm correctly accumulates these contributions without trying to enumerate all possibilities.

For
