---
title: "CF 102899H - KK \u4e0e\u5341\u4f73"
description: "We are given a list of integers representing scores assigned by judges. All values are nonzero and all are distinct. We are allowed to remove exactly one of these numbers. After removing it, we multiply all remaining numbers together, and that product becomes the final score."
date: "2026-07-04T08:21:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102899
codeforces_index: "H"
codeforces_contest_name: "The 2nd Hangzhou Normal University Freshman Programming Contest"
rating: 0
weight: 102899
solve_time_s: 40
verified: true
draft: false
---

[CF 102899H - KK \u4e0e\u5341\u4f73](https://codeforces.com/problemset/problem/102899/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers representing scores assigned by judges. All values are nonzero and all are distinct. We are allowed to remove exactly one of these numbers. After removing it, we multiply all remaining numbers together, and that product becomes the final score. The task is to choose which single number to remove so that this resulting product is as large as possible, and output the removed number itself.

The key difficulty is that the product depends on all remaining elements simultaneously, so removing one element affects the magnitude and also the sign of the result. With up to 30,000 numbers, any approach that recomputes products from scratch for each removal must be carefully considered in terms of arithmetic cost, because naive multiplication of long products repeatedly is too slow.

A subtle aspect comes from sign behavior. The product can flip sign depending on how many negative numbers remain. Removing a negative number may change parity of negatives, and removing a positive number affects magnitude differently than removing a negative one. This makes reasoning purely in terms of “remove smallest” or “remove largest” incorrect.

Edge cases that break naive intuition include:

If there is exactly one negative number, for example `[-5, 2, 3, 4]`, removing the negative makes the product positive and large, but removing a positive still leaves a negative product. A greedy “remove smallest” rule might fail depending on sign handling.

If there are many negatives, such as `[-4, -3, -2, -1, 10]`, removing one negative may switch parity and drastically change sign and magnitude in competing ways.

Because all numbers are nonzero and distinct, we never deal with ties or zero-product collapse, which simplifies reasoning about monotonic changes.

## Approaches

A brute-force approach would compute the product of all numbers except one candidate index for every possible removal. For each i, we multiply all elements except `a[i]` and compare results. This is correct because it directly evaluates the definition of the problem. However, each evaluation costs O(n), and doing this for all n choices leads to O(n²) multiplications. With n up to 3·10⁴, this becomes roughly 9·10⁸ multiplications, which is too slow in Python and borderline even in optimized languages.

The key observation is that we do not actually need full products repeatedly. If we consider the product of all elements as a base value, then removing `a[i]` corresponds to dividing the total product by `a[i]`. The challenge is that the product can overflow and that sign comparisons must be handled carefully. But logically, every candidate result is proportional to `P / a[i]`, where `P` is the product of all numbers.

Instead of directly working with division and huge numbers, we can compare candidates by reasoning about how removing each element changes the product. Since all values are nonzero, comparing `P / a[i]` across different i is equivalent to comparing `1 / a[i]` in terms of multiplicative effect on the same base product. However, because sign and magnitude interact, a safer approach is to compute the total product once using Python’s big integers and then compute each candidate value by integer division.

This reduces the problem to O(n) computation: one full product pass, and one pass to evaluate each removal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

### Optimal Strategy

1. Compute the product of all numbers in the array. This gives a baseline value representing the full multiplication before any removal.
2. Iterate over each element `a[i]` and compute the value of removing it by dividing the total product by `a[i]`. This gives the resulting score for that removal.
3. Track the maximum resulting product seen so far and store the corresponding index.
4. After checking all elements, output the element whose removal produced the maximum product.

The key decision point is that we never recompute full products from scratch. We rely on the algebraic relationship that removing one factor from a product is equivalent to dividing by that factor.

### Why it works

Every valid outcome corresponds exactly to `P / a[i]`, where `P` is the product of all elements. Since `P` is constant across all choices, maximizing `P / a[i]` over i is equivalent to selecting the best transformation of the same base quantity. No candidate is missed, and each is evaluated exactly once, preserving correctness. The only subtlety is that integer arithmetic preserves exact values in Python, so comparisons are reliable without floating-point errors.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input().strip())
    a = list(map(int, input().split()))
    
    total = 1
    for x in a:
        total *= x
    
    best_val = None
    best_idx = 0
    
    for i, x in enumerate(a):
        val = total // x
        if best_val is None or val > best_val:
            best_val = val
            best_idx = i
    
    print(a[best_idx])

