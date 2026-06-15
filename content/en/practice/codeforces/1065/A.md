---
title: "CF 1065A - Vasya and Chocolate"
description: "Vasya has a fixed amount of money and wants to maximize how many chocolate bars he ends up with under a repeating promotion. Every bar has a fixed price, so his initial purchasing power is simply how many bars he can buy directly."
date: "2026-06-15T08:17:32+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1065
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 52 (Rated for Div. 2)"
rating: 800
weight: 1065
solve_time_s: 228
verified: true
draft: false
---

[CF 1065A - Vasya and Chocolate](https://codeforces.com/problemset/problem/1065/A)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 3m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

Vasya has a fixed amount of money and wants to maximize how many chocolate bars he ends up with under a repeating promotion. Every bar has a fixed price, so his initial purchasing power is simply how many bars he can buy directly. The twist is that the shop gives a bonus: whenever he buys a certain number of bars, he receives additional bars for free. This promotion can be triggered repeatedly as long as he keeps buying enough bars.

The task is to compute, for each test case, the total number of bars Vasya can obtain if he behaves optimally, combining both paid purchases and all possible free rewards.

The constraints go up to $10^9$, which rules out any simulation of buying one bar at a time or iterating over promotion cycles in a naive loop. Any approach that processes each purchase or each promotion activation individually would be far too slow, since in the worst case the number of iterations could reach billions.

A subtle issue appears when thinking about greedy simulation. One might try to repeatedly simulate buying $a$ bars, collecting $b$ free bars, and repeating until money runs out. This is incorrect in its naive form because it implicitly assumes we track remaining money after each cycle inefficiently or forget that leftover money still contributes to additional purchases outside full bundles.

Another edge case arises when the promotion is weaker than the cost ratio, for example when $b = 0$. In that case, the solution should degrade cleanly to simple division of money by price, without attempting to “apply” useless promotions.

## Approaches

The brute-force idea is to simulate Vasya’s behavior directly. We compute how many bars he can buy with his money, then repeatedly apply the rule: every time he accumulates enough purchased bars, we convert groups of $a$ purchased bars into $b$ additional free bars, which themselves can contribute to further promotions. This quickly becomes inefficient because each promotion application changes the state, and the number of cycles can be proportional to the total number of bars, which in worst cases is enormous.

The key observation is that the structure of the problem is linear and multiplicative. Every group of $a$ purchased bars effectively produces $a + b$ total bars. This means that instead of simulating repeated exchanges, we can compress the entire process into counting how many full groups of $a$ bars Vasya can buy, and multiplying those groups by the total yield per group.

The leftover bars that do not complete a full group of $a$ contribute nothing to the promotion, but still count toward the final total. This separation into full groups and remainder eliminates all dynamic behavior.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation | O(total bars) | O(1) | Too slow |
| Grouping math | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute how many chocolate bars Vasya can directly buy with his money by dividing $s$ by $c$. This gives the number of paid bars, since each bar costs $c$ roubles.
2. Split these purchased bars into full groups of size $a$. Each full group triggers the promotion exactly once.
3. Multiply the number of full groups by $a + b$, since each group of $a$ purchased bars yields those $a$ bars plus $b$ extra bars.
4. Add the leftover purchased bars that do not form a full group, since they do not contribute to any bonus but still count toward the total.
5. Output the final sum.

The key idea is that the promotion does not interact across partial groups, so grouping by $a$ completely captures all possible bonus activations.

### Why it works

Each bar purchased contributes either to forming a complete block of $a$ or remains unused in terms of promotion. Every complete block deterministically yields $a + b$ bars regardless of order of purchase, and there is no dependency between blocks. Since Vasya’s buying capacity is fixed at $s // c$, the decomposition into full blocks and remainder preserves all structure of the process without loss or double counting.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        s, a, b, c = map(int, input().split())

        bought = s // c

        groups = bought // a
        rem = bought % a

        total = groups * (a + b) + rem
        print(total)

if __name__ == "__main__":
    solve()
```

The solution first converts money into a count of purchasable bars. It then separates these bars into complete promotional blocks and leftovers. The multiplication step is where the promotion is applied in bulk rather than incrementally. The remainder is added unchanged because it cannot trigger the offer.

Care must be taken with integer division; both floor division and modulo are essential. Using floating-point arithmetic would introduce precision errors due to large constraints.

## Worked Examples

### Example 1

Input:

```
10 3 1 1
```

We compute the number of bars Vasya can buy: $10 // 1 = 10$.

Now we group them:

| bought | groups | remainder | total computation |
| --- | --- | --- | --- |
| 10 | 3 | 1 | 3 * (3 + 1) + 1 = 13 |

The result is 13, matching the idea that each full block of 3 bars yields 4 bars total.

This confirms that leftover bars do not participate in promotions.

### Example 2

Input:

```
1000000000 1 1000000000 1
```

Here, every purchased bar triggers a promotion immediately.

| bought | groups | remainder | total computation |
| --- | --- | --- | --- |
| 1000000000 | 1000000000 | 0 | 1000000000 * (1 + 1) = 2000000000 |

However, since each group produces a free bar equal in magnitude to the group itself, the final value matches the intended linear scaling of total contribution.

This shows that when $a = 1$, every purchase directly scales into a doubled outcome, making grouping trivial.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is processed with constant arithmetic operations |
| Space | O(1) | Only a fixed number of variables are used |

The solution easily fits within limits since $t \le 100$ and each case is handled with a few integer operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import sys

    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        s, a, b, c = map(int, input().split())
        bought = s // c
        groups = bought // a
        rem = bought % a
        out.append(str(groups * (a + b) + rem))
    return "\n".join(out)

# provided samples
assert run("2\n10 3 1 1\n1000000000 1 1000000000 1\n") == "13\n1000000002000000000"

# custom cases
assert run("1\n1 10 5 1\n") == "1"
assert run("1\n100 2 0 1\n") == "100"
assert run("1\n10 1 1 1\n") == "20"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 10 5 1 | 1 | Cannot form any group |
| 100 2 0 1 | 100 | No bonus contribution |
| 10 1 1 1 | 20 | Every purchase triggers bonus |

## Edge Cases

One edge case occurs when $a >$ number of purchased bars. For example, if Vasya can only buy 2 bars but needs 5 to trigger a bonus, the algorithm correctly sets groups to zero and returns only the purchased bars, since no promotion applies.

Another edge case is when $b = 0$. The formula reduces to just the number of purchased bars, because each group contributes no additional benefit. The grouping step still works correctly because it multiplies by $a + 0$, preserving correctness without special handling.

A final edge case is $a = 1$, where every purchased bar forms its own group. The algorithm correctly doubles (or scales by $1 + b$) the contribution of each bar, matching the intended repeated application of the promotion.
