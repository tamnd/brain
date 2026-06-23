---
title: "CF 105498B - The Fortune Dice"
description: "We are given a single integer that represents a desired total score from rolling a standard six-sided die twice. Each roll produces a value between 1 and 6 inclusive, and the final outcome is the sum of the two results."
date: "2026-06-24T00:12:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105498
codeforces_index: "B"
codeforces_contest_name: "Khulna Regional Inter University Programming Contest (KRIUPC) MIRROR"
rating: 0
weight: 105498
solve_time_s: 74
verified: true
draft: false
---

[CF 105498B - The Fortune Dice](https://codeforces.com/problemset/problem/105498/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer that represents a desired total score from rolling a standard six-sided die twice. Each roll produces a value between 1 and 6 inclusive, and the final outcome is the sum of the two results. The task is to decide whether there exists any way to obtain the given target sum using two such rolls.

Although the input size is extremely small, the structure of the problem is a classic bounded-sum feasibility question. Each variable has a fixed domain, so the entire state space is finite and tiny. This immediately implies that any solution that enumerates all outcomes is already more than fast enough, and even a direct mathematical characterization of the possible sums is sufficient.

A common mistake comes from misreading the allowed range of sums. Since each die shows at least 1 and at most 6, the smallest possible sum is 2 and the largest is 12. Any value outside this range is impossible regardless of how the dice are rolled.

Two concrete edge situations expose typical reasoning errors. If the target is 1, a naive assumption that “any small number might be reachable” fails because the minimum sum is already 2, so the correct answer is No. If the target is 12, some might incorrectly assume it is rare or special, but it is actually achievable with (6, 6), so the correct answer is Yes.

## Approaches

A direct brute-force method considers every possible ordered pair of dice outcomes. There are 6 choices for the first roll and 6 for the second, producing 36 total combinations. For each pair, we compute the sum and compare it to the target value. This approach is correct because it checks the entire sample space without omission. Its cost is constant with respect to input size, since the number of outcomes never changes.

Even though brute force is already efficient enough here, we can simplify further by observing that we do not need to enumerate outcomes at all. The sum of two bounded integers depends only on their extreme values. The smallest achievable sum is 1 + 1 and the largest is 6 + 6. Every integer in between is achievable because the sum distribution of two dice is contiguous across that interval. This reduces the problem to a simple interval check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(36) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer x representing the target sum. This is the value we want to verify against the reachable range of dice sums.
2. Determine the minimum and maximum possible sums from two dice. The minimum comes from both dice showing 1, and the maximum comes from both showing 6.
3. Check whether x lies within this closed interval from 2 to 12. If it does, a valid pair of dice outcomes must exist that produces it.
4. If x is inside the interval, output "Yes". Otherwise output "No".

### Why it works

Every valid outcome corresponds to a pair (a, b) where both values are restricted to a fixed integer interval. The set of all possible sums is exactly the image of this Cartesian product under addition. Because both domains are continuous integer ranges, the resulting sum set has no gaps between its minimum and maximum values. Therefore membership in the reachable set is equivalent to a simple boundary check.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x = int(input().strip())
    if 2 <= x <= 12:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()
```

The solution reads the input once and directly compares it against the precomputed feasibility interval. There are no loops or additional data structures. The boundary conditions are the key detail: both endpoints 2 and 12 are included because they correspond to valid dice configurations (1,1) and (6,6).

## Worked Examples

Consider x = 7. The valid range is [2, 12], so 7 lies inside it.

| Step | x | Condition | Decision |
| --- | --- | --- | --- |
| Input | 7 | - | Read value |
| Check lower bound | 7 ≥ 2 | True | Continue |
| Check upper bound | 7 ≤ 12 | True | Valid |

This confirms that intermediate sums are always achievable.

Now consider x = 1.

| Step | x | Condition | Decision |
| --- | --- | --- | --- |
| Input | 1 | - | Read value |
| Check lower bound | 1 ≥ 2 | False | Reject |

This shows how values below the minimum bound are immediately eliminated.

The first example confirms that internal values work, while the second demonstrates that the lower boundary is strict.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a single comparison against fixed bounds |
| Space | O(1) | No auxiliary data structures are used |

The constant-time nature of the solution is far below the limits of any competitive programming environment. The input size is irrelevant because the computation does not scale with it.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import sys as _sys
    out = io.StringIO()
    def solve():
        x = int(input().strip())
        print("Yes" if 2 <= x <= 12 else "No")
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples (conceptual since statement has no explicit sample)
assert run("7\n") == "Yes", "typical achievable sum"
assert run("1\n") == "No", "below minimum impossible"
assert run("12\n") == "Yes", "maximum achievable sum"

# custom cases
assert run("2\n") == "Yes", "minimum boundary"
assert run("13\n") == "No", "just above maximum"
assert run("6\n") == "Yes", "middle value"
assert run("20\n") == "No", "far outside range"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | Yes | Lower boundary case |
| 13 | No | Just above valid range |
| 6 | Yes | Typical internal value |
| 20 | No | Extreme invalid input |

## Edge Cases

For the lower bound case, consider input x = 2. The algorithm checks 2 ≤ x ≤ 12, which holds true. This corresponds exactly to the dice outcome (1,1), confirming correctness at the boundary.

For the upper bound case, consider x = 12. The check also passes, and this corresponds to (6,6). Even though it is a single configuration, it still lies within the reachable set, so the algorithm correctly accepts it.

For a value below range such as x = 1, the lower bound check fails immediately because 1 < 2. This reflects the impossibility of obtaining a sum smaller than two independent positive integers each at least one.
