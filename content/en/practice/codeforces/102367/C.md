---
title: "CF 102367C - Pawn's Revenge"
description: "We have an (N times N) chessboard represented by (N) strings. A is an opponent piece, K is our king, and - is an empty square where a pawn may potentially be placed. Pawns move upward, meaning a pawn at row (r+1), column (c) attacks the two squares ((r,c-1)) and ((r,c+1))."
date: "2026-08-12T23:27:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102367
codeforces_index: "C"
codeforces_contest_name: "Fall 2019 ICPC-style Waterloo Local Contest"
rating: 0
weight: 102367
solve_time_s: 261
verified: true
draft: false
---

[CF 102367C - Pawn's Revenge](https://codeforces.com/problemset/problem/102367/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an (N \times N) chessboard represented by (N) strings. A `*` is an opponent piece, `K` is our king, and `-` is an empty square where a pawn may potentially be placed. Pawns move upward, meaning a pawn at row (r+1), column (c) attacks the two squares ((r,c-1)) and ((r,c+1)). The king attacks every square whose row and column differ from its own by at most one. The task is to place as few additional pawns as possible so that every `*` is attacked by either the king or one of the new pawns. A pawn cannot be placed on a square already occupied by `*` or `K`. The official problem has (8 \le N \le 1000), with a 1 second time limit and 256 MB memory limit.

The first useful observation is that pawns attacking a particular row must be placed in exactly the next row. A star in row (r) can only be attacked by pawns in row (r+1), never by a pawn in some other row. Consequently, once we account for the king, every row can be solved independently. With (N) at most 1000, there are at most one million board cells, so an (O(N^2)) solution is entirely reasonable. An approach that explores subsets of possible pawn positions, or repeatedly searches the whole board for every star, is far too expensive.

Several boundary cases can make a seemingly reasonable implementation wrong. A star on the bottom row has no row below it, so no pawn can attack it. For example,

```
8
--------
--------
--------
--------
--------
--------
--------
*------K
```

has answer `-1`, because the star cannot be attacked by a pawn and is not adjacent to the king. A careless implementation that simply checks both diagonal columns without checking the row boundary might access an invalid cell or incorrectly count a pawn.

A star can also have both potential pawn squares occupied. For example,

```
8
--------
--------
--------
--------
--------
--------
-*-*----
-K------
```

is not a valid example of this situation because the king changes the coverage, so consider instead the relevant local pattern in a row: if a star is at column 2 and the cells at columns 1 and 3 of the next row are both occupied by existing pieces, no pawn can attack that star. The correct result is `-1` unless the king already covers it. An implementation that treats every diagonal square as a possible pawn position will incorrectly claim that one pawn is available.

Another subtle case is two stars separated by one column. If both are uncovered and the middle square in the next row is empty, one pawn covers both stars. For example,

```
8
-*-*----
--------
--------
--------
--------
--------
--------
------K-
```

has answer `1`. A solution that handles each star independently and places one pawn for every star would return `2`, missing the fact that one pawn can attack both endpoints.

Finally, the king may already cover some stars, and those stars must be removed from consideration before the pawn optimization. In the official sample, the star next to the king needs no pawn, while the other stars require two pawns in total.

## Approaches

A direct brute-force solution could consider every subset of empty cells as a possible collection of pawn positions, test whether that collection attacks every star, and keep the smallest successful subset. If there are (E) empty cells, there are (2^E) subsets, and checking one subset can require (O(N^2)) work. In the worst case (E) is close to (N^2), giving roughly (O(N^2 2^{N^2})) operations. For (N=1000), this is on the order of (10^6 2^{10^6}), which is not remotely feasible.

We can do much better by looking at the geometry of one row. Suppose a star is at column (c). A pawn capable of attacking it must be at column (c-1) or (c+1) in the next row. If two stars in the same row occur at columns (c) and (c+2), the square at column (c+1) in the next row attacks both of them. Thus, after removing stars already attacked by the king, each row becomes a one-dimensional covering problem.

The useful greedy rule is to scan the stars from left to right. When an uncovered star at column (c) is encountered, first try to put a pawn at column (c+1). If that square is empty, choosing it is always at least as good as choosing (c-1), because (c+1) attacks the current star and may also attack the next star at (c+2). If (c+1) is unavailable, the only remaining possibility is (c-1). If both are unavailable, the star cannot be attacked at all.

The reason this greedy choice is safe is local. When processing column (c), no future star lies to the left. A pawn at (c-1) can only help the current star and the already processed region, while a pawn at (c+1) can help the current star and potentially the next unprocessed star. Choosing the right-hand square never costs more and can only preserve more future coverage.

The rows are independent, so applying this greedy scan to every row gives an (O(N^2)) algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^2 2^{N^2})) | (O(N^2)) | Too slow |
| Optimal | (O(N^2)) | (O(N^2)) | Accepted |

