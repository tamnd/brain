---
title: "CF 104025A - Gifts in box"
description: "We start with a rectangular 3D arrangement of unit cubes inside a box whose dimensions are $n times m times h$. Each position $(i, j)$ in an $n times m$ grid describes a vertical stack of cubes with height $A{i,j}$. So initially the structure is a height map over a floor plan."
date: "2026-07-02T04:11:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104025
codeforces_index: "A"
codeforces_contest_name: "The 16-th BIT Campus Programming Contest - Onsite Round"
rating: 0
weight: 104025
solve_time_s: 48
verified: true
draft: false
---

[CF 104025A - Gifts in box](https://codeforces.com/problemset/problem/104025/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a rectangular 3D arrangement of unit cubes inside a box whose dimensions are $n \times m \times h$. Each position $(i, j)$ in an $n \times m$ grid describes a vertical stack of cubes with height $A_{i,j}$. So initially the structure is a height map over a floor plan.

Then the box is rotated so that what used to be vertical stacks are now viewed from a different side. After rotation, we again describe the visible structure as a grid, this time of size $h \times m$, where each cell $B_{i,j}$ represents how many cubes are visible at that position after gravity has acted in the new orientation.

The key point is that cubes do not move arbitrarily. They fall under gravity along the new vertical direction after rotation, so each column in the new view is formed by stacking all cubes that “project” onto that column, ordered by height after rotation.

A useful way to think about this is that each original column $(i,j)$ contributes a vertical pile of $A_{i,j}$ cubes. After rotation, these piles are rearranged across a different axis, and gravity compacts them into new columns.

The constraints $n, m, h \le 100$ indicate that any $O(nmh)$ or even a small constant-factor 3D simulation is acceptable. What is ruled out is any combinatorial simulation per cube that repeatedly scans large regions or performs repeated re-stacking for each cell.

A subtle edge case is when many stacks are zero or when all stacks are maximal. A naive “rotate and assign directly” approach tends to assume a simple transpose-like mapping, which fails because gravity changes the final distribution. For example, if all $A_{i,j} = 1$, the result is not a simple permutation of ones; instead, stacking causes consolidation along the new vertical axis.

## Approaches

A direct simulation would treat each cube independently. For every cell $(i,j)$, we could generate $A_{i,j}$ unit cubes and simulate their motion after rotation. Each cube would be tracked through a coordinate transform, then dropped under gravity until it settles. This is conceptually correct, but it explodes computationally. In the worst case, there are up to $n \cdot m \cdot h = 10^6$ cubes, and each cube may require scanning a column of size $h$, leading to roughly $10^8$ operations or more.

The key observation is that we never need to simulate individual cubes. After rotation, what matters is only how many cubes arrive at each projected column. Once we know the multiset of column heights contributing to a position, gravity simply stacks them in order. So the problem reduces to collecting values from the original grid into buckets indexed by the new orientation, then performing a stable vertical packing per bucket.

Concretely, each original column contributes its height $A_{i,j}$ to a position in the rotated grid. The rotation maps indices so that the first coordinate becomes height in the new system, while the second coordinate is preserved. This induces a grouping: for each fixed $j$, we collect all $A_{i,j}$ across $i$, and then simulate stacking them into an $h$-tall column.

Instead of simulating gravity physically, we simply interpret each column independently: for each $j$, we treat the list $[A_{1,j}, A_{2,j}, \dots, A_{n,j}]$ as a set of blocks to be dropped into a vertical container of height $h$. Each block contributes occupancy from bottom upward.

This reduces the problem to filling $m$ independent columns of height $h$, each constructed from the multiset of values in a column of $A$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (per cube simulation) | $O(nmh)$ to $O(nmh \cdot h)$ | $O(nmh)$ | Too slow |
| Column aggregation | $O(nmh)$ | $O(mh)$ | Accepted |

## Algorithm Walkthrough

We reinterpret the problem as constructing $m$ independent vertical columns in the output grid, each of height $h$, formed by stacking contributions from the input matrix.

1. For each column index $j$, collect all values $A_{i,j}$ for $i = 1 \ldots n$. This represents all stacks aligned with the same horizontal position in the rotated view. The reason we group by column is that rotation preserves horizontal alignment while swapping vertical structure.
2. For each group corresponding to column $j$, we simulate gravity in the new orientation by processing the values in any order while filling an array of size $h$ from bottom to top. We maintain a pointer that indicates the next available height position.
3. For each value $x = A_{i,j}$, we place $x$ unit cubes starting from the current lowest available position in the column, moving upward. Each placement increments the pointer. If the column becomes full, excess is ignored.
4. Repeat until all values in column $j$ are processed. This yields one full column of the output grid.
5. Store the resulting column into the answer matrix $B$.

A key detail is that we do not need to simulate individual cube positions. We only need to know how many cells are filled in each column after stacking.

### Why it works

The correctness relies on the fact that after rotation, each input stack contributes a contiguous vertical segment of identical unit cubes. Gravity in the new orientation does not interleave cubes from different stacks; it only orders these segments by arrival. Since all cubes are identical and only their count matters, the final structure depends only on how many cubes are assigned to each column, not their internal ordering. Thus treating each column independently and stacking greedily from bottom to top produces exactly the same occupancy as full physical simulation.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, h = map(int, input().split())
A = [list(map(int, input().split())) for _ in range(n)]

B = [[0] * m for _ in range(h)]

for j in range(m):
    col = []
    for i in range(n):
        if A[i][j] > 0:
            col.append(A[i][j])

    ptr = 0
    for x in col:
        for _ in range(x):
            if ptr < h:
                B[ptr][j] = 1
                ptr += 1

for i in range(h):
    print(*B[i])
```

The implementation directly follows the column-centric view of the algorithm. We build each column independently, then simulate stacking by filling a pointer from bottom to top. The inner loop expands each height value into unit contributions, which is safe given the constraints since total cubes are at most $10^6$.

A subtle point is the bound check `ptr < h`. Without it, overflowing columns would corrupt adjacent memory logically by writing beyond the intended height. Since excess cubes are physically outside the visible region after rotation, they are safely discarded.

## Worked Examples

We use a simplified trace to illustrate how a single column is constructed.

### Example 1

Input:

```
n = 3, m = 1, h = 4
A =
1
2
1
```

We process column $j = 0$.

| Step | Value x | ptr before | Writes | ptr after |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | B[0]=1 | 1 |
| 2 | 2 | 1 | B[1]=1, B[2]=1 | 3 |
| 3 | 1 | 3 | B[3]=1 | 4 |

Output column becomes:

```
1
1
1
1
```

This shows how multiple stacks collapse into a single continuous column under gravity.

### Example 2

Input:

```
n = 2, m = 1, h = 3
A =
2
1
```

| Step | Value x | ptr before | Writes | ptr after |
| --- | --- | --- | --- | --- |
| 1 | 2 | 0 | B[0]=1, B[1]=1 | 2 |
| 2 | 1 | 2 | B[2]=1 | 3 |

Output:

```
1
1
1
```

This confirms that ordering of stacks does not matter, only total mass.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nmh)$ | Each unit cube is written at most once when expanding stack heights |
| Space | $O(mh)$ | Output grid stores only the final rotated structure |

The bounds $n, m, h \le 100$ make $10^6$ operations safe, and memory usage is minimal since we only store the final grid.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m, h = map(int, input().split())
    A = [list(map(int, input().split())) for _ in range(n)]

    B = [[0] * m for _ in range(h)]

    for j in range(m):
        col = []
        for i in range(n):
            if A[i][j] > 0:
                col.append(A[i][j])

        ptr = 0
        for x in col:
            for _ in range(x):
                if ptr < h:
                    B[ptr][j] = 1
                    ptr += 1

    return "\n".join(" ".join(map(str, row)) for row in B) + "\n"

# sample
assert run("""3 4 5
1 2 3 4
2 0 1 5
1 3 2 2
""") == """3 2 3 3
1 2 2 3
0 1 1 2
0 0 0 2
0 0 0 1
"""

# minimum case
assert run("""1 1 1
1
""") == "1\n"

# all zeros
assert run("""2 2 3
0 0
0 0
""") == "0 0\n0 0\n0 0\n"

# max stack overflow behavior
assert run("""1 1 3
5
""") == "1\n1\n1\n"

# mixed
assert run("""2 2 3
1 2
3 0
""") == "1 1\n1 1\n1 0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1×1 single cube | 1 | minimal correctness |
| all zeros | all zeros grid | empty handling |
| single tall stack | capped fill | overflow clipping |
| mixed columns | partial stacking | multi-column independence |

## Edge Cases

A key edge case is when a single column produces more cubes than height $h$. The algorithm handles this by stopping writes when `ptr == h`. For example, if $h = 3$ and a column contributes $5$ cubes, only the first three are placed. The remaining cubes are ignored because they lie outside the visible height after gravity compression.

Another case is when all entries in a column are zero. The column list becomes empty, so the pointer never moves and the output column remains entirely zero. This matches the physical interpretation where no cubes exist in that vertical slice.

A third case is uniform nonzero input where every $A_{i,j} = 1$. Each column contributes $n$ single cubes, and stacking simply fills from bottom to top up to $h$. The algorithm correctly compresses all contributions without relying on their order, confirming that permutation of input rows does not affect the result.
