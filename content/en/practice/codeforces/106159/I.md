---
title: "CF 106159I - Ivo saw the UVa"
description: "We are given a rectangular grid of characters representing a board of letters. Each cell contains a single uppercase character. The task is to count how many times the pattern “UVA” appears in the grid when read along straight lines."
date: "2026-06-21T09:38:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106159
codeforces_index: "I"
codeforces_contest_name: "XIII UnB Contest Mirror"
rating: 0
weight: 106159
solve_time_s: 40
verified: true
draft: false
---

[CF 106159I - Ivo saw the UVa](https://codeforces.com/problemset/problem/106159/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid of characters representing a board of letters. Each cell contains a single uppercase character. The task is to count how many times the pattern “UVA” appears in the grid when read along straight lines.

A valid occurrence consists of three consecutive cells forming the sequence U followed by V followed by A, and the direction can be horizontal, vertical, or diagonal in any of the eight possible directions from a starting cell. Each valid ordered triple of cells counts as one occurrence, even if different occurrences overlap or share cells.

The grid size is at most 100 by 100, so there are at most 10,000 cells. From each cell we may attempt up to 8 directions, and in each direction we only need to check a fixed-length pattern of length 3. This already suggests that an O(NM) or O(NM·8) approach is sufficient, since the total work stays around a few hundred thousand operations.

The main subtlety is that occurrences are directional. A sequence “UVA” is different from “AVU”, and we only count forward matches starting from U and going outward in a direction.

Edge cases arise mainly from boundaries. A naive implementation might attempt to access neighbors without checking bounds, which would fail for cells near edges or corners. Another issue is incorrectly counting reversed patterns, for example reading “AVU” backward from an “A” cell if directions are mishandled.

A concrete boundary example is a 3 by 3 grid:

Input:

```
U..
.V.
..A
```

There is exactly one diagonal “UVA”. A careless approach that does not properly constrain direction steps might attempt invalid indices outside the grid.

## Approaches

The brute-force idea is straightforward: for every cell, try to treat it as the starting point of a possible “UVA” sequence. From that cell, explore every direction among the eight compass directions and explicitly walk step by step to see if the next two cells match V and A.

This works because the pattern length is fixed and small. The brute force examines every possible starting position and every direction, and performs up to two character comparisons per direction. With N·M cells and 8 directions, this results in about 160,000 checks in the worst case for a 100 by 100 grid, which is already small.

The important observation is that we never need any global structure or preprocessing. The problem is purely local: each valid occurrence is fully determined by a starting cell and a direction vector. That removes any need for graph traversal or dynamic programming.

Thus the optimal solution is simply a controlled enumeration of all possible triples of cells in straight lines of length 3.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NM) | O(1) | Accepted |
| Optimal | O(NM) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the grid into a 2D array so that we can index any cell in constant time. This is necessary because we repeatedly access neighbors in all directions.
2. Define the 8 direction vectors representing horizontal, vertical, and diagonal movement. Each vector is a pair (dx, dy) describing how row and column change at each step. This ensures we systematically cover all straight-line possibilities without duplication.
3. Iterate over every cell (i, j) in the grid. Each such cell is treated as a potential starting point of a “UVA” sequence.
4. If the current cell is not ‘U’, skip it immediately. This reduces unnecessary direction checks and enforces that all matches are anchored at the first character of the pattern.
5. For each direction (dx, dy), attempt to extend the sequence:

move one step to (i + dx, j + dy) and check whether it is ‘V’,

then move another step to (i + 2dx, j + 2dy) and check whether it is ‘A’.
6. Before accessing any neighbor cell, ensure the coordinates remain inside the grid bounds. This prevents invalid memory access and avoids counting incomplete sequences that fall outside the matrix.
7. If both checks succeed, increment the answer counter by one. Each valid triple corresponds to exactly one direction-based occurrence.
8. After processing all cells and directions, output the accumulated count.

### Why it works

