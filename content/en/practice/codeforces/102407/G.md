---
title: "CF 102407G - Crazy domino"
description: "We have an (n times n) chessboard. We may place at most (n) checkers on individual cells. Every remaining cell must be covered by exactly one domino, where a domino always covers two cells sharing a side."
date: "2026-08-10T16:15:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102407
codeforces_index: "G"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0412\u0442\u043e\u0440\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102407
solve_time_s: 321
verified: true
draft: false
---

[CF 102407G - Crazy domino](https://codeforces.com/problemset/problem/102407/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an (n \times n) chessboard. We may place at most (n) checkers on individual cells. Every remaining cell must be covered by exactly one domino, where a domino always covers two cells sharing a side. The arrangement of checkers must be chosen so that the remaining board has exactly one possible domino tiling.

The input contains only (n), with (2 \le n \le 100). The output is an (n \times n) grid where `#` represents a checker and `.` represents a free cell. The construction is guaranteed to exist. The official limits are 2 seconds and 512 MB.

The small upper bound of 100 is slightly misleading. This is not a problem where we should search through the board. There are (n^2) cells, and even considering only arrangements containing exactly (n) checkers gives (\binom{n^2}{n}) candidates. For (n=100), this is roughly (10^{242}), so exhaustive construction is completely impossible. The intended solution has to exploit the fact that we only need one carefully designed pattern.

There are several edge cases that a generic parity-based construction can mishandle. For (n=2), putting checkers in both cells of the first row leaves the second row, which is exactly one domino, so `##` followed by `..` is already valid. For (n=3), the general odd-sized alternating-corner construction does not work, so a separate small construction is needed. The sample itself gives one such construction:

```
...
##.
#..
```

The six free cells have exactly one tiling.

For (n=4), the simple even construction works:

```
#..#
....
#..#
....
```

There are exactly four checkers, and the free cells are forced into dominoes from the two sides. Forgetting the parity distinction would either use too many checkers or leave a board with multiple tilings.

## Approaches

A brute-force solution could try every possible set of at most (n) checker cells. For every candidate, we would then have to determine whether the remaining cells can be tiled and whether that tiling is unique. The number of candidate sets alone is at least (\binom{n^2}{n}). At (n=100), this is around (10^{242}), before doing any work to check the tiling. The brute force is correct because it explicitly tests the definition, but the search space is far beyond anything feasible.

The useful observation is that we do not need to discover the tiling. We can construct the board so that the checkers on the boundary force every domino one after another. Once a cell has only one possible neighboring free cell, its domino is forced. Placing that domino can make another cell have only one possible partner, creating a chain of forced placements.

For even (n), put a checker in the first and last columns of every odd-numbered row. This uses exactly (n) checkers. The cells at the ends of every even row are then forced horizontally, and this forces the neighboring cells in the odd rows, continuing toward the center.

For odd (n \ge 5), alternate the checker between the two extreme columns. Odd rows receive a checker in the first column, while even rows receive one in the last column. Again there are exactly (n) checkers. The alternating boundary creates a chain of forced dominoes that propagates through the board. This is the construction given in the official tutorial.

The only exceptional value is (n=3), for which we use the small construction from the sample. The case (n=2) is handled directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (\Theta\left(\binom{n^2}{n}\right)) candidates before tiling checks | At least (O(n^2)) | Too slow |
| Construction | (O(n^2)) | (O(n^2)) | Accepted |

## Algorithm Walkthrough

1. Read (n) and create an (n \times n) board filled with `.`. We will only need to decide which cells become checkers.
2. If (n=2), put checkers in both cells of the first row. The remaining row consists of exactly two adjacent cells, so its domino tiling is forced.
3. If (n=3), use the grid

```
...
##.
#..
```

There are three checkers, and the remaining six cells are forced into three dominoes.

1. If (n) is even, put `#` in columns (1) and (n) of every odd-numbered row. In zero-based Python indices, this means rows `0, 2, 4, ...` receive a checker at columns `0` and `n - 1`.
2. If (n) is odd and at least (5), put a checker in column (1) on every odd-numbered row and in column (n) on every even-numbered row. In zero-based indexing, row `i` gets a checker in column `0` when `i` is even, and column `n - 1` when `i` is odd.
3. Print the resulting board. In the even case there are (2(n/2)=n) checkers. In the odd case there are ((n+1)/2+(n-1)/2=n) checkers, so the checker limit is satisfied exactly.

**Why it works.** The key invariant is that the boundary checkers eliminate all alternative partners for cells next to them. Once one forced domino is placed, another cell becomes forced, and the process continues. For the even construction, the forcing propagates symmetrically from the two extreme columns. For the odd construction, the two forcing directions alternate between the extreme columns as we move through the rows. Thus every free cell belongs to one forced domino, and there is no decision left when the tiling is completed. The official tutorial describes the same idea by observing that checkers in the extreme columns make the domino tiling unique.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    board = [['.' for _ in range(n)] for _ in range(n)]

    if n == 2:
        board[0][0] = '#'
        board[0][1] = '#'

    elif n == 3:
        board = [
            list("..."),
            list("##."),
            list("#.."),
        ]

    elif n % 2 == 0:
        for r in range(0, n, 2):
            board[r][0] = '#'
            board[r][n - 1] = '#'

    else:
        for r in range(n):
            if r % 2 == 0:
                board[r][0] = '#'
            else:
                board[r][n - 1] = '#'

    sys.stdout.write('\n'.join(''.join(row) for row in board))

if __name__ == "__main__":
    solve()
```

The board is initialized entirely with free cells, so every assignment of `#` is explicit and there is no need for a separate count of checkers.

The (n=2) and (n=3) cases are handled before the parity construction because they are the only small dimensions where the general patterns are not appropriate. For (n=3), the explicit sample construction is particularly convenient.

For even (n), iterating over `range(0, n, 2)` visits exactly the odd-numbered rows in one-based indexing. Both extreme columns receive a checker in each such row.

For odd (n \ge 5), every row receives exactly one checker. The checker alternates between the left and right boundary, so exactly (n) checkers are used.

There are no arithmetic risks or complicated boundary calculations. The only boundary-sensitive expressions are `0` and `n - 1`, which are valid for every allowed (n).

## Worked Examples

For Sample 1, (n=3), the algorithm enters the explicit small-case branch.

| Step | n | Action | Board |
| --- | --- | --- | --- |
| 1 | 3 | Initialize | `... / ... / ...` |
| 2 | 3 | Use special construction | `... / ##. / #..` |
| 3 | 3 | Print | `... / ##. / #..` |

The free cells are ((1,1),(1,2),(1,3),(2,3),(3,2),(3,3)). The domino covering the bottom row must use ((3,2),(3,3)). Then ((1,1),(1,2)) must form a horizontal domino, leaving ((1,3),(2,3)) as the final domino. No alternative remains.

For Sample 2, (n=4), the even construction is used.

| Row | n | Checker positions | Result |
| --- | --- | --- | --- |
| 1 | 4 | columns 1 and 4 | `#..#` |
| 2 | 4 | none | `....` |
| 3 | 4 | columns 1 and 4 | `#..#` |
| 4 | 4 | none | `....` |

The four checkers are exactly the allowed number. In row 2, both boundary cells can only pair horizontally because the cells directly above and below them are occupied by checkers. Those forced dominoes then force the remaining cells in rows 1 and 3. The same reasoning finishes the board.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^2)) | The board contains (n^2) cells and we initialize and output all of them. |
| Space | (O(n^2)) | The constructed board is stored as an (n \times n) character grid. |

