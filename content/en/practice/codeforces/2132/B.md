---
title: "CF 2132B - The Secret Number"
description: "We are given a number $n$ that was constructed in a very specific way. Someone secretly chose an integer $x$, then created another number $y$ by appending one or more zeros to the right of $x$. That means $y = x cdot 10^k$ for some $k ge 1$."
date: "2026-06-08T02:49:29+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 2132
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1043 (Div. 3)"
rating: 900
weight: 2132
solve_time_s: 98
verified: false
draft: false
---

[CF 2132B - The Secret Number](https://codeforces.com/problemset/problem/2132/B)

**Rating:** 900  
**Tags:** math  
**Solve time:** 1m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a number $n$ that was constructed in a very specific way. Someone secretly chose an integer $x$, then created another number $y$ by appending one or more zeros to the right of $x$. That means $y = x \cdot 10^k$ for some $k \ge 1$. Finally, they revealed only the sum $n = x + y$. Our task is to recover every possible original $x$ that could produce the given $n$.

So the structure is not arbitrary addition. It always has the form

$$n = x + x \cdot 10^k = x(1 + 10^k)$$

for some integer $k \ge 1$, and $x$ must be a positive integer. We are asked to find all such valid $x$ for each test case.

The constraints allow $n$ up to $10^{18}$ and up to $10^4$ test cases. That immediately rules out anything that tries all possible splits of digits or brute-forces candidates for $x$ up to $n$. Even $O(n)$ per test is impossible, and even $O(\sqrt{n})$ per test would be too slow in the worst case.

A subtle edge case comes from the fact that the construction depends on a power of ten shift. If we try to guess $k$ incorrectly or assume fixed-length splits of digits, we can miss valid solutions or overcount invalid ones.

For example, if $n = 1111$, valid answers exist:

- $x = 11$, since $11 + 1100 = 1111$
- $x = 101$, since $101 + 1010 = 1111$

A naive attempt that only checks prefix-suffix matches of equal length would miss $x = 11$. Conversely, checking all substrings as candidates for $x$ without enforcing the algebraic constraint would produce many invalid candidates.

## Approaches

A direct brute-force strategy would be to try every possible $x$ from $1$ to $n$, compute $y = n - x$, and check whether $y$ is equal to $x$ with some number of trailing zeros. This works because it directly enforces the definition, but it requires $O(n)$ checks per test case, which is impossible when $n$ can be as large as $10^{18}$.

Even if we optimize by only iterating over prefixes of digits of $n$, we still need to validate each candidate by division or string reconstruction, and the number of candidates remains proportional to the number of digits times possible shifts.

The key observation is that the structure $n = x(1 + 10^k)$ transforms the problem into a divisor search problem with a very special form. For each fixed $k$, the value $(1 + 10^k)$ is known, and $x$ must be exactly $n / (1 + 10^k)$ if divisible. Since $10^k$ grows exponentially, the number of valid $k$ is bounded by the number of digits of $n$, which is at most 18. This reduces the problem to checking only a small set of candidates.

We can therefore enumerate all possible $k$, compute the candidate denominator $d = 10^k + 1$, and test whether $n$ is divisible by $d$. If so, we recover $x$. This is efficient because the search space is logarithmic in $n$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over x | $O(n)$ | $O(1)$ | Too slow |
| Enumerate k (powers of 10) | $O(\log n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and prepare an empty list of answers. We will collect all valid $x$ values.
2. Iterate over possible values of $k$, starting from 1 while $10^k < n$. Each $k$ represents how many zeros were appended when forming $y = x \cdot 10^k$.
3. For each $k$, compute $d = 10^k + 1$. This comes directly from rewriting the equation $n = x(1 + 10^k)$.
4. Check whether $n \mod d = 0$. If not, no valid $x$ exists for this $k$, so continue.
5. If divisible, compute $x = n / d$. This is a candidate solution.
6. Store $x$ if it is positive. Since $d > 1$, positivity is guaranteed when division is exact, but we still keep the check conceptually.
7. After trying all $k$, sort the collected $x$ values and output them. Sorting is needed because different $k$ values may produce results in non-monotonic order.

### Why it works

Every valid construction satisfies $n = x(1 + 10^k)$ for some integer $k \ge 1$. Conversely, any $k$ for which $1 + 10^k$ divides $n$ yields a candidate $x$ that reconstructs a valid $y = x \cdot 10^k$. The algorithm enumerates all possible $k$, and for each one it either rejects or reconstructs exactly one possible $x$. No valid solution can be missed because every valid representation corresponds to exactly one such $k$, and no invalid solution can be added because divisibility enforces the original equation strictly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        res = []

        pow10 = 10
        k = 1

        while pow10 < n:
            d = pow10 + 1
            if n % d == 0:
                x = n // d
                res.append(x)
            pow10 *= 10
            k += 1

        if not res:
            print(0)
        else:
            res.sort()
            print(len(res))
            print(*res)

if __name__ == "__main__":
    solve()
```

The implementation follows the observation that only powers of ten matter. We maintain $10^k$ incrementally instead of recomputing it each time, which avoids unnecessary exponentiation overhead.

The loop stops when $10^k \ge n$ because beyond that point $1 + 10^k$ already exceeds $n$, making divisibility impossible.

Sorting at the end ensures the output order is correct even though larger $k$ does not necessarily correspond to smaller $x$.

## Worked Examples

### Example 1: $n = 1111$

We test increasing values of $k$.

| k | 10^k | d = 10^k + 1 | n mod d | x = n/d | valid |
| --- | --- | --- | --- | --- | --- |
| 1 | 10 | 11 | 0 | 101 | yes |
| 2 | 100 | 101 | 0 | 11 | yes |
| 3 | 1000 | 1001 | 1111 mod 1001 ≠ 0 | - | no |

Collected values are $\{101, 11\}$, which after sorting gives $11, 101$.

This demonstrates that different $k$ values correspond to different valid decompositions of the same number.

### Example 2: $n = 12$

| k | 10^k | d | n mod d | x | valid |
| --- | --- | --- | --- | --- | --- |
| 1 | 10 | 11 | 12 mod 11 = 1 | - | no |

No further $k$ is valid because $100 > 12$. The output is therefore empty.

This confirms that numbers not divisible by any $10^k + 1$ have no valid decomposition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t \log_{10} n)$ | For each test case we try at most one $k$ per digit length, up to 18 iterations |
| Space | $O(1)$ extra | Only a small list of candidates is stored per test |

The algorithm is easily fast enough because each test does only a handful of arithmetic operations, and even $10^4$ test cases remain well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        res = []

        pow10 = 10
        while pow10 < n:
            d = pow10 + 1
            if n % d == 0:
                res.append(n // d)
            pow10 *= 10

        if not res:
            out.append("0")
        else:
            res.sort()
            out.append(str(len(res)))
            out.append(" ".join(map(str, res)))

    return "\n".join(out)

# provided samples
assert run("""5
1111
12
55
999999999999999999
1000000000000000000
""") == """2
11 101
0
1
5
3
999999999 999000999000999 90909090909090909
0"""

# custom cases
assert run("""3
11
1010
1001
""") == """1
1
1
10
1
1"""

assert run("""1
1000000000000000000
""") == """0"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Small exact match cases | Single valid decomposition | correctness of basic division |
| Large power-of-ten boundary | 0 | ensures stopping condition works |
| Mixed structure numbers | multiple candidates or none | enumeration correctness |

## Edge Cases

One important edge case is when $n$ is exactly a power of ten or close to it. For example, $n = 1000000000000000000$. The algorithm iterates $k$, but every $10^k + 1$ either exceeds $n$ or does not divide it. The loop stops early, and no candidates are produced, correctly outputting 0.

Another edge case is when multiple values of $k$ produce valid results. For $n = 1111$, both $k = 1$ and $k = 2$ work. The algorithm naturally collects both because each $k$ is tested independently, and sorting ensures correct output order.

A final subtle case is when divisibility holds but the computed $x$ is not meaningful under the original construction. This cannot happen because $n \mod (10^k + 1) = 0$ implies exact algebraic reconstruction $n = x(1 + 10^k)$, which uniquely determines a valid $y = x \cdot 10^k$, preserving the required structure without additional checks.
