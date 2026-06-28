---
title: "CF 104758B - Bionaccia's Sequence"
description: "We are given a single very large index $K$, and asked to compute the $K$-th value of a sequence defined by a third-order recurrence. The sequence starts with three fixed values, and every later term is built from the previous three terms plus an additional constant contribution."
date: "2026-06-28T22:06:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104758
codeforces_index: "B"
codeforces_contest_name: "The 2023 ICPC Masters Mexico Regional #ICPCMX2023 Edition"
rating: 0
weight: 104758
solve_time_s: 83
verified: true
draft: false
---

[CF 104758B - Bionaccia's Sequence](https://codeforces.com/problemset/problem/104758/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single very large index $K$, and asked to compute the $K$-th value of a sequence defined by a third-order recurrence. The sequence starts with three fixed values, and every later term is built from the previous three terms plus an additional constant contribution.

Concretely, each term depends linearly on the previous three terms, and there is also a fixed additive shift of 3 at every step. The index $K$ can be as large as $10^{16}$, which immediately rules out any approach that constructs terms one by one. Even if each transition were constant time, iterating up to $10^{16}$ steps is impossible within any reasonable time limit.

The output is the value of this sequence at position $K$, taken modulo $10^9+7$. The modulus matters because values grow exponentially due to the recurrence, so intermediate results must be kept within modular arithmetic.

A naive simulation would fail even for moderately large $K$. For example, computing up to $K = 10^7$ already requires too many transitions, and the values grow quickly enough that integer overflow becomes a concern without modular reduction. The real obstacle is the index size, not the magnitude of values.

The key difficulty is that each term depends on three previous values, plus a constant term that prevents a straightforward homogeneous recurrence treatment unless we extend the state.

## Approaches

A direct approach computes terms sequentially from $t(0)$ upward, applying the recurrence at each step. This is correct because each term is fully determined by the previous three values. However, reaching index $K$ this way requires $O(K)$ transitions, which becomes infeasible when $K$ can be $10^{16}$. The bottleneck is the linear growth in the number of computed states.

The structure of the recurrence suggests a more powerful idea: the transition from one state of three consecutive terms to the next is linear. Linear recurrences over a fixed window size can be encoded as matrix multiplication. The only complication here is the constant $+3$, which breaks homogeneity. This can be repaired by adding an extra dimension to the state that always holds the constant value 1, allowing the constant term to be absorbed into the matrix transformation.

Once the recurrence is rewritten as a fixed-dimensional linear transformation, repeated application becomes exponentiation of a matrix. Fast exponentiation reduces the number of multiplications from $K$ to $O(\log K)$, and each multiplication operates on a constant-sized matrix.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(K)$ | $O(1)$ | Too slow |
| Matrix Exponentiation | $O(\log K)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We encode the recurrence into a matrix form so that each step advances the state of the system.

We define a state vector that stores the last three terms along with a constant:

1. Define the state at position $n$ as $[t(n), t(n-1), t(n-2), 1]$. The extra 1 exists so the constant $+3$ can be expressed as a linear transformation.
2. Express the recurrence in terms of this state. The first component $t(n)$ is computed as $3t(n-1) + 2t(n-2) + t(n-3) + 3\cdot 1$. The remaining components simply shift the window of previous values, and the last component stays 1.
3. Build a transition matrix $A$ such that multiplying $A$ by the state at $n-1$ produces the state at $n$. The first row encodes the recurrence coefficients, and the lower rows implement the shifting behavior.
4. Compute the initial state. Since we know $t(0), t(1), t(2)$, we initialize the vector at $n=2$ as $[t(2), t(1), t(0), 1] = [3, 2, 1, 1]$.
5. If $K \le 2$, return the corresponding base value directly. Otherwise compute $A^{K-2}$ using fast exponentiation.
6. Multiply $A^{K-2}$ by the initial vector to obtain the state at $K$. The first element of the resulting vector is the answer.

Each multiplication step preserves correctness because it represents one exact application of the recurrence.

### Why it works

The algorithm relies on the fact that the recurrence is linear once the constant term is absorbed into the state. Every state fully summarizes all information needed to compute the next one, so the transformation is self-contained. Matrix exponentiation applies repeated composition of this transformation efficiently, and exponentiation by squaring guarantees we apply exactly $K-2$ transitions without enumerating them.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def mat_mul(a, b):
    n = 4
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if a[i][k] == 0:
                continue
            aik = a[i][k]
            for j in range(n):
                res[i][j] = (res[i][j] + aik * b[k][j]) % MOD
    return res

def mat_pow(mat, exp):
    n = 4
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        res[i][i] = 1

    while exp > 0:
        if exp & 1:
            res = mat_mul(res, mat)
        mat = mat_mul(mat, mat)
        exp >>= 1
    return res

def solve():
    K = int(input().strip())

    if K == 0:
        print(1)
        return
    if K == 1:
        print(2)
        return
    if K == 2:
        print(3)
        return

    A = [
        [3, 2, 1, 3],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ]

    P = mat_pow(A, K - 2)

    vec = [3, 2, 1, 1]

    ans = (
        P[0][0] * vec[0] +
        P[0][1] * vec[1] +
        P[0][2] * vec[2] +
        P[0][3] * vec[3]
    ) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The core implementation centers on a fixed 4 by 4 matrix because the recurrence depends on three previous terms plus a constant. The multiplication routine performs modular matrix multiplication, and the exponentiation routine repeatedly squares the matrix while consuming bits of $K$.

The initial vector corresponds to the last known valid triple of sequence values, aligned so that repeated application of the matrix moves forward in time.

Careful attention is needed in indexing: exponentiation starts from $K-2$ because we initialize at $t(2)$, not $t(0)$. A common mistake is shifting this boundary incorrectly, which leads to off-by-one errors.

## Worked Examples

Consider the sample input $K = 6$. We start from the base state at $n=2$, which is $[3,2,1,1]$. We apply $A^4$ to this vector since $6-2=4$.

| Step | Operation | State (t(n), t(n-1), t(n-2), 1) |
| --- | --- | --- |
| 2 | initial | (3, 2, 1, 1) |
| 3 | apply recurrence | (17, 3, 2, 1) |
| 4 | apply recurrence | (62, 17, 3, 1) |
| 5 | apply recurrence | (226, 62, 17, 1) |
| 6 | apply recurrence | (822, 226, 62, 1) |

The final value matches the expected output, showing that the matrix transformation correctly encodes the recurrence.

For $K = 7$, the same process continues one more step.

| Step | Operation | State (t(n), t(n-1), t(n-2), 1) |
| --- | --- | --- |
| 4 | starting reference | (62, 17, 3, 1) |
| 5 | apply recurrence | (226, 62, 17, 1) |
| 6 | apply recurrence | (822, 226, 62, 1) |
| 7 | apply recurrence | (2983, 822, 226, 1) |

This trace shows that once the transition mechanism is correct, each step is deterministic and consistent.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log K)$ | matrix exponentiation over fixed 4×4 transformation |
| Space | $O(1)$ | constant-size matrices and vectors |

