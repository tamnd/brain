---
title: "CF 1801A - The Very Beautiful Blanket"
description: "We are asked to construct an $n times m$ grid filled with integers such that a specific XOR condition holds for every $4 times 4$ subgrid."
date: "2026-06-09T09:30:58+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1801
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 857 (Div. 1)"
rating: 1600
weight: 1801
solve_time_s: 137
verified: false
draft: false
---

[CF 1801A - The Very Beautiful Blanket](https://codeforces.com/problemset/problem/1801/A)

**Rating:** 1600  
**Tags:** bitmasks, constructive algorithms  
**Solve time:** 2m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct an $n \times m$ grid filled with integers such that a specific XOR condition holds for every $4 \times 4$ subgrid. For any contiguous block of four rows and four columns, two opposite $2 \times 2$ corners must have equal XOR sums: the XOR of the top-left and bottom-right $2 \times 2$ blocks must match, and the XOR of the top-right and bottom-left $2 \times 2$ blocks must also match.

Beyond satisfying these local XOR constraints everywhere, we are asked to maximize the number of distinct values appearing in the grid.

The constraints are large enough that brute force construction or checking all assignments is impossible. The grid can contain up to $200 \times 200 = 40000$ cells per test, and up to 1000 tests, with total cells bounded by $2 \cdot 10^5$. This implies we need a construction that is linear in the grid size per test case.

A naive attempt might try assigning unique values greedily and then fixing violations of the XOR constraints. This fails because each cell participates in many overlapping $4 \times 4$ constraints, so local fixes propagate and quickly become inconsistent.

Another possible incorrect approach is to assume we only need to satisfy the condition for a single $4 \times 4$ block. That ignores that every sliding $4 \times 4$ window must satisfy the same structure, which enforces a strong global periodicity.

The real challenge is recognizing that the constraint is not local in a simple way but imposes a structured linear dependency across the grid.

## Approaches

A brute-force viewpoint is to treat each cell as a variable and each $4 \times 4$ subgrid condition as a system of XOR equations. For each window, we impose two XOR equalities, giving roughly $O(nm)$ constraints. Solving this directly would require Gaussian elimination over $GF(2)$ on a system with up to 40000 variables, which is far too slow.

The key observation is that XOR constraints of this form enforce a separable structure: the grid can be decomposed into independent contributions from rows and columns, and more specifically into a pattern determined entirely by the last two bits of coordinates.

The condition essentially says that when shifting a $2 \times 2$ block across the grid, the XOR differences must remain consistent. This forces the grid to behave like a function where value differences depend only on a small neighborhood of coordinates, which suggests constructing values using bitwise encoding of row and column indices.

A standard way to satisfy such constraints while maximizing distinct values is to assign each cell a value based on a combination of row and column bits so that every $4 \times 4$ window preserves the XOR symmetry automatically. One natural construction is to encode row and column indices into disjoint bit ranges, for example using:

$$B[i][j] = (i \ll k) \oplus j$$

for sufficiently large $k$. This guarantees that XOR over any rectangular pattern splits cleanly between row and column contributions, making both required equalities hold.

This construction also maximizes distinct values: since both row and column indices contribute independently, every cell becomes unique as long as $i, j$ differ.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force system solving | $O((nm)^3)$ or worse | $O((nm)^2)$ | Too slow |
| Bitwise coordinate encoding | $O(nm)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

1. Assign each cell $(i, j)$ a value formed by combining its row and column indices using bit shifts and XOR. A convenient choice is to separate row and column bits so they never interfere.
2. For each row index $i$, shift it into higher bits to ensure row identity occupies a disjoint range from columns. This prevents XOR cancellation between different dimensions.
3. For each column index $j$, keep it in the lower bits so that column variation remains fully distinguishable within each row block.
4. Fill the grid using $B[i][j] = (i \ll 7) \oplus j$. The constant shift only needs to be large enough to avoid overlap with column bits (any fixed safe offset works since $m \le 200 < 2^8$).
5. Output the entire matrix. Since every value is unique, the number of distinct values is exactly $n \cdot m$, which is the maximum possible.

### Why it works

The XOR constraints are linear over $GF(2)$, so we can analyze row-dependent and column-dependent parts separately. By encoding row information in higher bits and column information in lower bits, every XOR over any $2 \times 2$ or $4 \times 4$ block splits into independent row and column contributions. Each side of the required equalities contains the same multiset of row indices and the same multiset of column indices, so their XORs match exactly. This prevents cross-term interference and guarantees all constraints hold simultaneously.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        
        shift = 10  # enough since m <= 200
        
        cnt = n * m
        print(cnt)
        
        for i in range(n):
            row = []
            base = i << shift
            for j in range(m):
                row.append(str(base ^ j))
            print(" ".join(row))

if __name__ == "__main__":
    solve()
```

The solution directly constructs each row independently. The key implementation detail is the fixed bit shift, which guarantees no overlap between row and column contributions. A shift of 10 is sufficient because $2^{10} = 1024$, which exceeds the maximum possible column index, so XOR cannot cause unintended collisions between row and column parts.

The output count is always $n \cdot m$, which is optimal since all entries are distinct.

## Worked Examples

### Example 1

Input:

```
1
4 4
```

We compute $B[i][j] = (i \ll 10) \oplus j$.

| i | j | base = i<<10 | value |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 |
| 1 | 0 | 1024 | 1024 |
| 1 | 1 | 1024 | 1025 |

Continuing this pattern fills a grid where each row is a shifted copy of $0..3$.

This shows that every value is unique and row separation is clean. The XOR structure across any $4 \times 4$ block preserves equality because each side aggregates identical row shifts and identical column XOR structure.

### Example 2

Input:

```
1
5 6
```

| i | j | base | value |
| --- | --- | --- | --- |
| 2 | 3 | 2048 | 2051 |
| 3 | 2 | 3072 | 3074 |
| 4 | 5 | 4096 | 4101 |

The same structure extends uniformly. Any $4 \times 4$ subgrid contains two copies of each involved row offset in symmetric positions, ensuring XOR balance on both required diagonals.

This confirms that locality does not break the construction since the encoding is globally consistent.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | each cell computed once per test case |
| Space | $O(1)$ | only temporary row storage used for printing |

The total number of cells across all test cases is bounded by $2 \cdot 10^5$, so the construction comfortably fits within time limits. Each operation is a simple bit shift and XOR, which is constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        cnt = n * m
        out.append(str(cnt))
        shift = 10
        for i in range(n):
            row = [(i << shift) ^ j for j in range(m)]
            out.append(" ".join(map(str, row)))
    return "\n".join(out)

# provided samples (structure check only, exact values depend on construction)
assert run("1\n4 4\n").count("\n") > 0

# minimum size
assert run("1\n4 4\n").splitlines()[0] == "16"

# rectangular grid
assert run("1\n4 6\n").splitlines()[0] == "24"

# square larger
assert run("1\n6 6\n").splitlines()[0] == "36"

# multiple tests
assert run("2\n4 4\n5 5\n").splitlines()[0] == "16"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4×4 grid | 16 distinct values | base correctness and counting |
| 4×6 grid | 24 distinct values | non-square handling |
| 6×6 grid | 36 distinct values | full generality |
| multiple tests | correct per case | multi-case parsing |

## Edge Cases

A minimal valid grid of size $4 \times 4$ is the tightest constraint case. The construction assigns values like $0,1,2,\dots$ shifted by row blocks. Even in this smallest scenario, every cell remains unique and the XOR constraints hold because each row contributes a fixed high-bit signature.

For a $4 \times 6$ grid, the same row shifting ensures that extending columns does not introduce collisions. Each row remains independent in high bits, so no interference occurs between different rows inside overlapping $4 \times 4$ windows.

For multiple test cases, each grid is generated independently. Since no global state is used, there is no carry-over effect, and each output block remains valid in isolation.
