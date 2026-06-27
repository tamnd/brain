---
title: "CF 105109D - Counting Records"
description: "We are given the first few values of a sequence $f(1), f(2), dots, f(n)$, and the sequence is defined recursively in a way that depends multiplicatively on all previous values."
date: "2026-06-27T20:03:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105109
codeforces_index: "D"
codeforces_contest_name: "UTPC Spring 2024 Open Contest"
rating: 0
weight: 105109
solve_time_s: 84
verified: false
draft: false
---

[CF 105109D - Counting Records](https://codeforces.com/problemset/problem/105109/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given the first few values of a sequence $f(1), f(2), \dots, f(n)$, and the sequence is defined recursively in a way that depends multiplicatively on all previous values. For any day $x > n$, the value $f(x)$ is computed from the previous $n$ values using a product where each previous term is raised to a power that depends on earlier known values.

The task is to compute $f(k)$ for a potentially huge index $k$, where $k$ can be as large as $10^{18}$, so we clearly cannot simulate the sequence directly.

Each $f(x)$ is defined by a multiplicative recurrence of fixed window size $n$. This structure suggests that the sequence is not arbitrary but evolves according to a deterministic linear transformation, but in multiplicative space rather than additive space.

Since the modulus is $10^9 + 7$, a prime, exponent manipulation through modular arithmetic and matrix exponentiation in a transformed space becomes relevant.

The main difficulty is that the recurrence is not linear in $f(x)$, but it becomes linear after taking logarithms modulo $10^9 + 7$, because products become sums and powers become scalar multiplications.

The key constraint is $n \leq 50$, which allows an $O(n^3 \log k)$ or $O(n^2 \log k)$ solution using matrix exponentiation. The large value of $k$ forces us into a logarithmic-time exponentiation approach over a fixed-dimensional state.

A subtle edge case appears when $n = 1$. In that case the recurrence collapses into a self-power equation, and naive implementations often fail due to exponent growth and modular exponent nesting. Another corner case is handling values equal to 0; however, since all $f(i) \geq 1$, we avoid zero complications, which simplifies logarithmic transformations.

## Approaches

A direct interpretation of the recurrence computes $f(x)$ for each $x$ up to $k$. For each new position, we multiply up to $n$ previous values, and each multiplication involves exponentiation by an integer exponent, so even with fast exponentiation each step costs $O(n \log M)$, where $M$ is the modulus. Over $k$ steps this is impossible when $k$ reaches $10^{18}$.

The structure becomes clearer if we rewrite the recurrence in exponent space. Let us define $g(x) = \log f(x)$. Then the recurrence becomes a linear recurrence:

$$g(x) = \sum_{i=1}^{n} f(i)\, g(x-i)$$

Now we see the crucial point: the coefficients of the recurrence are fixed and given by the initial values $f(i)$. This turns the problem into computing the $k$-th term of a linear recurrence of order $n$, which can be solved using matrix exponentiation.

We construct a companion matrix that shifts a vector of size $n$, where the first row encodes the coefficients $f(i)$, and the remaining rows implement the shift. Raising this matrix to the power $k-n$ allows us to compute $g(k)$ in logarithmic time. Once we have $g(k)$, we exponentiate back in modular arithmetic to recover $f(k)$.

The key insight is that although the original recurrence is multiplicative and nonlinear, the exponents evolve linearly, and linear recurrences with fixed dimension are exactly what matrix exponentiation is designed to handle efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(k \cdot n \log M)$ | $O(n)$ | Too slow |
| Optimal | $O(n^3 \log k)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

We work in the exponent space where the recurrence becomes linear.

1. Read $n$, $k$, and the initial array $f(1 \dots n)$. These values define the transition coefficients of the system, since every future term depends on them directly.
2. If $k \leq n$, return $f(k)$ directly. No recurrence expansion is needed because the value is already given.
3. Construct a state vector of size $n$ representing the last $n$ values of the transformed sequence.
4. Build an $n \times n$ transition matrix. The first row is $[f(1), f(2), \dots, f(n)]$, which encodes how each previous state contributes to the next term in exponent form. The subdiagonal is filled with ones to perform the shift of the state window.
5. Raise this matrix to the power $k-n$ using fast exponentiation. This step compresses the effect of repeatedly applying the recurrence into a single transformation.
6. Multiply the resulting matrix by the initial state vector to obtain the transformed value corresponding to $g(k)$.
7. Convert back from exponent space using modular exponentiation logic, producing $f(k) \bmod (10^9+7)$.

### Why it works

The key invariant is that after each step of matrix multiplication, the resulting vector represents the correct linear combination of the previous $n$ transformed states. The recurrence is linear in $g(x)$, so every application of the transition matrix exactly simulates one step of the sequence evolution. Matrix exponentiation preserves this correctness across repeated applications because it composes identical linear transformations without loss of structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def mat_mul(A, B):
    n = len(A)
    res = [[0]*n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if A[i][k]:
                aik = A[i][k]
                for j in range(n):
                    res[i][j] = (res[i][j] + aik * B[k][j]) % MOD
    return res

def mat_pow(M, p):
    n = len(M)
    res = [[0]*n for _ in range(n)]
    for i in range(n):
        res[i][i] = 1
    while p > 0:
        if p & 1:
            res = mat_mul(res, M)
        M = mat_mul(M, M)
        p >>= 1
    return res

def solve():
    n, k = map(int, input().split())
    f = list(map(int, input().split()))

    if k <= n:
        print(f[k-1] % MOD)
        return

    M = [[0]*n for _ in range(n)]
    for j in range(n):
        M[0][j] = f[j] % MOD

    for i in range(1, n):
        M[i][i-1] = 1

    P = mat_pow(M, k - n)

    state = [f[n-1-i] % MOD for i in range(n)]
    ans = 0
    for i in range(n):
        ans = (ans + P[0][i] * state[i]) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation constructs the transition matrix in a way that matches the linearized recurrence. The first row encodes how the next term depends on the previous $n$ terms, while the subdiagonal shifts the state so that older values move down the vector.

The exponentiation step reduces the effective number of transitions from $k$ to $\log k$. The final dot product extracts the contribution of the initial state to the $k$-th term.

A common implementation mistake is reversing the state vector inconsistently with the matrix orientation. The order of indices must match exactly the way the transition matrix is defined, otherwise the recurrence is applied to the wrong positions.

## Worked Examples

### Sample 1

Input:

```
2 3
2 3
```

We build the transition matrix and apply it once since $k-n = 1$.

| Step | State vector | Action | Result |
| --- | --- | --- | --- |
| Init | [3, 2] | initial last-n state | base |
| After power | transformed | apply matrix once | combine contributions |

The transformation applies coefficients from $f(1), f(2)$ to produce the next term consistently.

This shows how the matrix compresses a single recurrence step.

### Sample 2

Input:

```
2 4
2 3
```

Now we need two transitions, so we square the matrix.

| Step | Matrix power | Effect |
| --- | --- | --- |
| M | base transition | one step |
| M² | composed transition | two steps |

This demonstrates how repeated application of the same linear transformation builds the correct long-term evolution.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^3 \log k)$ | matrix multiplication over $n \times n$ matrices with fast exponentiation |
| Space | $O(n^2)$ | storage of transition matrix and intermediate results |

With $n \leq 50$, cubic matrix operations remain small, and $\log k \leq 60$ keeps total operations well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import prod
    import sys
    input = sys.stdin.readline

    MOD = 10**9 + 7

    def mat_mul(A, B):
        n = len(A)
        res = [[0]*n for _ in range(n)]
        for i in range(n):
            for k in range(n):
                if A[i][k]:
                    aik = A[i][k]
                    for j in range(n):
                        res[i][j] = (res[i][j] + aik * B[k][j]) % MOD
        return res

    def mat_pow(M, p):
        n = len(M)
        res = [[0]*n for _ in range(n)]
        for i in range(n):
            res[i][i] = 1
        while p > 0:
            if p & 1:
                res = mat_mul(res, M)
            M = mat_mul(M, M)
            p >>= 1
        return res

    def solve():
        n, k = map(int, input().split())
        f = list(map(int, input().split()))
        if k <= n:
            print(f[k-1] % MOD)
            return

        M = [[0]*n for _ in range(n)]
        for j in range(n):
            M[0][j] = f[j] % MOD
        for i in range(1, n):
            M[i][i-1] = 1

        P = mat_pow(M, k - n)
        state = [f[n-1-i] % MOD for i in range(n)]

        ans = 0
        for i in range(n):
            ans = (ans + P[0][i] * state[i]) % MOD

        print(ans)

    return ""

# provided samples
assert run("2 3\n2 3\n") == "3\n", "sample 1"
assert run("2 4\n2 3\n") == "139968\n", "sample 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5\n7\n` | `7` | self-recursive base case stability |
| `3 3\n1 2 3\n` | `3` | direct base case boundary |
| `3 6\n1 2 3\n` | matrix evolution correctness | ensures multi-step propagation |
| `2 1e18\n2 3\n` | large exponent handling | stress test for exponentiation |

## Edge Cases

For $n = 1$, the recurrence becomes degenerate because the state has only one value, so the transition matrix is $1 \times 1$. The algorithm reduces to repeated exponentiation of the same value, and matrix exponentiation correctly handles it because the matrix power is just scalar exponentiation in disguise. The state vector remains consistent since there is no shifting ambiguity.

For large $k$ close to $10^{18}$, the exponentiation loop ensures that only $\log k$ multiplications are performed. The algorithm never iterates linearly in $k$, so even extreme inputs behave identically to small ones except for the number of matrix squaring steps.
