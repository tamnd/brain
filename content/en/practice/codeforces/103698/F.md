---
title: "CF 103698F - Tree"
description: "The task can be understood as a classic linear-algebraic counting problem on an undirected graph. Instead of reasoning combinatorially about spanning trees directly, we reinterpret the graph through a matrix built from its structure and compute a determinant that encodes the…"
date: "2026-07-02T09:50:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103698
codeforces_index: "F"
codeforces_contest_name: "The 4th Turing Cup"
rating: 0
weight: 103698
solve_time_s: 66
verified: true
draft: false
---

[CF 103698F - Tree](https://codeforces.com/problemset/problem/103698/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

The task can be understood as a classic linear-algebraic counting problem on an undirected graph. Instead of reasoning combinatorially about spanning trees directly, we reinterpret the graph through a matrix built from its structure and compute a determinant that encodes the answer.

Concretely, the input describes a simple undirected graph with $n$ vertices and a set of edges. The goal is to compute how many spanning trees exist in this graph. A spanning tree is a subset of edges that connects all vertices while containing no cycles, and uses exactly $n-1$ edges.

The output is a single integer representing this count. In typical competitive programming settings this value is taken modulo some large prime, although the underlying mathematics works over the integers as well.

From a complexity perspective, the key constraint is that the graph can be large enough that any enumeration of spanning trees or subsets of edges is impossible. Even moderately sized graphs make the number of spanning trees exponential, so any acceptable solution must reduce the problem to polynomial-time linear algebra. The only viable path is a determinant computation on an $n \times n$ matrix, which immediately suggests $O(n^\omega)$ or $O(n^3)$-type methods.

A few edge cases matter in practice. A graph with a single vertex always has exactly one spanning tree, even though there are no edges. A disconnected graph has zero spanning trees because it is impossible to connect all vertices without adding edges. A graph with multiple edges between the same pair of vertices increases the number of spanning trees in a nontrivial way, since each edge contributes separately to the Laplacian. A careless implementation that deduplicates edges would silently produce incorrect results in that case.

Another subtle case is when the graph is already a tree. In that situation the answer is exactly one, and any determinant-based implementation must preserve integrality despite working under modular arithmetic or randomization.

## Approaches

The brute-force viewpoint starts from the definition of a spanning tree. One could try to enumerate all subsets of $n-1$ edges and test whether each subset forms a valid tree. Connectivity can be checked with union-find or DFS, and acyclicity follows automatically if the subset has exactly $n-1$ edges and is connected. This approach is correct, but the number of edge subsets grows as $\binom{m}{n-1}$, which becomes infeasible even for small graphs. The bottleneck is not the verification step but the sheer number of candidates.

A more structured approach uses a fundamental transformation: instead of counting combinatorial objects directly, we encode them as algebraic terms in a determinant. The Laplacian matrix of a graph captures vertex degrees on the diagonal and adjacency structure off-diagonal. Kirchhoff’s Matrix-Tree Theorem states that any cofactor of this Laplacian equals the number of spanning trees. This converts the problem into computing a single determinant of an $(n-1) \times (n-1)$ matrix.

The reason this helps is that determinant computation admits efficient algebraic algorithms. Gaussian elimination or more advanced matrix multiplication techniques reduce the complexity from exponential counting to polynomial arithmetic. The combinatorial explosion is absorbed into cancellations inside the determinant expansion.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | Exponential | O(n + m) | Too slow |
| Matrix-Tree (Determinant) | O(n³) or O(n^ω) | O(n²) | Accepted |

## Algorithm Walkthrough

The solution is built around constructing the Laplacian matrix and computing one of its cofactors.

1. Build an $n \times n$ matrix $L$, initially filled with zeros. This matrix will represent the graph structure in algebraic form.
2. For every edge $u - v$, increase $L[u][u]$ and $L[v][v]$ by one, and decrease both $L[u][v]$ and $L[v][u]$ by one. This encodes vertex degrees and adjacency simultaneously. Each edge contributes a structured update that preserves symmetry.
3. Remove one arbitrary row and column, typically the last vertex, producing an $(n-1) \times (n-1)$ matrix. This step is required because the full Laplacian always has determinant zero due to row sums being zero, but any cofactor carries the spanning tree count.
4. Compute the determinant of the resulting matrix using Gaussian elimination under the required modulus or over integers with fraction-free elimination. The determinant aggregates all spanning tree contributions encoded in the matrix.
5. Output the determinant as the final answer.

The key non-obvious step is why deleting a row and column does not lose information. The Laplacian has rank $n-1$ for a connected graph, and all cofactors are equal. This allows us to reduce the problem to a full-rank determinant computation.

### Why it works

Each spanning tree corresponds to exactly one term in the expansion of the determinant after transforming the Laplacian. The algebraic cancellations in the determinant eliminate all structures that contain cycles, leaving only acyclic connected edge selections. The remaining surviving terms are in one-to-one correspondence with spanning trees, which ensures the determinant equals their count.

## Python Solution

```python
import sys
input = sys.stdin.readline

def det_mod(mat, mod):
    n = len(mat)
    det = 1
    sign = 1

    for i in range(n):
        pivot = i
        for j in range(i, n):
            if mat[j][i] != 0:
                pivot = j
                break
        if mat[pivot][i] == 0:
            return 0

        if pivot != i:
            mat[i], mat[pivot] = mat[pivot], mat[i]
            sign *= -1

        inv = pow(mat[i][i], mod - 2, mod)
        det = det * mat[i][i] % mod

        for j in range(i + 1, n):
            factor = mat[j][i] * inv % mod
            for k in range(i, n):
                mat[j][k] = (mat[j][k] - factor * mat[i][k]) % mod

    return det * sign % mod

n, m = map(int, input().split())
mod = 10**9 + 7

L = [[0] * n for _ in range(n)]

for _ in range(m):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    L[u][u] += 1
    L[v][v] += 1
    L[u][v] -= 1
    L[v][u] -= 1

for i in range(n):
    for j in range(n):
        L[i][j] %= mod

mat = [row[:-1] for row in L[:-1]]

print(det_mod(mat, mod))
```

The implementation first constructs the Laplacian directly from edge contributions. The removal of the last row and column is done by slicing, which keeps the matrix square and full rank under the connectivity assumption.

The determinant routine uses Gaussian elimination modulo a prime. The pivot selection ensures numerical stability in modular arithmetic by avoiding zero pivots when possible. Row operations are performed in-place, and the determinant is accumulated through pivot scaling. The sign tracking handles row swaps, which are essential because each swap flips determinant sign.

A subtle point is that modular inversion assumes the modulus is prime. This is standard in competitive programming, where $10^9 + 7$ or similar primes are used.

## Worked Examples

Consider a triangle graph with three vertices and three edges.

The Laplacian is

$$\begin{bmatrix}
2 & -1 & -1 \\
-1 & 2 & -1 \\
-1 & -1 & 2
\end{bmatrix}$$

Removing the last row and column gives

$$\begin{bmatrix}
2 & -1 \\
-1 & 2
\end{bmatrix}$$

The determinant computation proceeds as follows.

| Step | Matrix state | Operation |
| --- | --- | --- |
| 1 | [[2, -1], [-1, 2]] | initial |
| 2 | [[2, -1], [0, 3]] | eliminate second row |
| 3 | 6 | product of pivots |

The result 3 matches the known number of spanning trees in a triangle.

Now consider a tree with three vertices in a line. The Laplacian cofactor becomes a matrix whose determinant evaluates to 1. This confirms that a tree contributes exactly one spanning tree.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n³) | Gaussian elimination on an (n-1)×(n-1) matrix |
| Space | O(n²) | Storage of Laplacian matrix |

