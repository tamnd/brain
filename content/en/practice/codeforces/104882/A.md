---
title: "CF 104882A - A+B?"
description: "We are counting integer pairs $(a, b)$ that satisfy a simple linear constraint: their sum is fixed to a given value $n$, and both numbers must lie inside a symmetric interval centered at zero."
date: "2026-06-28T09:17:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104882
codeforces_index: "A"
codeforces_contest_name: "Voronezh State University - Sitronics contest II"
rating: 0
weight: 104882
solve_time_s: 37
verified: true
draft: false
---

[CF 104882A - A+B?](https://codeforces.com/problemset/problem/104882/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are counting integer pairs $(a, b)$ that satisfy a simple linear constraint: their sum is fixed to a given value $n$, and both numbers must lie inside a symmetric interval centered at zero. The interval is defined by $p$: both $a$ and $b$ must be between $-10^p$ and $10^p$, inclusive.

So the task is not to search for pairs in two dimensions independently. Once $a$ is chosen, $b$ is forced to be $n - a$. The only question is how many integer values of $a$ keep both $a$ and $n-a$ inside the allowed range.

The input is just two integers, one defining the target sum and one defining the magnitude of allowed values. The output is the number of valid integer choices of $a$, which directly corresponds to valid pairs.

The constraints are very small in terms of structure complexity: $p \le 9$, so the bounds are at most $10^9$. That means the valid range is always a contiguous interval of size at most $2 \cdot 10^9 + 1$, so any solution that enumerates all possible values of $a$ is already borderline but still feasible in worst case, though unnecessary.

A naive mistake appears when one tries to independently choose $a$ and $b$ and then filter by sum, effectively double counting structure that is actually one-dimensional. Another common mistake is forgetting that both bounds must be enforced simultaneously on both variables.

A concrete edge situation occurs when the interval is so tight that no solutions exist. For example, if $n = 25$ and $p = 1$, the range is $[-10, 10]$. No two numbers in that range can sum to 25, so the answer must be 0. Any approach that only checks one side of the constraint would incorrectly report positive counts.

## Approaches

The brute-force interpretation is straightforward: iterate over all possible integers $a$ in the allowed range, compute $b = n - a$, and check whether $b$ also lies in the same range. Each valid $a$ contributes one valid pair. This is correct because every valid pair corresponds to exactly one choice of $a$.

The problem with this approach is the size of the search space. The range of $a$ has length $2 \cdot 10^p + 1$, which for $p = 9$ is about $2 \cdot 10^9$. That is far beyond what can be iterated within one second.

The key observation is that the constraint reduces to intersecting two intervals. From $a \in [-10^p, 10^p]$, we also need $n - a \in [-10^p, 10^p]$, which rearranges into another interval constraint on $a$: $a \in [n - 10^p, n + 10^p]$. So valid $a$ values lie in the intersection of two intervals:

$$[-10^p, 10^p] \cap [n - 10^p, n + 10^p]$$

Once the problem becomes interval intersection, the answer is just the length of that intersection in integers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(10^p)$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute the bound $M = 10^p$. This defines the allowed range for both variables. The entire problem is constrained by this single value.
2. Convert the condition $a \in [-M, M]$ directly into the first interval $I_1 = [-M, M]$.
3. Rewrite the condition $b = n - a \in [-M, M]$ into a constraint on $a$.

This becomes:

$$-M \le n - a \le M$$

which is equivalent to:

$$n - M \le a \le n + M$$

giving a second interval $I_2 = [n - M, n + M]$.
4. Compute the intersection of these two intervals. The left boundary is:

$$L = \max(-M, n - M)$$

and the right boundary is:

$$R = \min(M, n + M)$$
5. If $L > R$, the intervals do not overlap and no valid $a$ exists, so the answer is 0.
6. Otherwise, the number of integer values in the intersection is $R - L + 1$, which is the final answer.

### Why it works

Every valid pair $(a, b)$ is uniquely determined by $a$, and the constraints on $a$ are exactly the requirement that both $a$ and $n-a$ lie inside a fixed interval. This translates into two independent interval constraints on $a$. Their intersection captures precisely the feasible set with no overcounting or omission. The computation reduces the original two-variable constraint system into a single interval counting problem, which preserves all valid solutions and excludes all invalid ones by construction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, p = map(int, input().split())
    M = 10 ** p

    L = max(-M, n - M)
    R = min(M, n + M)

    if L > R:
        print(0)
    else:
        print(R - L + 1)

if __name__ == "__main__":
    solve()
```

The solution computes the maximum allowable range for $a$ under both constraints and directly counts how many integers lie in that overlap. The critical implementation detail is computing both bounds symmetrically and applying a simple max-min intersection. The off-by-one risk appears in the final count; the inclusive nature of integer intervals requires adding 1 to $R - L$.

## Worked Examples

### Example 1

Input:

```

```

Here $M = 10$. The constraints are:

$a \in [-10, 10]$ and $a \in [7 - 10, 7 + 10] = [-3, 17]$.

| Step | L candidate | R candidate | Interval |
| --- | --- | --- | --- |
| I1 | -10 | 10 | [-10, 10] |
| I2 | -3 | 17 | [-3, 17] |
| Intersection | -3 | 10 | [-3, 10] |

The number of integers is $10 - (-3) + 1 = 14$.

This confirms the algorithm correctly counts only values of $a$ that keep both variables inside range.

### Example 2

Input:

```

```

Here (M