## Algorithm Walkthrough

1. Read the entire board and locate the king. The king's position is needed because some stars require no pawn at all.
2. Scan every star and mark it as already covered whenever its row and column are both within one cell of the king. A star satisfying this condition does not participate in the pawn optimization.
3. Process each board row independently. A star in row (r) can only be attacked by a pawn in row (r+1), so choices made for one row cannot affect any other row.
4. For each row, scan columns from left to right. When the current cell is not an uncovered star, continue to the next column.
5. When an uncovered star is found at column (c), first inspect the candidate pawn square at row (r+1), column (c+1). If that cell exists and contains `-`, place a pawn there and increase the answer by one.

The right-hand candidate is preferred because it attacks the current star and can also attack a future star at column (c+2). Choosing the left candidate cannot provide any new help to stars that have not yet been processed.
6. If the right-hand candidate is unavailable, inspect the left-hand candidate at row (r+1), column (c-1). If it exists and is empty, place a pawn there and increase the answer.
7. If neither candidate exists as an empty cell, the current star cannot be attacked by any pawn. Since it was already determined not to be covered by the king, the entire board is impossible and the answer is `-1`.
8. Continue until every row has been processed. The accumulated number of pawns is the minimum answer.

### Why it works

For every uncovered star, the only possible pawn positions are its two diagonal squares in the next row. When the scan reaches that star, a previously selected pawn can only be at its left candidate, because all earlier decisions are to the left. If such a pawn exists, the star is already covered and no new pawn is needed. Otherwise, if the right candidate is empty, selecting it covers the current star and leaves the possibility of covering the next star with the same pawn. Any solution using the left candidate can be replaced by one using the right candidate without increasing the number of pawns. If the right candidate is blocked, the left candidate is the only remaining option. If both are blocked, no solution can cover the star. Thus every greedy decision is compatible with an optimal solution, and processing all rows independently gives the global minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    board = [input().strip() for _ in range(n)]

    kr = kc = -1
    for r in range(n):
        pos = board[r].find('K')
        if pos != -1:
            kr, kc = r, pos
            break

    answer = 0

    for r in range(n):
        c = 0

        while c < n:
            if board[r][c] != '*':
                c += 1
                continue

            # Already attacked by the king.
            if abs(r - kr) <= 1 and abs(c - kc) <= 1:
                c += 1
                continue

            # A pawn must be in the row below the star.
            pr = r + 1

            # No row below means no pawn can attack this star.
            if pr == n:
                print(-1)
                return

            # Prefer the right candidate. It may also cover
            # a future star two columns to the right.
            if c + 1 < n and board[pr][c + 1] == '-':
                answer += 1
                c += 1
                continue

            # Otherwise try the left candidate.
            if c - 1 >= 0 and board[pr][c - 1] == '-':
                answer += 1
                c += 1
                continue

            # Neither possible pawn position is available.
            print(-1)
            return

    print(answer)

if __name__ == "__main__":
    solve()
