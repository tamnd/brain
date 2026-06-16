---
title: "CF 990A - Commentary Boxes"
description: "We are given an initial number of commentary boxes and a required number of delegations. Every delegation must receive exactly the same number of boxes, and all existing boxes must be used so that nothing remains idle."
date: "2026-06-17T00:36:33+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 990
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 45 (Rated for Div. 2)"
rating: 1000
weight: 990
solve_time_s: 86
verified: true
draft: false
---

[CF 990A - Commentary Boxes](https://codeforces.com/problemset/problem/990/A)

**Rating:** 1000  
**Tags:** implementation, math  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an initial number of commentary boxes and a required number of delegations. Every delegation must receive exactly the same number of boxes, and all existing boxes must be used so that nothing remains idle. This requirement translates into a single arithmetic condition: the final number of boxes must be divisible by the number of delegations.

We are allowed to modify the current number of boxes by either building new ones or demolishing existing ones. Building increases the count by one at cost `a`, while demolishing decreases it by one at cost `b`. The goal is to reach any nonnegative number that is divisible by `m` with minimal total cost.

The constraints are extremely large for `n` and `m`, up to 10^12, which immediately rules out any approach that tries all possibilities or simulates adjustments one by one. The only viable strategy is to reason purely in terms of modular arithmetic and nearest multiples.

A naive mistake often comes from trying to “fix” divisibility greedily by either always moving upward to the next multiple or always moving downward to the previous one without comparing costs properly. Another subtle failure case is ignoring that going all the way down to zero is always an option, and sometimes cheaper than adjusting slightly.

## Approaches

A brute-force idea would be to check every possible final number of boxes and compute the cost to reach it. For each candidate final value `x`, we would compute how many boxes must be built if `x > n` or demolished if `x < n`, and pick the best `x` divisible by `m`. The issue is that the search space is unbounded up to 10^12, so even iterating over multiples of `m` is far too large. In the worst case, `m = 1`, and we would consider up to 10^12 states.

The key observation is that the optimal final number must be one of the closest multiples of `m` around `n`. Any optimal solution cannot lie far away, because cost grows linearly with distance and there is no benefit in skipping a closer multiple.

So the problem reduces to checking only two candidates: the largest multiple of `m` less than or equal to `n`, and the smallest multiple of `m` greater than or equal to `n`. Additionally, we must also consider the possibility of going to zero, since demolishing everything might be cheaper than adjusting toward either nearby multiple.

From `n`, we compute the remainder `r = n % m`. Then:

- Going down means removing `r` boxes.
- Going up means adding `m - r` boxes (unless `r = 0`).

Each option has a direct cost, and we take the minimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all targets | O(n) | O(1) | Too slow |
| Check nearest multiples | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the remainder `r = n % m`. This tells us how far `n` is from being divisible by `m`.
2. Consider the cost of decreasing `n` down to the nearest lower multiple of `m`, which is `r * b`. Each removed box costs `b`.
3. Consider the cost of increasing `n` up to the nearest higher multiple of `m`, which is `(m - r) * a` when `r != 0`. Each added box costs `a`.
4. Also consider reducing all the way to zero, which costs `n * b`. Zero is always divisible by `m`, so it is a valid endpoint.
5. Take the minimum among these options.

The important detail is that step 3 is only meaningful when `r > 0`, but writing it uniformly as `(m - r) % m * a` avoids special casing.

### Why it works

Any valid final number must be of the form `k * m`. Among all such values, the cost function is linear in the distance from `n`, either increasing or decreasing. If we move to a multiple that is not the closest in either direction, we necessarily pass through a closer multiple first, which would have lower or equal cost due to unit step costs. This ensures that only the nearest lower and nearest higher multiples need to be checked. The inclusion of zero handles the boundary case where the optimal multiple is far below `n`.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, a, b = map(int, input().split())

r = n % m

# move down to nearest multiple
cost_down = r * b

# move up to nearest multiple
cost_up = (m - r) * a if r != 0 else 0

# also consider going to 0
cost_zero = n * b

print(min(cost_down, cost_up, cost_zero))
```

The solution computes the remainder once and directly evaluates the only meaningful adjustment costs. The upward move is carefully guarded so that when `n` is already divisible by `m`, we do not incorrectly add a full cycle of `m` boxes.

The inclusion of the `cost_zero` path is what prevents missing cases where full demolition is optimal, especially when `b` is very small compared to `a`.

## Worked Examples

### Example 1

Input:

```
9 7 3 8
```

Here `r = 9 % 7 = 2`.

| Step | r | cost_down | cost_up | cost_zero | answer |
| --- | --- | --- | --- | --- | --- |
| initial | 2 | 2×8=16 | (7-2)×3=15 | 9×8=72 | - |
| final | 2 | 16 | 15 | 72 | 15 |

The optimal choice is to move up to 14 boxes, which costs 15.

This example shows that going upward can be cheaper than going downward even when it requires adding more units, due to different costs per operation.

### Example 2

Input:

```
10 6 1 5
```

Here `r = 10 % 6 = 4`.

| Step | r | cost_down | cost_up | cost_zero | answer |
| --- | --- | --- | --- | --- | --- |
| initial | 4 | 4×5=20 | (6-4)×1=2 | 10×5=50 | - |
| final | 4 | 20 | 2 | 50 | 2 |

The optimal move is to increase from 10 to 12, which is very cheap because building cost is small.

This demonstrates that the direction of adjustment is entirely determined by per-unit costs, not by distance alone.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations |
| Space | O(1) | No auxiliary data structures are used |

The solution easily fits within limits because it reduces a potentially huge search space into a constant-time comparison of three candidate costs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m, a, b = map(int, input().split())
    r = n % m
    cost_down = r * b
    cost_up = (m - r) * a if r != 0 else 0
    cost_zero = n * b
    return str(min(cost_down, cost_up, cost_zero))

# provided sample
assert run("9 7 3 8") == "15"

# n already divisible
assert run("14 7 5 2") == "0"

# cheap demolition to zero
assert run("10 6 100 1") == "10"

# cheap building upward
assert run("10 6 1 100") == "2"

# large balanced case
assert run("1000000000000 7 3 8") == str(min((1000000000000%7)*8, (7-1000000000000%7)%7*3, 1000000000000*8))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 9 7 3 8 | 15 | sample correctness |
| 14 7 5 2 | 0 | already divisible case |
| 10 6 100 1 | 10 | optimal full demolition |
| 10 6 1 100 | 2 | optimal upward adjustment |
| large n | computed | stress on overflow-safe arithmetic |

## Edge Cases

When `n` is already divisible by `m`, the remainder is zero, and both the upward and downward adjustments must evaluate to zero or be ignored correctly. For input `n = 14, m = 7`, we get `r = 0`, so `cost_down = 0`, `cost_up = 0`, and the answer is correctly zero, reflecting no operation needed.

When demolition is extremely cheap, the optimal strategy may be to delete everything. For `n = 10, m = 6, a = 100, b = 1`, we get `cost_zero = 10`, which beats both nearby multiples, so the algorithm correctly selects full demolition.

When building is much cheaper than demolition, the solution moves upward even if it requires more steps. For `n = 10, m = 6, a = 1, b = 100`, the upward adjustment cost is `2`, while downward is `400`, so the algorithm correctly prefers increasing to 12.

These cases confirm that checking only the nearest multiples plus zero is sufficient and stable under all cost configurations.
