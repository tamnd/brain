---
title: "CF 898A - Rounding"
description: "We are given a single non-negative integer, and we are asked to transform it into a nearby number whose last digit is zero."
date: "2026-06-17T03:31:30+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 898
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 451 (Div. 2)"
rating: 800
weight: 898
solve_time_s: 63
verified: true
draft: false
---

[CF 898A - Rounding](https://codeforces.com/problemset/problem/898/A)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single non-negative integer, and we are asked to transform it into a nearby number whose last digit is zero. The rule is that Vasya wants to “round” the number so that it becomes divisible by 10, and among all such candidates he chooses the closest one in terms of absolute difference. If there are two equally close candidates, either result is acceptable.

In practice, every integer lies between two multiples of 10: one obtained by decreasing the last digit down to zero, and one obtained by increasing the number up to the next multiple of 10. The task is to decide which of these two is closer, or whether the number is already a multiple of 10.

The input constraint is extremely small in algorithmic terms: the number is at most 10^9. This means any constant-time arithmetic operation is sufficient, and even a linear scan would be overkill. The structure of the problem does not depend on complex data structures or iteration; it is purely about the last digit.

A naive mistake that often appears here is trying to “simulate rounding” digit by digit or iterating downward or upward until reaching a valid multiple of 10. That is unnecessary but still safe under constraints; the real risk is incorrect handling of tie cases.

For example, if n = 5, both 0 and 10 are valid answers because they are equally distant. A naive implementation that always floors (to 0) or always ceils (to 10) without checking distance might still pass, but a mixed or incorrect distance comparison could fail if implemented inconsistently.

Another edge case is when n already ends in 0, such as 4720. Any correct solution should return the number unchanged.

## Approaches

A brute-force interpretation would be: start from n and move downward until hitting a multiple of 10, and separately move upward until hitting a multiple of 10, then compare which is closer. Each step would decrement or increment by 1, so in the worst case (numbers ending in 1 or 9) this takes up to 9 steps per direction. This is still constant time, but the idea does not scale conceptually and obscures the real structure of the problem.

The key observation is that the last digit completely determines everything. The nearest lower multiple of 10 is obtained by subtracting the last digit, and the nearest higher multiple is obtained by adding (10 − last_digit), unless the digit is already 0.

So instead of simulating movement, we directly compute the two candidates:

one is n − (n mod 10), the other is n + (10 − n mod 10), and we compare their distances from n. The smaller distance wins, and in case of equality either can be printed.

This reduces the problem to a single modulo operation and a couple of arithmetic operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) amortized, conceptually iterative | O(1) | Accepted but unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer n from input. The entire decision depends only on its last digit.
2. Compute d = n mod 10. This isolates how far n is from the nearest lower multiple of 10.
3. If d equals 0, return n immediately. The number is already a valid target, so no adjustment is needed.
4. Compute the lower candidate as n − d. This is the closest multiple of 10 that does not exceed n.
5. Compute the upper candidate as n + (10 − d). This is the closest multiple of 10 strictly greater than n.
6. Compare distances from n to both candidates. If (n − lower) is less than or equal to (upper − n), choose the lower candidate; otherwise choose the upper candidate.

The decision is purely based on proximity, and ties are resolved arbitrarily in favor of the lower side, which is valid.

### Why it works

Every integer can be uniquely written as a multiple of 10 plus a remainder between 0 and 9. The two closest multiples of 10 are exactly the ones obtained by removing that remainder or completing it to 10. Any other multiple of 10 is at least 10 units away. Since both candidates are within at most 9 units, they are guaranteed to be the nearest possible choices. The algorithm therefore examines all possible optimal answers and selects one of them.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    
    d = n % 10
    
    if d == 0:
        print(n)
        return
    
    lower = n - d
    upper = n + (10 - d)
    
    if n - lower <= upper - n:
        print(lower)
    else:
        print(upper)

if __name__ == "__main__":
    solve()
```

The code first extracts the last digit using modulo arithmetic, which directly encodes the rounding structure of the problem. The early return handles the trivial case where no rounding is required. The two candidate values are then constructed explicitly, avoiding any iterative search. The comparison uses direct distance computation, ensuring correctness even in the tie case.

A subtle point is that the upper candidate is always well-defined even when d is 0, but we avoid computing it in that case for clarity and to preserve the identity behavior.

## Worked Examples

### Example 1: n = 5

We compute the last digit and the candidates step by step.

| Step | n | d = n mod 10 | Lower candidate | Upper candidate | Decision |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 5 | 0 | 10 | compare |

Distance to lower is 5, distance to upper is also 5, so either is valid. The algorithm selects the lower candidate, 0.

This demonstrates the tie-breaking behavior where both sides are equally valid.

### Example 2: n = 4722

| Step | n | d | Lower | Upper | Decision |
| --- | --- | --- | --- | --- | --- |
| 1 | 4722 | 2 | 4720 | 4730 | compare |

Distance to lower is 2, distance to upper is 8. The lower candidate is strictly closer, so the output is 4720.

This shows the asymmetry when the number is closer to the previous multiple of 10.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed regardless of input size |
| Space | O(1) | No auxiliary data structures are used |

The constraint n ≤ 10^9 ensures that integer arithmetic remains trivial and fits comfortably within standard 32-bit or 64-bit integer types, so the solution runs instantly.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    d = n % 10
    if d == 0:
        return str(n)
    lower = n - d
    upper = n + (10 - d)
    if n - lower <= upper - n:
        return str(lower)
    else:
        return str(upper)

# provided samples
assert run("5\n") in ["0", "10"]

# custom cases
assert run("0\n") == "0", "minimum edge"
assert run("10\n") == "10", "already multiple of 10"
assert run("1\n") == "0", "closer to lower boundary"
assert run("9\n") == "10", "closer to upper boundary"
assert run("4722\n") == "4720", "typical middle case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 | 0 | smallest valid input |
| 10 | 10 | already rounded number |
| 1 | 0 | lower-bound preference |
| 9 | 10 | upper-bound correctness |
| 4722 | 4720 | general interior case |

## Edge Cases

For n = 0, the remainder is 0, so the algorithm immediately returns 0. No candidate construction is needed, and the identity case is handled directly.

For n = 10, d = 0 as well, so the same early exit triggers and returns 10, preserving correctness for already-rounded values.

For n = 1, d = 1, so lower = 0 and upper = 10. The algorithm compares distances 1 and 9 and correctly selects 0.

For n = 9, d = 9, so lower = 0 and upper = 10. The distances are again 9 and 1, so the algorithm correctly selects 10.

For n = 5, both candidates are equally distant, and the algorithm consistently chooses the lower value 0 due to the `<=` condition, which is acceptable under the problem’s tie rule.