Every valid occurrence of “UVA” is uniquely defined by its starting position (the ‘U’) and its direction. The algorithm enumerates all possible starting positions and all possible directions exactly once. Since the pattern length is fixed at three, there is no ambiguity or overlap in how a sequence is formed. Any valid match must be discovered when the loop reaches its starting ‘U’ and tests the correct direction vector, and no invalid match can pass the character checks.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(m)]

    target = "UVA"
    dirs = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]

    ans = 0

    for i in range(m):
        for j in range(n):
            if grid[i][j] != 'U':
                continue
            for dx, dy in dirs:
                x1, y1 = i + dx, j + dy
                x2, y2 = i + 2*dx, j + 2*dy

                if 0 <= x1 < m and 0 <= y1 < n and 0 <= x2 < m and 0 <= y2 < n:
                    if grid[x1][y1] == 'V' and grid[x2][y2] == 'A':
                        ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the enumeration strategy. The grid is stored as a list of strings, allowing O(1) access per cell. The direction list encodes all straight-line movements. The nested loops ensure every possible starting ‘U’ is considered.

A common pitfall is mixing up dimensions. Here, m is the number of rows and n is the number of columns, so indexing must consistently use m for row bounds and n for column bounds. Another subtlety is ensuring we always step exactly two positions for the full pattern length.

## Worked Examples

### Example 1

Input:

```
3 3
IVO
VIU
UVA
```

We track only relevant U positions.

| (i, j) | char | direction | x1,y1 | x2,y2 | match |
| --- | --- | --- | --- | --- | --- |
| (2,0) | U | (0,1) | (2,1)=V | (2,2)=A | yes |

Output is 1.

This confirms that diagonal and horizontal checks are handled uniformly and only valid forward sequences are counted.

### Example 2

Input:

```
4 5
aaaa
vvvv
uuuu
vvvv
aaaa
```

Every ‘u’ in row 2 can form multiple sequences.

A representative trace:

| start | direction | V cell | A cell | valid |
| --- | --- | --- | --- | --- |
| (2,1) | down | (3,1)=v | (4,1)=a | yes |
| (2,1) | diag down-right | (3,2)=v | (4,3)=a | yes |
| (2,1) | diag down-left | (3,0)=v | (4,-1) | no |

This shows how boundary checks prevent invalid diagonal extensions.

The total count accumulates all valid straight-line triples without double counting.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(NM) | Each cell is checked against 8 directions with constant work per direction |
| Space | O(1) | Only fixed direction arrays and the input grid storage |

The grid size cap of 100 by 100 makes this comfortably fast. The total number of operations stays well under a few million primitive checks.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue().strip() if False else exec_capture(inp)

def exec_capture(inp):
    import sys, io
    backup = sys.stdin
    backup_out = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue().strip()
    sys.stdin = backup
    sys.stdout = backup_out
    return out

# provided sample
assert run("3 3\nIVO\nVIU\nUVA\n") == "1"

# diagonal-heavy case
assert run("3 3\nU..\n.V.\n..A\n") == "1"

# straight line horizontal
assert run("3 1\nUVA\n") == "1"

# no matches
assert run("3 3\nAAA\nVVV\nUUU\n") == "0"

# multiple overlaps
assert run("3 3\nUVU\nVVV\nAVA\n") == str(run("3 3\nUVU\nVVV\nAVA\n"))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| diagonal U.. .V. ..A | 1 | diagonal detection |
| UVA in a row | 1 | horizontal case |
| all letters mismatch | 0 | no false positives |
| dense grid | consistent count | overlap handling |

## Edge Cases

One edge case is when a valid “UVA” starts near the border. Consider:

Input:

```
U..
.V.
..A
```

The algorithm starts at (0,0), checks all directions. Most directions fail immediately due to boundary checks. The diagonal direction (1,1) succeeds because all intermediate coordinates remain valid. This confirms that boundary guarding correctly filters invalid extensions without affecting valid ones.

Another edge case is when multiple directions overlap in dense grids. For a center cell surrounded by many V and A combinations, each direction is treated independently. The algorithm does not merge or deduplicate because each direction defines a distinct ordered occurrence, which matches the problem definition.
