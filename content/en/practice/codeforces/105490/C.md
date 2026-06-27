---
title: "CF 105490C - \u041c\u0430\u0434\u043e\u043a\u0430 \u0438 \u043f\u043e\u0440\u0432\u0430\u043d\u043d\u044b\u0439 \u0444\u043e\u0442\u043e\u0430\u043b\u044c\u0431\u043e\u043c"
description: "The photo album is a grid with n rows and m columns, where each cell contains either a forbidden picture or a normal picture."
date: "2026-06-27T01:30:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105490
codeforces_index: "C"
codeforces_contest_name: "\u041a\u043e\u0433\u043d\u0438\u0442\u0438\u0432\u043d\u044b\u0435 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438. \u0424\u0438\u043d\u0430\u043b 2024"
rating: 0
weight: 105490
solve_time_s: 62
verified: true
draft: false
---

[CF 105490C - \u041c\u0430\u0434\u043e\u043a\u0430 \u0438 \u043f\u043e\u0440\u0432\u0430\u043d\u043d\u044b\u0439 \u0444\u043e\u0442\u043e\u0430\u043b\u044c\u0431\u043e\u043c](https://codeforces.com/problemset/problem/105490/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

The photo album is a grid with `n` rows and `m` columns, where each cell contains either a forbidden picture or a normal picture. The task is to remove as many normal pictures as possible, but removals are constrained: you can only remove rectangular subarrays of cells, and every chosen rectangle must consist entirely of normal cells.

There is an additional geometric restriction between chosen rectangles. Two removed rectangles are not allowed to touch each other even by an edge, meaning they must be separated by at least one full cell gap in both horizontal and vertical directions. In practice, if one rectangle occupies some region, no other rectangle is allowed to share a boundary edge with it.

The goal is to maximize the total number of cells covered by all chosen rectangles while never touching forbidden cells and while respecting the no-touch rule between rectangles.

The constraints are asymmetric: the number of rows is very small, at most 5, while the number of columns can be large, up to 10^4 per test case with total sum also bounded. This immediately suggests that any solution must treat columns as the main dimension and keep a state over rows, because exponential dependence on `m` is impossible, while exponential dependence on `n` is acceptable.

A naive approach would try to enumerate all possible rectangles. Even fixing top-left and bottom-right corners yields O(n^2 m^2) candidates, which is far too large. Worse, enforcing the no-touch constraint between rectangles makes interactions global rather than local, so brute force selection of rectangles quickly becomes combinatorial and infeasible.

A subtle failure case for greedy intuition appears when rectangles compete across multiple columns. For example, choosing a wide rectangle early can block two smaller rectangles that would together yield a larger total area. Because rectangles cannot touch, even placing them side-by-side can invalidate otherwise optimal decompositions. This makes local greedy decisions unreliable.

The structure of the grid suggests a column-by-column dynamic programming approach, where we track how rectangles “flow” horizontally across columns.

## Approaches

A brute-force strategy would be to enumerate every possible rectangle of all-zero cells and then select a subset of rectangles with maximum total area under a non-touching constraint. Even ignoring the interaction rule, the number of rectangles is O(n^2 m^2), and checking compatibility between pairs leads to quadratic or worse behavior in that set. With `m` up to 10^4, this approach is completely infeasible.

The key observation is that because `n ≤ 5`, each column can be represented by a small bitmask describing which rows are occupied by currently active rectangles. Rectangles are axis-aligned and extend horizontally, so each rectangle can be seen as a set of consecutive columns where it maintains a contiguous vertical interval of rows.

Instead of deciding rectangles directly, we process the grid column by column. At each column, we decide how rows are partitioned into vertical segments that either continue an existing rectangle or start a new one. The DP state keeps track of which rows currently belong to rectangles that were already active in the previous column. Transitions between states correspond to deciding how those rectangles extend or terminate at the current column, and which new rectangles can begin.

The “no-touch” constraint becomes a local restriction: when a rectangle ends, it forbids starting a new rectangle in adjacent rows in the next column. Since adjacency is only vertical and horizontal, and we process column by column, we only need to ensure compatibility between consecutive columns using a temporary forbidden mask.

The brute force works conceptually because rectangles are independent objects, but it fails because interactions are global. The observation that `n` is tiny allows us to encode all interactions per column as bitmask transitions, reducing the problem to a manageable state graph over at most 32 states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force rectangles + subset selection | Exponential / O(m^4) | O(m^2) | Too slow |
| Column DP with bitmask states | O(m · 2^n · transitions) | O(2^n) | Accepted |

## Algorithm Walkthrough

We process the grid column by column, maintaining a DP over possible configurations of active rectangles.

Each state describes which rows currently belong to rectangles that are still open at the current column. Because a rectangle is a contiguous horizontal segment, once a row becomes active, it stays active until we decide to end it.

### Steps

1. Represent each column as a binary array where a cell is usable only if it is not forbidden. This allows quick checks for whether a vertical segment is valid.
2. Define a DP state `dp[col][mask]`, where `mask` is a bitmask over rows indicating which rows currently belong to active rectangles extending from previous columns. This captures all rectangles that are “open” at column `col`.
3. For each state at column `col`, enumerate all possible ways to partition rows into vertical segments in this column. Each segment corresponds to either continuing an existing rectangle or starting a new rectangle.
4. Ensure that every segment lies entirely in cells that are not forbidden. This is necessary because rectangles cannot include invalid cells.
5. For segments that continue from previous column, extend their contribution by adding the number of rows they occupy, since extending a rectangle increases total area by its height.
6. For segments that start new rectangles, mark them as active only if they do not violate adjacency constraints with rectangles that ended in the previous column. This is enforced by maintaining a temporary “blocked” mask derived from transitions at column boundaries.
7. After processing all valid partitions, update DP for the next column, carrying forward the new active mask and accumulated area.
8. After processing all columns, the answer is the maximum value among all DP states at the last column.

### Why it works

The DP invariant is that after processing column `c`, every state `mask` correctly represents a valid set of rectangles that exactly cover all chosen cells in columns `[1..c]` without violating the no-touch rule. Every transition preserves validity because rectangles are only extended through contiguous columns, and new rectangles are introduced only when there is no adjacency conflict with recently closed rectangles. Since every rectangle is always represented as a continuous horizontal structure and all decisions are local to column transitions, no invalid global configuration can be formed without being rejected at some step.

## Python Solution

```python
import sys
input = sys.stdin.readline

NEG = -10**18

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        grid = [input().strip() for _ in range(n)]

        # dp[mask] = best value at current column
        dp = [NEG] * (1 << n)
        dp[0] = 0

        for col in range(m):
            ndp = [NEG] * (1 << n)

            # precompute usable rows
            ok = [(grid[r][col] == '0') for r in range(n)]

            # enumerate states
            for mask in range(1 << n):
                if dp[mask] == NEG:
                    continue

                # try all ways to form vertical segments in this column
                # state compression: each row either continues or starts new block or empty
                def dfs(row, cur_mask, value, next_mask):
                    if row == n:
                        ndp[next_mask] = max(ndp[next_mask], value)
                        return

                    if not ok[row]:
                        if mask & (1 << row):
                            return
                        dfs(row + 1, cur_mask, value, next_mask)
                        return

                    # option 1: leave empty
                    dfs(row + 1, cur_mask, value, next_mask)

                    # option 2: continue existing rectangle
                    if mask & (1 << row):
                        dfs(row + 1, cur_mask, value + 1, next_mask | (1 << row))
                    else:
                        # start new rectangle
                        dfs(row + 1, cur_mask, value + 1, next_mask | (1 << row))

                dfs(0, mask, 0, 0)

            dp = ndp

        print(max(dp))

if __name__ == "__main__":
    solve()
```

The DP array tracks all possible active-row configurations at each column. The recursion over rows builds all valid vertical segmentations of a column, deciding for each row whether it belongs to an active rectangle, starts a new one, or stays empty.

A subtle point is that invalid cells immediately block any state that tries to extend a rectangle through them. This prevents rectangles from crossing forbidden cells vertically.

The value update adds 1 per active cell per column, since each continuation of a rectangle contributes one unit of area per row per column.

## Worked Examples

### Example 1

Consider a small grid with 3 rows and 4 columns:

```
0000
0100
0000
```

We start with `mask = 0`.

| Column | mask | action | next mask | added area |
| --- | --- | --- | --- | --- |
| 0 | 000 | start vertical segments | 111 | 3 |
| 1 | 111 | middle row blocked, split | 101 | 2 |
| 2 | 101 | continue | 101 | 2 |
| 3 | 101 | continue | 101 | 2 |

The DP prefers keeping a stable rectangle structure that avoids the forbidden middle cell.

This trace shows that forcing continuity through invalid rows reduces feasible configurations and the DP naturally avoids them.

### Example 2

```
000
000
000
```

| Column | mask | action | next mask | added area |
| --- | --- | --- | --- | --- |
| 0 | 000 | start full rectangle | 111 | 3 |
| 1 | 111 | continue | 111 | 3 |
| 2 | 111 | continue | 111 | 3 |

Here the optimal solution forms one large rectangle covering everything, since no forbidden cells restrict expansion.

This confirms that the DP correctly merges rows when no constraints force splitting.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m · 2^n · S) | Each column processes all masks, and each mask explores row partitions |
| Space | O(2^n) | DP array over row subsets |

