---
title: "CF 188C - LCM"
description: "We are given two positive integers and need to compute their least common multiple. The least common multiple, usually abbreviated as LCM, is the smallest positive integer that both numbers divide evenly."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 188
codeforces_index: "C"
codeforces_contest_name: "Surprise Language Round 6"
rating: 1400
weight: 188
solve_time_s: 119
verified: true
draft: false
---

[CF 188C - LCM](https://codeforces.com/problemset/problem/188/C)

**Rating:** 1400  
**Tags:** *special, implementation, math  
**Solve time:** 1m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two positive integers and need to compute their least common multiple. The least common multiple, usually abbreviated as LCM, is the smallest positive integer that both numbers divide evenly.

For example, if the numbers are 10 and 42, the answer is 210 because 210 is divisible by both 10 and 42, and no smaller positive number has that property.

The constraints are very small, both numbers are at most 1000. Even inefficient solutions would pass comfortably within the time limit. Still, this problem is mainly about recognizing the mathematical relationship between the greatest common divisor and the least common multiple.

A common mistake is computing the product directly and forgetting the overlap between common factors. Consider:

```
6 8
```

A careless implementation might think the answer is `6 * 8 = 48`, but the correct LCM is 24. The numbers share a factor of 2, so multiplying them counts that factor twice.

Another edge case appears when both numbers are equal:

```
7 7
```

The correct answer is 7, not 49. Equal numbers already divide each other, so their least common multiple is the number itself.

One more subtle issue is the order of operations in the formula. The standard formula is:

```
LCM(a, b) = a * b / GCD(a, b)
```

If the language uses fixed-size integers, multiplying first can overflow. Python integers grow automatically, so this problem is harmless here, but in languages like C++ it is safer to divide first:

```
a / gcd(a, b) * b
```

## Approaches

The most direct brute-force solution is to start from `max(a, b)` and repeatedly check each integer until finding one divisible by both numbers.

For example, with `a = 6` and `b = 8`, we would test:

```
8, 9, 10, 11, 12, 13, ..., 24
```

The first number divisible by both is 24.

This approach is correct because the least common multiple is exactly the first shared multiple encountered while scanning upward. The problem is efficiency. In the worst case, the search could take many iterations before reaching the answer. With larger constraints this becomes impractical.

The key observation is that the greatest common divisor already tells us how much overlap exists between the two numbers' prime factorizations.

Suppose:

```
a = gcd(a, b) * x
b = gcd(a, b) * y
```

The shared factors appear inside the gcd. If we simply multiply `a * b`, those shared factors are counted twice. Dividing by the gcd removes one copy of the overlap.

That gives the standard identity:

```
LCM(a, b) = (a * b) / GCD(a, b)
```

The Euclidean algorithm computes the gcd extremely quickly, even for very large integers. After obtaining the gcd, computing the lcm becomes immediate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(LCM(a, b)) | O(1) | Accepted for these limits, inefficient in general |
| Optimal | O(log(min(a, b))) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two integers `a` and `b`.
2. Compute `gcd(a, b)` using the Euclidean algorithm.

The Euclidean algorithm repeatedly replaces the larger number with the remainder until one number becomes zero. The remaining non-zero number is the gcd.
3. Divide one of the numbers by the gcd.

This removes the duplicated common factors before multiplication.
4. Multiply the result by the other number.

The expression becomes:

```
(a // gcd) * b
```
5. Print the final value.

### Why it works

The gcd contains exactly the factors shared by both numbers. Multiplying `a * b` includes those shared factors twice. Dividing by the gcd removes one duplicate copy, leaving each prime factor with exactly the highest exponent required for divisibility by both numbers. That is precisely the definition of the least common multiple.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

a, b = map(int, input().split())

g = gcd(a, b)

lcm = (a // g) * b

print(lcm)
```

The solution starts by reading the two integers from standard input. Python's built-in `math.gcd` function already implements the Euclidean algorithm efficiently.

After computing the gcd, the code divides `a` by the gcd before multiplying by `b`. Mathematically, this is equivalent to `(a * b) // gcd`, but the chosen order is safer in languages with fixed-size integers because it avoids unnecessarily large intermediate values.

The problem contains only one test case, so no loop is needed.

## Worked Examples

### Example 1

Input:

```
10 42
```

| Step | a | b | gcd | Computation | Result |
| --- | --- | --- | --- | --- | --- |
| Initial | 10 | 42 | - | - | - |
| Compute gcd | 10 | 42 | 2 | - | - |
| Divide first | 10 | 42 | 2 | 10 // 2 | 5 |
| Multiply | 5 | 42 | 2 | 5 * 42 | 210 |

Output:

```
210
```

This trace shows how dividing by the gcd removes duplicated factors. Both numbers contain a factor of 2, so multiplying directly would count it twice.

### Example 2

Input:

```
7 7
```

| Step | a | b | gcd | Computation | Result |
| --- | --- | --- | --- | --- | --- |
| Initial | 7 | 7 | - | - | - |
| Compute gcd | 7 | 7 | 7 | - | - |
| Divide first | 7 | 7 | 7 | 7 // 7 | 1 |
| Multiply | 1 | 7 | 7 | 1 * 7 | 7 |

Output:

```
7
```

This example demonstrates the equal-values edge case. Since both numbers are identical, the least common multiple is the number itself.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log(min(a, b))) | Euclidean algorithm reduces the numbers rapidly |
| Space | O(1) | Only a few integer variables are stored |

The constraints are tiny, so this solution easily fits within the time and memory limits. Even for much larger integers, the Euclidean algorithm remains extremely fast.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import gcd

def solve():
    a, b = map(int, input().split())
    g = gcd(a, b)
    print((a // g) * b)

def run(inp: str) -> str:
    global input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__

    return out.getvalue()

# provided sample
assert run("10 42\n") == "210\n", "sample 1"

# minimum values
assert run("1 1\n") == "1\n", "minimum case"

# equal numbers
assert run("7 7\n") == "7\n", "equal values"

# coprime numbers
assert run("9 28\n") == "252\n", "coprime numbers"

# maximum constraint values
assert run("1000 1000\n") == "1000\n", "maximum equal values"

# shared factors
assert run("12 18\n") == "36\n", "shared factors"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Smallest possible input |
| `7 7` | `7` | Equal numbers |
| `9 28` | `252` | Coprime numbers |
| `1000 1000` | `1000` | Maximum equal values |
| `12 18` | `36` | Proper handling of shared factors |

## Edge Cases

Consider the input:

```
6 8
```

The algorithm computes:

```
gcd(6, 8) = 2
```

Then:

```
(6 // 2) * 8 = 3 * 8 = 24
```

The output is:

```
24
```

This case confirms that shared factors are removed exactly once. A naive multiplication would incorrectly produce 48.

Now consider equal numbers:

```
7 7
```

The gcd is 7. The computation becomes:

```
(7 // 7) * 7 = 1 * 7 = 7
```

The algorithm correctly recognizes that the least common multiple of identical numbers is the number itself.

Finally, consider coprime numbers:

```
9 28
```

The gcd is 1, so:

```
(9 // 1) * 28 = 252
```

When the numbers share no factors, the lcm becomes their direct product. This matches the mathematical definition perfectly.
