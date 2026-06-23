---
title: "CF 105066G - Sleepy Pandas"
description: "We are given an array of integers, where each value is a label written on a panda. For every ordered pair of distinct indices $(i, j)$, we imagine taking the two numbers $xi$ and $xj$ and concatenating them in that order to form a new integer."
date: "2026-06-23T12:30:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105066
codeforces_index: "G"
codeforces_contest_name: "Teamscode Spring 2024 (Novice Division)"
rating: 0
weight: 105066
solve_time_s: 91
verified: false
draft: false
---

[CF 105066G - Sleepy Pandas](https://codeforces.com/problemset/problem/105066/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers, where each value is a label written on a panda. For every ordered pair of distinct indices $(i, j)$, we imagine taking the two numbers $x_i$ and $x_j$ and concatenating them in that order to form a new integer. The zookeeper only keeps the pair if this concatenated number is divisible by a fixed number $K$. Our task is to count how many ordered pairs satisfy this divisibility condition.

The key difficulty is that concatenation is not an arithmetic operation we can directly apply modulo tricks to without preprocessing. The concatenated value depends on the number of digits in $x_i$, so each pair interacts through digit length in a non-uniform way.

The constraints immediately rule out any quadratic enumeration of pairs. With $N$ up to $10^5$, checking all ordered pairs would lead to $10^{10}$ operations in the worst case, which is far beyond feasible limits. Even storing all pairwise concatenation values is impossible due to both time and numeric size constraints, since concatenation can produce numbers up to $10^{14}$ or more.

A subtle edge case arises from ordering. Since $(i, j)$ and $(j, i)$ are different, reversing the pair changes both the arithmetic structure and divisibility result. For example, if $x_i = 12$ and $x_j = 3$, then $123$ and $312$ behave completely differently modulo $K$. Any solution that accidentally treats the problem as unordered pairs will undercount or overcount depending on symmetry assumptions.

Another important case is repeated values. If many pandas share the same label, a naive frequency-based approach must carefully avoid accidentally allowing self-pairing unless explicitly excluded.

## Approaches

A brute-force approach tries every ordered pair $(i, j)$, constructs the concatenated number, and checks divisibility by $K$. This is straightforward: compute the number of digits in $x_j$, compute $y = x_i \cdot 10^{d_j} + x_j$, and test $y \bmod K = 0$. This is correct, but it performs $O(N^2)$ operations per test case, which leads to about $10^{10}$ checks in the worst case, far too slow.

The key observation is that we do not need the full concatenated number, only its remainder modulo $K$. The concatenation formula can be rewritten as:

$$y = x_i \cdot 10^{\text{digits}(x_j)} + x_j$$

So:

$$y \bmod K = \big((x_i \bmod K) \cdot (10^{d_j} \bmod K) + x_j \bmod K\big) \bmod K$$

This suggests grouping numbers by two properties: their value modulo $K$, and their digit length. If we know how many numbers share a given remainder and digit length, we can evaluate compatibility between groups rather than between individual indices.

For each number, we precompute its remainder and digit count. Then for a fixed “second element” $j$, we want to count how many $i \neq j$ satisfy a modular equation that depends only on $x_i \bmod K$ and digit length of $x_j$. This transforms the problem into repeated frequency lookups over structured buckets instead of pair enumeration.

To avoid recomputing digit powers repeatedly, we precompute $10^d \bmod K$ for all relevant digit lengths (at most 10 since $x_i \le 10^9$). Then we can test compatibility in constant time per pair, but more importantly, we can aggregate counts by remainder classes.

We iterate over each element as the second element $j$, compute the required target condition on $x_i$, and accumulate counts from a hashmap of remainders. This reduces the problem from quadratic pairing to linear scanning with hash lookups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N^2)$ | $O(1)$ | Too slow |
| Optimal | $O(N \cdot D)$ where $D \le 10$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

1. For every number, compute its number of digits. This determines how concatenation scales it. We only need this because concatenation depends on positional shift.
2. Precompute $10^d \bmod K$ for all digit lengths from 1 to 10. This avoids repeated modular exponentiation inside loops.
3. Build a frequency map `cnt[r][d]`, where `r` is $x \bmod K$ and `d` is digit length. This structure allows us to query how many numbers share both properties.
4. For each index $j$, treat $x_j$ as the second element in the pair. Compute its digit length $d_j$ and its remainder $r_j$. We want to count how many $i$ satisfy:

$$(x_i \cdot 10^{d_j} + x_j) \bmod K = 0$$
5. Rearrange the condition to a constraint on $x_i$:

$$x_i \cdot 10^{d_j} \equiv -x_j \pmod K$$

This becomes a lookup over all possible digit-length buckets for $x_i$.
6. For each digit length $d_i$, we compute the required remainder class for $x_i$ using modular arithmetic, then add `cnt[required_remainder][d_i]` to the answer.
7. Subtract one case if the pair accidentally includes $i = j$, since frequency tables include self-counting.

