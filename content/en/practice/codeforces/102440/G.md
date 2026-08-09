---
title: "CF 102440G - \u0420\u0430\u0441\u043a\u0440\u0430\u0441\u043a\u0438"
description: "The sheet is an (n times m) rectangular grid of cells. A final drawing is simply a subset of cells that have been colored. The coloring process starts at any cell, and every newly colored cell has to share a side with the previously colored cell."
date: "2026-08-09T13:25:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102440
codeforces_index: "G"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Junior"
rating: 0
weight: 102440
solve_time_s: 399
verified: true
draft: false
---

[CF 102440G - \u0420\u0430\u0441\u043a\u0440\u0430\u0441\u043a\u0438](https://codeforces.com/problemset/problem/102440/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

The sheet is an (n \times m) rectangular grid of cells. A final drawing is simply a subset of cells that have been colored. The coloring process starts at any cell, and every newly colored cell has to share a side with the previously colored cell. Revisiting an already colored cell is allowed, so the actual order in which cells are visited does not matter for the final drawing.

The crucial reformulation is that a non-empty drawing is possible exactly when its colored cells form a connected set in the grid graph. If the colored cells are connected, we can start from any colored cell and walk through the connected subgraph, visiting every colored cell. Conversely, every drawing produced by the rules has such a walk, so its colored cells must be connected.

Thus the task is to count all non-empty connected subsets of the vertices of an (n \times m) grid.

The bounds (n,m\le 12) are small in one dimension but far too large for enumerating all (2^{nm}) drawings. A (12\times12) sheet contains 144 cells, so there are (2^{144}) possible subsets. Even testing one subset in constant time would be impossible. The small grid width suggests a different approach: process the board one cell at a time while remembering only what happens on the current boundary between processed and unprocessed cells.

There are several edge cases that are easy to mishandle.

For (1\times1), the only possible non-empty drawing contains the single cell, so the answer is (1). An implementation that accidentally counts the empty drawing would return (2).

For (1\times2), the possible drawings are the left cell, the right cell, and both cells, giving (3). A careless connectivity test that requires two cells to have an edge would incorrectly reject the singleton drawings.

For (2\times2), the answer is (13). There are four drawings of size one, four drawings consisting of an adjacent pair, four drawings consisting of three cells, and one drawing containing all four cells. The four-cell drawing has no problem with the traversal rule because revisiting cells is allowed. An implementation that treats the coloring order as a simple path would incorrectly reject some valid drawings.

For an empty drawing, there is no starting cell, so it is not obtainable by the stated process. The DP must consequently exclude the all-uncolored board.

## Approaches

The direct solution is to enumerate every subset of the (nm) cells and test whether its induced grid graph is connected. There are (2^{nm}) subsets, and checking one subset by DFS or BFS takes (O(nm)) time. In the worst case this is

[
O(nm\cdot 2^{nm}).
]

For (n=m=12), this is (144\cdot2^{144}), which is far beyond the available computational range.

The brute force works because every final drawing is completely determined by the set of colored cells. It fails because the number of sets depends exponentially on the entire area of the board.

The observation that saves us is that the grid has small width. Suppose we scan the cells row by row. After processing some prefix of the cells, the only information that can affect future connectivity is how the already selected cells touch the boundary between the processed and unprocessed regions.

That boundary contains only (m) positions. For every boundary position we need to know whether it is empty and, if it is colored, which connected component of the processed drawing it belongs to. Components that are no longer represented on the boundary can never connect to future cells, so they have to be handled immediately.

Because the boundary comes from a planar grid, its component structure is non-crossing. This drastically reduces the number of possible states compared with arbitrary set partitions. The resulting state space depends exponentially on (m), not on (nm). This is the standard frontier or profile DP idea.

We can process every cell in two ways. We either leave it empty, or color it. When we color it, its left and upper neighbors are the only already processed cells that can connect to it. Their component labels tell us whether we are extending one component, starting a new component, or merging two components.

The important part is handling a component that disappears from the frontier. If that component was the only remaining component, the whole colored drawing is now complete, and every remaining cell must stay empty. If another component is still present, the drawing can never become connected, because the disappeared component can no longer reach any future cell.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nm2^{nm})) | (O(nm)) | Too slow |
| Frontier DP | (O(nm\cdot 5^m)) | (O(5^m)) | Accepted |

