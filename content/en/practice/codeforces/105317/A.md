---
title: "CF 105317A - Juan and Alfino"
description: "We are given two integers. One represents the cost of a single sandwich, and the other represents how much money Juan has available. Juan wants to spend his money only on full sandwiches and give them to friends, where each friend receives exactly one sandwich."
date: "2026-06-23T15:12:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105317
codeforces_index: "A"
codeforces_contest_name: "JPC 1.0"
rating: 0
weight: 105317
solve_time_s: 56
verified: true
draft: false
---

[CF 105317A - Juan and Alfino](https://codeforces.com/problemset/problem/105317/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers. One represents the cost of a single sandwich, and the other represents how much money Juan has available. Juan wants to spend his money only on full sandwiches and give them to friends, where each friend receives exactly one sandwich.

The task is to determine how many full sandwiches he can afford, which is equivalent to how many friends he can treat. Since each sandwich costs a fixed amount, the problem reduces to dividing the total available money by the price per sandwich and counting only complete purchases.

The constraints go up to $10^9$ for both values, which immediately rules out any simulation of spending one sandwich at a time. A loop that repeatedly subtracts the cost would take up to $10^9$ iterations in the worst case, which is far beyond what fits in one second in Python. The only viable approach is a constant-time arithmetic computation.

There are no tricky structural edge cases like arrays or graphs, but there is still a subtle correctness concern around integer division semantics. The result must be the number of complete sandwiches, meaning fractional affordability must be discarded. For example, if the cost is 5 and the money is 4, the correct answer is 0, not 0.8 or 1 due to rounding mistakes. Any implementation that uses floating-point division risks precision issues for large inputs near $10^9$.

## Approaches

The naive approach mirrors the story directly. We repeatedly subtract the cost of one sandwich from Juan’s money until he can no longer afford another one. Each subtraction corresponds to buying one sandwich and increasing the count of friends served. This is correct because each step reduces the remaining budget in valid discrete units.

However, this method becomes extremely slow when the cost is small and the budget is large. If the cost is 1 and the money is $10^9$, we would perform $10^9$ iterations, each doing constant work. That already exceeds typical time limits by orders of magnitude.

The key observation is that this repeated subtraction is exactly integer division. Instead of simulating each purchase, we can directly compute how many times the cost fits into the budget. This reduces the entire process to a single arithmetic operation.

The structure of the problem guarantees independence between purchases, there are no discounts, no accumulation effects, and no constraints linking purchases together. That makes the quotient $m \div c$ sufficient to describe the final answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (repeated subtraction) | O(m / c) | O(1) | Too slow |
| Optimal (integer division) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two integers $c$ and $m$ from input. These represent the cost per sandwich and total available money.
2. Compute how many whole sandwiches fit into the budget using integer division $m // c$. This operation automatically discards any remainder, which corresponds to unusable leftover money that cannot buy a full sandwich.
3. Output the computed value as the number of friends Juan can treat.

### Why it works

Each sandwich consumes exactly $c$ units of money, and there is no way to combine partial money from different sandwiches. Any valid purchase sequence must consume money in chunks of size $c$. Therefore, the maximum number of valid chunks that fit into $m$ is exactly the quotient of $m$ divided by $c$. No arrangement can exceed this because it would imply exceeding the total budget, and no arrangement can be smaller because we can always buy sandwiches greedily until the remaining money is less than $c$.

## Python Solution

```python
import sys
input = sys.stdin.readline

c, m = map(int, input().split())
print(m // c)
```

The solution directly applies integer division. The use of `//` is crucial because it ensures floor division, which correctly models counting only complete sandwiches.

No loops or extra memory are needed. The entire computation is a single constant-time operation after parsing input.

## Worked Examples

### Example 1

Input:

```
3 10
```

We track the computation:

| Step | c | m | m // c | Output so far |
| --- | --- | --- | --- | --- |
| Start | 3 | 10 | - | - |
| Compute | 3 | 10 | 3 | 3 |

The result is 3 because 10 contains three full groups of size 3, with 1 unit of money left unused.

This confirms that leftover money does not contribute to an extra sandwich.

### Example 2

Input:

```
5 4
```

| Step | c | m | m // c | Output so far |
| --- | --- | --- | --- | --- |
| Start | 5 | 4 | - | - |
| Compute | 5 | 4 | 0 | 0 |

Here the budget is insufficient for even one sandwich, so the answer is 0. This shows that the algorithm correctly handles cases where $m < c$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only parsing input and performing a single division operation |
| Space | O(1) | No auxiliary data structures are used |

The constraints allow up to $10^9$, but the solution performs constant-time arithmetic, so it comfortably fits within limits even in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    c, m = map(int, input().split())
    return str(m // c)

# provided samples
assert run("3 10") == "3"
assert run("5 39") == "7"

# custom cases
assert run("1 1") == "1", "minimum valid equal case"
assert run("1 1000000000") == "1000000000", "maximum budget single cost"
assert run("10 9") == "0", "just below threshold"
assert run("7 49") == "7", "exact division case"
assert run("6 1") == "0", "budget smaller than cost"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | smallest non-zero case |
| 1 1000000000 | 1000000000 | maximum output scale |
| 10 9 | 0 | strictly insufficient budget |
| 7 49 | 7 | exact divisibility correctness |
| 6 1 | 0 | no purchase possible case |

## Edge Cases

One edge case is when the budget is smaller than the cost. For input `c = 10, m = 3`, the algorithm computes `3 // 10 = 0`. This is correct because no full sandwich can be bought, and integer division naturally enforces this without special handling.

Another edge case is when the budget is exactly divisible by the cost, such as `c = 4, m = 12`. The computation yields `12 // 4 = 3`, and there is no remainder. The algorithm correctly counts all available purchases without overcounting.

A final case is when both values are at their maximum size, for example `c = 10^9, m = 10^9`. The result is `1`, and the computation remains safe because Python’s integer arithmetic handles large integers natively and division is constant time at this scale in competitive programming contexts.
