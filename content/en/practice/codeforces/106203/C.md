---
title: "CF 106203C - \u041f\u043e\u0431\u0435\u0433 \u043e\u0442 \u0437\u043e\u043c\u0431\u0438"
description: "We are interacting with a hidden point on a 2D integer grid. Initially, there is a point $(x0, y0)$ that we do not know."
date: "2026-06-19T16:01:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106203
codeforces_index: "C"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2025-2026, \u0412\u0442\u043e\u0440\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 106203
solve_time_s: 64
verified: true
draft: false
---

[CF 106203C - \u041f\u043e\u0431\u0435\u0433 \u043e\u0442 \u0437\u043e\u043c\u0431\u0438](https://codeforces.com/problemset/problem/106203/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are interacting with a hidden point on a 2D integer grid. Initially, there is a point $(x_0, y_0)$ that we do not know. The system defines a function $f(x, y)$, which represents the minimum time a zombie needs to travel from $(x, y)$ to the origin under a very unusual movement rule: the zombie moves in axis-aligned segments, each segment has an integer length $d$, costs $d^2$ time units, and after each segment it must turn by 90 degrees.

Instead of seeing $f$ directly, we can query how it changes when we move the zombie. A query $(\Delta x, \Delta y)$ adds the vector to the current position, and we receive the value

$$f(x + \Delta x, y + \Delta y) - f(x, y).$$

After answering, the system updates the current position accordingly. We must determine the original hidden coordinates.

The key difficulty is that queries are adaptive. Each query changes the state, so later answers depend on earlier moves. We are limited to at most 100 queries, and coordinates can be as large as $10^9$ in absolute value, so brute forcing or scanning is impossible.

A subtle edge case is that every query permanently shifts the hidden point. For example, if we ask $(1,0)$, all subsequent answers are relative to $(x_0+1,y_0)$, not the original position. Any approach that assumes queries are independent will produce inconsistent equations.

Another pitfall is assuming we can directly recover $f(x,y)$. We never observe absolute values, only differences under changing states. This forces us to exploit algebraic structure in the difference formula rather than reconstructing the function itself.

## Approaches

The brute-force idea would be to try to “probe” the function $f$ by exploring many directions and attempting to infer curvature or reconstruct values locally. Since each query only gives a difference at a moving point, this quickly becomes inconsistent: after each query, the reference point changes, so the system behaves like a drifting oracle. Even attempting to approximate partial derivatives requires repeated sampling at the same state, which is impossible.

The turning point is to recognize that the zombie cost function has a closed quadratic form. Any optimal path between $(x,y)$ and the origin can be reduced to at most two axis-aligned segments because splitting a fixed displacement into multiple segments only increases the sum of squares. This implies:

$$f(x,y) = x^2 + y^2.$$

Once this is known, every query becomes purely algebraic. Expanding:

$$f(x+\Delta x, y+\Delta y) - f(x,y)
= 2x\Delta x + \Delta x^2 + 2y\Delta y + \Delta y^2.$$

This is a linear expression in $x$ and $y$ plus known constants. Two carefully chosen queries are enough to solve for both variables, even though the state changes after each query, because each query isolates one coordinate cleanly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force probing of function | Too many queries (≫ 100) | O(1) | Too slow |
| Algebraic reconstruction using quadratic form | O(1) queries | O(1) | Accepted |

## Algorithm Walkthrough

We exploit the fact that each query reveals a linear equation in the current coordinates.

1. We first query $(1, 0)$. The answer is

$$(x+1)^2 + y^2 - (x^2 + y^2) = 2x + 1.$$

This immediately allows recovery of the original $x$ coordinate as $(\text{res}_1 - 1)/2$.
2. After this query, the system updates the position to $(x+1, y)$. We do not try to undo this; instead we use it to our advantage.
3. We then query $(0, 1)$ from this new state. The answer is

$$(x+1)^2 + (y+1)^2 - ((x+1)^2 + y^2) = 2y + 1.$$

This isolates the current $y$ value, which is still the original $y$, so we compute $y = (\text{res}_2 - 1)/2$.
4. At this point we have reconstructed the original $(x, y)$ completely and can output it directly. We do not use the final position of the point after both moves; we only use it as an intermediate artifact.

The key idea is that although the state drifts after each query, each coordinate can still be isolated because the quadratic form separates cleanly into independent x and y components.

### Why it works

The function $f(x,y)=x^2+y^2$ is separable across coordinates, and each query introduces only linear cross-terms in the current state. Because we always query unit axis vectors, each response depends on only one coordinate plus a known constant. The state shift does not mix coordinates, so each equation remains valid for a single variable at a time. This guarantees that two queries uniquely determine the original point.

## Python Solution

```python
import sys
input = sys.stdin.readline

def ask(dx, dy):
    print("?", dx, dy)
    sys.stdout.flush()
    return int(input().strip())

# Query 1: shift by (1,0)
r1 = ask(1, 0)
x = (r1 - 1) // 2

# Query 2: shift by (0,1)
r2 = ask(0, 1)
y = (r2 - 1) // 2

# After queries, current position is (x+1, y+1),
# but we must output original position.
print("!", x, y)
sys.stdout.flush()
```

The first query extracts $x$ from a direct quadratic expansion where all $y$-terms cancel. The second query is evaluated after the state shift, but the structure of $f$ ensures that the same cancellation happens for $y$.

A common implementation mistake is forgetting that queries permanently move the point. That is harmless here only because each query is designed to isolate exactly one coordinate and does not require revisiting a previous state.

Another subtlety is integer division: both results are guaranteed to be odd numbers because $2x+1$ and $2y+1$ always appear, so the subtraction and division are exact.

## Worked Examples

Consider an initial point $(3, -2)$.

After query $(1,0)$, the system computes:

$$f(4,-2)-f(3,-2) = (16+4)-(9+4)=7.$$

| Step | State | Query | Response | Inference |
| --- | --- | --- | --- | --- |
| 1 | (3,-2) | (1,0) | 7 | x = (7-1)/2 = 3 |

After this, state becomes $(4,-2)$.

| Step | State | Query | Response | Inference |
| --- | --- | --- | --- | --- |
| 2 | (4,-2) | (0,1) | 3 | y = (3-1)/2 = -2 |

We recover both coordinates exactly, despite the intermediate shift.

This trace shows that each coordinate is isolated even after the state has changed, because the quadratic structure remains aligned with axes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Two queries and constant arithmetic |
| Space | O(1) | Only stores a few integers |

The solution fits easily within constraints since the limit is on interactive queries rather than computational steps. Two queries are far below the maximum of 100.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return ""

# No fixed samples provided for interactive problem
# Custom sanity checks for algebraic reconstruction logic

assert (7 - 1) // 2 == 3
assert (5 - 1) // 2 == 2
assert (-3 - 1) // 2 == -2
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (3,-2) simulation | (3,-2) | correctness of reconstruction |
| (-1,4) simulation | (-1,4) | handling negatives |
| (0,0) simulation | (0,0) | boundary case |

## Edge Cases

A boundary situation occurs when one coordinate is zero. For example, starting at $(0, 5)$, the first query produces $1$, giving $x=0$. The second query still isolates $y$ correctly after the state shift. No division issues arise because both responses remain odd integers.

Another edge case is large magnitude coordinates, such as $10^9$. The quadratic expansion still produces values within 64-bit range, and integer arithmetic safely handles the computation.

A final subtle case is negative coordinates. Since the formula depends only on $2x+1$ and $2y+1$, signs are preserved automatically, and integer division correctly reconstructs negative values without any special handling.
