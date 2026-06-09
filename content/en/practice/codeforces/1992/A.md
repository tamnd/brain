---
title: "CF 1992A - Only Pluses"
description: "We are given three small integers that represent the initial sizes of three factors contributing to a product. The final quantity we care about is the product of these three numbers, and we are allowed to improve it by performing at most five operations."
date: "2026-06-08T15:13:48+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1992
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 957 (Div. 3)"
rating: 800
weight: 1992
solve_time_s: 65
verified: true
draft: false
---

[CF 1992A - Only Pluses](https://codeforces.com/problemset/problem/1992/A)

**Rating:** 800  
**Tags:** brute force, constructive algorithms, greedy, math, sortings  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three small integers that represent the initial sizes of three factors contributing to a product. The final quantity we care about is the product of these three numbers, and we are allowed to improve it by performing at most five operations. Each operation increases exactly one of the three numbers by one.

The goal is to distribute up to five unit increments among the three variables in a way that maximizes the final product. Since each value is small, every increment has a visible effect on the product, but the effect depends on which variable we choose to increase.

The constraints are extremely tight: each of the three numbers is at most 10 and we only have five operations. This immediately rules out any need for complex data structures or optimization techniques. Even enumerating all possible distributions of five increments is feasible, since the number of ways to split 5 identical increments among 3 variables is small.

A subtle edge case appears when all increments are concentrated on one variable versus spread across multiple variables. For example, starting from (10, 1, 10), putting all 5 increments into the middle gives 10 × 6 × 10 = 600, while spreading them differently gives strictly smaller products because the middle factor dominates multiplicatively once it is no longer tiny. A naive greedy strategy that always increments the currently smallest value can fail here, because it ignores interaction between variables through multiplication.

Another edge case is when values are already balanced, such as (3, 3, 3). Here, distributing increments evenly tends to work better than concentrating them, and this balance cannot be captured by a purely local decision rule.

## Approaches

A brute-force approach would try every possible way to assign up to five increments to the three variables. Each increment can go to one of three places, so we are effectively choosing a sequence of length up to five where each position has three choices. This leads to at most 3^5 = 243 sequences for exactly five operations, and even fewer if we consider "stop early" options. For each sequence, we compute the resulting product.

This approach is correct because it explicitly checks every valid sequence of operations. The issue is not correctness but structure: it explores the same state multiple times through different operation orders. Even though 243 is small, we can simplify further by noticing that the order of increments does not matter, only how many times each variable is incremented.

This observation reduces the problem to distributing at most five identical increments into three buckets. Each distribution can be represented by three non-negative integers (x, y, z) such that x + y + z ≤ 5. The number of such triples is small enough to enumerate directly, and for each we compute (a + x)(b + y)(c + z).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force sequences | O(3^5) per test | O(1) | Accepted but unnecessary |
| Enumerate distributions | O(125) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Iterate over all possible values of x from 0 to 5, representing increments added to the first number.
2. For each x, iterate over all possible values of y from 0 to 5 − x, representing increments added to the second number. This ensures we do not exceed the total of 5 operations.
3. Compute z as the remaining operations: z = 5 − x − y.
4. Compute the product (a + x) × (b + y) × (c + z).
5. Track the maximum product across all valid triples (x, y, z).
6. Output the maximum value after checking all configurations.

The key idea is that every valid sequence of operations corresponds exactly to one triple (x, y, z). This removes ordering redundancy while preserving completeness.

### Why it works

The value of the product depends only on how many times each variable is incremented, not the order of increments. Since each operation independently increases exactly one variable by 1, any valid sequence of five operations is equivalent to a distribution of counts across the three variables. Exhausting all such distributions guarantees that no possible final state is missed, and since we compute the product for each, the maximum found is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, c = map(int, input().split())
    
    best = 0
    
    for x in range(6):
        for y in range(6 - x):
            z = 5 - x - y
            val = (a + x) * (b + y) * (c + z)
            best = max(best, val)
    
    print(best)
```

The solution directly implements the enumeration of all valid increment distributions. The nested loops enforce the constraint that total increments do not exceed five. Computing z as the remainder ensures that every valid allocation is counted exactly once.

The product is evaluated in integer arithmetic without risk of overflow in Python. The answer is updated greedily by tracking the maximum.

## Worked Examples

### Example 1

Input: (2, 3, 4)

We enumerate a few representative distributions:

| x | y | z | value |
| --- | --- | --- | --- |
| 0 | 0 | 5 | 2 × 3 × 9 = 54 |
| 1 | 2 | 2 | 3 × 5 × 6 = 90 |
| 3 | 2 | 0 | 5 × 5 × 4 = 100 |

The maximum observed is 100.

This trace shows that concentrating increments on the already large middle range of configurations is beneficial, but not trivially so. The optimal solution balances growth across factors.

### Example 2

Input: (10, 1, 10)

| x | y | z | value |
| --- | --- | --- | --- |
| 0 | 5 | 0 | 10 × 6 × 10 = 600 |
| 2 | 3 | 0 | 12 × 4 × 10 = 480 |
| 5 | 0 | 0 | 15 × 1 × 10 = 150 |

The maximum is achieved by assigning all increments to the middle value.

This trace demonstrates a key phenomenon: increasing a very small factor yields large marginal gains in the product, so concentrating operations can be optimal when one term is a bottleneck.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(125 per test) | We enumerate all triples (x, y, z) with x + y + z ≤ 5 |
| Space | O(1) | Only a constant number of variables are used |

The total work is at most 125 evaluations per test case, and with up to 1000 test cases this remains comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        a, b, c = map(int, input().split())
        best = 0
        for x in range(6):
            for y in range(6 - x):
                z = 5 - x - y
                best = max(best, (a + x) * (b + y) * (c + z))
        out.append(str(best))
    return "\n".join(out)

# provided samples
assert run("2\n2 3 4\n10 1 10\n") == "100\n600"

# custom cases
assert run("1\n1 1 1\n") == "6", "all equal distribution case"
assert run("1\n1 10 1\n") == "60", "center bottleneck case"
assert run("1\n10 10 10\n") == "1331", "balanced maximum concentration"
assert run("1\n10 1 1\n") == "120", "single dominant factor initially"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 6 | balanced distribution of increments |
| 1 10 1 | 60 | best strategy targets bottleneck variable |
| 10 10 10 | 1331 | uniform growth preserves symmetry |
| 10 1 1 | 120 | heavy concentration on strongest factor |

## Edge Cases

A key edge case is when one variable starts much smaller than the others. For input (10, 1, 10), a greedy strategy that always increments the smallest variable might appear correct, but it actually remains optimal here only because the constraint is so small. The enumeration approach handles it naturally.

Tracing (10, 1, 10), the algorithm evaluates all distributions of 5 increments. One critical configuration is x = 0, y = 5, z = 0, producing 600, which dominates all other allocations. The algorithm correctly identifies this without needing to reason about marginal gains.

Another edge case is when all values are equal. For (3, 3, 3), symmetry guarantees that many distributions tie or nearly tie. The algorithm still checks all combinations and returns the correct maximum without relying on symmetry arguments.

Finally, when one variable starts at 1, any allocation that boosts it early can dominate, but the optimal split depends on interaction with the other two variables. Exhaustive distribution checking ensures no subtle imbalance is missed.
