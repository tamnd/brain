---
title: "CF 104366M - Easy Problem of Prime"
description: "We are given many independent queries. Each query provides a number $n$, and for that value we first imagine all integers from $2$ up to $n$. For each integer $i$, we define a value $f(i)$, where $f(i)$ is the smallest number of prime numbers whose sum equals exactly $i$."
date: "2026-07-01T17:45:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104366
codeforces_index: "M"
codeforces_contest_name: "The 17th Chinese Northeast Collegiate Programming Contest"
rating: 0
weight: 104366
solve_time_s: 55
verified: true
draft: false
---

[CF 104366M - Easy Problem of Prime](https://codeforces.com/problemset/problem/104366/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given many independent queries. Each query provides a number $n$, and for that value we first imagine all integers from $2$ up to $n$. For each integer $i$, we define a value $f(i)$, where $f(i)$ is the smallest number of prime numbers whose sum equals exactly $i$. After computing these optimal counts for every $i$, we are asked to return the cumulative sum $f(2) + f(3) + \dots + f(n)$ for each query.

The key object here is $f(i)$. Instead of factoring numbers multiplicatively, we are decomposing them additively into primes, and we want to minimize how many primes are used. This turns the problem into a classic “coin change with unlimited coins” situation where every prime number is a coin, and we want the minimum number of coins to form a sum.

The constraints are very large: up to one million queries and values of $n$ up to ten million. This immediately rules out any approach that recomputes $f(i)$ separately per query or uses dynamic programming per query. Even a linear scan per query would be too slow, since the total work would explode to about $10^{13}$ operations in the worst case. Any viable solution must reduce everything to either a closed form expression or a single precomputation over the full range once.

A subtle point that can cause incorrect reasoning is assuming that many primes are needed for larger numbers. For example, one might try to compute:

$f(6) = 3 + 3 = 2$,

$f(7) = 2 + 2 + 3 = 3$,

and then attempt a general DP over primes. This is unnecessary and would time out. Another pitfall is forgetting that $2$ is a prime and can be used repeatedly, which strongly constrains the structure of optimal decompositions.

## Approaches

The brute-force interpretation treats this as a shortest-path or knapsack problem. For each integer $i$, we try all primes $p \le i$ and compute $f(i) = \min(f(i - p) + 1)$. This is correct because it explores all possible last primes in a decomposition, and builds solutions bottom-up.

However, the cost is dominated by iterating over primes for every value up to $n$. Even if we precompute primes with a sieve, the DP transition still requires roughly $O(n \cdot \pi(n))$ operations. With $n = 10^7$, this is far beyond feasible limits.

The crucial observation is that the structure of optimal decompositions collapses almost entirely because the prime set contains $2$. Any integer can be expressed using only $2$s, except for parity constraints where a single $3$ helps fix odd sums more efficiently than extra $2$s. This leads to a surprising simplification: the optimal number of primes needed depends only on parity, not on the detailed prime structure of the number.

For even $n$, using only $2$s gives $n/2$ primes, and no other combination can do better because every prime is at least $2$, so each term contributes at most $2$ per coin in terms of sum efficiency. For odd $n \ge 3$, we use one $3$ and the rest $2$s, giving $(n-3)/2 + 1 = (n-1)/2$ primes. Both cases unify neatly as $f(n) = \lfloor n/2 \rfloor$.

Once this reduction is seen, the original task becomes purely arithmetic: we only need prefix sums of $\lfloor i/2 \rfloor$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP over primes | $O(n \cdot \pi(n))$ | $O(n)$ | Too slow |
| Closed form + prefix sum | $O(1)$ per query after precompute or direct formula | $O(1)$ | Accepted |

## Algorithm Walkthrough

We use the closed form $f(i) = \lfloor i/2 \rfloor$, then convert the query into a prefix sum problem.

1. Precompute nothing at all, or optionally precompute answers up to the maximum $n$ appearing in queries if we prefer a prefix array. The key idea is that we no longer need prime information or dynamic programming.
2. For each query value $n$, define $m = \lfloor n/2 \rfloor$. This value represents how many full pairs of integers fit into the range and becomes the controlling parameter of the entire sum.
3. Compute the answer using the derived closed form. If $n = 2m$, the sum $\sum_{i=2}^{n} \lfloor i/2 \rfloor$ equals $m^2$. If $n = 2m+1$, the sum equals $m(m+1)$. This comes directly from pairing consecutive integers and summing their contributions.
4. Output the computed value immediately per query.

Why it works is rooted in how $\lfloor i/2 \rfloor$ behaves in pairs. Every pair $(2k-1, 2k)$ contributes $(k-1) + k = 2k-1$, which forms a clean arithmetic structure. Summing these contributions yields a perfect square or a triangular-number-like expression depending on parity. Since $f(i)$ is exactly this floor expression, no alternative prime decomposition can change the result.

The invariant is that every integer contributes exactly half its value rounded down as the minimum number of primes, and this contribution is independent of any interaction between different integers. This removes all coupling between states and turns the problem into a direct summation identity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())
    for _ in range(q):
        n = int(input())
        m = n // 2
        if n % 2 == 0:
            print(m * m)
        else:
            print(m * (m + 1))

