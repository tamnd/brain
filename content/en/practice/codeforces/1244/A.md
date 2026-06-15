---
title: "CF 1244A - Pens and Pencils"
description: "Polycarp has two types of work tomorrow: writing lectures and drawing during practical classes. For lectures he must use pens, and each pen can be used for a limited number of lectures before it dries out."
date: "2026-06-15T21:22:15+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1244
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 592 (Div. 2)"
rating: 800
weight: 1244
solve_time_s: 153
verified: false
draft: false
---

[CF 1244A - Pens and Pencils](https://codeforces.com/problemset/problem/1244/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 2m 33s  
**Verified:** no  

## Solution
## Problem Understanding

Polycarp has two types of work tomorrow: writing lectures and drawing during practical classes. For lectures he must use pens, and each pen can be used for a limited number of lectures before it dries out. For practical classes he must use pencils, and each pencil can be reused across a fixed number of classes before it becomes unusable.

The task is to choose how many pens and pencils to take so that all lectures and practical classes can be covered, while also fitting everything inside a pencil case that can hold at most $k$ items in total. If it is impossible to both satisfy the workload requirements and stay within capacity, we must report failure.

Each test case gives the number of lectures $a$, practical classes $b$, pen capacity $c$, pencil capacity $d$, and total storage limit $k$. We output any valid pair $(x, y)$ where $x$ pens cover all lectures, $y$ pencils cover all practical classes, and $x + y \le k$.

The key constraint is that pens and pencils are independent in usage but coupled by a shared capacity limit. That coupling is what makes the problem nontrivial.

The input bounds are small, all values are at most 100 and up to 100 test cases. This immediately rules out anything heavier than constant time per test case. Even an $O(k^2)$ approach is fine in theory, but unnecessary.

A subtle edge case appears when one of the requirements forces a large number of items while capacity is small. For example, if $a = 10, c = 1$, then at least 10 pens are needed. If $k < 10$, the answer is impossible even if pencils are irrelevant. A naive approach that only checks total feasibility without respecting per-type minimums would fail here.

Another issue arises if one tries to greedily minimize total items without considering flexibility. Since any valid pair is accepted, minimizing is unnecessary and can lead to overthinking or incorrect balancing strategies.

## Approaches

A brute-force method would try all possible numbers of pens $x$ from 0 to $k$, compute how many lectures they can cover, and then check whether there exists a corresponding number of pencils $y$ that satisfies both coverage constraints and the capacity limit. For each $x$, computing feasibility is constant time, so the total complexity is $O(k)$ per test case. This already works under constraints, but it is more complicated than needed.

The key observation is that the minimum number of pens needed is fixed: each pen covers $c$ lectures, so we need at least $\lceil a / c \rceil$ pens. Similarly, we need at least $\lceil b / d \rceil$ pencils. If we take exactly these minimum required counts, the only remaining question is whether they fit into the pencil case. If they do not, increasing either type only makes the situation worse for capacity, since increasing items never helps feasibility under a fixed upper bound.

This reduces the problem to a direct feasibility check followed by output of the minimal required configuration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(k)$ per test | $O(1)$ | Accepted but unnecessary |
| Optimal | $O(1)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute the minimum number of pens needed as $x = \lceil a / c \rceil$. This ensures all lectures are covered because each pen supports at most $c$ lectures.
2. Compute the minimum number of pencils needed as $y = \lceil b / d \rceil$. This ensures all practical classes are covered because each pencil supports at most $d$ classes.
3. Check whether $x + y \le k$. This ensures the pencil case constraint is satisfied.
4. If the condition fails, output $-1$ because even the most efficient choice already exceeds capacity, and any alternative only increases usage.
5. Otherwise, output $x$ and $y$. Any additional items are unnecessary, and the problem allows any valid configuration, so this minimal construction is sufficient.

### Why it works

The construction uses the smallest possible number of items of each type that still satisfies workload requirements. Any valid solution must use at least these many pens and pencils individually, because reducing either would fail to cover all tasks. Therefore, if even this minimal configuration exceeds capacity, no rearrangement can fix it. If it fits, it is automatically a valid solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, c, d, k = map(int, input().split())

    pens = (a + c - 1) // c
    pencils = (b + d - 1) // d

    if pens + pencils > k:
        print(-1)
    else:
        print(pens, pencils)
```

The computation uses ceiling division via integer arithmetic, avoiding floating-point operations. Each test case is handled independently. The only decision point is the feasibility check against $k$, which directly reflects the storage constraint.

## Worked Examples

### Example 1

Input:

```
7 5 4 5 8
```

| Step | pens computation | pencils computation | sum | decision |
| --- | --- | --- | --- | --- |
| compute | (7+3)//4 = 2 | (5+4)//5 = 1 | 3 | 3 ≤ 8 |

Output is:

```
2 1
```

This demonstrates a case where both requirements are small and comfortably fit within capacity.

### Example 2

Input:

```
20 53 45 26 4
```

| Step | pens computation | pencils computation | sum | decision |
| --- | --- | --- | --- | --- |
| compute | (20+44)//45 = 1 | (53+25)//26 = 3 | 4 | 4 ≤ 4 |

Output is:

```
1 3
```

This shows a tight capacity boundary case where the solution exactly matches the limit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | Each test case requires only a few arithmetic operations |
| Space | $O(1)$ | No auxiliary structures beyond variables |

The constraints are small enough that even repeated arithmetic is trivial. The solution runs in constant time per test case, easily within limits.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        a, b, c, d, k = map(int, input().split())
        pens = (a + c - 1) // c
        pencils = (b + d - 1) // d
        if pens + pencils > k:
            out.append("-1")
        else:
            out.append(f"{pens} {pencils}")
    return "\n".join(out)

# provided samples
assert solve("""3
7 5 4 5 8
7 5 4 5 2
20 53 45 26 4
""") == """2 1
-1
1 3"""

# minimum case
assert solve("""1
1 1 1 1 2
""") == "1 1"

# tight impossible
assert solve("""1
10 10 5 5 3
""") == "-1"

# exact fit
assert solve("""1
4 6 2 3 3
""") in {"2 2", "2 2".strip()}
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 2 | 1 1 | smallest nontrivial valid case |
| 10 10 5 5 3 | -1 | impossible due to capacity |
| 4 6 2 3 3 | 2 2 | tight packing boundary |

## Edge Cases

When $a$ is not divisible by $c$, ceiling division is required. For example, $a = 5, c = 2$ gives $x = 3$. Using integer division without adjustment would incorrectly give 2, which fails to cover all lectures.

When capacity is exactly equal to required items, the solution must accept it. For example, if $x + y = k$, it is still valid, and rejecting equality would incorrectly discard correct answers.

When either $a = 0$ or $b = 0$, the formula still behaves correctly, producing zero pens or pencils as expected, since no items are needed for that category.
