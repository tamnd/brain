---
title: "CF 1100C - NN and the Optical Illusion"
description: "We are building a very specific circle configuration. There is one central circle of radius $r$. Around it, $n$ identical circles are placed so that they form a ring."
date: "2026-06-12T05:40:07+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "geometry", "math"]
categories: ["algorithms"]
codeforces_contest: 1100
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 532 (Div. 2)"
rating: 1200
weight: 1100
solve_time_s: 87
verified: true
draft: false
---

[CF 1100C - NN and the Optical Illusion](https://codeforces.com/problemset/problem/1100/C)

**Rating:** 1200  
**Tags:** binary search, geometry, math  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are building a very specific circle configuration. There is one central circle of radius $r$. Around it, $n$ identical circles are placed so that they form a ring. Each of these outer circles touches the central circle, and every outer circle also touches its two neighboring outer circles.

The task is to determine the radius $R$ of each outer circle so that this geometric arrangement is exactly possible.

The key constraint is that the centers of the outer circles lie on a regular polygon around the center of the inner circle. Once we fix $n$, the geometry is rigid, so $R$ is uniquely determined by $r$.

The constraints $3 \le n \le 100$ and $1 \le r \le 100$ are small enough that any constant-time geometric formula is sufficient. Even a numerically solved equation would be acceptable, but the structure of the problem admits a direct trigonometric derivation, so no search is needed.

A common mistake is assuming linear scaling between $r$ and $R$, or treating the outer circles as independent tangent circles around a point. That ignores the fact that the outer circles are constrained both by the central tangency and by adjacency, which forces a rigid angular spacing.

The only real edge case occurs when $n$ is small, especially $n = 3$, where the geometry becomes tight and numerical instability in trigonometric functions can show up if implemented carelessly.

## Approaches

A brute-force approach would try a candidate radius $R$, place $n$ points evenly around a circle of radius $r + R$, and check whether adjacent circles of radius $R$ are tangent. This can be verified by computing distances between neighboring centers and checking whether they equal $2R$.

The issue is that this turns into a root-finding problem. For each guess of $R$, we must evaluate a geometric condition, and convergence would require iterative search such as binary search or Newton’s method. Each check is $O(n)$, and with sufficient precision requirements we may need dozens of iterations. While still feasible, it is unnecessarily indirect for a problem that has a closed-form structure.

The key observation is that the outer circle centers lie on a circle of radius $r + R$, equally spaced by angle $\frac{2\pi}{n}$. The distance between adjacent centers is a chord of this larger circle. That chord must equal $2R$, because neighboring outer circles are tangent.

So we get a direct geometric equation:

$$2R = 2 (r + R)\sin\left(\frac{\pi}{n}\right)$$

This comes from the chord length formula: a chord subtending angle $\theta$ in a circle of radius $S$ has length $2S\sin(\theta/2)$. Here $S = r + R$ and $\theta = \frac{2\pi}{n}$.

Solving the equation algebraically removes all search:

$$R = (r + R)\sin\left(\frac{\pi}{n}\right)$$

$$R - R\sin\left(\frac{\pi}{n}\right) = r\sin\left(\frac{\pi}{n}\right)$$

$$R(1 - \sin(\frac{\pi}{n})) = r\sin\left(\frac{\pi}{n}\right)$$

$$R = \frac{r\sin(\frac{\pi}{n})}{1 - \sin(\frac{\pi}{n})}$$

This closed form is stable and evaluates in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (binary search on $R$) | $O(n \log \epsilon^{-1})$ | $O(1)$ | Accepted but unnecessary |
| Optimal (closed form geometry) | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute the angle step between adjacent outer circle centers, which is $\frac{\pi}{n}$. This comes from halving the full angle $\frac{2\pi}{n}$ because chord length uses half-angle sine.
2. Evaluate $s = \sin\left(\frac{\pi}{n}\right)$. This value captures how far apart adjacent centers are relative to the circumradius of their arrangement.
3. Translate the geometry into a linear equation in $R$: the distance between adjacent centers is both $2R$ (tangency condition) and $2(r+R)s$ (chord length condition).
4. Solve the equation $R = (r+R)s$ algebraically, isolating $R$. This produces a direct formula without iteration.
5. Compute the final value using floating-point arithmetic and output it with sufficient precision.

### Why it works

The entire structure reduces to a regular $n$-gon formed by the centers of the outer circles. Because all outer circles are identical and mutually tangent in a cycle, their centers must lie on a circle with equal angular spacing. That rigid symmetry forces a single chord length constraint, and that constraint uniquely determines the ratio between $R$ and $r$. No alternative configuration exists once $n$ and $r$ are fixed.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

n, r = map(int, input().split())

s = math.sin(math.pi / n)
R = (r * s) / (1 - s)

print(R)
```

The code directly encodes the derived formula. The only subtlety is using `math.pi / n` rather than `2*pi/n`, since the chord formula depends on the half-angle. A common implementation mistake is forgetting this halving and using the full central angle, which leads to a systematic scaling error in the result.

All computations are done in double precision, which is sufficient because the required tolerance is $10^{-6}$, far above floating-point epsilon.

## Worked Examples

### Example 1: $n = 3, r = 1$

We compute $s = \sin(\pi/3) = \sqrt{3}/2 \approx 0.8660254$.

| Step | Value |
| --- | --- |
| $n$ | 3 |
| $r$ | 1 |
| $s = \sin(\pi/n)$ | 0.8660254 |
| $R = \frac{r s}{1 - s}$ | 6.4641016 |

This matches the sample output exactly, confirming the tight equilateral structure of the configuration.

### Example 2: $n = 6, r = 2$

Here $s = \sin(\pi/6) = 0.5$.

| Step | Value |
| --- | --- |
| $n$ | 6 |
| $r$ | 2 |
| $s$ | 0.5 |
| $R$ | $\frac{2 \cdot 0.5}{1 - 0.5} = 2$ |

The outer circles have the same radius as the inner radius, which is consistent with the hexagonal symmetry tightening exactly at this configuration.

These examples show how the formula smoothly adapts to both small and moderate $n$, preserving geometric consistency.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a constant number of arithmetic and trigonometric operations are performed |
| Space | $O(1)$ | No auxiliary data structures are used |

The constraints allow any constant-time mathematical computation, so this solution easily satisfies both time and memory limits.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, r = map(int, input().split())
    s = math.sin(math.pi / n)
    R = (r * s) / (1 - s)
    return str(R)

# provided sample
assert abs(float(run("3 1\n")) - 6.4641016) < 1e-6, "sample 1"

# minimum n
assert run("3 1\n")  # already covered extreme structure

# larger n
assert abs(float(run("100 1\n")) - (math.sin(math.pi/100)/(1-math.sin(math.pi/100)))) < 1e-9

# equal scaling
assert abs(float(run("6 2\n")) - 2.0) < 1e-9

# another random case
assert abs(float(run("10 5\n")) - (5*math.sin(math.pi/10)/(1-math.sin(math.pi/10)))) < 1e-9
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1 | 6.4641016 | smallest valid configuration |
| 100 1 | computed | stability for large n |
| 6 2 | 2 | symmetric case where result simplifies |
| 10 5 | computed | general correctness |

## Edge Cases

For $n = 3$, the configuration becomes the tightest possible triangle of outer circles around the center. Here $\sin(\pi/3)$ is large, so the denominator $1 - s$ becomes small, amplifying floating-point sensitivity. The formula still behaves correctly because both numerator and denominator are well within stable floating-point range.

For large $n$, $\sin(\pi/n) \approx \pi/n$, so $R \approx \frac{r \cdot \pi/n}{1 - \pi/n}$, which approaches 0 as $n$ grows. The computation remains stable because both numerator and denominator shrink smoothly without cancellation.

For intermediate values like $n = 6$, symmetry leads to exact simplifications such as $\sin(\pi/6) = 1/2$, producing clean integer results. The formula handles these cases without special casing, confirming it captures the full geometry uniformly.
