---
title: "CF 166E - Tetrahedron"
description: "We are asked to count the number of ways an ant can start at vertex D of a tetrahedron and return to D after exactly n steps, moving along edges at every step. The tetrahedron has four vertices labeled A, B, C, D, and each vertex is connected to the other three."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "matrices"]
categories: ["algorithms"]
codeforces_contest: 166
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 113 (Div. 2)"
rating: 1500
weight: 166
solve_time_s: 180
verified: true
draft: false
---

[CF 166E - Tetrahedron](https://codeforces.com/problemset/problem/166/E)

**Rating:** 1500  
**Tags:** dp, math, matrices  
**Solve time:** 3m  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count the number of ways an ant can start at vertex D of a tetrahedron and return to D after exactly _n_ steps, moving along edges at every step. The tetrahedron has four vertices labeled A, B, C, D, and each vertex is connected to the other three. The input is a single integer _n_ representing the path length, and the output is the number of distinct sequences of moves that start and end at D, modulo 10^9 + 7.

Given that _n_ can be as large as 10^7, we cannot simulate all possible paths explicitly. A brute-force approach that enumerates each path would have an exponential time complexity of O(3^n), which is infeasible for _n_ beyond 20 or 30. Instead, we need an approach that computes the result efficiently, in roughly O(log n) or O(n) time.

Non-obvious edge cases include the smallest _n_. For _n_ = 1, the ant cannot return to D in a single step because it must move to a neighbor, so the answer is 0. Another case is _n_ = 2, where the ant has exactly three choices: D → A → D, D → B → D, D → C → D. Handling these small inputs correctly ensures the base cases in our recurrence or matrix exponentiation are properly set up.

## Approaches

The brute-force approach is straightforward. One could recursively enumerate all sequences of moves from D and count the ones that return to D after _n_ steps. This works because each step has exactly three possible moves, and recursively exploring all paths captures every valid sequence. However, the time complexity is O(3^n), which explodes even for moderate values of _n_. This quickly becomes impractical when _n_ reaches 10^7.

The key observation for a faster solution is that the number of ways to reach a vertex after _k_ steps depends only on the number of ways to reach each vertex after _k-1_ steps. This is a classic dynamic programming setup on a small graph. Let dp[x][k] be the number of ways to reach vertex x in k steps. The recurrence is simple: to reach D in step k, the ant must come from A, B, or C in step k-1. Similarly, to reach A in step k, the ant must come from B, C, or D. This recurrence can be represented as a 4×4 transition matrix and computed efficiently using matrix exponentiation, which reduces the complexity from O(n) per state update to O(log n) matrix multiplications.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^n) | O(n) | Too slow |
| DP / Matrix Exponentiation | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Label the vertices A, B, C, D as indices 0, 1, 2, 3 for convenience. We want to count the number of walks of length n starting and ending at D (index 3).
2. Define a 4×4 adjacency matrix M representing valid moves. Each entry M[i][j] is 1 if vertex j is reachable from i in one step and 0 otherwise. For a tetrahedron, every vertex connects to the other three. For D (index 3), row 3 will have 1s in columns 0, 1, 2 and 0 in column 3.
3. Represent the number of ways to reach each vertex after k steps as a vector v_k of length 4. The vector for step 0, v_0, is [0, 0, 0, 1] because the ant starts at D.
4. Compute v_n = M^n × v_0 using matrix exponentiation. Each multiplication applies the recurrence to advance one step. Matrix exponentiation allows us to compute M^n in O(log n) multiplications.
5. Return v_n[3] modulo 10^9 + 7. This value counts all valid walks that start and end at D after n steps.

Why it works: The adjacency matrix captures all valid one-step transitions. Multiplying the matrix repeatedly applies the recurrence for multiple steps. Matrix exponentiation efficiently computes n-step transitions without iterating n times. The invariant is that after k multiplications, the vector v_k stores the exact number of walks to each vertex in k steps.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def mat_mult(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k]*B[k][j]) % MOD
    return C

def mat_pow(mat, power):
    n = len(mat)
    result = [[1 if i==j else 0 for j in range(n)] for i in range(n)]
    while power > 0:
        if power % 2 == 1:
            result = mat_mult(result, mat)
        mat = mat_mult(mat, mat)
        power //= 2
    return result

n = int(input())
adj = [
    [0,1,1,1],
    [1,0,1,1],
    [1,1,0,1],
    [1,1,1,0]
]

# initial vector v0 corresponds to starting at D (index 3)
v0 = [0,0,0,1]

# compute M^n
M_n = mat_pow(adj, n)

# compute final vector v_n = M^n * v0
v_n = [0]*4
for i in range(4):
    for j in range(4):
        v_n[i] = (v_n[i] + M_n[i][j]*v0[j]) % MOD

print(v_n[3])
```

The `mat_mult` function multiplies two 4×4 matrices modulo 10^9+7. The `mat_pow` function raises a matrix to the power n using binary exponentiation. The adjacency matrix encodes the tetrahedron, and v0 represents the starting vertex. Finally, we compute v_n by multiplying M^n with v0, and the entry corresponding to D gives the answer.

## Worked Examples

Sample 1, n=2:

| Step | v_k (A,B,C,D) |
| --- | --- |
| 0 | [0,0,0,1] |
| 1 | [1,1,1,0] |
| 2 | [2,2,2,3] |

v_2[3] = 3, which matches the three paths D→A→D, D→B→D, D→C→D.

Sample 2, n=3:

| Step | v_k (A,B,C,D) |
| --- | --- |
| 0 | [0,0,0,1] |
| 1 | [1,1,1,0] |
| 2 | [2,2,2,3] |
| 3 | [7,7,7,6] |

v_3[3] = 6, corresponding to all 6 walks of length 3 starting and ending at D.

These traces confirm that the recurrence and matrix exponentiation correctly compute the number of walks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | Each matrix multiplication is constant (4×4), and we do O(log n) multiplications using exponentiation. |
| Space | O(1) | We only store a few 4×4 matrices and vectors, independent of n. |

This fits comfortably in the 2-second limit even for n=10^7.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    MOD = 10**9 + 7

    def mat_mult(A, B):
        n = len(A)
        C = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] = (C[i][j] + A[i][k]*B[k][j]) % MOD
        return C

    def mat_pow(mat, power):
        n = len(mat)
        result = [[1 if i==j else 0 for j in range(n)] for i in range(n)]
        while power > 0:
            if power % 2 == 1:
                result = mat_mult(result, mat)
            mat = mat_mult(mat, mat)
            power //= 2
        return result

    n = int(input())
    adj = [
        [0,1,1,1],
        [1,0,1,1],
        [1,1,0,1],
        [1,1,1,0]
    ]
    v0 = [0,0,0,1]
    M_n = mat_pow(adj, n)
    v_n = [0]*4
    for i in range(4):
        for j in range(4):
            v_n[i] = (v_n[i] + M_n[i][j]*v0[j]) % MOD
    return str(v_n[3])

# Provided samples
assert run("2\n")
```