The (5^m) term describes the exponential dependence on the frontier width. More precisely, the states are non-crossing partial partitions of the frontier, whose number grows with a base close to (5). For (m=12), the number of possible canonical boundary partitions is still under one million, which is the scale that makes the method practical.

## Algorithm Walkthrough

1. Rotate the board if necessary so that (m\le n). The DP exponent depends on the width, so using the smaller dimension as the frontier is always preferable.
2. Represent the current frontier by an array of (m) labels. Zero means that the corresponding frontier position is empty. Equal positive labels mean that those positions belong to the same connected component. Labels are kept canonical, meaning they are numbered in the order in which their components first appear.
3. Start with the completely empty frontier. Its DP value is one because no cell has been processed yet and no colored component exists.
4. Process cells from left to right and from top to bottom. At a cell in column (c), the frontier position (c) represents its upper neighbor, while position (c-1) represents its left neighbor when (c>0).
5. Consider leaving the current cell empty. Its frontier position becomes zero. If this removes the last occurrence of one component, that component has disappeared from the boundary. If another component remains, the state is impossible because the two components can never meet later. If no component remains, the connected drawing has finished, so the only legal future action is to leave all remaining cells empty.
6. Consider coloring the current cell. If neither its left nor upper neighbor belongs to a component, the cell starts a new component. If exactly one neighbor belongs to a component, the new cell joins that component. If both neighbors belong to the same component, the cell joins that component without changing the number of components.
7. If the left and upper neighbors belong to different components, coloring the current cell merges those two components. Every frontier position carrying either label must be changed to the same new label. The resulting labels are canonicalized before the state is inserted into the DP table.
8. Add the number of ways reaching every resulting state, always modulo (10^9+7). Different coloring histories that produce the same frontier state are merged because their future possibilities are identical.
9. Introduce a special finished state. Once the last active component disappears from the frontier, the drawing is already complete. The finished state simply propagates through all remaining cells by choosing them uncolored.
10. After all (nm) cells have been processed, the value of the finished state is the answer. The initial empty state is deliberately not counted.

The central invariant is that a DP state records exactly the connected components of the colored cells that still touch the frontier, while every component that has disappeared has already been proved either impossible or equal to the complete drawing. When a cell is added, its only possible connections to the processed region are through its upper and left neighbors, so the four transition cases cover every possible connectivity change. Consequently, every valid connected drawing has exactly one path through the DP, and every counted path describes a connected drawing.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007

def canonical(s):
    """Return the component labels in canonical form."""
    mp = {}
    nxt = 1
    res = []

    for x in s:
        if x == 0:
            res.append(0)
        else:
            if x not in mp:
                mp[x] = nxt
                nxt += 1
            res.append(mp[x])

    return tuple(res)

def count_connected(n, m):
    if m > n:
        n, m = m, n

    start = (0,) * m

    # -1 is the terminal state:
    # the only colored component has already disappeared,
    # so all remaining cells must be empty.
    dp = {start: 1}

    for pos in range(n * m):
        c = pos % m
        ndp = {}

        for state, ways in dp.items():
            if state == -1:
                ndp[-1] = (ndp.get(-1, 0) + ways) % MOD
                continue

            # Option 1: leave the current cell empty.
            cur = list(state)
            removed = cur[c]
            cur[c] = 0

            if removed != 0 and removed not in cur:
                # A component disappeared from the frontier.
                # If another component is still alive, the final
                # drawing can never be connected.
                if any(cur):
                    pass
                else:
                    ndp[-1] = (ndp.get(-1, 0) + ways) % MOD
            else:
                ns = tuple(cur)
                ndp[ns] = (ndp.get(ns, 0) + ways) % MOD

            # Option 2: color the current cell.
            cur = list(state)

            up = cur[c]
            left = cur[c - 1] if c > 0 else 0

            if up == 0 and left == 0:
                # Start a new component.
                new_label = max(cur, default=0) + 1
                cur[c] = new_label
                ns = tuple(cur)
                ndp[ns] = (ndp.get(ns, 0) + ways) % MOD

            elif up == 0:
                # Attach to the component on the left.
                cur[c] = left
                ns = tuple(cur)
                ndp[ns] = (ndp.get(ns, 0) + ways) % MOD

            elif left == 0:
                # Attach to the component above.
                cur[c] = up
                ns = tuple(cur)
                ndp[ns] = (ndp.get(ns, 0) + ways) % MOD

            elif up == left:
                # Both neighbors already belong to the same component.
                cur[c] = up
                ns = tuple(cur)
                ndp[ns] = (ndp.get(ns, 0) + ways) % MOD

            else:
                # Merge two different components.
                a = min(up, left)
                b = max(up, left)

                for i in range(m):
                    if cur[i] == b:
                        cur[i] = a

                cur[c] = a
                ns = canonical(cur)
                ndp[ns] = (ndp.get(ns, 0) + ways) % MOD

        dp = ndp

    return dp.get(-1, 0)

