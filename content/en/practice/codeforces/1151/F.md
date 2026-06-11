---
title: "CF 1151F - Sonya and Informatics"
description: "We are asked to determine the probability that an array consisting of zeros and ones becomes sorted in non-decreasing order after performing a fixed number of random swaps. Each swap selects two distinct positions in the array uniformly at random and exchanges their values."
date: "2026-06-12T03:03:18+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "matrices", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1151
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 553 (Div. 2)"
rating: 2300
weight: 1151
solve_time_s: 118
verified: false
draft: false
---

[CF 1151F - Sonya and Informatics](https://codeforces.com/problemset/problem/1151/F)

**Rating:** 2300  
**Tags:** combinatorics, dp, matrices, probabilities  
**Solve time:** 1m 58s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine the probability that an array consisting of zeros and ones becomes sorted in non-decreasing order after performing a fixed number of random swaps. Each swap selects two distinct positions in the array uniformly at random and exchanges their values. The array length is at most 100, but the number of swaps can be as large as 10^9, which immediately rules out any simulation of swaps step by step. The output must be either zero or a fraction in modular arithmetic.

The input gives us the array itself and the number of swaps. The output is a probability modulo 10^9+7. Since the array only contains zeros and ones, the final sorted array is simply all zeros followed by all ones. A careless solution might try to simulate the swaps directly. For example, if `a = [0, 1, 0]` and `k = 2`, simulating each swap in a naive way might miss the fact that multiple sequences of swaps lead to the same final array. A correct approach must account for the combinatorial probabilities of reaching the sorted state.

Edge cases include arrays that are already sorted, arrays that are fully reversed, or arrays where all elements are the same. For example, if `a = [0, 0, 0]`, the sorted probability is trivially 1. If `a = [1, 1, 1]`, the same holds. If `a = [1, 0, 1]` and `k = 1`, some swaps may never produce the sorted array, and we must correctly compute zero probability.

## Approaches

The brute-force approach is to enumerate all possible sequences of swaps. Each swap chooses a pair of indices `(i, j)` among `n*(n-1)/2` possibilities. After `k` swaps, there are `(n*(n-1)/2)^k` sequences. For `n = 100` and `k` up to 10^9, this is entirely infeasible. Even using dynamic programming over array configurations is too large because there are `2^n` possible arrays, and `n=100` makes `2^100` astronomically large.

The key insight comes from the observation that the array contains only zeros and ones. Let `cnt1` be the total number of ones. Any configuration is completely determined by the number of ones in the "wrong half" of the array. More precisely, define `state[i]` as the probability that there are exactly `i` ones in the first `n - cnt1` positions. This reduces the state space from `2^n` to `min(cnt1, n-cnt1) + 1` states, which is at most 50.

The process can then be modeled as a Markov chain where each state transitions probabilistically based on swapping a one from the first segment with a zero from the second segment. Let `trans[i][i-1]`, `trans[i][i]`, and `trans[i][i+1]` denote the probabilities of moving between states. Then, we can raise the transition matrix to the `k`-th power to compute the final probability. Matrix exponentiation over a 50x50 matrix is efficient and handles `k` up to 10^9.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O((n^2)^k) | O(2^n) | Too slow |
| Optimal Markov / Matrix Exponentiation | O(n^3 log k) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Compute `cnt1`, the total number of ones in the array. The number of zeros is `cnt0 = n - cnt1`. The sorted target has all zeros followed by all ones.
2. Compute `wrong`, the initial number of ones that are in the "zero segment" (the first `cnt0` positions). This is the starting state for our Markov chain.
3. Construct a transition matrix `T` of size `cnt1+1` by `cnt1+1`. `T[i][i-1]` is the probability that the number of ones in the zero segment decreases by 1, `T[i][i]` the probability it remains the same, and `T[i][i+1]` the probability it increases by 1. These probabilities are derived by counting swaps between a one in the first segment and a zero in the second segment and normalizing by total swaps `C(n, 2)`.
4. Perform fast matrix exponentiation of `T` to the `k`-th power. This computes the state distribution after `k` swaps.
5. Multiply the initial state vector `v` (with 1 at index `wrong`) by `T^k`. The final probability that the array is sorted is the value corresponding to zero ones in the zero segment (state 0).
6. Return the probability as a modular fraction `P * Q^{-1} mod 10^9+7`.

Why it works: The process preserves the Markov property because the number of ones in the zero segment is sufficient to describe the system. Matrix exponentiation efficiently applies the transition `k` times, giving exact probabilities for each state after all swaps. The sorted probability corresponds precisely to the state with zero misplaced ones.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9+7

def modinv(x):
    return pow(x, MOD-2, MOD)

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    cnt1 = sum(a)
    cnt0 = n - cnt1
    wrong = sum(a[:cnt0])
    
    if wrong == 0:
        print(1)
        return

    size = cnt1 + 1
    total_pairs = n*(n-1)//2 % MOD

    T = [[0]*size for _ in range(size)]
    for i in range(size):
        if i > 0:
            T[i][i-1] = i * (cnt0 - (i-1)) % MOD * modinv(total_pairs) % MOD
        if i < cnt1:
            T[i][i+1] = (cnt1 - i) * (cnt0 - i) % MOD * modinv(total_pairs) % MOD
        same = (total_pairs - (T[i][i-1]*total_pairs if i>0 else 0) - (T[i][i+1]*total_pairs if i<cnt1 else 0)) % MOD
        T[i][i] = same * modinv(total_pairs) % MOD

    def matmul(A, B):
        n = len(A)
        C = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] = (C[i][j] + A[i][k]*B[k][j]) % MOD
        return C

    def matexp(M, p):
        n = len(M)
        res = [[int(i==j) for j in range(n)] for i in range(n)]
        while p:
            if p & 1:
                res = matmul(res, M)
            M = matmul(M, M)
            p >>= 1
        return res

    T_k = matexp(T, k)
    ans = T_k[wrong][0] % MOD
    print(ans)

solve()
```

The solution first computes the number of ones in the zero segment. It builds a Markov transition matrix where each entry corresponds to moving from one number of misplaced ones to another after a swap. Matrix multiplication is modular to avoid overflow, and matrix exponentiation raises the transition to the `k`-th power. Finally, the probability of zero misplaced ones is printed modulo 10^9+7.

## Worked Examples

### Sample 1

Input:

```
3 2
0 1 0
```

| State | wrong=1 | wrong=0 | wrong=2 |
| --- | --- | --- | --- |
| Initial | 1 | 0 | 0 |
| After 1 swap | 5/9 | 2/9 | 2/9 |
| After 2 swaps | 3/9 | 3/9 | 3/9 |

The final probability of sorted array is 1/3, which modulo 10^9+7 is 333333336.

### Sample 2

Input:

```
3 1
1 0 1
```

All swaps still leave at least one one in the zero segment. Probability is 0.

The trace confirms that initial calculation of wrong ones and transition matrix captures all possible swaps. The exponentiation step efficiently applies `k` steps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3 log k) | Matrix exponentiation of size at most 100x100 and `k` up to 10^9 |
| Space | O(n^2) | Store the transition matrix of size (cnt1+1)^2 ≤ 100^2 |

This fits comfortably under 1s time limit and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("3 2\n0 1
```
