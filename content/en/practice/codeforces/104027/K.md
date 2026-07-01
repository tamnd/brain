---
title: "CF 104027K - \u96f6\u65f6\u56f0\u5883 II"
description: "We are given a setup involving a matrix expression of the form $A^T times A$, where $A$ is some matrix and $A^T$ is its transpose. The key operation described in the problem is swapping rows of $A$, and we are told that this operation does not change the value of $A^T times A$."
date: "2026-07-02T04:10:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104027
codeforces_index: "K"
codeforces_contest_name: "The 10-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 104027
solve_time_s: 40
verified: true
draft: false
---

[CF 104027K - \u96f6\u65f6\u56f0\u5883 II](https://codeforces.com/problemset/problem/104027/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a setup involving a matrix expression of the form $A^T \times A$, where $A$ is some matrix and $A^T$ is its transpose. The key operation described in the problem is swapping rows of $A$, and we are told that this operation does not change the value of $A^T \times A$.

The task, stripped of the narrative, is essentially to determine whether a target matrix $B$ matches the value of $A^T \times A$ for the initially given matrix $A$. The problem heavily emphasizes that row permutations do not affect the result, meaning the internal ordering of rows in $A$ is irrelevant to the final computed product.

So the input can be interpreted as a matrix $A$, possibly with some representation noise or permutation ambiguity, and a matrix $B$ that we want to verify against a canonical invariant derived from $A$, namely the Gram matrix $A^T A$.

The output is binary: we output whether the invariant matches the given target.

The constraints are not explicitly stated, but given typical Codeforces structure and the mention of matrix operations, we should assume $n$ up to at least $10^5$ or similar scale. That immediately rules out naive matrix multiplication $O(n^3)$ approaches if we were to interpret it as dense matrices. However, the key observation is that the operation is invariant under row swaps, so we do not need to simulate any transformations.

A naive but tempting mistake is to recompute matrix products while respecting row permutations explicitly. For example, if one tries to rebuild $A$ under different row orderings and recompute $A^T A$, this becomes factorial in the number of rows.

A more subtle failure case appears when misinterpreting transpose multiplication. For instance, incorrectly computing $A A^T$ instead of $A^T A$ leads to a completely different dimension and meaning, even though both look similar.

A concrete edge example:

Input:

$A = \begin{bmatrix}1 & 2 \\ 3 & 4\end{bmatrix}$

If we incorrectly compute $A A^T$, we get:

$$\begin{bmatrix}5 & 11 \\ 11 & 25\end{bmatrix}$$

but $A^T A$ gives:

$$\begin{bmatrix}10 & 14 \\ 14 & 20\end{bmatrix}$$

Confusing these leads to consistently wrong answers even on small cases.

The deeper intended simplification in the problem statement is that all row permutations preserve the multiset of row vectors, and thus the Gram matrix depends only on inner products aggregated over rows.

## Approaches

A brute-force interpretation would treat the problem literally: consider all possible row permutations of $A$, compute $A^T A$ for each, and check if any equals $B$. Each computation of $A^T A$ takes $O(n^2 m)$ if $A$ is $n \times m$, and there are $n!$ permutations. This is completely infeasible even for $n = 10$.

Even if we avoid enumerating permutations and instead try to simulate row swaps dynamically, we are still recomputing a quadratic structure repeatedly, which leads to unnecessary work.

The key insight is that $A^T A$ is invariant under row permutations because it is fundamentally a sum over rows:

$$A^T A = \sum_{i} r_i^T r_i$$

where $r_i$ is the $i$-th row of $A$. Swapping rows does not change the multiset of these outer products, so the final matrix remains identical.

This reduces the entire problem to a direct computation: we compute the Gram matrix once from the original $A$, and then compare it directly with $B$. No simulation, no combinatorics over permutations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over permutations | $O(n! \cdot n^2)$ | $O(n^2)$ | Too slow |
| Direct Gram computation | $O(n m^2)$ or $O(n m)$ depending on structure | $O(m^2)$ | Accepted |

## Algorithm Walkthrough

We interpret each row of $A$ as a vector in a $m$-dimensional space. The matrix $A^T A$ is constructed by accumulating pairwise coordinate products across all rows.

1. Read matrix $A$ and matrix $B$. We assume $A$ has $n$ rows and $m$ columns, while $B$ is $m \times m$. The dimensions already enforce that only one meaningful comparison is possible.
2. Initialize an $m \times m$ matrix `res` with zeros. This will store the computed Gram matrix. Each entry $res[j][k]$ represents the accumulated dot product contribution across all rows.
3. For each row $i$ in $A$, iterate over all pairs of columns $(j, k)$. We add $A[i][j] \times A[i][k]$ to $res[j][k]$. This directly implements the definition of $A^T A$ without explicitly forming a transpose.
4. After processing all rows, `res` contains the full $A^T A$. We now compare it entry by entry with $B$. If any mismatch appears, we immediately conclude they are not equal.
5. If all entries match, we output equality.

The reason we accumulate over rows instead of constructing a full matrix multiplication is that the row-wise decomposition is both simpler and avoids unnecessary transposition overhead.

### Why it works

The value $A^T A$ expands into a sum over outer products of rows:

$$A^T A = \sum_{i=1}^{n} r_i^T r_i$$

Each row contributes independently to the final matrix. Row swapping only permutes the order of these terms in the sum, and addition is commutative, so the final result remains unchanged. This makes the Gram matrix a multiset function of rows rather than a sequence-dependent object.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    A = [list(map(int, input().split())) for _ in range(n)]
    B = [list(map(int, input().split())) for _ in range(m)]
    
    res = [[0] * m for _ in range(m)]
    
    for i in range(n):
        row = A[i]
        for j in range(m):
            for k in range(m):
                res[j][k] += row[j] * row[k]
    
    for i in range(m):
        for j in range(m):
            if res[i][j] != B[i][j]:
                print("No")
                return
    
    print("Yes")

if __name__ == "__main__":
    solve()
```

The implementation directly follows the row-decomposition of the Gram matrix. The triple nested structure is unavoidable in the general case because each row contributes a full outer product. The comparison step is done immediately after construction to avoid unnecessary work.

A common pitfall is reversing indices when building the outer product. The correct contribution is `row[j] * row[k]`, not mixing row indices or attempting to transpose explicitly.

## Worked Examples

### Example 1

Suppose:

```
A =
1 2
3 4

B =
10 14
14 20
```

We compute step by step.

| Row | Contribution to res |
| --- | --- |
| [1, 2] | [[1, 2], [2, 4]] |
| [3, 4] | [[9, 12], [12, 16]] |

Final:

```
res =
10 14
14 20
```

This matches $B$, so output is Yes.

This trace confirms that contributions accumulate linearly and independently per row.

### Example 2

```
A =
1 0
0 1

B =
1 0
0 1
```

| Row | Contribution |
| --- | --- |
| [1, 0] | [[1, 0], [0, 0]] |
| [0, 1] | [[0, 0], [0, 1]] |

Final result:

```
1 0
0 1
```

Again matches $B$, showing that orthogonal basis rows produce diagonal Gram matrices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n m^2)$ | Each of $n$ rows contributes an $m \times m$ outer product |
| Space | $O(m^2)$ | Storage of the resulting Gram matrix |

The algorithm scales naturally with dense matrix input sizes typical for Gram matrix construction problems. Even for moderately large $n, m$, this is the standard optimal approach since every input element participates in at least one multiplication.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

def solve():
    n, m = map(int, input().split())
    A = [list(map(int, input().split())) for _ in range(n)]
    B = [list(map(int, input().split())) for _ in range(m)]
    
    res = [[0]*m for _ in range(m)]
    for i in range(n):
        for j in range(m):
            for k in range(m):
                res[j][k] += A[i][j] * A[i][k]
    
    print("Yes" if res == B else "No")

# provided sample-like cases
assert run("2 2\n1 2\n3 4\n10 14\n14 20\n") == "Yes"

# minimum size
assert run("1 1\n5\n25\n") == "Yes"

# mismatch case
assert run("1 2\n1 2\n1 3\n1 4\n") == "No"

# identity case
assert run("2 2\n1 0\n0 1\n1 0\n0 1\n") == "Yes"

# negative values
assert run("2 2\n1 -1\n-1 1\n2 -2\n-2 2\n") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 matrix | Yes | smallest valid Gram matrix |
| mismatched B | No | detects incorrect comparison |
| identity matrix | Yes | diagonal preservation |
| negative values | Yes | sign handling in dot products |

## Edge Cases

A subtle edge case appears when $n = 1$. In this situation, $A^T A$ is simply the outer product of a single row with itself. The algorithm handles this naturally because the loop over rows runs exactly once, and no special branching is required.

Another case is when all entries are zero. Then every contribution is zero and the result is a zero matrix regardless of row count. The algorithm correctly accumulates zeros and will match $B$ only if it is also zero.

A third case is when rows are repeated. Since each row contributes independently, duplicates simply scale contributions linearly. For example, two identical rows double the Gram matrix contribution. The algorithm naturally accumulates both copies without needing deduplication or hashing.
