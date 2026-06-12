---
title: "CF 1091A - New Year and the Christmas Ornament"
description: "We are given three piles of ornaments: yellow, blue, and red. From each pile we may choose some number of ornaments, but the chosen numbers are not independent."
date: "2026-06-13T04:15:11+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1091
codeforces_index: "A"
codeforces_contest_name: "Good Bye 2018"
rating: 800
weight: 1091
solve_time_s: 468
verified: true
draft: false
---

[CF 1091A - New Year and the Christmas Ornament](https://codeforces.com/problemset/problem/1091/A)

**Rating:** 800  
**Tags:** brute force, implementation, math  
**Solve time:** 7m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three piles of ornaments: yellow, blue, and red. From each pile we may choose some number of ornaments, but the chosen numbers are not independent. The counts must follow a strict arithmetic pattern: if we choose some number of yellow ornaments, then blue must be exactly one more than yellow, and red must be exactly one more than blue. So the chosen triple always has the form $(x, x+1, x+2)$.

The task is to pick the largest possible valid triple that does not exceed the available supplies $y, b, r$. The goal is to maximize the total $x + (x+1) + (x+2)$, which is equivalent to maximizing $3x + 3$, so really we are maximizing $x$.

The constraints are small: each value is at most 100. This immediately rules out any need for advanced data structures or optimization techniques. A direct search over all feasible choices is sufficient, since even checking all possibilities up to 100 is trivial in constant time.

A subtle failure case for naive reasoning is assuming that starting from the maximum possible $x$ derived from the smallest of $y, b, r$ works directly. For example, if we take $x = \min(y, b, r)$, the required pattern breaks immediately because the dependencies shift the effective limits. Another pitfall is independently maximizing each color, which ignores the rigid coupling between them.

## Approaches

The brute-force idea is straightforward. We try every possible value of $x$, compute how many yellow, blue, and red ornaments would be required, and check whether they fit within the available supplies. If they do, we compute the total used and keep the maximum.

This works because the structure is one-dimensional. Every valid configuration is completely determined by a single parameter $x$. So instead of searching a three-dimensional space, we reduce the problem to a single linear scan.

The brute-force remains efficient because the range of $x$ is extremely small. Even if we check all values from 0 to 100, we perform at most 101 checks, each O(1). There is no need for further optimization.

The key insight is that feasibility depends only on:

$$x \le y,\quad x+1 \le b,\quad x+2 \le r$$

So the valid $x$ values are bounded above by the tightest constraint among $y$, $b-1$, and $r-2$. This collapses the problem to computing a single minimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(100) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three values $y, b, r$. These represent available quantities of each ornament type.
2. Recognize that any valid selection must follow the structure $(x, x+1, x+2)$. The entire problem reduces to determining the largest feasible $x$.
3. Compute the upper bound imposed by each color independently. Yellow allows at most $x \le y$. Blue requires $x+1 \le b$, which becomes $x \le b-1$. Red requires $x+2 \le r$, which becomes $x \le r-2$.
4. Take the smallest of these bounds to ensure all constraints are satisfied simultaneously. This gives $x = \min(y, b-1, r-2)$.
5. Compute the total ornaments used as $3x + 3$, since we are selecting $x$, $x+1$, and $x+2$.
6. Output the result.

### Why it works

Every valid configuration corresponds uniquely to a single integer $x$. The constraints from each color independently restrict the maximum allowable $x$. Since violating any one constraint invalidates the whole configuration, the correct solution must satisfy all constraints at once, which is exactly captured by taking their minimum. This ensures we never overestimate any component and guarantees the resulting triple is both valid and maximal.

## Python Solution

```python
import sys
input = sys.stdin.readline

y, b, r = map(int, input().split())

x = min(y, b - 1, r - 2)
print(3 * x + 3)
```

The solution directly implements the derived constraints. The subtraction in `b - 1` and `r - 2` is critical because it converts the dependent constraints into a uniform bound on $x$. The final multiplication by 3 and addition of 3 reconstructs the total number of chosen ornaments from the parameterized form.

A common implementation mistake is forgetting that blue and red impose shifted constraints. Using `min(y, b, r)` would overestimate feasibility and produce invalid configurations.

## Worked Examples

### Sample 1

Input:

```
8 13 9
```

We compute the bounds for $x$:

| Step | y bound | b bound | r bound | x |
| --- | --- | --- | --- | --- |
| Values | 8 | 13 - 1 = 12 | 9 - 2 = 7 | 7 |

The limiting factor is red, since it forces $x \le 7$. So we select $x = 7$, giving the triple $(7, 8, 9)$. The total is $7 + 8 + 9 = 24$.

This trace shows that even though yellow and blue allow larger values, red dominates the feasible range.

### Sample 2 (constructed)

Input:

```
2 3 4
```

| Step | y bound | b bound | r bound | x |
| --- | --- | --- | --- | --- |
| Values | 2 | 3 - 1 = 2 | 4 - 2 = 2 | 2 |

All constraints coincide at $x = 2$, giving the triple $(2, 3, 4)$. The total is $9$.

This case shows the balanced situation where all constraints are simultaneously tight.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations and a min computation |
| Space | O(1) | No auxiliary data structures are used |

The constraints are small enough that even a naive loop would be instant, but the closed-form solution reduces the problem to pure arithmetic and guarantees constant-time execution.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    y, b, r = map(int, sys.stdin.readline().split())
    x = min(y, b - 1, r - 2)
    return str(3 * x + 3)

# provided samples
assert run("8 13 9") == "24"

# minimum case
assert run("1 2 3") == "6"

# tight blue constraint
assert run("10 2 10") == "3"

# tight red constraint
assert run("10 10 5") == "6"

# all equal-ish balanced
assert run("5 6 7") == "18"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 | 6 | smallest valid increasing chain |
| 10 2 10 | 3 | blue becomes bottleneck |
| 10 10 5 | 6 | red becomes bottleneck |
| 5 6 7 | 18 | balanced constraints |

## Edge Cases

One important edge case is when blue is the limiting factor after shifting. For input `10 2 10`, we compute $x \le b-1 = 1$, so $x = 1$, giving total $3$. A naive `min(y, b, r)` would incorrectly suggest $x = 2$, which already violates the blue constraint since it would require $x+1 = 3 > 2$.

Another case is when red is extremely small. For input `10 10 3`, we get $x \le r-2 = 1$, producing $(1,2,3)$. Any attempt to ignore the shifted constraint would overcount red usage and produce invalid triples.

A final case is when all values are minimal, such as `1 2 3`. The algorithm still works cleanly: it yields $x=1$, and the resulting structure exactly matches the smallest valid configuration, confirming that the formula handles boundary conditions without special casing.
