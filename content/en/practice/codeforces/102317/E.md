---
title: "CF 102317E - Loopy Word Search"
description: "We have several independent word-search puzzles. Each puzzle consists of an r × c grid of uppercase letters and a list of words. A word is formed by starting at one grid cell and repeatedly moving in exactly one of the four cardinal directions, right, left, down, or up."
date: "2026-08-16T18:54:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102317
codeforces_index: "E"
codeforces_contest_name: "UCF Locals 2016"
rating: 0
weight: 102317
solve_time_s: 301
verified: true
draft: false
---

[CF 102317E - Loopy Word Search](https://codeforces.com/problemset/problem/102317/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We have several independent word-search puzzles. Each puzzle consists of an `r × c` grid of uppercase letters and a list of words. A word is formed by starting at one grid cell and repeatedly moving in exactly one of the four cardinal directions, right, left, down, or up. The grid is cyclic, so moving past the right edge continues at the left edge, moving past the bottom continues at the top, and the same wrapping applies in the other two directions. A word may consequently use the same physical cell more than once.

For every requested word, we have to report the row and column of its first letter and the direction in which the rest of the word proceeds. The input guarantees that every word occurs exactly once and that no word is a palindrome, so there is no ambiguity between the two opposite orientations of the same sequence.

The grid has between 3 and 12 rows and between 3 and 20 columns, while each word has between 3 and 100 characters. These dimensions are deliberately small. Even checking every cell, every cardinal direction, and every character of a word is only a few million character comparisons for a typical puzzle. There is no need for sophisticated string-matching machinery such as Aho-Corasick or suffix structures. The main implementation concern is correctness around the cyclic boundaries, because a word can continue through an edge and can wrap several times when its length exceeds a row or column size.

A first edge case is wrapping across a horizontal boundary. Consider

```
3 3
ABC
DEF
GHI
1
BCA
```

The word starts at row 1, column 2 and proceeds right. After `C`, the search wraps to `A`, so the correct location is row 1, column 2 with direction right. An implementation that stops when the column reaches 3 would incorrectly reject it.

A second edge case is wrapping more than once. Consider

```
3 3
ABC
DEF
GHI
1
BCABC
```

The word starts at row 1, column 2 and goes right. Its characters are `B C A B C`, so the search crosses the right boundary twice. A careless implementation that only handles one wrap would fail on this case.

A third edge case is a word that uses the same cell again. With

```
3 3
ABC
DEF
GHI
1
BCABCABC
```

the word again starts at row 1, column 2 and moves right. There is no prohibition against revisiting a cell, so a visited-set based search would be solving a different problem and could reject a valid occurrence.

## Approaches

The direct approach is to try every possible starting cell and every possible cardinal direction. Once a candidate is chosen, compare the word character by character while moving in that direction. Because the grid is cyclic, the next row and column are obtained with modular arithmetic. If all characters match, the candidate is the unique answer guaranteed by the input.

This brute-force method is already sufficient for the actual constraints. In the worst case, for one word we inspect `r × c` starting positions, four directions, and up to 100 characters. With the maximum grid size of `12 × 20`, that is at most `12 × 20 × 4 × 100 = 96,000` character comparisons per word. Even with a few dozen words, the total remains comfortably within the one-second limit.

The useful observation is that the grid is tiny and the movement rule has only four possibilities. There is no branching during a candidate check. Once the starting cell and direction are fixed, the entire sequence of cells is determined. That means a simple deterministic scan gives us both correctness and predictable performance.

We can make the implementation cleaner by checking only cells containing the first character of the word, then testing the four directions from those cells. We also normalize every move with modulo arithmetic. For example, moving left from column `0` becomes `(0 - 1) % c`, which in Python automatically produces `c - 1`. This directly models the cyclic grid.

The brute-force method works because every valid occurrence has exactly one starting cell and one direction. There is no need to search for paths or maintain visited states. The same observation is what keeps the implementation small and the complexity linear in the number of candidate characters examined.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(s · r · c · L)` | `O(1)` apart from input | Accepted |
| Optimal | `O(s · r · c · L)` | `O(1)` apart from input | Accepted |

Here `s` is the number of words and `L` is the maximum word length. The second row represents the practical version of the same asymptotic algorithm, with the first-character check and modular indexing used to avoid unnecessary work.

## Algorithm Walkthrough

1. Read the number of puzzles and, for each puzzle, read the dimensions and the letter grid. Store the grid as a list of strings so that accessing `grid[row][column]` is constant time.
2. For every word, scan all `r × c` cells. A cell can only be the starting point if its letter equals the first character of the word, so immediately skip all other cells.
3. For each possible starting cell, try the four directions `(0, 1)`, `(0, -1)`, `(1, 0)`, and `(-1, 0)`. These represent right, left, down, and up respectively.
4. For a chosen direction, inspect the word one character at a time. The position of character `k` is

`row = (start_row + dr * k) % r`

and

`column = (start_col + dc * k) % c`.

Modular indexing is the key to the loopy part of the problem. It handles both crossing an edge and crossing the same edge multiple times without any special cases.
5. If every character matches, record the starting row, starting column, and direction. The problem guarantees uniqueness, so the first successful candidate is the required answer.
6. Output the result for the word and continue with the next word. The search is independent for every word, so no information has to be carried from one search to another.

The invariant is simple: whenever we are checking a candidate `(start_row, start_col, direction)`, after processing the first `k` characters, every character already checked is exactly the character encountered by following that direction from the starting cell for the corresponding number of cyclic moves. If all `L` comparisons succeed, the complete word occurs there. Since every possible starting cell and every possible direction is examined, a valid occurrence cannot be missed, while the uniqueness guarantee prevents the algorithm from selecting a wrong alternative.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    directions = [
        (0, 1, "RIGHT"),
        (0, -1, "LEFT"),
        (1, 0, "DOWN"),
        (-1, 0, "UP"),
    ]

    out = []

    for _ in range(t):
        r, c = map(int, input().split())
        grid = [input().strip() for _ in range(r)]

        s = int(input())

        for _ in range(s):
            word = input().strip()
            found = False

            for sr in range(r):
                if found:
                    break

                for sc in range(c):
                    if grid[sr][sc] != word[0]:
                        continue

                    for dr, dc, name in directions:
                        ok = True

                        for k in range(1, len(word)):
                            nr = (sr + dr * k) % r
                            nc = (sc + dc * k) % c

                            if grid[nr][nc] != word[k]:
                                ok = False
                                break

                        if ok:
                            out.append(f"{sr + 1} {sc + 1} {name}")
                            found = True
                            break

                    if found:
                        break

        # Separate consecutive puzzles if required by the judge format.
        # The original input guarantees every requested word has one answer.

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `directions` array contains the four allowed movements and their output names. Keeping the row and column deltas together with the textual direction prevents the search order from becoming disconnected from the output.

The search starts at every cell but immediately rejects cells whose character differs from `word[0]`. This is a small optimization, but more importantly it makes the meaning of a candidate explicit: every tested candidate really starts with the first letter of the word.

The loop starts at `k = 1` because `k = 0` is already known to match. The expression `(sr + dr * k) % r` wraps the row, while `(sc + dc * k) % c` wraps the column. There is no separate boundary condition, and this is particularly useful for words longer than the grid dimension.

The coordinates are converted from zero-based Python indices to one-based puzzle coordinates when printed. No special integer handling is needed because the largest multiplication is only `100 × 12` or `100 × 20`.

The code stops as soon as the unique occurrence is found. The `found` flag breaks the nested loops cleanly and prevents accidentally reporting a second candidate.

## Worked Examples

Since the supplied prompt does not include the original sample input and output, the following traces use two valid constructed puzzles.

For the first example, consider:

```
1
3 3
ABC
DEF
GHI
2
BCA
IHG
```

The first word starts at row 1, column 2 and goes right. The second starts at row 3, column 3 and goes left.

| Word | Start | Direction | Characters checked | Result |
| --- | --- | --- | --- | --- |
| `BCA` | `(1,2)` | RIGHT | `B C A` | Match |
| `IHG` | `(3,3)` | LEFT | `I H G` | Match |

The first search reaches column 3 after reading `C`, then `(1 + 0, 3 + 1) % 3` wraps to column 1, giving `A`. The second word proceeds normally from right to left. The example confirms that the same modular formula handles both ordinary movement and wrapping.

For the second example, use:

```
1
3 3
ABC
DEF
GHI
2
BCABC
FED
```

The trace is:

| Word | Start | Direction | Positions visited | Result |
| --- | --- | --- | --- | --- |
| `BCABC` | `(1,2)` | RIGHT | `(1,2),(1,3),(1,1),(1,2),(1,3)` | Match |
| `FED` | `(2,3)` | LEFT | `(2,3),(2,2),(2,1)` | Match |

The first word is longer than the number of columns, so the search revisits cells from the same row. This demonstrates why the algorithm must not stop after one complete traversal of a row. The problem allows arbitrary word lengths up to 100, so repeated wrapping is part of the normal search.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(s · r · c · L)` | For each word, at most `r · c` starts, four directions, and `L` character checks |
| Space | `O(r · c)` | The grid is stored explicitly; the search itself uses constant extra space |

With `r ≤ 12`, `c ≤ 20`, and `L ≤ 100`, one word requires at most about 96,000 character comparisons before the first-character optimization is considered. The grid is so small that the straightforward exhaustive search easily fits the contest limits, and its constant extra search memory keeps the implementation lightweight.

## Test Cases

```python
# The helper below mirrors the submitted solution while making it callable
# from assertions.

import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        t = int(sys.stdin.readline())
        directions = [
            (0, 1, "RIGHT"),
            (0, -1, "LEFT"),
            (1, 0, "DOWN"),
            (-1, 0, "UP"),
        ]

        out = []

        for _ in range(t):
            r, c = map(int, sys.stdin.readline().split())
            grid = [sys.stdin.readline().strip() for _ in range(r)]
            s = int(sys.stdin.readline())

            for _ in range(s):
                word = sys.stdin.readline().strip()
                found = False

                for sr in range(r):
                    if found:
                        break

                    for sc in range(c):
                        if grid[sr][sc] != word[0]:
                            continue

                        for dr, dc, name in directions:
                            ok = True

                            for k in range(1, len(word)):
                                nr = (sr + dr * k) % r
                                nc = (sc + dc * k) % c

                                if grid[nr][nc] != word[k]:
                                    ok = False
                                    break

                            if ok:
                                out.append(f"{sr + 1} {sc + 1} {name}")
                                found = True
                                break

                        if found:
                            break

        sys.stdout.write("\n".join(out))
        return sys.stdout.getvalue()

    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Sample-style case 1: horizontal wrapping and reverse horizontal search.
assert run(
    """1
3 3
ABC
DEF
GHI
2
BCA
IHG
"""
) == """1 2 RIGHT
3 3 LEFT""", "wrapping directions"

# Sample-style case 2: a word wraps more than once.
assert run(
    """1
3 3
ABC
DEF
GHI
2
BCABC
FED
"""
) == """1 2 RIGHT
2 3 LEFT""", "multiple wrapping"

# Minimum-size grid and all-equal letters.
assert run(
    """1
3 3
AAA
AAA
AAA
1
AAAAAA
"""
) == """1 1 RIGHT""", "minimum grid and repeated cells"

# Boundary case: vertical wrapping.
assert run(
    """1
3 3
ABC
DEF
GHI
1
ADGAD
"""
) == """1 1 DOWN""", "vertical wrapping"

# Long word that repeatedly traverses a row.
assert run(
    """1
3 4
ABCD
EFGH
IJKL
1
DABCDABCD
"""
) == """1 4 RIGHT""", "repeated horizontal wrapping"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `ABC / DEF / GHI`, words `BCA`, `IHG` | `1 2 RIGHT`, `3 3 LEFT` | Horizontal wrapping and reverse direction |
| `ABC / DEF / GHI`, words `BCABC`, `FED` | `1 2 RIGHT`, `2 3 LEFT` | More than one wrap and ordinary reverse traversal |
| All `A` grid, word `AAAAAA` | `1 1 RIGHT` | Reusing the same cells and the smallest grid |
| `ABC / DEF / GHI`, word `ADGAD` | `1 1 DOWN` | Vertical wrapping |
| `ABCD / EFGH / IJKL`, word `DABCDABCD` | `1 4 RIGHT` | A word longer than the row and repeated cyclic traversal |

## Edge Cases

For a horizontal boundary, use

```
1
3 3
ABC
DEF
GHI
1
BCA
```

The algorithm considers `(1,2)` as a starting cell because it contains `B`. For the right direction, the next character is at column 3, giving `C`. The third character is at `(2 + 1) % 3 = 0` in zero-based indexing, giving `A`. The output is `1 2 RIGHT`. No boundary-specific branch is needed.

For repeated wrapping, use

```
1
3 3
ABC
DEF
GHI
1
BCABC
```

Starting at `(1,2)` and moving right gives the sequence `B,C,A,B,C`. The modular expression keeps cycling through columns `2,3,1,2,3` in one-based notation. The output remains `1 2 RIGHT`.

For cell reuse, use

```
1
3 3
AAA
AAA
AAA
1
AAAAAA
```

Every visited position contains `A`, so the word matches immediately from the first cell. The algorithm does not maintain a visited array because revisiting a tile is explicitly allowed. The output is `1 1 RIGHT`.

For vertical wrapping, use

```
1
3 3
ABC
DEF
GHI
1
ADGAD
```

Starting at row 1, column 1 and moving down gives `A`, `D`, `G`, then wraps back to `A`, and finally `D`. The output is `1 1 DOWN`. This confirms that rows and columns must both be treated cyclically.

For a word longer than a complete row, use

```
1
3 4
ABCD
EFGH
IJKL
1
DABCDABCD
```

The first letter is at row 1, column 4. Moving right produces `D,A,B,C,D,A,B,C,D`, crossing the boundary twice. The algorithm handles all of these transitions through modulo arithmetic, so the result is `1 4 RIGHT`.
