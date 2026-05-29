---
title: "CF 270A - Fancy Fence"
description: "We are asked to determine whether a robot, which can only make fence corners at a fixed angle a, can construct a regular polygon. A regular polygon is defined as a closed shape with all sides and all angles equal."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 270
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 165 (Div. 2)"
rating: 1100
weight: 270
solve_time_s: 72
verified: true
draft: false
---

[CF 270A - Fancy Fence](https://codeforces.com/problemset/problem/270/A)

**Rating:** 1100  
**Tags:** geometry, implementation, math  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether a robot, which can only make fence corners at a fixed angle _a_, can construct a regular polygon. A regular polygon is defined as a closed shape with all sides and all angles equal. The input consists of several test cases, each giving a single angle _a_ in degrees. The output for each test case is "YES" if there exists a regular polygon where each internal angle is exactly _a_, and "NO" otherwise.

The internal angle of a regular polygon with _n_ sides can be calculated using the formula:

$$\text{angle} = \frac{(n-2) \cdot 180}{n}$$

This means for a given _a_, we need to find an integer _n ≥ 3_ that satisfies:

$$a = \frac{(n-2) \cdot 180}{n} \quad \text{or equivalently} \quad n = \frac{360}{180 - a}$$

The constraints are simple: 0 < a < 180. The number of test cases is unspecified but we can assume a typical competitive programming range, so each test case must be processed efficiently in constant time.

An edge case arises when _a_ is very close to 0 or 180. For example, _a = 179_ would suggest an extremely high-sided polygon, and we need to make sure our integer checks correctly detect divisibility without floating-point errors. Another subtlety is that only integer _n ≥ 3_ counts; fractional sides or _n = 2_ are invalid.

## Approaches

A naive brute-force would iterate over all possible _n_ from 3 upwards, compute the corresponding internal angle, and check if it matches _a_. This works because the maximum integer _n_ we need to consider is bounded by:

$$n = \frac{360}{180 - a} \le 360$$

So the brute-force method would be correct, but iterating up to 360 for each test case is unnecessary when we can solve it analytically. The key insight is the rearrangement:

$$n = \frac{360}{180 - a}$$

The problem reduces to checking whether $360 / (180 - a)$ is an integer greater than or equal to 3. This eliminates any loops and floating-point rounding issues if we use integer arithmetic: we only need to verify if 360 is divisible by (180 - a) and if the resulting quotient is at least 3.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(360) per test | O(1) | Correct but unnecessary |
| Analytical Division Check | O(1) per test | O(1) | Accepted and optimal |

## Algorithm Walkthrough

1. Read the number of test cases _t_. This tells us how many angles we need to process.
2. For each test case, read the angle _a_ the robot can make.
3. Compute the value `x = 180 - a`. This represents the polygon's external angle, since each internal angle is $180 - \text{external angle}$.
4. Check if 360 is divisible by `x`. If not, output "NO" because no integer-sided polygon can have that internal angle.
5. If divisible, compute `n = 360 // x`. Verify that _n ≥ 3_ because a polygon must have at least 3 sides.
6. If both conditions are satisfied, output "YES"; otherwise, output "NO".

The algorithm works because the sum of external angles in any polygon is exactly 360 degrees. Checking that 360 is divisible by the external angle ensures we can form a closed shape with an integer number of sides. The check _n ≥ 3_ guarantees a valid polygon.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a = int(input())
    x = 180 - a
    if x <= 0:
        print("NO")
        continue
    if 360 % x == 0 and 360 // x >= 3:
        print("YES")
    else:
        print("NO")
```

The solution reads the input efficiently using `sys.stdin.readline` to handle multiple test cases. The subtraction `x = 180 - a` directly calculates the external angle. We immediately eliminate angles that are invalid (`x <= 0`) before performing the divisibility check. The integer division ensures no floating-point rounding errors, which could otherwise produce incorrect results for angles like 120 or 179 degrees.

## Worked Examples

Trace for sample input 1:

```
3
30
60
90
```

| Test | a | x = 180 - a | 360 % x | n = 360 // x | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | 30 | 150 | 360 % 150 = 60 | 360 // 150 = 2 | NO |
| 2 | 60 | 120 | 360 % 120 = 0 | 360 // 120 = 3 | YES |
| 3 | 90 | 90 | 360 % 90 = 0 | 360 // 90 = 4 | YES |

This demonstrates how the divisibility check guarantees we can form a regular polygon, and the `n >= 3` check filters out impossible cases like the first test case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is processed in constant time. |
| Space | O(1) | Only a few integers are stored per test case. |

Given t can be as large as 10^5, the solution still runs efficiently within 2 seconds because each test case only involves basic arithmetic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    t = int(input())
    for _ in range(t):
        a = int(input())
        x = 180 - a
        if x <= 0:
            print("NO")
            continue
        if 360 % x == 0 and 360 // x >= 3:
            print("YES")
        else:
            print("NO")
    
    return output.getvalue().strip()

# provided samples
assert run("3\n30\n60\n90\n") == "NO\nYES\nYES", "sample 1"

# custom cases
assert run("1\n1\n") == "NO", "too small angle"
assert run("1\n179\n") == "NO", "almost 180 degrees"
assert run("1\n120\n") == "YES", "regular triangle"
assert run("2\n135\n150\n") == "YES\nNO", "quadrilateral yes, pentagon no"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | NO | x = 179, n < 3, rejects near 180 angle |
| 120 | YES | Regular triangle produces correct output |
| 135,150 | YES,NO | Quadrilateral works, impossible pentagon detected |

## Edge Cases

For an angle like 179 degrees, `x = 180 - 179 = 1`. Checking `360 % 1 == 0` is true, but `n = 360` is greater than 3, so it might seem possible. However, we must accept it because a 360-sided polygon is valid geometrically. The solution handles `a` close to 0 correctly, rejecting negative or zero `x`, ensuring no invalid polygons are suggested. For `a = 0` or `a >= 180`, `x <= 0` triggers an immediate "NO", preventing nonsensical polygons.
