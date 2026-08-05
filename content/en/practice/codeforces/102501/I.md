---
title: "CF 102501I - Rats"
description: "Douglas performs a classic capture and recapture experiment to estimate the size of a rat population. On the first day, he catches n1 rats, marks all of them, and releases them. On the second day, he catches n2 rats, among which n12 are already marked."
date: "2026-08-05T17:46:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102501
codeforces_index: "I"
codeforces_contest_name: "2019-2020 ICPC Southwestern European Regional Programming Contest (SWERC 2019-20)"
rating: 0
weight: 102501
solve_time_s: 189
verified: true
draft: false
---

[CF 102501I - Rats](https://codeforces.com/problemset/problem/102501/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

Douglas performs a classic capture and recapture experiment to estimate the size of a rat population.

On the first day, he catches `n1` rats, marks all of them, and releases them. On the second day, he catches `n2` rats, among which `n12` are already marked. Instead of computing the estimate manually, our task is simply to evaluate the Chapman estimator

$$\left\lfloor \frac{(n_1+1)(n_2+1)}{n_{12}+1}\right\rfloor-1$$

and print the resulting integer.

The input consists of exactly three integers, so there is no searching, simulation, or optimization involved. Every value is at most 10000, making the largest product

$$(10000+1)^2 = 100020001,$$

which easily fits inside a 32 bit signed integer. Python integers have arbitrary precision anyway, so overflow is never a concern.

The only work required is evaluating one multiplication, one integer division, and one subtraction. Any algorithm beyond constant time would be unnecessary.

A subtle implementation mistake is using floating point arithmetic instead of integer arithmetic. For example, with input

```
10000 10000 3
```

the correct result is

```
25004999
```

Using floating point division followed by conversion to an integer may still work for these limits, but relying on floating point is unnecessary and can introduce rounding errors in similar problems. Integer floor division directly matches the mathematical definition.

Another easy mistake is forgetting the final subtraction by one. For input

```
1 1 1
```

the formula becomes

$$\left\lfloor\frac{2\cdot2}{2}\right\rfloor-1
=2-1
=1,$$

so the correct output is

```
1
```

Printing only the quotient would incorrectly produce `2`.

A third common error is omitting the added ones inside the formula. For input

```
0 0 0
```

the correct computation is

$$\left\lfloor\frac{1\cdot1}{1}\right\rfloor-1=0,$$

so the answer is

```
0
```

Using `n1 * n2 / n12` would even divide by zero.

## Approaches

A brute force interpretation would attempt to estimate the population by considering every possible population size, checking which values are compatible with the observed captures, or even simulating repeated experiments. Such an approach is mathematically unnecessary and could require examining millions of candidate values if the search range were chosen generously.

The problem statement already provides the Chapman estimator as the desired estimate. The population size is not something we must infer algorithmically. We only need to substitute the three input values into the given expression and compute the result.

The key observation is that the estimator already includes the required floor operation. Integer floor division computes exactly the same value without using floating point arithmetic. After that, subtract one and print the result.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(M), where M is the searched population range | O(1) | Too slow and unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three integers `n1`, `n2`, and `n12`.
2. Compute the numerator `(n1 + 1) * (n2 + 1)`. The formula explicitly adds one to both capture counts before multiplying.
3. Divide the numerator by `n12 + 1` using integer floor division. This matches the floor operation in the estimator exactly.
4. Subtract one from the quotient to obtain the Chapman estimate.
5. Print the resulting integer.

### Why it works

The algorithm is a direct implementation of the mathematical definition given in the problem. Integer floor division computes

$$\left\lfloor\frac{(n_1+1)(n_2+1)}{n_{12}+1}\right\rfloor,$$

which is precisely the first part of the estimator. Subtracting one afterward completes the formula exactly, so the computed value is identical to the required estimate.

## Python Solution

```python
import sys
input = sys.stdin.readline

n1, n2, n12 = map(int, input().split())

answer = ((n1 + 1) * (n2 + 1)) // (n12 + 1) - 1
print(answer)
```

The program begins by reading the three integers from standard input.

The next line evaluates the formula directly. The multiplication is performed before the division, preserving exact integer arithmetic. Using `//` is essential because the mathematical expression requires the floor of the quotient.

Finally, the program subtracts one and prints the result. No special cases are needed because `n12 + 1` is always at least one, so division by zero cannot occur.

## Worked Examples

### Example 1

Input:

```
15 18 11
```

| Step | n1 | n2 | n12 | Numerator | Quotient | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| Read input | 15 | 18 | 11 | - | - | - |
| Compute numerator | 15 | 18 | 11 | 304 | - | - |
| Floor division | 15 | 18 | 11 | 304 | 25 | - |
| Subtract one | 15 | 18 | 11 | 304 | 25 | 24 |

The estimate produced by the Chapman formula is `24`.

### Example 2

Input:

```
0 0 0
```

| Step | n1 | n2 | n12 | Numerator | Quotient | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| Read input | 0 | 0 | 0 | - | - | - |
| Compute numerator | 0 | 0 | 0 | 1 | - | - |
| Floor division | 0 | 0 | 0 | 1 | 1 | - |
| Subtract one | 0 | 0 | 0 | 1 | 1 | 0 |

This example shows why the added ones inside the formula matter. Even when every input is zero, the computation remains valid and produces `0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations are performed. |
| Space | O(1) | Only a few integer variables are stored. |

The running time and memory usage are independent of the input values. The solution comfortably satisfies the limits.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    n1, n2, n12 = map(int, input().split())
    print(((n1 + 1) * (n2 + 1)) // (n12 + 1) - 1)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out.getvalue()

# provided sample
assert run("15 18 11\n") == "24\n", "sample 1"

# minimum values
assert run("0 0 0\n") == "0\n", "minimum input"

# all values equal
assert run("5 5 5\n") == "5\n", "all equal"

# no recaptured rats
assert run("10 20 0\n") == "230\n", "zero recaptures"

# maximum values
assert run("10000 10000 10000\n") == "10000\n", "maximum values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 0` | `0` | Smallest legal input and correct handling of the added ones |
| `5 5 5` | `5` | Correct subtraction after division |
| `10 20 0` | `230` | Denominator becomes one when no marked rats are recaptured |
| `10000 10000 10000` | `10000` | Largest input values and arithmetic near the upper bounds |

## Edge Cases

Consider the input

```
0 0 0
```

The algorithm computes `(0 + 1) * (0 + 1) = 1`, divides by `0 + 1 = 1`, obtaining `1`, and subtracts one to produce `0`. Every operation is well defined because the denominator is never zero.

Consider the input

```
1 1 1
```

The numerator is `(1 + 1) * (1 + 1) = 4`. Dividing by `1 + 1 = 2` gives `2`, and subtracting one produces `1`. This confirms that the final subtraction is part of the estimator and cannot be omitted.

Consider the input

```
10000 10000 3
```

The numerator is `10001 × 10001 = 100020001`. Integer floor division by `4` yields `25005000`, and subtracting one gives `25004999`. The calculation stays entirely within integer arithmetic, avoiding any rounding issues while handling the largest permitted multiplication.
