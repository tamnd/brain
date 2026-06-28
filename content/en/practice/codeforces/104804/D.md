---
title: "CF 104804D - \u0420\u044b\u0446\u0430\u0440\u0438"
description: "We are given a bag containing a total of $n$ indistinguishable draw tokens, where exactly $k$ of them are special knight tokens and the remaining $n-k$ are ordinary tokens. From this bag, a player draws $m$ tokens uniformly at random without replacement."
date: "2026-06-28T13:25:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104804
codeforces_index: "D"
codeforces_contest_name: "Central Russia Regional Contest, 2022, Qualification Contest"
rating: 0
weight: 104804
solve_time_s: 66
verified: false
draft: false
---

[CF 104804D - \u0420\u044b\u0446\u0430\u0440\u0438](https://codeforces.com/problemset/problem/104804/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a bag containing a total of $n$ indistinguishable draw tokens, where exactly $k$ of them are special knight tokens and the remaining $n-k$ are ordinary tokens. From this bag, a player draws $m$ tokens uniformly at random without replacement. The task is to compute the probability that among the drawn tokens there is at least one knight.

The randomness is purely combinatorial: every subset of size $m$ among the $n$ tokens is equally likely. The output is the probability of selecting a subset that intersects the set of knights in at least one element.

The constraints are small, with $n \le 20$ and $m \le 20$, so any approach that enumerates subsets or uses combinatorial counting is feasible. This immediately rules out the need for approximations or floating-point stochastic simulation. Exact combinatorics is required.

A key edge situation appears when there are no knights or when all tokens are knights. If $k = 0$, no draw can contain a knight, so the probability must be zero unless $m = 0$ (which does not occur here since $m \ge 1$). If $k = n$, every draw contains only knights, so the probability is exactly one as long as $m \le n$. Another subtle case occurs when $m > n - k$, meaning it is impossible to avoid drawing a knight; in this case the answer is also exactly one. Any solution that tries to compute ratios without handling these degenerate cases may run into division by zero or incorrect combinatorial bounds.

## Approaches

The brute-force idea is to enumerate all possible subsets of size $m$ from the $n$ tokens and count how many of them contain at least one knight. The total number of subsets is $\binom{n}{m}$, which is at most $\binom{20}{10} = 184756$, so enumeration is completely feasible. For each subset, we check whether it intersects the knight set. This is correct because all subsets are equally likely.

However, brute-force does unnecessary work because we only care about whether a subset contains at least one knight, not which specific knight appears or how many appear. This suggests grouping subsets by the number of knights chosen. Instead of iterating over subsets explicitly, we can count directly: choose $i$ knights from the $k$ available and $m-i$ non-knights from the $n-k$ ordinary tokens, summing over all valid $i \ge 1$. This reduces the problem to a small combinatorial sum.

An even cleaner perspective is to use the complement event. Instead of counting subsets with at least one knight, we count subsets with zero knights, meaning all $m$ chosen tokens come from the $n-k$ ordinary ones. That count is simply $\binom{n-k}{m}$ when $m \le n-k$, and zero otherwise. The probability we want is then one minus this ratio over $\binom{n}{m}$.

This approach avoids summations entirely and reduces the solution to computing binomial coefficients.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | $O(\binom{n}{m} \cdot m)$ | $O(m)$ | Accepted but unnecessary |
| Complement Counting | $O(n^2)$ or $O(nm)$ | $O(nm)$ | Accepted |

## Algorithm Walkthrough

1. Precompute binomial coefficients $C[n][k]$ for $0 \le n,k \le 20$. This is needed because all combinatorial values we use depend on small $n$, and precomputation avoids repeated recursion or factorial division.
2. Compute the total number of ways to draw $m$ tokens from $n$, which is $C[n][m]$. This represents the full probability space where every outcome is equally likely.
3. Compute the number of ways to draw $m$ tokens without selecting any knight. This is only possible by choosing all $m$ tokens from the $n-k$ non-knights, giving $C[n-k][m]$ when $m \le n-k$, otherwise zero. The reason is that avoiding knights forces all selections to come from the remaining pool.
4. Compute the probability of the complement event as $P(\text{no knight}) = \frac{C[n-k][m]}{C[n][m]}$. This is valid because both numerator and denominator count equally likely subsets.
5. Subtract from one to get the desired probability: $P(\text{at least one knight}) = 1 - P(\text{no knight})$.
6. Print the result using floating-point division.

### Why it works

Every size-$m$ subset belongs to exactly one of two disjoint categories: it contains at least one knight, or it contains none. The second category is exactly the subsets fully contained in the non-knight set. Counting that category directly avoids overcounting configurations with multiple knights and replaces a multi-case sum with a single closed form. Since binomial coefficients count uniform combinatorial outcomes, the ratio of counts exactly matches the probability under uniform random sampling.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXN = 20

# precompute binomial coefficients
C = [[0] * (MAXN + 1) for _ in range(MAXN + 1)]
for i in range(MAXN + 1):
    C[i][0] = 1
    for j in range(1, i + 1):
        C[i][j] = C[i - 1][j - 1] + C[i - 1][j]

def solve():
    n, k, m = map(int, input().split())

    total = C[n][m] if m <= n else 0
    if total == 0:
        print("1.00000000")
        return

    non_knights = n - k

    if m > non_knights:
        print("1.00000000")
        return

    no_knight = C[non_knights][m]
    ans = 1.0 - no_knight / total
    print(f"{ans:.8f}")

if __name__ == "__main__":
    solve()
```

The solution begins by building Pascal’s triangle up to 20, which ensures all combinations are available in constant time per query. The main computation then relies on two combinatorial lookups.

The first important boundary is when $m > n$, which should not occur under constraints but is handled defensively by treating total combinations as zero. The second is when $m > n-k$, where the answer is immediately one because it is impossible to avoid knights. This avoids accessing invalid binomial values.

The subtraction form is numerically stable in this setting because all values are small integers, and floating-point precision is more than sufficient for 4 decimal places.

## Worked Examples

### Sample 1

Input: $n=5, k=2, m=2$

We compute total ways to pick 2 from 5, which is 10. The non-knights count is 3, so ways to pick 2 without knights is $\binom{3}{2} = 3$.

| Step | Value |
| --- | --- |
| Total subsets $C[5][2]$ | 10 |
| Non-knight subsets $C[3][2]$ | 3 |
| Probability no knight | 0.3 |
| Final probability | 0.7 |

This shows the complement interpretation directly counts all safe draws and subtracts them from the full space.

### Sample 2

Input: $n=8, k=2, m=4$

Total subsets is $C[8][4] = 70$. Non-knights are 6, so safe subsets are $C[6][4] = 15$.

| Step | Value |
| --- | --- |
| Total subsets $C[8][4]$ | 70 |
| Non-knight subsets $C[6][4]$ | 15 |
| Probability no knight | 15/70 |
| Final probability | 0.78571429 |

This case shows that even when knights are few, the complement method correctly scales the probability.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Building Pascal triangle up to 20 takes constant bounded work |
| Space | $O(n^2)$ | Storing binomial table up to 20x20 |

The constraints are extremely small, so this solution runs in constant time in practice. Memory usage is negligible, and all operations are simple integer arithmetic followed by a single floating-point division.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    MAXN = 20
    C = [[0] * (MAXN + 1) for _ in range(MAXN + 1)]
    for i in range(MAXN + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = C[i - 1][j - 1] + C[i - 1][j]

    n, k, m = map(int, input().split())
    total = C[n][m]
    non_knights = n - k

    if m > non_knights:
        return "1.00000000\n"

    ans = 1.0 - C[non_knights][m] / total
    return f"{ans:.8f}\n"

# provided samples
assert run("5 2 2") == "0.70000000\n"
assert run("8 2 4") == "0.78571429\n"
assert run("5 1 6") == "1.00000000\n"

# custom cases
assert run("5 0 2") == "0.00000000\n", "no knights"
assert run("5 5 2") == "1.00000000\n", "all knights"
assert run("10 3 1") == "0.30000000\n", "single draw"
assert run("6 2 6") == "1.00000000\n", "must pick all"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 0 2 | 0.00000000 | no knights available |
| 5 5 2 | 1.00000000 | all tokens are knights |
| 10 3 1 | 0.30000000 | single draw probability |
| 6 2 6 | 1.00000000 | forced inclusion of knights |

## Edge Cases

When there are no knights in the bag, the complement term becomes identical to the total number of subsets. For example, with input $5, 0, 2$, we get total $C[5][2] = 10$ and non-knight subsets $C[5][2] = 10$, giving probability zero. The algorithm naturally handles this without special branching beyond arithmetic.

When all tokens are knights, the non-knight pool has size zero. For $5, 5, 2$, we compute $C[0][2] = 0$, so probability becomes one. This reflects that every draw must contain knights because there are no alternatives.

When $m > n-k$, such as $5, 2, 4$, it is impossible to avoid knights since only 3 non-knights exist. The algorithm detects this via the condition $m > n-k$ and directly outputs one, matching the combinatorial reality that the complement count is zero.
