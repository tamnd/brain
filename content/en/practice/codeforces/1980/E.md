---
title: "CF 1980E - Permutation of Rows and Columns"
description: "We are given two rectangular grids of numbers, both of size $n times m$, and together they contain exactly the numbers from $1$ to $n cdot m$, each appearing once. So each matrix is just a rearrangement of the same set of tiles."
date: "2026-06-08T16:53:12+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "greedy", "hashing", "implementation", "math", "matrices", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1980
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 950 (Div. 3)"
rating: 1600
weight: 1980
solve_time_s: 80
verified: true
draft: false
---

[CF 1980E - Permutation of Rows and Columns](https://codeforces.com/problemset/problem/1980/E)

**Rating:** 1600  
**Tags:** constructive algorithms, data structures, greedy, hashing, implementation, math, matrices, sortings  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two rectangular grids of numbers, both of size $n \times m$, and together they contain exactly the numbers from $1$ to $n \cdot m$, each appearing once. So each matrix is just a rearrangement of the same set of tiles.

The only allowed moves are swapping entire rows or swapping entire columns. We can do this any number of times. The task is to determine whether we can transform the first grid into the second using only these row and column swaps.

The key constraint is that row swaps do not change the order inside a row, they only reorder rows, and column swaps do not change the order inside a column, they only reorder columns. So the structure of the grid is preserved up to independent permutations of row indices and column indices.

The input size is large: across all test cases, the total number of cells is at most $2 \cdot 10^5$. This strongly suggests an $O(nm)$ per test case or linear overall solution. Anything involving repeated sorting per test or simulation of operations is fine only if it is linear in total input size.

A naive misunderstanding would be to think we need to simulate swaps or try to “align” rows and columns greedily. That would fail in cases like:

Example:

$$a =
\begin{pmatrix}
1 & 2 \\
3 & 4
\end{pmatrix}, \quad
b =
\begin{pmatrix}
4 & 3 \\
2 & 1
\end{pmatrix}$$

A naive row-matching approach might conclude mismatch because no row matches directly, but swapping both rows and columns makes the transformation possible.

Another subtle failure case is assuming row multisets must match row-by-row. That is wrong because rows themselves are permuted arbitrarily.

The real difficulty is that both row and column permutations interact globally rather than locally.

## Approaches

The brute-force viewpoint is to think of applying row and column swaps as generating all permutations of rows and columns. That means any transformation corresponds to choosing a permutation of rows and a permutation of columns. In principle, we could try all row permutations and column permutations and check if the resulting matrix matches. That would involve $n!\cdot m!$ possibilities, which is completely infeasible even for $n=5$.

The key insight is that row and column swaps act independently on indices. If we assign each value its position in both matrices, we can think in terms of coordinates. Every number $x$ in matrix $a$ has coordinates $(r_a[x], c_a[x])$, and in matrix $b$, coordinates $(r_b[x], c_b[x])$.

If a valid transformation exists, then there must exist a permutation of rows and a permutation of columns such that for every value $x$, its row index maps consistently and its column index maps consistently. In other words, the transformation induces two bijections:

one on row indices and one on column indices, and they must simultaneously explain all placements.

This reduces the problem to checking consistency of these induced mappings. A clean way to enforce this is to anchor row relationships using positions of values: values appearing in the same row in $a$ must map to values appearing in the same row in $b$, after reindexing rows consistently. The same applies to columns.

A simpler and standard reformulation is to treat each value as a pair $(row, col)$, then observe that the relative ordering of rows between any two values must be preserved between $a$ and $b$, and similarly for columns. This induces a constraint graph where inconsistencies immediately reveal impossibility.

A more implementation-friendly characterization is to normalize both matrices by replacing values with their positions and checking whether the induced row-ordering and column-ordering of all values is identical up to permutation. Sorting values by their positions in one matrix and verifying consistency in the other leads to a linear or near-linear check using hashing or signature comparisons per row and column.

The most practical solution uses positional encoding: for each value, record its row and column in both matrices, then verify that the relative ordering of rows and columns among all values is identical in both representations. This can be reduced to checking that the mapping from rows in $a$ to rows in $b$ is consistent, and similarly for columns.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force permutations of rows/cols | $O(n! \cdot m!)$ | $O(nm)$ | Too slow |
| Positional consistency mapping | $O(nm)$ | $O(nm)$ | Accepted |

## Algorithm Walkthrough

We build a direct mapping between positions of values in both matrices and verify that row and column permutations implied by these mappings are consistent.

1. Read both matrices and store, for every value $x$, its coordinates in $a$: $(r_a[x], c_a[x])$ and in $b$: $(r_b[x], c_b[x])$.

This step converts the grid problem into a point-matching problem over permutations.
2. For each value $x$, we interpret the transformation as mapping row $r_a[x]$ to $r_b[x]$, and column $c_a[x]$ to $c_b[x]$.

If a valid global row permutation exists, then all values sharing a row in $a$ must map consistently to the same row structure in $b$.
3. We enforce consistency of row mapping by selecting one representative value per row in $a$, and ensuring all values in that row map to the same row permutation in $b$.

If any row in $a$ tries to map to multiple rows in $b$, transformation is impossible.
4. Repeat the same logic for columns, ensuring each column in $a$ consistently maps to a single column in $b$.
5. After establishing mappings, we verify injectivity: no two distinct rows in $a$ map to the same row in $b$, and similarly for columns.

This ensures the mapping is a true permutation rather than a collapse.
6. If both row and column mappings are valid permutations, output YES; otherwise output NO.

### Why it works

Row swaps only permute row indices globally, meaning the identity of which values share a row is invariant under any sequence of operations. The same holds for columns. So the partition of values induced by rows (and by columns) must be preserved between $a$ and $b$, up to renaming of row indices and column indices.

If two values are in the same row in $a$, they must end up in the same row in $b$ after applying the row permutation. This forces a well-defined mapping from rows of $a$ to rows of $b$. The same argument applies in reverse, ensuring bijectivity.

Thus the algorithm is checking whether the row-partition and column-partition induced by the permutation of values can be consistently relabeled.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())

        pos_a = {}
        pos_b = {}

        for i in range(n):
            row = list(map(int, input().split()))
            for j, x in enumerate(row):
                pos_a[x] = (i, j)

        for i in range(n):
            row = list(map(int, input().split()))
            for j, x in enumerate(row):
                pos_b[x] = (i, j)

        row_map = {}
        col_map = {}

        ok = True

        for x in pos_a:
            ra, ca = pos_a[x]
            rb, cb = pos_b[x]

            if ra in row_map and row_map[ra] != rb:
                ok = False
                break
            if ca in col_map and col_map[ca] != cb:
                ok = False
                break

            row_map[ra] = rb
            col_map[ca] = cb

        if ok:
            if len(set(row_map.values())) != len(row_map):
                ok = False
            if len(set(col_map.values())) != len(col_map):
                ok = False

        out.append("YES" if ok else "NO")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution first compresses both matrices into position lookup tables so each value directly reveals its coordinates. Then it builds two partial mappings: one for rows and one for columns. The consistency checks ensure that a row in the first matrix never tries to map to two different rows in the second matrix, which would contradict the existence of a global row permutation.