With (n \le 100), the board contains at most 10,000 cells. The algorithm performs only a constant amount of work per cell, so it is far below the 2-second limit and uses negligible memory compared with the 512 MB limit.

## Test Cases

The samples allow any valid construction, so the test harness below validates the returned board rather than requiring a particular sample output. For small boards it also counts all domino tilings recursively and verifies that exactly one exists. The maximum-size test checks the structural requirements directly.

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        n = int(sys.stdin.readline())
        board = [['.' for _ in range(n)] for _ in range(n)]

        if n == 2:
            board[0][0] = '#'
            board[0][1] = '#'

        elif n == 3:
            board = [
                list("..."),
                list("##."),
                list("#.."),
            ]

        elif n % 2 == 0:
            for r in range(0, n, 2):
                board[r][0] = '#'
                board[r][n - 1] = '#'

        else:
            for r in range(n):
                if r % 2 == 0:
                    board[r][0] = '#'
                else:
                    board[r][n - 1] = '#'

        sys.stdout.write('\n'.join(''.join(row) for row in board))
        return sys.stdout.getvalue()

    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def run(inp: str) -> str:
    return solve_data(inp)

def count_tilings(board):
    n = len(board)
    free = []

    for r in range(n):
        for c in range(n):
            if board[r][c] == '.':
                free.append((r, c))

    index = {cell: i for i, cell in enumerate(free)}
    full = (1 << len(free)) - 1

    memo = {}

    def dfs(mask):
        if mask == full:
            return 1

        if mask in memo:
            return memo[mask]

        for i, (r, c) in enumerate(free):
            if mask & (1 << i):
                continue

            ways = 0

            for dr, dc in ((1, 0), (0, 1)):
                nr, nc = r + dr, c + dc
                j = index.get((nr, nc))

                if j is not None and not (mask & (1 << j)):
                    ways += dfs(mask | (1 << i) | (1 << j))

            memo[mask] = ways
            return ways

        return 0

    return dfs(0)

