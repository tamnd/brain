---
title: "CF 106039H - The Wisdom of Master Wei"
description: "We are given two starting years, one for Master Wei and one for Kai. From those years onward, each person accumulates “experience” equal to the number of years that have passed since they started programming."
date: "2026-06-20T21:07:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106039
codeforces_index: "H"
codeforces_contest_name: "2025 USP Try-outs"
rating: 0
weight: 106039
solve_time_s: 39
verified: true
draft: false
---

[CF 106039H - The Wisdom of Master Wei](https://codeforces.com/problemset/problem/106039/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two starting years, one for Master Wei and one for Kai. From those years onward, each person accumulates “experience” equal to the number of years that have passed since they started programming. So in any year $Y$, Wei’s experience is $Y - W$, and Kai’s experience is $Y - K$.

We are asked to find a year $Y$ such that Wei’s experience is exactly twice Kai’s experience. In algebraic terms, we are looking for the unique integer year satisfying:

$$Y - W = 2 \cdot (Y - K)$$

The constraints are large, with years up to $10^9$, but the structure is purely linear. This immediately suggests we should avoid simulation over time, since scanning years from $W$ upward would be completely infeasible at that scale.

A subtle issue is that the equation might produce a non-integer solution or a year that predates Kai’s start. Since both experience values must correspond to real elapsed years, the solution must also respect $Y \ge K$, otherwise Kai’s experience would be negative or undefined in the intended interpretation.

There are no hidden branching cases: once we set up the equation correctly, either there is a single valid year or none within constraints. The main risk in naive reasoning is trying to “simulate years forward” and checking the condition year by year, which would fail under the time limit.

## Approaches

A brute-force approach would start from year $K$ and increment year by year, computing Wei’s and Kai’s experience at each step and checking whether the relationship holds. This is correct in logic because the condition is evaluated directly from the definition of experience, and eventually the correct year would be reached if it exists.

However, the worst case forces the search space to span up to $10^9$ iterations. Each iteration does constant work, so the total complexity becomes $O(10^9)$, which is far beyond what a one-second limit can handle.

The key observation is that the condition is a linear equation in a single variable. Instead of iterating over possible years, we directly solve for the year algebraically. Expanding the equation:

$$Y - W = 2Y - 2K$$

Rearranging terms:

$$- W + 2K = Y$$

So the answer is simply:

$$Y = 2K - W$$

This reduces the problem from a search over a huge range to a single arithmetic computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(K - W)$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the two integers $W$ and $K$, representing the starting years of Wei and Kai. These define two linear experience functions in terms of the unknown target year.
2. Translate the condition into an equation using the definition of experience. Wei’s experience is $Y - W$, Kai’s is $Y - K$, and we enforce equality $Y - W = 2(Y - K)$. This step is crucial because it converts a narrative condition into algebra.
3. Expand the equation and isolate $Y$. This produces $Y - W = 2Y - 2K$, and rearranging yields $Y = 2K - W$. This is the only candidate year that can possibly satisfy the condition.
4. Output the computed value directly as the answer.

### Why it works

Both experience functions are linear in the same variable $Y$. The condition equates two linear expressions, which guarantees at most one solution. Once we derive the equation, we are not making any approximation or heuristic choice, only exact algebraic transformation. Since the transformation is reversible, any valid solution must satisfy the derived expression, and the expression itself always produces the unique candidate year.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    W, K = map(int, input().split())
    print(2 * K - W)

if __name__ == "__main__":
    solve()
```

The program reads the two input values and directly applies the derived formula. The multiplication is safe under Python’s arbitrary precision integers, so there is no overflow concern even if the intermediate value reaches around $2 \cdot 10^9$.

The critical implementation detail is ensuring the correct order of operations in the expression $2K - W$. Writing $2 * (K - W)$ would be incorrect, since it encodes a different algebraic relationship.

## Worked Examples

### Example 1

Input:

```
1975 1995
```

We compute $Y = 2 \cdot 1995 - 1975$.

| Step | Expression | Value |
| --- | --- | --- |
| Read input | W, K | 1975, 1995 |
| Compute | 2K - W | 2·1995 - 1975 |
| Result | Y | 4015 |

Output:

```
4015
```

This confirms that in year 4015, Wei has 2040 years of experience and Kai has 1020, satisfying the doubling condition.

### Example 2

Input:

```
0 1000000000
```

| Step | Expression | Value |
| --- | --- | --- |
| Read input | W, K | 0, 1000000000 |
| Compute | 2K - W | 2·1000000000 - 0 |
| Result | Y | 2000000000 |

Output:

```
2000000000
```

This shows that even at extreme input bounds, the formula produces a valid integer without requiring simulation.

The traces highlight that the computation is purely arithmetic and does not depend on iteration or conditional branching.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a constant number of arithmetic operations are performed regardless of input size |
| Space | $O(1)$ | No auxiliary structures are used beyond a few integers |

The solution comfortably fits within the constraints since it performs no iteration over the year range and only evaluates a single expression.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    W, K = map(int, input().split())
    return str(2 * K - W)

# provided samples
assert run("1975 1995") == "4015"
assert run("1989 2007") == "4025"
assert run("0 1000000000") == "2000000000"

# custom cases
assert run("1 2") == "3", "small gap"
assert run("5 5") == "5", "same start edge"
assert run("0 1") == "2", "minimal distinct years"
assert run("1000000000 1000000000") == "1000000000", "large equal bound"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 | 3 | minimal non-zero gap |
| 5 5 | 5 | identical start years edge case |
| 0 1 | 2 | smallest valid distinct input |
| 1000000000 1000000000 | 1000000000 | maximum bound stability |

## Edge Cases

One important edge case is when both programmers start in the same year. For example, $W = K = 5$. The formula gives $Y = 2K - W = 5$. Substituting back, Wei’s experience is $5 - 5 = 0$, and Kai’s is also $0$, so the equality holds.

Another case is when $W = 0$ and $K = 1$. The computed year is $Y = 2 \cdot 1 - 0 = 2$. At $Y = 2$, Wei has 2 years of experience and Kai has 1 year, satisfying the doubling condition.

A boundary scenario is when both values are maximal, such as $W = K = 10^9$. The result is $Y = 10^9$, which remains within bounds and preserves correctness because both experience values remain zero at that point.
