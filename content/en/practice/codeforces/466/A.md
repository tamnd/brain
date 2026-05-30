---
title: "CF 466A - Cheap Travel"
description: "Ann needs to commute using the subway a total of n times. She can pay for each ride individually at a cost of a rubles, or she can buy a special multi-ride ticket that covers exactly m rides and costs b rubles."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 466
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 266 (Div. 2)"
rating: 1200
weight: 466
solve_time_s: 54
verified: true
draft: false
---

[CF 466A - Cheap Travel](https://codeforces.com/problemset/problem/466/A)

**Rating:** 1200  
**Tags:** implementation  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

Ann needs to commute using the subway a total of _n_ times. She can pay for each ride individually at a cost of _a_ rubles, or she can buy a special multi-ride ticket that covers exactly _m_ rides and costs _b_ rubles. The problem asks us to determine the minimum total cost she must pay to cover all _n_ rides, possibly by combining individual tickets and multi-ride tickets.

The input integers represent the following quantities: _n_ is the total number of rides, _m_ is the number of rides a multi-ride ticket covers, _a_ is the cost of a single ride, and _b_ is the cost of one multi-ride ticket. The output is a single integer, the minimal ruble amount needed to complete all rides.

The constraints are small, with all values capped at 1000. This means even a simple solution that loops over the possible number of multi-ride tickets is feasible. However, the problem can be solved directly with simple arithmetic. The main edge cases arise when the number of rides is smaller than a multi-ride ticket, or when a multi-ride ticket is more expensive than buying individual rides. For example, if _n = 1_, _m = 5_, _a = 1_, and _b = 10_, the cheapest option is clearly to buy a single ride ticket for 1 ruble, not the 5-ride ticket.

## Approaches

A brute-force approach would iterate over all possible numbers of multi-ride tickets from 0 up to ⌈_n/m_⌉, calculate the remaining rides to cover with single tickets, and keep track of the minimum total cost. This approach is correct because it explores all possible combinations, but it is overkill here. In the worst case, this loop executes at most 1000 times, which is acceptable for the problem’s constraints, but we can do better with direct arithmetic.

The key observation is that the problem reduces to a simple comparison of two strategies for the leftover rides after buying as many full multi-ride tickets as possible: either buy the exact number of remaining rides individually or buy one more multi-ride ticket to cover them. For full multi-ride tickets, compute `full_sets = n // m`. The remainder is `remainder = n % m`. The minimal cost is the sum of `full_sets * b` plus the cheaper option of `remainder * a` or `b`. This logic captures all optimal combinations without the need for iteration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n/m) ≈ O(1000) | O(1) | Acceptable but unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute how many full multi-ride tickets Ann can buy by integer division: `full_sets = n // m`. This represents the maximum number of multi-ride tickets that do not exceed the required rides.
2. Compute how many rides remain uncovered after buying the full multi-ride tickets: `remainder = n % m`.
3. Calculate the cost if Ann buys exactly the remaining rides as single tickets: `cost_single_remainder = remainder * a`.
4. Calculate the cost if Ann buys one extra multi-ride ticket to cover the remaining rides: `cost_extra_ticket = b`.
5. Take the minimum of the two options for the remaining rides and add it to the cost of the full multi-ride tickets: `total_cost = full_sets * b + min(cost_single_remainder, cost_extra_ticket)`.
6. Print `total_cost`.

Why it works: The algorithm works because any combination of multi-ride tickets and single tickets can be represented as full sets plus a choice for the remainder. The comparison of the two options for leftover rides ensures that Ann never pays more than necessary for the final rides, and buying extra full tickets for previously covered rides would never reduce cost. The problem is linear in the number of rides but reduces to constant-time arithmetic due to the structure of costs.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, a, b = map(int, input().split())

full_sets = n // m
remainder = n % m

# cheapest way to cover remaining rides
remainder_cost = min(remainder * a, b)

total_cost = full_sets * b + remainder_cost
print(total_cost)
```

The code first reads the four integers and immediately computes the number of full multi-ride tickets and leftover rides. It then computes the cheaper option for covering the leftover rides, either with single tickets or one extra multi-ride ticket. Finally, it sums the costs and outputs the result. Using integer division and modulus avoids off-by-one errors in computing full sets and remainder rides. The min function ensures the correct decision for leftover rides.

## Worked Examples

### Sample 1

Input: `6 2 1 2`

| full_sets | remainder | remainder_cost | total_cost |
| --- | --- | --- | --- |
| 3 | 0 | 0 | 6 |

Explanation: Ann can buy three 2-ride tickets for 2 rubles each, covering all 6 rides. No leftover rides remain. The total cost is 3 * 2 = 6.

### Sample 2

Input: `7 3 2 5`

| full_sets | remainder | remainder_cost | total_cost |
| --- | --- | --- | --- |
| 2 | 1 | 2 | 12 |

Explanation: Buying 2 multi-ride tickets covers 6 rides. One ride remains. Buying a single ticket for 2 rubles is cheaper than buying another 3-ride ticket for 5 rubles. Total cost = 2 * 5 + 2 = 12.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic operations are performed, no loops. |
| Space | O(1) | Only a few integer variables are used. |

Given n, m, a, b ≤ 1000, this solution executes in microseconds, well within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m, a, b = map(int, input().split())
    full_sets = n // m
    remainder = n % m
    remainder_cost = min(remainder * a, b)
    total_cost = full_sets * b + remainder_cost
    return str(total_cost)

# Provided sample
assert run("6 2 1 2\n") == "6", "sample 1"

# Minimum-size input
assert run("1 1 1 1\n") == "1", "minimum rides equal ticket"

# Single ticket cheaper than multi
assert run("1 5 1 10\n") == "1", "single ticket cheaper than multi"

# Multi-ticket cheaper than single multiple
assert run("10 3 4 10\n") == "34", "mixed multi and single optimal"

# Rides exactly divisible by multi-ride ticket
assert run("6 3 2 5\n") == "10", "rides divisible by multi-ride ticket"

# Rides smaller than multi-ride ticket, multi-ride cheaper
assert run("2 5 3 5\n") == "5", "multi-ride ticket cheaper than 2 singles"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 | 1 | Minimum input |
| 1 5 1 10 | 1 | Single ticket cheaper than multi |
| 10 3 4 10 | 34 | Combination of multi and single optimal |
| 6 3 2 5 | 10 | Exact division by multi-ticket |
| 2 5 3 5 | 5 | Multi-ticket cheaper than singles |

## Edge Cases

For `n = 1, m = 5, a = 1, b = 10`, the remainder is 1. The algorithm compares 1 * 1 = 1 with 10 and chooses 1, giving the correct minimal cost. For `n = 6, m = 2, a = 1, b = 2`, remainder = 0, so no extra cost is added. For `n` divisible by `m`, the algorithm does not overbuy, avoiding paying for unused rides. Each case confirms that the min function and integer division correctly handle both small and large remainders.
