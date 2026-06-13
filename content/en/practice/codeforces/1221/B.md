---
title: "CF 1221B - Knights"
description: "We are filling an $n times n$ chessboard where every cell must contain either a white knight or a black knight. After the board is filled, we look at all pairs of cells where a knight can attack another knight using standard chess knight moves."
date: "2026-06-13T18:11:45+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1221
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 73 (Rated for Div. 2)"
rating: 1100
weight: 1221
solve_time_s: 206
verified: false
draft: false
---

[CF 1221B - Knights](https://codeforces.com/problemset/problem/1221/B)

**Rating:** 1100  
**Tags:** constructive algorithms, greedy  
**Solve time:** 3m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are filling an $n \times n$ chessboard where every cell must contain either a white knight or a black knight. After the board is filled, we look at all pairs of cells where a knight can attack another knight using standard chess knight moves. A “duel” is counted only when two conditions hold simultaneously: the two cells attack each other and the knights in those two cells have different colors.

So the task is not about placing pieces sparsely, but about coloring every cell in a way that maximizes how many attacking edges connect opposite colors. Each cell is a vertex in a graph, and edges connect pairs of cells a knight move apart. We are essentially trying to 2-color this fixed graph to maximize the number of edges that go between different colors.

The constraint $3 \le n \le 100$ implies the board has at most 10,000 cells, and each cell has at most 8 knight moves, so the graph has on the order of tens of thousands of edges. This rules out any exponential search or flow-based optimization. We need something that assigns colors in linear time over the grid.

A naive concern is that not all bipartitions behave the same on this graph because it is not bipartite. If it were bipartite, any valid 2-coloring would maximize cross edges automatically. Here, some cycles of odd length exist in the knight graph, so color choice matters. However, the key observation is that the graph is highly regular under a simple parity structure, which we can exploit.

A typical failure case for naive reasoning is to try alternating colors like a chessboard pattern. For small boards, this often works, but it is not guaranteed optimal because the knight graph does not respect parity of $i + j$. For example, from $(1,1)$ a knight can reach both even and odd parity squares, so strict checkerboard coloring does not align with adjacency structure.

## Approaches

A brute-force approach would treat each cell independently, assigning either W or B, and checking all $2^{n^2}$ configurations. For each configuration we would compute all knight edges and count how many connect opposite colors. This is immediately infeasible since even for $n = 10$, $2^{100}$ configurations already exceed any computational limit.

We can instead think in terms of local structure. Each edge contributes to the answer only if its endpoints have different colors. So we want to maximize the number of edges crossing the cut induced by the coloring. This is a maximum cut problem on the knight graph.

In general graphs, max cut is hard. But here the structure is geometric and symmetric. The key insight is that every knight move shifts coordinates by either $(\pm 1, \pm 2)$ or $(\pm 2, \pm 1)$. In both cases, the sum $i + j$ changes by exactly $\pm 3$, which preserves parity modulo 2. So every edge always connects cells of opposite parity in a checkerboard sense of $(i + j) \bmod 2$. This means the graph is already bipartite with respect to this parity.

Once we know the graph is bipartite, the maximum cut is achieved by coloring the two partitions differently. That ensures every edge contributes exactly once to the answer, which is optimal since no edge can contribute more than one duel.

So the optimal strategy is simply to assign one color to cells where $i + j$ is even and the other color to cells where it is odd.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^{n^2} \cdot n^2)$ | $O(n^2)$ | Too slow |
| Optimal | $O(n^2)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

1. For every cell $(i, j)$, compute the value $(i + j) \bmod 2$. This partitions the grid into two sets based on parity.
2. Assign color W to one parity class and B to the other, for example W when $(i + j) \bmod 2 = 0$ and B otherwise. This choice is arbitrary since swapping colors does not change the number of duels.
3. Output the resulting grid row by row.

The reason this works is that every valid knight move always connects two cells with different parity under $(i + j) \bmod 2$. Therefore, every edge in the knight graph goes between the two color classes, meaning every possible interaction is counted as a duel.

### Why it works

The invariant is that all knight edges are between cells of opposite $(i + j)$ parity. Since our coloring matches this partition exactly, every edge connects different colors. This makes the number of duels equal to the total number of knight edges, which is the maximum possible since no configuration can exceed counting all edges.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
for i in range(n):
    row = []
    for j in range(n):
        if (i + j) % 2 == 0:
            row.append('W')
        else:
            row.append('B')
    print("".join(row))
```

The implementation directly encodes the parity-based partition. The loop over all cells builds each row independently, ensuring $O(n^2)$ construction.

A subtle point is that we do not need to explicitly compute or store edges between cells. The structure of knight moves is fully handled by the parity observation, so the solution avoids graph construction entirely.

## Worked Examples

### Example 1: $n = 3$

We compute the coloring grid.

| Cell (i, j) | i+j | parity | color |
| --- | --- | --- | --- |
| (0,0) | 0 | even | W |
| (0,1) | 1 | odd | B |
| (0,2) | 2 | even | W |
| (1,0) | 1 | odd | B |
| (1,1) | 2 | even | W |
| (1,2) | 3 | odd | B |
| (2,0) | 2 | even | W |
| (2,1) | 3 | odd | B |
| (2,2) | 4 | even | W |

Output:

```
WBW
BWB
WBW
```

This confirms the alternating structure. Every knight move from a cell lands on a cell of opposite parity, so every possible interaction is maximized.

### Example 2: $n = 4$

We repeat the same construction.

| Cell | parity | color |
| --- | --- | --- |
| (0,0) | even | W |
| (0,1) | odd | B |
| (0,2) | even | W |
| (0,3) | odd | B |
| (1,0) | odd | B |
| (1,1) | even | W |
| (1,2) | odd | B |
| (1,3) | even | W |

This pattern extends consistently across the grid, confirming that no local adjustment is needed for boundary cells.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Each cell is processed once to determine its color |
| Space | $O(1)$ extra | Only output storage is used |

The constraints allow up to 10,000 cells, so a linear scan over the grid is trivial within limits. No adjacency structure is stored, keeping memory usage minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    n = int(input())
    out = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append('W' if (i + j) % 2 == 0 else 'B')
        out.append("".join(row))
    return "\n".join(out)

# provided sample
assert run("3\n") == "WBW\nBWB\nWBW"

# minimum size
assert run("3\n") != ""

# all same parity check structure consistency
assert run("4\n").split("\n")[0][0] == 'W'

# larger sanity
assert run("5\n").count('W') + run("5\n").count('B') == 25
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 | fixed pattern | correctness on sample structure |
| 4 | checkerboard grid | parity consistency |
| 5 | full coverage | no missing cells |

## Edge Cases

For $n = 3$, the smallest valid board, the parity pattern still works without modification. Every cell is assigned deterministically, and there are no boundary exceptions because coloring depends only on coordinates, not on available moves.

For larger boards like $n = 100$, the same rule scales uniformly. Even edge cells such as $(0,0)$ or $(n-1,n-1)$ follow the same parity logic. Since knight moves always preserve the bipartite structure, boundary position does not affect correctness, and the output remains optimal across the entire grid.
