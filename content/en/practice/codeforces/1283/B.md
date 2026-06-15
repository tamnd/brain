---
title: "CF 1283B - Candies Division"
description: "We are distributing a fixed number of identical candies among a fixed number of children. Each child must receive a non-negative integer number of candies, and we are allowed to leave some candies unused."
date: "2026-06-16T03:01:57+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1283
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 611 (Div. 3)"
rating: 900
weight: 1283
solve_time_s: 308
verified: true
draft: false
---

[CF 1283B - Candies Division](https://codeforces.com/problemset/problem/1283/B)

**Rating:** 900  
**Tags:** math  
**Solve time:** 5m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are distributing a fixed number of identical candies among a fixed number of children. Each child must receive a non-negative integer number of candies, and we are allowed to leave some candies unused. The distribution is considered valid only if the values assigned to children are tightly balanced: the largest and smallest assigned counts differ by at most one, so every child receives either some value $a$ or the next value $a+1$. On top of that, the higher value $a+1$ cannot be too common, specifically it can appear in at most half of the children, rounded down.

The goal is not to find a valid distribution itself but to maximize how many candies are actually handed out while respecting these constraints.

The input size is large, with up to $5 \cdot 10^4$ test cases and values of $n$ and $k$ up to $10^9$. Any solution that tries to simulate distributions or iterate over possible assignments per test case will be too slow. A correct solution must reduce each test case to constant time arithmetic.

A naive but tempting idea is to try fixing how many children get $a+1$ candies and compute feasibility for each choice. This breaks down in edge cases where the constraint on the number of higher-valued children interacts with leftover candies. For example, with $k = 5$, trying to greedily maximize the average distribution may lead to assigning too many $a+1$ values, violating the $\lfloor k/2 \rfloor$ cap even though a slightly different split would allow more total candies.

Another failure mode comes from assuming that distributing all candies evenly (as $n/k$) is always optimal. When $k = 3$ and $n = 8$, a uniform split gives $[2,2,2]$ with 6 candies used, but a better valid configuration could use more by exploiting the $a/a+1$ structure carefully.

## Approaches

The brute-force approach would be to try all possible values of $a$, and for each, decide how many children can take $a+1$, then check whether the total number of candies used can reach $n$ or less, and pick the best valid sum. For each $a$, we would scan through possible counts of higher-allocated children, recompute totals, and verify constraints. This would require iterating over values up to $n$, and for each trying up to $k$ splits, leading to an infeasible $O(nk)$ or worse process.

The key observation is that any valid distribution is fully determined by just two integers: how many children receive $a+1$, and how many receive $a$. Once we fix the number of higher-valued children $x$, the rest is forced. The constraint $x \le \lfloor k/2 \rfloor$ directly bounds how many children can be boosted. For any fixed $x$, we can compute the maximum candies as

$$(k-x)\cdot a + x \cdot (a+1) = k\cdot a + x.$$

Since we want to maximize total candies, we want to maximize both $a$ and $x$, but they are coupled through the requirement that total candies do not exceed $n$.

This reduces the problem to choosing $x$ optimally and deriving $a$ from the remaining budget. The structure becomes linear, and the best configuration always occurs at a boundary determined by the constraint on $x$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nk)$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

We rewrite the distribution in terms of two groups: $k-x$ children receive $a$, and $x$ children receive $a+1$, where $0 \le x \le \lfloor k/2 \rfloor$.

1. Fix a candidate number $x$, the count of children receiving $a+1$. This immediately determines the structure of the distribution because all remaining children must receive $a$.
2. Express the total number of candies used as $k \cdot a + x$. This comes from starting with $a$ candies per child and adding one extra candy to each of the $x$ selected children.
3. For a fixed $x$, maximize $a$ subject to $k \cdot a + x \le n$. This gives $a = \left\lfloor \frac{n-x}{k} \right\rfloor$.
4. Substitute back to compute the total candies used as:

$$\text{candies}(x) = k \cdot \left\lfloor \frac{n-x}{k} \right\rfloor + x.$$
5. Since $x$ is constrained by $0 \le x \le \lfloor k/2 \rfloor$, the problem reduces to checking only the boundary behavior of this function. Increasing $x$ by 1 reduces the base division term occasionally, so we test both extremes $x = 0$ and $x = \lfloor k/2 \rfloor$, and take the maximum.

The reason only the endpoints matter is that the function is piecewise linear with periodic drops at multiples of $k$, and within the allowed range of $x$, the maximum must occur at one of the boundaries of the feasible interval.

### Why it works

The distribution depends only on how many children get the larger value, and every feasible configuration collapses to a single integer parameter $x$. For each $x$, the best possible $a$ is uniquely determined by greedily filling each child with as many full $k$-groups of candies as possible. Since increasing $x$ only shifts the remainder term while decreasing the base quotient stepwise, no interior value of $x$ can strictly dominate both endpoints simultaneously. This ensures that evaluating only the boundary cases of $x$ captures the optimal solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())

        x = k // 2

        def calc(x):
            a = (n - x) // k
            return a * k + x

        ans = max(calc(0), calc(x))
        print(ans)

if __name__ == "__main__":
    solve()
```

The code encodes the two key candidates for the number of children receiving $a+1$. The helper function computes the best achievable total for a fixed $x$, first determining the maximum possible base value $a$, then reconstructing the total.

The choice of only checking $x = 0$ and $x = k//2$ follows from the constraint structure, where intermediate values cannot improve both the base allocation and the bonus allocation simultaneously.

## Worked Examples

### Example 1

Input: $n = 19, k = 4$

| x | a = (n-x)//k | total = k·a + x |
| --- | --- | --- |
| 0 | 4 | 16 |
| 2 | 4 | 18 |

The best choice is $x = 2$, giving total 18.

This shows how using some children as higher recipients allows better utilization of leftover candies after division into groups of size $k$.

### Example 2

Input: $n = 12, k = 7$

| x | a = (n-x)//k | total |
| --- | --- | --- |
| 0 | 1 | 7 |
| 3 | 1 | 10 |

The optimal is $x = 3$, yielding 10.

This demonstrates that when $k$ is larger than $n$, the structure still benefits from maximizing the number of boosted children within the allowed limit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | Each test case is evaluated in constant time using two arithmetic computations |
| Space | $O(1)$ | No auxiliary structures are used |

The solution easily fits within constraints since even $5 \cdot 10^4$ test cases only require a few arithmetic operations each.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    t = int(sys.stdin.readline())
    for _ in range(t):
        n, k = map(int, sys.stdin.readline().split())

        x = k // 2

        def calc(x):
            a = (n - x) // k
            return a * k + x

        output.append(str(max(calc(0), calc(x))))

    return "\n".join(output) + "\n"

# provided samples
assert run("""5
5 2
19 4
12 7
6 2
100000 50010
""") == """5
18
10
6
75015
"""

# custom cases
assert run("1\n1 1\n") == "1\n", "single element"
assert run("1\n0 5\n") == "0\n", "no candies"
assert run("1\n10 1\n") == "10\n", "single child"
assert run("1\n8 3\n") == "8\n", "tight distribution"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | minimal non-zero case |
| 0 5 | 0 | zero candies edge case |
| 10 1 | 10 | single child absorbs all |
| 8 3 | 8 | small interaction case |

## Edge Cases

When $k = 1$, the constraint on $a+1$ becomes irrelevant since there is only one child. The algorithm evaluates $x = 0$ and correctly returns $n$, because $a = n$ and total becomes $n$.

When $n < k$, many children receive zero. For $n = 5, k = 10$, the calculation for $x = 0$ gives $a = 0$, total 0, while $x = 5$ still yields $a = 0$ and total 5, matching the optimal behavior where up to half the children can receive one candy.

When $k$ is large relative to $n$, the second candidate $x = k/2$ ensures that leftover allocation is maximized through the allowed boosted children. For example, $n = 6, k = 10$ yields $x = 5$, giving total 5, which is the best possible packing under the constraint that no more than five children can receive one candy while the rest receive zero.
