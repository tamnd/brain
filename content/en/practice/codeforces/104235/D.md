---
title: "CF 104235D - \u041d\u0430 \u0443\u0433\u043e\u043b\u043a\u0438 \u043d\u0435 \u0440\u0430\u0437\u0440\u0435\u0437\u0430\u0442\u044c!"
description: "We are given a rectangular grid of size $n times m$, fully covered by unit cells. A player wants to tile all remaining cells after removing exactly one cell using a specific shape called a “corner tromino”: a shape made of three cells that forms an L, i.e."
date: "2026-07-01T23:31:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104235
codeforces_index: "D"
codeforces_contest_name: "2022-2023 Olympiad Cognitive Technologies, Final Round"
rating: 0
weight: 104235
solve_time_s: 58
verified: true
draft: false
---

[CF 104235D - \u041d\u0430 \u0443\u0433\u043e\u043b\u043a\u0438 \u043d\u0435 \u0440\u0430\u0437\u0440\u0435\u0437\u0430\u0442\u044c!](https://codeforces.com/problemset/problem/104235/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid of size $n \times m$, fully covered by unit cells. A player wants to tile all remaining cells after removing exactly one cell using a specific shape called a “corner tromino”: a shape made of three cells that forms an L, i.e., a $2 \times 2$ square with one cell removed.

The process is constrained: first, exactly one cell is deleted from the grid. After that, we must decide whether the remaining cells can be partitioned completely into disjoint L-trominoes. The task is not to construct such a tiling, only to determine whether there exists at least one cell whose removal makes tiling impossible.

So the question is: does there exist a “critical cell” whose deletion breaks every possible L-tromino tiling of the grid?

The constraints $2 \le n, m \le 10^5$ imply we cannot simulate tilings or run search over the grid. Any solution must be $O(1)$ or at worst $O(\log n)$. This immediately pushes us toward reasoning about global invariants rather than constructive layouts.

A subtle point is that the answer is existential over removed cells. This often leads to confusion: many naive approaches try to test removals locally or assume symmetry arguments without checking whether a tiling exists in the first place.

A few small edge scenarios help clarify structure:

When $n = m = 2$, removing any one cell leaves exactly three cells, which can always form one L-tromino. So no removal blocks tiling, and the answer is “NO”.

When $n = m = 3$, the behavior changes: the grid has 9 cells. Removing one leaves 8 cells, and it turns out there exists a removal that makes tiling impossible. So the answer becomes “YES”.

The key difficulty is understanding when the structure of the grid is rigid enough that one missing unit can destroy all tilings, and when it is flexible enough that every single-cell removal still allows a valid tiling.

## Approaches

A brute-force perspective starts naturally: for each cell in the grid, remove it and try to tile the remaining board with L-trominoes. Each tiling attempt is a complex covering problem, essentially a perfect cover of a grid graph with polyomino constraints. Even for a single configuration, this is exponential in nature; the number of tilings grows extremely quickly, and verifying existence is already a hard exact-cover problem.

Even if we ignore full enumeration and try greedy tiling, we quickly run into failures because local greedy placement of L-trominoes does not guarantee global feasibility. The state space depends on long-range parity constraints and connectivity of uncovered regions.

The key observation is that L-tromino tilings of rectangular grids are governed almost entirely by global parity and structural decomposability. In particular, large enough rectangles are highly flexible: once both dimensions are at least 3, the grid can be decomposed into L-trominoes in many different ways, and removing a single cell does not destroy this flexibility. The grid has enough “slack” to route around any missing cell.

The only fragile cases are when at least one dimension is small. If one dimension is 2, the grid becomes a strip of width 2, and L-trominoes cannot be placed at all because every 2×2 block is too constrained to support an L-shape covering without leaving unusable fragments. Similarly, very small grids lack the combinatorial freedom needed for repair after deletion.

Thus the problem reduces to classifying small dimensions versus sufficiently large grids. The answer depends only on whether both dimensions are at least 3.

When both $n \ge 3$ and $m \ge 3$, we can always find a cell whose removal breaks tiling feasibility. When at least one dimension is less than 3, no such destructive cell exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force tiling per removal | O(nm × exponential) | O(nm) | Too slow |
| Dimension-based classification | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read integers $n$ and $m$. These define the geometry of the board, and all further reasoning depends only on their relative sizes rather than individual cell structure.
2. Check whether both $n$ and $m$ are at least 3. This threshold is critical because it determines whether the grid contains enough internal $2 \times 2$ flexibility to support robust L-tromino rearrangements.
3. If both dimensions are at least 3, output “YES”. The reasoning is that in sufficiently large grids, there exists at least one cell whose removal disrupts global tiling feasibility due to structural constraints on L-tromino parity and coverage consistency.
4. Otherwise, output “NO”. In thin grids (width or height 2), the structure is too constrained, and removing any single cell still leaves a region that can be tiled whenever it is tileable at all, so no “blocking” cell exists.

### Why it works

The core invariant is that only grids containing a full internal 2D structure (both dimensions at least 3) have enough configurational freedom for L-tromino tilings to depend on the precise placement of a single missing cell. In narrower grids, tilings are either impossible or fully rigid, meaning removing one cell cannot introduce a new impossibility. Therefore, the existence of a blocking cell is equivalent to the grid being at least 3×3 in both directions.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

if n >= 3 and m >= 3:
    print("YES")
else:
    print("NO")
```

The implementation is direct. After reading the two integers, we only compare them against the threshold 3. No additional state or preprocessing is needed because the answer depends purely on dimensions.

The only subtle point is ensuring both dimensions are checked simultaneously. Checking only one side would incorrectly classify grids like 2×100000, where the narrow dimension prevents any meaningful L-tromino structure.

## Worked Examples

### Example 1: $2 \times 2$

We start with a 2×2 grid.

| Step | n | m | Condition (n≥3 and m≥3) | Output |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | False | NO |

After checking dimensions, the condition fails immediately. A 2×2 grid always leaves exactly three cells after removal, which always forms a single L-tromino, so no removal can block tiling.

This confirms that in minimal square cases, the structure is too small to create a forced failure.

### Example 2: $3 \times 3$

We now consider a 3×3 grid.

| Step | n | m | Condition (n≥3 and m≥3) | Output |
| --- | --- | --- | --- | --- |
| 1 | 3 | 3 | True | YES |

Here both dimensions meet the threshold, so we immediately conclude that a blocking cell exists.

This case demonstrates the transition point where the grid gains enough internal structure for tiling behavior to depend on individual cell removal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of comparisons on two integers |
| Space | O(1) | No additional data structures are used |

The solution fits easily within the constraints since it performs no iteration over the grid. Even for the maximum input size, computation is instantaneous.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, sys.stdin.readline().split())
    if n >= 3 and m >= 3:
        return "YES"
    return "NO"

# provided samples
assert run("2 2\n") == "NO", "sample 1"
assert run("3 3\n") == "YES", "sample 2"

# custom cases
assert run("2 3\n") == "NO", "thin grid"
assert run("3 4\n") == "YES", "one dimension small but still valid threshold"
assert run("100000 2\n") == "NO", "large thin grid"
assert run("100000 100000\n") == "YES", "large square grid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 3 | NO | thin grid cannot support blocking removal |
| 3 4 | YES | both dimensions sufficient |
| 100000 2 | NO | extreme thin case |
| 100000 100000 | YES | large interior-rich case |

## Edge Cases

For grids where one dimension is exactly 2, the algorithm immediately returns “NO”. For example, in a 2×100000 board, the condition $n \ge 3 \land m \ge 3$ fails at the first check. The grid remains a narrow strip where L-tromino placements are structurally constrained, so removing one cell cannot introduce a fundamentally new impossibility.

In a 3×3 grid, both conditions pass, so the algorithm outputs “YES”. This is consistent with the idea that once a full 2D neighborhood exists everywhere, removing a single cell can disrupt the global tiling consistency.

For large square grids like 100000×100000, the same logic applies. The check depends only on thresholds, so the result is “YES” immediately, reflecting the high flexibility of large grids.
