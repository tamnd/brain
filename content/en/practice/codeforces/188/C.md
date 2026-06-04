---
title: "CF 188C - LCM"
description: "We are given two positive integers and need to compute their least common multiple. The least common multiple, usually abbreviated as LCM, is the smallest positive integer that is divisible by both numbers without leaving a remainder."
date: "2026-06-04T23:19:02+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 188
codeforces_index: "C"
codeforces_contest_name: "Surprise Language Round 6"
rating: 1400
weight: 188
solve_time_s: 182
verified: true
draft: false
---

[CF 188C - LCM](https://codeforces.com/problemset/problem/188/C)

**Rating:** 1400  
**Tags:** *special, implementation, math  
**Solve time:** 3m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two positive integers and need to compute their least common multiple. The least common multiple, usually abbreviated as LCM, is the smallest positive integer that is divisible by both numbers without leaving a remainder.

For example, if the numbers are 10 and 42, then 210 is divisible by both 10 and 42, and no smaller positive number has that property.

The constraints are very small. Both numbers are at most 1000, so even fairly inefficient methods would finish quickly. That said, the problem is fundamentally a math problem, and there is a standard formula that computes the answer immediately. Since the input contains only two numbers, the running time is effectively constant.

A common mistake is to multiply the numbers directly and assume that product is always the LCM.

Consider:

```
Input:
6 8
```

The correct answer is:

```
24
```

A careless implementation might output:

```
48
```

because 6 × 8 = 48. The product is divisible by both numbers, but it is not the smallest such value.

Another subtle case occurs when one number already divides the other.

```
Input:
5 10
```

The correct answer is:

```
10
```

The larger number is already a common multiple of both values. Returning the product 50 would be incorrect.

## Approaches

The most direct approach is brute force. Starting from the larger of the two numbers, repeatedly test successive integers until finding one divisible by both inputs. The first such number is the LCM.

This works because the definition of LCM is exactly "the smallest positive common multiple." Eventually a common multiple must appear, so the search terminates.

Even though the constraints are tiny, brute force does unnecessary work. In the worst case, we may test many candidate numbers before reaching the answer.

The key observation is the relationship between the greatest common divisor (GCD) and the least common multiple:

$$\text{LCM}(a,b)\times\text{GCD}(a,b)=a\times b$$

This formula works because the GCD represents the factor counted twice when multiplying the two numbers together. Dividing by the GCD removes that duplication.

Once we compute the GCD using Euclid's algorithm, the LCM follows immediately:

$$\text{LCM}(a,b)=\frac{a\times b}{\text{GCD}(a,b)}$$

Euclid's algorithm runs extremely quickly, making this approach both elegant and efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(LCM(a,b)) | O(1) | Accepted for these constraints, but inefficient |
| Optimal | O(log(min(a,b))) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read integers `a` and `b`.
2. Compute `g = gcd(a, b)` using Euclid's algorithm.

Euclid's algorithm repeatedly replaces `(a, b)` with `(b, a % b)` until the second value becomes zero. The remaining non-zero value is the GCD.
3. Compute the least common multiple using:

$$\text{lcm}=\frac{a\times b}{g}$$

The division must happen by the GCD because the common factors are counted twice in the product.
4. Output the resulting LCM.

### Why it works

The correctness follows from the identity

$$\text{LCM}(a,b)\times\text{GCD}(a,b)=a\times b.$$

The GCD contains exactly the factors shared by both numbers. When multiplying `a` and `b`, those shared factors appear twice. Dividing by the GCD removes one copy of every shared factor, leaving the smallest number that still contains all prime factors required by both inputs. That number is precisely the least common multiple.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

a, b = map(int, input().split())

print(a * b // gcd(a, b))
```

The solution reads the two integers and computes their greatest common divisor using Python's built-in `gcd` function.

The formula `a * b // gcd(a, b)` directly implements the mathematical relationship between GCD and LCM. Integer division is used because the result is guaranteed to be an integer.

One implementation detail worth remembering is the order of operations. The multiplication should happen before the division. In languages with fixed-width integer types this can cause overflow, but Python integers grow automatically, so there is no risk here.

## Worked Examples

### Example 1

Input:

```
10 42
```

| Step | a | b | gcd | lcm |
| --- | --- | --- | --- | --- |
| Read input | 10 | 42 | - | - |
| Compute GCD | 10 | 42 | 2 | - |
| Compute LCM | 10 | 42 | 2 | 210 |

Output:

```
210
```

This example shows the standard case where the numbers share a common factor. The GCD is 2, so dividing the product 420 by 2 gives the smallest common multiple, 210.

### Example 2

Input:

```
5 10
```

| Step | a | b | gcd | lcm |
| --- | --- | --- | --- | --- |
| Read input | 5 | 10 | - | - |
| Compute GCD | 5 | 10 | 5 | - |
| Compute LCM | 5 | 10 | 5 | 10 |

Output:

```
10
```

This trace demonstrates the case where one number divides the other. The LCM is simply the larger value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log(min(a, b))) | Euclid's algorithm computes the GCD in logarithmic time |
| Space | O(1) | Only a few variables are stored |

With inputs no larger than 1000, this solution runs essentially instantly and uses negligible memory. It easily fits within the given limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from math import gcd

def solve():
    a, b = map(int, input().split())
    print(a * b // gcd(a, b))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out

# provided sample
assert run("10 42\n") == "210\n", "sample 1"

# custom cases
assert run("1 1\n") == "1\n", "minimum values"
assert run("5 10\n") == "10\n", "one divides the other"
assert run("6 8\n") == "24\n", "shared factors"
assert run("1000 1000\n") == "1000\n", "maximum equal values"
assert run("999 1000\n") == "999000\n", "coprime near upper bound"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Minimum valid input |
| `5 10` | `10` | One number divides the other |
| `6 8` | `24` | Correct handling of shared factors |
| `1000 1000` | `1000` | Equal values at the upper limit |
| `999 1000` | `999000` | Coprime numbers near the maximum constraint |

## Edge Cases

Consider the input:

```
5 10
```

The algorithm computes:

```
gcd(5, 10) = 5
lcm = (5 × 10) / 5 = 10
```

The output is:

```
10
```

This correctly handles the situation where one number is already a multiple of the other.

Now consider:

```
6 8
```

The algorithm computes:

```
gcd(6, 8) = 2
lcm = (6 × 8) / 2 = 24
```

The output is:

```
24
```

This confirms that dividing by the GCD removes duplicated common factors from the product.

Finally, consider equal numbers:

```
1000 1000
```

The computation becomes:

```
gcd(1000, 1000) = 1000
lcm = (1000 × 1000) / 1000 = 1000
```

The result is exactly the original number, which is the correct least common multiple when both inputs are identical.