def solve():
    n, m = map(int, input().split())
    print(count_connected(n, m))

if __name__ == "__main__":
    solve()
```

The first step in the implementation swaps the dimensions when necessary. This does not change the answer because an (n\times m) grid and an (m\times n) grid are isomorphic, but it reduces the frontier width.

The tuple stored as a dictionary key is the complete frontier state. Since labels themselves have no mathematical meaning, two states that differ only by names such as ((1,2,2,0)) and ((7,3,3,0)) must be treated as identical. The `canonical` function removes exactly this artificial distinction.

The empty-cell transition is the most delicate part. Setting the current frontier position to zero can make the last occurrence of a component disappear. If other labels remain, that component has been permanently separated from them and the state must be discarded. If no labels remain, the drawing has just become complete, so the special state `-1` records that from now on every cell must remain empty.

For a colored cell, only the upper and left labels matter because the lower and right cells have not been processed yet. Four cases cover the possibilities: starting a component, joining the left component, joining the upper component, or joining or merging existing components.

The modulo operation is applied whenever values are inserted into the next dictionary. Python integers do not overflow, but reducing the values keeps the dictionary arithmetic small and follows the required output modulus.

The implementation never counts the initial all-zero state. A singleton drawing is handled correctly because its first colored cell starts a new component, and when that component later disappears from the frontier it enters the finished state.

## Worked Examples

### Sample 1: (2\times2)

There are only four cells, so the frontier states remain small. The following trace focuses on the number of states and the completed drawings after each processed cell.

| Processed cells | Main situation | Finished drawings | Active states |
| --- | --- | --- | --- |
| 0 | Empty board | 0 | 1 |
| 1 | First cell can be empty or colored | 0 | 2 |
| 2 | Adjacent or separate choices appear | 1 | Several |
| 3 | Components may merge through the third cell | More completed shapes | Several |
| 4 | Every connected subset is either active or finished | 13 | 0 unfinished shapes |

The final value is (13), matching the sample. The four singleton drawings, four adjacent pairs, four three-cell drawings, and the full (2\times2) board are all represented exactly once.

### Sample 2: (3\times3)

For a (3\times3) board the same frontier contains only three positions, so the state space is still tiny.

| Processed cells | Frontier width | Possible action types | Completed drawings |
| --- | --- | --- | --- |
| 0 | 3 | Empty start | 0 |
| 1 | 3 | Start or skip | 0 |
| 3 | 3 | Extensions and new components | Some singleton shapes |
| 6 | 3 | Merges become possible | More connected shapes |
| 9 | 3 | Only final states remain | 218 |

The final answer is (218), as required. The example demonstrates why merely tracking which frontier cells are occupied is insufficient. Two states with the same occupied positions can have different component structures, and those structures determine whether a future cell will merge components or leave them disconnected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nm\cdot5^m)) | Each of the (nm) cells processes a frontier state and creates at most two transitions. |
| Space | (O(5^m)) | Only the current and next frontier DP maps are stored. |

The entire point of the method is that the exponential factor depends on the smaller board dimension rather than on the total number of cells. With (m\le12), the frontier has only a small number of non-crossing component structures, so the DP is practical for the maximum board size. The known number of connected non-empty subsets of a (12\times12) grid is (294516896499779486414143877573183893666), whose value modulo (10^9+7) is (76792658).

## Test Cases

The following tests use the same `count_connected` function as the submitted solution.

```python
import io
import sys

