---
title: "CF 222E - Decoding Genome"
description: "We are asked to count the number of valid sequences of nucleotides of length n for a Martian DNA strand, given a total of m nucleotides and a list of forbidden consecutive pairs. Each nucleotide is represented by a letter from 'a' to 'z' and 'A' to 'Z' depending on its index."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "matrices"]
categories: ["algorithms"]
codeforces_contest: 222
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 137 (Div. 2)"
rating: 1900
weight: 222
solve_time_s: 190
verified: true
draft: false
---

[CF 222E - Decoding Genome](https://codeforces.com/problemset/problem/222/E)

**Rating:** 1900  
**Tags:** dp, matrices  
**Solve time:** 3m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count the number of valid sequences of nucleotides of length _n_ for a Martian DNA strand, given a total of _m_ nucleotides and a list of forbidden consecutive pairs. Each nucleotide is represented by a letter from 'a' to 'z' and 'A' to 'Z' depending on its index. A forbidden pair means that the first nucleotide in the pair cannot be immediately followed by the second nucleotide in a valid DNA sequence. The goal is to compute the number of sequences of length _n_ modulo 10^9+7.

The constraints are instructive. _n_ can be as large as 10^15, which rules out any solution that iterates over the sequence length explicitly. _m_ is at most 52, which is small enough to allow matrix-based dynamic programming or state compression techniques. The number of forbidden pairs _k_ can be up to _m_², which means in the worst case we may need to track almost every nucleotide transition.

A naive approach that tries to generate every sequence and check validity fails immediately because the number of sequences grows exponentially with _n_. Edge cases arise when all pairs are forbidden, or when only a single nucleotide is allowed repeatedly. For example, with _n=3, m=2_, and the forbidden pairs being all possible transitions except 'aa', the only valid sequence is 'aaa'. A careless approach that assumes each nucleotide can follow any other will overcount and give an incorrect answer.

## Approaches

A brute-force solution would enumerate all sequences of length _n_, checking each against the forbidden list. This is correct in principle because it explicitly validates each candidate, but it performs O(m^n) operations, which is entirely impractical for n up to 10^15.

The key insight is that the problem is equivalent to counting walks of length _n-1_ in a directed graph where vertices represent nucleotides and edges represent allowed transitions. If we define a transition matrix _T_ where T[i][j] is 1 if nucleotide i can be followed by nucleotide j and 0 otherwise, then the total number of sequences is the sum of all entries in the matrix _T^(n-1)_ multiplied by the number of possible first nucleotides. Matrix exponentiation allows us to compute _T^(n-1)_ in O(m^3 log n) operations. Since m ≤ 52, this is fast enough even when n is extremely large.

The brute-force works because it enumerates all sequences, but fails when n is large. The observation that sequence counting with pairwise constraints can be represented as a matrix of allowed transitions lets us reduce the problem to matrix exponentiation. This transforms an exponential problem into one manageable by repeated squaring.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m^n) | O(n) | Too slow |
| Matrix Exponentiation | O(m^3 log n) | O(m^2) | Accepted |

## Algorithm Walkthrough

1. Map each nucleotide character to a number from 0 to m-1. This simplifies indexing in the transition matrix.
2. Initialize an m × m matrix T where each entry is 1, indicating that every nucleotide can follow every other nucleotide initially.
3. Iterate over the list of forbidden pairs. For each pair, set the corresponding entry in T to 0. This ensures the matrix encodes exactly the allowed transitions.
4. Implement matrix multiplication and modular arithmetic functions to handle multiplications modulo 10^9+7. This keeps numbers in the correct range and avoids overflow.
5. Compute T^(n-1) using fast exponentiation by squaring. For each power, multiply matrices and reduce modulo 10^9+7.
6. Sum all entries in T^(n-1). Each entry represents the number of sequences of length n starting from a nucleotide i and ending at nucleotide j. Since the first nucleotide can be any of the m nucleotides, the total number of sequences is simply the sum of all entries.
7. Output the result modulo 10^9+7.

Why it works: At each step of exponentiation, the matrix multiplication exactly counts the number of sequences of a given length ending in each nucleotide. By inductively applying the power, we correctly compute the number of sequences of length n respecting all forbidden transitions. The modulo operation does not interfere with correctness because all arithmetic is modular.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def char_to_index(c):
    if 'a' <= c <= 'z':
        return ord(c) - ord('a')
    return ord(c) - ord('A') + 26

def mat_mult(A, B):
    m = len(A)
    C = [[0]*m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            for k in range(m):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD
    return C

def mat_pow(mat, power):
    m = len(mat)
    result = [[1 if i==j else 0 for j in range(m)] for i in range(m)]
    while power:
        if power % 2 == 1:
            result = mat_mult(result, mat)
        mat = mat_mult(mat, mat)
        power //= 2
    return result

def solve():
    n, m, k = map(int, input().split())
    T = [[1]*m for _ in range(m)]
    for _ in range(k):
        pair = input().strip()
        i = char_to_index(pair[0])
        j = char_to_index(pair[1])
        T[i][j] = 0

    if n == 1:
        print(m % MOD)
        return

    Tn = mat_pow(T, n-1)
    total = 0
    for i in range(m):
        for j in range(m):
            total = (total + Tn[i][j]) % MOD
    print(total)

solve()
```

The solution first converts characters to indices to simplify matrix access. It initializes the transition matrix with ones and zeroes out forbidden pairs. Matrix exponentiation uses squaring to handle extremely large n efficiently. Finally, we sum all entries to count sequences, which corresponds exactly to the sum over all possible starting and ending nucleotides.

## Worked Examples

For input

```
3 3 2
ab
ba
```

The nucleotide indices are: a=0, b=1, c=2. The transition matrix T is initially all ones, then T[0][1] and T[1][0] are set to 0:

|  | a | b | c |
| --- | --- | --- | --- |
| a | 1 | 0 | 1 |
| b | 0 | 1 | 1 |
| c | 1 | 1 | 1 |

Raising T to the power of n-1=2 and summing entries gives 17, matching the sample output. This confirms that forbidden pairs are correctly applied and matrix exponentiation correctly counts sequences.

For input

```
2 1 1
aa
```

We have a single nucleotide 'a'. T is [[0]]. T^(2-1) is [[0]], sum is 0, which correctly reflects that no sequence of length 2 is allowed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m^3 log n) | Matrix multiplication takes O(m^3), exponentiation applies log n squarings |
| Space | O(m^2) | Storing the transition matrix and intermediate results |

With m ≤ 52, m^3 is ~140k operations per multiplication. log n ≤ 50 for n up to 10^15, so total operations are feasible within 2 seconds. Space of O(m^2) is negligible compared to memory limit.

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
assert run("3 3 2\nab\nba\n") == "17", "sample 1"
assert run("2 1 1\naa\n") == "0", "sample 2"

# custom cases
assert run("1 5 0\n") == "5", "single length sequences"
assert run("3 2 0\n") == "8", "no forbidden pairs"
assert run("4 2 4\nab\nba\naa\nbb\n") == "0", "all pairs forbidden"
assert run("2 3 1\nac\n") == "8", "single forbidden pair"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 0 | 5 | single nucleotide sequences |
| 3 2 0 | 8 | sequences without forbidden pairs |
| 4 2 4 | 0 | no valid sequences possible |
| 2 3 1 | 8 | one forbidden pair correctly applied |

## Edge Cases

For n=1, the code correctly handles the case separately, returning m. For n=2 and all pairs forbidden, the matrix exponentiation produces zeros, resulting in output 0. For maximum n=10^15 and m=52, the matrix exponentiation remains efficient due to log
