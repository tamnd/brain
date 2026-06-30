---
title: "CF 104442H - El m\u00e1ximo de diversi\u00f3n"
description: "We are given several independent sequences of points in the plane, where each sequence describes a fixed route that must be followed in order. Each route is a list of coordinates $(x1, y1), (x2, y2), dots, (xn, yn)$, and we only care about movements between consecutive points."
date: "2026-06-30T18:07:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104442
codeforces_index: "H"
codeforces_contest_name: "AdaByron Regional Madrid 2023"
rating: 0
weight: 104442
solve_time_s: 46
verified: true
draft: false
---

[CF 104442H - El m\u00e1ximo de diversi\u00f3n](https://codeforces.com/problemset/problem/104442/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent sequences of points in the plane, where each sequence describes a fixed route that must be followed in order. Each route is a list of coordinates $(x_1, y_1), (x_2, y_2), \dots, (x_n, y_n)$, and we only care about movements between consecutive points.

For every consecutive pair of points, we compute a “fun cost” defined by a linear expression: three times the absolute horizontal displacement plus twice the signed vertical displacement. The horizontal part ignores direction, while the vertical part preserves direction, so moving upward and downward are treated differently.

For each test case, the goal is simply to find the maximum value of this cost among all consecutive pairs in the route.

The input size constraints allow up to 200 sequences, each with up to 1000 points, so at most about 200,000 edges in total. This immediately suggests that an $O(n)$ scan per test case is sufficient, since even a full linear pass over all points stays comfortably within limits.

A common subtle mistake here comes from misreading the absolute value structure. Only the x difference is absolute. The y difference is not. For example, between $(0, 0)$ and $(0, -10)$, the contribution is $3 \cdot 0 + 2 \cdot (-10) = -20$, which is negative. A mistaken implementation that applies absolute value to both coordinates would incorrectly turn this into $20$, changing the maximum entirely.

Another issue is assuming the result must be non-negative. Because of the signed vertical term, the maximum over all edges can still be negative if all movements decrease the expression.

## Approaches

The structure of the problem is extremely local. Each edge contributes independently to the final answer, and there is no interaction between different segments of the path. This immediately rules out any need for prefix structures, dynamic programming, or geometric optimization.

A brute-force approach is already optimal: compute the value for every adjacent pair and track the maximum. There is no alternative formulation that reduces the number of required comparisons, since every edge must be inspected at least once to guarantee correctness.

One might try to search for a global geometric interpretation, but the expression is not a distance metric and does not satisfy symmetry or triangle properties in a useful way. The dependence is strictly pairwise, so the problem reduces to scanning an array of computed values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Evaluate each edge independently | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read the number of points $n$ and the coordinate list. The coordinates are given in flattened form, so we interpret them as consecutive pairs.
2. Initialize a variable `best` to a very small number, since all computed values may be negative.
3. Iterate over each consecutive pair of points from $i = 1$ to $n - 1$. For each pair, extract $(x_i, y_i)$ and $(x_{i+1}, y_{i+1})$.
4. Compute the horizontal difference as $|x_{i+1} - x_i|$. This ensures direction does not matter for horizontal movement.
5. Compute the vertical difference as $y_{i+1} - y_i$ without modification.
6. Evaluate the cost $3 \cdot |x_{i+1} - x_i| + 2 \cdot (y_{i+1} - y_i)$.
7. Update `best` if this value is larger than the current stored maximum.
8. After processing all edges, output `best`.

### Why it works

Each edge contributes an independent scalar score, and the problem asks for the maximum among these independent values. Since there is no coupling between edges, any global optimum must coincide with the maximum of the local evaluations. The algorithm enumerates all possible contributors exactly once, so no candidate can be missed and no value is double-counted or modified by future steps.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        
        best = -10**18
        
        for i in range(n - 1):
            x1, y1 = arr[2*i], arr[2*i + 1]
            x2, y2 = arr[2*i + 2], arr[2*i + 3]
            
            val = 3 * abs(x2 - x1) + 2 * (y2 - y1)
            if val > best:
                best = val
        
        out.append(str(best))
    
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the mathematical definition. The key detail is keeping the vertical term signed. Another subtle point is initializing `best` with a very small value instead of zero, since all computed values can be negative.

## Worked Examples

Consider a single route with three points: $(0,0)$, $(2,1)$, $(3,-2)$.

For the first segment:

| Segment | Δx | Δy | Value |
| --- | --- | --- | --- |
| (0,0) → (2,1) | 2 | 1 | 3·2 + 2·1 = 8 |

For the second segment:

| Segment | Δx | Δy | Value |
| --- | --- | --- | --- |
| (2,1) → (3,-2) | 1 | -3 | 3·1 + 2·(-3) = -3 |

The maximum is 8.

This trace shows that negative vertical movement can reduce the score significantly, so the optimal edge is not necessarily the one with largest absolute displacement.

Now consider a case where all values are negative, such as $(0,0)$, $(0,-1)$, $(0,-2)$.

| Segment | Δx | Δy | Value |
| --- | --- | --- | --- |
| (0,0) → (0,-1) | 0 | -1 | -2 |
| (0,-1) → (0,-2) | 0 | -1 | -2 |

The answer is -2, confirming that the maximum does not imply positivity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each adjacent pair is evaluated exactly once |
| Space | O(1) | Only a constant number of variables are used |

The total number of points across all test cases is bounded by about 200,000, so the solution runs easily within time limits under a linear scan model.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        
        best = -10**18
        for i in range(n - 1):
            x1, y1 = arr[2*i], arr[2*i + 1]
            x2, y2 = arr[2*i + 2], arr[2*i + 3]
            val = 3 * abs(x2 - x1) + 2 * (y2 - y1)
            best = max(best, val)
        out.append(str(best))
    
    return "\n".join(out)

# minimum size
assert run("1\n2\n0 0 1 1\n") == "5"

# all negative vertical movement
assert run("1\n3\n0 0 0 -1 0 -2\n") == "-2"

# horizontal only
assert run("1\n3\n0 0 5 0 10 0\n") == "15"

# mixed values
assert run("1\n4\n0 0 1 2 3 -1 4 0\n") == "9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 → 1 1 | 5 | basic formula correctness |
| descending y chain | -2 | negative maximum handling |
| pure x movement | 15 | absolute x contribution |
| mixed movement | 9 | correct max selection |

## Edge Cases

A key edge case is when all vertical movements are negative, which can make every segment value negative. The algorithm still works because it does not assume non-negativity; it initializes the maximum with a very small value and updates it purely by comparison.

Another edge case is a flat horizontal path. In this situation, the result depends only on horizontal gaps. The absolute value ensures direction changes do not affect the result, so a path that goes left and right still accumulates positive contributions correctly.
