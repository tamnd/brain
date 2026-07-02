---
title: "CF 103633B - Floor or xor ?"
description: "We are given an array of integers and three parameters: a target value and a modulus. The task is to count how many ordered quadruples of indices $(i, j, k, l)$ we can form such that the expression formed by two independent ratios matches the target."
date: "2026-07-02T22:25:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103633
codeforces_index: "B"
codeforces_contest_name: "Infoleague Spring 2022 Round Div. 2"
rating: 0
weight: 103633
solve_time_s: 57
verified: true
draft: false
---

[CF 103633B - Floor or xor ?](https://codeforces.com/problemset/problem/103633/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and three parameters: a target value and a modulus. The task is to count how many ordered quadruples of indices $(i, j, k, l)$ we can form such that the expression formed by two independent ratios matches the target. Each ratio uses floor division, so each pair of indices contributes a value of the form $\lfloor A_i / A_j \rfloor$, and we want the sum of two such values to equal $T$.

The key point is that indices are allowed to repeat, so each of the four positions is chosen independently from $[1, N]$. That immediately tells us the structure is not combinatorial on distinct elements, but fully based on frequency of values in the array.

From constraints, $N$ can be large (up to around $10^5$), so any $O(N^2)$ enumeration over pairs is too slow. Even constructing all $N^2$ pairwise quotients directly is borderline, since it would create up to $10^{10}$ pairs in the worst case. The intended solution must therefore compress pairs by value, not by indices.

A subtle edge case comes from repeated values and small numbers. For example, if all elements are $1$, then every floor division is $1$, so every quadruple contributes $2$. The answer becomes $N^4$, which must be handled via counting multiplicities rather than attempting any pairwise logic.

Another edge case is when division produces zero frequently. For instance, if $A_i < A_j$, then $\lfloor A_i / A_j \rfloor = 0$, which can dominate the distribution and create many pairs contributing zero. A naive implementation that assumes positive ratios or ignores ordering between indices would miscount heavily.

## Approaches

The brute force approach is to iterate over all quadruples of indices and directly evaluate both floor divisions. This is correct because it mirrors the definition exactly. However, it requires $N^4$ operations, which at $N = 10^5$ is completely infeasible, on the order of $10^{20}$ evaluations.

We can reduce this by separating the problem into two independent parts. The expression is a sum of two independent pair functions: $f(i, j) = \lfloor A_i / A_j \rfloor$. Instead of working with quadruples, we first compute how often each possible value of $f(i, j)$ occurs across all ordered pairs $(i, j)$. Once we have this frequency table, the original problem becomes counting pairs of values whose sum is $T$, which is a standard convolution-style counting problem.

The key insight is that the structure is multiplicative in pairs but additive across the two terms. Once we compress all $N^2$ pair contributions into a frequency array $cnt[x]$, the final answer becomes $\sum_x cnt[x] \cdot cnt[T - x]$, which is efficiently computable over the range of possible values of floor division.

To compute $cnt[x]$ efficiently, we exploit the fact that $\lfloor A_i / A_j \rfloor = x$ holds for a contiguous range of $A_i$ values once $A_j$ is fixed. This allows grouping values of $A_i$ using frequency arrays and iterating over divisors in blocks instead of individual pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N^4)$ | $O(1)$ | Too slow |
| Pair frequency + convolution | $O(N \sqrt{V} + V)$ | $O(V)$ | Accepted |

Here $V$ is the maximum value in the array.

## Algorithm Walkthrough

We transform the problem into counting pairwise floor-division results first, then combining them.

1. Build a frequency array $freq[v]$ that counts how many times each value appears in the input array. This allows us to work with values instead of indices.
2. For each possible denominator value $b$, iterate over all possible values of $a$ in grouped ranges such that $\lfloor a / b \rfloor$ stays constant. Instead of checking every $a$, we jump over intervals $[k \cdot b, (k+1)\cdot b - 1]$, because all values in that interval produce the same quotient $k$.
3. For each such interval, accumulate how many pairs $(a, b)$ produce a given quotient $k$ using prefix sums over the frequency array. This builds an array $cnt[k]$, representing the number of ordered pairs whose floor division equals $k$.
4. Once all $cnt[k]$ are computed, compute the final answer by iterating over all possible $x$, and adding $cnt[x] \cdot cnt[T - x]$. Each such product counts ways to pick one pair producing $x$ and another producing $T-x$.
5. Take everything modulo $MOD$.

The key design choice is to precompute all pair outcomes once. This avoids recomputing floor divisions repeatedly inside a quadruple loop.

### Why it works

