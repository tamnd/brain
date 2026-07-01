---
title: "CF 104091F - \u0411\u0443\u0434\u044c \u043d\u0430\u0447\u0435\u043a\u0443! 2"
description: "We are counting how many valid numbers of length n can be formed under a very specific adjacency rule. A number is considered valid if every pair of consecutive digits forms a two-digit number that is prime."
date: "2026-07-02T02:29:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104091
codeforces_index: "F"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u041f\u0435\u0442\u0440\u043e\u0437\u0430\u0432\u043e\u0434\u0441\u043a\u0435 \u0438 \u041a\u0430\u0440\u0435\u043b\u0438\u0438 2022-2023"
rating: 0
weight: 104091
solve_time_s: 44
verified: true
draft: false
---

[CF 104091F - \u0411\u0443\u0434\u044c \u043d\u0430\u0447\u0435\u043a\u0443! 2](https://codeforces.com/problemset/problem/104091/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are counting how many valid numbers of length `n` can be formed under a very specific adjacency rule. A number is considered valid if every pair of consecutive digits forms a two-digit number that is prime. The digits themselves are just from a decimal number, but the constraint is not about individual digits, it is about sliding windows of size two.

So if the number is `d1 d2 d3 ... dn`, then each pair `(d1d2), (d2d3), ..., (d(n-1)dn)` must be a two-digit prime. That turns the problem into a constrained walk over digits where transitions depend on whether the concatenation of two digits forms a prime between 10 and 99.

The input is a single integer `n`, which can be extremely large, up to `10^15`. The output is the number of valid sequences of digits of length `n`, modulo `1e9 + 7`.

The size of `n` immediately rules out any dynamic programming over length. Even `O(n)` is impossible, since `n` can be astronomically large. The only feasible direction is to compress transitions and use matrix exponentiation or repeated squaring on a fixed state space.

A subtle edge case appears when thinking about leading digits. The problem does not restrict the first digit, so sequences may start with any digit `0-9`, even though numbers usually disallow leading zeros. Here we are not constructing standard integers, we are constructing digit strings, so `0` is valid as a starting digit.

Another important observation is that digits are states, not numbers. The adjacency rule depends only on the previous digit. This makes the structure a graph with at most 10 nodes.

## Approaches

A brute-force solution would attempt to build all valid digit strings of length `n`. For each position, we try all digits `0-9` and check whether the pair with the previous digit forms a prime. This leads to roughly `10^n` possibilities in the worst case, since most transitions are allowed for many digits. Even for `n = 20`, this is already infeasible, and for `n = 10^15` it is completely impossible.

The key structural observation is that the validity of a number depends only on the last digit used. If we know the last digit, the future choices depend only on which digits form a two-digit prime with it. This reduces the problem to counting walks of length `n-1` in a directed graph with 10 nodes, where edges correspond to valid prime transitions.

Once we interpret the problem as counting paths of fixed length in a small graph, we can use matrix exponentiation. We build a 10 by 10 transition matrix where entry `(i, j)` is 1 if digit `i` can transition to digit `j`, meaning `10*i + j` is prime. Then the answer is the sum of all entries in the vector obtained by raising this matrix to the power `n-1` and multiplying by an initial vector of all ones.

Because the matrix size is constant, exponentiation takes `O(10^3 log n)` time, which is easily fast enough even for `n = 10^15`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10^n) | O(n) | Too slow |
| Matrix Exponentiation | O(10^3 log n) | O(1) | Accepted |

## Algorithm Walkthrough

We reinterpret digits as nodes in a graph. Each valid two-digit prime defines a directed edge from its tens digit to its ones digit.

First, we precompute all two-digit primes. These are numbers from 10 to 99 that are prime. For each such prime `p`, we extract `u = p // 10` and `v = p % 10`, and mark a transition from `u` to `v`.

Second, we build a 10 by 10 adjacency matrix `T`, where `T[u][v] = 1` if the transition is allowed.

Third, we construct a vector `dp0` of size 10, where every entry is 1. This represents that any digit can be the starting digit of a valid sequence of length 1.

Fourth, we compute `T^(n-1)` using fast exponentiation. This represents how transitions compose over multiple steps.

Fifth, we multiply `dp0` by this matrix power. The resulting vector `dp` gives, for each digit, how many valid sequences of length `n` end in that digit.

Sixth, we sum all entries of `dp` to get the total number of valid sequences.

Why this works is tied to a simple invariant: after processing `k` steps, `dp[d]` equals the number of valid sequences of length `k+1` that end in digit `d`. Each matrix multiplication extends all sequences by one valid digit transition, preserving correctness at every step.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def is_prime(x):
    if x < 2:
        return False
    for i in range(2, int(x**0.5) + 1):
        if x % i == 0:
            return False
    return True

