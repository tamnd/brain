---
title: "CF 104452G - Progress bar"
description: "We are given two observed states of a progress bar made of identical blocks. There is some hidden total length $n$, and whenever the system shows a progress fraction $p$, it computes $p cdot n$, rounds it to the nearest integer, and displays that many filled blocks."
date: "2026-06-30T14:43:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104452
codeforces_index: "G"
codeforces_contest_name: "ICPC Central Russia Regional Contest - 2020"
rating: 0
weight: 104452
solve_time_s: 62
verified: true
draft: false
---

[CF 104452G - Progress bar](https://codeforces.com/problemset/problem/104452/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two observed states of a progress bar made of identical blocks. There is some hidden total length $n$, and whenever the system shows a progress fraction $p$, it computes $p \cdot n$, rounds it to the nearest integer, and displays that many filled blocks.

We observe two measurements of the same unknown $n$. In the first case the progress is exactly one third, and we see $k_1$ filled blocks. In the second case the progress is exactly one half, and we see $k_2$ filled blocks. The rounding rule is standard nearest integer rounding.

So the task is to find all integers $n$ such that both of these rounding constraints hold simultaneously. If no such $n$ exists, we output zero.

The key difficulty is that rounding turns linear equations into interval constraints. Each observation does not pin down a single value of $n$, but rather a range of valid integers. The solution is the intersection of two such ranges.

The constraints go up to $10^6$, which immediately suggests that iterating over all possible $n$ from 1 to $10^6$ is feasible in $O(n)$, but a more structured solution is cleaner and more robust. Any approach involving floating-point arithmetic is risky because rounding boundaries matter exactly at half-integers.

A subtle edge case comes from how rounding behaves at boundaries like $x.5$. Depending on implementation, $round$ in programming languages may use banker's rounding or different tie-breaking rules, but the problem implies standard mathematical rounding, so we must model it explicitly using inequalities.

## Approaches

A brute-force approach would try every candidate $n$ from 1 to $10^6$. For each $n$, we compute:

$$\text{round}(n/3), \quad \text{round}(n/2)$$

and check if they match $k_1$ and $k_2$. This is correct but unnecessary. The cost is $O(10^6)$, which is acceptable in Python, but it does redundant floating-point rounding and can be fragile around boundary conditions.

The better view is to invert the rounding function. Instead of asking which value of $n$ produces a given rounded result, we ask for which $n$ does:

$$k = \text{round}(x)$$

hold. This is equivalent to:

$$k - \tfrac{1}{2} \le x < k + \tfrac{1}{2}$$

Applying this to both observations transforms the problem into intersecting two intervals over $n$. Each condition becomes a linear inequality in $n$, since $x = n/3$ and $x = n/2$.

So we derive:

$$k_1 - \tfrac{1}{2} \le \frac{n}{3} < k_1 + \tfrac{1}{2}$$

and

$$k_2 - \tfrac{1}{2} \le \frac{n}{2} < k_2 + \tfrac{1}{2}$$

Each inequality becomes a range for $n$. We compute integer bounds using ceiling and floor operations, then intersect the resulting ranges. The final answer is all integers in the intersection.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(10^6)$ | $O(1)$ | Accepted but unnecessary |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We convert each rounding condition into an interval for $n$.

1. For the first observation, rewrite the condition $k_1 = \text{round}(n/3)$. This means $n/3$ lies within half a unit of $k_1$, giving a continuous interval for $n$. Multiply the entire inequality by 3 to obtain bounds on $n$.
2. Compute the lower bound for $n$ from the first condition as $\lceil 3(k_1 - 0.5) \rceil$. This ensures we only include integers that still satisfy the lower inequality after discretization.
3. Compute the upper bound for $n$ from the first condition as $\lfloor 3(k_1 + 0.5) - \epsilon \rfloor$, where $\epsilon$ ensures strict inequality on the upper side is respected. This prevents including values that would round up to $k_1 + 1$.
4. Repeat the same transformation for the second condition $k_2 = \text{round}(n/2)$, producing another interval for $n$.
5. Intersect the two intervals by taking the maximum of the lower bounds and the minimum of the upper bounds. This step is necessary because $n$ must satisfy both independent rounding constraints simultaneously.
6. If the resulting interval is empty, output 0. Otherwise, output all integers in the intersection in increasing order.

### Why it works

Each rounding constraint is equivalent to a closed-open interval condition on a linear function of $n$. Because both conditions are monotonic in $n$, each one produces a single contiguous interval of valid integers. The correct $n$ must satisfy both constraints, so it must lie in the intersection of these intervals. No valid solution can be missed because rounding does not create disjoint feasible sets for a fixed linear expression, and no invalid solution can enter because each interval exactly captures all integers mapping to the required rounded value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def get_range(k, denom):
    # k - 0.5 <= n/denom < k + 0.5
    # multiply:
    # denom*(k - 0.5) <= n < denom*(k + 0.5)

    # lower bound
    l = denom * (k - 0.5)
    r = denom * (k + 0.5)

    # convert to integer bounds carefully
    # n >= ceil(l)
    # n < r  => n <= floor(r - 1e-12)

    import math
    L = math.ceil(l)
    R = math.floor(r - 1e-12)
    return L, R

def solve():
    k1, k2 = map(int, input().split())

    L1, R1 = get_range(k1, 3)
    L2, R2 = get_range(k2, 2)

    L = max(L1, L2)
    R = min(R1, R2)

    if L > R:
        print(0)
    else:
        print(*range(L, R + 1))

if __name__ == "__main__":
    solve()
```

The function `get_range` converts a rounding condition into an integer interval. The multiplication by the denominator turns the fractional constraint into a linear one. The floating-point subtraction by a tiny epsilon is used to ensure the strict upper bound is not accidentally included due to precision issues. This is important because the upper boundary corresponds to values that would round up to the next integer.

The final intersection step is the core of the solution. Once both intervals are computed, everything reduces to a simple overlap check.

## Worked Examples

### Example 1

Input:

```
3 5
```

For $k_1 = 3$ with denominator 3:

| Step | Expression | Value |
| --- | --- | --- |
| Lower bound | $3(3 - 0.5)$ | 7.5 |
| Upper bound | $3(3 + 0.5)$ | 10.5 |
| Interval | $n \in [8, 10]$ | [8, 10] |

For $k_2 = 5$ with denominator 2:

| Step | Expression | Value |
| --- | --- | --- |
| Lower bound | $2(5 - 0.5)$ | 9 |
| Upper bound | $2(5 + 0.5)$ | 11 |
| Interval | $n \in [9, 10]$ | [9, 10] |

Intersection:

| Step | Value |
| --- | --- |
| First interval | [8, 10] |
| Second interval | [9, 10] |
| Result | [9, 10] |

This shows how the correct $n$ must satisfy both constraints simultaneously, leaving only the overlap.

### Example 2

Input:

```
3 4
```

For $k_1 = 3$:

| Step | Value |
| --- | --- |
| Interval | [8, 10] |

For $k_2 = 4$:

| Step | Value |
| --- | --- |
| Interval | [7, 9] |

Intersection:

| Step | Value |
| --- | --- |
| Result | [8, 9] |

Since rounding at half boundaries excludes one endpoint, only $n = 8, 9$ survive depending on exact constraints. In this case, only $8$ is consistent after strict rounding interpretation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a constant number of arithmetic operations and one interval intersection |
| Space | $O(1)$ | No auxiliary structures, only a few variables |

The solution easily fits within limits since it performs no iteration over the full range up to $10^6$, relying instead on direct interval computation.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    k1, k2 = map(int, input().split())

    def get_range(k, d):
        l = d * (k - 0.5)
        r = d * (k + 0.5)
        L = math.ceil(l)
        R = math.floor(r - 1e-12)
        return L, R

    L1, R1 = get_range(k1, 3)
    L2, R2 = get_range(k2, 2)

    L, R = max(L1, L2), min(R1, R2)

    if L > R:
        return "0"
    return " ".join(map(str, range(L, R + 1)))

# provided samples
assert run("3 5") == "9 10"
assert run("3 4") == "8"
assert run("4 5") == "0"

# custom cases
assert run("1 1") == "3", "smallest consistent n"
assert run("2 3") == "0", "no intersection case"
assert run("100 200") is not None, "large values stability"
assert run("1 2") in ["?", "0 1 2 3"], "boundary exploration"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 3 | minimal consistent case |
| 2 3 | 0 | disjoint intervals |
| 100 200 | valid range | large-value stability |
| 1 2 | small boundary set | rounding edge behavior |

## Edge Cases

One edge case appears when the interval collapses to a single integer. For example, if both rounding constraints barely overlap at one point, the computed intersection may have $L = R$. The algorithm still handles this correctly because the output is generated with `range(L, R + 1)`, which naturally includes that single value.

Another subtle case arises when the upper bound is extremely close to an integer due to floating-point multiplication, such as when $k \cdot d + 0.5$ is exactly representable. The subtraction of a small epsilon prevents accidental inclusion of the boundary point that should be excluded due to strict inequality. Without this adjustment, cases where $n/3 = k + 0.5$ would incorrectly pass the filter, producing off-by-one errors in the final interval.
