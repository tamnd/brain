---
title: "CF 104053G - Game"
description: "Two players repeatedly build up numbers by multiplying chosen integers. Alice controls set $A$, Bob controls set $B$. Both start with values $alpha = 1$ and $beta = 1$. On every Alice move she picks any element from $A$ and multiplies it into $alpha$."
date: "2026-07-02T03:36:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104053
codeforces_index: "G"
codeforces_contest_name: "2022 China Collegiate Programming Contest (CCPC) Guangzhou Onsite"
rating: 0
weight: 104053
solve_time_s: 68
verified: true
draft: false
---

[CF 104053G - Game](https://codeforces.com/problemset/problem/104053/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

Two players repeatedly build up numbers by multiplying chosen integers. Alice controls set $A$, Bob controls set $B$. Both start with values $\alpha = 1$ and $\beta = 1$. On every Alice move she picks any element from $A$ and multiplies it into $\alpha$. On every Bob move he picks any element from $B$ and multiplies it into $\beta$. The process alternates forever, starting with Alice.

Bob’s winning condition is simple but global in time: if at any moment $\alpha$ divides $\beta$, Bob immediately wins. Alice never has a direct winning condition; her goal is only to avoid ever reaching a state where Bob can force this divisibility condition.

We are allowed to remove any subset of elements from $A$ before the game begins. After removing elements, the game is played with the remaining numbers in $A$. A subset is called valid if removing it does not change the fact that Alice can still avoid losing under optimal play. We must count how many subsets are valid.

The constraints are small enough that factorization and per-element reasoning are feasible. Both sets contain at most 500 numbers, and each number is at most 500. This immediately suggests that prime factorization is the correct language, since all interactions under multiplication decompose cleanly over primes. Any solution that tries to simulate gameplay directly is too slow because the game is infinite and branching over choices is exponential at every turn.

A subtle edge case is when Alice already loses even without removing anything. For example, if Bob can guarantee $\alpha \mid \beta$ from the start regardless of strategy, then no subset helps Alice and the answer must be zero. Another corner case is the empty subset of $A$. Removing everything makes $\alpha$ stay at 1 forever, so Bob trivially wins at the start since $\beta$ also starts at 1, making divisibility immediate. This means the empty subset is never valid.

## Approaches

The naive interpretation of the game tries to simulate optimal play. At every step, Alice and Bob choose moves that maximize their own objective. A brute-force state would need to track the current values of $\alpha$ and $\beta$, which grow multiplicatively without bound, and also consider all future choices of both players. Even if we compress values, the branching factor remains $|A| \cdot |B|$ per move, and the game has no natural termination bound. This makes direct game simulation infeasible.

The key observation comes from rewriting the divisibility condition in terms of prime exponents. Write every number as a vector of exponents over primes up to 500. Then $\alpha \mid \beta$ is equivalent to every prime having exponent in $\alpha$ not exceeding that in $\beta$. Since multiplication adds exponents, each move adds one of these vectors.

Now the game becomes a competition over multiple independent coordinates. On each turn Alice adds one vector from $A$, Bob adds one from $B$. Since they can reuse elements, long-term behavior is governed by which vectors maximize growth in each direction. For a fixed prime $p$, only the maximum exponent contributed by any element matters asymptotically, because repeatedly choosing the best contributor dominates any mixed strategy.

This reduces the game to comparing, for each prime $p$, the maximum exponent available to Alice and Bob. If Bob’s maximum is at least Alice’s maximum for every prime, then Bob can eventually match or exceed Alice in every coordinate and force divisibility. Otherwise, if there exists a prime where Alice has a strictly larger maximum contributor, she can keep that coordinate ahead forever, preventing Bob’s win condition.

Once this characterization is available, the subset problem becomes purely structural. Removing elements from $A$ changes Alice’s maximum exponent per prime. A subset is valid exactly when after removal there still exists at least one prime where Alice’s remaining maximum exceeds Bob’s fixed maximum.

This turns the problem into counting subsets that avoid destroying all “winning primes”.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Game Simulation | Exponential in moves | Large state space | Too slow |
| Prime-factor + subset counting | $O(n \cdot P + n \log n)$ | $O(n \cdot P)$ | Accepted |

## Algorithm Walkthrough

We first precompute prime factorizations for all numbers up to 500 so that each number can be represented as a vector of exponents.

1. Factor every number in $B$, and compute for each prime $p$ the maximum exponent appearing among all elements of $B$. Call this $maxB[p]$. This captures Bob’s strongest possible growth in each coordinate.
2. Factor every number in $A$, and similarly compute $maxA[p]$, the maximum exponent present in the full set $A$. This tells us whether Alice is globally ahead in each prime direction before any deletions.
3. If for every prime $p$, $maxA[p] \le maxB[p]$, then Bob already dominates or matches Alice in all coordinates. In this case Alice cannot maintain any advantage even with the full set, so every subset is losing and the answer is zero.
4. Otherwise, identify which elements of $A$ are “safe”. An element is safe if for every prime $p$, its exponent does not exceed $maxB[p]$. These elements cannot individually push any coordinate beyond Bob’s capability.
5. Let $k$ be the number of safe elements. Any subset composed only of safe elements cannot create a prime where Alice exceeds Bob, so all such subsets are losing positions for Alice.
6. Therefore, invalid subsets are exactly all subsets of safe elements, which is $2^k$. The total number of subsets is $2^{|A|}$, so valid subsets equal $2^{|A|} - 2^k$, taken modulo $10^9+7$.

The reason this works is that only the maximum exponent per prime matters for the long-term dominance condition. Any element exceeding Bob’s bound in at least one prime is enough to potentially maintain Alice’s advantage in that coordinate, so removing all such elements destroys her only winning direction. Conversely, keeping at least one such element preserves at least one coordinate where Alice can stay ahead indefinitely.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7
MAXV = 500

# sieve for smallest prime factor
spf = list(range(MAXV + 1))
for i in range(2, MAXV + 1):
    if spf[i] == i:
        for j in range(i * i, MAXV + 1, i):
            if spf[j] == j:
                spf[j] = i

def factor(x):
    res = {}
    while x > 1:
        p = spf[x]
        cnt = 0
        while x % p == 0:
            x //= p
            cnt += 1
        res[p] = cnt
    return res

n, m = map(int, input().split())
A = list(map(int, input().split()))
B = list(map(int, input().split()))

maxB = {}
for b in B:
    f = factor(b)
    for p, c in f.items():
        maxB[p] = max(maxB.get(p, 0), c)

maxA_full = {}
for a in A:
    f = factor(a)
    for p, c in f.items():
        maxA_full[p] = max(maxA_full.get(p, 0), c)

# check if Alice is already doomed
alice_wins_somewhere = False
for p, v in maxA_full.items():
    if v > maxB.get(p, 0):
        alice_wins_somewhere = True
        break

if not alice_wins_somewhere:
    print(0)
    sys.exit()

maxB_default = lambda p: maxB.get(p, 0)

safe = 0
for a in A:
    f = factor(a)
    ok = True
    for p, c in f.items():
        if c > maxB_default(p):
            ok = False
            break
    if ok:
        safe += 1

ans = (pow(2, n, MOD) - pow(2, safe, MOD)) % MOD
print(ans)
```

The implementation relies on a smallest prime factor sieve to factor every number quickly. This is necessary because repeated trial division would still be fast enough here but is less structured and harder to reason about.

We compute Bob’s per-prime maxima once and treat them as fixed thresholds. Then each element of $A$ is classified as safe or unsafe by comparing its prime exponents against these thresholds. The final combinatorial subtraction comes directly from counting subsets.

A subtle implementation detail is the early exit when Alice has no winning prime even in the full set. In that case, no subset can change the outcome, so returning zero is required by the problem statement.

## Worked Examples

### Example 1

Input:

```
2 3
2 6
6 7 8
```

We compute Bob’s maxima: $6 = 2 \cdot 3$, $7$, $8 = 2^3$. So $maxB[2]=3$, $maxB[3]=1$, $maxB[7]=1$.

For Alice, $2$ gives $2^1$, $6$ gives $2^1 \cdot 3^1$, so $maxA[2]=1$, $maxA[3]=1$. Alice never exceeds Bob in any prime, so she is already dominated. The algorithm outputs 0.

This demonstrates the early termination case.

### Example 2

Consider:

```
2 2
4 9
2 3
```

Bob has $2^1$ and $3^1$, so $maxB[2]=1$, $maxB[3]=1$. Alice has $4=2^2$, $9=3^2$, so she has winning primes in both coordinates.

Safe elements are those not exceeding Bob’s maxima. Neither 4 nor 9 is safe, so $k=0$. Total subsets are 4, invalid subsets are 1 (empty set), so answer is 3.

This shows how subsets are counted purely through element classification.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(( | A |
| Space | $O(V)$ | Storage for smallest prime factors and exponent maps |

The constraints cap both sets at 500 elements with values up to 500, so factoring and per-element scans remain comfortably within limits. The solution avoids any combinatorial explosion by reducing the game to per-prime maxima.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import prod

    MOD = 10**9 + 7
    MAXV = 500
    spf = list(range(MAXV + 1))
    for i in range(2, MAXV + 1):
        if spf[i] == i:
            for j in range(i * i, MAXV + 1, i):
                if spf[j] == j:
                    spf[j] = i

    def factor(x):
        res = {}
        while x > 1:
            p = spf[x]
            c = 0
            while x % p == 0:
                x //= p
                c += 1
            res[p] = c
        return res

    n, m = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    maxB = {}
    for b in B:
        f = factor(b)
        for p, c in f.items():
            maxB[p] = max(maxB.get(p, 0), c)

    maxA = {}
    for a in A:
        f = factor(a)
        for p, c in f.items():
            maxA[p] = max(maxA.get(p, 0), c)

    if all(maxA.get(p, 0) <= maxB.get(p, 0) for p in maxA):
        return "0"

    safe = 0
    for a in A:
        f = factor(a)
        ok = True
        for p, c in f.items():
            if c > maxB.get(p, 0):
                ok = False
                break
        if ok:
            safe += 1

    return str((pow(2, n, MOD) - pow(2, safe, MOD)) % MOD)

# provided samples
assert run("""2 3
2 6
6 7 8
""") == "0"

# custom cases
assert run("""2 2
4 9
2 3
""") == "3", "both sides small primes"
assert run("""1 1
2
2
""") == "0", "equal powers immediate loss"
assert run("""3 2
2 4 8
2 3
""") == "6", "some safe some unsafe"
assert run("""1 1
4
2
""") == "1", "single element strictly stronger"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| equal small primes | 3 | subset subtraction logic |
| equal start powers | 0 | immediate Bob dominance |
| mixed powers | 6 | partial safe classification |
| single strong element | 1 | basic positive case |

## Edge Cases

When Alice has no prime where she exceeds Bob even before deletions, the full set is already losing. For an input like $A = [6]$, $B = [6]$, both have identical exponent profiles. The algorithm computes $maxA[p] \le maxB[p]$ for all primes and immediately returns zero. This matches the fact that even with no deletions Bob wins instantly.

When every element of $A$ is safe, the answer becomes $2^{|A|} - 2^{|A|} = 0$. For example if all $a_i$ are small and dominated by Bob in every prime, every subset still loses. The safe-count mechanism correctly captures this because every element passes the safety check.
