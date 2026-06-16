---
title: "CF 996A - Hit the Lottery"
description: "We are given a single integer representing the total amount of money Allen wants to withdraw. The bank only dispenses cash using fixed denominations: 1, 5, 10, 20, and 100."
date: "2026-06-17T00:01:29+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 996
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 492 (Div. 2) [Thanks, uDebug!]"
rating: 800
weight: 996
solve_time_s: 82
verified: true
draft: false
---

[CF 996A - Hit the Lottery](https://codeforces.com/problemset/problem/996/A)

**Rating:** 800  
**Tags:** dp, greedy  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer representing the total amount of money Allen wants to withdraw. The bank only dispenses cash using fixed denominations: 1, 5, 10, 20, and 100. The task is to represent the given amount exactly using these bill values while minimizing the total number of bills used.

This is not a partition problem with arbitrary coins. The set of denominations is fixed and small, and we are asked for the smallest count of pieces that sum to a target value. Each denomination can be used unlimited times.

The input constraint allows the amount to be as large as one billion. That immediately rules out any dynamic programming over the value range, since even a linear DP in terms of n would require up to 10^9 states, which is infeasible. Any valid solution must work in constant time.

A naive attempt might try to explore combinations of bills, for example trying all ways to pick counts of each denomination. Even if we only consider counts of five types of bills, a brute force enumeration over possible counts of 100s, 20s, 10s, 5s, and 1s quickly becomes unbounded because the number of 1-dollar bills can vary up to 10^9. Even restricting combinations still leads to an impractical search space.

A subtle edge case arises when smaller denominations are used excessively before larger ones. For example, taking too many 20s when a 100 bill would reduce the total count leads to a non-optimal construction. A correct solution must avoid locally suboptimal choices.

## Approaches

A brute-force approach would try all possible combinations of bills whose total sum equals n, tracking the minimum number of bills among valid combinations. Conceptually, this is correct because it enumerates the entire solution space. However, the number of combinations grows with n itself, since the count of 1-dollar bills can vary independently up to n. Even if we discretize by denominations, the search space is proportional to n/1 choices in the worst dimension, leading to linear or worse exploration per state. This is far beyond the limits for n up to 10^9.

The key observation is that the denominations are structured in a canonical system: each larger bill is a multiple or near-multiple of smaller ones, and greedily taking the largest possible bill at each step never blocks an optimal solution. This is because 100, 20, 10, and 5 are aligned such that replacing one larger bill with smaller ones always increases the number of bills. For instance, one 20-dollar bill is always better than two 10-dollar bills, and one 10-dollar bill is always better than two 5-dollar bills, and so on.

This structure reduces the problem to repeatedly extracting the maximum number of high-value bills from the remaining amount, then moving to the next denomination. The process becomes a simple sequence of integer divisions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / O(n) | O(1) | Too slow |
| Optimal (Greedy) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We process denominations from largest to smallest, always extracting as many bills of the current denomination as possible.

### Steps

1. Start with the largest denomination, 100, and compute how many 100-dollar bills fit into the remaining amount using integer division. Subtract their total value from the amount.
2. Move to 20-dollar bills and repeat the same operation on the remainder. This step is correct because any leftover after removing 100s is strictly less than 100, so using 20s is locally optimal within that reduced range.
3. Repeat the same greedy extraction for 10-dollar bills.
4. Repeat again for 5-dollar bills.
5. Finally, whatever remains must be paid using 1-dollar bills, so the remainder itself is the count of 1-dollar bills.

### Why it works

The correctness comes from the fact that each denomination is the best possible way to represent its value in terms of smaller bills. Any attempt to replace a larger bill with smaller ones strictly increases or preserves the number of bills only when using identical replacements, but never improves the count. This creates a monotonic structure: once we take as many large bills as possible, no later combination of smaller bills can compensate to reduce the total number of bills used.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())

bills = [100, 20, 10, 5, 1]
ans = 0

for b in bills:
    ans += n // b
    n %= b

print(ans)
```

The solution iterates through the denominations in descending order and repeatedly extracts the maximum number of bills for each value. The variable `ans` accumulates the total number of bills used. Each step reduces `n` to the remaining amount that cannot be represented by higher denominations.

The order of processing is critical. If smaller denominations were processed first, larger bills might never be used even when they would reduce the total count.

Integer division and modulo operations are safe here because all values remain within Python’s integer range, and no precision issues occur.

## Worked Examples

### Example 1: n = 125

| Step | Denomination | Bills Taken | Remaining n | Total Bills |
| --- | --- | --- | --- | --- |
| 1 | 100 | 1 | 25 | 1 |
| 2 | 20 | 1 | 5 | 2 |
| 3 | 10 | 0 | 5 | 2 |
| 4 | 5 | 1 | 0 | 3 |
| 5 | 1 | 0 | 0 | 3 |

This trace shows how the greedy strategy naturally decomposes 125 into 100 + 20 + 5, producing the minimum of 3 bills.

### Example 2: n = 68

| Step | Denomination | Bills Taken | Remaining n | Total Bills |
| --- | --- | --- | --- | --- |
| 1 | 100 | 0 | 68 | 0 |
| 2 | 20 | 3 | 8 | 3 |
| 3 | 10 | 0 | 8 | 3 |
| 4 | 5 | 1 | 3 | 4 |
| 5 | 1 | 3 | 0 | 7 |

This demonstrates how leftover amounts after greedy extraction are always handled exactly by smaller denominations without any need for backtracking.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Fixed number of denominations, each processed once |
| Space | O(1) | Only a few integer variables are used |

The computation does not depend on n in terms of loop depth or recursion. Even for n up to 10^9, the algorithm performs a constant number of arithmetic operations, well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline().strip())
    bills = [100, 20, 10, 5, 1]
    ans = 0
    for b in bills:
        ans += n // b
        n %= b
    return str(ans)

# provided sample
assert run("125\n") == "3"

# minimum input
assert run("1\n") == "1"

# exact large denomination
assert run("100\n") == "1"

# multiple of 20
assert run("80\n") == "4"

# mixed case
assert run("68\n") == "7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | smallest boundary case |
| 100 | 1 | exact large denomination |
| 80 | 4 | multiple mid-denomination handling |
| 68 | 7 | mixed greedy decomposition |

## Edge Cases

A key edge case is when the amount is just below a large denomination, for example n = 99. The algorithm takes zero 100-dollar bills, then proceeds to 20-dollar bills, yielding four 20s (80), leaving 19, then one 10, one 5, and four 1s. The total is 4 + 1 + 1 + 4 = 10 bills. Any attempt to force a 100-dollar bill would be invalid, and any attempt to overuse smaller denominations earlier would only increase the count.

Another case is when n is exactly divisible by a large denomination such as 200. The algorithm immediately selects two 100-dollar bills and terminates with no remainder, confirming that greedy extraction produces a tight optimal representation with no need for smaller bills.