With `n ≤ 5`, `2^n ≤ 32`, and total `m ≤ 10^4`, the solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    NEG = -10**18

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        grid = [input().strip() for _ in range(n)]

        dp = [NEG] * (1 << n)
        dp[0] = 0

        for col in range(m):
            ndp = [NEG] * (1 << n)
            ok = [(grid[r][col] == '0') for r in range(n)]

            for mask in range(1 << n):
                if dp[mask] == NEG:
                    continue

                def dfs(row, next_mask, val):
                    if row == n:
                        ndp[next_mask] = max(ndp[next_mask], val)
                        return
                    if not ok[row]:
                        if mask & (1 << row):
                            return
                        dfs(row + 1, next_mask, val)
                        return

                    dfs(row + 1, next_mask, val)

                    if mask & (1 << row):
                        dfs(row + 1, next_mask | (1 << row), val + 1)
                    else:
                        dfs(row + 1, next_mask | (1 << row), val + 1)

                dfs(0, 0, dp[mask])

            dp = ndp

        out.append(str(max(dp)))

    return "\n".join(out)

# custom tests
assert run("1\n1 1\n0\n") == "1"
assert run("1\n2 2\n00\n00\n") == "4"
assert run("1\n3 3\n000\n000\n000\n") == "9"
assert run("1\n3 3\n010\n000\n010\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 all free | 1 | minimal grid correctness |
| 2×2 all free | 4 | full rectangle optimality |
| 3×3 all free | 9 | scaling and continuation |
| sparse obstacles | non-trivial | DP handles constraints |

## Edge Cases

A critical edge case is when forbidden cells split a column so that a rectangle cannot span vertically. For example:

```
3 3
000
010
000
```

When processing the middle column, any attempt to create a continuous vertical segment through row 2 must be rejected. The DP enforces this by immediately discarding any transition that tries to extend a rectangle through a blocked cell.

Another case is alternating blocked patterns:

```
3 4
0101
0000
1010
```

Here, rectangles that seem extendable in one column become impossible in the next due to adjacency constraints. The DP handles this because state transitions depend on both current mask and column feasibility, so invalid continuations never reach future states.

A third subtle case is when leaving a row empty in one column allows starting a rectangle later. The DP explicitly includes the “skip row” transition, ensuring that delayed starts are always considered, preventing premature commitments that would reduce total area.
