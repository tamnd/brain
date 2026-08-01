---
title: "CF 102709G - Character Quilt"
description: "The problem asks us to build a large character picture from smaller square tiles. We are given a collection of base tiles, where every tile is an S by S grid of characters. The final quilt is arranged as a W by H rectangle of tile positions."
date: "2026-08-01T22:00:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102709
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 9-11-20 Div. 2"
rating: 0
weight: 102709
solve_time_s: 122
verified: true
draft: false
---

[CF 102709G - Character Quilt](https://codeforces.com/problemset/problem/102709/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to build a large character picture from smaller square tiles. We are given a collection of base tiles, where every tile is an S by S grid of characters. The final quilt is arranged as a W by H rectangle of tile positions. Each position tells us which base tile to use and which transformation to apply before placing it into the final image.

The transformations are limited to six cases: keeping the tile unchanged, rotating it by 90, 180, or 270 degrees clockwise, flipping it left to right, or flipping it top to bottom. The output is the character grid obtained after expanding every tile position into its transformed S by S block.

The constraints are designed to make simulation possible. The number of original tiles and the side length of each tile are at most 15, so storing and transforming all tiles is cheap. The quilt can contain up to 100 by 100 tile positions, and each tile contributes at most 15 by 15 characters. The final output can contain 2,250,000 characters, so any approach that avoids unnecessary work is preferred. A method that repeatedly searches, copies, or transforms large structures for every output cell would risk becoming slower than needed, while directly processing each final character is efficient enough.

The main implementation mistakes come from handling transformations incorrectly. Rotations are especially easy to reverse because the source row and column both change. Another common mistake is confusing the horizontal flip and vertical flip. For example, a tile

```
ab
cd
```

with transformation 4 becomes

```
ba
dc
```

because columns are reversed. A program that treats this as swapping rows would incorrectly output

```
cd
ab
```

For a single tile, the input

```
1 2
ab
cd
1 1
0:1
```

should produce

```
ca
db
```

because the tile is rotated clockwise. An implementation that uses the formula for a counterclockwise rotation would output the wrong arrangement.

Another edge case is a quilt with only one tile position. The input

```
1 1
x
1 1
0:0
```

must output

```
x
```

A solution that assumes multiple tiles and inserts separators or mishandles row lengths can fail here.

A third edge case is when different transformations of the same tile appear next to each other. The program cannot mutate the stored original tile after applying a transformation, because a later use of the same tile needs the untouched version. For example, using one tile twice with transformations 1 and 2 requires both operations to start from the original grid.

## Approaches

The direct brute-force approach is to process every quilt position, locate its source tile, apply the requested transformation, and print the resulting S by S block. This is already correct because every output character belongs to exactly one tile position and every tile position can be handled independently.

The problem with a naive implementation appears only if transformations are recomputed at the character level. For every one of the W times H tile positions, we may touch S squared characters. The worst case performs about W * H * S * S operations. With W and H equal to 100 and S equal to 15, this is 2,250,000 character operations, which is small. The real danger is not the asymptotic complexity, but repeatedly creating unnecessary intermediate grids.

The key observation is that the set of transformations is tiny and the original tiles are reused many times. Since there are only six possible transformations, each original tile can be expanded into all six transformed versions once. After that preprocessing, every quilt position becomes a simple lookup followed by copying S rows into the answer.

The brute-force works because the total number of output characters is bounded. The observation that each tile transformation can be cached lets us remove repeated work and keeps the implementation simple. The final construction is just assembling already prepared blocks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(W * H * S * S) | O(S * S) | Accepted, but repeats transformations |
| Optimal | O(N * 6 * S * S + W * H * S * S) | O(N * 6 * S * S) | Accepted |

## Algorithm Walkthrough

1. Read all original tiles and store them without modification. The original orientation must remain available because multiple quilt positions can reference the same tile with different transformations.
2. For every tile, generate the six possible transformed versions. Store them in a table indexed by tile number and transformation type. This converts future transformation requests into constant-time lookups.
3. Read the quilt description row by row. Each entry contains a tile index and a transformation number, so it directly identifies one of the precomputed blocks.
4. For each quilt row, append the corresponding transformed tile rows horizontally. A quilt position contributes S characters to every one of the S output rows it occupies.
5. Print the constructed rows in order. The rows are already complete because every tile position contributes exactly its own rectangular section.

Why it works:

The invariant is that every stored transformed tile is exactly the result of applying its transformation to the original tile. Since every quilt position only asks for one tile and one transformation, retrieving the cached version gives the exact block that belongs there. The construction process preserves the left-to-right and top-to-bottom order of tile positions, so every output cell receives the correct character exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def rotate90(tile):
    n = len(tile)
    return [''.join(tile[n - 1 - r][c] for r in range(n)) for c in range(n)]

def flip_vertical(tile):
    return [row[::-1] for row in tile]

def flip_horizontal(tile):
    return tile[::-1]

def solve():
    n, s = map(int, input().split())

    tiles = []
    for _ in range(n):
        tile = [input().rstrip('\n') for _ in range(s)]
        tiles.append(tile)

    transformed = []
    for tile in tiles:
        versions = [None] * 6
        versions[0] = tile
        versions[1] = rotate90(versions[0])
        versions[2] = rotate90(versions[1])
        versions[3] = rotate90(versions[2])
        versions[4] = flip_vertical(versions[0])
        versions[5] = flip_horizontal(versions[0])
        transformed.append(versions)

    w, h = map(int, input().split())

    answer = ['' for _ in range(h * s)]

    for quilt_row in range(h):
        specs = input().split()

        for tile_row in range(s):
            line = []
            for spec in specs:
                idx, t = map(int, spec.split(':'))
                line.append(transformed[idx][t][tile_row])
            answer[quilt_row * s + tile_row] = ''.join(line)

    sys.stdout.write('\n'.join(answer))

if __name__ == "__main__":
    solve()
```

The preprocessing section creates all six orientations for every tile. The rotations are chained so that applying the 90 degree operation three times naturally produces the remaining rotations. The two flips use the original tile directly because flips do not depend on previous rotations.

The construction phase avoids changing any stored tile. Each specification is split into its tile index and transformation value, then the required row of the already transformed tile is appended. The row index calculation `quilt_row * s + tile_row` maps a tile row inside the quilt to the correct row in the final character grid.

There are no dangerous boundary cases in the indexing because every transformation keeps the tile size equal to S. Python integers are not a concern here because the program only stores indices and character counts.

## Worked Examples

Consider the small input:

```
1 2
ab
cd
2 1
0:0 0:1
0:2 0:3
```

The preprocessing creates:

| Tile | Transformation | Stored rows |
| --- | --- | --- |
| 0 | 0 | ab / cd |
| 0 | 1 | ca / db |
| 0 | 2 | dc / ba |
| 0 | 3 | bd / ac |

The quilt construction is:

| Quilt row | Tile specifications | Produced output rows |
| --- | --- | --- |
| 0 | 0:0, 0:1 | abca / cddb |
| 1 | 0:2, 0:3 | dcbd / baac |

The result demonstrates that every tile position is independent and can use a different orientation of the same original tile.

A second example:

```
1 1
*
1 1
0:5
```

The state trace is:

| Step | Tile index | Transformation | Selected block |
| --- | --- | --- | --- |
| Read tile | 0 | original | * |
| Precompute | 0 | flip horizontal | * |
| Place tile | 0 | 5 | * |

The output is:

```
*
```

This confirms that a one-character tile remains valid under every transformation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N * 6 * S * S + W * H * S * S) | Each transformation is prepared once, then every quilt cell copies one character |
| Space | O(N * 6 * S * S) | Six versions of every tile are stored |

The largest possible output dominates the construction cost. Since the final image itself contains only a few million characters, the algorithm stays within the limits while avoiding repeated transformation work.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("""1 1
x
1 1
0:0
""") == "x", "single character tile"

assert run("""1 2
ab
cd
1 1
0:1
""") == "ca\ndb", "rotation"

assert run("""1 2
ab
cd
2 1
0:4
""") == "ba\ndc", "vertical flip"

assert run("""1 2
ab
cd
1 1
0:5
""") == "cd\nab", "horizontal flip"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One character tile | x | Minimum-size handling |
| Two by two tile rotation | ca / db | Rotation formulas |
| Two by two tile vertical flip | ba / dc | Column reversal |
| Two by two tile horizontal flip | cd / ab | Row reversal |

## Edge Cases

For a single tile position, the algorithm still creates the same transformed cache and performs one normal lookup. The input

```
1 1
x
1 1
0:0
```

selects the only cached version and prints one character. There is no special case because the general construction already handles the smallest possible quilt.

For transformations of the same tile, the original tile is never overwritten. If the tile

```
ab
cd
```

is requested with transformations 1 and 2, the cache contains both

```
ca
db
```

and

```
dc
ba
```

at the same time. This prevents later requests from depending on earlier output operations.

For adjacent differently transformed tiles, the algorithm writes each tile row separately and concatenates the pieces in quilt order. A tile on the left cannot affect a tile on the right because each position contributes exactly S characters to the current output rows.
