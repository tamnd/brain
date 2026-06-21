---
title: "CF 105684A - \u0421\u043a\u043e\u0440\u043e \u043d\u043e\u0432\u044b\u0439 \u0433\u043e\u0434"
description: "We are given a fixed number of candies and a fixed number of employees. Each employee must receive either exactly 2 candies or exactly 3 candies. If an employee receives 3 candies, they are considered happy; otherwise, they receive 2 candies and are not happy."
date: "2026-06-22T05:01:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105684
codeforces_index: "A"
codeforces_contest_name: "\u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u041d\u0415\u0419\u041c\u0410\u0420\u041a 2024-25, \u0412\u0442\u043e\u0440\u043e\u0439 \u043e\u0442\u0431\u043e\u0440"
rating: 0
weight: 105684
solve_time_s: 50
verified: true
draft: false
---

[CF 105684A - \u0421\u043a\u043e\u0440\u043e \u043d\u043e\u0432\u044b\u0439 \u0433\u043e\u0434](https://codeforces.com/problemset/problem/105684/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed number of candies and a fixed number of employees. Each employee must receive either exactly 2 candies or exactly 3 candies. If an employee receives 3 candies, they are considered happy; otherwise, they receive 2 candies and are not happy. The task is to maximize the number of happy employees while distributing all candies so that every employee gets a valid bundle.

The input contains two large integers, the total number of candies and the number of employees. The constraints allow values up to $10^9$ for candies and up to $5 \cdot 10^8$ for employees, so any solution must run in constant or logarithmic time per test case. A linear scan over employees or candies would be acceptable only if there were multiple test cases with small bounds, but here the scale already suggests a direct arithmetic construction.

A subtle point is that the total number of candies is at least twice the number of employees. This guarantees that assigning 2 candies to everyone is always feasible, so we never face an infeasible situation where some employee cannot receive the minimum required amount. The problem is purely about upgrading some employees from 2 to 3 candies by redistributing surplus.

Edge cases come from parity and surplus structure.

If $n = 2m$, then every employee must receive exactly 2 candies. There is no room to promote anyone to 3 candies, so the answer is 0. For example, $n = 10, m = 5$, total distribution is forced, and no one can be happy.

If $n = 3m$, then every employee can receive 3 candies, so all are happy and the answer is $m$.

Between these extremes, we must carefully reason about how many 1-candy upgrades are possible without violating feasibility.

## Approaches

A brute-force approach would try to assign candies employee by employee, choosing either 2 or 3 candies for each, and checking all combinations. With $m$ employees, this leads to $2^m$ possible assignments, which is completely infeasible even for $m = 40$, let alone up to $5 \cdot 10^8$.

A more structured view is to start from a baseline where everyone receives 2 candies. This consumes $2m$ candies. The remaining $n - 2m$ candies represent extra units that can be used to upgrade some employees from 2 to 3 candies. Each such upgrade costs exactly 1 extra candy and increases the number of happy employees by one.

However, upgrading all remaining candies is not always directly equivalent to the answer because we must ensure that we do not exceed the number of employees. Even if there are many leftover candies, we cannot have more than $m$ happy employees. Thus the answer is limited by both the surplus and the number of employees.

This leads to a direct interpretation: each happy employee consumes exactly 3 candies, so if we choose $x$ happy employees and $m - x$ unhappy employees, total candies needed is

$$3x + 2(m - x) = 2m + x.$$

This must be at most $n$, so $x \le n - 2m$. Also $x \le m$. The maximum feasible $x$ is therefore the minimum of these two bounds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^m)$ | $O(m)$ | Too slow |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

### Optimal reasoning steps

1. Start by imagining that every employee receives the minimum possible allocation of 2 candies. This consumes exactly $2m$ candies, and this configuration is always valid due to the constraint $n \ge 2m$.
2. Compute the remaining number of candies after this baseline assignment. Let this be $r = n - 2m$. These are the only candies available for increasing happiness.
3. Observe that increasing an employee from 2 candies to 3 candies consumes exactly 1 additional candy and converts that employee into a happy one. So each happy employee corresponds to spending 1 unit from $r$.
4. Conclude that at most $r$ employees can be made happy using the surplus candies.
5. Also observe that the number of happy employees cannot exceed the total number of employees $m$, since each employee can be counted at most once.
6. Take the minimum of these two constraints, $r$ and $m$, as the final answer.

### Why it works

Every valid assignment can be transformed into the baseline assignment of all 2-candy employees by subtracting 1 candy from each happy employee. This shows a one-to-one correspondence between a solution with $x$ happy employees and a configuration where exactly $x$ surplus candies are distributed on top of the baseline. Since the baseline is fixed and consumes the minimum possible candies, any valid configuration must satisfy $x \le n - 2m$. No arrangement can bypass this bound because each happiness unit has a fixed cost of exactly one extra candy beyond the base requirement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    base = 2 * m
    surplus = n - base
    if surplus < 0:
        surplus = 0
    print(min(m, surplus))

if __name__ == "__main__":
    solve()
```

The implementation directly encodes the reasoning. The variable `base` represents the mandatory allocation where everyone gets 2 candies. The `surplus` variable captures how many additional 1-candy increments we can distribute. The final answer is bounded both by this surplus and by the number of employees. The guard against negative surplus is technically unnecessary under the constraints, but it preserves correctness if the constraint is relaxed or misread.

## Worked Examples

### Example 1

Input:

```
10 4
```

We compute:

| Step | Base (2m) | Surplus (n - 2m) | Answer |
| --- | --- | --- | --- |
| Start | 8 | - | - |
| Compute | 8 | 2 | - |
| Final | 8 | 2 | 2 |

This means we can upgrade at most 2 employees to receive 3 candies, while the remaining 2 receive 2 candies.

This matches the structure: two employees take 3 candies (6 total), and two take 2 candies (4 total), summing to 10.

### Example 2

Input:

```
10 5
```

| Step | Base (2m) | Surplus (n - 2m) | Answer |
| --- | --- | --- | --- |
| Start | 10 | - | - |
| Compute | 10 | 0 | - |
| Final | 10 | 0 | 0 |

No extra candies remain after giving everyone 2 candies, so no one can be upgraded.

This demonstrates the tight boundary case where the baseline exactly matches the total resources.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a constant number of arithmetic operations are performed |
| Space | $O(1)$ | No additional data structures are used |

The solution easily fits within the constraints since it performs no iteration over $m$ or $n$, which could be extremely large.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    base = 2 * m
    surplus = n - base
    if surplus < 0:
        surplus = 0
    return str(min(m, surplus))

# provided samples
assert run("10 4\n") == "2"
assert run("10 5\n") == "0"

# minimum edge (smallest valid m)
assert run("4 2\n") == "0"

# exact all-happy case
assert run("6 2\n") == "2"

# large surplus
assert run("100 10\n") == "10"

# tight base equality
assert run("20 10\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 2 | 0 | minimal feasible case, no surplus |
| 6 2 | 2 | full happiness possible |
| 100 10 | 10 | surplus exceeds m, cap applies |
| 20 10 | 0 | exact base saturation case |

## Edge Cases

For the case where $n = 2m$, every employee receives exactly 2 candies and no upgrades are possible. For example, input `10 5` produces base $2m = 10$ and surplus 0. The algorithm sets `surplus = 0` and returns `min(5, 0) = 0`, correctly matching the forced distribution.

When $n$ is large enough to support all employees receiving 3 candies, such as `6 2`, the computation yields base 4 and surplus 2. The result is `min(2, 2) = 2`, meaning all employees can be made happy. The algorithm naturally saturates at $m$, preventing overcounting even when surplus is large.
