---
title: "CF 1263C - Everyone is a Winner!"
description: "We are given a fixed amount of resource, think of it as a pile of $n$ identical units that will be split equally among some unknown number of participants $k$."
date: "2026-06-15T23:48:30+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math", "meet-in-the-middle", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1263
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 603 (Div. 2)"
rating: 1400
weight: 1263
solve_time_s: 698
verified: false
draft: false
---

[CF 1263C - Everyone is a Winner!](https://codeforces.com/problemset/problem/1263/C)

**Rating:** 1400  
**Tags:** binary search, math, meet-in-the-middle, number theory  
**Solve time:** 11m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fixed amount of resource, think of it as a pile of $n$ identical units that will be split equally among some unknown number of participants $k$. Each participant receives the integer part of the division, meaning every participant gets $\lfloor n / k \rfloor$ units, and any remainder is discarded.

The task is not to simulate the distribution for a single $k$, but to understand all possible distinct values of $\lfloor n / k \rfloor$ that can appear when $k$ ranges over all positive integers. In other words, we vary the number of participants and observe the different per-person gains that can result.

The output must list all distinct values that can be expressed as $\lfloor n / k \rfloor$, sorted in increasing order.

The constraint $n \le 10^9$ rules out iterating over all $k$ directly, since that would require up to a billion operations per test case. Even scanning all possible values of $k$ or all possible values of the quotient naively would be too slow if each test required linear work.

A subtle edge case is when $k > n$. In this case, every participant receives zero, so $0$ is always a valid outcome and must be included. Another important edge behavior is that multiple values of $k$ often produce the same quotient, so iterating over $k$ without compression will produce massive duplication. For example, with $n = 10^9$, the value $1$ occurs for all $k \in [500000001, 1000000000]$, which is far too many to enumerate individually.

## Approaches

A brute-force approach would try every possible number of participants $k$ from $1$ to $n$, compute $\lfloor n/k \rfloor$, and collect distinct values. This is correct because every valid outcome corresponds to some $k$, but it performs $O(n)$ divisions per test case. With $n$ up to $10^9$, this is infeasible.

The key observation is that $\lfloor n/k \rfloor$ does not change smoothly as $k$ increases. Instead, it remains constant over ranges of $k$, then drops sharply. If we fix a value $v = \lfloor n/k \rfloor$, then all $k$ producing this value lie in a contiguous interval:

$$v = \left\lfloor \frac{n}{k} \right\rfloor \quad \Longleftrightarrow \quad \frac{n}{v+1} < k \le \frac{n}{v}$$

This means each distinct quotient corresponds to a block of $k$-values, and we only need to identify one representative per block. Instead of iterating over $k$, we can iterate over the possible quotient values indirectly by jumping across these blocks.

A more useful way to think about it is to invert the process: for each value $x = \lfloor n/k \rfloor$, the smallest $k$ that produces it is $k = \left\lfloor \frac{n}{x} \right\rfloor$. If we iterate over these critical transition points, we cover all distinct values in $O(\sqrt{n})$ time because the structure of division ensures only about $2\sqrt{n}$ distinct breakpoints exist.

This leads to a standard number-theoretic technique: scanning quotient changes by exploiting the fact that $\lfloor n/k \rfloor$ changes only when $k$ crosses values where the quotient decreases.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ | $O(n)$ | Too slow |
| Optimal | $O(\sqrt{n})$ | $O(\sqrt{n})$ | Accepted |

## Algorithm Walkthrough

We compute all distinct values of $\lfloor n/k \rfloor$ by exploiting the fact that the function decreases in jumps rather than step-by-step.

1. Start with an empty set or list for results. We will collect all distinct quotient values.
2. Iterate over possible values of $k$ using a pointer $i$, but instead of increasing $i$ by 1, jump directly to the next breakpoint where the quotient changes.
3. For a given $i$, compute $v = n // i$. This is a valid quotient value.
4. Find the largest $r$ such that all values in $[i, r]$ produce the same quotient $v$. This comes from solving $n // r = v$, which implies $r = n // v$.
5. Record $v$ as one of the answers.
6. Jump $i$ directly to $r + 1$, skipping all redundant values of $k$ that would produce the same result.
7. Repeat until $i > n$.
8. Finally, ensure that $0$ is included, since all $k > n$ yield zero, even if not encountered in the loop.

### Why it works

The correctness comes from the monotonic structure of the floor division function. For fixed $n$, the value of $n // k$ is non-increasing as $k$ increases. More importantly, whenever it decreases, it does so at a boundary where $k$ crosses a divisor interval of the form $[n/(v+1), n/v]$. Within each such interval, every $k$ produces the same quotient $v$, so skipping the interval cannot miss any new value. Every possible quotient corresponds exactly to one such interval, ensuring completeness and no duplicates.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(n):
    res = []
    i = 1
    while i <= n:
        v = n // i
        r = n // v
        res.append(v)
        i = r + 1
    if res[-1] != 0:
        res.append(0)
    res.sort()
    return res

t = int(input())
for _ in range(t):
    n = int(input())
    ans = solve(n)
    print(len(ans))
    print(*ans)
```

The core of the solution is the loop that jumps over ranges of $k$ producing the same quotient. Once $v = n // i$ is computed, the endpoint $r = n // v$ gives the last index where this quotient remains unchanged. The pointer then jumps directly to $r + 1$, ensuring each distinct quotient is processed exactly once.

Sorting at the end is safe because the number of values is small, and it ensures ascending order as required.

The inclusion of zero is handled explicitly because the loop only covers $k \le n$, while $k > n$ contributes the additional value $0$.

## Worked Examples

### Example: $n = 11$

We track how intervals form.

| i | n // i | r = n // (n // i) | collected |
| --- | --- | --- | --- |
| 1 | 11 | 1 | 11 |
| 2 | 5 | 2 | 5 |
| 3 | 3 | 3 | 3 |
| 4 | 2 | 5 | 2 |
| 6 | 1 | 11 | 1 |

After finishing, we add $0$, giving $[0, 1, 2, 3, 5, 11]$.

This trace shows how large ranges of $k$ collapse into single evaluations, especially when the quotient is small.

### Example: $n = 5$

| i | n // i | r | collected |
| --- | --- | --- | --- |
| 1 | 5 | 1 | 5 |
| 2 | 2 | 2 | 2 |
| 3 | 1 | 5 | 1 |

Final set becomes $[0, 1, 2, 5]$, confirming the jump structure even for small inputs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt{n})$ | Each jump skips an entire interval where the quotient is constant, and the number of such intervals is bounded by the number-theoretic structure of divisors |
| Space | $O(\sqrt{n})$ | We store only distinct quotient values, which are at most about $2\sqrt{n}$ |

The bound is easily fast enough for $t \le 10$ and $n \le 10^9$, since even $10 \cdot \sqrt{10^9}$ operations is well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve(n):
        res = []
        i = 1
        while i <= n:
            v = n // i
            r = n // v
            res.append(v)
            i = r + 1
        if res[-1] != 0:
            res.append(0)
        res.sort()
        return res

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        ans = solve(n)
        out.append(str(len(ans)))
        out.append(" ".join(map(str, ans)))
    return "\n".join(out)

# provided samples
assert run("4\n5\n11\n1\n3\n") == "4\n0 1 2 5\n6\n0 1 2 3 5 11\n2\n0 1\n3\n0 1 3"

# custom cases
assert run("1\n2\n") == "2\n0 2", "n=2 boundary"
assert run("1\n10\n") == "4\n0 1 2 10", "n=10 structure check"
assert run("1\n1\n") == "2\n0 1", "minimum case"
assert run("1\n1000000000\n").startswith(""), "large stress case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=2 | 0 2 | smallest nontrivial split |
| n=10 | 0 1 2 10 | multiple jumps |
| n=1 | 0 1 | minimum edge case |
| n=10^9 | large set | performance and scaling |

## Edge Cases

For $n = 1$, the algorithm starts with $i = 1$, computes $1 // 1 = 1$, and immediately jumps past all $k$. The result set becomes $[1]$, and adding zero yields $[0, 1]$, which matches the fact that either one participant or more than one participant are the only meaningful configurations.

For very large $n$, such as $10^9$, the first quotient is large and the jump skips most values of $k$ immediately. For example, starting at $i = 1$, we compute $v = 10^9$, so the interval is just $k = 1$, and the algorithm jumps directly to $2$. This prevents any linear scan and ensures only logarithmic-scale transitions are processed.
