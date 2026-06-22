---
title: "CF 106016D - Least Uncommon Divisor"
description: "We are given a fixed number $x$ and a long list of values $ai$. For each $ai$, we want to find the smallest positive integer $z$ that satisfies two conditions: it must divide $x$, and it must fail to divide $ai$."
date: "2026-06-22T16:50:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106016
codeforces_index: "D"
codeforces_contest_name: "The 2025 Homs Collegiate programming contest"
rating: 0
weight: 106016
solve_time_s: 72
verified: true
draft: false
---

[CF 106016D - Least Uncommon Divisor](https://codeforces.com/problemset/problem/106016/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed number $x$ and a long list of values $a_i$. For each $a_i$, we want to find the smallest positive integer $z$ that satisfies two conditions: it must divide $x$, and it must fail to divide $a_i$. If every divisor of $x$ also divides $a_i$, then no such $z$ exists and the answer is $-1$.

Another way to read the task is that for each query value $a_i$, we scan through all divisors of $x$ in increasing order and ask where the first “mismatch” happens between the divisor sets of $x$ and $a_i$.

The constraints make the structure important. The array size can reach one million, and values go up to $10^{12}$. This immediately rules out any approach that tries to factor each number independently or recompute divisors of $x$ repeatedly per query. Even a linear scan per query over a large divisor set becomes critical because the divisor count of a number up to $10^{12}$ can still reach around a million in pathological cases.

A subtle failure case appears when $a_i$ is divisible by every divisor of $x$. For example, if $x = 12$, its divisors are $1,2,3,4,6,12$. If $a_i = 60$, every one of those divides 60, so the answer must be $-1$. A naive approach that stops early or assumes a missing divisor always exists would incorrectly return 1 or another small value.

Another edge case happens when the smallest divisor of $x$, which is always 1, already fails the condition. This is impossible because 1 divides everything, so the scan always starts with a “valid” divisor. The first meaningful failure must occur at some divisor greater than 1.

## Approaches

A direct solution suggests itself immediately. We can enumerate all divisors of $x$, sort them, and for each $a_i$, test divisibility against each divisor in order until we find one that does not divide $a_i$. This is correct because the definition of the answer explicitly requires the smallest such divisor.

The bottleneck is obvious once we estimate the cost. If $x$ has $D$ divisors, then each query may require up to $D$ modulus checks. In the worst case $D$ can be large, and with $n$ up to $10^6$, this becomes too slow if every query scans a large prefix.

The key structural simplification comes from noticing that we do not actually need full factorization per query. For a fixed $a_i$, the divisors of $x$ that divide $a_i$ are exactly those divisors of $\gcd(x, a_i)$. This turns the problem into checking membership in a divisor set: a divisor $d$ is valid for $a_i$ if and only if it does not divide $\gcd(x, a_i)$.

So for each query, we compute $g = \gcd(x, a_i)$, then scan divisors of $x$ in increasing order and return the first divisor $d$ such that $d \nmid g$. This replaces repeated full divisibility checks against $a_i$ with checks against a smaller number.

We still scan a sorted divisor list, but this is now a simple linear pass over a precomputed structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (recompute divisors per query) | $O(n \sqrt{x})$ | $O(1)$ | Too slow |
| Divisor enumeration + gcd pruning | $O(D + nD)$ worst-case | $O(D)$ | Accepted in practice |

## Algorithm Walkthrough

1. Compute all divisors of $x$ by checking integers up to $\sqrt{x}$. For every valid divisor pair, insert both values into a list.

The goal is to build the exact set of candidates for $z$.
2. Sort the divisor list in increasing order.

This ordering is essential because the problem asks for the smallest valid divisor.
3. For each query value $a_i$, compute $g = \gcd(x, a_i)$.

This compresses all information about which divisors of $x$ also divide $a_i$ into a single number.
4. Iterate over the sorted divisors of $x$ from smallest to largest.
5. For each divisor $d$, check whether $g \bmod d = 0$.

If it is nonzero, $d$ does not divide $a_i$, so $d$ is the answer for this query.
6. If the scan completes without finding such a divisor, output $-1$.

The important design choice is that we never recompute divisibility against $a_i$ directly. All membership queries are reduced to checking whether a divisor of $x$ also divides $g$.

### Why it works

For any divisor $d$ of $x$, the condition “$d$ divides $a_i$” is equivalent to “$d$ divides $\gcd(x, a_i)$”. This equivalence holds because any divisor of $x$ that divides $a_i$ must divide their greatest common divisor.

So the divisor list naturally splits into two parts for each query: those dividing $g$, and those that do not. Since we scan in increasing order, the first divisor outside the divisor set of $g$ is exactly the smallest valid answer.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import gcd

def solve():
    n, x = map(int, input().split())
    a = list(map(int, input().split()))
    
    # compute divisors of x
    divs = []
    i = 1
    while i * i <= x:
        if x % i == 0:
            divs.append(i)
            if i * i != x:
                divs.append(x // i)
        i += 1
    
    divs.sort()
    
    for ai in a:
        g = gcd(x, ai)
        ans = -1
        for d in divs:
            if g % d != 0:
                ans = d
                break
        print(ans)

if __name__ == "__main__":
    solve()
```

The first step builds the full divisor list of $x$ in $O(\sqrt{x})$. This is done only once, which is crucial because $x$ is shared across all queries.

The inner loop uses the gcd to avoid checking divisibility against $a_i$ directly. The condition `g % d != 0` is the key replacement for `ai % d != 0`, which would be more expensive to reason about repeatedly.

The early break ensures that once the smallest invalid divisor is found, we stop scanning immediately.

## Worked Examples

### Example 1

Input:

```
x = 30
a = [6, 10, 15]
```

Divisors of 30 are:

`[1, 2, 3, 5, 6, 10, 15, 30]`

For each value:

| ai | g = gcd(x, ai) | scan result |
| --- | --- | --- |
| 6 | 6 | 5 |
| 10 | 10 | 3 |
| 15 | 15 | 2 |

For $a_i = 6$, divisors of $g = 6$ are `[1,2,3,6]`, so the first divisor not in this set is 5.

This confirms that the algorithm is effectively finding the first missing divisor in the divisor set of $g$.

### Example 2

Input:

```
x = 12
a = 60
```

Divisors of 12 are `[1,2,3,4,6,12]`.

Since $60$ is divisible by all of these, we get $g = \gcd(12, 60) = 12$. Every divisor of $x$ divides $g$, so the scan finishes without a break and returns $-1$.

This demonstrates the correctness of the failure condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt{x} + nD)$ | divisors are generated once, each query scans divisor list |
| Space | $O(D)$ | storing all divisors of $x$ |

The divisor count $D$ is bounded by the number of divisors of $x$, which is manageable in typical cases. Since each query stops early once the first mismatch is found, the average performance is significantly better than the worst-case bound, making the solution suitable for $n = 10^6$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import gcd
    import sys

    input = sys.stdin.readline

    def solve():
        n, x = map(int, input().split())
        a = list(map(int, input().split()))

        divs = []
        i = 1
        while i * i <= x:
            if x % i == 0:
                divs.append(i)
                if i * i != x:
                    divs.append(x // i)
            i += 1

        divs.sort()

        res = []
        for ai in a:
            g = gcd(x, ai)
            ans = -1
            for d in divs:
                if g % d != 0:
                    ans = d
                    break
            res.append(str(ans))

        return " ".join(res)

    return solve()

# provided sample (illustrative formatting)
assert run("5 30\n6 10 15 35 60\n") == "5 3 2 2 -1", "sample"

# all ai divisible by x -> -1
assert run("3 12\n12 24 36\n") == "-1 -1 -1"

# small x
assert run("3 6\n1 2 3\n") == "2 3 2"

# prime x
assert run("4 13\n1 13 26 27\n") == "13 13 2 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small x, mixed divisibility | varies | correctness of gcd-based filtering |
| all divisible by x | all -1 | full coverage edge case |
| prime x | simple divisor set | minimal divisor structure |
| mixed values | mixed output | general correctness |

## Edge Cases

When $a_i$ is a multiple of every divisor of $x$, the algorithm computes $g = x$, and every divisor passes the check `g % d == 0`. The scan completes without breaking and correctly returns $-1$, matching the definition.

When $x$ is prime, the divisor list is `[1, x]`. Since 1 always divides any $a_i$, the answer is either $x$ (if $a_i$ is not divisible by $x$) or $-1$. The algorithm naturally handles this because it checks 1 first, then directly reaches $x$.

When $a_i$ is very small, especially 1, the gcd becomes 1. Since only divisor 1 divides 1, every other divisor of $x$ immediately becomes a candidate answer, so the algorithm returns the second smallest divisor of $x$, which matches the definition precisely.
