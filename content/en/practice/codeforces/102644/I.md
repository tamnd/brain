---
title: "CF 102644I - Count Paths Queries"
description: "The problem describes a directed graph with up to 200 vertices. A path is a sequence of exactly k directed edges, and vertices or edges may appear more than once."
date: "2026-08-01T10:19:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102644
codeforces_index: "I"
codeforces_contest_name: "Matrix Exponentiation"
rating: 0
weight: 102644
solve_time_s: 64
verified: true
draft: false
---

[CF 102644I - Count Paths Queries](https://codeforces.com/problemset/problem/102644/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a directed graph with up to 200 vertices. A path is a sequence of exactly `k` directed edges, and vertices or edges may appear more than once. For every query, we are asked how many different walks start at vertex `s`, finish at vertex `t`, and contain exactly `k` edges. The answer must be printed modulo `1,000,000,007`.

The input graph can contain up to 200 vertices and 200 queries, while the required path length can be as large as `10^9`. A direct simulation of paths is impossible because the number of possible walks grows exponentially with `k`. Even a dynamic programming approach that processes every step is too slow because `k` is not bounded by a small value. The small number of vertices is the key constraint: it allows us to perform operations on `200 x 200` matrices.

A careless solution can fail on several cases. If `k` is large, iterating one edge at a time will never finish. For example, with a single edge `1 -> 1` and query `(1, 1, 1000000000)`, the answer is `1`, but a step-by-step simulation would require one billion transitions.

Another common mistake is forgetting that paths can revisit vertices. For input:

```
2 2 3
1 2
2 1
1 1 3
```

the correct output is:

```
0
```

The only possible walks alternate between the two vertices, so after three edges we end at vertex `2`, not vertex `1`. Treating the graph as a simple path problem would produce an incorrect result.

A third edge case is an empty graph. For example:

```
3 0 2
1 2 5
3 3 1
```

The output is:

```
0
0
```

because no edge exists, so no positive-length walk can be created.

## Approaches

The brute-force idea is to follow every possible walk from the starting vertex. For each query, we could run a depth-first search that chooses the next edge `k` times and count how many times we reach the destination. This is correct because it enumerates exactly all valid walks. However, the number of walks can grow as large as `n^k`, so even a graph with only 200 vertices becomes impossible when `k` reaches `10^9`.

A better first observation is that we only care about transitions between vertices. Let `A[i][j]` represent whether there is an edge from `i` to `j`, or more precisely, the number of one-edge paths from `i` to `j`. Matrix multiplication naturally combines transitions. The entry `(i, j)` of `A^2` tells us how many two-edge paths go from `i` to `j`, because every possible middle vertex is considered. The same idea extends to any length, so the answer is the `(s, t)` element of `A^k`.

The remaining issue is that `k` can be huge. Binary exponentiation solves this exactly like ordinary exponentiation. We precompute powers `A^(1), A^(2), A^(4), A^(8)`, and so on. Each bit of `k` tells us which powers should be multiplied together.

Because there are only 200 queries, it is better to compute the powers once and reuse them. Each query then only needs at most 30 matrix-vector style transitions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^k) | O(k) | Too slow |
| Matrix Exponentiation | O(n^3 log k + qn^2 log k) | O(n^2 log k) | Accepted |

## Algorithm Walkthrough

1. Build the adjacency matrix `A`. The value `A[i][j]` stores the number of direct edges from vertex `i` to vertex `j`. Since there are no multiple edges, every entry is either `0` or `1`.
2. Precompute powers of the matrix. Store `A`, `A^2`, `A^4`, `A^8`, and continue until the largest possible bit of `k` is covered. Each next matrix is obtained by multiplying the previous matrix by itself.
3. For a query `(s, t, k)`, start with the identity matrix as the current result and scan the bits of `k`.
4. Whenever a bit of `k` is set, multiply the current result by the corresponding precomputed power.
5. Return the value at row `s`, column `t` of the final matrix.

The reason binary exponentiation works is that every positive integer can be represented as a sum of powers of two. Matrix multiplication preserves the meaning of path composition, so multiplying the selected powers combines exactly the required number of edges.

