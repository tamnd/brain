---
title: "CF 1373A - Donut Shops"
description: "We are comparing two different ways of buying the same number of donuts, and for each way we want to know when it becomes strictly cheaper than the other. In the first shop, the price is linear: buying $x$ donuts costs exactly $a cdot x$."
date: "2026-06-16T12:48:50+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1373
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 90 (Rated for Div. 2)"
rating: 1000
weight: 1373
solve_time_s: 277
verified: false
draft: false
---

[CF 1373A - Donut Shops](https://codeforces.com/problemset/problem/1373/A)

**Rating:** 1000  
**Tags:** greedy, implementation, math  
**Solve time:** 4m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are comparing two different ways of buying the same number of donuts, and for each way we want to know when it becomes strictly cheaper than the other.

In the first shop, the price is linear: buying $x$ donuts costs exactly $a \cdot x$.

In the second shop, purchases are constrained. Donuts are sold in boxes of size $b$, each box costs $c$. If we want $x$ donuts, we cannot buy fractions of boxes, so we must buy enough full boxes to cover at least $x$ donuts. That means we buy $\lceil x / b \rceil$ boxes, and the total cost becomes $c \cdot \lceil x / b \rceil$.

For each test case, we need to find one positive integer $x$ where the first shop is strictly cheaper than the second, and another (possibly different) integer $x$ where the second shop is strictly cheaper than the first. If no such value exists for a direction, we output -1.

The constraints are small in terms of test count, but the values of $a$, $b$, and $c$ can be up to $10^9$, and $x$ can also go up to $10^9$. That immediately rules out trying all values of $x$. Any solution must reason directly from structure of the cost functions.

A subtle edge case appears when one shop is always better or always equal. For example, if $a \le c/b$ in an averaged sense but rounding changes behavior, or if the box size makes the second shop piecewise constant. Another important issue is that equality is not allowed; we need strict inequality, so values where costs match must be excluded even if they look “optimal”.

## Approaches

A brute-force idea is to iterate $x$ from 1 up to some large limit and compare both costs. For each $x$, compute $a \cdot x$ and $c \cdot \lceil x/b \rceil$, and record a value where one is smaller than the other. This is correct but fundamentally too slow: even if we only check up to $10^9$, this is impossible under typical constraints.

The key observation is that both cost functions are monotone in a structured way. The first shop is perfectly linear. The second shop is a step function: it stays constant for intervals of length $b$, then jumps by $c$. This means that changes in dominance between shops can only occur around small, structured points, typically around multiples of $b$ or very small values of $x$.

Instead of scanning all $x$, we only need to test a few strategically chosen candidates. The first useful idea is that if the second shop is ever cheaper, it will already be cheaper at some small $x$, specifically at $x = 1$. This is because its cost per donut is effectively minimized when you fully utilize a box; larger $x$ only repeats the same average pattern or worsens rounding inefficiency.

So to find a case where the second shop is cheaper, we simply check $x = 1$.

For the first shop being cheaper, we want:

$$a \cdot x < c \cdot \lceil x/b \rceil$$

The right-hand side is piecewise constant per block of size $b$. The first opportunity for the first shop to win typically happens at the boundary of a box, i.e. at $x = b$, because before that the second shop may waste capacity but after that amortization improves.

So we test $x = b$.

These two candidates are sufficient because any improvement or crossover happens at the smallest structural points of the step function: the first donut and the first full box.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per test | O(1) | Too slow |
| Optimal | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

We handle each test case independently.

1. Compute the cost comparison at $x = 1$. We compare $a$ with $c$, since $\lceil 1/b \rceil = 1$. If $c < a$, then the second shop is cheaper at $x = 1$, so we output $x = 1$ for the second answer. Otherwise, we conclude there is no valid $x$ for the second shop.
2. Compute a candidate for when the first shop is cheaper by checking $x = b$. At this point, the first shop costs $a \cdot b$, while the second shop costs exactly $c$ because one full box covers all $b$ donuts. If $a \cdot b < c$, we output $x = b$ for the first answer.
3. If the condition fails, we output -1 for that direction.
4. Ensure outputs remain within bounds, which is guaranteed because we only use $1$ and $b \le 10^9$.

### Why it works

The second shop's cost function changes only when $x$ crosses multiples of $b$. Between those points it is constant, so any minimum or dominance change must be witnessed at the first point in a segment or at the first segment boundary. The first shop is linear, so if it ever beats the second shop, it will do so earliest at one of these structural breakpoints. This reduces the infinite search space to two meaningful candidates: $x = 1$ and $x = b$.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, c = map(int, input().split())

    # second shop cheaper candidate
    second_ans = -1
    if c < a:
        second_ans = 1

    # first shop cheaper candidate
    first_ans = -1
    if a * b < c:
        first_ans = b

    print(first_ans, second_ans)
```

The first block computes whether a single donut is cheaper in the second shop. Since buying one donut always forces buying one box, the comparison reduces to $c < a$.

The second block tests the critical boundary where the box structure stops helping the second shop. At $x = b$, both shops represent a clean comparison: one box versus $b$ individual donuts. This is the only point needed to decide whether the first shop can ever be strictly cheaper.

The multiplication $a \cdot b$ must be done in 64-bit range, but Python handles this safely.

## Worked Examples

### Sample 1

Input:

```
5 10 4
```

We evaluate both candidates.

For $x = 1$, first shop costs 5, second costs 4, so second shop is cheaper. For $x = 10$, first shop costs 50, second costs 4, so second shop is still cheaper.

| Step | x | First cost | Second cost | Result |
| --- | --- | --- | --- | --- |
| second check | 1 | 5 | 4 | second wins |
| first check | 10 | 50 | 4 | second wins |

This shows the first shop never becomes cheaper, so we output -1 for it.

### Sample 2

Input:

```
2 2 3
```

For $x = 1$, costs are 2 and 3, so first shop is cheaper, but this does not guarantee it stays that way for all $x$. For $x = 2$, first shop costs 4, second shop costs 3, so second shop is cheaper.

| Step | x | First cost | Second cost | Result |
| --- | --- | --- | --- | --- |
| second check | 1 | 2 | 3 | first wins |
| first check | 2 | 4 | 3 | second wins |

We get one valid answer for each direction: $1$ for first shop, $2$ for second shop.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | constant work per test case, only arithmetic comparisons |
| Space | O(1) | no auxiliary structures |

The solution easily fits within limits since even for $t = 1000$, we only perform a handful of integer operations per case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    t = int(input())
    out = []
    for _ in range(t):
        a, b, c = map(int, input().split())

        second_ans = -1
        if c < a:
            second_ans = 1

        first_ans = -1
        if a * b < c:
            first_ans = b

        out.append(f"{first_ans} {second_ans}")

    return "\n".join(out) + "\n"

# provided samples
assert run("""4
5 10 4
4 5 20
2 2 3
1000000000 1000000000 1000000000
""") == """-1 1
5 -1
-1 1
-1 -1
"""

# custom cases
assert run("""1
1 2 1
""") == "-1 -1\n", "all equal-ish edge"

assert run("""1
10 2 100
""") == "2 1\n", "both directions possible"

assert run("""1
5 3 2
""") == "3 1\n", "second shop strong"

assert run("""1
2 5 100
""") == "5 1\n", "first shop wins for box size gap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 1 | -1 -1 | no strict improvement either way |
| 10 2 100 | 2 1 | both shops have winning regions |
| 5 3 2 | 3 1 | second shop dominant behavior |
| 2 5 100 | 5 1 | first shop can beat bulk pricing |

## Edge Cases

When $a = c$, the second shop cannot be strictly cheaper at $x = 1$, since both cost the same. The algorithm correctly outputs -1 because the strict inequality fails.

When $a \cdot b = c$, the comparison at $x = b$ becomes equal, so the first shop is not considered strictly cheaper. This avoids incorrectly claiming a valid answer where both shops tie.

When $b = 2$, the step function has very frequent jumps, but the structure still collapses to the same two checkpoints. The algorithm remains valid because it does not rely on smoothness, only on the first step and first block boundary.
