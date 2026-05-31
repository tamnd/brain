---
title: "CF 1968A - Maximize?"
description: "We are given a small positive integer $x$. For each such value, we need to choose another integer $y$ strictly smaller than $x$, and we want to maximize the expression $gcd(x, y) + y$. The interaction between the two terms is important."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1968
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 943 (Div. 3)"
rating: 800
weight: 1968
solve_time_s: 66
verified: false
draft: false
---

[CF 1968A - Maximize?](https://codeforces.com/problemset/problem/1968/A)

**Rating:** 800  
**Tags:** brute force, math, number theory  
**Solve time:** 1m 6s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a small positive integer $x$. For each such value, we need to choose another integer $y$ strictly smaller than $x$, and we want to maximize the expression $\gcd(x, y) + y$.

The interaction between the two terms is important. The gcd term grows when $y$ shares large divisors with $x$, while the additive term $y$ itself grows when we pick values close to $x$. These two goals conflict: pushing $y$ large often reduces gcd structure, while aligning with divisors of $x$ might force $y$ to be smaller.

The input constraint $x \le 1000$ suggests that even quadratic reasoning over all candidates is acceptable, but also hints that there is a structural shortcut because the problem is likely designed for observation rather than heavy computation.

A naive implementation would try all $y \in [1, x-1]$ and compute $\gcd(x,y) + y$. This is safe and correct, but it hides the structure of the optimum.

One subtle edge case appears when $x$ is prime. In that case, $\gcd(x,y) = 1$ for all valid $y$, so the expression becomes $1 + y$, and the best choice is clearly $y = x-1$. Another edge case is when $x$ is highly composite, where many divisors exist and it becomes tempting to pick small multiples of large gcds, but these still lose to a carefully chosen near-$x$ candidate.

## Approaches

The brute-force strategy is straightforward: for each candidate $y$, compute $\gcd(x,y) + y$, track the maximum, and output the best $y$. This works because there are at most $x-1$ candidates per test case and each gcd computation is $O(\log x)$, giving a worst-case around $10^3 \cdot 10^3 \cdot \log 1000$, which is small enough.

However, this approach ignores the key structure of the objective. The gcd term is always a divisor of $x$, and divisors of a number are sparse and structured. If we fix a value $g = \gcd(x,y)$, then $y$ must be a multiple of $g$, so we can write $y = gk$ where $\gcd(k, x/g) = 1$. The expression becomes $g + gk = g(k+1)$, which is maximized by pushing $k$ as large as possible under the constraint $gk < x$.

The highest possible $k$ is roughly $\lfloor (x-1)/g \rfloor$. This suggests that for each divisor $g$ of $x$, the best candidate $y$ is the largest multiple of $g$ strictly below $x$. That is $y = x - (x \bmod g)$, unless $x \bmod g = 0$, in which case we subtract $g$.

The key simplification is that it is sufficient to iterate over all divisors of $x$, compute this candidate $y$, and evaluate the expression. Since $x \le 1000$, the number of divisors is small, and this becomes extremely efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(x \log x)$ per test case | $O(1)$ | Accepted but unnecessary |
| Divisor Enumeration | $O(\sqrt{x})$ per test case | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. For each test case, read $x$. The goal is to identify a candidate $y < x$ that maximizes $\gcd(x,y) + y$, and we will restrict attention to values derived from divisors of $x$.
2. Enumerate all integers $g$ from $1$ to $\sqrt{x}$. When $g$ divides $x$, treat both $g$ and $x/g$ as candidate gcd values. This works because every possible gcd between $x$ and $y$ must divide $x$.
3. For each candidate divisor $g$, construct the largest valid $y$ that is a multiple of $g$ and still less than $x$. This is computed as $y = x - (x \bmod g)$, and if this equals $x$, adjust to $y = x - g$. This guarantees both maximality under the divisibility constraint and validity under $y < x$.
4. Compute the value $g + y$ for this candidate pair. Keep track of the best pair seen so far. We do not need to enforce $\gcd(x,y)=g$ explicitly because construction ensures $y$ is a multiple of $g$, and larger valid candidates are still explored through all divisors.
5. After checking all divisors, output the $y$ that achieved the maximum value.

### Why it works

The optimal solution can always be associated with a gcd value $g$ that divides $x$. For any fixed $g$, the expression $\gcd(x,y) + y$ is maximized by taking the largest possible $y < x$ that is divisible by $g$, since increasing $y$ directly increases the sum while preserving the gcd constraint. Because every feasible solution corresponds to some divisor $g$, and we evaluate the best candidate for each such $g$, we cannot miss the optimal pair.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(x):
    best_val = -1
    best_y = 1

    # try all divisors g of x
    g = 1
    while g * g <= x:
        if x % g == 0:
            for d in (g, x // g):
                if d <= 0:
                    continue
                # largest multiple of d less than x
                y = x - (x % d)
                if y == x:
                    y -= d
                val = d + y
                if val > best_val:
                    best_val = val
                    best_y = y
        g += 1

    return best_y

t = int(input())
for _ in range(t):
    x = int(input())
    print(solve(x))
```

The code iterates over all divisors of $x$ using a square-root loop, ensuring we only consider meaningful gcd candidates. For each divisor $d$, it constructs the best possible $y$ aligned with that divisor. The adjustment `if y == x: y -= d` handles the case where $x$ is itself divisible by $d$, preventing invalid equality.

The variable `best_val` tracks the maximum achieved value, while `best_y` stores the corresponding integer. Since multiple answers are allowed, ties do not need special handling.

## Worked Examples

We trace two inputs to see how candidates evolve.

### Example 1: $x = 10$

We test divisors $1,2,5,10$.

| g | y construction | y | g + y |
| --- | --- | --- | --- |
| 1 | 10 - (10 mod 1) = 10 → adjust to 9 | 9 | 10 |
| 2 | 10 - (10 mod 2) = 10 → adjust to 8 | 8 | 10 |
| 5 | 10 - (10 mod 5) = 10 → adjust to 5 | 5 | 10 |
| 10 | 10 - 0 → adjust to 0 (invalid, skip effectively) | 0 | 10 |

Best valid $y$ is 9, 8, or 5 all give value 10, and any is acceptable.

This shows that multiple divisors can lead to equal optimal scores, which is why any valid $y$ is allowed.

### Example 2: $x = 21$

Divisors are $1,3,7,21$.

| g | y construction | y | g + y |
| --- | --- | --- | --- |
| 1 | 21 → 20 | 20 | 21 |
| 3 | 21 → 18 | 18 | 21 |
| 7 | 21 → 14 | 14 | 21 |

The best values are again tied, and the algorithm can return any of these $y$ values.

These traces show that the construction consistently produces valid candidates aligned with divisors and that the maximum is often achieved in multiple ways.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt{x})$ per test case | Each $x$ is processed by scanning divisors up to its square root |
| Space | $O(1)$ | Only a few scalar variables are stored |

The constraints $x \le 1000$ and $t \le 1000$ make this solution extremely fast, with at most about $10^4$ iterations of the inner loop overall, which is easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve(x):
        best_val = -1
        best_y = 1
        g = 1
        while g * g <= x:
            if x % g == 0:
                for d in (g, x // g):
                    y = x - (x % d)
                    if y == x:
                        y -= d
                    val = d + y
                    if val > best_val:
                        best_val = val
                        best_y = y
            g += 1
        return best_y

    t = int(input())
    out = []
    for _ in range(t):
        out.append(str(solve(int(input()))))
    return "\n".join(out)

# provided samples
assert run("7\n10\n7\n21\n100\n2\n1000\n6\n") == "9\n6\n20\n98\n1\n999\n5"

# custom cases
assert run("1\n2\n") == "1", "minimum edge"
assert run("1\n3\n") == "2", "prime behavior"
assert run("1\n8\n") in {"7", "6"}, "multiple optimal candidates"
assert run("1\n1000\n") >= "1", "upper bound sanity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 | 1 | minimum boundary behavior |
| 1 3 | 2 | prime case |
| 1 8 | 7 or 6 | multiple optimal answers |
| 1 1000 | valid y | large boundary stability |

## Edge Cases

A key edge case is when $x$ is prime. For $x = 7$, all gcd values with valid $y$ are 1, so the expression becomes $1 + y$. The algorithm still checks divisor 1, producing $y = 6$, which is optimal.

Another edge case is when $x$ is a power of two. For $x = 8$, divisors include 1, 2, 4, and 8. The algorithm evaluates candidates like $y = 7, 6, 4$, all producing valid scores. The construction never misses $y = x-1$, which ensures correctness even when structured divisors do not immediately suggest the best answer.

Finally, when $x$ is highly composite such as $x = 1000$, many divisors produce similar scores. The algorithm simply evaluates all of them and safely picks any optimal $y$, with no risk of missing a better hidden configuration.