The final injectivity check ensures we truly have permutations, not many-to-one mappings, which would violate reversibility of row and column swaps.

A common pitfall is forgetting that consistency must be enforced globally across all values, not row-by-row independently.

## Worked Examples

### Example 1

Input:

```
1
2 2
1 2
3 4
4 3
2 1
```

| value | pos in a | pos in b | row map | col map |
| --- | --- | --- | --- | --- |
| 1 | (0,0) | (1,1) | 0→1 | 0→1 |
| 2 | (0,1) | (1,0) | 0→1 | 1→0 |
| 3 | (1,0) | (0,1) | 1→0 | 0→1 |
| 4 | (1,1) | (0,0) | 1→0 | 1→0 |

All mappings are consistent and bijective.

This shows that even when both rows and columns are fully reversed, the mapping remains valid as long as consistency is preserved.

### Example 2

Input:

```
1
2 2
1 2
3 4
4 1
2 3
```

| value | pos in a | pos in b | row map | col map |
| --- | --- | --- | --- | --- |
| 1 | (0,0) | (1,1) | 0→1 | 0→1 |
| 2 | (0,1) | (0,1) | 0→0 | 1→1 |
| 3 | (1,0) | (1,0) | 1→1 | 0→0 |
| 4 | (1,1) | (0,0) | 1→0 | 1→0 |