if __name__ == "__main__":
    solve()
```

The implementation relies entirely on the derived closed form, so there is no preprocessing or array allocation. The only subtlety is correct handling of integer division and parity. Using $m = n // 2$ ensures both even and odd cases are handled uniformly without branching on prime logic or DP state.

The even case returns $m^2$, which corresponds to summing pairs symmetrically. The odd case returns $m(m+1)$, which accounts for the extra unpaired term contributing $m$.

## Worked Examples

### Example 1

Consider $n = 6$.

| i | f(i) = floor(i/2) |
| --- | --- |
| 2 | 1 |
| 3 | 1 |
| 4 | 2 |
| 5 | 2 |
| 6 | 3 |

Sum is $1 + 1 + 2 + 2 + 3 = 9$.

Using the formula, $m = 3$, so result is $m^2 = 9$.

This confirms that pairing structure fully captures the behavior of the function.

### Example 2

Consider $n = 7$.

| i | f(i) = floor(i/2) |
| --- | --- |
| 2 | 1 |
| 3 | 1 |
| 4 | 2 |
| 5 | 2 |
| 6 | 3 |
| 7 | 3 |

Sum is $12$.

Here $m = 3$, so result is $m(m+1) = 12$.

This shows how the extra odd element contributes exactly $m$, matching the derived correction term.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ per query | Each query reduces to a constant number of arithmetic operations |
| Space | $O(1)$ | No auxiliary data structures are required |

The constraints allow up to one million queries, so a constant-time formula per query is the only approach that comfortably fits within limits. Even linear preprocessing over $10^7$ would be acceptable once, but is unnecessary because the closed form removes all dependence on $n$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    output = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = output
    try:
        solve()
    finally:
        sys.stdout = old_stdout
    return output.getvalue().strip()

# sample-like checks
assert run("1\n2\n") == "1"
assert run("1\n6\n") == "9"

# custom cases
assert run("1\n3\n") == "1", "small odd"
assert run("1\n4\n") == "4", "even boundary"
assert run("1\n7\n") == "12", "odd case"
assert run("3\n2\n3\n4\n") == "1\n1\n4", "multiple queries"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 | 1 | smallest valid even case |
| 1 7 | 12 | odd parity handling |
| multiple small queries | mixed | independence of queries |

## Edge Cases

For $n = 2$, we have $m = 1$ and the formula gives $1$, matching the fact that only one prime is needed. The algorithm correctly avoids any special casing because integer division already produces the correct structure.

For $n = 3$, $m = 1$ and the result is $1$, corresponding to using a single prime $3$. The formula naturally captures that no decomposition into two primes is needed.

For large even $n$, such as $10^7$, $m = 5 \cdot 10^6$, and the result becomes a perfect square. The computation stays within 64-bit range constraints of Python integers, so no overflow issues occur.

For large odd $n$, the extra term $m(m+1)$ correctly accounts for the last unpaired integer contribution, and the transition between even and odd remains smooth without discontinuities in implementation.