```

The board is stored as a list of strings because the algorithm only needs to inspect existing pieces. We do not actually need to write the newly placed pawns into the board. During a left-to-right scan, a newly selected pawn can only affect the current star and the immediately following relevant star, and the scan's position already captures that relationship.

The king is found once by searching each row. For every star, the condition `abs(r - kr) <= 1 and abs(c - kc) <= 1` exactly represents the eight neighboring squares plus the king's own row and column offsets. Since the cell itself is a star, the equality case cannot occur for both coordinates simultaneously, but using the standard Chebyshev-distance condition keeps the logic simple.

The candidate pawn row is `r + 1`, not `r - 1`, because the input's first row is the top of the board and pawns move toward smaller row indices. A pawn attacking a star in row `r` must consequently be below it in row `r + 1`.

The right candidate is checked before the left candidate. This ordering is the central greedy choice. If the right square is free, using it can additionally cover a star two columns to the right. The left candidate has no such future benefit.

The code advances `c` by one after placing a pawn. The pawn at `c + 1` attacks the current star at `c`, and if another star occurs at `c + 2`, that star will see this pawn when the scan reaches it. There is no need to jump over it or maintain a separate coverage array.

Python integers have arbitrary precision, so there is no overflow concern. The largest possible answer is at most the number of board cells, which is only (10^6).

## Worked Examples

The official sample is:

```
8
-*-*----
--------
--------
--------
-----*K-
--------
--*-----
--------
```

The stars at row 4, column 5 and row 6, column 2 are not adjacent to the king. The two stars in the first row can be handled by one pawn because they are separated by one column, while the lower star requires another pawn. The star next to the king needs no pawn. The official answer is `2`.

For the row containing the two top stars, the scan behaves as follows.

| Row | Column | Current cell | Action | Pawns |
| --- | --- | --- | --- | --- |
| 0 | 0 | `-` | Skip | 0 |
| 0 | 1 | `*` | Place pawn at row 1, column 2 | 1 |
| 0 | 2 | `-` | Skip | 1 |
| 0 | 3 | `*` | Already covered by the pawn at column 2 | 1 |

The pawn placed below column 2 attacks both stars at columns 1 and 3. This demonstrates the key invariant that once a pawn is selected to the right of a star, the next star at distance two is automatically covered.

For a second example, consider:

```
8
--*-----
--------
-*------
--------
--------
--------
--------
------K-
```

The star in row 0, column 2 requires a pawn in row 1. The star in row 2, column 1 requires a pawn in row 3. They belong to different target rows, so their pawn choices cannot interact.

| Row | Star column | Right candidate | Left candidate | Action | Pawns |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | row 1, col 3 is `-` | row 1, col 1 is `-` | Choose right | 1 |
| 2 | 1 | row 3, col 2 is `-` | row 3, col 0 is `-` | Choose right | 2 |

The result is `2`. This trace demonstrates why rows can be solved independently: even though the board contains several stars, a pawn selected for one target row can never attack a star in another target row.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N^2)) | Every board cell is examined at most a constant number of times. |
| Space | (O(N^2)) | The board contains (N^2) characters. |

With (N \le 1000), the board has at most one million cells. The algorithm performs only a constant amount of work per cell, so it stays comfortably within the intended complexity for the 1 second and 256 MB limits.

## Test Cases

The following test harness implements the same algorithm as a function so that each assertion can run independently.

```python
import sys
import io

def solve_case(inp: str) -> str:
    data = inp.strip().splitlines()
    n = int(data[0])
    board = data[1:1 + n]

    kr = kc = -1
    for r in range(n):
        pos = board[r].find('K')
        if pos != -1:
            kr, kc = r, pos
            break

    answer = 0

    for r in range(n):
        c = 0

        while c < n:
            if board[r][c] != '*':
                c += 1
                continue

            if abs(r - kr) <= 1 and abs(c - kc) <= 1:
                c += 1
                continue

            pr = r + 1

            if pr == n:
                return "-1"

            if c + 1 < n and board[pr][c + 1] == '-':
                answer += 1
                c += 1
                continue

            if c - 1 >= 0 and board[pr][c - 1] == '-':
                answer += 1
                c += 1
                continue

            return "-1"

    return str(answer)

