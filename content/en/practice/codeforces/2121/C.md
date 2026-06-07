---
title: "CF 2121C - Those Who Are With Us"
description: "We are given a rectangular grid of integers. In one move, we pick a single row and a single column. Every cell that lies in that chosen row or that chosen column gets decreased by one, with the intersection cell counted only once."
date: "2026-06-08T03:47:17+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2121
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1032 (Div. 3)"
rating: 1200
weight: 2121
solve_time_s: 94
verified: true
draft: false
---

[CF 2121C - Those Who Are With Us](https://codeforces.com/problemset/problem/2121/C)

**Rating:** 1200  
**Tags:** greedy, implementation  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid of integers. In one move, we pick a single row and a single column. Every cell that lies in that chosen row or that chosen column gets decreased by one, with the intersection cell counted only once.

The task is to choose this row and column so that after performing this single operation, the largest value anywhere in the grid becomes as small as possible.

The key difficulty is that decreasing one row and one column affects a cross-shaped region, not a simple subarray. Every candidate choice of row and column changes many cells at once, and we must reason about how the maximum element behaves after this structured decrement.

The constraints allow up to $2 \cdot 10^5$ total cells across all test cases. That immediately rules out trying all $n \cdot m$ row and column pairs for every test case, since that would lead to roughly $O(n^2 m^2)$ behavior in the worst case, which is far too large. We need a method closer to linear or near-linear per test case.

A subtle edge case appears when the maximum value is unique. If the only maximum lies at a single cell, we can always pick its row and column, reducing it and potentially reducing the global maximum. But when multiple maximums exist in different rows and columns, a single operation might not cover all of them, and some maxima remain untouched. This distinction drives the entire solution.

## Approaches

A brute-force solution would try every pair $(r, c)$, simulate decreasing all cells in row $r$ and column $c$, and compute the resulting maximum. Each simulation costs $O(nm)$, and there are $O(nm)$ choices, leading to $O(n^2 m^2)$ in the worst case. This is completely infeasible.

The key observation is that we do not need to fully simulate each choice. We only care about whether the maximum value after the operation becomes either the original maximum or one less than it. Since every affected cell decreases by exactly one, the only way to reduce the global maximum is to ensure that all occurrences of the current maximum value are “covered” by the chosen row and column.

If a maximum cell is not in the selected row or column, it remains unchanged, so the maximum stays the same. If all maximum cells are covered, then every maximum cell decreases to at most max minus one, and the new answer becomes that value, unless a second-largest value remains unaffected and equals the original maximum minus one.

Thus the problem reduces to checking whether we can choose a row and column that cover all positions containing the global maximum. If yes, the answer is reduced; otherwise, it remains unchanged.

We refine this further. Suppose the maximum value appears at several cells. We attempt to pick a row and column such that every maximum occurrence lies either in that row or that column. If such a pair exists, the maximum decreases by one; otherwise, it stays the same.

The only candidates for $r$ and $c$ that matter are derived from the positions of maximum elements. We only need to examine rows and columns that appear in those positions, which keeps the search linear in the number of maximum cells.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2 m^2)$ | $O(1)$ | Too slow |
| Max-position filtering | $O(nm)$ | $O(nm)$ | Accepted |

## Algorithm Walkthrough

We solve each test case independently.

1. Scan the entire grid to find the maximum value.

This establishes the target level we are trying to eliminate or reduce.
2. Collect all coordinates where this maximum value appears.

These are the only cells that matter for deciding whether the operation can reduce the answer.
3. Try to determine whether there exists a row $r$ such that all maximum cells are either in row $r$ or lie in a single common column.

More precisely, for each candidate row containing at least one maximum, we check whether all remaining uncovered maxima share the same column.
4. To test a candidate row $r$, look at all maximum positions not in row $r$. If they exist, all of them must have the same column $c$. If this holds, we found a valid pair $(r, c)$.
5. If no such configuration exists, then it is impossible to cover all maximum cells with a single row and column, so at least one maximum remains unaffected.
6. If a valid pair exists, the final answer becomes maximum minus one. Otherwise, it remains the original maximum.

### Why it works

The operation only reduces cells that lie in one chosen row or column. Every maximum cell must be affected if we want to reduce the global maximum. A maximum cell is affected only if it lies in the chosen row or chosen column. Therefore, every maximum position must belong to the union of one row and one column.

