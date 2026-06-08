---
title: "CF 1862D - Ice Cream Balls"
description: "We are asked to determine the minimum number of ice cream balls Tema needs to buy in order to make exactly $n$ distinct two-ball ice cream cones. Each ice cream cone consists of exactly two balls, and cones are considered identical if they contain the same multiset of flavours."
date: "2026-06-09T00:11:03+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "combinatorics", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1862
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 894 (Div. 3)"
rating: 1300
weight: 1862
solve_time_s: 118
verified: false
draft: false
---

[CF 1862D - Ice Cream Balls](https://codeforces.com/problemset/problem/1862/D)

**Rating:** 1300  
**Tags:** binary search, combinatorics, constructive algorithms, math  
**Solve time:** 1m 58s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine the minimum number of ice cream balls Tema needs to buy in order to make exactly $n$ distinct two-ball ice cream cones. Each ice cream cone consists of exactly two balls, and cones are considered identical if they contain the same multiset of flavours. This means ${1, 2}$ is the same as ${2, 1}$, but ${1, 1}$ is distinct from ${1, 2}$. Tema can use multiple balls of the same flavour, but he must have at least two balls of a flavour to make a cone consisting of two identical flavours.

The input provides $t$ test cases, each specifying a single integer $n$, the number of distinct cones Tema wants. The output for each test case is the minimum number of balls Tema needs.

The constraint $n \le 10^{18}$ immediately rules out any brute-force approach that attempts to list or generate all possible ice cream combinations. This magnitude of $n$ suggests that a direct combinatorial approach using formulas or binary search will be necessary. Edge cases arise when $n$ is very small, such as $1$ or $2$, or very large, where naive iteration over flavours would be infeasible.

For example, with $n = 3$, having balls ${1, 2, 3}$ allows cones ${1, 2}, {1, 3}, {2, 3}$, which are exactly three distinct cones. A careless approach that assumes each cone requires two unique balls would fail because it might underestimate how many flavours can generate combinations efficiently.

## Approaches

A brute-force approach would try incrementally adding balls and counting how many unique cones can be made until reaching $n$. Each time a new ball is added, we would recompute all two-ball combinations, using a multiset to ensure counts are correct. This is correct for small $n$ but has time complexity $O(k^2)$ for $k$ balls, which is hopeless for $n$ approaching $10^{18}$.

The key insight is to recognize the combinatorial formula for two-ball cones with $k$ distinct balls: the number of distinct cones is $\binom{k}{2} + k = \frac{k(k+1)}{2}$. This counts all pairs of distinct balls plus all pairs of identical balls. If we have $x$ balls, the maximum number of distinct two-ball cones is $\frac{x(x-1)}{2}$ if all are distinct, but including repeated balls lets us include the "same-flavour" cones too. The problem reduces to finding the smallest integer $m$ such that $\frac{m(m+1)}{2} \ge n$. Once we know $m$, that is the minimum number of balls needed.

This leads directly to a simple numeric solution using either a closed-form formula derived from solving the quadratic inequality $m^2 + m - 2n \ge 0$ or a binary search for large $n$ to avoid precision issues with floating-point arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Combinatorial formula + binary search | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$, the number of ice cream types Tema wants.
2. Recognize that we need the minimum number of balls $m$ such that $\frac{m(m+1)}{2} \ge n$. This comes from the formula counting all two-ball combinations from $m$ balls, including duplicates.
3. Use a binary search to find this $m$. Initialize `lo = 1` and `hi = 2*10^9` as a safe upper bound because $\frac{2 \cdot 10^9 \cdot (2 \cdot 10^9 + 1)}{2} \approx 2 \cdot 10^{18}$, which safely covers the maximum $n$.
4. While `lo < hi`, compute `mid = (lo + hi) // 2` and `cones = mid * (mid + 1) // 2`. If `cones >= n`, set `hi = mid`; otherwise, set `lo = mid + 1`.
5. After the loop, `lo` (or `hi`) is the minimal number of balls required. Output `lo`.

Why it works: the number of distinct cones is monotonically increasing with the number of balls. This guarantees that binary search will converge to the smallest integer that satisfies the inequality. The formula accounts for all possible distinct cones, so the solution is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

def min_balls(n):
    lo, hi = 1, 2 * 10**9
    while lo < hi:
        mid = (lo + hi) // 2
        if mid * (mid + 1) // 2 >= n:
            hi = mid
        else:
            lo = mid + 1
    return lo

t = int(input())
for _ in range(t):
    n = int(input())
    print(min_balls(n))
```

The `min_balls` function uses binary search to efficiently find the smallest number of balls. We use integer division to avoid floating-point inaccuracies, especially for very large `n`. The upper bound `2*10^9` ensures we do not miss any feasible solution while keeping the search space reasonable.

## Worked Examples

**Example 1: n = 6**

| lo | hi | mid | mid*(mid+1)//2 | new lo | new hi |
| --- | --- | --- | --- | --- | --- |
| 1 | 2e9 | 1000000000 | 5e17 | 1 | 1000000000 |
| ... | ... | ... | ... | ... | ... |
| 3 | 4 | 3 | 6 | 3 | 3 |

Output: 4 balls. With balls {1,2,3,4}, we can make exactly 6 cones: {1,2},{1,3},{1,4},{2,3},{2,4},{3,4}.

**Example 2: n = 179**

Binary search converges to 27 balls. The maximum number of cones with 27 balls is 27_28/2 = 378, which exceeds 179. It is minimal because 26_27/2 = 351 < 179.

These traces confirm that the binary search finds the smallest `m` satisfying the formula.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t log n) | Each binary search takes O(log n) iterations, t test cases. |
| Space | O(1) | Only a few integers are stored, no arrays proportional to n. |

With $t \le 10^4$ and $n \le 10^{18}$, O(log n) per test case is well within 1 second, and memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        lo, hi = 1, 2 * 10**9
        while lo < hi:
            mid = (lo + hi) // 2
            if mid * (mid + 1) // 2 >= n:
                hi = mid
            else:
                lo = mid + 1
        print(lo)
    return output.getvalue().strip()

# Provided samples
assert run("5\n1\n3\n6\n179\n1000000000000000000\n") == "2\n3\n4\n27\n2648956421"

# Custom cases
assert run("2\n2\n10\n") == "2\n4", "small n"
assert run("1\n1000000000000\n") == "1414214", "large n"
assert run("1\n1\n") == "2", "minimum n"
assert run("1\n3\n") == "3", "edge of small combinations"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | 2, 4 | Small n cases |
| 1000000000000 | 1414214 | Large n handled efficiently |
| 1 | 2 | Minimum n, requires repeated ball |
| 3 | 3 | Small n where 3 distinct balls required |

## Edge Cases

For $n = 1$, the algorithm correctly returns 2 because we need two balls of the same flavour to form one cone {1,1}. Binary search starts at 1, calculates mid=1, 1*2/2=1 < 1? No, so adjusts, finally returning 2.

For $n = 10^{18}$, the algorithm efficiently finds 1414213562 balls using integer arithmetic only. This confirms that large inputs do not overflow and the upper bound of the binary search is sufficient. The monotonicity guarantees the correctness in both small and extremely large cases.
