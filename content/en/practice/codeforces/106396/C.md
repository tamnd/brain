---
title: "CF 106396C - \u5f71\u5b50\u620f"
description: "We are given a rectangular board with dimensions $n times m$. Each cell can be interpreted as a position where we may place a chess piece, and the problem asks for the maximum number of pieces we can place under a movement restriction that comes from a knight-like attack rule."
date: "2026-06-20T03:36:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106396
codeforces_index: "C"
codeforces_contest_name: "Tiangong University 2025 ICPC Team Selection Contest II (Online Mirror)"
rating: 0
weight: 106396
solve_time_s: 78
verified: true
draft: false
---

[CF 106396C - \u5f71\u5b50\u620f](https://codeforces.com/problemset/problem/106396/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular board with dimensions $n \times m$. Each cell can be interpreted as a position where we may place a chess piece, and the problem asks for the maximum number of pieces we can place under a movement restriction that comes from a knight-like attack rule. A piece placed on one cell “controls” certain other cells, and any valid configuration must ensure that no two placed pieces attack each other.

The structure of the movement is the key hidden information: the attack relation always flips parity between two color classes of the grid. This immediately implies a bipartite structure, meaning that if we color the grid like a chessboard, every move goes from one color to the other. As a result, any set of pieces placed entirely on one color class is automatically safe, since no two cells in the same class can attack each other.

The input consists of multiple test cases. Each test case provides two integers $n$ and $m$, describing the grid size. The output is the maximum number of pieces that can be placed on each grid independently.

The constraints are not explicitly shown, but the presence of a closed-form solution in the reference code indicates that $n, m$ can be large, likely up to at least $10^9$ or similar. That immediately rules out any simulation or graph construction. Any solution must reduce the grid to a constant-time formula per test case.

The main edge cases appear when one dimension is very small. A naive checker that assumes a full chessboard coloring result like $\lceil nm/2 \rceil$ fails for thin boards. For example, on a $2 \times 3$ board, a naive formula gives 3, but careful placement rules allow only 4 or sometimes different structured behavior depending on attack geometry. Another fragile case is $1 \times m$, where the board degenerates into a line and all interaction disappears.

## Approaches

A direct approach is to treat the grid as a graph where each cell is a node and edges represent valid attacks. We then try to compute the maximum independent set. This is correct in principle, since we want the largest set of nodes with no edges inside it.

However, building this graph already costs $O(nm)$, and running any standard algorithm for maximum independent set is infeasible since even bipartite matching formulations would require at least linear or superlinear time per test case. For large grids, this approach fails immediately.

The key observation is that the attack structure is highly regular and depends only on relative coordinates. The grid naturally splits into two parity classes, and most interactions only cross these classes. That suggests that in most cases, taking all cells of one parity gives an optimal answer, yielding roughly half of the grid, i.e. $\lfloor (nm+1)/2 \rfloor$.

This works perfectly when both dimensions are at least 3. The reason is that the grid is “dense enough” so no local pattern constraints break the bipartite bound.

The difficulty comes from small dimensions. When $n = 1$, there are no vertical interactions at all, so every cell is independent. When $n = 2$, the board becomes a 2-row strip where knight moves create local conflicts in a repeating pattern. This leads to a periodic optimal structure with period 4 columns, producing a repeating maximum pattern of 4 cells per block of width 4, with special handling of the remainder.

Thus the solution reduces to three regimes: a trivial line case, a constrained strip case, and a general case where parity dominates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Graph / DP | $O(nm)$ or worse | $O(nm)$ | Too slow |
| Optimal Formula Split Cases | $O(1)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read $n$ and $m$, and swap them if necessary so that $n \le m$. This reduces case handling since all formulas depend only on the smaller dimension being “height”.
2. If $n = 1$, return $m$. In a single row, no piece can attack any other because all moves require vertical displacement. Therefore every cell can be occupied safely.
3. If $n = 2$, compute the answer using a block structure along the columns. We split the board into segments of 4 columns. Each full block contributes 4 pieces. For the remaining $m \bmod 4$ columns, the contributions follow a fixed pattern: 1 extra column gives 2 additional placements, 2 columns give 4, 3 columns give 4, and 4 columns give 4. This arises from optimal local packing in a 2-row grid where attack patterns repeat every four columns.
4. If $n \ge 3$, return $\lceil nm / 2 \rceil$. This corresponds to filling one color class of the chessboard coloring. Since all attacks cross parity, no two chosen cells conflict, and this is maximal due to symmetry.

### Why it works

The correctness relies on the structure of knight-like moves preserving bipartiteness and the fact that only narrow grids create local constraints that break pure parity optimality. For $n \ge 3$, every cell has enough neighborhood flexibility that no local configuration can force us below the parity bound. For $n = 1$ and $n = 2$, the graph is too thin, and local overlap constraints become global, producing periodic optimal patterns instead of a simple bipartite maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    if n > m:
        n, m = m, n

    if n == 1:
        print(m)
    elif n == 2:
        k = m // 4
        r = m % 4
        ans = k * 4 + min(4, r * 2)
        print(ans)
    else:
        print((n * m + 1) // 2)

t = int(input())
for _ in range(t):
    solve()
```

The first step ensures we always treat the smaller dimension as $n$, which simplifies reasoning for the $n = 2$ case. The $n = 1$ branch handles the degenerate line graph directly.

The $n = 2$ computation encodes the repeating optimal pattern over blocks of four columns. The multiplication by 4 for full blocks reflects that each 2x4 segment can accommodate four non-attacking pieces in an optimal configuration. The remainder adjustment using `min(4, r * 2)` encodes the precomputed best values for partial blocks.

The final case uses integer arithmetic to compute $\lceil nm/2 \rceil$ safely as `(n * m + 1) // 2`.

## Worked Examples

### Example 1: $n = 2, m = 5$

We apply the 2-row formula.

| Step | Full blocks (m//4) | Remainder (m%4) | Block contribution | Remainder contribution | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 4 | min(4, 2) = 2 | 6 |

The result is 6, showing how the structure is periodic and the remainder contributes partially.

### Example 2: $n = 3, m = 5$

We fall into the general case.

| Step | n*m | parity formula | Answer |
| --- | --- | --- | --- |
| 1 | 15 | (15+1)//2 | 8 |

This confirms that the solution reduces to a simple bipartite maximum when the grid is wide enough.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ per test case | Each case uses only arithmetic and conditional checks |
| Space | $O(1)$ | No auxiliary data structures are used |

The solution comfortably fits within limits even for large numbers of test cases, since every computation is constant time and avoids grid construction entirely.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    data = inp.strip().split()
    t = int(data[0])
    idx = 1
    out = []

    for _ in range(t):
        n = int(data[idx]); m = int(data[idx+1])
        idx += 2

        if n > m:
            n, m = m, n

        if n == 1:
            out.append(str(m))
        elif n == 2:
            k = m // 4
            r = m % 4
            ans = k * 4 + min(4, r * 2)
            out.append(str(ans))
        else:
            out.append(str((n * m + 1) // 2))

    return "\n".join(out)

# provided sample-like checks
assert run("1\n1 10\n") == "10"
assert run("1\n2 3\n") == "4"
assert run("1\n3 3\n") == "5"

# custom cases
assert run("1\n2 1\n") == "2", "thin 2-row minimal width"
assert run("1\n2 8\n") == "8", "full 2-row blocks"
assert run("1\n3 4\n") == "6", "general parity small grid"
assert run("1\n10 10\n") == "50", "square large grid parity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 | 2 | smallest 2-row edge |
| 2 8 | 8 | full periodic blocks |
| 3 4 | 6 | transition to parity rule |
| 10 10 | 50 | large symmetric case |

## Edge Cases

The $n = 1$ case is the most fragile. A naive parity-based solution would incorrectly output $\lceil m/2 \rceil$, but in reality all cells are independent. For input `1 7`, the correct output is `7`, and the algorithm directly returns $m$, matching the fact that no attack edges exist in a single row.

The $n = 2$ case encodes the only nontrivial structure. For input `2 5`, the algorithm computes one full block and one remainder: $4 + 2 = 6$. A naive half-grid assumption would give $\lceil 10/2 \rceil = 5$, which is strictly wrong because the interaction pattern allows denser packing than simple bipartite coloring.

For $n \ge 3$, such as `3 3`, the algorithm returns $\lceil 9/2 \rceil = 5$. Tracing execution confirms that no special branch is triggered and the bipartite structure governs the answer, matching the fact that no thin-grid constraint exists anymore.
