---
title: "CF 415B - Mashmokh and Tokens"
description: "Each day Mashmokh receives a pile of tokens, and at the end of that day he can exchange some of them for money using a fixed conversion rule. If he returns $w$ tokens, the money he gets depends only on how many full “blocks” of size $a$ are contained in a linear function of $w$."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 415
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 240 (Div. 2)"
rating: 1500
weight: 415
solve_time_s: 67
verified: true
draft: false
---

[CF 415B - Mashmokh and Tokens](https://codeforces.com/problemset/problem/415/B)

**Rating:** 1500  
**Tags:** binary search, greedy, implementation, math  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

Each day Mashmokh receives a pile of tokens, and at the end of that day he can exchange some of them for money using a fixed conversion rule. If he returns $w$ tokens, the money he gets depends only on how many full “blocks” of size $a$ are contained in a linear function of $w$. The exact mapping is linear and then floored, so fractional progress toward the next unit of money is worthless.

The key goal is not to maximize tokens converted directly, but to maximize money while saving as many tokens as possible. Since unused tokens do not carry over to future days, each day is independent, and we only need to decide how many tokens to exchange that day to reach the maximum possible monetary value.

The input gives $n$ days, parameters $a$ and $b$, and an array $x_i$ describing how many tokens are available each day. The output for each day is how many tokens can be saved after choosing an optimal exchange amount.

The constraint $n \le 10^5$ forces an $O(n)$ or $O(n \log n)$ solution. Anything involving per-day simulation over all possible token choices would be too slow since $x_i$ can be as large as $10^9$, making brute force infeasible.

A subtle edge case appears when $x_i$ is very small compared to $a$. For example, if $x_i < a$, no exchange might be possible depending on the formula, and a naive greedy assumption like “use all tokens” would fail. Another edge case is when $x_i$ lies exactly on a multiple boundary where increasing exchanged tokens does not increase money, meaning saving one extra token is always optimal.

## Approaches

A direct approach is to try every possible number of tokens $w$ from $0$ to $x_i$, compute the resulting money, and pick the best one while maximizing leftover tokens among ties. This is correct but extremely slow. For each day we would do $O(x_i)$ work, which in the worst case becomes $O(n \cdot 10^9)$, completely impossible.

The structure of the money function is the crucial observation. The money depends only on $\left\lfloor \frac{a \cdot w}{b} \right\rfloor$, so the value increases only at discrete thresholds of $w$. Between two consecutive thresholds, increasing $w$ does not change the money. This means we never need to consider all values of $w$, only the smallest $w$ that achieves the maximum possible integer value under the constraint $w \le x_i$.

For a fixed $x_i$, the optimal strategy is to compute the maximum money obtainable by using all tokens, then find the minimum number of tokens needed to achieve that same money level. The difference between $x_i$ and that minimal requirement is exactly the number of tokens that can be saved.

This turns the problem into a simple arithmetic transformation per day.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(\sum x_i)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We focus on a single day with $x$ tokens.

1. Compute the maximum money achievable if all tokens are used. This is $k = \left\lfloor \frac{a \cdot x}{b} \right\rfloor$. This value represents the best possible integer reward level for the day.
2. Interpret $k$ backwards: determine the smallest number of tokens $w$ such that $\left\lfloor \frac{a \cdot w}{b} \right\rfloor = k$. This ensures we hit the same reward level without wasting tokens.
3. Solve the inequality

$$k \le \frac{a \cdot w}{b} < k+1$$

which rearranges to

$$\frac{k \cdot b}{a} \le w < \frac{(k+1)\cdot b}{a}$$

1. The smallest integer $w$ satisfying this is

$$w_{\min} = \left\lceil \frac{k \cdot b}{a} \right\rceil$$

1. The number of saved tokens is simply $x - w_{\min}$.

Each day is independent, so we repeat this computation for all inputs.

### Why it works

The key invariant is that the money function partitions the integer line into contiguous intervals where every value in the interval produces the same reward. Within each interval, spending more tokens does not improve the outcome. Therefore, the optimal strategy is always to select the left boundary of the interval corresponding to the maximum achievable reward under the constraint $w \le x$. This guarantees maximal savings because any larger $w$ would not increase reward, and any smaller $w$ would reduce it.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, a, b = map(int, input().split())
    xs = list(map(int, input().split()))
    
    for x in xs:
        k = (a * x) // b
        w_min = (k * b + a - 1) // a
        print(x - w_min, end=' ')
        
solve()
```

The solution computes the best achievable reward level $k$ using all tokens. It then reconstructs the smallest number of tokens required to reach that same reward using a ceiling division trick: $(k \cdot b + a - 1) // a$. Subtracting this from $x$ gives the maximum number of tokens that can be safely saved without reducing money.

Care must be taken with integer arithmetic. The multiplication $a \cdot x$ can reach $10^{18}$, but Python handles it safely. The ceiling division must be implemented carefully to avoid off-by-one errors.

## Worked Examples

### Example 1

Input:

```
5 1 4
12 6 11 9 1
```

We compute per day.

| x | k = floor(a·x/b) | w_min = ceil(k·b/a) | saved |
| --- | --- | --- | --- |
| 12 | 3 | 12 | 0 |
| 6 | 1 | 4 | 2 |
| 11 | 2 | 8 | 3 |
| 9 | 2 | 8 | 1 |
| 1 | 0 | 0 | 1 |

Output:

```
0 2 3 1 1
```

This confirms that savings come from trimming each value down to the smallest amount that preserves the same reward level.

### Example 2

Input:

```
3 2 3
5 4 1
```

| x | k = floor(a·x/b) | w_min | saved |
| --- | --- | --- | --- |
| 5 | 3 | 5 | 0 |
| 4 | 2 | 3 | 1 |
| 1 | 0 | 0 | 1 |

Output:

```
0 1 1
```

This example shows how different reward levels create different interval widths, but the same principle applies.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | each day uses constant arithmetic operations |
| Space | $O(1)$ | only input storage and a few integers |

The linear complexity is sufficient for $n \le 10^5$, and all operations are simple integer arithmetic, well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    input = sys.stdin.readline

    n, a, b = map(int, input().split())
    xs = list(map(int, input().split()))
    
    out = []
    for x in xs:
        k = (a * x) // b
        w_min = (k * b + a - 1) // a
        out.append(str(x - w_min))
    return " ".join(out)

# provided sample
assert run("5 1 4\n12 6 11 9 1\n") == "0 2 3 1 1"

# minimum input
assert run("1 1 1\n1\n") == "0"

# small boundary
assert run("3 2 3\n5 4 1\n") == "0 1 1"

# all equal
assert run("4 3 5\n10 10 10 10\n") == "0 0 0 0"

# large values
assert run("2 1000000000 1000000000\n1000000000 999999999\n") == "0 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 / 1 | 0 | smallest case |
| 3 2 3 / 5 4 1 | 0 1 1 | boundary arithmetic |
| all equal | 0 0 0 0 | consistency |
| large values | 0 0 | overflow safety |

## Edge Cases

When $x_i$ is very small, such as $x_i = 1$, the computed reward level $k$ becomes zero. In that case, the minimal $w$ that achieves the same reward is also zero, so all tokens can be saved. The algorithm correctly handles this because $k = 0$ leads to $w_{\min} = 0$, producing full savings.

When $x_i$ is large and close to a boundary where increasing $w$ does not change $\left\lfloor \frac{a w}{b} \right\rfloor$, the computed $w_{\min}$ collapses to the nearest threshold. For example, if $a=1, b=4, x=6$, then $k=1$, and $w_{\min}=4$. The algorithm correctly saves $2$ tokens, matching the fact that spending beyond $4$ yields no additional benefit.

When $a$ and $b$ are equal, the function becomes $k = x$, and $w_{\min} = x$, so no tokens are saved. The algorithm naturally reduces to zero savings because every token contributes exactly one unit of reward.
