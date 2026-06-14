---
title: "CF 1549A - Gregor and Cryptography"
description: "We are given a prime number $P$, and for each test case we must output two integers $a$ and $b$ such that both lie between 2 and $P$, with $a < b$, and the remainders when dividing $P$ by $a$ and by $b$ are equal."
date: "2026-06-14T20:17:59+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1549
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 736 (Div. 2)"
rating: 800
weight: 1549
solve_time_s: 221
verified: false
draft: false
---

[CF 1549A - Gregor and Cryptography](https://codeforces.com/problemset/problem/1549/A)

**Rating:** 800  
**Tags:** math, number theory  
**Solve time:** 3m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a prime number $P$, and for each test case we must output two integers $a$ and $b$ such that both lie between 2 and $P$, with $a < b$, and the remainders when dividing $P$ by $a$ and by $b$ are equal.

In more concrete terms, we are looking for two different divisors that leave the same “leftover amount” when used to divide the same prime number. We are not required to find all such pairs, only one valid pair per test case.

The constraints are large in value but small in structure. The number of test cases is up to 1000, and each $P$ can be as large as $10^9$. That immediately rules out any approach that tries to search all pairs $(a, b)$ or even tries all values of $a$ and computes remainders repeatedly. A quadratic or even linear scan per test case is unnecessary but still feasible in theory; however, the real constraint is that we want a constant-time construction per test case.

A subtle edge case is the smallest allowed prime $P = 5$. Any construction must still respect $2 \le a < b \le P$. A naive attempt to pick something like $(P-2, P-1)$ can fail for small values if not checked carefully, because the ordering and remainder equality may not hold universally for arbitrary patterns.

## Approaches

A brute-force approach would try all pairs $(a, b)$ with $2 \le a < b \le P$ and check whether $P \bmod a = P \bmod b$. This is correct because it directly enforces the condition. However, it examines roughly $O(P^2)$ pairs, which is impossible when $P$ is up to $10^9$. Even restricting to a single test case makes this infeasible.

A more structured observation comes from understanding what the condition actually means. If two moduli produce the same remainder when dividing the same number, then the number can be expressed in the form $P = k a + r = \ell b + r$ for some shared remainder $r$. The key simplification is that we do not need to control the remainder at all; we only need it to match.

The trick is to deliberately force a simple, shared remainder. For any odd prime $P$, choosing $a = 2$ makes $P \bmod 2 = 1$. If we can find another $b$ such that $P \bmod b = 1$, we are done. The simplest such choice is $b = P - 1$, because dividing $P$ by $P - 1$ always leaves remainder 1.

This reduces the problem to a constant-time construction per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(P^2)$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the prime number $P$. We process each test case independently since there is no interaction between cases.
2. Fix $a = 2$. This is the smallest valid choice and guarantees a predictable remainder pattern for any odd prime.
3. Set $b = P - 1$. This choice ensures that $b$ is always within bounds and strictly larger than 2 for all $P \ge 5$.
4. Output $a$ and $b$.

The reason this construction is valid comes from the arithmetic properties of division. Since $P$ is an odd prime greater than 2, dividing by 2 always leaves remainder 1. On the other hand, dividing $P$ by $P - 1$ always yields quotient 1 and remainder 1 as well, because $P = 1 \cdot (P - 1) + 1$. This guarantees the required equality of remainders.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        p = int(input())
        print(2, p - 1)

if __name__ == "__main__":
    main()
```

The implementation is direct because the construction is constant time per test case. There is no need for loops, searches, or primality checks since the input guarantees that $P$ is prime.

The only subtlety is ensuring that $p - 1$ is always valid. Since $P \ge 5$, we always have $p - 1 \ge 4$, so it safely exceeds 2 and maintains $a < b$.

## Worked Examples

### Example 1

Input:

```
P = 17
```

We apply the construction $a = 2$, $b = 16$.

| Step | a | b | P mod a | P mod b |
| --- | --- | --- | --- | --- |
| Initialization | 2 | 16 |  |  |
| Compute remainders | 2 | 16 | 1 | 1 |

Both remainders match, so the pair is valid.

This confirms that the construction does not depend on special properties of 17, only on the structure of division.

### Example 2

Input:

```
P = 5
```

We again use $a = 2$, $b = 4$.

| Step | a | b | P mod a | P mod b |
| --- | --- | --- | --- | --- |
| Initialization | 2 | 4 |  |  |
| Compute remainders | 2 | 4 | 1 | 1 |

Even at the smallest valid input size, the construction holds because 5 divided by 2 and by 4 both leave remainder 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | Each test case outputs a constant-time construction |
| Space | $O(1)$ | No auxiliary storage beyond input variables |

The solution runs comfortably within limits because it performs only two integer operations and one print per test case, making it linear in the number of test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        p = int(input())
        out.append(f"{2} {p-1}")
    return "\n".join(out) + "\n"

# provided samples
assert run("2\n17\n5\n") == "2 16\n2 4\n", "sample case"

# custom cases
assert run("1\n7\n") == "2 6\n", "small prime"
assert run("1\n11\n") == "2 10\n", "medium prime"
assert run("1\n5\n") == "2 4\n", "minimum boundary"
assert run("3\n5\n7\n13\n") == "2 4\n2 6\n2 12\n", "multiple cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 7 | 2 6 | correctness on small prime |
| 1, 11 | 2 10 | general mid-range behavior |
| 1, 5 | 2 4 | minimum constraint handling |
| 3 cases | multiple outputs | repeated test stability |

## Edge Cases

The most important edge case is the smallest prime $P = 5$. In this case, the only valid construction must still satisfy strict inequalities. The algorithm produces $(2, 4)$, and checking directly shows both remainders equal to 1, so the constraint is satisfied without needing any special handling.

Another implicit edge case is any large prime close to $10^9$. Even there, $P - 1$ remains valid and distinct from 2, so the construction does not break due to overflow or ordering issues.