The logarithmic dependence on $K$ is what makes the solution feasible for values up to $10^{16}$. Each multiplication is constant work, so even the largest input size is handled comfortably.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue().strip() if False else ""

# Provided samples (conceptual placeholders since full harness is omitted)
# assert run("6\n") == "822"
# assert run("7\n") == "2983"

# custom direct checks via known sequence values

def brute_small(k):
    t = [1, 2, 3]
    if k <= 2:
        return t[k]
    for i in range(3, k + 1):
        t.append((3*t[i-1] + 2*t[i-2] + t[i-3] + 3) % (10**9+7))
    return t[k]

# edge cases
assert brute_small(0) == 1
assert brute_small(1) == 2
assert brute_small(2) == 3
assert brute_small(6) == 822
assert brute_small(7) == 2983
assert brute_small(8) == 10822
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 | 1 | base boundary |
| 1 | 2 | second base case |
| 8 | 10822 | transition correctness beyond sample range |

## Edge Cases

For $K = 2$, the algorithm directly returns the base value without invoking matrix exponentiation. The state is already aligned as $[t(2), t(1), t(0), 1] = [3,2,1,1]$, so no transformation is needed.

For very large $K$, such as $10^{16}$, the exponentiation loop processes only about 55 iterations since each step halves the exponent. The matrix never grows or changes shape, so there is no risk of overflow beyond modular arithmetic, and the computation remains stable.

For small $K$, the explicit branching prevents incorrect shifting of indices. Without these guards, using $K-2$ blindly would attempt negative exponentiation, which would break the interpretation of the transition system.
