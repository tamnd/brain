---
title: "CF 102448I - Ivan and the swimming pool"
description: "We have an (N times M) grid. Each cell contains the maximum depth that can be excavated at that location before hitting rock. We must choose exactly (S) cells to form the pool. The chosen cells must be connected through shared sides, and the pool has one uniform depth."
date: "2026-08-09T14:31:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102448
codeforces_index: "I"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2020"
rating: 0
weight: 102448
solve_time_s: 597
verified: true
draft: false
---

[CF 102448I - Ivan and the swimming pool](https://codeforces.com/problemset/problem/102448/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an (N \times M) grid. Each cell contains the maximum depth that can be excavated at that location before hitting rock. We must choose exactly (S) cells to form the pool. The chosen cells must be connected through shared sides, and the pool has one uniform depth.

If a chosen cell allows excavation only to depth (7), the whole pool cannot be deeper than (7). Thus, for any connected set of (S) cells, its achievable depth is the minimum depth among those cells. The task is to maximize that minimum.

A useful way to think about a candidate depth (D) is to discard every cell whose value is smaller than (D). The remaining cells are precisely the places where a pool of depth (D) could be built. The question becomes whether these remaining cells contain a connected component with at least (S) cells.

The total number of cells is at most (10^6), so an algorithm that repeatedly examines the whole grid for many candidate depths is too expensive. There can be (10^6) different depth values, making an (O(NM)) scan for every possible depth an (O((NM)^2)) algorithm, which would reach about (10^{12}) cell examinations in the worst case. We need something close to linear, apart from the cost of ordering the cells.

The dimensions themselves can also be very large. A grid with (N=M=1000) already contains (10^6) cells, and either dimension is allowed to be as large as (10^6). This rules out algorithms depending on (N^2), (M^2), or repeated full-grid traversals. The memory limit also means that storing large Python objects for every cell should be avoided when possible.

There are several edge cases where a superficially correct solution can fail.

For (S=1), no connectivity is needed beyond the single cell. For example,

```
1 1 1
42
```

has answer (42). A solution that always tries to connect a cell to a neighbor would incorrectly conclude that no pool exists.

Another important case is when high-valued cells are disconnected. Consider

```
2 1 3
10 1 10
```

The answer is (1), not (10). There are two cells of depth (10), but they are separated by the depth-(1) cell. A solution that simply takes the (S) largest values without considering connectivity would return the wrong result.

The opposite situation also matters. If a connected component contains more than (S) cells, we are allowed to use exactly (S) of them. For example,

```
3 1 5
8 8 8 8 8
```

has answer (8), even though the component contains five cells. A solution that requires a component to have exactly (S) cells would incorrectly reject it.

Finally, when (S=N\cdot M), every cell must belong to the pool. For example,

```
4 2 2
5 7
8 6
```

has answer (5), because the minimum depth over the entire grid is (5). A method that stops as soon as it finds a large high-valued region can miss the fact that the pool must contain every cell when (S) equals the entire grid size.

## Approaches

A direct approach is to try every possible pool depth. For a candidate depth (D), we keep only cells with value at least (D), run a flood fill over those cells, and check whether any connected component has at least (S) cells. This is correct because every cell in such a component can support depth (D), and any connected component with at least (S) cells contains a connected subset of exactly (S) cells.

The problem is the number of candidate depths. There can be as many as (NM) distinct values. A single flood fill takes (O(NM)) time in the worst case, so checking every distinct depth takes (O((NM)^2)). With (NM=10^6), that is potentially (10^{12}) cell visits.

We can improve the idea by processing depths from largest to smallest instead of independently checking every depth.

Suppose we have already activated every cell whose depth is at least (D). At that moment, the active cells form exactly the graph relevant to a pool of depth (D). When we decrease the threshold, newly activated cells are simply added to this graph. Connectivity only grows, so we never need to recompute any connected component from scratch.

This is precisely what a Disjoint Set Union structure is designed for. Each activated cell starts as its own component. Whenever an activated cell has an activated neighbor, we merge their components. The DSU stores the size of every component, so after activating a cell we can immediately check whether its component has reached size (S).

The first depth at which a component reaches size (S) is the answer. Processing in descending order means every previously activated cell has depth at least the current depth. Consequently, a component reaching size (S) at depth (D) gives a valid pool of depth (D), while no larger depth could have supported (S) connected cells because we would already have stopped earlier.

There is one Python-specific implementation detail worth handling carefully. The grid can contain (10^6) cells, so storing tuples such as `(depth, row, column)` creates substantial memory overhead. Instead, each cell is represented by one integer containing both its depth and its flattened cell index. Since (NM\le10^6<2^{20}), the lower 20 bits are enough for the index. The remaining bits store the depth. Python's built-in sort can then order these packed integers efficiently.

The DSU arrays are stored using `array('i')`, which uses four bytes per entry instead of Python's much larger per-integer object representation. The active cells are stored in a `bytearray`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O((NM)^2)) | (O(NM)) | Too slow |
| Optimal | (O(NM\log(NM))) | (O(NM)) | Accepted |

## Algorithm Walkthrough

1. Flatten the two-dimensional grid into indices from (0) to (NM-1). Store every cell as one packed integer containing its depth and flattened index. Sorting these integers in descending order gives us the cells from deepest to shallowest.
2. Create a DSU structure with one initially separate component for every cell. Also create an `active` array. A cell is active only after it has been reached in the descending sweep.
3. Process the cells in descending depth order. When a cell is encountered, activate it and make its component size equal to one.
4. Check the cell's four possible grid neighbors. For every neighbor that is already active, merge the two DSU components. We only merge active neighbors because an inactive neighbor has depth smaller than the current threshold and cannot belong to a pool of the current depth.
5. After all possible unions for the newly activated cell, inspect the size of its DSU component. If that size is at least (S), return the current cell's depth.
6. Continue until a component reaches (S) cells. Such a component consists entirely of cells whose depths are at least the reported value, and it is connected. Since it contains at least (S) cells, we can select exactly (S) connected cells from it.

Why does a connected component with more than (S) cells always contain a connected subset of exactly (S) cells? Start from any vertex and repeatedly add an adjacent vertex that belongs to the component. Because the component is connected, this process can continue until exactly (S) vertices have been selected.

The invariant behind the whole sweep is that immediately before processing depth (D), every active cell has depth at least (D), and the DSU components are exactly the connected components of those active cells. When the current cell is activated, only edges to already active neighbors need to be added, so the invariant remains true. Thus, when a component first reaches (S) cells, it represents a feasible pool at that depth. Because depths are processed from largest to smallest, the first such depth is maximal.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

SHIFT = 20
MASK = (1 << SHIFT) - 1

def solve():
    S, N, M = map(int, input().split())
    total = N * M

    # Pack (depth, index) into one integer.
    # The lower 20 bits store the index because total <= 10^6 < 2^20.
    cells = []
    append = cells.append

    idx = 0
    for _ in range(N):
        row = map(int, input().split())
        for depth in row:
            append((depth << SHIFT) | idx)
            idx += 1

    cells.sort(reverse=True)

    parent = array('i', range(total))
    size = array('i', [1]) * total
    active = bytearray(total)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        a = find(a)
        b = find(b)

        if a == b:
            return a

        if size[a] < size[b]:
            a, b = b, a

        parent[b] = a
        size[a] += size[b]
        return a

    for code in cells:
        depth = code >> SHIFT
        idx = code & MASK

        active[idx] = 1
        root = idx

        row = idx // M
        col = idx - row * M

        if row > 0:
            other = idx - M
            if active[other]:
                root = union(root, other)

        if row + 1 < N:
            other = idx + M
            if active[other]:
                root = union(root, other)

        if col > 0:
            other = idx - 1
            if active[other]:
                root = union(root, other)

        if col + 1 < M:
            other = idx + 1
            if active[other]:
                root = union(root, other)

        root = find(root)

        if size[root] >= S:
            print(depth)
            return

if __name__ == "__main__":
    solve()
```

The input is read row by row so that the program never creates one giant list of all input tokens. Each depth is immediately packed together with its flattened position and appended to `cells`.

The expression `(depth << SHIFT) | idx` stores two pieces of information in one integer. Since the largest possible number of cells is (10^6), 20 bits are enough for `idx`. Sorting the packed values in descending order consequently sorts primarily by depth, which is exactly the order required by the DSU sweep.

The `active` byte array is separate from the DSU. A DSU parent value alone cannot tell us whether a cell has already been activated, because every cell has a parent from the beginning. The byte array lets us test whether a neighbor belongs to the current threshold graph.

The grid is flattened row by row. For index `idx`, the cell above is `idx - M`, the cell below is `idx + M`, the left cell is `idx - 1`, and the right cell is `idx + 1`. The row and column checks prevent wrapping around the edges. In particular, checking `col > 0` before using `idx - 1` prevents the first cell of a row from incorrectly connecting to the previous row.

The DSU uses union by size and path compression. Both operations are effectively constant time amortized, more precisely (O(\alpha(NM))), where (\alpha) is the inverse Ackermann function.

The code checks the component size after all unions involving the current cell. This order matters because the cell may connect several previously separate components, and the final merged component is the one whose size must be compared with (S).

Python integers do not overflow, so the packed representation is safe. The largest packed value is below (10^8\cdot2^{20}+2^{20}), which is easily within Python's integer range.

## Worked Examples

### Sample 1

The input is

```
1 2 4
9 7 7 9
7 8 8 7
```

The flattened grid is `[9, 7, 7, 9, 7, 8, 8, 7]`. Since (S=1), the first activated cell already forms a valid component.

| Activated depth | Cell index | Component after unions | Largest relevant size | Decision |
| --- | --- | --- | --- | --- |
| 9 | 0 | `{0}` | 1 | Stop |

The first cell has depth (9), so the answer is (9).

This demonstrates the (S=1) boundary case. Connectivity with other cells is irrelevant because a single cell is already a connected set.

### Sample 2

The input is

```
2 2 4
9 7 7 9
7 8 8 7
```

Here (S=2). The two cells with depth (9) are indices (0) and (3), and they are not adjacent. The two cells with depth (8) are indices (6) and (5), and they are adjacent.

| Activated depth | Cell index | New unions | Component size containing cell | Decision |
| --- | --- | --- | --- | --- |
| 9 | 3 | none | 1 | Continue |
| 9 | 0 | none | 1 | Continue |
| 8 | 6 | none | 1 | Continue |
| 8 | 5 | (5\leftrightarrow6) | 2 | Stop |

When index (5) is activated, it is adjacent to index (6), so the two depth-(8) cells form a component of size (2). We have found a valid pool at depth (8).

The depth-(9) cells cannot produce a pool of size (2), because they belong to different components. This demonstrates why simply taking the largest values is insufficient and why connectivity must be maintained explicitly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(NM\log(NM))) | Sorting (NM) packed cell values dominates; all DSU operations are almost linear |
| Space | (O(NM)) | Packed cells, DSU arrays, and the active array each use linear space |

With at most (10^6) cells, the algorithm performs one sort and a constant number of DSU operations per cell. The Python implementation also avoids the large memory overhead of Python tuples and per-cell DSU integers by using packed integers and `array('i')`. This keeps the representation comfortably within the 256 MB memory limit while avoiding the repeated full-grid traversals that would make the naive approach too slow.

## Test Cases

```python
# The solution above is assumed to be available as solve().
# This helper redirects stdin/stdout so solve() can be tested directly.

import sys
import io
from contextlib import redirect_stdout

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    out = io.StringIO()
    try:
        with redirect_stdout(out):
            solve()
    finally:
        sys.stdin = old_stdin
        input = old_input

    return out.getvalue().strip()

# Provided samples
assert run(
    """1 2 4
9 7 7 9
7 8 8 7
"""
) == "9", "sample 1"

assert run(
    """2 2 4
9 7 7 9
7 8 8 7
"""
) == "8", "sample 2"

assert run(
    """3 2 4
9 7 7 9
7 8 8 7
"""
) == "7", "sample 3"

# Minimum-size input
assert run(
    """1 1 1
42
"""
) == "42", "single cell"

# S = 1 must choose the deepest individual cell
assert run(
    """1 2 3
5 1 9
1 1 1
"""
) == "9", "S=1"

# High cells exist, but they are disconnected.
assert run(
    """2 1 3
10 1 10
"""
) == "1", "disconnected high cells"

# All cells have the same depth, and S equals the entire grid.
assert run(
    """6 2 3
7 7 7
7 7 7
"""
) == "7", "all equal and S=NM"

# Maximum number of cells: 1 x 1,000,000.
# Every cell has the same depth, so the whole row is one component.
max_case = "1000000 1 1000000\n" + ("7 " * 1000000)
assert run(max_case) == "7", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 42` | 42 | Minimum grid size and single-cell pool |
| `1 2 3 / 5 1 9 / 1 1 1` | 9 | (S=1), so no connection is required |
| `2 1 3 / 10 1 10` | 1 | Prevents treating the (S) largest values as automatically connected |
| `6 2 3 / all 7` | 7 | All equal values and (S=N\cdot M) |
| `1000000 1 1000000 / all 7` | 7 | Maximum total number of cells and boundary-scale input |

## Edge Cases

The single-cell case is handled immediately when the first cell is activated. For

```
1 1 1
42
```

the cell has depth (42), becomes an active component of size (1), and since (S=1), the algorithm returns (42). No neighbor is required.

For disconnected high-valued cells, consider

```
2 1 3
10 1 10
```

The two depth-(10) cells are activated first, but neither has an active neighbor, so both components remain size (1). The depth-(1) middle cell is then activated and joins both sides, producing one component of size (3). At that point the component has size at least (S=2), so the answer is (1). The algorithm correctly rejects the tempting but invalid pair of isolated depth-(10) cells.

When a component is larger than (S), the algorithm deliberately checks `>= S` rather than `== S`. For

```
3 1 5
8 8 8 8 8
```

the first three adjacent cells already form a connected component of exactly three cells, so the algorithm returns (8). If more cells had been activated before the check, a component of size four or five would still be valid because we can take a connected subset of exactly three cells.

When (S=N\cdot M), the threshold cannot be accepted until every cell has been activated. For

```
4 2 2
5 7
8 6
```

the cells of depth (8), (7), and (6) are activated first, but their component has size only three. The final depth-(5) cell joins that component, making its size four. The algorithm then returns (5), which is exactly the minimum depth of the entire grid.

The grid boundary checks are also essential. In a row-major representation, the last cell of one row is numerically adjacent to the first cell of the next row, but those cells are not horizontally adjacent in the grid. The conditions on `col` prevent such false connections. Similarly, `row > 0` and `row + 1 < N` prevent vertical accesses outside the grid.

The descending order is what makes the first successful DSU component optimal. At depth (D), every active cell has capacity at least (D). If a component reaches (S), a pool of depth (D) exists. Any larger depth was processed earlier and failed to produce such a component, so no better answer was skipped.

This version is ready to use as a contest editorial. If you want, I can also produce a shorter Codeforces-style version focused on the core DSU insight and implementation.
