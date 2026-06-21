---
title: "CF 105895M - \u732b\u5a18\u90e8\u7f72"
description: "We are given a small grid, up to 8 by 8, where each cell is either allowed or forbidden. Allowed cells contain a cat and are marked with a character like Y, while forbidden cells are marked with N."
date: "2026-06-21T15:15:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105895
codeforces_index: "M"
codeforces_contest_name: "The 21st Southeast University Programming Contest (Summer)"
rating: 0
weight: 105895
solve_time_s: 46
verified: true
draft: false
---

[CF 105895M - \u732b\u5a18\u90e8\u7f72](https://codeforces.com/problemset/problem/105895/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small grid, up to 8 by 8, where each cell is either allowed or forbidden. Allowed cells contain a cat and are marked with a character like `Y`, while forbidden cells are marked with `N`. The task is to place as many catgirls as possible on allowed cells, under the restriction that no two placed catgirls are adjacent horizontally or vertically.

This is fundamentally a maximum independent set problem on a grid graph with some vertices removed. Each cell is a vertex if it is usable, and edges connect orthogonally adjacent cells. We want to pick the largest subset of usable vertices such that no edge has both endpoints selected.

The constraint n, m ≤ 8 is the key structural signal. The grid has at most 64 cells, which immediately rules out general exponential search over all subsets of cells without pruning. A naive subset enumeration would consider up to 2^64 states, which is far too large even with aggressive pruning. At the same time, the small width strongly suggests a profile dynamic programming or bitmask DP over rows or columns.

A subtle case that breaks greedy intuition is when local optimal placements block future dense regions. For example, in a 2x3 all-`Y` grid, placing greedily in a checkerboard pattern might miss configurations that shift density between rows.

Another corner case is when all cells are `N` except a sparse structure like a diagonal. Any solution must respect that adjacency is only horizontal and vertical, so diagonal placements do not interfere and should all be allowed.

## Approaches

A brute-force method would try all subsets of grid cells and check validity by scanning all pairs or checking adjacency constraints. This is conceptually simple: pick a subset, verify that no two selected cells are adjacent, and count the size if valid. The correctness is straightforward because it directly encodes the definition of the problem.

However, the number of subsets grows as 2^(n·m). In the worst case of a 8×8 grid, this is 2^64, which is completely infeasible. Even if validity checking is O(64) per subset, the total work is astronomically large.

The key observation is that adjacency is local and the grid is narrow. Instead of deciding all cells independently, we process row by row and encode each row selection as a bitmask. A valid configuration for a row is one where no two selected cells are adjacent horizontally. Then compatibility between consecutive rows enforces that vertically adjacent cells are not both chosen.

This transforms the problem into a profile DP over rows, where each state is a valid bitmask for a row, and transitions depend only on adjacent rows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | O(2^(nm) · nm) | O(nm) | Too slow |
| Row DP with bitmask states | O(n · 2^m · 2^m) | O(2^m) | Accepted |

## Algorithm Walkthrough

We treat each row independently and represent selections in a row using a bitmask of length m. A bit is 1 if we place a catgirl in that column.

1. For each row, enumerate all bitmasks from 0 to 2^m − 1 and keep only those that are valid within the row. A mask is valid if it does not place two catgirls in adjacent columns, meaning no two consecutive bits are 1, and it only places catgirls on cells that contain `Y`. This ensures we never violate horizontal adjacency or place on forbidden cells.
2. Precompute, for every row, which masks are compatible with that row’s grid constraints. We store for each row a list of valid masks and their corresponding counts of selected cells.
3. Define DP where dp[row][mask] is the maximum number of catgirls we can place up to this row if we choose configuration mask for this row.
4. Initialize dp for row 0 by setting dp[0][mask] to the number of set bits in mask for all valid masks.
5. For each subsequent row, transition from every valid previous mask to every valid current mask, but only if the two masks do not overlap vertically. This means no column has a 1 in both masks, because that would place catgirls in adjacent rows in the same column.
6. Update dp[row][cur_mask] as the maximum over all compatible previous masks of dp[row-1][prev_mask] plus the popcount of cur_mask.
7. The answer is the maximum value over all dp[last_row][mask].

The reason we can do this efficiently is that each row depends only on the previous row, so the state collapses to a manageable 2^m space rather than exponential over all cells.

### Why it works

The DP state fully captures the only relevant history needed for future decisions, which is the chosen configuration of the previous row. Any earlier rows affect the future only through their contribution to the total count, already stored in the DP value. The compatibility check enforces that no vertical or horizontal adjacency violations occur, so every transition preserves validity. Since every valid global placement corresponds to exactly one sequence of row masks, and all such sequences are considered, the maximum is guaranteed to be found.

## Python Solution

```python
import sys
input = sys.stdin.readline

def valid_masks(row_str, m):
    masks = []
    for mask in range(1 << m):
        ok = True
        for j in range(m):
            if (mask >> j) & 1:
                if row_str[j] == 'N':
                    ok = False
                    break
                if j > 0 and (mask >> (j - 1)) & 1:
                    ok = False
                    break
        if ok:
            cnt = bin(mask).count("1")
            masks.append((mask, cnt))
    return masks

def solve():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    row_masks = [valid_masks(grid[i], m) for i in range(n)]

    prev = {0: 0}

    for i in range(n):
        curr = {}
        for cmask, ccnt in row_masks[i]:
            best = 0
            for pmask, pval in prev.items():
                if pmask & cmask == 0:
                    best = max(best, pval + ccnt)
            curr[cmask] = max(curr.get(cmask, 0), best)
        prev = curr

    print(max(prev.values()))

if __name__ == "__main__":
    solve()
```

The solution builds, for each row, all configurations that respect horizontal adjacency and avoid forbidden cells. The DP dictionary `prev` stores the best achievable value for each mask of the previous row.

The transition checks `pmask & cmask == 0`, which enforces vertical adjacency constraints column by column. If both rows place a catgirl in the same column, they would be adjacent vertically, which is forbidden.

The dictionary-based DP avoids iterating over invalid states entirely, which keeps implementation simple given the small constraints. Since m ≤ 8, the number of masks is at most 256 per row, which is very manageable.

## Worked Examples

Consider a small 3×3 grid:

```
YYY
YNY
YYY
```

We track DP per row.

### Row 0

| mask | valid | count | dp |
| --- | --- | --- | --- |
| 000 | yes | 0 | 0 |
| 001 | yes | 1 | 1 |
| 010 | yes | 1 | 1 |
| 100 | yes | 1 | 1 |
| 101 | yes | 2 | 2 |
| 110 | yes | 2 | 2 |

### Row 1 (middle row has center blocked)

Valid masks exclude any with center bit set.

| mask | valid | count |
| --- | --- | --- |
| 000 | yes | 0 |
| 001 | yes | 1 |
| 010 | no | - |
| 100 | yes | 1 |
| 101 | yes | 2 |
| 110 | no | - |

Transition combines compatible masks. For example, mask 101 in row 1 cannot pair with row 0 mask 101 because of column overlap, but can pair with 010 or 001 depending on constraints.

The DP evolves by taking maximum compatible sums.

### Row 2

Same as row 0, but transitions depend only on row 1 results.

This trace shows that decisions are localized per row and conflicts only arise through column overlaps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · 4^m) | For each row, we try all valid masks against all previous masks, each up to 2^m |
| Space | O(2^m) | We store DP only for previous row states |

