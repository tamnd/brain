---
title: "CF 106394E - Grid Coloring"
description: "We are given a square grid of size $n times n$, and each cell must be colored with one of two colors, red or blue. A coloring is considered valid if every cell has exactly two neighbors (sharing a side) that have the same color as itself."
date: "2026-06-25T10:10:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106394
codeforces_index: "E"
codeforces_contest_name: "RUCP x WiCS Mini-Contest"
rating: 0
weight: 106394
solve_time_s: 45
verified: true
draft: false
---

[CF 106394E - Grid Coloring](https://codeforces.com/problemset/problem/106394/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a square grid of size $n \times n$, and each cell must be colored with one of two colors, red or blue. A coloring is considered valid if every cell has exactly two neighbors (sharing a side) that have the same color as itself.

So each cell looks at its up, down, left, and right neighbors (when they exist), and among those adjacent cells, exactly two must match its color. Cells on the border have fewer neighbors, so their condition is interpreted using only the existing neighbors.

The task is to determine whether such a coloring exists for each given $n$, and if it does, output one valid configuration.

The constraints allow up to $t \le 100$ test cases and $n \le 1000$, with the sum of $n^2$ across tests at most $10^6$. This means any solution that is $O(n^2)$ per test case is acceptable, but anything cubic or involving repeated per-cell simulation inside multiple iterations would be too slow.

A brute-force assignment over all $2^{n^2}$ grids is obviously impossible. Even trying to assign colors greedily and backtracking locally would explode because every cell’s validity depends on a global structure, not just local consistency.

A subtle edge case appears immediately at small sizes. For $n = 1$, the single cell has no neighbors, so it cannot have exactly two same-colored neighbors, making the answer impossible. For $n = 2$, every cell has exactly two neighbors, so the condition reduces to “both neighbors must match the cell’s color,” which forces the entire grid to be monochromatic, and that actually works. For $n = 3$, attempts to satisfy the condition fail because corner and center constraints conflict, and no periodic pattern can satisfy all degrees simultaneously.

A naive approach that tries to assign colors row by row while satisfying local constraints will often fail because fixing one row forces contradictions in adjacent rows.

## Approaches

A brute-force viewpoint would be to assign colors cell by cell and check whether the condition holds at the end. That works conceptually because verification is straightforward: for each cell, count matching neighbors and check if it equals two. The cost is $O(n^2)$ per configuration, but the number of configurations is exponential, so this is immediately infeasible.

Trying to improve this greedily, one might attempt to assign colors while maintaining partial validity, ensuring that each cell has a “target” number of matching neighbors. The failure point is that decisions propagate in both directions: setting a cell influences its neighbors, but those neighbors also constrain the original cell later, so local greedy decisions are not stable.

The key structural insight is to stop thinking in terms of local constraints and instead look for a global repeating pattern where every cell has identical local environment. If every interior cell sees the same pattern of neighbors, the condition automatically becomes uniform and either holds everywhere or nowhere.

The requirement “exactly two same-colored neighbors” suggests a fixed degree pattern, and the simplest way to satisfy such uniform constraints in a grid is to use a periodic tiling. A $2 \times 2$ repeating block is the natural candidate because it guarantees identical neighborhood structure for all interior cells.

If we try a block like:

```
BB
BB
```

every cell inside has all neighbors (up to four) equal to itself, which makes each interior cell have 4 matching neighbors, not 2, so that fails.

The next attempt is a checkerboard pattern, but that gives zero matching neighbors, which also fails.

The correct construction comes from mixing structure across both parity classes in a way that ensures each cell sees exactly two identical neighbors horizontally or vertically. One such pattern is to enforce equality along diagonals of slope 1, which creates paired adjacency in both directions. A clean way to express this is:

$$color(i, j) = (i + j) \bmod 2 \text{ with a controlled flip on alternating rows}$$

but more concretely, the construction that works for this problem is to build repeating $2 \times 2$ blocks of the form:

```
R R
B B
```

This ensures that within each row, neighbors match in pairs, and vertical adjacency is structured so that each cell sees exactly two same-colored neighbors: one horizontal and one vertical, depending on position.

However, this pattern only works consistently when $n$ is even. When $n$ is odd, the parity mismatch forces an unpaired row at the boundary, breaking the uniform degree condition. That is why odd sizes fail.

So the full solution becomes a parity argument: even $n$ admits a tiling construction, odd $n$ does not.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force assignment + validation | exponential | $O(n^2)$ | Too slow |
| Greedy local assignment | $O(n^2)$ with backtracking risk | $O(n^2)$ | Fails cases |
| Periodic 2×2 construction + parity check | $O(n^2)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

1. First check whether $n$ is even. If it is odd, immediately conclude that no valid construction exists, because any uniform tiling breaks at the boundary row and cannot preserve the required neighbor count globally.
2. If $n$ is even, construct the grid row by row using a repeating $2 \times 2$ pattern. This ensures that every local neighborhood repeats identically across the grid, so we only need to verify one representative cell.
3. For every pair of rows $i$ and $i+1$, fill columns in blocks of two. Within each block, assign identical colors horizontally, and alternate the pair vertically so that each column also forms consistent vertical pairing.
4. Output the resulting grid.

### Why it works

The construction enforces that every cell belongs to a uniform $2 \times 2$ tile where all adjacency relationships are identical up to translation. In such a tiling, each cell has exactly two neighbors with the same color because each color class forms disjoint chains of length two in both row and column directions. Since every cell lies in an identical local environment, verifying one cell implicitly verifies all others, making the condition globally consistent.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())

        if n % 2 == 1:
            print("NO")
            continue

        print("YES")
        for i in range(n):
            row = []
            for j in range(n):
                # 2x2 repeating block:
                if (i // 2 + j // 2) % 2 == 0:
                    row.append('R')
                else:
                    row.append('B')
            print("".join(row))

if __name__ == "__main__":
    solve()
```

The code directly implements a $2 \times 2$ periodic tiling. The expression `i // 2` and `j // 2` groups the grid into blocks of size two, and the parity of their sum alternates colors across blocks. This ensures consistency both horizontally and vertically, so every cell has the same neighborhood structure.

The early rejection for odd $n$ handles the impossibility case without attempting construction.

A common implementation mistake is to use `(i + j) % 2`, which produces a checkerboard and fails the neighbor-count requirement, or to forget integer division grouping, which destroys the $2 \times 2$ structure entirely.

## Worked Examples

### Example 1

Input:

```
n = 2
```

We build the grid:

| i | j | i//2 | j//2 | parity | color |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | R |
| 0 | 1 | 0 | 0 | 0 | R |
| 1 | 0 | 0 | 0 | 0 | R |
| 1 | 1 | 0 | 0 | 0 | R |

Output:

```
RR
RR
```

Every cell has exactly two neighbors (since each cell has 2 or 3 neighbors depending on position), and all of them match, so the condition holds.

This confirms that even the smallest valid even case works under the construction.

### Example 2

Input:

```
n = 4
```

We get a repeating block structure:

| Block position | Color |
| --- | --- |
| (0,0) | R |
| (0,1) | R |
| (1,0) | R |
| (1,1) | R |
| (0,2) | B |
| (0,3) | B |
| (1,2) | B |
| (1,3) | B |

Continuing this pattern fills the whole grid.

This shows how each $2 \times 2$ region is internally uniform, and adjacency across blocks alternates cleanly without breaking the “two same neighbors” rule.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ per test | Each cell is assigned exactly once |
| Space | $O(n^2)$ | Grid storage for output |

The constraints allow up to $10^6$ total cells, so a single pass construction per cell is easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided samples (format adapted since original omitted full samples)
# assert run("...") == "..."

# minimum odd
assert "NO" in run("1\n1\n")

# smallest even
out = run("1\n2\n")
assert "YES" in out and "RR" in out

# larger even
out = run("1\n4\n")
assert "YES" in out

# multiple tests
out = run("3\n2\n3\n4\n")
assert out.count("YES") == 2 and out.count("NO") == 1

# all even same size
out = run("2\n2\n2\n")
assert out.count("YES") == 2
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n = 1 | NO | smallest impossible case |
| n = 2 | YES + grid | base constructive case |
| n = 4 | YES + grid | larger even correctness |
| mixed t | mixed | handling multiple cases |

## Edge Cases

For $n = 1$, the algorithm immediately rejects it because no cell can satisfy a requirement involving two same-colored neighbors when none exist. The input `1\n1\n` triggers the early check and outputs `NO`.

For $n = 2$, the construction produces a fully uniform block. Every cell’s neighborhood is consistent with the rule because all neighbors are identical, so each cell trivially satisfies the condition.

For larger even $n$, the repeating $2 \times 2$ tiling ensures that boundary effects do not break the structure, since every boundary cell still lies inside a complete block with the same adjacency pattern as interior cells.
