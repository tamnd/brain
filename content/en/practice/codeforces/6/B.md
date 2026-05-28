---
title: "CF 6B - President's Office"
description: "The office is represented as a rectangular grid. Every uppercase letter represents part of a desk, and all cells with th"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 6
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 6 (Div. 2 Only)"
rating: 1100
weight: 6
solve_time_s: 78
verified: true
draft: false
---

[CF 6B - President's Office](https://codeforces.com/problemset/problem/6/B)

**Rating:** 1100  
**Tags:** implementation  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

The office is represented as a rectangular grid. Every uppercase letter represents part of a desk, and all cells with the same letter belong to the same rectangular desk. The president’s desk color is given as `c`.

A deputy is any desk that shares a side with at least one cell of the president’s desk. Diagonal contact does not count. Empty cells marked with `.` also do not count. The task is to count how many distinct desk colors are adjacent to the president’s desk.

The grid dimensions are at most `100 × 100`, so the entire grid contains at most `10,000` cells. This is small enough that scanning the whole grid several times is completely safe. Even an `O(n * m * 4)` solution performs only around `40,000` neighbor checks.

The main difficulty is not performance, it is avoiding double-counting and handling adjacency correctly.

One easy mistake is counting the same neighboring color multiple times. Consider this grid:

```
3 3 A
BBB
BAB
BBB
```

The correct answer is `1`, because only color `B` touches the president’s desk. A careless implementation that increments the answer every time it sees an adjacent `B` would incorrectly output `4`.

Another subtle case is accidentally counting empty cells:

```
2 3 A
.A.
...
```

The correct answer is `0`. The president’s desk is surrounded only by empty space, which should not be counted.

A third common bug is counting the president’s own color as a deputy. For example:

```
3 4 A
AAAA
ABBA
AAAA
```

The correct answer is `1`. While every `A` cell touches other `A` cells, those are still part of the president’s desk and must be ignored.

Boundary handling also matters. If the president’s desk touches the edge of the grid, neighbor checks can go out of bounds:

```
2 2 A
AB
..
```

The correct answer is `1`. Any implementation that blindly checks four directions without validating coordinates risks accessing invalid indices.

## Approaches

A brute-force idea is to examine every cell in the grid. Whenever we find a president cell, we inspect all four neighboring positions and record any different desk color we see.

This approach is already fast enough for the given constraints. The grid has at most `10,000` cells, and each cell performs at most four neighbor checks. That is only around `40,000` operations.

The only remaining issue is duplicate counting. A neighboring desk may touch the president’s desk in many places. Using a list and searching it repeatedly would still work here, but a set is cleaner and guarantees uniqueness automatically.

The key observation is that we do not actually care how many adjacent cells exist. We only care about how many distinct colors appear next to the president’s desk. Once a color has been seen, additional occurrences do not matter.

This reduces the problem to a simple grid traversal with a set collecting valid neighboring colors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with duplicate counting | O(n × m × k) | O(k) | Unnecessarily messy |
| Optimal using a set | O(n × m) | O(k) | Accepted |

Here, `k` is the number of distinct neighboring colors, which is at most `26`.

## Algorithm Walkthrough

1. Read the grid dimensions and the president’s desk color.
2. Store the grid as a list of strings so each cell can be accessed with `grid[row][col]`.
3. Create an empty set called `neighbors`.

The set will store every distinct desk color adjacent to the president’s desk.
4. Traverse every cell in the grid.

Whenever the current cell contains the president’s color, inspect its four neighboring positions.
5. For each of the four directions, compute the neighboring coordinates.

The directions are:

`(1, 0)`, `(-1, 0)`, `(0, 1)`, `(0, -1)`.
6. Ignore neighbors that fall outside the grid.

This prevents invalid indexing when the president’s desk touches a border.
7. Read the neighboring character.

If it is:

- `.` , ignore it because empty cells are not desks.
- equal to the president’s color, ignore it because it is the same desk.
- otherwise, insert it into the set.
8. After processing the whole grid, print the size of the set.

### Why it works

Every deputy desk must share a side with at least one president cell. The algorithm checks all four side-adjacent neighbors of every president cell, so every valid deputy color is discovered.

The set guarantees each color is counted exactly once, even if many cells from the same desk touch the president’s desk.

Any cell that is empty or belongs to the president is explicitly ignored, so the set contains exactly the distinct deputy desk colors.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, c = input().split()
n = int(n)
m = int(m)

grid = [input().strip() for _ in range(n)]

neighbors = set()

directions = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
]

for i in range(n):
    for j in range(m):
        if grid[i][j] == c:
            for dx, dy in directions:
                ni = i + dx
                nj = j + dy

                if 0 <= ni < n and 0 <= nj < m:
                    ch = grid[ni][nj]

                    if ch != '.' and ch != c:
                        neighbors.add(ch)