def validate_small(inp: str):
    n = int(inp)
    out = run(inp).strip().splitlines()

    assert len(out) == n
    assert all(len(row) == n for row in out)

    checkers = sum(row.count('#') for row in out)
    assert checkers <= n

    board = [list(row) for row in out]
    assert count_tilings(board) == 1

# Sample 1
validate_small("3\n")

# Sample 2
validate_small("4\n")

# Minimum size
validate_small("2\n")

# Small odd case that needs the special construction
validate_small("5\n")

# Boundary and parity case
validate_small("6\n")

# Maximum size
out = run("100\n").strip().splitlines()
assert len(out) == 100
assert all(len(row) == 100 for row in out)
assert all(ch in ".#" for row in out for ch in row)
assert sum(row.count('#') for row in out) <= 100
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3` | Any valid 3 by 3 construction | Provided Sample 1 and the special odd case |
| `4` | Any valid 4 by 4 construction | Provided Sample 2 and even parity |
| `2` | `## / ..` | Minimum allowed (n) and boundary handling |
| `5` | Alternating extreme-column checkers | Smallest odd case using the general construction |
| `6` | Checkers on both extremes of odd rows | Even construction and row indexing |
| `100` | A valid 100 by 100 grid | Maximum size and checker-count bound |

## Edge Cases

For (n=2), the exact input is:

```
2
```

The algorithm produces:

```
##
..
```

There are two checkers, which satisfies the limit. The two remaining cells are adjacent, so there is exactly one domino placement.

For (n=3), the exact input is:

```
3
```

The algorithm produces:

```
...
##.
#..
```

The checker count is three. The bottom two free cells form a forced horizontal domino, after which the top-left pair and the rightmost vertical pair are forced. This is why the explicit (n=3) branch is needed.

For an even dimension such as (n=6), the construction is:

```
#....#
......
#....#
......
#....#
......
```

There are six checkers. Every boundary cell in an even row is trapped between checker cells vertically, so it must pair inward horizontally. Those forced dominoes then determine the neighboring cells in the odd rows, and the process continues until every free cell is covered.

For an odd dimension such as (n=5), the construction is:

```
#....
....#
#....
....#
#....
```

Again there are exactly five checkers. The alternating boundary positions create the forcing chain described in the construction. The parity of (n) makes the two forcing fronts meet consistently instead of leaving an unmatched central cell.

For (n=100), the same even construction uses exactly 100 checkers, one pair on each of the 50 odd-numbered rows. The algorithm does not depend on any special numerical property of 100, so the maximum constraint is handled in exactly the same way as every other even value.