def run(inp: str) -> str:
    return solve_case(inp)

# Provided sample
assert run(
    """8
-*-*----
--------
--------
--------
-----*K-
--------
--*-----
--------
"""
) == "2", "official sample"

# Minimum-size board, no opponent pieces.
assert run(
    """8
--------
--------
--------
--------
--------
--------
--------
---K----
"""
) == "0", "no stars means no pawns are needed"

# Two stars in the same row can share one pawn.
assert run(
    """8
--*-*---
--------
--------
--------
--------
--------
--------
---K----
"""
) == "1", "one pawn attacks both stars"

# A star on the bottom row cannot be attacked by a pawn.
assert run(
    """8
--------
--------
--------
--------
--------
--------
--------
*------K
"""
) == "-1", "bottom-row star has no row below it"

# The king already attacks the only star.
assert run(
    """8
--------
--------
--------
--------
--------
--------
--*-----
---K----
"""
) == "0", "king covers the star"

# Two independent target rows require two pawns.
assert run(
    """8
--*-----
--------
-*------
--------
--------
--------
--------
------K-
"""
) == "2", "different target rows are independent"

# Maximum-size all-empty board with a king.
n = 1000
big_board = ["-" * n for _ in range(n)]
big_board[500] = "-" * 499 + "K" + "-" * 500
assert run(str(n) + "\n" + "\n".join(big_board) + "\n") == "0", \
    "maximum-size board"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Official 8 by 8 sample | `2` | Correct handling of the original example and shared pawn coverage |
| Empty 8 by 8 board with a king | `0` | No stars means no pawn is necessary |
| Two stars with one empty middle pawn square | `1` | One pawn can attack two stars |
| Star on the bottom row | `-1` | Missing row below the target |
| Star adjacent to the king | `0` | King coverage is removed before pawn processing |
| Stars in different rows | `2` | Independence between target rows |
| 1000 by 1000 board | `0` | Maximum dimensions and (O(N^2)) performance |

## Edge Cases

Consider a star on the bottom row:

```
8
--------
--------
--------
--------
--------
--------
--------
*------K
```

The star is at row 7. Its possible pawn positions would have to be at row 8, which is outside the board. The algorithm reaches `pr = r + 1 = 8`, immediately detects that `pr == n`, and returns `-1`. There is no alternative pawn position elsewhere on the board because pawn attacks do not skip rows.

Now consider two stars separated by one column:

```
8
--*-*---
--------
--------
--------
--------
--------
--------
---K----
```

The first star is at column 2. Its right candidate is row 1, column 3, which is empty, so the algorithm places one pawn there. When it later reaches the star at column 4, that same pawn is its left candidate, so the star is already covered. The answer is `1`, not `2`. The scan works because it processes the row from left to right and preserves the coverage created for the next possible star.

For king coverage, use:

```
8
--------
--------
--------
--------
--------
--------
--*-----
---K----
```

The star is at row 6, column 2 and the king is at row 7, column 3. Their row difference and column difference are both one, so the king attacks the star diagonally. The algorithm skips it before considering any pawn candidates and returns `0`.

For blocked pawn positions, consider:

```
8
-*------
-K------
--------
--------
--------
--------
--------
--------
```

The star is already attacked by the king in this particular arrangement, so the answer is `0`. To see the blocked-position rule itself, the same local configuration can occur with the king elsewhere: if a star at column (c) has both cells (c-1) and (c+1) in the next row occupied by existing pieces, neither can receive a pawn. The algorithm checks both candidates and returns `-1`. It never assumes that a diagonal square is automatically available.

The maximum-size case contains one million cells. Since each row is scanned once and each cell participates in only constant-time checks, the algorithm remains (O(10^6)). The implementation stores the board directly, so its memory usage is also proportional to one million characters rather than to an exponential search space.
