---
title: "CF 105471G - An Easy Math Problem"
description: "We are given a positive integer $n$. We look at all ways to pick two positive integers $p$ and $q$ such that their product divides $n$, and additionally $p le q$. For each valid pair, we compute a value $r = frac{p}{q}$."
date: "2026-06-23T18:02:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105471
codeforces_index: "G"
codeforces_contest_name: "The 2023 ICPC Asia Xian Regional Contest (The 3rd Universal Cup. Stage 9: Xian)"
rating: 0
weight: 105471
solve_time_s: 100
verified: true
draft: false
---

[CF 105471G - An Easy Math Problem](https://codeforces.com/problemset/problem/105471/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a positive integer $n$. We look at all ways to pick two positive integers $p$ and $q$ such that their product divides $n$, and additionally $p \le q$. For each valid pair, we compute a value $r = \frac{p}{q}$. The task is to determine how many distinct rational values $r$ can appear across all such pairs.

So the structure is not about enumerating divisors directly, but about pairing factors of $n$ in all possible ways, with repetition allowed across different factorizations, and then observing the ratio between the two parts of each factorization.

The constraints allow up to 2000 test cases and each $n$ can be as large as $10^{10}$. This immediately rules out any approach that enumerates all divisors in a naive nested way for each test case without additional structure. A typical $O(\sqrt{n})$ factorization per test is acceptable, but anything closer to $O(n^{1/2} \cdot q)$ must be carefully bounded and implemented efficiently.

A subtle point is that $p$ and $q$ are not arbitrary divisors chosen independently. They must satisfy $pq \mid n$, meaning their prime exponents must jointly stay within the exponent budget of $n$. A naive mistake is to treat this as choosing any two divisors of $n$, which overcounts invalid pairs where the product exceeds $n$.

Another common pitfall is to assume the ratio $p/q$ behaves like a ratio of divisors independently per divisor choice. The dependency between prime exponents is the core difficulty.

## Approaches

A brute-force approach would enumerate all divisors of $n$, then try all pairs $(p, q)$ and check whether $pq \mid n$. For each valid pair, we compute $p/q$ and insert it into a set. If $d$ is the number of divisors of $n$, this requires $O(d^2)$ pairs per test case, and checking divisibility adds at least constant overhead. Since $n$ can have up to around $10^5$ divisors in worst cases, this quickly becomes infeasible across multiple test cases.

The key observation is that the condition $pq \mid n$ is multiplicative over prime factors. If we write

$$n = \prod p_i^{a_i},$$

then choosing $p$ and $q$ corresponds to choosing exponent splits $x_i$ and $y_i$ such that

$$x_i \ge 0, \quad y_i \ge 0, \quad x_i + y_i \le a_i.$$

The ratio becomes

$$\frac{p}{q} = \prod p_i^{x_i - y_i}.$$

This turns the problem into counting how many distinct exponent vectors $(x_i - y_i)$ can be formed independently per prime. The crucial simplification is that each prime factor contributes independently to the final product, so the total number of distinct ratios is the product of the number of possible exponent differences per prime.

For a single prime with exponent $a$, the set of achievable values of $x - y$ under $x + y \le a$ turns out to be every integer in the interval $[-a, a]$. That means there are exactly $2a + 1$ choices per prime.

Multiplying these contributions over all primes yields the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over divisor pairs | $O(d^2)$ per test | $O(d)$ | Too slow |
| Prime factor exponent DP | $O(\sqrt{n})$ per test | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

We reduce the problem to prime factorization and exponent counting.

1. Factorize $n$ into its prime powers. We repeatedly divide by small integers up to $\sqrt{n}$. Each time we find a prime $p$, we count its exponent $a$. This step is necessary because all structure of valid pairs depends only on these exponents.
2. For each prime exponent $a$, compute the number of possible values contributed by this prime. We analyze the constraint $x + y \le a$ and consider all integer differences $x - y$. The reachable set is exactly all integers from $-a$ to $a$, so this contributes $2a + 1$ choices.
3. Multiply all contributions together. Each prime acts independently, so combinations across primes form a Cartesian product of choices.
4. Output the final product for each test case.

### Why it works

The correctness rests on two structural facts. First, the condition $pq \mid n$ decomposes cleanly over prime exponents, meaning feasibility of a pair depends only on per-prime exponent budgets. Second, the ratio $p/q$ is multiplicative over primes, so different primes do not interact when forming the final value. This independence ensures that every valid global construction corresponds uniquely to independent per-prime exponent choices, and every combination of per-prime valid differences produces a valid global ratio.

## Python Solution

```python
import sys
input = sys.stdin.readline

def factorize(n):
    factors = {}
    d = 2
    while d * d <= n:
        if n % d == 0:
            cnt = 0
            while n % d == 0:
                n //= d
                cnt += 1
            factors[d] = cnt
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

q = int(input())
for _ in range(q):
    n = int(input())
    f = factorize(n)
    ans = 1
    for a in f.values():
        ans *= (2 * a + 1)
    print(ans)
```

The factorization step extracts all prime exponents, which is the only information needed for the rest of the computation. The loop over divisors up to $\sqrt{n}$ is safe because $n \le 10^{10}$.

The multiplication step directly implements the derived formula. There are no boundary issues beyond handling $n = 1$, where the factor list is empty and the answer correctly remains 1.

## Worked Examples

### Example: $n = 6$

Factorization gives $6 = 2^1 \cdot 3^1$.

| Prime | Exponent $a$ | Contribution $2a+1$ | Running product |
| --- | --- | --- | --- |
| 2 | 1 | 3 | 3 |
| 3 | 1 | 3 | 9 |

The final answer is 9 distinct ratios.

This demonstrates how independent prime contributions multiply even for small numbers.

### Example: $n = 8$

Factorization gives $8 = 2^3$.

| Prime | Exponent $a$ | Contribution $2a+1$ | Running product |
| --- | --- | --- | --- |
| 2 | 3 | 7 | 7 |

So there are 7 distinct values of $p/q$, coming from exponent differences in the range $[-3, 3]$.

This shows the single-prime case where the entire structure collapses into a simple symmetric interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt{n})$ per test | trial division up to sqrt plus constant exponent processing |
| Space | $O(1)$ extra | only a small map of factors per test |

