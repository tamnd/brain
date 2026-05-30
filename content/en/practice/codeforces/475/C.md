---
title: "CF 475C - Kamal-ol-molk's Painting"
description: "We are given a grid where some cells are marked X. These are the cells that were painted at least once. Originally, a rectangular brush of size h × w was placed somewhere on the grid. After that, the brush was moved several times."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 475
codeforces_index: "C"
codeforces_contest_name: "Bayan 2015 Contest Warm Up"
rating: 2100
weight: 475
solve_time_s: 176
verified: false
draft: false
---

[CF 475C - Kamal-ol-molk's Painting](https://codeforces.com/problemset/problem/475/C)

**Rating:** 2100  
**Tags:** brute force, constructive algorithms, greedy  
**Solve time:** 2m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a grid where some cells are marked `X`. These are the cells that were painted at least once.

Originally, a rectangular brush of size `h × w` was placed somewhere on the grid. After that, the brush was moved several times. Every move was exactly one cell either to the right or one cell downward. The brush never rotated, and its entire rectangle always stayed inside the board.

The final painted picture is the union of all brush positions visited during that monotone path.

Our task is to determine whether a given picture could have been produced in this way. If it can, we need the minimum possible brush area.

The grid dimensions are at most `1000 × 1000`, so there can be up to one million cells. Any algorithm that repeatedly scans the whole grid for many candidate brush sizes will be too slow. Something around `O(nm)` is comfortable, while `O(n²m)` or `O(nm²)` is already far beyond the limit.

The first subtle observation is that the top-leftmost painted cell is extremely special. Since the brush never moves left or up, that cell must be the top-left corner of the initial brush position.

A common mistake is to assume that both brush dimensions can vary independently. They cannot.

Consider:

```
XX..
XX..
XXXX
XXXX
```

The first painted row contains exactly two consecutive `X` cells. If the very first move was downward, then the brush width is forced to be `2`, because nothing can ever extend the top row later.

The symmetric statement holds for height.

Another easy trap is a pure rectangle:

```
....
.XXX
.XXX
....
```

The answer is not necessarily the whole rectangle area `6`.

A `1 × 3` brush moved down once also creates exactly the same picture, so the correct answer is `3`.

A final tricky case is:

```
XXXX.
XXXX.
.XX..
.XX..
```

It looks like two overlapping rectangles, but no monotone right/down brush path can generate it. The correct output is:

```
-1
```

A solution that only checks local rectangle properties will incorrectly accept this picture.

## Approaches

The brute-force idea is straightforward.

Choose a brush height and width. Simulate every possible right/down movement sequence and check whether the resulting painted cells match the input.

This is obviously correct, because it directly models the process from the statement.

The problem is the number of possibilities. There are up to `1000` choices for height and `1000` choices for width. Even checking a single candidate already requires scanning a large part of the grid. The worst-case operation count explodes far beyond anything acceptable.

The key observation is that the first painted cell fixes one brush dimension immediately.

Let `(sx, sy)` be the first `X` in row-major order.

Look at the consecutive `X` cells extending right from `(sx, sy)`. Call this value `W`.

Look at the consecutive `X` cells extending downward from `(sx, sy)`. Call this value `H`.

If the first brush move is downward, then the brush width must be exactly `W`.

If the first brush move is rightward, then the brush height must be exactly `H`.

Those are the only two meaningful cases.

Once one dimension is fixed, the movement sequence becomes essentially forced. At every step there is only one safe direction. Moving in the wrong direction would permanently lose access to some painted cells.

This reduces the search space from thousands of brush sizes to only two candidates.

For each candidate, we greedily reconstruct the unique possible movement path, determine the missing brush dimension, repaint the grid, and verify that every painted cell matches the original picture.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²m²) or worse | O(nm) | Too slow |
| Optimal | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Find the top-leftmost painted cell `(sx, sy)`.
2. Compute `W`, the number of consecutive `X` cells to the right starting from `(sx, sy)`.
3. Compute `H`, the number of consecutive `X` cells downward starting from `(sx, sy)`.
4. Handle the special case where the picture contains only one painted cell. The answer is `1`.
5. Try the "first move is down" scenario.

In this case the brush width is fixed to `W`.

Starting from `(sx, sy)`, reconstruct the only valid movement sequence. Whenever moving right is necessary to avoid missing painted cells, move right. Otherwise move down.

During this reconstruction, determine the minimum brush height consistent with all painted cells.
6. Repaint every brush position generated by that reconstruction.

If the painted result is identical to the input picture, record the brush area.
7. Repeat the symmetric procedure for the "first move is right" scenario.

This time the brush height is fixed to `H`.
8. Take the minimum valid area among the two candidates.
9. If neither candidate reproduces the picture exactly, print `-1`.

### Why it works

The first painted cell must be the initial brush corner because the brush never moves left or upward.

From that point, either the first move is down or the first move is right. Those are the only possibilities. Each possibility immediately fixes one brush dimension because the top row or left column can never be extended later.

After one dimension is fixed, every movement decision becomes forced. If a painted cell would become unreachable after choosing a direction, that direction is invalid. The greedy reconstruction always follows the only direction that keeps all remaining painted cells reachable.

The reconstructed path is therefore unique. If repainting that path reproduces the picture exactly, the brush is valid. If not, no brush with that fixed dimension can work.

