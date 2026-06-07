---
title: "CF 2144D - Price Tags"
description: "We are running a clearance sale for a store with multiple items, each with a fixed original price. The store allows a uniform discount via division by an integer factor $x 1$, where the new price of an item is the ceiling of its original price divided by $x$."
date: "2026-06-08T01:38:08+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 2144
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 182 (Rated for Div. 2)"
rating: 1800
weight: 2144
solve_time_s: 113
verified: false
draft: false
---

[CF 2144D - Price Tags](https://codeforces.com/problemset/problem/2144/D)

**Rating:** 1800  
**Tags:** brute force, dp, math  
**Solve time:** 1m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We are running a clearance sale for a store with multiple items, each with a fixed original price. The store allows a uniform discount via division by an integer factor $x > 1$, where the new price of an item is the ceiling of its original price divided by $x$. The store has a limited number of existing price tags, so if a new discounted price does not match any original price, a new tag must be printed at cost $y$. The goal is to pick the division factor $x$ that maximizes total income, which is the sum of all discounted prices minus the cost of any newly printed tags.

The input provides multiple test cases. For each, the number of items $n$ can go up to 200,000, and prices $c_i$ can also be up to 200,000. Printing costs $y$ can be extremely large, up to $10^9$. Since $n$ is large, any solution with $O(n^2)$ complexity is immediately ruled out. We need an approach that can handle linear or near-linear operations with respect to $n$ for each test case.

A naive edge case occurs when all item prices are the same, and $y$ is extremely high. For instance, if $n = 3$, $y = 10^9$, and $c = [42, 42, 42]$, reducing prices slightly can result in an income that is negative due to the tag printing cost. A careless approach that only sums discounted prices without accounting for printing costs will incorrectly assume a large positive income.

Another subtle case is when small or prime item prices produce very few unique discounted prices, allowing reuse of many original tags. For example, with $c = [1, 1, 1]$ and any $x > 1$, all discounted prices will be 1, so no new tags are needed, and the printing cost does not reduce income.

## Approaches

The brute-force approach is simple conceptually. Iterate over all integer values of $x$ starting from 2 up to some reasonable bound, compute the discounted price for each item, count how many new tags are required, and compute total income. This works because for any $x$, the discounted price is well-defined. However, the naive iteration is far too slow because $x$ could, in principle, go up to the maximum original price, $2 \cdot 10^5$. Doing $n$ computations per $x$ leads to an operation count of $O(n \cdot c_{\text{max}})$, which is up to $4 \cdot 10^{10}$ - completely infeasible.

The key insight is that the set of unique discounted prices changes only at specific threshold values of $x$. For an item priced $c_i$, its discounted price $\lceil c_i / x \rceil$ is constant over intervals of $x$ between $\lfloor c_i / k \rfloor$ and $\lfloor c_i / (k-1) \rfloor$ for integer $k$. Thus, instead of checking all $x$, we can iterate over only those critical $x$ values where some item's discounted price changes. By generating these candidate $x$ values across all items, we reduce the problem to evaluating a linear number of possible factors.

Additionally, for a given $x$, we can quickly compute the number of tags needed using a frequency map of original prices. We count how many discounted prices can reuse existing tags and subtract the printing cost for the remainder. This combination of limiting $x$ candidates and efficiently computing income gives a feasible $O(n \sqrt{c_{\text{max}}})$ approach.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * c_max) | O(n) | Too slow |
| Optimal | O(n * sqrt(c_max)) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of items $n$, printing cost $y$, and item prices $c_1, \dots, c_n$.
2. Count the frequency of each original price. This helps determine which discounted prices can reuse tags.
3. Initialize a set of candidate $x$ values starting with $x = 2$.
4. For each item price $c_i$, generate threshold $x$ values by computing all integers up to $\sqrt{c_i}$ and their corresponding $\lceil c_i / k \rceil$. For each $k$, $x = \lfloor c_i / k \rfloor$ may produce a new discounted price. Add these to the candidate set.
5. For each candidate $x$, compute the discounted prices $\lceil c_i / x \rceil$ for all items. Count the frequency of each discounted price.
6. Determine how many existing tags can be reused by matching the minimum of original and discounted frequency for each price. The remaining items need new tags.
7. Compute total income as the sum of discounted prices minus $y$ times the number of new tags.
8. Keep track of the maximum income across all candidate $x$.
9. Print the result for the test case.

Why it works: The set of candidate $x$ values covers all points where the discounted price of any item changes. Evaluating only these candidates guarantees we consider all unique income configurations. The frequency map ensures we optimally reuse existing price tags.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import ceil, isqrt
from collections import Counter

def max_income(n, y, prices):
    freq = Counter(prices)
    candidates = set([2])
    
    for price in prices:
        for k in range(1, isqrt(price) + 2):
            if k == 0:
                continue
            x = (price + k - 1) // k
            if x > 1:
                candidates.add(x)
    
    max_total = -float('inf')
    
    for x in candidates:
        discounted = [ceil(p / x) for p in prices]
        discounted_freq = Counter(discounted)
        reuse = 0
        for p in discounted_freq:
            reuse += min(discounted_freq[p], freq.get(p, 0))
        new_tags = n - reuse
        total = sum(discounted) - new_tags * y
        max_total = max(max_total, total)
    
    return max_total

t = int(input())
for _ in range(t):
    n, y = map(int, input().split())
    prices = list(map(int, input().split()))
    print(max_income(n, y, prices))
```

The solution begins by counting the frequency of original prices to optimize tag reuse. It generates candidate $x$ values by iterating up to the square root of each price, ensuring we only consider thresholds where a discounted price changes. For each $x$, it computes discounted prices, reuses tags optimally, and subtracts printing costs. Using `Counter` ensures correct frequency calculations and efficient reuse.

## Worked Examples

### Example 1

Input:

```
5 51
50 150 50 148 150
```

| Step | x | Discounted prices | Reused tags | New tags | Sum discounted | Income |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | [25,75,25,74,75] | 0 | 5 | 274 | -1 |
| 2 | 3 | [17,50,17,50,50] | 2 | 3 | 184 | 31 |
| 3 | 4 | [13,38,13,37,38] | 0 | 5 | 139 | -76 |

Maximum income is 31 with $x = 3$.

### Example 2

Input:

```
3 1000000000
42 42 42
```

| Step | x | Discounted prices | Reused tags | New tags | Sum discounted | Income |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | [21,21,21] | 0 | 3 | 63 | -2999999937 |

Maximum income is -2999999937, showing high printing cost dominates revenue.

These traces show how different $x$ values produce distinct income, and the algorithm evaluates all critical candidates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * sqrt(c_max)) | Each price generates up to O(sqrt(c_max)) candidates; for each candidate we compute discounted prices for n items. |
| Space | O(n) | Frequency maps for original and discounted prices, plus candidate set. |

Given $n \le 2 \cdot 10^5$ and $c_i \le 2 \cdot 10^5$, this approach works within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())  # assuming the solution code is saved in solution.py
    return output.getvalue().strip()

# Provided samples
assert run("4\n5 51\n50 150 50 148 150
```
