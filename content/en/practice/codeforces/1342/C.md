---
title: "CF 1342C - Yet Another Counting Problem"
description: "We are working with integers and modular arithmetic, but the structure becomes clearer if we think of the infinite number line as being colored by a periodic rule. For any integer $x$, we compute two values: first we take $x bmod a$, then reduce that result modulo $b$."
date: "2026-06-16T09:31:04+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1342
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 86 (Rated for Div. 2)"
rating: 1600
weight: 1342
solve_time_s: 290
verified: false
draft: false
---

[CF 1342C - Yet Another Counting Problem](https://codeforces.com/problemset/problem/1342/C)

**Rating:** 1600  
**Tags:** math, number theory  
**Solve time:** 4m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We are working with integers and modular arithmetic, but the structure becomes clearer if we think of the infinite number line as being colored by a periodic rule.

For any integer $x$, we compute two values: first we take $x \bmod a$, then reduce that result modulo $b$. In parallel, we also compute $x \bmod b$ followed by modulo $a$. If these two final results differ, we count $x$.

Each query gives a segment $[l, r]$, and we must count how many integers in that range satisfy this inequality condition.

The key difficulty is that $l$ and $r$ can be as large as $10^{18}$, so we cannot evaluate each number individually. The structure depends only on residues modulo $a$ and $b$, both of which are small (at most 200), which strongly suggests periodicity over some cycle related to $a$ and $b$.

A brute force idea would test every number in each query range. That already breaks immediately when a query interval is large. For example, if $l = 1$ and $r = 10^{18}$, iterating is impossible.

A more subtle issue is that even if we precompute values for a prefix, the pattern of equality depends on both mod $a$ and mod $b$, so we need a structured repetition argument rather than naive prefix simulation.

Edge cases appear when $a = b$. In that case both expressions are identical for all $x$, so the answer is always zero. A careless implementation that assumes periodic behavior without checking this will still work, but will waste computation or risk division edge confusion.

Another edge case is when one of $a$ or $b$ equals 1. Then one of the modulo chains collapses to zero, and the expression simplifies significantly. The implementation must still handle this cleanly inside a general formula.

## Approaches

The brute-force method evaluates the condition for every integer in every query interval. Each evaluation takes constant time, so a single query costs $O(r - l + 1)$, and in the worst case this is $10^{18}$. This is immediately infeasible.

The core observation is that the condition depends only on $x \bmod a$ and $x \bmod b$. These two residues repeat with period $a$ and $b$, so together the pair repeats with period $\mathrm{lcm}(a, b)$. Since $a, b \le 200$, this period is at most 40000, which is small enough to precompute.

We can therefore compute, for one full cycle of length $L = \mathrm{lcm}(a, b)$, how many values satisfy the condition. Then any prefix up to $x$ can be expressed as:

full cycles plus a remainder segment.

So we build a prefix array over one period and answer each query using two prefix evaluations.

This reduces each query to constant time after preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(\sum (r-l))$ | $O(1)$ | Too slow |
| Periodic prefix on LCM | $O(a \cdot b + q)$ per test | $O(a \cdot b)$ | Accepted |

## Algorithm Walkthrough

1. Compute $L = \mathrm{lcm}(a, b)$. This defines the repetition period of all relevant residue pairs because both modulo patterns repeat simultaneously after this length.
2. Build an array `bad[i]` for $i \in [1, L]$, where `bad[i] = 1` if $((i \bmod a) \bmod b) \ne ((i \bmod b) \bmod a)$, otherwise 0. This directly encodes whether each position contributes to the answer.
3. Build a prefix sum array `pref`, where `pref[i]` stores how many valid values are in $[1, i]$. This allows constant-time range counting inside the period.
4. Precompute `total = pref[L]`, the number of valid values in one full cycle. This lets us handle large ranges by splitting them into full cycles plus remainder.
5. To answer a query $[l, r]$, compute:

the number of valid values in $[1, r]$ minus the number in $[1, l-1]$. Each of these is computed using full cycles:

$$f(x) = (x // L) \cdot total + pref[x \bmod L]$$

with careful handling when $x \bmod L = 0$.

### Why it works

The value of the expression depends only on the pair $(x \bmod a, x \bmod b)$. Since both residues repeat independently with periods $a$ and $b$, the combined state repeats every $\mathrm{lcm}(a, b)$. This makes the indicator function periodic, so counting over large ranges reduces to counting over full cycles plus a fixed prefix, which preserves correctness for every integer interval.

## Python Solution

```python
import sys
input = sys.stdin.readline

def lcm(a, b):
    import math
    return a // math.gcd(a, b) * b

t = int(input())
for _ in range(t):
    a, b, q = map(int, input().split())
    L = lcm(a, b)

    bad = [0] * (L + 1)
    pref = [0] * (L + 1)

    for i in range(1, L + 1):
        x = i % a
        y = i % b
        if (x % b) != (y % a):
            bad[i] = 1
        pref[i] = pref[i - 1] + bad[i]

    total = pref[L]

    def calc(x):
        if x <= 0:
            return 0
        cycles = x // L
        rem = x % L
        return cycles * total + pref[rem]

    out = []
    for _q in range(q):
        l, r = map(int, input().split())
        out.append(str(calc(r) - calc(l - 1)))

    print(" ".join(out))
```

The implementation relies on explicitly building one full period of the function and using prefix sums to turn range queries into constant-time arithmetic.

The main subtlety is handling indexing correctly. The array is 1-based, so the prefix sum for a remainder uses `pref[rem]` directly, and full cycles multiply by `pref[L]`. Another important detail is using `l - 1` safely inside `calc`, where non-positive values must return zero.

## Worked Examples

We trace the first sample test case: $a = 4, b = 6$, with small queries.

Assume the period is $L = \mathrm{lcm}(4,6) = 12$.

We compute `bad[i]` over one cycle.

| i | i%4 | i%6 | (i%4)%6 | (i%6)%4 | bad |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 | 0 |
| 2 | 2 | 2 | 2 | 2 | 0 |
| 3 | 3 | 3 | 3 | 3 | 0 |
| 4 | 0 | 4 | 0 | 0 | 0 |
| 5 | 1 | 5 | 1 | 1 | 0 |
| 6 | 2 | 0 | 2 | 0 | 1 |
| 7 | 3 | 1 | 3 | 1 | 1 |
| 8 | 0 | 2 | 0 | 2 | 1 |
| 9 | 1 | 3 | 1 | 3 | 1 |
| 10 | 2 | 4 | 2 | 0 | 1 |
| 11 | 3 | 5 | 3 | 1 | 1 |
| 12 | 0 | 0 | 0 | 0 | 0 |

From this we get a prefix array and can answer queries. For example, query $[1, 7]$ gives sum of bad values in that range, which matches the sample output.

This trace confirms that the condition is not uniformly distributed and depends on residue interactions, but still repeats cleanly over the LCM.

A second example with $a = b$ shows a degenerate case. If $a = b = 5$, then for every $x$, both expressions are identical, so `bad[i] = 0` for all $i$. The prefix array remains zero, and every query returns zero regardless of range size.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t \cdot L + q)$ | Each test builds one cycle of size $L = \mathrm{lcm}(a,b)$ and answers queries in O(1) |
| Space | $O(L)$ | Prefix and marking arrays over one period |

Since $a, b \le 200$, the LCM is at most 40000, making preprocessing feasible even for multiple test cases, and queries are efficiently handled within constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    def solve():
        t = int(input())
        for _ in range(t):
            a, b, q = map(int, input().split())
            L = a * b // math.gcd(a, b)

            bad = [0] * (L + 1)
            pref = [0] * (L + 1)

            for i in range(1, L + 1):
                x = i % a
                y = i % b
                bad[i] = 1 if (x % b) != (y % a) else 0
                pref[i] = pref[i - 1] + bad[i]

            total = pref[L]

            def calc(x):
                if x <= 0:
                    return 0
                return (x // L) * total + pref[x % L]

            out = []
            for _ in range(q):
                l, r = map(int, input().split())
                out.append(str(calc(r) - calc(l - 1)))
            print(" ".join(out))

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    res = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return res.strip()

# provided sample
assert run("""2
4 6 5
1 1
1 3
1 5
1 7
1 9
7 10 2
7 8
100 200
""") == """0 0 0 2 4
0 91"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| $a=b$ case | all zeros | equality collapse |
| $a=1$ case | direct simplification | boundary modulo behavior |
| large range | stable repetition | LCM cycle correctness |
| small random | brute agreement | correctness of condition |

## Edge Cases

When $a = b$, every term evaluates identically because both expressions reduce to the same computation, so the algorithm’s marking array becomes entirely zero. The prefix sum remains constant and every query returns zero, matching the expected mathematical simplification.

When $a = 1$ or $b = 1$, one side of the expression collapses to zero for all $x$. The implementation still works because the modulo operations correctly produce constant residues, and the periodic structure degenerates to a trivial cycle of length equal to the other parameter.

When $l$ and $r$ span multiple full cycles plus a partial tail, the `calc` function splits the range cleanly into `(x // L)` full repetitions and a remainder segment. This avoids any dependence on alignment of query boundaries with cycle boundaries, ensuring correctness for arbitrary intervals.