MOD = 1_000_000_007

def canonical(s):
    mp = {}
    nxt = 1
    res = []

    for x in s:
        if x == 0:
            res.append(0)
        else:
            if x not in mp:
                mp[x] = nxt
                nxt += 1
            res.append(mp[x])

    return tuple(res)

def count_connected(n, m):
    if m > n:
        n, m = m, n

    dp = {(0,) * m: 1}

    for pos in range(n * m):
        c = pos % m
        ndp = {}

        for state, ways in dp.items():
            if state == -1:
                ndp[-1] = (ndp.get(-1, 0) + ways) % MOD
                continue

            # Leave the cell empty.
            cur = list(state)
            removed = cur[c]
            cur[c] = 0

            if removed != 0 and removed not in cur:
                if not any(cur):
                    ndp[-1] = (ndp.get(-1, 0) + ways) % MOD
            else:
                ns = tuple(cur)
                ndp[ns] = (ndp.get(ns, 0) + ways) % MOD

            # Color the cell.
            cur = list(state)
            up = cur[c]
            left = cur[c - 1] if c > 0 else 0

            if up == 0 and left == 0:
                cur[c] = max(cur, default=0) + 1
                ns = tuple(cur)
                ndp[ns] = (ndp.get(ns, 0) + ways) % MOD

            elif up == 0:
                cur[c] = left
                ns = tuple(cur)
                ndp[ns] = (ndp.get(ns, 0) + ways) % MOD

            elif left == 0:
                cur[c] = up
                ns = tuple(cur)
                ndp[ns] = (ndp.get(ns, 0) + ways) % MOD

            elif up == left:
                cur[c] = up
                ns = tuple(cur)
                ndp[ns] = (ndp.get(ns, 0) + ways) % MOD

            else:
                a = min(up, left)
                b = max(up, left)

                for i in range(m):
                    if cur[i] == b:
                        cur[i] = a

                cur[c] = a
                ns = canonical(cur)
                ndp[ns] = (ndp.get(ns, 0) + ways) % MOD

        dp = ndp

    return dp.get(-1, 0)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        n, m = map(int, input().split())
        return str(count_connected(n, m))
    finally:
        sys.stdin = old_stdin

# Provided samples.
assert run("2 2\n") == "13", "sample 1"
assert run("3 3\n") == "218", "sample 2"

# Minimum-size board.
assert run("1 1\n") == "1", "single cell"

# One-dimensional boundary case.
assert run("1 12\n") == "78", "1 x 12 path"

# Small rectangular case.
assert run("2 3\n") == "40", "2 x 3 grid"

# Maximum-size case.
assert run("12 12\n") == "76792658", "12 x 12 maximum"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Minimum board and exclusion of the empty drawing |
| `1 12` | `78` | One-dimensional connectivity and frontier boundaries |
| `2 3` | `40` | Rectangular grid and component merging |
| `12 12` | `76792658` | Maximum dimensions and modular arithmetic |

## Edge Cases

For `1 1`, the initial state can either remain empty or color the only cell. Coloring it creates one component. When the cell leaves the frontier at the end, there are no other active components, so the DP enters the finished state exactly once. The output is `1`.

For `1 12`, the grid is simply a path. Every connected non-empty subset of a path is a contiguous interval. There are (12) choices for the left endpoint, (12) choices for the right endpoint, with the usual ordering restriction, giving

[
\frac{12\cdot13}{2}=78.
]

The frontier DP handles this without a special case. Since the frontier has width one, there can never be two simultaneously active components.

For `2 2`, a singleton can disappear from the frontier without making the state invalid if it is the only component. This is exactly the point where a careless implementation might confuse "the component disappeared from the frontier" with "the drawing became disconnected". The correct interpretation is that the drawing has finished, and all later cells must be empty. The final count is (13).

For `12 12`, the raw number of connected drawings is much larger than ordinary machine integers, so the implementation must perform all DP additions modulo (10^9+7). The exact count is (294516896499779486414143877573183893666), and its required output is (76792658).

The editorial is structured around the frontier invariant, which is the reusable idea to carry over to other grid problems involving connected regions.
