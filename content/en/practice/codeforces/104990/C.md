---
title: "CF 104990C - Counting Relative Lists"
description: "We are asked to count sequences of length $N$, where each element is chosen from the integers $1$ to $M$, and every pair of adjacent elements must be coprime, meaning their greatest common divisor equals 1."
date: "2026-06-28T04:22:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104990
codeforces_index: "C"
codeforces_contest_name: "First Masters Championship LATAM 2024"
rating: 0
weight: 104990
solve_time_s: 61
verified: true
draft: false
---

[CF 104990C - Counting Relative Lists](https://codeforces.com/problemset/problem/104990/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count sequences of length $N$, where each element is chosen from the integers $1$ to $M$, and every pair of adjacent elements must be coprime, meaning their greatest common divisor equals 1. Every position in the sequence depends only on its immediate predecessor, so the structure is inherently local, but the sequence can be extremely long.

The key tension in the constraints comes from $N$ being as large as $10^8$, while $M$ is at most 100. This immediately rules out any approach that processes each position of the sequence explicitly. Any solution that iterates over the length of the sequence is impossible, since even $O(N)$ work is already too large. The only viable direction is to compress the problem so that the dependence on $N$ becomes logarithmic or otherwise eliminated, typically through matrix exponentiation or fast exponentiation on a transition system.

A subtle point is that the adjacency condition only depends on the values, not their positions. This means the entire problem can be seen as walks over a fixed graph of size $M$, where nodes are integers $1 \dots M$, and edges connect coprime pairs. A sequence is then a walk of length $N$ in this graph.

Edge cases worth isolating include $N = 1$, where any value from $1$ to $M$ is valid, and $M = 1$, where the only possible sequence is all ones. Another delicate case is when many numbers are not coprime, which can make the graph sparse but does not change the exponential growth nature of the counting problem.

## Approaches

A direct approach is to build all valid sequences recursively. We choose the first number freely, then for each position choose any number coprime with the previous one. This defines a branching process over a graph of size $M$. The correctness is immediate because it enforces the adjacency condition directly.

The failure point is the growth rate. Even if each node had only a few neighbors on average, the number of sequences grows exponentially with $N$. For $N = 10^8$, even a single path cannot be enumerated. So the issue is not correctness but inability to represent the repeated structure efficiently.

The key observation is that this is a Markov process over a fixed state space of size $M$. We only care about how many ways we can end at each value after $k$ steps. If we store a vector $dp[k][x]$ meaning the number of sequences of length $k$ ending at value $x$, then transitions depend only on coprimality. This becomes a linear transformation on a vector of size $M$, which can be encoded as a matrix multiplication.

Let $T[i][j] = 1$ if $\gcd(i, j) = 1$, otherwise $0$. Then:

$$dp_{k+1}[j] = \sum_{i=1}^M dp_k[i] \cdot T[i][j]$$

Thus, $dp_k$ evolves as repeated multiplication by a fixed $M \times M$ matrix. We need $T^N$ applied to an initial vector. Since $N$ is huge, we compute matrix exponentiation in $O(M^3 \log N)$. With $M \le 100$, this is feasible.

We must also be careful: $N$ counts the number of elements in the sequence, so transitions occur $N-1$ times.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(M^N)$ | $O(N)$ recursion | Too slow |
| Matrix Exponentiation | $O(M^3 \log N)$ | $O(M^2)$ | Accepted |

## Algorithm Walkthrough

1. Construct a set of states representing values from $1$ to $M$. Each state corresponds to the last element of a partial sequence.
2. Build a transition matrix $T$, where $T[i][j] = 1$ if $i$ and $j$ are coprime. This encodes whether we can move from value $i$ to value $j$ in one step.
3. Initialize a base vector $v$ where $v[i] = 1$, since any single-element sequence ending at $i$ is valid.
4. Interpret extending a sequence by one element as multiplying the current vector by $T$. This converts the counting problem into repeated linear transformations.
5. Compute $T^{N-1}$ using binary exponentiation on matrices. Each multiplication composes two transition systems into a longer one.
6. Multiply the resulting matrix by the base vector to obtain counts of sequences of length $N$ ending at each value.
7. Sum all entries of the resulting vector to get the total number of valid sequences.

### Why it works

The crucial invariant is that after processing $k$ steps, the vector entry for state $i$ equals the number of valid sequences of length $k+1$ ending in $i$. Every extension step preserves this invariant because every valid sequence of length $k+1$ is uniquely formed by appending a valid predecessor of length $k$, and the transition matrix exactly encodes all valid adjacencies. No sequence is double-counted or omitted because every transition is considered independently and the recurrence is exhaustive over all predecessors.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def mat_mul(a, b):
    n = len(a)
    m = len(b[0])
    p = len(b)
    res = [[0] * m for _ in range(n)]
    for i in range(n):
        ai = a[i]
        ri = res[i]
        for k in range(p):
            if ai[k]:
                aik = ai[k]
                bk = b[k]
                for j in range(m):
                    ri[j] = (ri[j] + aik * bk[j]) % MOD
    return res

def mat_pow(mat, exp):
    n = len(mat)
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
    N, M = map(int, input().split())

    if N == 1:
        print(M)
        return

    T = [[0] * M for _ in range(M)]
    for i in range(M):
        for j in range(M):
            if __import__("math").gcd(i + 1, j + 1) == 1:
                T[i][j] = 1

    P = mat_pow(T, N - 1)

    ans = 0
    for i in range(M):
        ans = (ans + sum(P[j][i] for j in range(M))) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution builds a full adjacency matrix over values $1 \dots M$, where edges represent valid transitions under the gcd constraint. The exponentiation raises this transition system to length $N-1$, because a sequence of length $N$ has $N-1$ transitions.

The multiplication order matters: matrices represent transitions from previous state (row) to next state (column). The final summation aggregates all possible ending states. The special case $N=1$ avoids exponentiation entirely since every single value is valid.

## Worked Examples

### Example 1: $N = 2, M = 3$

We build transitions among values 1 to 3.

| i | j | gcd(i,j) | T[i][j] |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 1 | 2 | 1 | 1 |
| 1 | 3 | 1 | 1 |
| 2 | 1 | 1 | 1 |
| 2 | 2 | 2 | 0 |
| 2 | 3 | 1 | 1 |
| 3 | 1 | 1 | 1 |
| 3 | 2 | 1 | 1 |
| 3 | 3 | 3 | 0 |

For $N=2$, we apply one transition. The number of valid pairs is simply the number of ones in this matrix, which is 7.

This confirms that the algorithm correctly reduces the problem to counting valid edges when the sequence length is minimal.

### Example 2: $N = 2, M = 10$

Here the structure is larger, but still a single-step transition problem. The matrix counts how many pairs in $1 \dots 10$ are coprime. The algorithm sums all valid directed edges in the coprimality graph, yielding 63.

This demonstrates that the method does not depend on enumerating sequences, only on structural properties of gcd relationships.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(M^3 \log N)$ | Matrix exponentiation over $M \times M$ transition matrix |
| Space | $O(M^2)$ | Storage of transition and temporary matrices |

With $M \le 100$, cubic operations are bounded around $10^6$ per multiplication, and $\log N \le 27$, which is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue()

# provided samples (expected outputs assumed)
# assert run("2 3\n") == "7\n"
# assert run("2 10\n") == "63\n"

# minimum size
assert run("1 1\n") == "1\n", "single element only one value"

# small uniform
assert run("1 5\n") == "5\n", "any single element allowed"

# adjacency heavy small case
assert run("2 2\n") == "3\n", "pairs among 1 and 2"

# chain length 3 small check
assert run("3 2\n") == "5\n", "valid short sequences"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | single state base case |
| 1 5 | 5 | no transitions needed |
| 2 2 | 3 | small transition graph correctness |
| 3 2 | 5 | multi-step propagation consistency |

## Edge Cases

For $N = 1$, every value from $1$ to $M$ forms a valid sequence of length one. The algorithm bypasses matrix exponentiation and directly outputs $M$, which matches the definition since no adjacency constraints apply without a second element.

For $M = 1$, the transition matrix is $1 \times 1$ with a single entry $T[1][1] = 1$. Every sequence consists entirely of ones, so there is exactly one valid sequence for any $N$. The exponentiation step preserves this identity matrix behavior, and the final sum yields 1 regardless of length.