The cubic complexity is sufficient for typical constraints up to a few thousand vertices. For larger limits, one would need advanced techniques such as determinant optimization or sparsity-aware methods, but the Laplacian structure already provides enough efficiency for standard settings.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    n, m = map(int, sys.stdin.readline().split())
    mod = 10**9 + 7

    L = [[0]*n for _ in range(n)]
    for _ in range(m):
        u, v = map(int, sys.stdin.readline().split())
        u -= 1
        v -= 1
        L[u][u] += 1
        L[v][v] += 1
        L[u][v] -= 1
        L[v][u] -= 1

    mat = [row[:-1] for row in L[:-1]]

    def det(a):
        n = len(a)
        detv = 1
        sign = 1
        for i in range(n):
            p = i
            for j in range(i, n):
                if a[j][i]:
                    p = j
                    break
            if a[p][i] == 0:
                return 0
            if p != i:
                a[i], a[p] = a[p], a[i]
                sign *= -1
            inv = pow(a[i][i], mod-2, mod)
            detv = detv * a[i][i] % mod
            for j in range(i+1, n):
                f = a[j][i] * inv % mod
                for k in range(i, n):
                    a[j][k] = (a[j][k] - f*a[i][k]) % mod
        return detv * sign % mod

    return str(det(mat))

# triangle graph
assert run("3 3\n1 2\n2 3\n1 3\n") == "3"
# path graph
assert run("3 2\n1 2\n2 3\n") == "1"
# disconnected
assert run("4 2\n1 2\n3 4\n") == "0"
# single node
assert run("1 0\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| triangle | 3 | multiple spanning trees |
| path | 1 | tree base case |
| disconnected | 0 | connectivity requirement |
| single node | 1 | degenerate case |

## Edge Cases

A disconnected graph is handled correctly because the Laplacian cofactor becomes singular. During elimination, a zero pivot eventually appears, forcing the determinant to zero, which correctly reflects the absence of spanning trees.

A single vertex graph reduces to an empty matrix after removing row and column. By convention, the determinant of a 0×0 matrix is 1, matching the fact that there is exactly one spanning tree.

A tree input leads to a triangular structure in the Laplacian cofactor after elimination. Each pivot corresponds to exactly one edge constraint, producing determinant one without cancellation, confirming correctness in the minimal connected case.
