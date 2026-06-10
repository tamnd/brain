---
title: "CF 1525A - Potion-making"
description: "We are tasked with creating a potion that contains exactly $k%$ magic essence and $(100-k)%$ water. The cauldron starts empty, and we can only add one liter at a time of either ingredient."
date: "2026-06-10T17:32:26+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1525
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 109 (Rated for Div. 2)"
rating: 800
weight: 1525
solve_time_s: 587
verified: true
draft: false
---

[CF 1525A - Potion-making](https://codeforces.com/problemset/problem/1525/A)

**Rating:** 800  
**Tags:** math, number theory  
**Solve time:** 9m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are tasked with creating a potion that contains exactly $k\%$ magic essence and $(100-k)\%$ water. The cauldron starts empty, and we can only add one liter at a time of either ingredient. The goal is to determine the minimum number of liters we must pour to achieve the exact ratio. The input provides a number of test cases $t$, each specifying the desired percentage $k$, and the output must give the minimal number of total liters for each.

The key observation is that the potion's ratio only depends on the relative counts of essence and water, not on the absolute volume. Therefore, the problem reduces to finding the smallest integers $e$ and $w$ such that 

$$\frac{e}{e + w} = \frac{k}{100}.$$

We can rewrite this as $100 \cdot e = k \cdot (e + w)$, which leads to $100e - k(e + w) = 0$, or equivalently $e \cdot (100 - k) = w \cdot k$. This is a linear Diophantine equation in integers $e$ and $w$. 

The constraints are small, $1 \le k \le 100$ and $t \le 100$, so an $O(1)$ arithmetic solution per test case is sufficient. Edge cases occur when $k$ divides 100 evenly (e.g., $k = 25, 50, 100$) and when $k$ is coprime with 100 (e.g., $k = 3, 7$). A naive solution that tests all volumes up to 100 would work but is unnecessary given the existence of a simple number-theoretic formula.

## Approaches

The brute-force approach would iterate through all possible volumes $e + w$ starting from 1, checking whether the fraction $e/(e+w)$ equals $k/100$. For $k = 1$ or $k = 99$, this could require up to 100 steps, which is acceptable but not elegant.

The optimal approach uses greatest common divisor reasoning. If $g = \gcd(k, 100)$, then $k = g \cdot k'$ and $100 = g \cdot 100'$. The minimal total liters that satisfy the ratio is exactly $100/g$, since 

$$\frac{e}{e+w} = \frac{k}{100} = \frac{k'}{100'}$$ 

and the smallest integers in that ratio are $e = k'$ and $w = 100' - k'$, giving $e + w = k' + (100' - k') = 100' = 100/g$. This yields an immediate formula without iteration.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | O(100) per test case | O(1) | Accepted but unnecessary |
| Optimal | O(log 100) per test case | O(1) | Accepted and elegant |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read the percentage $k$.
3. Compute the greatest common divisor $g = \gcd(k, 100)$. This identifies the largest factor that can reduce both numerator and denominator.
4. Compute the minimal number of total liters as $100/g$. This corresponds to the smallest integers $e$ and $w$ that satisfy the ratio.
5. Print the result for the test case.

Why it works: By reducing the fraction $k/100$ to lowest terms, we find the smallest integer ratio that maintains the exact percentage. The sum of the numerator and denominator of this reduced fraction gives the minimal total volume. No smaller integer combination can satisfy the exact ratio because any smaller sum would violate the reduced fraction property.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    k = int(input())
    g = math.gcd(k, 100)
    print(100 // g)
```

The solution reads each test case, computes the greatest common divisor, and outputs the minimal total volume. The choice of integer division ensures we obtain the exact number of liters. Python's built-in `math.gcd` handles all edge cases automatically, including $k = 100$ and $k = 1$.

## Worked Examples

**Example 1:** $k = 3$

| Variable | Value |
|---|---|
| k | 3 |
| gcd(k,100) | 1 |
| 100 / gcd(k,100) | 100 |

We need 3 liters of essence and 97 liters of water, totaling 100 liters. This confirms the minimal total is 100.

**Example 2:** $k = 25$

| Variable | Value |
|---|---|
| k | 25 |
| gcd(k,100) | 25 |
| 100 / gcd(k,100) | 4 |

The minimal combination is 1 liter of essence and 3 liters of water, totaling 4 liters. The algorithm correctly computes the smallest volume.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(t * log 100) | gcd computation per test case takes O(log 100) |
| Space | O(1) | only a few integers stored per test case |

Given $t \le 100$, this fits well within time and memory limits.

## Test Cases

```python
import sys, io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        k = int(input())
        g = math.gcd(k, 100)
        output.append(str(100 // g))
    return "\n".join(output)

# Provided samples
assert run("3\n3\n100\n25\n") == "100\n1\n4", "sample 1"

# Custom tests
assert run("3\n1\n50\n99\n") == "100\n2\n100", "edge and half values"
assert run("2\n2\n10\n") == "50\n10", "small divisors"
assert run("2\n33\n66\n") == "100\n50", "nontrivial gcd"
```

| Test input | Expected output | What it validates |
|---|---|---|
| 1,50,99 | 100,2,100 | smallest, half, large coprime |
| 2,10 | 50,10 | small divisors |
| 33,66 | 100,50 | gcd not trivial |

## Edge Cases

When $k = 100$, the gcd is 100, and 100/100 = 1, confirming that pouring a single liter suffices. When $k = 1$, gcd(1,100) = 1, and the algorithm correctly outputs 100 liters. The formula automatically handles percentages that divide 100 evenly and those that are coprime with 100, guaranteeing correctness in all boundary conditions.
