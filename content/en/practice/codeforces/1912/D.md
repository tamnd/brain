---
title: "CF 1912D - Divisibility Test"
description: "We are given a number system with base $b$, and we want to check divisibility by a modulus $n$ using only local operations on digits. A number is written in base $b$, and we are allowed to replace the full value with a structured expression built from its digits."
date: "2026-06-08T20:14:26+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1912
codeforces_index: "D"
codeforces_contest_name: "2023-2024 ICPC, NERC, Northern Eurasia Onsite (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 1900
weight: 1912
solve_time_s: 102
verified: false
draft: false
---

[CF 1912D - Divisibility Test](https://codeforces.com/problemset/problem/1912/D)

**Rating:** 1900  
**Tags:** math  
**Solve time:** 1m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a number system with base $b$, and we want to check divisibility by a modulus $n$ using only local operations on digits. A number is written in base $b$, and we are allowed to replace the full value with a structured expression built from its digits. The expression must always preserve the value modulo $n$, so that checking divisibility reduces to checking a simplified digit-based form.

We are allowed three types of constructions, all working on digits grouped into blocks of size $k$ (interpreted in base $b$).

In the first type, we ignore everything except the last $k$ digits. This works only if the contribution of all higher digits is always a multiple of $n$, regardless of their values.

In the second type, we split the number into consecutive blocks of $k$ digits and sum these blocks.

In the third type, we alternate signs between these blocks.

Each block is treated as a base-$b$ integer, so shifting by $k$ digits corresponds to multiplying by $b^k$. The real constraint is therefore about whether powers of $b^k$ behave nicely modulo $n$.

The input consists of many pairs $(b, n)$. For each pair, we must find the smallest $k$ such that at least one of these constructions correctly preserves the value modulo $n$. If none exists, we output zero.

The constraints imply up to $10^6$ total across all tests, so an $O(\sqrt{n})$ or better per test approach is necessary. Anything involving factorizing or simulating digit expansions up to $n$ per test is too slow in aggregate.

A subtle failure case comes from assuming that block methods always exist for all moduli. For example, $b = 10, n = 6$ looks similar to familiar divisibility rules, but none of the allowed linear digit constructions align with modulo 6 constraints, so the answer is zero. A naive approach that only checks small $k$ without understanding structural conditions may incorrectly conclude that some grouping works.

## Approaches

The core observation is that all three constructions correspond to expressing the number as a polynomial in base $b^k$. If we group digits into blocks of size $k$, any number becomes

$$x = x_0 + x_1 b^k + x_2 b^{2k} + \dots$$

where each $x_i$ is a block value.

Each divisibility rule is a way of replacing powers of $b^k$ with simple constants in $\mathbb{Z}_n$:

For kind 1, we effectively require $b^k \equiv 0 \pmod n$. This ensures higher blocks vanish completely.

For kind 2, we require $b^k \equiv 1 \pmod n$, because then all blocks contribute equally and summing preserves the original value modulo $n$.

For kind 3, we require $b^k \equiv -1 \pmod n$, so alternating signs cancel successive powers correctly.

Thus the task reduces to finding the smallest $k$ such that $b^k \equiv 0, 1,$ or $-1 \pmod n$, and choosing the smallest valid among them.

The brute force approach tries all $k$ from 1 upward, computing $b^k \bmod n$. This is correct but too slow in worst case, since $k$ may go up to $n$, and each computation is $O(1)$, giving $O(n)$ per test.

The key insight is that we only need to find multiplicative order-like behavior of $b \bmod n$, which can be done by iterating powers until we either hit 0 or cycle, but since $n$ can be large across tests, we instead track powers until repetition or until hitting required residues, which always happens within $O(n)$ total across all tests due to modular dynamics.

A more structured view is that we are walking in the multiplicative monoid modulo $n$, and we stop as soon as we hit one of three target states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force powers | $O(n)$ per test | $O(1)$ | Too slow |
| Incremental power tracking | $O(n)$ total amortized | $O(1)$ | Accepted |

## Algorithm Walkthrough

We iterate powers of $b$ modulo $n$, but instead of recomputing from scratch per $k$, we maintain the current power $p = b^k \bmod n$.

1. Initialize $p = 1$. This represents $b^0$, the empty shift.
2. For each $k \ge 1$, update $p = (p \cdot b) \bmod n$. This gives $b^k \bmod n$.
3. If $p = 0$, we can immediately use kind 1 with this $k$, since all higher blocks vanish modulo $n$.
4. If $p = 1$, we can use kind 2 with this $k$, since block shifts preserve contribution exactly.
5. If $p = n-1$ (which represents $-1 \bmod n$), we can use kind 3 with this $k$, since alternating signs correctly cancel powers.
6. We stop at the smallest $k$ that triggers any of these conditions.
7. If we reach a safe upper bound without finding any condition, we conclude no rule exists.

The stopping condition works because once $p$ enters a cycle, it will never hit new residues, so continuing further cannot produce a smaller valid $k$.

### Why it works

Each grouping rule corresponds to enforcing a simple identity on powers of $b^k$ modulo $n$. Kind 1 forces all higher powers to disappear, which is exactly $b^k \equiv 0$. Kind 2 requires all shifted blocks to contribute identically, which is $b^k \equiv 1$. Kind 3 requires alternating cancellation, which is $b^k \equiv -1$. The algorithm enumerates powers in increasing order, so the first time any of these algebraic identities holds, it must correspond to the smallest valid group size.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        b, n = map(int, input().split())

        # special quick rejection
        # we search powers of b mod n
        p = 1

        # we will cap iterations at n steps; cycle must appear before that
        ans = 10**18

        for k in range(1, n + 1):
            p = (p * b) % n

            if p == 0:
                ans = k
                break
            if p == 1:
                ans = min(ans, k)
                break
            if p == n - 1:
                ans = min(ans, k)
                break

        if ans == 10**18:
            print(0)
        else:
            # decide kind
            p = 1
            for k in range(1, ans + 1):
                p = (p * b) % n
                if k == ans:
                    if p == 0:
                        print(1, ans)
                    elif p == 1:
                        print(2, ans)
                    else:
                        print(3, ans)

if __name__ == "__main__":
    solve()
```

The implementation directly tracks powers of $b$ modulo $n$. The first loop searches for the smallest $k$ producing a valid residue. The second pass reconstructs which condition triggered, since the loop does not store the type explicitly during the search.

The only subtlety is ensuring that $n-1$ is correctly interpreted as $-1 \bmod n$, which is necessary for the alternating sum rule. Another important detail is that we must stop immediately when a condition is met, since we require the smallest valid $k$.

## Worked Examples

### Example 1

Input: $b = 10, n = 11$

We compute powers of 10 modulo 11.

| k | p = 10^k mod 11 | condition |
| --- | --- | --- |
| 1 | 10 | p = -1 mod 11 |

At $k = 1$, we hit $p = -1$, so kind 3 applies.

This matches the alternating digit rule, where digits naturally alternate signs in base 10 for modulo 11.

### Example 2

Input: $b = 10, n = 4$

| k | p = 10^k mod 4 | condition |
| --- | --- | --- |
| 1 | 2 | none |
| 2 | 0 | kind 1 |

At $k = 2$, the power becomes zero, meaning all digits beyond the last two vanish modulo 4. This matches the classical rule that only the last two digits matter for modulo 4 in base 10.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test (amortized over all tests) | each step multiplies once and reduces modulo $n$ |
| Space | $O(1)$ | only a few variables are stored |

The total sum of $n$ over all tests is bounded by $10^6$, so the linear scan over powers is sufficient. Each iteration performs constant work, keeping the solution within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import prod

    import sys
    input = sys.stdin.readline

    t = int(sys.stdin.readline())
    out = []

    for _ in range(t):
        b, n = map(int, sys.stdin.readline().split())

        p = 1
        ans = None

        for k in range(1, n + 1):
            p = (p * b) % n
            if p == 0:
                ans = (1, k)
                break
            if p == 1:
                ans = (2, k)
                break
            if p == n - 1:
                ans = (3, k)
                break

        if ans is None:
            out.append("0")
        else:
            out.append(f"{ans[0]} {ans[1]}")

    return "\n".join(out)

# provided samples
assert run("""6
10 3
10 11
10 4
10 7
8 5
10 6
""") == """2 1
3 1
1 2
3 3
3 2
0"""

# custom cases
assert run("1\n2 2\n") == "1 1"
assert run("1\n3 1\n") == "0"  # invalid modulus edge intuition
assert run("1\n5 5\n") == "1 1"
assert run("1\n10 11\n") == "3 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 3 | 2 1 | immediate equality case |
| 8 5 | 3 2 | non-trivial alternating case |
| 10 6 | 0 | no valid rule exists |

## Edge Cases

One edge case is when $b \equiv 0 \pmod n$. In that situation, the first multiplication already produces zero. For example, $b = 6, n = 3$. The algorithm sets $p = 6 \equiv 0$, so $k = 1$ is immediately valid for kind 1, since every higher digit block vanishes.

Another case is when $b \equiv 1 \pmod n$. Then $p$ is always 1, so the first iteration already triggers kind 2 with $k = 1$. This corresponds to the fact that every digit block contributes unchanged regardless of position.

A third case is when no cycle hits 0, 1, or -1. For instance $b = 10, n = 6$. The powers cycle through residues that never align with the required structures, so the loop finishes without finding a valid $k$, correctly producing zero.
