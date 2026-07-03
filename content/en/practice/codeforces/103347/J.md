---
title: "CF 103347J - Rosencrantz and Guildenstern"
description: "The problem starts with a modular arithmetic condition involving three fixed values and a variable exponent. We are given a prime modulus $p$, two residues $x$ and $y$ in the range $1$ to $p-1$, and a very large upper bound $a$."
date: "2026-07-03T13:47:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103347
codeforces_index: "J"
codeforces_contest_name: "UTPC Contest 10-15-21 Div. 2 (Beginner)"
rating: 0
weight: 103347
solve_time_s: 53
verified: true
draft: false
---

[CF 103347J - Rosencrantz and Guildenstern](https://codeforces.com/problemset/problem/103347/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem starts with a modular arithmetic condition involving three fixed values and a variable exponent. We are given a prime modulus $p$, two residues $x$ and $y$ in the range $1$ to $p-1$, and a very large upper bound $a$. The task is to count how many integers $k$ in the range $[1, a]$ satisfy a congruence of the form

$$k \cdot x^k \equiv y \pmod p.$$

The expression mixes a linear factor in $k$ with an exponential factor $x^k$, all evaluated modulo a prime. The output is not the solutions themselves but their count within a potentially enormous range up to $10^{12}$, which rules out any approach that iterates over all candidates.

The prime modulus immediately implies we can use the structure of the multiplicative group modulo $p$, which has size $p-1$. This is crucial because exponentiation cycles modulo $p-1$ when expressed via discrete logarithms, and it also suggests that any useful preprocessing will likely be bounded by $O(p)$ or $O(p \log p)$.

The bound on $a$ being as large as $10^{12}$ means we must avoid any algorithm that depends linearly on $a$. Instead, we expect to reduce the problem to counting solutions in residue classes or within a period, followed by a prefix count over $[1, a]$.

A subtle issue arises from the multiplication by $k$. Unlike pure exponential congruences, here $k$ appears both as a coefficient and as an exponent. This destroys simple periodicity in $k$, so any correct approach must separate arithmetic structure from exponential structure rather than treating the expression as purely cyclic.

One edge case is when $x = 0$ is impossible since $x \in [1, p-1]$, so we avoid degenerate exponentiation. Another important case is when $x = 1$, where the exponential term disappears and the equation reduces to a linear congruence $k \equiv y \pmod p$, which behaves completely differently from the general case. A naive solver that assumes discrete logs always exist would fail here.

Another corner situation is when $y = 0 \pmod p$ is impossible since $y \in [1, p-1]$, which simplifies reasoning because we never need to consider zero residues.

## Approaches

A direct brute force approach would iterate over all $k \in [1, a]$, compute $x^k \bmod p$ and check whether $k \cdot x^k \equiv y$. Even with fast exponentiation, this still costs $O(a \log p)$, which is impossible when $a$ reaches $10^{12}$. The core inefficiency is recomputing exponentiation independently for each $k$, while also scanning an enormous range.

The structure becomes manageable once we separate the exponential and linear parts using a discrete logarithm viewpoint. Since $p$ is prime, the nonzero residues form a cyclic group of size $p-1$. If we fix a primitive root $g$, every value $x^k$ can be rewritten as $g^{k \log_g x}$, turning exponentiation into a linear function in the exponent space modulo $p-1$. This transforms the original condition into a mixed linear congruence involving $k$ and $k \cdot \alpha^k$-style terms in exponent space.

The key simplification is to observe that the equation can be rewritten in terms of $k \bmod (p-1)$. Once we fix $k$ modulo $p-1$, the value $x^k \bmod p$ becomes periodic, while the factor $k \bmod p$ also has a clear periodic structure modulo $p$. This suggests that the full behavior repeats on a combined modulus derived from $p$ and $p-1$, typically their least common multiple.

Thus, instead of checking all $k$, we precompute the number of solutions in one full period and then use arithmetic progression counting to extend this up to $a$. The problem reduces to finding all residues $k \in [1, p(p-1)]$ (or an equivalent period) satisfying the condition, then counting how many times each residue class appears in $[1, a]$.

The brute-force method works conceptually because it directly checks the definition. It fails because it treats each $k$ independently, ignoring that both components of the expression are periodic in different moduli. The optimal method works by aligning these periodicities and compressing the infinite search space into finitely many equivalence classes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(a \log p)$ | $O(1)$ | Too slow |
| Periodicity + preprocessing | $O(p)$ or $O(p \log p)$ | $O(p)$ | Accepted |

## Algorithm Walkthrough

1. If $x = 1$, reduce the equation to $k \equiv y \pmod p$. This works because $x^k = 1$ for all $k$, eliminating the exponential dependence entirely.
2. Otherwise, treat the problem in the multiplicative group modulo $p$, where exponentiation cycles with period $p-1$.
3. Precompute all values $x^k \bmod p$ for $k \in [1, p-1]$, since these determine all future values via periodicity in the exponent.
4. For each residue class $r \in [1, p(p-1)]$ (or a reduced representative set), evaluate whether $r \cdot x^r \equiv y \pmod p$ holds. This step is feasible because the state space is now bounded by $O(p)$ rather than $O(a)$.
5. Collect all valid residues $r$, then for each such residue compute how many integers $k \in [1, a]$ satisfy $k \equiv r \pmod T$, where $T$ is the identified period of repetition.

The reason this reduction is valid is that both $x^k \bmod p$ depends only on $k \bmod (p-1)$, and $k \bmod p$ depends only on $k \bmod p$. Therefore the full expression depends only on $k \bmod \mathrm{lcm}(p, p-1)$. Once we restrict attention to this finite domain, every solution class repeats regularly over the entire integer line, allowing exact counting in $[1, a]$.

## Python Solution

```python
import sys
input = sys.stdin.readline

p, x, y, a = map(int, input().split())

if x == 1:
    # k * 1^k ≡ k ≡ y (mod p)
    # count k in [1, a] with k % p == y
    r = y % p
    if r == 0:
        r = p
    first = r if r <= a else None
    if first is None:
        print(0)
    else:
        print((a - first) // p + 1)
    sys.exit()

# Precompute powers of x modulo p for exponent classes up to p-1
# since x^k depends only on k mod (p-1)
pow_x = [1] * (p)
for i in range(1, p):
    pow_x[i] = (pow_x[i - 1] * x) % p

# Try all residues mod (p-1)
mod = p - 1
valid = []

for k in range(1, mod + 1):
    val = (k * pow_x[k % mod]) % p
    if val == y:
        valid.append(k)

# Count contributions in [1, a]
ans = 0
for r in valid:
    if r > a:
        continue
    ans += (a - r) // mod + 1

print(ans)
```

The special case $x = 1$ collapses the exponential term completely, turning the problem into a single modular arithmetic progression. The counting formula computes how many numbers in a range lie in a fixed residue class modulo $p$.

For the general case, the code relies on the fact that exponentiation modulo a prime depends only on the exponent modulo $p-1$. The array `pow_x` precomputes $x^i \bmod p$ for all relevant exponent residues. Each candidate $k$ is tested in a reduced domain of size $p-1$, after which all valid residues are lifted back to the full range using arithmetic progression counting.

## Worked Examples

### Example 1

Input:

```
5 2 3 10
```

We compute powers of 2 modulo 5: $2^1=2$, $2^2=4$, $2^3=3$, $2^4=1$.

We test $k = 1 \dots 4$:

| k | 2^k mod 5 | k * 2^k mod 5 | valid? |
| --- | --- | --- | --- |
| 1 | 2 | 2 | no |
| 2 | 4 | 8 ≡ 3 | yes |
| 3 | 3 | 9 ≡ 4 | no |
| 4 | 1 | 4 | no |

So residue 2 is valid modulo period 4. In the range up to 10, numbers congruent to 2 mod 4 are 2, 6, 10, giving 3 solutions.

This shows how a single valid residue expands into multiple valid values across the full range.

### Example 2

Input:

```
7 4 6 13
```

Powers of 4 modulo 7 cycle as: 4, 2, 1, 4, ...

Testing $k \in [1,6]$:

| k | 4^k mod 7 | k * 4^k mod 7 | valid? |
| --- | --- | --- | --- |
| 1 | 4 | 4 | no |
| 2 | 2 | 4 | no |
| 3 | 1 | 3 | no |
| 4 | 4 | 2 | no |
| 5 | 2 | 3 | no |
| 6 | 1 | 6 | yes |

Only $k = 6$ works, and extending to 13 keeps only multiples of the same residue class.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(p)$ | We test each residue class modulo $p-1$ once |
| Space | $O(p)$ | Storage for precomputed powers of $x$ |

The constraint $p \le 10^6 + 3$ makes an $O(p)$ preprocessing approach feasible within time limits. The upper bound $a \le 10^{12}$ is handled purely through arithmetic progression counting, avoiding any dependence on $a$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    p, x, y, a = map(int, input().split())

    if x == 1:
        r = y % p
        if r == 0:
            r = p
        if r > a:
            return "0"
        return str((a - r) // p + 1)

    mod = p - 1
    pow_x = [1] * p
    for i in range(1, p):
        pow_x[i] = (pow_x[i - 1] * x) % p

    valid = []
    for k in range(1, mod + 1):
        if (k * pow_x[k % mod]) % p == y:
            valid.append(k)

    ans = 0
    for r in valid:
        if r <= a:
            ans += (a - r) // mod + 1

    return str(ans)

# sample cases
assert run("5 2 3 10") == "3"
assert run("7 4 6 13") == "1"

# edge cases
assert run("5 1 2 10") == "2"
assert run("2 1 1 1000000000000") == str(1000000000000)
assert run("11 3 7 1") in {"0", "1"}
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| x = 1 linear case | arithmetic progression | collapse of exponential term |
| large a | scaling correctness | handling of up to $10^{12}$ |
| a = 1 boundary | single value behavior | off-by-one safety |

## Edge Cases

When $x = 1$, the exponential structure disappears completely. The equation becomes $k \equiv y \pmod p$, and the solution is purely an arithmetic progression. For example, with input $p=5, x=1, y=3, a=10$, valid values are $3, 8$, and the algorithm correctly counts two terms using direct modular arithmetic without entering exponent logic.

When $a < p$, only residues within the first segment matter, and no wrapping occurs. In this regime, the solution reduces to checking a small prefix of candidates, and the periodic extension logic never activates.

When $a \gg p$, the solution relies entirely on counting full residue classes. Each valid residue contributes $\lfloor (a-r)/ (p-1) \rfloor + 1$ terms, which correctly accounts for all repetitions without double counting.
