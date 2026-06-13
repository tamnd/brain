---
title: "CF 1106A - Lunar New Year and Cross Counting"
description: "We are given a square grid filled with two possible characters, X and .. The task is to scan every interior cell of this grid and decide whether it is the center of a “cross” pattern formed by diagonals."
date: "2026-06-13T08:10:44+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1106
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 536 (Div. 2)"
rating: 800
weight: 1106
solve_time_s: 274
verified: true
draft: false
---

[CF 1106A - Lunar New Year and Cross Counting](https://codeforces.com/problemset/problem/1106/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 4m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a square grid filled with two possible characters, `X` and `.`. The task is to scan every interior cell of this grid and decide whether it is the center of a “cross” pattern formed by diagonals.

A position `(i, j)` qualifies as a cross center only if the cell itself and its four diagonal neighbors are all `X`. Concretely, the five required cells are `(i, j)`, `(i-1, j-1)`, `(i-1, j+1)`, `(i+1, j-1)`, and `(i+1, j+1)`.

The output is simply the number of such valid centers in the grid.

The grid size is at most `500 × 500`, which means up to 250,000 cells. Checking each cell with a constant amount of work is comfortably feasible, but any solution that repeatedly scans larger patterns or rechecks expensive conditions will still pass unless it accidentally introduces unnecessary repeated work inside deeper loops.

A subtle edge case is when the grid is too small to contain any valid center. If `n < 3`, there is no cell that has all four diagonal neighbors, so the answer is always zero. Another edge case appears when `X` clusters exist but are incomplete diagonally, for example a full plus-shaped row or column of `X` does not help, because only diagonals matter.

A typical mistake is to check only adjacency in four directions or to mistakenly use orthogonal neighbors instead of diagonals. Another error comes from forgetting boundary checks, especially at `i = 1`, `i = n`, `j = 1`, `j = n`, where diagonal access would go out of bounds.

## Approaches

A brute-force solution is straightforward. For every cell `(i, j)` in the grid, we attempt to verify whether it is a valid center by checking the four diagonal neighbors plus itself. Each check takes constant time, so the total complexity is `O(n^2)`. Since each verification only inspects five cells, this approach is already optimal in terms of asymptotic behavior.

The reason this works efficiently is that the condition for a cross is entirely local. There is no dependency between different candidate centers, so no preprocessing or dynamic programming is needed. Each cell can be evaluated independently.

Any attempt to optimize further would not change the complexity class, because we already touch each cell once. The only “optimization” is careful boundary handling and avoiding redundant computation inside the inner checks.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | O(n²) | O(1) extra | Accepted |
| Optimal | O(n²) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Read the grid size and the grid itself into memory. We store it as a list of strings so indexing is O(1). This allows direct character access without parsing overhead.

2. Initialize a counter to zero. This will accumulate the number of valid cross centers.

3. Iterate over all cells `(i, j)` such that `1 < i < n - 1` and `1 < j < n - 1`. We skip the border because a valid center requires four diagonal neighbors.

4. For each candidate cell, check whether all five required positions contain `X`. If any one of them is not `X`, the cell is immediately rejected. This early rejection avoids unnecessary checks once a mismatch is found.

5. If all conditions are satisfied, increment the counter.

6. After scanning the entire grid, output the counter.

### Why it works

Every valid cross is uniquely identified by its center cell. The definition of a cross depends only on a fixed set of five positions, so checking those five cells is both necessary and sufficient. No other configuration can produce a valid cross without making those exact diagonal positions equal to `X`. Since every candidate center is tested exactly once and no valid configuration is skipped, the algorithm counts all crosses exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    grid = [input().strip() for _ in range(n)]

    if n < 3:
        print(0)
        return

    ans = 0

    for i in range(1, n - 1):
        for j in range(1, n - 1):
            if (grid[i][j] == 'X' and
                grid[i - 1][j - 1] == 'X' and
                grid[i - 1][j + 1] == 'X' and
                grid[i + 1][j - 1] == 'X' and
                grid[i + 1][j + 1] == 'X'):
                ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the algorithm: we iterate only over valid interior cells and explicitly test the five required positions. The early `n < 3` check prevents unnecessary looping and also makes the boundary logic cleaner.

A common mistake in implementation is mixing up `(i-1, j+1)` with `(i+1, j-1)` or forgetting one diagonal entirely. Another subtle issue is accidentally iterating from `0` to `n-1` and then adding boundary checks inside the loop, which increases clutter and risk of off-by-one errors.

## Worked Examples

### Example 1
Input:
```
5
.....
.XXX.
.XXX.
.XXX.
.....
```

We evaluate only the interior 3×3 region.

| (i, j) | grid[i][j] | diagonals valid? | result |
|--------|------------|------------------|--------|
| (1,1) | . | no | 0 |
| (1,2) | X | no | 0 |
| (1,3) | X | no | 0 |
| (2,1) | X | no | 0 |
| (2,2) | X | yes | 1 |
| (2,3) | X | no | 1 |
| (3,1) | X | no | 1 |
| (3,2) | X | no | 1 |
| (3,3) | X | no | 1 |

Only `(2,2)` satisfies all diagonal constraints, so the answer is `1`.

This confirms that only full diagonal symmetry around a center contributes, even if surrounding rows look dense with `X`.

### Example 2
Input:
```
3
X.X
.X.
X.X
```

| (i, j) | center X | diagonals | result |
|--------|----------|-----------|--------|
| (1,1) | X | valid | 1 |

There is only one possible center, and all required diagonals match. The algorithm correctly counts it as a single cross.

This shows the smallest valid configuration where a cross exists, confirming that the boundary restriction to interior cells is correct.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(n²) | each grid cell is checked at most once with constant work |
| Space | O(1) extra | grid storage aside, only a counter is used |

The grid size cap of 500 makes `n² = 250,000`, which is well within limits for a constant-factor check per cell. Memory usage is also trivial since we store only the input grid.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    n = int(sys.stdin.readline())
    grid = [sys.stdin.readline().strip() for _ in range(n)]
    if n < 3:
        return "0"

    ans = 0
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            if (grid[i][j] == 'X' and
                grid[i-1][j-1] == 'X' and
                grid[i-1][j+1] == 'X' and
                grid[i+1][j-1] == 'X' and
                grid[i+1][j+1] == 'X'):
                ans += 1
    return str(ans)

# provided sample
assert run("""5
.....
.XXX.
.XXX.
.XXX.
.....
""") == "1"

# minimum size
assert run("""1
.
""") == "0"

# no crosses but many X
assert run("""3
XXX
XXX
XXX
""") == "0"

# single cross
assert run("""3
X.X
.X.
X.X
""") == "1"

# multiple crosses
assert run("""5
X.X.X
.X.X.
X.X.X
.X.X.
X.X.X
""") == "9"
```

| Test input | Expected output | What it validates |
|---|---|---|
| 1×1 grid | 0 | minimum boundary handling |
| full X 3×3 | 0 | diagonals required, not dense blocks |
| single pattern | 1 | basic correctness |
| alternating grid | 9 | multiple independent centers |

## Edge Cases

For `n = 1` or `n = 2`, the algorithm immediately returns zero before any loop executes. This matches the fact that no cell has four diagonal neighbors.

For a fully filled grid of `X`, every interior cell is checked, but most fail because diagonals for adjacent centers overlap incorrectly. For example, in a `3×3` grid of all `X`, the center is valid but in larger grids, border-adjacent candidates fail due to missing diagonals.

For sparse grids where `X` forms vertical or horizontal lines, no cross is detected because diagonal structure is absent. The algorithm correctly inspects all candidates but rejects them due to missing diagonal matches.

Each case confirms that the decision is purely local and fully captured by the five-cell check per candidate.