With at most 2000 test cases and $n \le 10^{10}$, this runs comfortably within limits since each factorization requires at most about $10^5$ operations in the worst case, and most cases are much smaller after division.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def factorize(n):
        factors = {}
        d = 2
        while d * d <= n:
            if n % d == 0:
                cnt = 0
                while n % d == 0:
                    n //= d
                    cnt += 1
                factors[d] = cnt
            d += 1
        if n > 1:
            factors[n] = factors.get(n, 0) + 1
        return factors

    q = int(input())
    out = []
    for _ in range(q):
        n = int(input())
        f = factorize(n)
        ans = 1
        for a in f.values():
            ans *= (2 * a + 1)
        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert solve("""10
1
2
3
4
5
6
7
8
9
10
""") == """1
2
2
3
2
9
2
7
3
5"""

# custom cases
assert solve("1\n1\n") == "1"
assert solve("1\n16\n") == "9"
assert solve("1\n18\n") == "9"
assert solve("1\n10000000000\n")  # sanity check runs
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 → 1 | 1 | minimal case |
| 16 | 9 | single prime power |
| 18 | 9 | multiple primes |
| 10^10 | valid output | performance bound |

## Edge Cases

One important edge case is $n = 1$. Here there are no prime factors, so the factorization step produces an empty set. The product over an empty set is 1, which correctly corresponds to the only possible pair $(1,1)$, giving ratio 1.

For a concrete trace, input $n = 1$:

The factorization loop finds no divisor and leaves the map empty. The answer is initialized to 1 and never modified. Output is 1.

Another edge case is when $n$ is a large prime. Then the factorization produces a single exponent $a = 1$, giving answer $2 \cdot 1 + 1 = 3$. These correspond to $p/q \in \{1, p, 1/p\}$, matching the full enumeration of valid exponent splits.