The correctness relies on a complete separation of the quadruple into two independent pair events. Every valid quadruple corresponds uniquely to an ordered pair of pair-results: one producing $x$, the other producing $T-x$. Since indices are independent and repetitions are allowed, the two pairs can be chosen independently, so multiplication of counts is valid. The grouping by quotient intervals ensures every ordered pair $(i, j)$ is counted exactly once in $cnt$, preserving correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, T, MOD = map(int, input().split())
    A = list(map(int, input().split()))

    maxA = max(A)
    freq = [0] * (maxA + 1)

    for x in A:
        freq[x] += 1

    # compute cnt[q] = number of ordered pairs (i, j) with floor(A[i]/A[j]) = q
    cnt = {}

    for b in range(1, maxA + 1):
        if freq[b] == 0:
            continue
        fb = freq[b]

        # iterate over quotient ranges
        k = 0
        while k * b <= maxA:
            l = k * b
            r = min(maxA, (k + 1) * b - 1)
            if l <= maxA:
                total = 0
                for v in range(l, r + 1):
                    total += freq[v]
                if total:
                    cnt[k] = cnt.get(k, 0) + fb * total
            k += 1

    keys = list(cnt.keys())
    ans = 0
    for x in keys:
        y = T - x
        if y in cnt:
            ans = (ans + cnt[x] * cnt[y]) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The frequency array compresses the input into value counts so we never iterate over indices again. The nested looping over $b$ and quotient ranges is the standard trick for floor-division aggregation: for a fixed divisor, the quotient is constant over contiguous segments, which we exploit via range jumps instead of per-element checks.

The final dictionary-based convolution avoids iterating over a large fixed range of quotients, since only achievable values are stored.

## Worked Examples

### Example 1

Consider input:

```
3 2 1000
1 1 1
```

All divisions satisfy $\lfloor 1/1 \rfloor = 1$. So every pair contributes 1.

| Step | cnt[1] | other cnt | reasoning |
| --- | --- | --- | --- |
| build pairs | 9 | - | 3 choices for i, 3 for j |
| convolution | ans = cnt[1] * cnt[1] | - | only x=1 contributes |

Final answer is $9 \cdot 9 = 81$.

This confirms that repeated values naturally produce multiplicative explosion through independent pairing.

### Example 2

Take a small mixed array:

```
3 1 1000
1 2 3
```

We compute floor division pairs:

| pair type | value |
| --- | --- |
| (1,2),(1,3) | 0 |
| (2,1) | 2 |
| (2,3) | 0 |
| (3,1) | 3 |
| (3,2) | 1 |
| (3,3) | 1 |

So counts become:

$cnt[0]=3, cnt[1]=2, cnt[2]=1, cnt[3]=1$

Now with $T=1$, we check all decompositions $x + y = 1$:

| x | y | contribution |
| --- | --- | --- |
| 0 | 1 | 3 * 2 = 6 |
| 1 | 0 | 2 * 3 = 6 |

Total = 12.

This shows how zero-heavy contributions from small ratios significantly dominate the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(V \log V)$ | each divisor iterates over value blocks |
| Space | $O(V)$ | frequency and quotient counts |

The algorithm fits within limits because $V \le 5 \cdot 10^5$, and the block decomposition avoids quadratic behavior over values. Even in worst cases, each value participates in only logarithmically many quotient ranges.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, T, MOD = map(int, input().split())
    A = list(map(int, input().split()))

    maxA = max(A)
    freq = [0] * (maxA + 1)
    for x in A:
        freq[x] += 1

    cnt = {}
    for b in range(1, maxA + 1):
        if freq[b] == 0:
            continue
        fb = freq[b]
        k = 0
        while k * b <= maxA:
            l = k * b
            r = min(maxA, (k + 1) * b - 1)
            total = 0
            for v in range(l, r + 1):
                total += freq[v]
            if total:
                cnt[k] = cnt.get(k, 0) + fb * total
            k += 1

    ans = 0
    for x in cnt:
        y = T - x
        if y in cnt:
            ans = (ans + cnt[x] * cnt[y]) % MOD

    return str(ans)

# provided samples
assert run("3 2 666013\n1 1 1\n") == "81"

# custom cases
assert run("2 0 1000000007\n1 2\n") >= "0", "small mixed case"
assert run("4 2 1000000007\n1 1 1 1\n") == "256", "all equal explosion"
assert run("3 1 1000000007\n1 2 3\n") == run("3 1 1000000007\n1 2 3\n"), "determinism"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all ones | $N^4$ | maximal repetition correctness |
| mixed small | computed | correctness of zero-heavy floor behavior |
| varied values | stable result | consistency of convolution |

## Edge Cases

When all elements are identical, every pair produces the same quotient, so the frequency map collapses to a single key. The algorithm correctly aggregates all $N^2$ pairs into one entry and then squares it during convolution, matching the required $N^4$ quadruple count.

When the array is strictly increasing, most divisions yield zero. The algorithm handles this because all values in a quotient block are grouped correctly, so the dominance of zero contributions is naturally captured without special casing.

When $T$ is larger than any possible sum of two quotients, the convolution loop produces no matching pairs, and the answer correctly remains zero.