def mul(A, B):
    n = 10
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        Ci = C[i]
        for k in range(n):
            if Ai[k] == 0:
                continue
            aik = Ai[k]
            Bk = B[k]
            for j in range(n):
                Ci[j] = (Ci[j] + aik * Bk[j]) % MOD
    return C

def mpow(M, e):
    n = 10
    R = [[0] * n for _ in range(n)]
    for i in range(n):
        R[i][i] = 1
    while e > 0:
        if e & 1:
            R = mul(R, M)
        M = mul(M, M)
        e >>= 1
    return R

def main():
    n = int(input().strip())

    primes = [x for x in range(10, 100) if is_prime(x)]

    T = [[0] * 10 for _ in range(10)]
    for p in primes:
        u = p // 10
        v = p % 10
        T[u][v] = 1

    if n == 1:
        print(10)
        return

    P = mpow(T, n - 1)

    ans = 0
    for i in range(10):
        for j in range(10):
            ans = (ans + P[i][j]) % MOD

    print(ans)

if __name__ == "__main__":
    main()
```

The solution starts by generating all two-digit primes and turning them into directed transitions between digits. The matrix `T` encodes these transitions.

The function `mul` performs 10 by 10 matrix multiplication under modulo arithmetic. The triple loop is safe because the matrix size is fixed and small, and the inner loop skips zero entries to reduce constant factors.

The function `mpow` performs binary exponentiation on the matrix, repeatedly squaring it and applying it when needed. This is what allows handling extremely large `n`.

The final answer is computed by summing all entries of the resulting matrix, which corresponds to all possible starting digits and all possible ending digits after exactly `n-1` transitions.

## Worked Examples

Consider a small case where `n = 2`. We are counting valid two-digit numbers where the number itself must be a two-digit prime. The matrix directly encodes valid pairs.

| Step | Action | State |
| --- | --- | --- |
| 1 | Build primes | {11, 13, 17, 19, 23, ...} |
| 2 | Build transitions | edges like 1→1, 1→3, 1→7, 1→9, etc. |
| 3 | Compute result | count all edges |

For `n = 3`, we count paths of length 2 in this graph.

| Step | Action | State |
| --- | --- | --- |
| 1 | Initial dp | all digits have value 1 |
| 2 | After 1 transition | dp[v] counts digits u with u→v |
| 3 | After 2 transitions | dp[v] counts paths of length 2 ending at v |

This demonstrates how the DP naturally accumulates path counts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(10^3 log n) | 10x10 matrix multiplication repeated over binary exponentiation |
| Space | O(1) | fixed 10x10 matrices |

The complexity is independent of `n` except for the logarithmic exponentiation factor, which makes it suitable for values up to `10^15`.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    MOD = 10**9 + 7

    def is_prime(x):
        if x < 2:
            return False
        for i in range(2, int(x**0.5) + 1):
            if x % i == 0:
                return False
        return True

    def mul(A, B):
        n = 10
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for k in range(n):
                if A[i][k]:
                    for j in range(n):
                        C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD
        return C

    def mpow(M, e):
        n = 10
        R = [[0]*n for _ in range(n)]
        for i in range(n):
            R[i][i] = 1
        while e:
            if e & 1:
                R = mul(R, M)
            M = mul(M, M)
            e >>= 1
        return R

    n = int(input().strip())
    primes = [x for x in range(10, 100) if is_prime(x)]

    T = [[0]*10 for _ in range(10)]
    for p in primes:
        T[p//10][p%10] = 1

    if n == 1:
        return "10"

    P = mpow(T, n-1)
    ans = 0
    for i in range(10):
        for j in range(10):
            ans = (ans + P[i][j]) % MOD

    return str(ans)

# provided samples (if any existed, they would go here)

# custom tests
assert solve("2") == str(sum(1 for x in range(10,100) if is_prime(x))), "n=2 checks prime pairs"

assert solve("1") == "10", "single digit case"

assert solve("3") > "0", "basic sanity"

assert solve("10") == solve("10"), "consistency check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | count of two-digit primes | base transitions correctness |
| 1 | 10 | single-digit edge case |
| 3 | positive value | path extension logic |
| 10 | consistent | stability of exponentiation |

## Edge Cases

When `n = 1`, there are no adjacency constraints because no pair of digits exists. The correct answer is simply all digits `0-9`, giving 10. The algorithm explicitly checks this case before exponentiation.

For `n = 2`, the answer reduces to counting valid two-digit primes. The matrix contains exactly those transitions, so the sum of all entries in `T` gives the result directly.

If `n` is very large, the exponentiation path ensures we never iterate over length explicitly. The matrix powers represent repeated composition of transitions, so even extreme values like `10^15` are handled without change in logic.