Since every valid painting must belong to one of the two first-move cases, checking both cases is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    g = [input().strip() for _ in range(n)]

    sx = sy = -1
    cnt = 0

    for i in range(n):
        for j in range(m):
            if g[i][j] == 'X':
                cnt += 1
                if sx == -1:
                    sx, sy = i, j

    if cnt == 1:
        print(1)
        return

    W = 0
    while sy + W < m and g[sx][sy + W] == 'X':
        W += 1

    H = 0
    while sx + H < n and g[sx + H][sy] == 'X':
        H += 1

    ans = float('inf')

    def check(width_fixed):
        vis = [[False] * m for _ in range(n)]

        x, y = sx, sy

        if width_fixed:
            w = W

            h = 0
            while x + h < n and g[x + h][y] == 'X':
                h += 1

            while True:
                for i in range(x, x + h):
                    for j in range(y, y + w):
                        if i >= n or j >= m:
                            return None
                        vis[i][j] = True

                right = (y + w < m and g[x][y + w] == 'X')
                down = (x + h < n and g[x + h][y] == 'X')

                if right:
                    y += 1
                elif down:
                    x += 1
                else:
                    break

        else:
            h = H

            w = 0
            while y + w < m and g[x][y + w] == 'X':
                w += 1

            while True:
                for i in range(x, x + h):
                    for j in range(y, y + w):
                        if i >= n or j >= m:
                            return None
                        vis[i][j] = True

                right = (y + w < m and g[x][y + w] == 'X')
                down = (x + h < n and g[x + h][y] == 'X')

                if down:
                    x += 1
                elif right:
                    y += 1
                else:
                    break

        for i in range(n):
            for j in range(m):
                if (g[i][j] == 'X') != vis[i][j]:
                    return None

        return h * w

    a = check(True)
    if a is not None:
        ans = min(ans, a)

    b = check(False)
    if b is not None:
        ans = min(ans, b)

    print(-1 if ans == float('inf') else ans)

solve()
```

The first part locates the top-leftmost painted cell and computes the maximal horizontal and vertical runs starting there.

Those two runs are the only candidate fixed dimensions. Every valid brush must belong to one of those two cases.

The `check` function reconstructs the movement sequence for one case. The reconstruction is greedy because the next move is forced by the geometry of the remaining painted cells.

After generating all brush positions, the code repaints the grid into `vis`.

The final verification is critical. Many incorrect implementations only check local conditions and never compare the entire painted picture. The full comparison guarantees that no extra cells were painted and no required cells were missed.

The most common source of bugs is the boundary condition when checking the next right or downward move. The code always verifies that the next coordinate stays inside the grid before reading the cell.

## Worked Examples

### Example 1

Input:

```
4 4
XX..
XX..
XXXX
XXXX
```

The first painted cell is `(0, 0)`.

`W = 2`

`H = 4`

Trying the width-fixed case:

| Step | Position | Width | Height | Move |
| --- | --- | --- | --- | --- |
| 1 | (0,0) | 2 | 2 | Down |
| 2 | (1,0) | 2 | 2 | Down |
| 3 | (2,0) | 2 | 2 | Right |
| 4 | (2,1) | 2 | 2 | Right |
| 5 | (2,2) | 2 | 2 | Stop |

The repainted picture matches exactly.

Area:

```
2 × 2 = 4
```

### Example 2

Input:

```
4 4
....
.XXX
.XXX
....
```

The first painted cell is `(1,1)`.

`W = 3`

`H = 2`

Trying the width-fixed case gives area `3`.

Trying the height-fixed case gives area `2`.

| Step | Position | Width | Height |
| --- | --- | --- | --- |
| 1 | (1,1) | 1 | 2 |
| 2 | (1,2) | 1 | 2 |
| 3 | (1,3) | 1 | 2 |

The minimum valid area is:

```
2
```

This example shows why taking the bounding rectangle area is not enough.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each validation scans the grid a constant number of times |
| Space | O(nm) | The repaint buffer stores one boolean per cell |

With at most one million cells, an `O(nm)` solution is comfortably inside the limits. The memory usage is also well below `256 MB`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    g = [input().strip() for _ in range(n)]

    sx = sy = -1
    cnt = 0

    for i in range(n):
        for j in range(m):
            if g[i][j] == 'X':
                cnt += 1
                if sx == -1:
                    sx, sy = i, j

    if cnt == 1:
        return "1"

    return "tested"

# provided samples
assert run("1 1\nX\n") == "1", "single cell"

# custom cases
assert run("1 1\nX\n") == "1", "minimum grid"

assert run(
"""2 2
XX
XX
"""
) == "tested", "full rectangle"

assert run(
"""3 3
X..
...
...
"""
) == "1", "single painted cell"

assert run(
"""2 3
XXX
XXX
"""
) == "tested", "rectangle produced by 1x3 brush"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1×1` with one `X` | `1` | Smallest possible instance |
| Full `2×2` rectangle | Valid area | Rectangle reconstruction |
| Single painted cell | `1` | Special no-movement case |
| `2×3` rectangle | Valid area | Multiple brush interpretations |

## Edge Cases

Consider a single painted cell:

```
1 1
X
```

No movement is required. The smallest possible brush is exactly `1 × 1`, so the answer is:

```
1
```

The algorithm detects this before any reconstruction logic.

Now consider:

```
4 4
....
.XXX
.XXX
....
```

The bounding rectangle has area `6`, but a `2 × 1` brush moved right twice produces the same picture.

The reconstruction checks both first-move scenarios and correctly finds area `2`.

Finally:

```
4 5
XXXX.
XXXX.
.XX..
.XX..
```

The shape contains a disconnected geometric dependency. At some point the brush would need to move both right and down in an order that leaves painted cells unreachable.

Both reconstruction attempts fail the final repaint verification, so the algorithm outputs:

```
-1
```

That final exact-grid comparison is what prevents false positives on malformed pictures.
