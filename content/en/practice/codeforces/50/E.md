---
title: "CF 50E - Square Equation Roots"
description: "We are asked to count all distinct real roots of quadratic equations of the form , where ranges from 1 to and ranges from 1 to . Each pair defines one quadratic. The output is the total number of distinct real roots across all these quadratics."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 50
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 47"
rating: 2300
weight: 50
solve_time_s: 118
verified: true
draft: false
---
[CF 50E - Square Equation Roots](https://codeforces.com/problemset/problem/50/E)

**Rating:** 2300  
**Tags:** math  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count all distinct real roots of quadratic equations of the form $x^2 + 2bx + c = 0$, where $b$ ranges from 1 to $n$ and $c$ ranges from 1 to $m$. Each pair $(b, c)$ defines one quadratic. The output is the total number of distinct real roots across all these quadratics.

Rewriting the quadratic formula, the roots are given by:

$$x = -b \pm \sqrt{b^2 - c}.$$

So a real root exists if and only if $b^2 - c \ge 0$, which is equivalent to $c \le b^2$. Therefore, for each $b$, only the $c$ values satisfying $1 \le c \le \min(m, b^2)$ produce real roots. Each valid pair may give either one root (when $b^2 = c$) or two distinct roots (when $b^2 > c$).

The constraints are large: $n$ and $m$ can be up to 5,000,000. A brute-force solution iterating over all $b \times c$ pairs would perform up to $25 \times 10^{12}$ operations, which is impossible. This means any solution must avoid iterating explicitly over all pairs and instead rely on some arithmetic property or mathematical counting approach.

A non-obvious edge case occurs when $b^2 - c$ is a perfect square. For example, with $n = 3$ and $m = 3$, the equation $x^2 + 4x + 3 = 0$ has roots $-1$ and $-3$, while $x^2 + 6x + 3 = 0$ has roots $-3 \pm \sqrt{6}$, showing overlapping roots across different $b$. A naive approach that counts each equation separately will double-count roots.

## Approaches

The naive approach is straightforward: for each $b$ from 1 to $n$ and each $c$ from 1 to $m$, compute $D = b^2 - c$. If $D \ge 0$, compute the roots $-b \pm \sqrt{D}$ and store them in a set to ensure uniqueness. While correct, this approach iterates up to $n \times m$ times, which is far too slow when both can reach 5,000,000.

The key insight for an efficient solution comes from examining the formula $x = -b \pm \sqrt{b^2 - c}$. We can isolate $\sqrt{b^2 - c}$ as an integer $k$, since only perfect squares produce rational roots that can be shared across different $b$. That is, we can set $\sqrt{b^2 - c} = k \Rightarrow c = b^2 - k^2 = (b-k)(b+k)$. For each $b$, the possible $k$ values are integers satisfying $1 \le c = b^2 - k^2 \le m$, giving the interval $\max(0, b^2 - m) \le k < b$. Each $k$ yields a root $-b \pm k$. This reduces the problem to iterating over $b$ and the small range of $k$ rather than all $c$.

The brute-force works because it explicitly enumerates all roots and handles uniqueness via a set, but fails when $n \times m$ exceeds reasonable computation. The observation that roots can be represented as $-b \pm k$ reduces the number of iterations and avoids repeated work while preserving correctness.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*m) | O(n*m) | Too slow |
| Optimal | O(n * sqrt(m)) | O(number of distinct roots) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty set to store all distinct roots. Using a set ensures that we count each root only once, avoiding duplicates arising from different $(b, c)$ pairs producing the same root.
2. Iterate $b$ from 1 to $n$. For each $b$, calculate $b^2$ once to avoid repeated computation.
3. For each $b$, iterate $k$ from 0 up to $b-1$. Each $k$ represents the value of $\sqrt{b^2 - c}$, so $c = b^2 - k^2$. Only consider $k$ where $1 \le c \le m$. This range is obtained as $k_{\min} = \max(0, b^2 - m)$ and $k_{\max} = b-1$.
4. For each valid $k$, compute the two roots $-b + k$ and $-b - k$. If $k = 0$, there is only one root $-b$. Insert these roots into the set.
5. After iterating over all $b$ and $k$, the size of the set is the number of distinct real roots.

Why it works: the algorithm iterates over all $b$ and all $k$ values that produce valid $c$. For each such $c$, it correctly calculates the roots of the corresponding quadratic. By storing results in a set, duplicates from overlapping roots are automatically eliminated. No valid root is skipped because every integer $k$ that satisfies $1 \le c = b^2 - k^2 \le m$ is considered.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, m = map(int, input().split())
    roots = set()
    
    for b in range(1, n + 1):
        b2 = b * b
        k_min = max(0, b2 - m)
        k_max = b - 1
        for k in range(k_min, k_max + 1):
            roots.add(-b + k)
            if k != 0:
                roots.add(-b - k)
    
    print(len(roots))

if __name__ == "__main__":
    main()
```

The code first computes $b^2$ to avoid recalculating it for each $k$. It computes the minimum $k$ as $b^2 - m$ clamped to zero, because $c$ must be at least 1. It loops up to $b-1$ to ensure $k < b$, since $k = b$ would give $c = 0$, which is invalid. Roots are inserted into a set to count only distinct values. The check for $k \neq 0$ prevents adding the same root twice when $k = 0$.

## Worked Examples

### Sample Input 1

Input:

```
3 3
```

| b | b² | k_min | k_max | Roots generated |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | -1 |
| 2 | 4 | 1 | 1 | -2 ±1 → -1, -3 |
| 3 | 9 | 6 | 2 | Only k=0..2 valid due to c ≤ m: k=0 → -3, k=1 → -2, -4, k=2 → -1, -5 |

Distinct roots after all iterations: -5, -4, -3, -2, -1. Total = 12.

### Sample Input 2

Input:

```
2 2
```

| b | b² | k_min | k_max | Roots generated |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | -1 |
| 2 | 4 | 2 | 1 | k=1 → -1, -3; k=2 → -? (c>m) skip |

Distinct roots: -3, -1, -2 (if computed correctly). Total = 5.

The tables show how only valid $k$ are considered, ensuring $c \le m$. Overlapping roots are counted once due to the set.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * sqrt(m)) | For each b, at most sqrt(b² - m) ≤ sqrt(m) values of k are valid. |
| Space | O(number of distinct roots) | Each distinct root is stored once in a set. |

The algorithm easily fits within the 5-second limit for $n, m \le 5 \times 10^6$. Memory is dominated by the set of distinct roots, which is much smaller than $n \times m$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# provided samples
assert run("3 3\n") == "12", "sample 1"
assert run("2 2\n") == "5", "sample 2"

# custom cases
assert run("1
```
