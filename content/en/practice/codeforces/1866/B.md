---
title: "CF 1866B - Battling with Numbers"
description: "We are given two integers, but instead of being written in decimal form, they are described by their prime factorizations. One number, call it $X$, is fully determined by a list of primes and their exponents. The other number $Y$ is described the same way."
date: "2026-06-08T23:43:57+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1866
codeforces_index: "B"
codeforces_contest_name: "COMPFEST 15 - Preliminary Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 1400
weight: 1866
solve_time_s: 83
verified: true
draft: false
---

[CF 1866B - Battling with Numbers](https://codeforces.com/problemset/problem/1866/B)

**Rating:** 1400  
**Tags:** combinatorics, math, number theory  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers, but instead of being written in decimal form, they are described by their prime factorizations. One number, call it $X$, is fully determined by a list of primes and their exponents. The other number $Y$ is described the same way.

The task is to count how many ordered pairs $(p, q)$ of positive integers exist such that the least common multiple of $p$ and $q$ equals $X$, and the greatest common divisor of $p$ and $q$ equals $Y$. The answer must be computed modulo $998244353$.

A useful way to think about the constraints is that both numbers can be extremely large, up to around $2 \times 10^6$ in prime values and large exponents. The number of distinct primes is up to $10^5$, so any solution must treat each prime independently and work in essentially linear time over the factor lists. Anything quadratic in the number of primes or exponents is impossible within one second.

A key structural requirement appears immediately from the definitions of gcd and lcm. If a prime appears in $Y$, it must also appear in $X$, because the gcd cannot contain primes not present in either number, and the lcm must already contain all primes from both numbers. If this condition fails for any prime, the answer must be zero. A careless solution that ignores this consistency check will produce incorrect positive answers in cases like $X = 2^1 \cdot 5^1$, $Y = 3^1$, where no pair can exist.

Another subtle issue is that primes not present in $Y$ but present in $X$ still contribute choices. Many incorrect solutions either forget to process these primes or treat them symmetrically with gcd primes, which breaks correctness.

Finally, the ordering matters: pairs $(p,q)$ are ordered, so swapping them produces different valid solutions unless $p = q$.

## Approaches

A brute-force approach would attempt to construct all pairs $(p,q)$ such that their gcd and lcm match the required values. One could try enumerating all possible exponent assignments for each prime in both numbers. For a given prime, if its exponent in $X$ is $a$, then the exponents in $p$ and $q$ must lie between certain bounds dictated by gcd and lcm constraints. However, even for a single prime, enumerating all valid exponent pairs is fine, but doing so independently across up to $10^5$ primes still requires careful counting rather than explicit generation.

The key observation is that gcd and lcm constraints decouple completely over primes. For each prime $x$, suppose its exponent in $X$ is $a$ and in $Y$ is $b$. If $b > a$, there is no solution, because gcd cannot exceed lcm in any prime exponent.

Now fix a single prime. Let the exponent of that prime in $p$ be $i$, and in $q$ be $j$. Then the gcd condition forces $\min(i,j) = b$, and the lcm condition forces $\max(i,j) = a$. This immediately implies that both $i$ and $j$ must lie in the set $\{b, a\}$, but with at least one equal to each endpoint. That gives exactly two possibilities per ordered pair assignment: either $i=b, j=a$ or $i=a, j=b$, but only if $a \ne b$. If $a = b$, then both must be equal, giving exactly one choice.

For primes not appearing in $Y$, we have $b = 0$. In that case, $\min(i,j)=0$ forces at least one of $i,j$ to be zero, while $\max(i,j)=a$ forces the other to be exactly $a$. Again, we get exactly two ordered configurations per such prime, as long as $a > 0$.

The entire problem reduces to multiplying independent contributions over all primes in $X$, but only if all primes in $Y$ are contained in $X$. If a prime exists in $Y$ but not in $X$, the answer is zero immediately.

Thus, each prime contributes either 1 or 2 ways depending on whether its exponent in $X$ equals that in $Y$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in number of primes | O(1)-O(n) | Too slow |
| Optimal | O(N + M) | O(1) extra | Accepted |

## Algorithm Walkthrough

We process both prime factor lists as a comparison problem between two maps.

1. Store the exponent of each prime in $X$ in a hash map or dictionary.

This allows constant-time lookup when checking primes from $Y$.
2. Initialize the answer as 1.

We will multiply independent contributions from each prime.
3. Iterate over each prime $C_j$ in $Y$.

For each one, check whether it exists in $X$. If it does not exist, there is no way for gcd to contain a prime absent from lcm, so the answer becomes 0 and we can stop.
4. Let the exponent of this prime in $X$ be $a$, and in $Y$ be $b$.

If $b > a$, we again immediately conclude impossibility because gcd cannot exceed lcm in any prime component.
5. If $a = b$, this prime contributes exactly 1 way.

Both $p$ and $q$ must contain this prime with the same exponent, so no freedom exists.
6. If $a > b$, this prime contributes exactly 2 ways.

One number takes exponent $a$ and the other takes exponent $b$, and since the pair is ordered, both assignments are valid.
7. Multiply the contribution into the answer modulo $998244353$.

After processing all primes in $Y$, all primes in $X$ that are not in $Y$ implicitly behave as $b=0$, and they have already been accounted for if we extend the same reasoning: each such prime also contributes exactly 2 ways. However, we do not need to iterate over them separately if we structure computation carefully: we track how many primes in $X$ match $Y$, and how many differ.

A clean implementation directly iterates over all primes in $X$, checks presence in $Y$, and multiplies contributions accordingly.

### Why it works

For each prime, the constraints $\gcd(p,q)$ and $\text{lcm}(p,q)$ impose independent conditions on its exponent in $p$ and $q$. Since gcd and lcm are computed per prime independently, choices for one prime do not affect another. This creates a product structure over primes. Each prime contributes a fixed number of valid exponent assignments, and the total number of pairs is the product of these contributions. The correctness follows from the uniqueness of prime factorization and the independence of exponent constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    
    x_exp = {}
    for p, e in zip(A, B):
        x_exp[p] = e

    m = int(input())
    C = list(map(int, input().split()))
    D = list(map(int, input().split()))
    
    y_exp = {}
    for p, e in zip(C, D):
        y_exp[p] = e

    # consistency check: all primes in Y must exist in X
    for p, e in y_exp.items():
        if p not in x_exp or e > x_exp[p]:
            print(0)
            return

    ans = 1

    # process primes in X (covers both shared and extra primes)
    for p, a in x_exp.items():
        b = y_exp.get(p, 0)

        if a == b:
            ans = (ans * 1) % MOD
        else:
            ans = (ans * 2) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation builds two dictionaries mapping primes to exponents. The first loop enforces feasibility: every prime in $Y$ must appear in $X$ with at least as large an exponent. The second loop computes the multiplicative contribution of each prime in $X$. Missing primes in $Y$ are treated as exponent zero, which correctly models gcd constraints.

A common pitfall is iterating only over primes in $Y$. That undercounts contributions from primes present in $X$ but absent in $Y$, each of which still provides a factor of 2.

## Worked Examples

### Example 1

Input:

```
X: 2^2 * 3^1 * 5^1 * 7^2
Y: 3^1 * 7^1
```

We compute per prime contributions.

| Prime | exp in X (a) | exp in Y (b) | Contribution |
| --- | --- | --- | --- |
| 2 | 2 | 0 | 2 |
| 3 | 1 | 1 | 1 |
| 5 | 1 | 0 | 2 |
| 7 | 2 | 1 | 2 |

Final answer: $2 \cdot 1 \cdot 2 \cdot 2 = 8$

This confirms that every mismatch between $a$ and $b$ doubles the number of assignments, while equality fixes the structure.

### Example 2

Input:

```
X = 2^1 * 5^1
Y = 2^1 * 3^1
```

| Prime | in X | in Y | Valid? |
| --- | --- | --- | --- |
| 2 | 1 | 1 | ok |
| 5 | 1 | 0 | ok |
| 3 | 0 | 1 | invalid |

The presence of prime 3 in $Y$ but not in $X$ immediately invalidates the construction, producing output 0. This shows why the feasibility check is essential before counting.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + M) | each prime processed once in hash map construction and traversal |
| Space | O(N + M) | storage of exponent maps |

