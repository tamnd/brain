---
title: "CF 106063J - Juan vs Frank"
description: "The problem reduces the whole story to a single economic decision repeated for as many friends as possible. Each friend requires buying one identical item that costs a fixed amount of money, and Juan has a limited budget."
date: "2026-06-25T12:15:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106063
codeforces_index: "J"
codeforces_contest_name: "2025 ICPC Gran Premio de Mexico 3ra Fecha"
rating: 0
weight: 106063
solve_time_s: 39
verified: true
draft: false
---

[CF 106063J - Juan vs Frank](https://codeforces.com/problemset/problem/106063/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem reduces the whole story to a single economic decision repeated for as many friends as possible. Each friend requires buying one identical item that costs a fixed amount of money, and Juan has a limited budget. The question is asking for the maximum number of full purchases he can complete without exceeding his money.

In more concrete terms, the input gives two integers, the price of one item and the total amount of money available. Each purchase consumes exactly that fixed price from the budget, and leftover money that is insufficient for another full purchase cannot be used.

The output is a single integer representing how many complete purchases can be made.

The constraints are large but trivial for computation. Both values can go up to 10^9, which immediately rules out any simulation that subtracts repeatedly one by one in the worst case, since that would degrade to linear time in the amount of money. A direct loop could require up to 10^9 iterations in the worst case, which is far beyond the allowed time budget.

Instead, the structure of the problem strongly suggests a constant-time arithmetic operation is expected.

There are no tricky structural edge cases involving ordering or multiple inputs. The only subtle cases are boundary conditions when the budget is smaller than the cost, or exactly divisible by the cost. For example, if the cost is 5 and the budget is 4, no purchase is possible and the answer is 0. If the cost is 5 and the budget is 10, the answer is exactly 2. If the budget is not a multiple, say 39 with cost 5, then only the integer number of full purchases matters and the remainder is irrelevant.

A naive mistake would be to try to account for leftover money as if it could contribute partially, for example mistakenly rounding up instead of down. That would produce incorrect answers in cases like cost 5 and budget 6, where only 1 purchase is valid but a ceiling-based approach would incorrectly give 2.

## Approaches

The brute-force idea is straightforward: repeatedly subtract the cost from the budget while it remains non-negative, counting how many times this is possible. This is correct because each subtraction corresponds exactly to buying one item, and the process naturally stops when the remaining money is insufficient.

However, this approach is too slow when the budget is large. If the cost is 1 and the budget is 10^9, the loop runs 10^9 times, which cannot pass in a one-second time limit.

The key observation is that this repeated subtraction is exactly integer division. Instead of simulating each purchase, we can directly compute how many times the cost fits into the budget using a single division operation. This compresses the entire process into a constant-time computation while preserving correctness.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subtraction loop | O(m / c) | O(1) | Too slow |
| Direct integer division | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two integers representing the cost of one item and the total available money. These define a repeated subtraction process.
2. Compute how many full units of the cost fit into the budget using integer division. This directly corresponds to the number of complete purchases possible before the remaining money becomes insufficient.
3. Output the computed quotient as the final answer.

The reason this step is valid is that every purchase consumes an identical fixed amount, so the number of purchases depends only on how many disjoint copies of that amount can be packed into the total budget.

### Why it works

The total money can be viewed as a line segment of length m, and each purchase consumes a segment of fixed length c. The maximum number of non-overlapping segments of length c that fit into m is exactly the integer quotient of m divided by c. No arrangement or strategy changes this count because every item is identical and independent.

## Python Solution

```python
import sys
input = sys.stdin.readline

c, m = map(int, input().split())

print(m // c)
```

The solution reads two integers and immediately applies integer division. There is no need for loops or additional data structures because the problem is fully determined by a single arithmetic relationship.

A subtle point is ensuring integer division is used rather than floating-point division. Floating-point division followed by truncation could introduce precision issues for large values, while integer division is exact and safe.

## Worked Examples

### Example 1

Input:

```
3 10
```

| Step | Cost (c) | Money (m) | m // c | Output |
| --- | --- | --- | --- | --- |
| 1 | 3 | 10 | 3 | 3 |

Here, 3 full purchases can be made, leaving 1 unit of money unused. That remainder cannot fund another purchase, so it is ignored.

### Example 2

Input:

```
5 39
```

| Step | Cost (c) | Money (m) | m // c | Output |
| --- | --- | --- | --- | --- |
| 1 | 5 | 39 | 7 | 7 |

Seven purchases consume 35 units of money, leaving 4 units unused. Since 4 is less than 5, no further purchase is possible.

These examples confirm that the answer depends only on integer division, not on leftover money beyond full cost units.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only one arithmetic operation is performed regardless of input size |
| Space | O(1) | No additional memory beyond a few variables is used |

The solution easily fits within limits since it performs constant work per test case, and there is only one test case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    c, m = map(int, input().split())
    return str(m // c)

# provided samples
assert run("3 10") == "3"
assert run("2 4") == "2"
assert run("5 39") == "7"

# custom cases
assert run("5 4") == "0", "budget smaller than cost"
assert run("1 1000000000") == "1000000000", "maximal purchases"
assert run("7 7") == "1", "exact division"
assert run("8 15") == "1", "remainder ignored"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 4 | 0 | No purchase possible when budget is too small |
| 1 1000000000 | 1000000000 | Maximum stress case |
| 7 7 | 1 | Exact divisibility |
| 8 15 | 1 | Correct floor behavior |

## Edge Cases

A key edge case is when the budget is smaller than the cost. For input `5 4`, the algorithm computes `4 // 5`, which correctly yields 0. Any subtraction-based reasoning also stops immediately, but only the division approach guarantees this in constant time.

Another case is exact divisibility, such as `7 14` (not in samples but representative). The computation `14 // 7` gives 2, matching the fact that no remainder remains and no partial purchase is possible.

A final case is when the cost is 1. For input like `1 10^9`, the answer equals the budget itself, since every unit of money buys exactly one item. This tests that the implementation handles maximum values without overflow or performance issues.
