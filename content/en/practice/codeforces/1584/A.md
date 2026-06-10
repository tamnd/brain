---
title: "CF 1584A - Mathematical Addition"
description: "For each test case we are given two positive integers, $u$ and $v$. We must find any pair of integers $x$ and $y$, not both zero, such that $$frac{x}{u}+frac{y}{v}=frac{x+y}{u+v}.$$ The task is not to count solutions or find a particular one."
date: "2026-06-10T09:40:49+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1584
codeforces_index: "A"
codeforces_contest_name: "Technocup 2022 - Elimination Round 2"
rating: 800
weight: 1584
solve_time_s: 341
verified: false
draft: false
---

[CF 1584A - Mathematical Addition](https://codeforces.com/problemset/problem/1584/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 5m 41s  
**Verified:** no  

## Solution
## Problem Understanding

For each test case we are given two positive integers, $u$ and $v$. We must find any pair of integers $x$ and $y$, not both zero, such that

$$\frac{x}{u}+\frac{y}{v}=\frac{x+y}{u+v}.$$

The task is not to count solutions or find a particular one. Any valid pair is accepted as long as both values stay within the allowed range.

The constraints are very small from an algorithmic perspective. There are at most $1000$ test cases, and $u,v$ can be as large as $10^9$. Since the numbers themselves are large, searching over possible values of $x$ and $y$ is unrealistic. The intended solution must derive a direct formula and output an answer in constant time for each test case.

A common mistake is to assume that $x=0$ or $y=0$ always works. Consider $u=2$, $v=3$. If we choose $x=0$, the equation becomes

$$\frac{y}{3}=\frac{y}{5}.$$

For any nonzero $y$, this is false. Only $y=0$ works, but $(0,0)$ is forbidden.

Another trap is dividing by expressions that might become zero during algebraic manipulation without first understanding the structure of the equation. A correct derivation should produce a solution valid for every positive $u$ and $v$.

The case $u=v$ also deserves attention. For example, when $u=v=1$, many derived formulas still work, but some ad hoc constructions may accidentally return $(0,0)$. A valid answer is $(-1,1)$.

## Approaches

A brute-force approach would try different values of $x$ and $y$ until a valid pair is found. Since $x$ and $y$ may be any integers in a huge range, even restricting the search to a small interval provides no guarantee of success. The search space is effectively infinite, making brute force unusable.

The real challenge is to understand the equation algebraically.

Starting from

$$\frac{x}{u}+\frac{y}{v}=\frac{x+y}{u+v},$$

multiply both sides by $uv(u+v)$:

$$xv(u+v)+yu(u+v)=uv(x+y).$$

Expanding gives

$$xuv+xv^2+yu^2+yuv=uvx+uvy.$$

The terms $uvx$ and $uvy$ cancel from both sides:

$$xv^2+yu^2=0.$$

Now the equation is much simpler. We only need integers satisfying

$$xv^2=-yu^2.$$

One obvious choice is

$$x=-u^2,\qquad y=v^2.$$

Substituting:

$$(-u^2)v^2+(v^2)u^2=0.$$

The condition is satisfied immediately.

This pair is never $(0,0)$ because $u$ and $v$ are positive. Also,

$$u^2,v^2 \le 10^{18}$$

since $u,v\le10^9$, so the output bounds are respected.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Unbounded | O(1) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read $u$ and $v$.
2. Set

$$x=-u^2.$$
3. Set

$$y=v^2.$$
4. Output $x$ and $y$.

The reason this works is that the original equation reduces exactly to

$$xv^2+yu^2=0.$$

With the chosen values,

$$(-u^2)v^2+(v^2)u^2=0,$$

so the condition is always satisfied.

### Why it works

After clearing denominators and simplifying, every valid solution must satisfy

$$xv^2+yu^2=0.$$

The construction

$$x=-u^2,\qquad y=v^2$$

makes the two terms exact opposites. Their sum is zero, which means the simplified equation holds. Since the simplification was algebraically equivalent to the original equation, the original equation also holds. Because $u$ and $v$ are positive, neither $u^2$ nor $v^2$ is zero, so the pair cannot be $(0,0)$.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    u, v = map(int, input().split())
    print(-u * u, v * v)
```

The implementation follows the mathematical construction directly.

For each test case we read $u$ and $v$, compute $-u^2$ and $v^2$, and print them.

Python integers automatically handle values up to $10^{18}$, so there is no overflow concern. The largest possible magnitude is

$$(10^9)^2 = 10^{18},$$

which exactly matches the allowed output range.

No special handling is needed for equal values, large values, or any other corner case because the formula is valid for every positive $u$ and $v$.

## Worked Examples

### Example 1

Input:

```
u = 2
v = 3
```

| Step | u | v | x | y |
| --- | --- | --- | --- | --- |
| Read input | 2 | 3 | - | - |
| Compute x | 2 | 3 | -4 | - |
| Compute y | 2 | 3 | -4 | 9 |

Verification:

$$xv^2+yu^2=(-4)\cdot9+9\cdot4=0.$$

This example shows how the construction immediately satisfies the reduced equation.

### Example 2

Input:

```
u = 6
v = 9
```

| Step | u | v | x | y |
| --- | --- | --- | --- | --- |
| Read input | 6 | 9 | - | - |
| Compute x | 6 | 9 | -36 | - |
| Compute y | 6 | 9 | -36 | 81 |

Verification:

$$(-36)\cdot81+81\cdot36=0.$$

This example demonstrates that the same formula works regardless of whether $u$ and $v$ share common factors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only two multiplications and one output |
| Space | O(1) | No extra data structures |

Even for the maximum $1000$ test cases, the program performs only a few thousand arithmetic operations. This is far below the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        u, v = map(int, input().split())
        out.append(f"{-u*u} {v*v}")

    return "\n".join(out) + "\n"

# provided sample input, using the editorial's valid construction
assert run(
"""4
1 1
2 3
3 5
6 9
"""
) == (
"""-1 1
-4 9
-9 25
-36 81
"""
)

# minimum values
assert run(
"""1
1 1
"""
) == (
"""-1 1
"""
), "minimum input"

# equal values
assert run(
"""1
7 7
"""
) == (
"""-49 49
"""
), "u equals v"

# large values
assert run(
"""1
1000000000 1000000000
"""
) == (
"""-1000000000000000000 1000000000000000000
"""
), "boundary magnitude"

# mixed values
assert run(
"""1
1 1000000000
"""
) == (
"""-1 1000000000000000000
"""
), "asymmetric case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `-1 1` | Smallest legal values |
| `7 7` | `-49 49` | Equal parameters |
| `10^9 10^9` | `-10^18 10^18` | Maximum output magnitude |
| `1 10^9` | `-1 10^18` | Highly asymmetric inputs |

## Edge Cases

Consider the smallest possible input:

```
1
1 1
```

The algorithm outputs:

```
-1 1
```

Checking the reduced equation:

$$(-1)\cdot1^2+1\cdot1^2=0.$$

The pair is not $(0,0)$, so it is valid.

Now consider equal values:

```
1
5 5
```

The algorithm outputs:

```
-25 25
```

Substituting into the simplified condition:

$$(-25)\cdot25+25\cdot25=0.$$

Nothing special is required when $u=v$.

Finally, consider the largest possible values:

```
1
1000000000 1000000000
```

The algorithm outputs:

```
-1000000000000000000 1000000000000000000
```

Both numbers are exactly within the allowed range. The reduced equation becomes

$$(-10^{18})\cdot10^{18}+10^{18}\cdot10^{18}=0.$$

The construction remains valid even at the boundary of the constraints.