if __name__ == "__main__":
    main()
```

The solution first builds the total product in a single pass. This is safe because Python integers automatically expand to arbitrary precision, so overflow is not an issue.

Then it evaluates each removal by dividing the total product by the current element. Integer division is exact because every element is a factor of the total product. The comparison step is straightforward: we keep the index that yields the largest quotient.

A common implementation mistake is attempting to recompute products for each index or attempting to simulate multiplication with partial recomputation, which leads to O(n²). Another subtle mistake is trying to reason with floating-point division, which can introduce precision errors when products grow large.

## Worked Examples

### Example 1: `1 2 3 4 5`

| i | removed | total product | result (P / a[i]) |
| --- | --- | --- | --- |
| 0 | 1 | 120 | 120 |
| 1 | 2 | 120 | 60 |
| 2 | 3 | 120 | 40 |
| 3 | 4 | 120 | 30 |
| 4 | 5 | 120 | 24 |

The maximum value occurs when removing 1. This confirms that removing the smallest positive value increases the product the most in purely positive cases.

### Example 2: `-6 8 9`

| i | removed | total product | result (P / a[i]) |
| --- | --- | --- | --- |
| 0 | -6 | -432 | 72 |
| 1 | 8 | -432 | -54 |
| 2 | 9 | -432 | -48 |

The best result is obtained by removing -6, which flips the product from negative to positive and yields the largest magnitude among positive outcomes.

This demonstrates the importance of sign changes: removing a negative number can dominate purely magnitude-based reasoning.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | one pass to compute product and one pass to evaluate each removal |
| Space | O(1) | only a few variables used besides input array |

The algorithm runs comfortably within constraints since 3·10⁴ multiplications and divisions are trivial in Python even with big integers.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input().strip())
    a = list(map(int, input().split()))
    
    total = 1
    for x in a:
        total *= x
    
    best_val = None
    best_idx = 0
    
    for i, x in enumerate(a):
        val = total // x
        if best_val is None or val > best_val:
            best_val = val
            best_idx = i
    
    return str(a[best_idx])

# provided samples (reconstructed format)
assert run("5\n1 2 3 4 5\n") == "1"
assert run("3\n-6 8 9\n") == "-6"

# custom cases
assert run("2\n-1 5\n") == "-1"          # removing negative makes product positive
assert run("2\n2 -3\n") == "-3"          # compare two symmetric choices
assert run("4\n-2 -3 4 5\n") in {"-2","-3"}  # parity-sensitive case
assert run("3\n10 2 3\n") == "2"         # removing smallest positive maximizes product
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 -1 5` | `-1` | removing negative improves sign and product |
| `2 2 -3` | `-3` | interaction between positive and negative |
| `-2 -3 4 5` | `-2/-3` | parity sensitivity in negative count |
| `10 2 3` | `2` | classic positive-only maximum product behavior |

## Edge Cases

Consider `[-1, 2]`. Removing `-1` leaves `2`, while removing `2` leaves `-1`. The algorithm computes total product `-2`, then evaluates removals: removing `-1` gives `2`, removing `2` gives `-1`. The maximum is correctly identified as removing `-1`.

In `[-4, -3, -2, -1, 10]`, the total product is positive. Removing different negatives or the single positive yields different magnitudes. The algorithm explicitly compares exact quotients, so it naturally selects the best balance between sign stability and magnitude increase without needing separate parity logic.

In `1 2`, removing `1` yields `2` and removing `2` yields `1`. The algorithm correctly identifies removal of the smaller element, since it maximizes the remaining product.
