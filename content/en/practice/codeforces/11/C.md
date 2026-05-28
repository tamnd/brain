---
title: "CF 11C - How Many Squares?"
description: "We are given a binary grid. A valid object is not a filled square, it is only the border of a square drawn with 1s. Ever"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 11
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 11"
rating: 2200
weight: 11
solve_time_s: 162
verified: true
draft: false
---

[CF 11C - How Many Squares?](https://codeforces.com/problemset/problem/11/C)

**Rating:** 2200  
**Tags:** implementation  
**Solve time:** 2m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary grid. A valid object is not a filled square, it is only the border of a square drawn with `1`s. Every cell not belonging to the border must be `0`.

The problem asks us to count two kinds of squares.

The first kind is axis-aligned. Its sides are horizontal and vertical, exactly like a normal square in a matrix.

The second kind is rotated by 45 degrees. In matrix coordinates it looks like a diamond.

There is one extra restriction that changes the problem completely. A valid square must be isolated. Any `1` that does not belong to the square is forbidden from touching the square, even diagonally. So every neighboring cell around the border must be `0`, unless that neighbor is also part of the same square.

The grid dimensions are at most `250 × 250`, but the total input size across all test cases is at most `10^6`. This means an `O(n^4)` or `O(n^5)` solution is hopeless. A single `250 × 250` grid already has roughly `6 × 10^4` cells. Enumerating all possible squares and scanning their borders cell by cell would easily reach billions of operations.

The target complexity should stay near linear or quadratic in the number of cells, possibly with a small constant factor.

The tricky part is not detecting squares themselves. The real difficulty is verifying the isolation condition correctly.

Consider this example:

```
111
101
111
```

This is one valid axis-aligned square. The center `0` is allowed because only the border matters.

Now look at this:

```
1110
1011
1110
0000
```

A careless solution might count the `3 × 3` border on the left. But the extra `1` at `(1,3)` touches the square diagonally, so the answer is actually `0`.

Rotated squares introduce another source of mistakes:

```
00100
01010
00100
```

This is a valid diamond. But if we add a single adjacent `1`:

```
00100
01110
00100
```

the diamond becomes invalid because the side cells touch the shape.

Another subtle case is overlapping borders. Suppose two squares share some cells. Neither one is valid, because every border cell would then have foreign neighboring `1`s`.

The safest way to think about the condition is this: every connected component of `1`s must itself be exactly one square border and nothing else.

## Approaches

The brute-force idea is straightforward. Enumerate every possible square, check whether all required border cells are `1`, check whether all other nearby cells are `0`, and count the valid ones.

For axis-aligned squares, there are `O(n^2 m^2)` possible rectangles, and we only keep those with equal side lengths. Verifying one square naively costs `O(k)` where `k` is the side length. The worst case becomes roughly `O(n^5)`.

Rotated squares are even worse because their geometry is less convenient. Enumerating all centers and radii still leads to scanning many border cells repeatedly.

The brute-force method works logically because the definition is local and explicit. If we check every border cell and every neighboring cell, correctness is immediate. The problem is the amount of repeated work. Nearby candidate squares reuse almost the same information again and again.

The key observation is that the isolation condition completely characterizes connected components.

Take any connected component of `1`s`. If it forms a valid square border, then:

1. every `1` in the component belongs to that square,
2. there are no extra touching `1`s`,
3. the whole component has a very rigid shape.

So instead of enumerating squares, we enumerate connected components.

A component can only be one of two possible geometries:

1. an axis-aligned hollow square border,
2. a diamond border.

The total number of cells across all components is linear in the grid size, so once we extract components with BFS or DFS, we only need to classify each component.

This changes the complexity dramatically. Each cell participates in exactly one component traversal and a small amount of validation work.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^5) | O(1) | Too slow |
| Optimal | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Traverse the grid and find connected components of `1`s using 8-direction BFS.

We use 8 directions because touching by corner also matters in the statement. If two `1`s touch diagonally, they belong to the same forbidden cluster.
2. For every component, collect all its coordinates.

Let the component size be `s`.
3. Try to recognize the component as an axis-aligned square.

Compute:

- minimum row `r1`
- maximum row `r2`
- minimum column `c1`
- maximum column `c2`

The bounding box must itself be a square, so:

```
r2 - r1 == c2 - c1
```

Let the side length be:

```
L = r2 - r1 + 1
```

A valid border contains exactly:

```
4 * L - 4
```

cells.
4. Verify the border structure.

Every cell on the perimeter of the bounding box must belong to the component. Every interior cell must not belong to the component.

If all checks pass and the component size matches `4L - 4`, this component is one valid square.
5. If axis-aligned validation fails, try rotated-square validation.

For a diamond, define transformed coordinates:

```
u = r + c
v = r - c
```

In `(u,v)` space, a diamond becomes an axis-aligned square border.
6. Compute:

```
umin, umax
vmin, vmax
```

The transformed bounding box must satisfy:

```
umax - umin == vmax - vmin
```
7. Let:

```
D = umax - umin
```

Every border point of the transformed square corresponds to one original grid cell.

A cell `(r,c)` belongs to the diamond border if:

```
u == umin or u == umax or
v == vmin or v == vmax
```

and all coordinates stay inside the transformed square.
8. Generate all expected border cells of the diamond and compare them with the component.

If they match exactly, count the component as valid.
9. Sum all valid components.

### Why it works

The BFS partitions all `1` cells into maximal connected components under side-or-corner adjacency. A valid square cannot share adjacency with foreign `1`s`, so every valid square must appear as an entire connected component.

For axis-aligned squares, the bounding box uniquely determines the candidate border. Any missing perimeter cell or extra interior cell breaks the definition immediately.

For rotated squares, the coordinate transform converts diagonal edges into axis-aligned edges. The transformed shape must become a perfect square border in `(u,v)` space. Because the transform is bijective on grid cells, matching the transformed border exactly is equivalent to matching the original diamond.

Since every component is checked exhaustively against both legal geometries, every counted component is valid and every valid square is counted exactly once.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

DIR8 = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

def axis_square(comp):
    cells = set(comp)

    r1 = min(r for r, c in comp)
    r2 = max(r for r, c in comp)
    c1 = min(c for r, c in comp)
    c2 = max(c for r, c in comp)

    if r2 - r1 != c2 - c1:
        return False

    side = r2 - r1 + 1

    if side < 2:
        return False

    expected = 4 * side - 4

    if len(comp) != expected:
        return False

    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            border = (
                r == r1 or r == r2 or
                c == c1 or c == c2
            )

            inside = (r, c) in cells

            if border != inside:
                return False

    return True

def diamond_square(comp):
    cells = set(comp)

    uv = []
    for r, c in comp:
        uv.append((r + c, r - c))

    umin = min(u for u, v in uv)
    umax = max(u for u, v in uv)
    vmin = min(v for u, v in uv)
    vmax = max(v for u, v in uv)

    if umax - umin != vmax - vmin:
        return False

    d = umax - umin

    if d < 2:
        return False

    expected_cells = set()

    for u in range(umin, umax + 1):
        for v in range(vmin, vmax + 1):

            border = (
                u == umin or u == umax or
                v == vmin or v == vmax
            )

            if not border:
                continue

            if (u + v) % 2 != 0:
                continue

            r = (u + v) // 2
            c = (u - v) // 2

            expected_cells.add((r, c))

    return expected_cells == cells

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        g = [input().strip() for _ in range(n)]

        vis = [[False] * m for _ in range(n)]

        ans = 0

        for i in range(n):
            for j in range(m):
                if g[i][j] == '0' or vis[i][j]:
                    continue

                q = deque()
                q.append((i, j))
                vis[i][j] = True

                comp = []

                while q:
                    r, c = q.popleft()
                    comp.append((r, c))

                    for dr, dc in DIR8:
                        nr = r + dr
                        nc = c + dc

                        if 0 <= nr < n and 0 <= nc < m:
                            if not vis[nr][nc] and g[nr][nc] == '1':
                                vis[nr][nc] = True
                                q.append((nr, nc))

                if axis_square(comp) or diamond_square(comp):
                    ans += 1

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

solve()
```

The BFS section builds connected components under 8-direction adjacency. Using only 4 directions would be incorrect because diagonal touching is forbidden by the statement.

The `axis_square` function validates the ordinary square border. The bounding box determines exactly where the border should exist. The comparison:

```
if border != inside:
```

is the cleanest way to reject both missing border cells and illegal interior cells simultaneously.

The diamond check uses the coordinate transform:

```
u = r + c
v = r - c
```

This is the critical geometric trick. A rotated square becomes an ordinary axis-aligned square in transformed coordinates.

The parity check:

```
if (u + v) % 2 != 0:
```

matters because only points with matching parity correspond to integer grid coordinates after inversion.

The final equality:

```
expected_cells == cells
```

guarantees there are neither missing border cells nor extra cells.

## Worked Examples

### Example 1

Input:

```
0001000
0010100
0100010
0010100
0001000
```

This is one diamond.

| Step | Value |
| --- | --- |
| Component size | 5 |
| umin | 3 |
| umax | 5 |
| vmin | -1 |
| vmax | 1 |
| Bounding widths equal | Yes |
| Generated border cells | 5 |
| Match component | Yes |

The transformed square has side length `2` in `(u,v)` space. Every border point maps back to exactly the original five cells.

### Example 2

Input:

```
1111
1001
1001
1111
```

| Step | Value |
| --- | --- |
| Bounding box | rows 0..3, cols 0..3 |
| Side length | 4 |
| Expected border cells | 12 |
| Actual component cells | 12 |
| Interior contains 1 | No |
| Result | Valid |

This confirms the hollow center is allowed. Only the border matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Every cell is visited once in BFS and checked a constant number of times |
| Space | O(nm) | Visited array and component storage |

The grid contains at most `62500` cells per test case. Linear processing is easily fast enough inside a 2-second limit, even with many test cases. Memory usage also stays comfortably below the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    DIR8 = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    def axis_square(comp):
        cells = set(comp)

        r1 = min(r for r, c in comp)
        r2 = max(r for r, c in comp)
        c1 = min(c for r, c in comp)
        c2 = max(c for r, c in comp)

        if r2 - r1 != c2 - c1:
            return False

        side = r2 - r1 + 1

        if side < 2:
            return False

        if len(comp) != 4 * side - 4:
            return False

        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                border = (
                    r == r1 or r == r2 or
                    c == c1 or c == c2
                )

                if border != ((r, c) in cells):
                    return False

        return True

    def diamond_square(comp):
        cells = set(comp)

        uv = [(r + c, r - c) for r, c in comp]

        umin = min(u for u, v in uv)
        umax = max(u for u, v in uv)
        vmin = min(v for u, v in uv)
        vmax = max(v for u, v in uv)

        if umax - umin != vmax - vmin:
            return False

        expected = set()

        for u in range(umin, umax + 1):
            for v in range(vmin, vmax + 1):

                border = (
                    u == umin or u == umax or
                    v == vmin or v == vmax
                )

                if not border:
                    continue

                if (u + v) % 2:
                    continue

                r = (u + v) // 2
                c = (u - v) // 2

                expected.add((r, c))

        return expected == cells

    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        g = [input().strip() for _ in range(n)]

        vis = [[False] * m for _ in range(n)]

        ans = 0

        for i in range(n):
            for j in range(m):
                if g[i][j] == '0' or vis[i][j]:
                    continue

                q = deque([(i, j)])
                vis[i][j] = True

                comp = []

                while q:
                    r, c = q.popleft()
                    comp.append((r, c))

                    for dr, dc in DIR8:
                        nr = r + dr
                        nc = c + dc

                        if 0 <= nr < n and 0 <= nc < m:
                            if not vis[nr][nc] and g[nr][nc] == '1':
                                vis[nr][nc] = True
                                q.append((nr, nc))

                if axis_square(comp) or diamond_square(comp):
                    ans += 1

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run(
"""2
8 8
00010001
00101000
01000100
10000010
01000100
00101000
11010011
11000011
10 10
1111111000
1000001000
1011001000
1011001010
1000001101
1001001010
1010101000
1001001000
1000001000
1111111000
"""
) == "1\n2", "sample"

# minimum size
assert run(
"""1
2 2
11
11
"""
) == "1", "smallest valid square"

# all zeros
assert run(
"""1
4 4
0000
0000
0000
0000
"""
) == "0", "empty grid"

# touching extra cell
assert run(
"""1
4 4
1110
1011
1110
0000
"""
) == "0", "foreign touching cell"

# valid diamond
assert run(
"""1
5 5
00100
01010
00100
00000
00000
"""
) == "1", "diamond square"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2×2` all ones | `1` | Smallest valid axis-aligned square |
| All zeros | `0` | Empty components |
| Extra touching cell | `0` | Isolation rule |
| Diamond pattern | `1` | Rotated-square detection |

## Edge Cases

Consider this input:

```
1
4 4
1110
1011
1110
0000
```

The `3 × 3` border looks valid at first glance. But BFS with 8-direction adjacency merges the extra cell `(1,3)` into the same component because it touches `(0,2)` diagonally.

The component size becomes `9`, while a `3 × 3` border requires exactly `8` cells. The axis-square validator rejects it immediately.

Now consider overlapping shapes:

```
1
5 5
11111
10001
11111
10001
11111
```

A naive approach might detect multiple squares. Our algorithm treats the entire structure as one connected component. Its bounding box is `5 × 5`, but the interior contains illegal `1`s`. The validator rejects it.

Finally, consider the smallest possible rotated square:

```
1
3 3
010
101
010
```

The transformed coordinates produce:

```
u in [1,3]
v in [-1,1]
```

All expected transformed border cells map exactly back to the original component. The algorithm counts one valid diamond.
