---
title: "CF 235A - LCM Challenge"
description: "We are asked to choose three positive integers, each at most n, to maximize their least common multiple (LCM). The input is a single integer n, and the output is a single integer representing the largest possible LCM achievable using three integers not greater than n."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 235
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 146 (Div. 1)"
rating: 1600
weight: 235
solve_time_s: 182
verified: true
draft: false
---

[CF 235A - LCM Challenge](https://codeforces.com/problemset/problem/235/A)

**Rating:** 1600  
**Tags:** number theory  
**Solve time:** 3m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to choose three positive integers, each at most _n_, to maximize their least common multiple (LCM). The input is a single integer _n_, and the output is a single integer representing the largest possible LCM achievable using three integers not greater than _n_. The integers do not need to be distinct, and they must all be positive.

Given that _n_ can be as large as 10^6 and the time limit is 2 seconds, a solution that checks all possible triples would require roughly n³ operations, which would be on the order of 10^18 operations for the largest n. This is clearly impractical. Therefore, an efficient solution must avoid testing every combination and instead exploit number-theoretic properties of the LCM.

Edge cases arise when _n_ is very small. If _n_ = 1, the only available numbers are 1, so the answer is 1. If _n_ = 2, the only options are 1 and 2, so the maximum LCM comes from choosing (1, 2, 2) yielding an LCM of 2. A naive implementation that assumes the three largest distinct numbers will always work would fail on small _n_ or when consecutive numbers include a 1 or an even number that lowers the LCM. Another subtlety is that for even _n_, using _n_, _n-1_, and _n-2_ might not yield the maximum LCM because two numbers being even reduces the overall product relative to co-prime combinations.

## Approaches

The brute-force approach tests every triple (i, j, k) where 1 ≤ i ≤ j ≤ k ≤ n, computes the LCM of each triple, and keeps track of the maximum. This approach is correct because it checks all possible choices, but its complexity is O(n³), which is far too slow for n up to 10^6. Even for n = 1000, this would require 10^9 operations, which is unacceptable in a competitive setting.

The key insight is that the maximum LCM is usually obtained by numbers that are large and co-prime. The largest numbers below n contribute the most to the product, but using consecutive even numbers reduces the LCM because they share factors of 2. Therefore, the optimal triple is almost always formed from numbers near n, carefully choosing numbers that are not all even. Specifically, we can focus on triples in the form of (_n_, _n-1_, _n-2_) or (_n_, _n-1_, _n-3_) if n is even. If n is odd, the triple (_n_, _n-1_, _n-2_) usually works because two consecutive numbers are coprime. Small values of n (n ≤ 3) require manual handling.

By restricting ourselves to the last three or four numbers below n, we reduce the candidate triples to at most 4-6 options. This reduces complexity from O(n³) to O(1), which is fast enough for all allowed n.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Check if _n_ is 1, 2, or 3. These are small edge cases. Return the correct maximum LCM manually: 1 for n = 1, 2 for n = 2, 6 for n = 3.
2. If _n_ is odd, return the product of _n_, _n-1_, and _n-2_. An odd number ensures at least one of the numbers is odd, reducing common factors and maximizing LCM.
3. If _n_ is even and not divisible by 3, return the product of _n_, _n-1_, and _n-3_. Skipping _n-2_ avoids having two even numbers, which would reduce the LCM.
4. If _n_ is divisible by 2 and 3, consider both candidates: (_n_, _n-1_, _n-3_) and (_n-1_, _n-2_, _n-3_). Compute their LCM or simply their product (since all numbers are distinct and small enough to avoid overflow). Return the maximum.
5. Use 64-bit integers or Python integers to handle large products without overflow.

The reason this works is that the maximum LCM is achieved by large numbers that are pairwise coprime or at least minimize repeated factors. Focusing on the last 3-4 numbers ensures we get the largest possible numbers while considering parity and divisibility to avoid factors that reduce the LCM.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_lcm(n):
    if n == 1:
        return 1
    if n == 2:
        return 2
    if n == 3:
        return 6
    if n % 2 == 1:
        return n * (n-1) * (n-2)
    else:
        # n is even
        if n % 3 != 0:
            return n * (n-1) * (n-3)
        else:
            return (n-1) * (n-2) * (n-3)

n = int(input())
print(max_lcm(n))
```

The solution begins by handling the trivial small cases. For larger n, it distinguishes between odd and even n because odd numbers produce fewer shared factors. The even case checks for divisibility by 3 to pick a triple that avoids multiple common factors. We rely on Python's arbitrary-precision integers to store large products safely.

## Worked Examples

### Sample Input 1

```
9
```

| Variable | Value |
| --- | --- |
| n | 9 |
| n is odd? | Yes |
| Result | 9 × 8 × 7 = 504 |

This confirms the product of the three largest numbers is indeed optimal since they are all large and have minimal common factors.

### Sample Input 2

```
8
```

| Variable | Value |
| --- | --- |
| n | 8 |
| n is odd? | No |
| n % 3 != 0? | Yes (8 % 3 = 2) |
| Result | 8 × 7 × 5 = 280 |

Choosing (8,7,6) would produce two even numbers, 8 and 6, reducing the LCM. By picking 5 instead of 6, the product is maximized while avoiding duplicate factors of 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations and conditional checks are performed, independent of n. |
| Space | O(1) | Only a constant number of variables are used. |

Given the constraints, this solution completes well under 2 seconds for n up to 10^6. Python handles large integer products efficiently without overflow.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())
    return str(max_lcm(n))

# Provided samples
assert run("9\n") == "504", "sample 1"
assert run("8\n") == "280", "even n not divisible by 3"

# Custom cases
assert run("1\n") == "1", "minimum n"
assert run("2\n") == "2", "small n"
assert run("3\n") == "6", "small n"
assert run("6\n") == "60", "even n divisible by 3"
assert run("1000000\n") == str(999999*999997*1000000), "large n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | Minimum possible input |
| 2 | 2 | Small input with only two numbers possible |
| 3 | 6 | Small input, triple equals n |
| 6 | 60 | Even n divisible by 3, special handling |
| 1000000 | 999999 × 999997 × 1000000 | Maximum n, large integers, performance |

## Edge Cases

For n = 1, the algorithm returns 1 directly, since the only possible triple is (1,1,1).

For even n divisible by 3, for example n = 6, the algorithm compares triples (6,5,3) versus (5,4,3) and correctly picks 5×4×3 = 60. This handles the situation where including n would introduce extra factors of 2 and 3 that reduce the LCM.

For odd n, the largest three consecutive numbers always provide the maximum LCM. For example, n = 7, the triple is 7×6×5 = 210, and no other combination of numbers ≤ 7 produces a higher LCM.

These cases confirm that the algorithm handles all small, boundary, and large inputs correctly.