Row mapping becomes inconsistent: row 0 maps to both 1 and 0. This violates the requirement of a single global row permutation.

This demonstrates how a single conflict in induced mappings invalidates the transformation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | Each value is processed once to build positions and verify mappings |
| Space | $O(nm)$ | Storing position maps for all values |

The solution scales linearly with the total number of elements across all test cases, which fits comfortably under the constraint of $2 \cdot 10^5$ total cells.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n, m = map(int, input().split())
            pa, pb = {}, {}

            for i in range(n):
                for j, x in enumerate(map(int, input().split())):
                    pa[x] = (i, j)
            for i in range(n):
                for j, x in enumerate(map(int, input().split())):
                    pb[x] = (i, j)

            rm, cm = {}, {}
            ok = True
            for x in pa:
                ra, ca = pa[x]
                rb, cb = pb[x]
                if ra in rm and rm[ra] != rb:
                    ok = False
                    break
                if ca in cm and cm[ca] != cb:
                    ok = False
                    break
                rm[ra] = rb
                cm[ca] = cb

            if ok:
                if len(set(rm.values())) != len(rm):
                    ok = False
                if len(set(cm.values())) != len(cm):
                    ok = False

            out.append("YES" if ok else "NO")

        return "\n".join(out)

    return solve()

# provided samples
assert run("""7
1 1
1
1
2 2
1 2
3 4
4 3
2 1
2 2
1 2
3 4
4 3
1 2
3 4
1 5 9 6
12 10 4 8
7 11 3 2
1 5 9 6
12 10 4 8
7 11 3 2
3 3
1 5 9
6 4 2
3 8 7
9 5 1
2 4 6
7 8 3
2 3
1 2 6
5 4 3
6 1 2
3 4 5
1 5
5 1 2 3 4
4 2 5 1 3
""") == """YES
YES
NO
YES
YES
NO
YES"""

# custom cases

# minimum size
assert run("""1
1 1
1
1
""") == "YES"

# impossible mapping
assert run("""1
2 2
1 2
3 4
1 3
2 4
""") == "NO"

# row-only swap
assert run("""1
2 3
1 2 3
4 5 6
4 5 6
1 2 3
""") == "YES"

# column-only swap
assert run("""1
3 2
1 2
3 4
5 6
2 1
4 3
6 5
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 identity | YES | trivial base case |
| inconsistent mapping | NO | detects row/column conflict |
| row permutation only | YES | row swaps alone sufficient |
| column permutation only | YES | column swaps alone sufficient |

## Edge Cases

A tricky edge case is when row mappings are locally consistent but globally collide. For example, if two different rows in $a$ both try to map into the same row in $b$, the algorithm catches this via injectivity check.

Consider:

```
a:
1 2
3 4

b:
1 2
3 4
```

Here identity mapping is valid.

Now modify:

```
b:
3 4
1 2
```

Row mapping becomes 0→1 and 1→0, which is fine. But if a third row existed trying to map inconsistently, the conflict would appear only when checking global uniqueness of mapped values, not per assignment.

The algorithm correctly handles this by enforcing both consistency and bijection constraints over the entire mapping space, rather than relying on local row comparisons.
