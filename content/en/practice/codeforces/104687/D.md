---
title: "CF 104687D - \u0421\u0443\u043c\u043c\u0430 2"
description: "We are working with two integer intervals. One interval defines all valid values of $x$, and another defines all valid values of $y$."
date: "2026-06-29T08:46:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104687
codeforces_index: "D"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440 \u0432 \u0426\u0420\u041e\u0414 2022"
rating: 0
weight: 104687
solve_time_s: 59
verified: true
draft: false
---

[CF 104687D - \u0421\u0443\u043c\u043c\u0430 2](https://codeforces.com/problemset/problem/104687/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with two integer intervals. One interval defines all valid values of $x$, and another defines all valid values of $y$. We are asked to count how many pairs $(x, y)$ can be formed such that $x$ is chosen from its interval, $y$ is chosen from its interval, and their sum is exactly a fixed target value $n$.

Geometrically, you can think of this as counting lattice points inside a rectangle in the plane that lie on the line $x + y = n$. Every valid pair corresponds to a single integer point on this diagonal line segment.

The constraints are large: endpoints go up to $10^9$. This immediately rules out iterating over all values of $x$ or $y$. Any solution that loops over even $10^9$ elements is impossible within typical time limits. We need a way to compute the size of the intersection analytically in constant time.

A subtle failure case for naive reasoning happens when one assumes that for every $x$ in $[l_1, r_1]$, the value $y = n - x$ is automatically valid if it lies in $[l_2, r_2]$ without carefully tracking interval overlap. For example, if $n = 20$, $x = 1$ forces $y = 19$, which may lie outside the second interval even if both intervals individually are large. The correctness depends entirely on the overlap of transformed ranges, not just the existence of a solution per endpoint.

Another corner case appears when the intervals do not intersect in the transformed space at all. For instance, if the smallest possible sum $l_1 + l_2$ is already greater than $n$, or the largest possible sum $r_1 + r_2$ is smaller than $n$, then no solution exists. A naive approach that does not reason about feasibility bounds may still attempt to count pairs and produce incorrect positive values.

## Approaches

A brute-force approach would enumerate every possible $x$ in $[l_1, r_1]$, compute $y = n - x$, and check whether $y$ lies inside $[l_2, r_2]$. This is correct because it directly enforces all constraints. However, its runtime is proportional to the size of the first interval, which in the worst case is $10^9$. Even at $10^8$ operations per second, this is far beyond practical limits.

The key observation is that the equation $x + y = n$ removes one degree of freedom. Once $x$ is chosen, $y$ is fixed. Instead of scanning all $x$, we can determine exactly which $x$ values produce a valid $y$. The condition $l_2 \le n - x \le r_2$ can be rewritten as inequalities on $x$, which transforms the problem into finding the intersection of two intervals in one dimension.

From $l_2 \le n - x \le r_2$, we derive:

$$n - r_2 \le x \le n - l_2$$

So valid $x$ must lie both in $[l_1, r_1]$ and in $[n - r_2, n - l_2]$. The answer becomes the length of the intersection of these two intervals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(r_1 - l_1 + 1)$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

### 1. Convert the condition on $y$ into bounds on $x$

We rewrite $y = n - x$ inside $l_2 \le y \le r_2$, producing $n - r_2 \le x \le n - l_2$. This step removes the dependency on $y$, reducing the problem to a single variable.

### 2. Compute the effective valid interval for $x$

We now have two constraints on $x$: the original interval $[l_1, r_1]$, and the transformed interval $[n - r_2, n - l_2]$. The valid $x$ values must satisfy both simultaneously.

### 3. Take the intersection of the two intervals

The intersection interval is:

$$L = \max(l_1, n - r_2), \quad R = \min(r_1, n - l_2)$$

This step is justified because both constraints are independent and must hold at the same time.

### 4. Count integer points in the intersection

If $L \le R$, the number of integers is $R - L + 1$. Otherwise, there are no valid pairs.

### Why it works

Every valid pair $(x, y)$ corresponds uniquely to an integer $x$ satisfying both interval constraints. The transformation $y = n - x$ is bijective between valid pairs and valid $x$-values. The algorithm does not discard or double-count any value because each step preserves equivalence of constraints, only rewriting them into a single-variable form.

## Python Solution

```python
import sys
input = sys.stdin.readline

l1, r1, l2, r2, n = map(int, input().split())

left = max(l1, n - r2)
right = min(r1, n - l2)

if left <= right:
    print(right - left + 1)
else:
    print(0)
```

The code directly implements the interval transformation. The only subtlety is careful handling of boundary arithmetic. The expressions `n - r2` and `n - l2` define the valid projection of the second interval onto the x-axis. Taking `max` and `min` ensures we respect both constraints simultaneously. The final conditional guards against negative interval length, which corresponds to empty intersection.

## Worked Examples

### Example 1

Input:

```
1 10 1 10 20
```

We compute transformed bounds for $x$: $20 - r_2 = 10$, $20 - l_2 = 19$. So valid $x$ interval from second constraint is $[10, 19]$. Intersecting with $[1, 10]$:

| Step | Value |
| --- | --- |
| l1, r1 | [1, 10] |
| transformed x-range | [10, 19] |
| intersection L | max(1, 10) = 10 |
| intersection R | min(10, 19) = 10 |

There is exactly one valid $x = 10$, giving $y = 10$. This confirms that only the boundary point satisfies both intervals.

### Example 2

Input:

```
0 5 0 5 3
```

We compute transformed bounds: $3 - r_2 = -2$, $3 - l_2 = 3$. Intersection with $[0, 5]$:

| Step | Value |
| --- | --- |
| l1, r1 | [0, 5] |
| transformed x-range | [-2, 3] |
| intersection L | max(0, -2) = 0 |
| intersection R | min(5, 3) = 3 |

Valid $x$ values are $0,1,2,3$, giving 4 pairs. This shows how partial overlap produces a full segment of solutions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | only constant number of arithmetic and comparisons |
| Space | $O(1)$ | no auxiliary structures |

The solution performs a fixed amount of integer arithmetic regardless of input size. This easily fits within constraints even for many test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    l1, r1, l2, r2, n = map(int, sys.stdin.readline().split())
    left = max(l1, n - r2)
    right = min(r1, n - l2)
    return str(max(0, right - left + 1))

# provided sample
assert run("1 10 1 10 20\n") == "1"

# minimal case, single point
assert run("0 0 0 0 0\n") == "1"

# no solution case
assert run("1 5 1 5 100\n") == "0"

# full overlap case
assert run("0 10 0 10 10\n") == "11"

# boundary tight intersection
assert run("2 8 3 9 10\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 0 0 | 1 | single exact solution |
| 1 5 1 5 100 | 0 | no feasible pairs |
| 0 10 0 10 10 | 11 | full interval overlap |
| 2 8 3 9 10 | 6 | partial intersection correctness |

## Edge Cases

One edge case is when the transformed interval lies completely outside the original interval. For example, input:

```
1 3 10 20 5
```

We compute transformed bounds: $5 - 20 = -15$, $5 - 10 = -5$. So valid $x$ from second constraint is $[-15, -5]$. Intersection with $[1, 3]$ gives empty range since $L = 1$, $R = -5$, and $L > R$. The algorithm correctly outputs 0.

Another case is when both intervals collapse to a single point that satisfies the sum constraint:

```
7 7 13 13 20
```

Transformed bounds are $20 - 13 = 7$ and $20 - 13 = 7$, so both intervals become exactly $[7,7]$. Intersection is a single point, and the algorithm returns 1. This confirms that degenerate intervals are handled naturally without special branching.