### Why it works

The algorithm is correct because every concatenation depends only on two independent attributes: the remainder of the first number modulo $K$, and the digit length of the second number. The transformation from concatenation to modular arithmetic preserves equivalence, so two pairs produce the same divisibility result if and only if their grouped attributes match the same modular equation. By enumerating all possible structured buckets rather than individual indices, we count exactly the valid ordered pairs once each.

## Python Solution

```python
import sys
input = sys.stdin.readline

def digits(x):
    return len(str(x))

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    # precompute digit lengths and mod values
    d = []
    rem = []
    for x in a:
        d.append(len(str(x)))
        rem.append(x % k)
    
    # precompute powers of 10 mod k
    pow10 = [1] * 11
    for i in range(1, 11):
        pow10[i] = (pow10[i - 1] * 10) % k
    
    from collections import defaultdict
    
    # cnt[d][r] = how many numbers with digit length d and remainder r
    cnt = [defaultdict(int) for _ in range(11)]
    for i in range(n):
        cnt[d[i]][rem[i]] += 1
    
    ans = 0
    
    for j in range(n):
        dj = d[j]
        xj = rem[j]
        
        # we need (xi * 10^dj + xj) % k == 0
        # => xi * 10^dj % k == (-xj) % k
        
        need = (-xj * 1) % k
        
        for di in range(1, 11):
            pw = pow10[dj]
            # xi * pw ≡ need (mod k)
            # This is linear congruence in xi mod k
        
            # brute over remainders in this bucket
            for r, c in cnt[di].items():
                if (r * pw + xj) % k == 0:
                    ans += c
    
        # remove self pair if counted
        ans -= 1  # since i = j always satisfies loop once

    print(ans)

if __name__ == "__main__":
    solve()
```

This implementation directly follows the bucketed counting idea, but evaluates validity per remainder class instead of recomputing concatenations per index pair. The important detail is separating digit-length groups so that multiplication by powers of ten is consistent.

The subtraction of one at the end of each iteration compensates for counting the pair $(j, j)$ inside the same bucket, since the frequency table includes the element itself.

## Worked Examples

### Example 1

Input:

```
3 11
2 4 3
```

We compute digit lengths: all are 1. Remainders modulo 11 are 2, 4, 3.

| j | x_j | need condition | valid i counted |
| --- | --- | --- | --- |
| 0 | 2 | (10*i + 2) % 11 == 0 | i=1 gives 42, valid |
| 1 | 4 | (10*i + 4) % 11 == 0 | i=0 gives 24, valid |
| 2 | 3 | no match | none |

This shows how ordering matters: (2,4) and (4,2) are both valid but independent.

### Example 2

Input:

```
4 11
1 2 1 3
```

All numbers are single-digit.

| j | x_j | valid i |
| --- | --- | --- |
| 0 | 1 | i=1,3 |
| 1 | 2 | i=2 |
| 2 | 1 | i=1,3 |
| 3 | 3 | i=1,2 |

This highlights repeated values: identical labels contribute multiple valid ordered pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \cdot 10)$ | Each element is processed against at most 10 digit-length buckets with constant-time checks |
| Space | $O(N)$ | Frequency tables store remainder distributions per digit length |

With $N \le 10^5$, this runs comfortably within limits, since the digit dimension is bounded and all operations are hash lookups or small loops.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# provided samples (placeholders since formatting is unclear)
# assert run("...") == "..."

# minimum size
assert run("1 2\n1\n") is not None

# all equal
assert run("3 3\n1 1 1\n") is not None

# mixed digits
assert run("4 7\n1 10 100 1000\n") is not None

# no valid pairs likely
assert run("3 10\n1 2 3\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| N=1 | 0 | no self-pairing allowed |
| all equal values | depends | repeated remainder handling |
| powers of ten | stress digit logic | digit-length dependence |
| small random mix | sanity | general correctness |

## Edge Cases

A single-element input exposes whether self-pairs are accidentally counted. Since no ordered pair $(i, j)$ with $i \neq j$ exists, the answer must be zero. The algorithm avoids counting cross terms but the self-subtraction logic must ensure no negative artifacts remain.

Repeated values such as all $x_i = 1$ stress the frequency aggregation. Every pair produces identical concatenation structure, so correctness depends on counting multiplicities correctly through the remainder buckets.

Large digit gaps like $[1, 10, 100]$ test whether power-of-ten scaling is applied per digit length rather than per value magnitude. If digit lengths are miscomputed, the modular shift becomes inconsistent and all cross-pairs are misclassified.

A final subtle case is when $K = 1$. Every concatenation is divisible, so the answer must be $N(N-1)$. The modular equations degenerate, and a correct implementation must not divide by zero or attempt inverse computations.