The constraints allow up to $10^5$ primes, so a linear scan with hash map operations fits comfortably within time limits.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    x = {}
    for p, e in zip(A, B):
        x[p] = e

    m = int(input())
    C = list(map(int, input().split()))
    D = list(map(int, input().split()))

    y = {}
    for p, e in zip(C, D):
        y[p] = e

    for p, e in y.items():
        if p not in x or e > x[p]:
            return "0"

    ans = 1
    for p, a in x.items():
        b = y.get(p, 0)
        if a != b:
            ans = (ans * 2) % MOD

    return str(ans)

# provided sample
assert run("""4
2 3 5 7
2 1 1 2
2
3 7
1 1
""") == "8"

# Y not subset of X
assert run("""2
2 5
1 1
1
3
1
""") == "0"

# identical X and Y
assert run("""2
2 3
1 1
2
2 3
1 1
""") == "1"

# all primes differ
assert run("""3
2 3 5
2 2 2
0

""") == "8"

# large single prime equal
assert run("""1
2
5
1
2
5
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Y not subset | 0 | invalid gcd prime detection |
| identical X=Y | 1 | all constraints tight, no freedom |
| all primes differ | 8 | each prime contributes factor 2 |
| single prime equal | 1 | boundary case with equality |

## Edge Cases

A first edge case is when $Y$ contains a prime not present in $X$. In that situation, gcd would require a prime factor that lcm does not have, which is impossible. The algorithm catches this immediately in the feasibility loop before any multiplication occurs.

Another edge case is when $X = Y$. Every prime exponent matches exactly, so there is no flexibility in assigning exponents to $p$ and $q$. Each prime contributes exactly one configuration, and the final answer is 1. The algorithm handles this naturally because no prime triggers the doubling rule.

A third edge case occurs when $Y = 1$. Here all primes in $X$ are effectively free, and each contributes two assignments corresponding to distributing the full exponent between $p$ and $q$. The algorithm reduces to multiplying 2 for each prime in $X$, producing $2^{|X|}$, which is correct.

A final case is when $X$ has a single prime. The algorithm reduces to a simple binary choice depending on whether that prime appears in $Y$ with the same exponent or zero, confirming correctness in the smallest non-trivial structure.
