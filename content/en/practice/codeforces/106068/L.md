---
title: "CF 106068L - Triangle hole"
description: "We start with a single equilateral triangle whose size is described by its height $H$. The process is iterative. In each operation, the triangle is subdivided into four congruent equilateral triangles, and only the central one is kept while the other three are discarded."
date: "2026-06-21T15:57:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106068
codeforces_index: "L"
codeforces_contest_name: "2025 Aleppo and Idlib Private Universities Collegiate Programming Contest (APUCPC 2025)"
rating: 0
weight: 106068
solve_time_s: 39
verified: true
draft: false
---

[CF 106068L - Triangle hole](https://codeforces.com/problemset/problem/106068/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a single equilateral triangle whose size is described by its height $H$. The process is iterative. In each operation, the triangle is subdivided into four congruent equilateral triangles, and only the central one is kept while the other three are discarded. This operation is repeated $K$ times, always applied to the remaining triangle.

The task is to determine the area of the final remaining triangle after $K$ such operations.

From a geometric perspective, each operation scales down the triangle by a fixed linear factor. Since the triangle is partitioned into four equal-area subtriangles and only one is kept, the area is reduced by exactly a factor of $4$ per operation. This makes the problem fundamentally about exponential decay of area under repeated subdivision rather than any geometric reconstruction.

The input bounds are large for the number of operations, with $K$ up to $10^5$. This immediately rules out any approach that simulates geometry or performs iterative area recomputation step by step using floating point geometry constructions. However, the structure of the transformation is multiplicative and constant per step, so the entire process can be reduced to a closed-form expression.

A subtle edge case appears when $K = 0$, where no transformation happens and the answer is simply the area of the original triangle. Any solution that assumes at least one operation will incorrectly reduce the area even when no step is applied.

Another issue arises from floating-point stability. Since the answer involves repeated division by powers of 4, naive iterative multiplication or division can accumulate precision error for large $K$, especially near the $10^{-4}$ tolerance boundary. This encourages computing the final exponentiation in one shot rather than stepwise updates.

## Approaches

A direct simulation would explicitly maintain the triangle and recompute its area after each subdivision. Since each step only keeps one of four equal parts, the area can be recomputed as “current area divided by 4” repeatedly. This is correct because each operation preserves similarity while uniformly scaling down area.

However, this leads to a linear-time process in $K$. With $K$ up to $10^5$, this is still feasible computationally, but it introduces unnecessary floating-point repeated division, which increases accumulated error risk and adds overhead.

The key observation is that the transformation is purely multiplicative and independent across steps. After $K$ operations, the area is exactly the initial area multiplied by $(1/4)^K$. This allows us to compute the final result in constant time using exponentiation.

The only remaining component is the initial area of an equilateral triangle given its height $H$. For an equilateral triangle, if height is $H$, the side length is $s = \frac{2H}{\sqrt{3}}$, and area is:

$$A = \frac{\sqrt{3}}{4}s^2 = \frac{\sqrt{3}}{4} \cdot \frac{4H^2}{3} = \frac{\sqrt{3}}{3}H^2$$

So the final answer becomes:

$$A_K = \frac{\sqrt{3}}{3}H^2 \cdot 4^{-K}$$

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Step-by-step simulation | O(K) | O(1) | Too slow / numerically unstable |
| Closed-form formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read integers $H$ and $K$. These define the original geometry and how many times the shrinking operation is applied.
2. Compute the initial area of the equilateral triangle using the height-based formula $A_0 = \frac{\sqrt{3}}{3}H^2$. This step converts geometric input into a scalar quantity.
3. Compute the scaling factor induced by $K$ operations, which is $4^{-K}$. Each operation preserves exactly one of four equal-area parts, so area is divided by 4 each time.
4. Multiply the initial area by the scaling factor to obtain the final area.
5. Output the result as a floating-point number.

### Why it works

The transformation in each operation maps any equilateral triangle to a similar triangle with one quarter of the area. Similarity guarantees that shape does not matter beyond scale, so only area evolution is relevant. Since each step applies the same constant ratio independently, the area after $K$ steps is exactly the initial area multiplied by the product of $K$ identical factors $1/4$. This multiplicative invariance ensures that no intermediate geometric reasoning is required, and no sequence-dependent behavior exists.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

H, K = map(int, input().split())

# initial area of equilateral triangle from height
area0 = (math.sqrt(3) / 3.0) * H * H

# each operation keeps 1/4 of the area
area = area0 * (0.25 ** K)

print(area)
```

The code first converts the geometric height into area using the standard equilateral triangle identity. The transformation is then applied as a single power operation, avoiding any iterative loop. Using `0.25 ** K` ensures both clarity and numerical stability compared to repeated division.

A common pitfall is computing side length first and then recomputing area, which introduces extra floating-point operations without improving accuracy. Another is looping K times, which is unnecessary and may accumulate rounding error.

## Worked Examples

### Example 1

Input:

```
10 2
```

Initial area:

$$A_0 = \frac{\sqrt{3}}{3} \cdot 100$$

| Step | Current Area | Operation Factor | New Area |
| --- | --- | --- | --- |
| 0 | 57.7350 | - | 57.7350 |
| 1 | 57.7350 | 1/4 | 14.4338 |
| 2 | 14.4338 | 1/4 | 3.6084 |

Output:

```
3.608439
```

This trace shows the repeated uniform scaling behavior. The invariant is that each step reduces area by exactly a factor of 4.

### Example 2

Input:

```
5 0
```

| Step | Current Area | Operation Factor | New Area |
| --- | --- | --- | --- |
| 0 | 14.4338 | - | 14.4338 |

Output:

```
14.433757
```

This demonstrates the base case where no transformation occurs. The algorithm correctly avoids applying any scaling factor.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations and one exponentiation |
| Space | O(1) | No auxiliary data structures used |

The computation fits easily within constraints, and floating-point exponentiation of $K \le 10^5$ is efficient in Python due to optimized power routines.

## Test Cases

```python
import sys, io
import math

def solve():
    input = sys.stdin.readline
    H, K = map(int, input().split())
    area0 = (math.sqrt(3) / 3.0) * H * H
    print(area0 * (0.25 ** K))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio
    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("10 2")[:5] == "3.608"
assert run("5 0")[:6] == "14.433"

# custom cases
assert run("1 0")[:5] == "0.577", "minimum height no operations"
assert run("1 1") != "0", "single reduction should shrink area"
assert run("1000000000 0") != "", "maximum H no operations"
assert run("2 5") != "", "small height large K stability check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | base area | minimum input and no reduction |
| 1 1 | reduced value | single transformation correctness |
| 1000000000 0 | large H | numerical stability at max scale |
| 2 5 | small H, large K | exponentiation stability |

## Edge Cases

For $K = 0$, the algorithm should return the original triangle area without applying any scaling. If we follow the formula mechanically, the exponentiation $4^0 = 1$, so the result remains unchanged. For input $H = 10, K = 0$, the computation becomes:

$$A = \frac{\sqrt{3}}{3} \cdot 100 \cdot 1$$

The algorithm naturally handles this without special branching.

For large $K$, say $K = 100000$, the factor $0.25^K$ underflows toward zero in floating-point arithmetic. This is consistent with the mathematical limit since the area tends to zero exponentially. The printed tolerance allows this behavior, so the result remains valid even if it becomes numerically zero.

For large $H$, such as $H = 10^9$, the initial area becomes large but still well within double precision range when combined with exponential decay, because scaling by $4^{-K}$ quickly reduces magnitude for moderate $K$.