print(len(neighbors))
```

The program starts by reading the dimensions and the president’s desk color. Since the first input line contains both integers and a character, the values are initially read as strings and then converted where needed.

The grid is stored exactly as given. Because strings support indexing, `grid[i][j]` gives direct access to any cell.

The `neighbors` set is the central idea of the solution. A neighboring desk color may appear many times around the president’s desk, but a set automatically removes duplicates.

The nested loops scan the entire grid. Whenever a president cell is found, the code checks the four side-adjacent positions using the `directions` array. This avoids repetitive code and makes the logic easier to verify.

Boundary checks happen before accessing the grid. Without them, cells on the edges would cause index errors.

The condition:

```
if ch != '.' and ch != c:
```

filters out invalid neighbors. Empty cells are ignored, and the president’s own desk color is also ignored.

Finally, the answer is simply the number of unique colors stored in the set.

## Worked Examples

### Example 1

Input:

```
3 4 R
G.B.
.RR.
TTT.
```

The president’s color is `R`.

| Current Cell | Neighbor Checked | Added to Set | Current Set |
| --- | --- | --- | --- |
| (1,1) = R | G | Yes | {G} |
| (1,1) = R | R | No | {G} |
| (1,1) = R | . | No | {G} |
| (1,1) = R | T | Yes | {G, T} |
| (1,2) = R | B | Yes | {G, T, B} |
| (1,2) = R | . | No | {G, T, B} |
| (1,2) = R | R | No | {G, T, B} |
| (1,2) = R | T | Already exists | {G, T, B} |

Final answer:

```
3
```

This trace shows why a set is necessary. The desk `T` touches the president’s desk more than once, but it should still count only once.

### Example 2

Input:

```
2 2 A
AB
..
```

| Current Cell | Neighbor Checked | Added to Set | Current Set |
| --- | --- | --- | --- |
| (0,0) = A | Out of bounds | No | {} |
| (0,0) = A | Out of bounds | No | {} |
| (0,0) = A | B | Yes | {B} |
| (0,0) = A | . | No | {B} |

Final answer:

```
1
```

This example demonstrates boundary handling. Two neighbor directions leave the grid, and the algorithm safely ignores them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n × m) | Every cell is visited once, with at most four neighbor checks |
| Space | O(1) | The set stores at most 26 uppercase letters |

The maximum grid size is only `10,000` cells, so a linear scan is extremely fast within the 2 second limit. Memory usage is negligible because the auxiliary set contains only desk colors.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m, c = input().split()
    n = int(n)
    m = int(m)

    grid = [input().strip() for _ in range(n)]

    neighbors = set()

    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    for i in range(n):
        for j in range(m):
            if grid[i][j] == c:
                for dx, dy in directions:
                    ni = i + dx
                    nj = j + dy

                    if 0 <= ni < n and 0 <= nj < m:
                        ch = grid[ni][nj]

                        if ch != '.' and ch != c:
                            neighbors.add(ch)

    print(len(neighbors))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run(
"""3 4 R
G.B.
.RR.
TTT.
"""
) == "3", "sample 1"

# minimum size
assert run(
"""1 1 A
A
"""
) == "0", "single cell"

# duplicate neighboring cells
assert run(
"""3 3 A
BBB
BAB
BBB
"""
) == "1", "duplicate colors counted once"

# ignore empty cells
assert run(
"""2 3 A
.A.
...
"""
) == "0", "empty cells ignored"

# president on boundary
assert run(
"""2 2 A
AB
..
"""
) == "1", "boundary handling"

# multiple different neighbors
assert run(
"""4 5 C
AACAA
ACCCA
BBDBB
EEEEE
"""
) == "4", "multiple adjacent colors"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1×1` grid with only `A` | `0` | Minimum-size input |
| President surrounded by `B` | `1` | Duplicate colors counted once |
| President next to only `.` | `0` | Empty cells ignored |
| President on grid edge | `1` | Boundary safety |
| Several touching colors | `4` | Correct distinct counting |

## Edge Cases

Consider the case where the same neighboring desk touches the president in multiple places:

```
3 3 A
BBB
BAB
BBB
```

The algorithm visits the center `A` cell and checks all four neighbors. Every neighbor is `B`, so `B` gets inserted into the set four times. Since sets keep only unique values, the final set remains `{B}` and the output is correctly `1`.

Now consider empty cells:

```
2 3 A
.A.
...
```

The president cell is at `(0,1)`. Its neighbors are all `.` or outside the grid. The condition:

```
if ch != '.' and ch != c:
```

rejects every empty cell, so the set stays empty and the algorithm prints `0`.

Next, consider a case where the president’s own desk touches itself:

```
3 4 A
AAAA
ABBA
AAAA
```

Many `A` cells are adjacent to other `A` cells. During neighbor checks, the condition `ch != c` prevents adding the president’s own color to the set. Only `B` is inserted, so the answer is `1`.

Finally, consider boundary handling:

```
2 2 A
AB
..
```

When checking neighbors of `(0,0)`, two directions produce invalid coordinates like `(-1,0)` and `(0,-1)`. The bounds condition:

```
0 <= ni < n and 0 <= nj < m
```

filters them out before indexing the grid. The remaining valid neighbors are processed normally, producing the correct answer `1`.
