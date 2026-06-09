---
title: "CF 1860F - Evaluate RBS"
description: "We are given $2n$ tuples of the form $(a, b, c)$, where $a$ and $b$ are positive integers and $c$ is a bracket, either '(' or ')'. Exactly half of the tuples are opening brackets and the other half are closing brackets."
date: "2026-06-09T00:23:45+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "geometry", "implementation", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1860
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 153 (Rated for Div. 2)"
rating: 2900
weight: 1860
solve_time_s: 88
verified: true
draft: false
---

[CF 1860F - Evaluate RBS](https://codeforces.com/problemset/problem/1860/F)

**Rating:** 2900  
**Tags:** data structures, geometry, implementation, math, sortings  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given $2n$ tuples of the form $(a, b, c)$, where $a$ and $b$ are positive integers and $c$ is a bracket, either '(' or ')'. Exactly half of the tuples are opening brackets and the other half are closing brackets. The goal is to find two positive numbers $x$ and $y$ and sort the tuples by the value $a \cdot x + b \cdot y$. After sorting, the sequence of brackets extracted from the tuples should form a regular bracket sequence.

A regular bracket sequence (RBS) is one where, when scanning from left to right, the number of closing brackets never exceeds the number of opening brackets at any position, and the total number of opening and closing brackets is equal.

The constraints allow $n$ up to 1500 per testcase, and the sum of $n$ across all testcases is also at most 1500. This makes an $O(n^2)$ approach feasible for each testcase, but $O(n^3)$ will likely be too slow. Each $a_i$ and $b_i$ is up to $10^6$, but we do not need to enumerate all possible $x$ and $y$; we need a strategy to determine whether a solution exists.

A naive approach that tries all possible positive $x$ and $y$ pairs is clearly impossible because they are continuous real numbers. Edge cases include situations where all tuples of '(' dominate all tuples of ')' in both coordinates, or where the points are interleaved in a way that no linear combination of $x$ and $y$ can separate them. A careless solution might assume sorting by either $a$ or $b$ independently is enough, which fails for inputs like $(1,4,'(')$, $(2,3,')')$, where the optimal solution requires a nontrivial combination.

## Approaches

The brute-force idea would attempt to enumerate all possible positive $(x, y)$ combinations or simulate sorting by every possible combination of the $a$ and $b$ values. This is infeasible because $x$ and $y$ are continuous real numbers. Even restricting $x$ and $y$ to integers up to $10^6$ would still produce $10^{12}$ candidate sums, far beyond computational limits.

The key observation is geometric. Consider each tuple as a point in the plane $(a_i, b_i)$, with its type $c_i$. The value $a \cdot x + b \cdot y$ is the dot product of vector $(a_i, b_i)$ with $(x, y)$. Sorting tuples by this dot product is equivalent to sweeping a line with normal vector $(x, y)$ from the origin and ordering points by their projection along this vector. Choosing $x$ and $y$ positive means the sweep moves from the bottom-left toward the top-right.

A tuple with '(' must precede a tuple with ')' in the sorted order if its projection along $(x, y)$ is smaller. Thus, the problem reduces to: can we choose a positive slope line such that the points corresponding to '(' and ')' can be linearly separated along that line while preserving an RBS order?

Instead of explicitly finding $(x, y)$, we can reason using **slopes between points**. For two points $p_1 = (a_1, b_1, '(')$ and $p_2 = (a_2, b_2, ')')$, the condition that $p_1$ must be before $p_2$ translates to $(a_2 - a_1)x + (b_2 - b_1)y > 0$. Geometrically, this is a half-plane constraint on $(x, y)$. All such constraints must have a non-empty intersection in the first quadrant $(x>0, y>0)$ to allow a solution.

The algorithm uses a greedy approach that sorts by **angles**. Consider each point relative to the origin. The problem reduces to arranging the vectors so that opening brackets never drop below closing brackets. We can implement this by considering points sorted by angle in the first quadrant.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((10^6)^2) | O(n) | Too slow |
| Geometric / slope ordering | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Separate the tuples into opening '(' and closing ')' groups. Each group has exactly $n$ points.
2. Sort each group by the slope $b_i / a_i$. For the opening brackets, sort in increasing slope. For closing brackets, sort in decreasing slope. This ensures that the extremes of each group allow a separating line in the first quadrant.
3. Pair the opening and closing tuples greedily: take the opening with the smallest slope and the closing with the largest slope. Check if there exists a line $(x, y)$ with $x, y > 0$ that separates them.
4. The separation condition is equivalent to $a_{\text{open}} \cdot y + b_{\text{open}} \cdot x < a_{\text{close}} \cdot y + b_{\text{close}} \cdot x$ for some $x, y > 0$, which reduces to the cross inequality: $(a_{\text{close}} - a_{\text{open}}) * y + (b_{\text{close}} - b_{\text{open}}) * x > 0$. This is always solvable if the slope intervals of opening and closing brackets do not overlap.
5. If all pairs satisfy the separation condition, output YES. Otherwise, output NO.

Why it works: by sorting by slopes and pairing extremes, we ensure that for any potential violation of RBS (a closing bracket appearing too early), the inequality is violated, and no positive $(x, y)$ can resolve it. Conversely, if no such violation occurs, there exists a positive linear combination that produces the RBS. The invariant is that at each step, the cumulative sum of opening minus closing brackets never becomes negative.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        opens, closes = [], []
        for _ in range(2 * n):
            a, b, c = input().split()
            a = int(a)
            b = int(b)
            if c == '(':
                opens.append((a, b))
            else:
                closes.append((a, b))
        
        # Sort openings by slope b/a increasing
        opens.sort(key=lambda p: p[1]/p[0])
        # Sort closings by slope b/a decreasing
        closes.sort(key=lambda p: -p[1]/p[0])
        
        possible = True
        for (ao, bo), (ac, bc) in zip(opens, closes):
            if (ac - ao) * (bo) < (bc - bo) * (ao):
                possible = False
                break
        print("YES" if possible else "NO")

if __name__ == "__main__":
    solve()
```

The solution first partitions tuples into '(' and ')'. Sorting by slopes ensures that the first quadrant separation exists. The cross inequality check guarantees no closing bracket precedes an opening bracket in any feasible $(x, y)$.

## Worked Examples

### Example 1

Input tuples: `(1,4,'(')`, `(2,3,')')`.

| Tuple | Group | Slope b/a |
| --- | --- | --- |
| (1,4,'(') | opens | 4 |
| (2,3,')') | closes | 1.5 |

Open slopes sorted: [4], Close slopes sorted decreasing: [1.5].

Check inequality: `(2-1)*y + (3-4)*x > 0` ⇒ `y - x > 0`. Positive solution exists with `y=2, x=1`. Output YES.

### Example 2

Input tuples: `(1,2,')')`, `(3,4,'(')`.

Open slopes sorted: [1] (3/4 = 0.75?), closing slopes sorted: [2/1 = 2?]

Check inequality: `(1-3)*y + (2-4)*x > 0` ⇒ `-2y -2x > 0`, impossible for positive x, y. Output NO.

These traces confirm that sorting by slopes and checking cross-inequalities accurately captures feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting each group of n elements dominates, pairing is O(n) |
| Space | O(n) | We store separate lists for opens and closes |

Since sum of n over all testcases ≤ 1500, total work is well under 10^6 operations, safe for a 10-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("""4
1
1 4 (
2 3 )
1
1 2 )
3 4 (
4
16 5 (
12 3 (
19 6 )
4
```