If two maximum cells lie in different rows and different columns simultaneously, then no single row-column pair can cover both unless one of the rows is chosen as the main row and all remaining maxima share a single column. This is exactly the condition tested in the algorithm. The structure of coverage by a row plus a column fully characterizes feasibility, so checking this condition is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        grid = []
        mx = 0

        for _ in range(n):
            row = list(map(int, input().split()))
            grid.append(row)
            mx = max(mx, max(row))

        positions = []
        for i in range(n):
            for j in range(m):
                if grid[i][j] == mx:
                    positions.append((i, j))

        rows = set(i for i, _ in positions)
        cols = set(j for _, j in positions)

        ok = False

        # try fixing a row
        for r in rows:
            col_candidate = -1
            valid = True
            for i, j in positions:
                if i == r:
                    continue
                if col_candidate == -1:
                    col_candidate = j
                elif col_candidate != j:
                    valid = False
                    break
            if valid:
                ok = True
                break

        # try fixing a column if not already ok
        if not ok:
            for c in cols:
                row_candidate = -1
                valid = True
                for i, j in positions:
                    if j == c:
                        continue
                    if row_candidate == -1:
                        row_candidate = i
                    elif row_candidate != i:
                        valid = False
                        break
                if valid:
                    ok = True
                    break

        print(mx - 1 if ok else mx)

if __name__ == "__main__":
    solve()
```

The solution first extracts the maximum value and all its occurrences. It then tests whether those occurrences can be covered by a single row plus a single column in either orientation. The two-phase check corresponds exactly to choosing which of the two selected indices acts as the dominant row or column.

A common implementation pitfall is assuming that selecting a row and column that individually contain many maxima is enough. The constraint is stricter: all maxima outside the chosen row must align to a single column.

## Worked Examples

Consider a small grid:

Input:

```
1
3 3
2 1 2
1 2 1
2 1 2
```

The maximum is 2 and occurs at four corners. We test candidate rows.

| Step | Chosen row | Remaining max positions | Distinct columns | Valid |
| --- | --- | --- | --- | --- |
| 1 | 0 | (2,0), (2,2), (1,1), (2,0), (2,2) | 0,2,1 | No |

No row isolates remaining maxima into one column, so row-based covering fails. Column-based checking similarly fails because remaining maxima are spread across multiple rows and columns. Therefore output stays 2.

This trace shows that even though maxima are frequent, their geometric spread prevents a single cross from covering them.

Now consider:

Input:

```
1
2 3
5 1 5
1 1 1
```

Maximum is 5 at positions (0,0) and (0,2).

If we choose row 0, all maximums are already in that row, so the operation automatically covers them.

| Step | Row | Remaining max positions | Columns outside row | Valid |
| --- | --- | --- | --- | --- |
| 1 | 0 | none | none | Yes |

So answer becomes 4.

This confirms that when all maxima already lie in a single row, the operation trivially reduces the maximum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | We scan the grid once and then process only maximum positions |
| Space | $O(k)$ | We store positions of maximum elements |

The total number of cells across all test cases is bounded by $2 \cdot 10^5$, so a linear scan per test case is sufficient. The additional work on maximum positions is negligible in comparison.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    t = int(input())
    out_lines = []

    for _ in range(t):
        n, m = map(int, input().split())
        grid = []
        mx = 0
        for _ in range(n):
            row = list(map(int, input().split()))
            grid.append(row)
            mx = max(mx, max(row))

        positions = [(i, j)
                     for i in range(n)
                     for j in range(m)
                     if grid[i][j] == mx]

        rows = set(i for i, _ in positions)
        cols = set(j for _, j in positions)

        ok = False

        for r in rows:
            col_candidate = -1
            valid = True
            for i, j in positions:
                if i == r:
                    continue
                if col_candidate == -1:
                    col_candidate = j
                elif col_candidate != j:
                    valid = False
                    break
            if valid:
                ok = True
                break

        if not ok:
            for c in cols:
                row_candidate = -1
                valid = True
                for i, j in positions:
                    if j == c:
                        continue
                    if row_candidate == -1:
                        row_candidate = i
                    elif row_candidate != i:
                        valid = False
                        break
                if valid:
                    ok = True
                    break

        out_lines.append(str(mx - 1 if ok else mx))

    return "\n".join(out_lines)

# provided sample (partial check placeholder)
assert run("""1
1 1
1
""") == "0"

# custom cases
assert run("""1
2 2
1 2
3 4
""") == "3", "no max coverage change"

assert run("""1
1 3
5 5 5
""") == "4", "all maxima in one row"

assert run("""1
3 3
2 1 2
1 2 1
2 1 2
""") == "2", "spread maxima cannot be covered"

assert run("""1
2 3
5 1 5
1 1 1
""") == "4", "row covers all maxima"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single cell | 0 | minimal case |
| all equal row | 4 | full row coverage |
| scattered maxima | 2 | impossible coverage |
| row + column structure | 4 | constructive success |

## Edge Cases

A key edge case is when every cell is already maximum. In that case, picking any row and column still leaves many unaffected cells, but all are reduced uniformly, so the maximum decreases by exactly one. The algorithm handles this because all maximum positions lie in every row, so any row-based check immediately succeeds.

Another edge case is when maximum positions form an L-shape. For example, maxima at (0,0), (0,1), (1,0). No single row or column covers all of them simultaneously. The algorithm detects this because after fixing any row or column, the remaining positions still split across multiple rows and columns, causing the check to fail.

A final subtle case is when there is exactly one maximum cell. Any chosen row and column that includes it will succeed immediately, and the answer correctly becomes maximum minus one.
