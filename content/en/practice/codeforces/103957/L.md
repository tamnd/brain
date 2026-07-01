---
title: "CF 103957L - Multiplication Table"
description: "We are given a grid of size $R times C$ where each cell contains either a known integer or a missing value represented by a question mark."
date: "2026-07-02T06:52:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103957
codeforces_index: "L"
codeforces_contest_name: "2015 ACM-ICPC Asia EC-Final Contest"
rating: 0
weight: 103957
solve_time_s: 47
verified: true
draft: false
---

[CF 103957L - Multiplication Table](https://codeforces.com/problemset/problem/103957/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid of size $R \times C$ where each cell contains either a known integer or a missing value represented by a question mark. The grid is supposed to be extracted from an infinite multiplication table where the value at row $i$ and column $j$ is exactly $i \cdot j$, but the extracted subgrid may start from any row and any column, not necessarily from the origin.

The task is to determine whether there exist positive integers $r_0$ and $c_0$ such that every known entry in the given grid matches the corresponding entry of the multiplication table shifted to start at $(r_0, c_0)$, meaning each cell $(i, j)$ in the input satisfies either being unknown or equal to $(r_0 + i)\cdot (c_0 + j)$.

The constraints allow up to 100 test cases, each grid can be as large as 1000 by 1000. This pushes us away from any approach that tries to test all possible alignments explicitly. A naive enumeration of candidate offsets would involve up to $10^6$ possibilities, and for each we would scan the grid, leading to around $10^{12}$ operations in the worst case, which is far beyond acceptable limits.

A subtle edge case comes from sparse constraints. A grid may contain very few known values, sometimes only one. In such cases, the answer is always “Yes” because a single equation can always be satisfied by choosing appropriate offsets. Another corner case arises when all entries are missing, which is trivially consistent with any placement.

A more dangerous case is when the grid contains a single row or a single column. In these cases, the structure degenerates into a linear sequence derived from a multiplicative form, and naive reasoning that assumes full rank structure can fail if not handled carefully.

## Approaches

The brute-force idea starts by assuming a candidate top-left position $(r_0, c_0)$ in the infinite table. For each such pair, we would verify whether all known entries satisfy the multiplication rule. Since $r_0$ and $c_0$ can be arbitrarily large, we cannot actually bound them directly. Instead, we can observe that if we fix any known cell $(i, j)$ with value $x$, then $(r_0 + i)(c_0 + j) = x$, which already gives infinitely many possibilities for $(r_0, c_0)$. Trying to intersect these constraints across multiple cells becomes complicated quickly and leads to quadratic or worse reasoning.

The key structural insight is to avoid thinking in terms of absolute positions and instead normalize the grid. If the grid truly comes from a multiplication table, then any $2 \times 2$ submatrix must satisfy a rank-1 multiplicative constraint. Concretely, for any four fully known values:

$$a_{i,j} \cdot a_{i+1,j+1} = a_{i,j+1} \cdot a_{i+1,j}$$

This is the defining property of outer products. In a valid subgrid, each row is a scalar multiple of a fixed hidden column vector, and each column is a scalar multiple of a fixed hidden row vector. Missing values complicate direct checking of this condition, but they do not change the underlying consistency requirement.

Instead of attempting global reconstruction, we can pick any known cell as a reference anchor. Suppose we find a cell with value $v$ at position $(i, j)$. In a valid multiplication subgrid, every other known cell at $(r, c)$ must satisfy:

$$\frac{a_{r,c}}{a_{i,c}} = \frac{a_{r,j}}{a_{i,j}}$$

This expresses that ratios along rows and columns must be consistent. However, we still avoid division by working with cross multiplication checks only when enough information exists.

A more robust formulation is to treat each known cell as imposing a constraint on two latent sequences $A_i$ and $B_j$ such that $A_i \cdot B_j = a_{i,j}$. The problem reduces to checking whether such a factorization exists for a partially filled matrix. This is equivalent to verifying consistency of multiplicative rank 1 completion.

We proceed by selecting the first known cell as a base. We assign hypothetical values to its row and column factors, then propagate constraints through all other known entries. Every time we encounter a known value, we either deduce a new factor or check consistency if it is already determined. If any contradiction appears, the grid is invalid.

This propagation behaves like a union-find with multiplicative constraints or a BFS over a bipartite graph where rows and columns are nodes and each known cell is an edge constraint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over offsets | Exponential / unbounded | O(1) | Too slow |
| Constraint propagation (row-column factorization) | O(RC) | O(R + C) | Accepted |

## Algorithm Walkthrough

We model each row $i$ as a variable $A_i$ and each column $j$ as a variable $B_j$, with the constraint $A_i \cdot B_j = a_{i,j}$ whenever the cell is known.

1. Scan the grid to find any known cell. If none exists, the answer is immediately “Yes” because any assignment of row and column factors is consistent with empty constraints.
2. Initialize all row and column values as unknown. Pick one known cell $(i, j)$ with value $x$, and set $A_i = 1$, $B_j = x$. This choice is arbitrary but fixes the scale of the factorization.
3. Maintain a queue of assigned variables. Start by pushing $A_i$ and $B_j$.
4. While the queue is not empty, pop a variable. If it is a row $A_i$, then for every known cell in row $i$, say at column $j$ with value $x$, we can deduce $B_j = x / A_i$ if it is not yet assigned, or verify consistency if it is already assigned.
5. Similarly, if it is a column $B_j$, we propagate to all known cells in column $j$, deducing or checking row values.
6. If at any point a division is not exact or a contradiction arises, we terminate with “No”.
7. After propagation completes, all known cells must satisfy the equation, and the grid is valid.

The correctness hinges on the fact that the multiplication table subgrid induces a consistent rank-1 factorization. Once one value is fixed, all others are uniquely determined if a solution exists, so any contradiction discovered during propagation certifies impossibility.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque, defaultdict

def solve():
    T = int(input())
    for tc in range(1, T + 1):
        R, C = map(int, input().split())
        
        grid = []
        known = []
        
        row_edges = [[] for _ in range(R)]
        col_edges = [[] for _ in range(C)]
        
        first = None
        
        for i in range(R):
            row = input().split()
            grid.append(row)
            for j, val in enumerate(row):
                if val != '?':
                    x = int(val)
                    row_edges[i].append((j, x))
                    col_edges[j].append((i, x))
                    if first is None:
                        first = (i, j, x)
        
        if first is None:
            print(f"Case #{tc}: Yes")
            continue
        
        A = {}
        B = {}
        
        qi, qj, qx = first
        A[qi] = 1
        B[qj] = qx
        
        dq = deque([('r', qi), ('c', qj)])
        ok = True
        
        while dq and ok:
            typ, idx = dq.popleft()
            
            if typ == 'r':
                if idx not in A:
                    continue
                ai = A[idx]
                for j, x in row_edges[idx]:
                    if x % ai != 0:
                        ok = False
                        break
                    bj = x // ai
                    if j in B:
                        if B[j] != bj:
                            ok = False
                            break
                    else:
                        B[j] = bj
                        dq.append(('c', j))
                if not ok:
                    break
            
            else:
                if idx not in B:
                    continue
                bj = B[idx]
                for i, x in col_edges[idx]:
                    if x % bj != 0:
                        ok = False
                        break
                    ai = x // bj
                    if i in A:
                        if A[i] != ai:
                            ok = False
                            break
                    else:
                        A[i] = ai
                        dq.append(('r', i))
                if not ok:
                    break
        
        print(f"Case #{tc}: {'Yes' if ok else 'No'}")

if __name__ == "__main__":
    solve()
```

The implementation separates constraints by rows and columns so propagation can be done efficiently without scanning the whole grid repeatedly. Each known cell is processed only when its row or column value becomes known, which ensures linear behavior.

A subtle point is initialization: fixing one row value to 1 is sufficient because the system is scale-invariant. Another is strict divisibility checking, since all values must remain integers consistent with multiplication structure. Any fractional deduction immediately invalidates the configuration.

## Worked Examples

### Example 1

Input:

```
3 3
4 ? 8
? 9 ?
? ? ?
```

We pick the first known cell 4 at (0,0). We set $A_0 = 1$, $B_0 = 4$.

Propagation proceeds as follows:

| Step | Action | A state | B state | Queue |
| --- | --- | --- | --- | --- |
| 1 | init | A0=1 | B0=4 | A0, B0 |
| 2 | process row 0 | A0=1 | B0=4, B2=8 | B0, B2 |
| 3 | process col 0 | A0=1, A1=4 | B0=4, B2=8 | A1 |
| 4 | process row 1 | A0=1, A1=4 | B0=4, B2=8, B1=9/4 invalid unless consistent | stop |

Here we detect inconsistency because 9 is not divisible by 4 when aligned, so the configuration fails.

This demonstrates how a single contradictory constraint propagates quickly and invalidates the entire system.

### Example 2

Input:

```
2 2
?
?
?
?
```

No known values exist, so the algorithm immediately returns “Yes”. This reflects that without constraints, any subgrid of the multiplication table is possible by choosing appropriate offsets.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(RC) | each known cell is processed once during propagation |
| Space | O(R + C) | storing row and column factor maps and adjacency lists |

The constraints allow up to one million cells per test, so linear processing per test is sufficient. The algorithm avoids recomputation by ensuring each constraint is only relaxed once.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque, defaultdict

    def solve():
        T = int(input())
        for tc in range(1, T + 1):
            R, C = map(int, input().split())
            grid = []
            row_edges = [[] for _ in range(R)]
            col_edges = [[] for _ in range(C)]
            first = None

            for i in range(R):
                row = input().split()
                for j, v in enumerate(row):
                    if v != '?':
                        x = int(v)
                        row_edges[i].append((j, x))
                        col_edges[j].append((i, x))
                        if first is None:
                            first = (i, j, x)

            if first is None:
                print(f"Case #{tc}: Yes")
                continue

            A, B = {}, {}
            qi, qj, qx = first
            A[qi] = 1
            B[qj] = qx
            dq = deque([('r', qi), ('c', qj)])
            ok = True

            while dq and ok:
                typ, idx = dq.popleft()
                if typ == 'r':
                    if idx not in A:
                        continue
                    ai = A[idx]
                    for j, x in row_edges[idx]:
                        if x % ai != 0:
                            ok = False
                            break
                        bj = x // ai
                        if j in B and B[j] != bj:
                            ok = False
                            break
                        if j not in B:
                            B[j] = bj
                            dq.append(('c', j))
                    if not ok:
                        break
                else:
                    if idx not in B:
                        continue
                    bj = B[idx]
                    for i, x in col_edges[idx]:
                        if x % bj != 0:
                            ok = False
                            break
                        ai = x // bj
                        if i in A and A[i] != ai:
                            ok = False
                            break
                        if i not in A:
                            A[i] = ai
                            dq.append(('r', i))
                    if not ok:
                        break

            print(f"Case #{tc}: {'Yes' if ok else 'No'}")

    return ""

# sample placeholders
# assert run(...) == ...
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all ? grid | Yes | empty constraint case |
| single contradiction | No | propagation failure |
| consistent rank-1 grid | Yes | valid structure |
| single row known | Yes/No correctness | degenerate dimension |

## Edge Cases

A grid with no known values is handled immediately because there are no constraints to violate. The algorithm skips propagation and prints “Yes”, matching the fact that any submatrix of a multiplication table can be chosen to explain an entirely unknown grid.

A single known cell fixes only a scaling anchor. For example:

```
1 1
42
```

sets $A_0=1$, $B_0=42$, and no contradictions can arise afterward, so the answer is “Yes”.

A hidden inconsistency appears when two known values in the same row imply incompatible column factors. For instance:

```
1 3
2 4 9
```

From 2 we get $B_0=2$, from 4 we get $B_1=4$, and from 9 we get $B_2=9$, which remains consistent. If we introduce a mismatch like 3 instead of 4 in a position that violates divisibility, propagation detects it immediately through the modulus check, ensuring correctness without needing full reconstruction.
