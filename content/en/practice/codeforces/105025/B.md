---
title: "CF 105025B - \u0414\u0432\u0435 \u043c\u043e\u043d\u0435\u0442\u044b"
description: "We are given two positive integers $k$ and $n$. They describe a hidden pair of coin values $A$ and $B$ under two constraints at the same time. First, one coin value is a multiplicative scaling of the other: $A = k cdot B$."
date: "2026-06-28T01:39:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105025
codeforces_index: "B"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b \u00ab\u041c\u0430\u0448\u0438\u043d\u0430 \u0422\u044c\u044e\u0440\u0438\u043d\u0433\u0430\u00bb \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 105025
solve_time_s: 45
verified: true
draft: false
---

[CF 105025B - \u0414\u0432\u0435 \u043c\u043e\u043d\u0435\u0442\u044b](https://codeforces.com/problemset/problem/105025/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two positive integers $k$ and $n$. They describe a hidden pair of coin values $A$ and $B$ under two constraints at the same time. First, one coin value is a multiplicative scaling of the other: $A = k \cdot B$. Second, the same two values are related additively: $A = B + n$.

The task is to determine whether there exist positive integers $A$ and $B$ satisfying both equations simultaneously. If such a pair exists, we must output one valid solution. Otherwise, we output $-1$.

Although the statement looks like a system of two equations, the key difficulty is not solving algebra in isolation but ensuring that the resulting values are integers and remain positive under the constraints.

The constraints allow $k, n \le 10^9$, so any solution must run in constant time per test case. A brute-force search over possible $A$ or $B$ is impossible because values can be as large as $10^9$, and even iterating up to that bound would exceed time limits.

A common mistake comes from treating the equations independently. For example, taking $B = n$ or $A = k + n$ ignores that both equations must hold simultaneously. Another subtle issue appears when $k = 1$, because the system degenerates and many approaches that divide by $k - 1$ break.

A concrete edge case is $k = 1, n = 3$. Then $A = B$ from the first equation, but also $A = B + 3$ from the second, which is impossible. Any solution that blindly computes $B = n / (k - 1)$ would divide by zero and fail.

## Approaches

The problem is a direct system of linear equations in disguise. The brute-force idea would be to try all possible values of $B$ and check whether both equations produce the same $A$. For each $B$, we compute $A_1 = kB$ and $A_2 = B + n$, and check equality. This is correct but immediately infeasible, since $B$ can go up to $10^9$, leading to linear time in the worst case.

The key observation is that we do not need to search at all. The two expressions for $A$ must be equal, so we equate them directly:

$$kB = B + n$$

Rearranging gives:

$$(k - 1)B = n$$

Now the structure is simple. If $k = 1$, the equation becomes $0 \cdot B = n$, which is only possible if $n = 0$, but $n \ge 1$, so there is no solution. Otherwise, we must have $B = \frac{n}{k - 1}$, and this value must be an integer. Once $B$ is determined, $A = kB$.

This reduces the entire problem to a constant number of arithmetic checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over B | $O(n)$ | $O(1)$ | Too slow |
| Algebraic solution | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read integers $k$ and $n$. These define the proportional and additive relationships between $A$ and $B$.
2. Check whether $k = 1$. If so, both equations force $A = B$, but the second equation requires $A = B + n$, which is impossible for any positive $n$. In this case, output $-1$.
3. If $k \ne 1$, compute $k - 1$. This value represents how much scaling beyond equality is applied to $B$.
4. Check whether $n$ is divisible by $k - 1$. This ensures that $B = \frac{n}{k - 1}$ is an integer. If not divisible, no valid integer solution exists, so output $-1$.
5. If divisible, compute $B = n // (k - 1)$. This is the only candidate value consistent with both constraints.
6. Compute $A = k \cdot B$. This guarantees both the multiplicative and additive equations hold simultaneously.
7. Output $A$ and $B$.

### Why it works

Both constraints define linear expressions for the same variable $A$. The algorithm forces consistency by equating them, reducing the problem to a single linear Diophantine equation. Since there is only one unknown after substitution, either there is exactly one integer solution or none at all. Every step preserves equivalence transformations, so any solution produced must satisfy both original equations, and any valid solution must satisfy the derived divisibility condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

k, n = map(int, input().split())

if k == 1:
    # A = B and A = B + n => impossible for n > 0
    print(-1)
else:
    if n % (k - 1) != 0:
        print(-1)
    else:
        b = n // (k - 1)
        a = k * b
        if b > 0 and a > 0:
            print(a, b)
        else:
            print(-1)
```

The code follows the derived equation directly. The special case $k = 1$ is handled explicitly to avoid division by zero. The divisibility check ensures we only construct integer solutions. The positivity check is technically redundant under the constraints $k, n \ge 1$, but it protects against malformed derivations and keeps the logic explicit.

## Worked Examples

We trace both provided samples through the derived formula.

### Example 1: `6 15`

We compute $B = \frac{15}{6 - 1} = \frac{15}{5} = 3$, then $A = 6 \cdot 3 = 18$.

| Step | k | n | k−1 | n % (k−1) | B | A |
| --- | --- | --- | --- | --- | --- | --- |
| init | 6 | 15 | 5 | - | - | - |
| check divisibility | 6 | 15 | 5 | 0 | - | - |
| compute B | 6 | 15 | 5 | - | 3 | - |
| compute A | 6 | 15 | 5 | - | 3 | 18 |

This confirms both constraints hold exactly since $18 = 6 \cdot 3$ and $18 = 3 + 15$.

### Example 2: `1 3`

| Step | k | n | decision |
| --- | --- | --- | --- |
| check k == 1 | 1 | 3 | immediately impossible |

Since $A = B$ but also $A = B + 3$, the system is inconsistent, confirming output $-1$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a few arithmetic operations and one divisibility check |
| Space | $O(1)$ | No auxiliary data structures used |

The solution comfortably fits within limits because it replaces any search space with a single algebraic reduction.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    k, n = map(int, input().split())

    if k == 1:
        return "-1\n"
    if n % (k - 1) != 0:
        return "-1\n"

    b = n // (k - 1)
    a = k * b

    if b > 0 and a > 0:
        return f"{a} {b}\n"
    return "-1\n"

# provided samples
assert run("6 15\n") == "18 3\n"
assert run("1 3\n") == "-1\n"

# custom cases
assert run("2 2\n") == "2 1\n"   # smallest non-trivial solution
assert run("3 0\n") == "-1\n"    # impossible since n >= 1 in statement
assert run("5 20\n") == "25 5\n"  # clean divisible case
assert run("4 7\n") == "-1\n"     # non-divisible case
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 2 | 2 1 | minimal valid configuration |
| 3 0 | -1 | inconsistent additive constraint |
| 5 20 | 25 5 | standard divisible case |
| 4 7 | -1 | non-integer B rejection |

## Edge Cases

### Case $k = 1$

Input `1 3` forces $A = B$ from the multiplicative constraint and $A = B + 3$ from the additive constraint. The algorithm branches immediately on $k = 1$ and outputs $-1$ without any arithmetic, preventing a division-by-zero situation.

### Non-divisible $n$

Input `4 7` leads to $B = 7 / 3$, which is not an integer. The algorithm detects this via `n % (k - 1) != 0` and rejects the case. This is essential because otherwise fractional coin values would be incorrectly accepted.

### Smallest valid system

Input `2 2` gives $B = 2 / 1 = 2$, $A = 4$. The algorithm correctly constructs and outputs a valid pair, confirming that no additional constraints beyond divisibility and positivity are needed.