Since m ≤ 8, 4^m ≤ 65536, and n ≤ 8, the total work is small enough for a 2 second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def valid_masks(row_str, m):
        masks = []
        for mask in range(1 << m):
            ok = True
            for j in range(m):
                if (mask >> j) & 1:
                    if row_str[j] == 'N':
                        ok = False
                        break
                    if j > 0 and (mask >> (j - 1)) & 1:
                        ok = False
                        break
            if ok:
                cnt = bin(mask).count("1")
                masks.append((mask, cnt))
        return masks

    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    row_masks = [valid_masks(grid[i], m) for i in range(n)]

    prev = {0: 0}
    for i in range(n):
        curr = {}
        for cmask, ccnt in row_masks[i]:
            best = 0
            for pmask, pval in prev.items():
                if pmask & cmask == 0:
                    best = max(best, pval + ccnt)
            curr[cmask] = max(curr.get(cmask, 0), best)
        prev = curr

    return str(max(prev.values()))

# provided sample (structure inferred)
assert run("4 4\nYYYY\nYYNN\nNYNY\nYYYY\n") == "7"

# all blocked
assert run("2 2\nNN\nNN\n") == "0"

# single row all valid
assert run("1 5\nYYYYY\n") == "3"

# checkerboard free placement
assert run("3 3\nYYY\nYYY\nYYY\n") == "5"

# sparse diagonal
assert run("3 3\nYNN\nNYN\nNNY\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all N grid | 0 | empty feasibility |
| single row | max independent set in line | horizontal constraint |
| full grid | dense packing with conflicts | DP correctness |
| diagonal | no adjacency interaction | vertical/horizontal separation |

## Edge Cases

A fully blocked grid is handled cleanly because every row only has the mask 0 as valid. The DP never grows beyond zero and returns 0.

A single row grid reduces to selecting non-adjacent cells in a line. The row mask generation enforces no consecutive bits, so the DP collapses correctly to a 1D maximum independent set.

A diagonal pattern like

```
YNN
NYN
NNY
```

ensures that vertical adjacency never triggers. Each row independently allows a single placement, and since column overlap never occurs, DP accumulates all three placements.
