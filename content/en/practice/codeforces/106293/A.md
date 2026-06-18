---
title: "CF 106293A - \u0421\u0440\u0435\u0434\u043d\u0435\u0435 \u0438 \u043c\u0435\u0434\u0438\u0430\u043d\u0430"
description: "We are given two fixed integers $a$ and $b$, and we are allowed to choose a third integer $c$. Once $c$ is chosen, we form a triple $(a, b, c)$."
date: "2026-06-18T22:34:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106293
codeforces_index: "A"
codeforces_contest_name: "\u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 1\u0421, \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u0442\u0443\u0440 2025-2026"
rating: 0
weight: 106293
solve_time_s: 55
verified: true
draft: false
---

[CF 106293A - \u0421\u0440\u0435\u0434\u043d\u0435\u0435 \u0438 \u043c\u0435\u0434\u0438\u0430\u043d\u0430](https://codeforces.com/problemset/problem/106293/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two fixed integers $a$ and $b$, and we are allowed to choose a third integer $c$. Once $c$ is chosen, we form a triple $(a, b, c)$. The goal is to make $c$ as large as possible while keeping a specific inequality true: the arithmetic mean of the three numbers must not exceed their median.

The arithmetic mean is simply $(a+b+c)/3$. The median is the middle value after sorting the three numbers in non-decreasing order. So for any choice of $c$, the ordering of the triple changes the median, which makes the condition piecewise and dependent on how $c$ compares to $a$ and $b$.

The key constraint is that $a$ and $b$ can be as large as $10^{18}$, so any solution must avoid brute force over $c$. Trying values of $c$ linearly or even with binary search over the entire range is too slow unless we can evaluate the condition in constant time.

A subtle difficulty comes from the fact that the median is not fixed. For example, if $a = 1$, $b = 10$, and $c = 5$, then the median is $5$, but if $c = 100$, the median becomes $10$. The condition changes structure depending on which of the three possible positions $c$ occupies in the sorted order.

Edge cases arise when all three numbers collapse into a single value or when $c$ is extremely large and becomes the maximum element. For instance, if $a = b = 3$, then any valid solution must respect symmetry, and the correct answer becomes $c = 3$, because any larger $c$ would push the median upward in a way that violates the inequality.

## Approaches

A brute-force approach would try increasing values of $c$, compute the median each time by sorting the triple, and check whether the inequality holds. Each check is $O(1)$, but $c$ ranges up to $10^{18}$, so even iterating through a meaningful subset is impossible.

The key observation is that the median of three numbers has only three structural cases depending on where $c$ lies relative to $a$ and $b$. Once we sort $a$ and $b$, we only need to consider whether $c$ is the smallest, middle, or largest element. In each case, the median becomes a fixed expression, turning the inequality into a simple linear constraint on $c$. This reduces the problem from searching over integers to evaluating a small number of algebraic conditions and taking the maximum feasible value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over $c$ | $O(10^{18})$ | $O(1)$ | Too slow |
| Case analysis by ordering | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We start by ensuring a clean ordering between the two fixed values.

1. Sort the input so that $a \le b$. This removes symmetry and ensures all later reasoning about relative positions of $c$ is consistent.
2. Consider the first structural case where $c \le a \le b$. In this situation, the sorted triple is $(c, a, b)$, so the median is $a$. The inequality becomes $(c + a + b)/3 \le a$, which simplifies to $c + b \le 2a$. Since $b \ge a$, this immediately restricts $c \le a$. The largest feasible value in this region is therefore $c = a$.
3. Consider the second case where $a \le c \le b$. Now the sorted triple is $(a, c, b)$, so the median is $c$. The condition becomes $a + b + c \le 3c$, which simplifies to $a + b \le 2c$, or $c \ge (a+b)/2$. Since we want to maximize $c$ while staying in this interval, we try $c = b$. Substituting, we get $a + b \le 2b$, which always holds because $b \ge a$. So the maximum feasible value in this region is $c = b$.
4. Consider the third case where $a \le b \le c$. Now the sorted triple is $(a, b, c)$, so the median is $b$. The inequality becomes $a + b + c \le 3b$, which simplifies to $a + c \le 2b$, giving an upper bound $c \le 2b - a$. Since we are in the region $c \ge b$, the best possible choice is $c = 2b - a$.
5. Finally, compare candidates from all cases. The best from the first case is $a$, from the second is $b$, and from the third is $2b-a$. Since $b \ge a$, the first case is never optimal. Also, $2b-a \ge b$, so the third case dominates the second. Therefore the final answer is $c = 2b - a$.
6. If the original ordering had $a > b$, symmetry gives $c = 2a - b$. Combining both directions, the answer is $2\max(a,b) - \min(a,b)$.

### Why it works

The median constraint depends only on ordering, and with three elements there are only three possible order configurations. Within each configuration, the inequality becomes linear in $c$, producing a single upper or lower bound. The optimal solution must lie at the boundary of one of these regions, and comparing those boundaries exhausts all possibilities without missing transitions between orderings.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a = int(input())
    b = int(input())
    
    if a > b:
        a, b = b, a
    
    # optimal derived from case analysis
    print(2 * b - a)

if __name__ == "__main__":
    solve()
```

The implementation first normalizes the ordering so that all reasoning assumes $a \le b$. This avoids duplicating case logic. The final formula $2b-a$ directly corresponds to the best achievable value from the region where $c$ becomes the maximum element, which dominates all other configurations.

A common mistake is forgetting that the optimal solution always lies at a boundary where $c$ is either aligned with $a$, $b$, or the derived linear bound $2b-a$. The final reduction collapses all of this structure into a single expression.

## Worked Examples

### Example 1

Input:

$a = 1, b = 10$

We first sort, so $a=1, b=10$.

| Step | Case | Median | Constraint | Candidate |
| --- | --- | --- | --- | --- |
| 1 | $c \le a$ | 1 | $c \le 1$ | 1 |
| 2 | $a \le c \le b$ | c | always valid up to 10 | 10 |
| 3 | $c \ge b$ | 10 | $c \le 19$ | 19 |

The best value is 19, which comes from the third case. This demonstrates that pushing $c$ above both numbers increases the median in a controlled linear way.

### Example 2

Input:

$a = 7, b = 7$

Sorted already.

| Step | Case | Median | Constraint | Candidate |
| --- | --- | --- | --- | --- |
| 1 | $c \le 7$ | 7 | $c \le 7$ | 7 |
| 2 | $7 \le c \le 7$ | 7 | always valid | 7 |
| 3 | $c \ge 7$ | 7 | $c \le 7$ | 7 |

All cases collapse to the same boundary, confirming that symmetry forces $c = 7$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a few comparisons and arithmetic operations are performed |
| Space | $O(1)$ | No additional data structures are used |

The solution runs instantly even for maximum input sizes because it avoids any iteration over the range of possible values for $c$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    
    a = int(input())
    b = int(input())
    
    if a > b:
        a, b = b, a
    
    return str(2 * b - a)

# provided samples (conceptual, since exact sample text is partial)
assert run("1\n10\n") == "19", "basic increasing pair"
assert run("3\n3\n") == "3", "equal values"

# custom cases
assert run("1\n1\n") == "1", "minimum symmetric case"
assert run("5\n10\n") == "15", "checks linear extension"
assert run("10\n5\n") == "15", "order swap symmetry"
assert run("1000000000000000000\n1\n") == str(2*1000000000000000000 - 1), "large boundary case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 1 | 1 | smallest symmetric case |
| 5, 10 | 15 | standard increasing pair |
| 10, 5 | 15 | symmetry under swapping |
| large values | 2b-a | stress test for overflow logic |

## Edge Cases

When $a = b$, the algorithm reduces immediately to $c = a$. In this situation all three numbers are identical, so the mean and median always coincide regardless of ordering, and the linear formula $2b-a$ correctly collapses to $a$.

When one value is extremely large compared to the other, for example $a = 1$ and $b = 10^{18}$, the algorithm selects $c = 2b - a$. This corresponds to placing $c$ above both numbers, where the median stabilizes at $b$. The inequality then becomes tight at the boundary $a + c = 2b$, which the formula satisfies exactly.

When inputs are swapped, the normalization step ensures consistency. For instance, $a = 10, b = 1$ is converted internally to $a = 1, b = 10$, so the same reasoning applies without branching on input order.
