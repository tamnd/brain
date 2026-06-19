---
title: "CF 106199A - \u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0441\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u044f"
description: "We are given an array of integers and asked to compare two expressions built from it. The first expression takes the greatest common divisor of all array elements and then applies factorial to that result."
date: "2026-06-19T18:33:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106199
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2024-2025, \u0412\u0442\u043e\u0440\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 106199
solve_time_s: 56
verified: true
draft: false
---

[CF 106199A - \u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0441\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u044f](https://codeforces.com/problemset/problem/106199/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and asked to compare two expressions built from it. The first expression takes the greatest common divisor of all array elements and then applies factorial to that result. The second expression instead takes factorial of each element first and then computes the gcd of those factorial values. The task is to decide whether these two values are always equal for the given array.

The input size can reach up to 100000 elements, and each element can be as large as 10^9. This immediately rules out any approach that tries to compute factorials explicitly, since factorial grows extremely fast and becomes infeasible even for modest inputs. Even storing or manipulating full factorial values is impossible, so any solution must rely on structural properties of gcd and factorial rather than direct computation.

A subtle edge case appears when the gcd of the array is 1. In that case the left expression becomes 1! which is 1. The right expression also becomes gcd of a list of factorials, and since every factorial is divisible by 1, the result is also 1. So arrays with gcd equal to 1 are always valid.

A more interesting situation occurs when the gcd is greater than 1. For example, if all numbers are multiples of 2 but some are not multiples of higher powers like 4 or 8, factorial behavior introduces extra prime factors that are not reflected in the original gcd structure. This mismatch is the source of inequality.

A minimal counterexample intuition already appears with small numbers like 2 and 3. Their gcd is 1 so equality holds, but once all numbers share a common divisor greater than 1, the factorial structure amplifies prime exponents in a way that can break equality.

## Approaches

A brute-force attempt would directly compute the gcd of the array, compute its factorial, and also compute factorial for each element and then take gcd. The first part is fine, but the second part fails immediately because even 20! already exceeds 10^18, and here values go up to 10^9, making factorial values astronomically large. Even using big integers, computing 100000 factorials is impossible within time limits.

The key observation is that factorial structure is entirely driven by prime exponents. For a number x!, the exponent of a prime p is determined by Legendre’s formula. When we take gcd of factorials, we are effectively taking the minimum exponent across all these Legendre sums. The question reduces to whether applying factorial before or after gcd preserves these minimum exponent relationships.

The decisive simplification is that the two expressions are equal if and only if the gcd of the array is 1. If the gcd is 1, both sides evaluate to 1 as explained earlier. If the gcd is greater than 1, then all elements share at least one prime factor, and factorial amplification makes the second expression strictly larger than the first in terms of exponent structure, breaking equality.

Thus the entire problem collapses to a single gcd computation over the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (factorials + gcd) | Impossible (factorial blowup) | O(n) + huge integers | Not usable |
| Optimal (check gcd only) | O(n log A) | O(1) | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Compute the gcd of all elements in the array. This value captures the maximum integer that divides every element simultaneously, which is exactly the only structural information needed.
2. Check whether this gcd equals 1. This is the only decision point in the problem, because the equality of expressions depends entirely on whether a nontrivial common divisor exists.
3. If the gcd is 1, output YES. Otherwise output NO.

### Why it works

The factorial operation preserves divisibility but amplifies prime exponents in a non-linear way. When all numbers are coprime in aggregate (gcd equals 1), no prime factor is forced to appear in every element, and both constructions collapse to 1. When a nontrivial gcd exists, every number contains at least one shared prime factor, and factorials introduce additional multiplicities of these primes that are not synchronized across the array, causing the gcd of factorials to exceed the factorial of the gcd. This structural mismatch guarantees inequality whenever gcd is greater than 1.

## Python Solution

```python
import sys
input = sys.stdin.readline

from math import gcd

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    g = 0
    for x in a:
        g = gcd(g, x)
    
    if g == 1:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The implementation directly follows the reduction to a single gcd computation. The gcd is accumulated iteratively, which avoids storing intermediate results or doing any expensive factorial-related work. The final comparison is constant time.

A subtle detail is initializing the gcd accumulator with 0. This is safe because gcd(0, x) = x, so it correctly seeds the computation with the first array element without special casing.

## Worked Examples

### Example 1

Input:

```
5
1 2 3 4 5
```

| Step | Current gcd |
| --- | --- |
| start | 0 |
| after 1 | 1 |
| after 2 | 1 |
| after 3 | 1 |
| after 4 | 1 |
| after 5 | 1 |

The final gcd is 1, so the answer is YES. This matches the fact that no number greater than 1 divides all elements simultaneously, and both expressions collapse to 1.

### Example 2

Input:

```
3
6 30 15
```

| Step | Current gcd |
| --- | --- |
| start | 0 |
| after 6 | 6 |
| after 30 | 6 |
| after 15 | 3 |

The final gcd is 3, so the answer is NO. Here all numbers share a common factor greater than 1, and factorial amplification creates a mismatch between the two constructions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log A) | Each gcd operation runs in logarithmic time in the value size |
| Space | O(1) | Only a single accumulator is stored |

The constraints allow up to 100000 numbers with values up to 10^9, so an iterative gcd pass is easily fast enough within one second.

## Test Cases

```python
import sys, io
from math import gcd

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    
    g = 0
    for x in a:
        g = gcd(g, x)
    
    return "YES" if g == 1 else "NO"

# provided samples
assert run("5\n1 2 3 4 5\n") == "YES"
assert run("3\n6 30 15\n") == "NO"

# custom cases
assert run("1\n1\n") == "YES", "single element 1"
assert run("1\n10\n") == "NO", "single element >1"
assert run("4\n2 4 8 16\n") == "NO", "all even numbers"
assert run("3\n2 3 5\n") == "YES", "pairwise coprime-ish"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | YES | single element edge |
| 10 | NO | single non-one element |
| 2 4 8 16 | NO | common divisor > 1 |
| 2 3 5 | YES | gcd equals 1 case |

## Edge Cases

When the array contains a single element equal to 1, the gcd is 1 and the answer is YES, matching both expressions evaluating to 1. When the array contains a single element greater than 1, the gcd equals that element, and the answer becomes NO since factorial amplification on the right side cannot match the left structure.

For arrays where all elements share a common divisor like 2, the gcd becomes at least 2 and the algorithm outputs NO. The gcd computation directly captures this condition without needing to inspect factorial behavior.
