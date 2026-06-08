---
title: "CF 1996A - Legs"
description: "The farm has only chickens and cows, and Farmer John counts a total of n legs. Chickens contribute 2 legs each and cows contribute 4 legs each. The question asks for the smallest possible number of animals consistent with the total leg count."
date: "2026-06-08T14:41:05+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 1996
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 962 (Div. 3)"
rating: 800
weight: 1996
solve_time_s: 132
verified: true
draft: false
---

[CF 1996A - Legs](https://codeforces.com/problemset/problem/1996/A)

**Rating:** 800  
**Tags:** binary search, math, ternary search  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

The farm has only chickens and cows, and Farmer John counts a total of `n` legs. Chickens contribute 2 legs each and cows contribute 4 legs each. The question asks for the smallest possible number of animals consistent with the total leg count. Essentially, we are distributing `n` legs into groups of 2 and 4, while minimizing the sum of animals.

The input is multiple test cases. Each test case is a single even integer `n` representing the total legs counted. The output is one integer per test case: the minimum number of animals that could generate exactly `n` legs.

The constraints are small: `n` goes up to 2000 and `t` is up to 1000. Since `n` is bounded, any solution with linear operations in `n` per test case (O(n)) will run comfortably in under a second. We also know `n` is always even, which simplifies some edge cases - we never have to handle odd totals of legs.

An edge case arises when `n` is very small, like `2`. In that case, the only possibility is a single chicken, even though there are technically multiple combinations of animals that sum to `n` legs in larger examples. Another subtle point is that the minimum number of animals occurs when we maximize the number of cows because each cow contributes more legs per animal, lowering the total count. A careless approach might try to split all legs into chickens first, producing too many animals.

## Approaches

A brute-force approach is to iterate over all possible numbers of cows from 0 to `n//4`, compute the remaining legs for chickens, and track the minimum total animals. This is correct because it enumerates all feasible combinations. The number of operations is proportional to `n//4` per test case. With `n` up to 2000, this is about 500 iterations per test case, acceptable given the constraints, but it is unnecessary because the solution can be expressed mathematically.

The key insight is that minimizing the number of animals is equivalent to maximizing the number of cows. If each cow has 4 legs, and each chicken has 2, then we first allocate as many cows as possible without exceeding `n`. The remaining legs are assigned to chickens. Algebraically, if `n` is even, the minimum number of animals is `n // 4` cows plus `(n % 4) / 2` chickens. Since `n` is even, `(n % 4)` is either 0 or 2, so the division always yields an integer. This converts the problem to a simple arithmetic calculation per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted but unnecessarily slow |
| Optimal | O(1) | O(1) | Accepted and efficient |

## Algorithm Walkthrough

1. For each test case, read the total leg count `n`. Since `n` is guaranteed even, we can safely divide by 2 or 4 without worrying about fractions.
2. Compute the maximum number of cows as `n // 4`. Each cow uses 4 legs, so using the maximum possible cows reduces the number of remaining animals.
3. Compute the remaining legs as `n % 4`. Because `n` is even, this is either 0 or 2.
4. The remaining legs are assigned to chickens. Since each chicken has 2 legs, the number of chickens is `(n % 4) // 2`.
5. Add the number of cows and chickens to get the total minimum number of animals.
6. Print the result for each test case.

Why it works: The invariant is that the maximum number of 4-legged animals always produces the minimum total number of animals. Any fewer cows would require more chickens to satisfy the same total legs, increasing the total number of animals. Because `n` is even, the leftover legs after allocating cows is always divisible by 2, so the calculation of chickens is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    cows = n // 4
    chickens = (n % 4) // 2
    print(cows + chickens)
```

In this code, `n // 4` determines the maximum number of cows, and `(n % 4) // 2` determines the remaining chickens. We do not need any loops or conditionals because the modulo and integer division handle all even `n`. Using `sys.stdin.readline` ensures fast input for multiple test cases.

## Worked Examples

### Sample 1

Input: 2

| n | cows = n//4 | remainder = n%4 | chickens = remainder//2 | total |
| --- | --- | --- | --- | --- |
| 2 | 0 | 2 | 1 | 1 |

This shows that 2 legs correspond to 1 chicken, confirming the minimal number of animals.

### Sample 2

Input: 6

| n | cows = n//4 | remainder = n%4 | chickens = remainder//2 | total |
| --- | --- | --- | --- | --- |
| 6 | 1 | 2 | 1 | 2 |

One cow uses 4 legs, leaving 2 legs for one chicken, giving a total of 2 animals. This confirms the algorithm maximizes cows first.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Arithmetic operations are constant time |
| Space | O(1) | Only a few integer variables are used |

With `t` up to 1000, the total time is well under the limit. Memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        cows = n // 4
        chickens = (n % 4) // 2
        print(cows + chickens)
    return output.getvalue().strip()

# provided samples
assert run("3\n2\n6\n8\n") == "1\n2\n2", "sample 1"

# custom cases
assert run("2\n4\n10\n") == "1\n3", "boundary case"
assert run("1\n2000\n") == "500", "maximum input"
assert run("1\n14\n") == "4", "even n not divisible by 4"
assert run("1\n16\n") == "4", "n divisible by 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4,10 | 1,3 | Edge cases with small even numbers, one divisible by 4 |
| 2000 | 500 | Maximum n, large input efficiency |
| 14 | 4 | Even n not divisible by 4 |
| 16 | 4 | n divisible by 4 exactly |

## Edge Cases

For the smallest input, n=2, the algorithm computes `0` cows and `1` chicken, correctly yielding 1 animal. For n not divisible by 4 but still even, such as n=6, we assign 1 cow and 1 chicken, which is fewer animals than 3 chickens, demonstrating that maximizing cows reduces total animals. For large n, like n=2000, the integer division and modulo operations remain correct and fast. The algorithm handles all even n in the allowed range without any special casing.