Why it works: after processing some bits of `k`, the maintained matrix represents the number of paths using the processed portion of the exponent. When a set bit is encountered, multiplying by `A^(2^i)` appends exactly that many edges to every possible partial path. The invariant remains true until all bits are processed, at which point the matrix equals `A^k`.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def multiply(a, b):
    n = len(a)
    bt = [[b[j][i] for j in range(n)] for i in range(n)]
    res = [[0] * n for _ in range(n)]

    for i in range(n):
        ai = a[i]
        ri = res[i]
        for j in range(n):
            s = 0
            bj = bt[j]
            for k in range(n):
                s += ai[k] * bj[k]
            ri[j] = s % MOD
    return res

def solve():
    n, m, q = map(int, input().split())

    mat = [[0] * n for _ in range(n)]
    for _ in range(m):
        a, b = map(int, input().split())
        mat[a - 1][b - 1] = 1

    powers = [mat]
    for _ in range(31):
        powers.append(multiply(powers[-1], powers[-1]))

    ans = []
    for _ in range(q):
        s, t, k = map(int, input().split())
        s -= 1
        t -= 1

        vec = [0] * n
        vec[s] = 1

        bit = 0
        while k:
            if k & 1:
                new_vec = [0] * n
                p = powers[bit]
                for i in range(n):
                    if vec[i]:
                        vi = vec[i]
                        row = p[i]
                        for j in range(n):
                            new_vec[j] = (new_vec[j] + vi * row[j]) % MOD
                vec = new_vec
            k >>= 1
            bit += 1

        ans.append(str(vec[t]))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The matrix multiplication routine uses a transposed copy of the second matrix so that each inner loop accesses contiguous rows. This avoids repeatedly indexing columns and makes the cubic multiplication faster in Python.

The query phase does not multiply two full matrices. Instead, it multiplies a starting vector by the required matrices. The starting vector has a single `1` at the source vertex, representing one empty path before taking any edges. After all bits are processed, the destination position contains the number of walks of length `k`.

The exponent loop handles values up to `10^9`, so 30 to 31 iterations are enough. The modulo operation is applied during every accumulation to keep values within Python integer limits and match the required output.

## Worked Examples

For the sample:

```
3 4 4
1 2
2 3
3 1
2 1
1 2 6
3 3 5
1 3 1
3 2 54
```

the first query can be traced as follows.

| Step | Current exponent bit | Vector state |
| --- | --- | --- |
| Start | none | `[1,0,0]` |
| Use `A^2` | bit set | counts paths of length 2 |
| Use `A^4` | bit set | counts paths of length 6 |

After combining the selected powers, the value for vertex `2` is `2`, which matches the two valid walks of length six.

For the query `(1,3,1)`, only the first power is used.

| Step | Current exponent bit | Vector state |
| --- | --- | --- |
| Start | none | `[1,0,0]` |
| Use `A` | bit set | `[0,1,0]` |

Vertex `3` has value `0`, because there is no direct edge from `1` to `3`.

These examples show that the algorithm counts walks by length, not simple paths, and that the exponentiation process correctly handles both small and large lengths.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3 log K + qn^2 log K) | Matrix powers require cubic multiplication, while each query uses vector multiplication |
| Space | O(n^2 log K) | Stores the precomputed powers |

With `n <= 200`, the cubic preprocessing is feasible. The large value of `k` is reduced to only about 30 binary steps, so the algorithm fits the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old
    return out

assert run("""3 4 4
1 2
2 3
3 1
2 1
1 2 6
3 3 5
1 3 1
3 2 54
""") == """2
1
0
922111
"""

assert run("""1 0 1
1 1 1
""") == "0\n"

assert run("""2 2 2
1 2
2 1
1 1 2
1 2 3
""") == """1
1
"""

assert run("""3 3 2
1 2
2 3
3 1
1 1 1000000000
2 1 1
""") == """1
0
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex with no edges | `0` | Empty graph handling |
| Two-cycle graph | Alternating counts | Revisiting vertices |
| Three-cycle with huge `k` | Correct modular exponentiation | Large exponent handling |

## Edge Cases

For a graph with no edges, the adjacency matrix is entirely zero. Every matrix power remains zero, so every query asking for a positive number of steps correctly returns zero.

For a cycle such as:

```
2 2 1
1 2
2 1
1 1 1000000000
```

the powers of the adjacency matrix correctly preserve the alternating movement. Because the exponent is processed by bits instead of individual steps, the solution reaches the answer without simulating the billion transitions.

For repeated visits, the matrix multiplication interpretation naturally includes paths that return to already visited vertices. No special handling is needed because matrix powers count walks rather than simple paths.
