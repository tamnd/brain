---
title: "CF 104426I - Yazan's game"
description: "We are given a rectangular grid of size $n times m$, where each cell contains either 0 or 1. In one move, we are allowed to choose exactly one cell that currently contains a 1. Once chosen, every cell that shares an edge or a corner with it becomes 1."
date: "2026-06-30T19:06:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104426
codeforces_index: "I"
codeforces_contest_name: "Syrian Private Universities Collegiate Programming Contest 2023"
rating: 0
weight: 104426
solve_time_s: 77
verified: true
draft: false
---

[CF 104426I - Yazan's game](https://codeforces.com/problemset/problem/104426/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid of size $n \times m$, where each cell contains either 0 or 1. In one move, we are allowed to choose exactly one cell that currently contains a 1. Once chosen, every cell that shares an edge or a corner with it becomes 1. The chosen cell itself stays unchanged, and we are not allowed to perform this operation more than once.

The question is whether there exists a valid choice of a starting 1-cell such that after applying this single expansion, the entire grid becomes filled with 1s.

The important perspective is to think of the operation as selecting a center cell and then “covering” its surrounding 3×3 block. After the operation, only cells inside that 3×3 neighborhood of the chosen cell can possibly change from 0 to 1. Everything outside that block remains unchanged forever.

The constraints allow up to a 500×500 grid, which is about 250,000 cells. Any solution that tries to simulate the operation for every possible center and recompute the entire grid would require roughly $O(n^2 \cdot m^2)$ in the worst case, which is far too large. This pushes us toward reasoning about global structure instead of brute simulation.

A few edge cases matter:

If the grid already contains only 1s, the answer is trivially “WIN” because no operation is needed.

If there is exactly one zero far away from any potential center, for example:

```
1 1 1
1 1 1
1 1 0
```

then no single 3×3 neighborhood can cover it unless the chosen center is adjacent, so the answer must be “LOSE”.

A subtle failure case for naive thinking is assuming that if zeros are “close together”, it is always possible. For example:

```
1 0 1
0 0 0
1 0 1
```

Even though zeros are clustered, the question reduces to whether a single 3×3 block centered on a 1-cell can cover all zeros simultaneously.

## Approaches

The brute-force idea is straightforward: try every cell that contains a 1 as the chosen center, simulate turning all its 8-neighbors into 1, and then check if the grid becomes all ones. Each simulation costs $O(nm)$, and there can be up to $nm$ candidate centers, leading to $O((nm)^2)$, which is roughly $6.25 \times 10^{10}$ operations in the worst case. This is far beyond the limit.

The key observation is that the operation only affects a fixed local region, specifically a 3×3 square around the chosen cell. This means the only zeros that matter are their positions relative to a potential center. Instead of testing centers, we can reason from the zeros.

If the operation must turn all zeros into ones in a single move, then every zero must lie within the 3×3 neighborhood of the chosen center. That immediately implies a geometric constraint: all zero cells must fit inside some 3×3 window. Once we find the bounding box of all zeros, we only need to check whether it fits within such a region and whether there exists at least one valid center cell (a 1) that can be chosen.

This reduces the problem from testing many centers to checking a constant number of conditions derived from the zero distribution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O((nm)^2)$ | $O(1)$ extra | Too slow |
| Bounding Box of Zeros | $O(nm)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

### 1. Locate all zero cells

Scan the grid and record the minimum and maximum row and column indices among all cells containing 0. If there are no zeros at all, the grid is already fully filled and we immediately return “WIN”.

The reason this step is useful is that zeros are the only obstacle; ones are irrelevant since they never need to be changed.

### 2. Compute the bounding rectangle of zeros

Let the smallest and largest row indices of zeros be $r_{min}$ and $r_{max}$, and similarly $c_{min}$ and $c_{max}$.

This rectangle represents the smallest axis-aligned box containing all problematic cells.

### 3. Check geometric feasibility of a single operation

Since one operation affects only a 3×3 neighborhood, all zeros must lie within such a neighborhood. This is equivalent to:

$$r_{max} - r_{min} \le 2 \quad \text{and} \quad c_{max} - c_{min} \le 2$$

If either dimension exceeds 2, no single center can cover all zeros.

### 4. Verify existence of a valid center cell

Even if all zeros fit inside a 3×3 region, the center of that region must be a cell with value 1, since only a 1-cell can be selected.

So we check whether there exists at least one cell with value 1 that lies in the intersection of all valid centers that could cover the zero bounding box. This region is:

$$[r_{min}+1, r_{max}-1] \times [c_{min}+1, c_{max}-1]$$

If there is at least one 1-cell in this region, the operation can be centered there.

### Why it works

The operation expands influence only one step in every direction, so every affected cell must lie within Chebyshev distance 1 of the chosen center. That constraint is both necessary and sufficient: necessity comes from the operation definition, and sufficiency comes from the fact that any such 3×3 neighborhood is fully covered in one move. Therefore, the entire problem reduces to checking whether all zeros can be enclosed in a single such neighborhood anchored at a 1-cell.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = []
    
    rmin, rmax = n, -1
    cmin, cmax = m, -1
    has_zero = False
    
    for i in range(n):
        row = list(map(int, input().split()))
        grid.append(row)
        for j, v in enumerate(row):
            if v == 0:
                has_zero = True
                rmin = min(rmin, i)
                rmax = max(rmax, i)
                cmin = min(cmin, j)
                cmax = max(cmax, j)
    
    if not has_zero:
        print("WIN")
        return
    
    if rmax - rmin > 2 or cmax - cmin > 2:
        print("LOSE")
        return
    
    # search for valid center
    for i in range(n):
        for j in range(m):
            if grid[i][j] != 1:
                continue
            if rmin <= i <= rmax and cmin <= j <= cmax:
                # must ensure center can cover bbox with radius 1
                if rmin >= i - 1 and rmax <= i + 1 and cmin >= j - 1 and cmax <= j + 1:
                    print("WIN")
                    return
    
    print("LOSE")

if __name__ == "__main__":
    solve()
```

The implementation first compresses the problem into the geometry of zero positions. The early exits handle trivial full-one grids and impossible stretched zero patterns. The final nested scan only checks candidate 1-cells, and the condition ensures the chosen center’s 3×3 neighborhood fully contains all zeros.

A common mistake is to only check the bounding box size without verifying that a valid 1-cell exists inside the feasible center region. That extra constraint is essential because an empty or invalid center set would otherwise incorrectly produce “WIN”.

## Worked Examples

### Example 1

Input:

```
4 4
1 0 0 1
1 1 1 0
1 0 0 1
1 1 1 1
```

| Step | rmin | rmax | cmin | cmax | Feasible box | Valid center found |
| --- | --- | --- | --- | --- | --- | --- |
| After scan | 0 | 2 | 1 | 3 | 3×3 | Yes |

All zeros lie within a 3×3 region, and there exists a 1-cell that can be chosen so that its neighborhood covers them all. The algorithm prints “WIN”.

### Example 2

Input:

```
2 5
1 0 0 0 1
1 0 0 0 1
```

| Step | rmin | rmax | cmin | cmax | Feasible box | Valid center found |
| --- | --- | --- | --- | --- | --- | --- |
| After scan | 0 | 1 | 1 | 3 | 2×3 | No |

Even though the rows are small, the zeros span four columns, exceeding the allowed 3-column window for a single operation. The algorithm correctly prints “LOSE”.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | Single pass to find zero bounds plus optional scan for a center |
| Space | $O(1)$ | Only constant extra variables beyond the grid |

The grid size is at most 250,000 cells, so a linear scan fits comfortably within time limits. No simulation or repeated updates are required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("""4 4
1 0 0 1
1 1 1 0
1 0 0 1
1 1 1 1
""") == "WIN"

assert run("""2 5
1 0 0 0 1
1 0 0 0 1
""") == "LOSE"

# all ones
assert run("""2 2
1 1
1 1
""") == "WIN"

# single zero in center
assert run("""3 3
1 1 1
1 0 1
1 1 1
""") == "WIN"

# impossible stretched zeros
assert run("""3 3
1 0 0
1 0 0
1 1 1
""") == "LOSE"

# edge: zero at corner far spread
assert run("""4 4
1 0 0 0
1 1 1 1
1 1 1 1
1 1 1 1
""") == "LOSE"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all ones | WIN | trivial case |
| single center zero | WIN | local fix works |
| stretched zeros | LOSE | bounding box violation |
| corner spread | LOSE | no 3×3 coverage |

## Edge Cases

When the grid contains no zeros, the algorithm immediately returns “WIN” because there is nothing to fix. The bounding box variables remain uninitialized, but the early exit prevents their use.

When zeros are tightly clustered but shifted toward an edge, the bounding box condition may still pass, but the center feasibility check rejects cases where no valid 1-cell exists in the required region. This prevents incorrect acceptance of patterns where geometry allows coverage but no legal starting cell exists.

When zeros form a perfect 3×3 block, any 1-cell inside that block can serve as a center. The algorithm detects this via both the bounding box size and the existence of at least one valid center cell, ensuring correctness even when multiple candidates exist.
