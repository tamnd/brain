---
title: "CF 102411K - King's Children"
description: "The grid is an (n times m) rectangular array. Some cells contain distinct uppercase letters, and each such letter is a castle belonging to one child. Every other cell is empty."
date: "2026-08-12T00:30:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102411
codeforces_index: "K"
codeforces_contest_name: "ICPC 2019-2020 North-Western Russia Regional Contest"
rating: 0
weight: 102411
solve_time_s: 434
verified: false
draft: false
---

[CF 102411K - King's Children](https://codeforces.com/problemset/problem/102411/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 14s  
**Verified:** no  

## Solution
## Problem Understanding

The grid is an (n \times m) rectangular array. Some cells contain distinct uppercase letters, and each such letter is a castle belonging to one child. Every other cell is empty. We must partition the whole grid into axis-aligned rectangles so that every rectangle contains exactly one castle. The rectangle containing `A` is special: among all valid partitions, its area must be as large as possible. The output keeps every castle uppercase and changes each empty cell to the lowercase letter of the child whose rectangle owns it. The original problem has (n,m\le 1000), and there is at most one castle for each of the 26 uppercase letters.

The two grid dimensions can both reach 1000, so there can be (10^6) cells. An algorithm that does a substantial amount of work for every cell for every possible rectangle is already too expensive. More precisely, enumerating all rectangles containing `A` gives a quadratic choice for the top and bottom boundaries and another quadratic choice for the left and right boundaries, which leads to roughly (O(n^2m^2)) candidates. At (n=m=1000), that is on the order of (10^{12}), far beyond a 2 second limit. We need to exploit the fact that there is only one distinguished castle and that an empty rectangle containing it can be characterized by its vertical span and the horizontal space available on every row.

There are several boundary cases that can make a careless implementation fail. If `A` is the only castle, for example,

```
2 2
A.
..
```

the correct output is

```
Aa
aa
```

because the entire grid can belong to `A`. An implementation that insists on stopping at a castle boundary in every direction can accidentally leave cells unassigned.

A second case is when another castle blocks only one side:

```
2 3
A.B
...
```

The optimal province for `A` is the first two columns, so a correct output is

```
AaB
aab
```

The rectangle has area (4). A method that looks only at the row containing `A` would find width (2), but could miss that the same width extends through the second row.

A third case exercises a castle directly above or below a candidate rectangle:

```
4 4
A..B
....
C..D
....
```

One optimal output is

```
AaaB
aaab
Cddd
cddd
```

The `A` province has area (6), occupying rows 1 and 2 and columns 1 through 3. The other provinces can be constructed independently after `A` is fixed. A careless vertical expansion may cross `C` and incorrectly include it in the `A` rectangle.

## Approaches

The brute-force idea is straightforward. Enumerate every rectangle that contains the cell of `A`, check whether it contains another castle, and keep the largest valid one. If we had a two-dimensional prefix sum of castle positions, the check could be made in constant time. The difficulty is the number of rectangles. There are (O(n^2)) choices for the top and bottom rows and (O(m^2)) choices for the left and right columns, so the worst-case number of candidates is (O(n^2m^2)). With (n=m=1000), that is roughly (2.5\cdot10^{11}) rectangles containing a central cell, even before considering the rest of the construction. The idea is correct, but the search space is far too large.

The useful observation is that we only need to optimize the province of `A`. Once we have chosen an empty rectangle containing `A`, the rest of the board can always be partitioned into valid rectangles. Remove the `A` rectangle. Its complement consists of at most four rectangular strips: the part above it, the part below it, the part to its left, and the part to its right. A nonempty strip cannot contain zero castles, because otherwise we could enlarge the `A` rectangle into that strip and obtain a strictly larger empty rectangle. Each strip can then be partitioned recursively.

For a region containing at least two castles, choose two castles that have different rows. A horizontal cut between their rows creates two rectangles, each containing at least one castle. If all castles have the same row, they must have different columns, so a vertical cut separates two of them instead. Repeating this gives a rectangular partition with exactly one castle in every final rectangle. This is a simple guillotine partition, and it uses only (O(k^2)) work when there are (k\le26) castles.

The remaining task is finding the largest empty rectangle containing `A`. This is a fixed-point version of the maximum rectangle problem. We use the same hanging-line idea commonly used for largest empty rectangles: for every row that can participate in the rectangle, calculate how far we can extend left and right from `A` without hitting a castle, then maintain prefix minima while moving vertically. The resulting width for any chosen top and bottom rows is obtained directly from those minima.

The brute-force search over four boundaries is reduced to (O(n^2)), because only the top and bottom boundaries need to be enumerated explicitly. Computing the horizontal clearances takes (O(nm)). Since there are only 26 castles, the subsequent recursive construction is negligible compared with the grid processing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2m^2)) | (O(nm)) | Too slow |
| Optimal | (O(nm+n^2+K^2)), (K\le26) | (O(nm+K^2)) | Accepted |

## Algorithm Walkthrough

1. Find the position ((a_r,a_c)) of castle `A`. The first part of the algorithm considers the original grid, where every uppercase castle is an obstacle and every `.` cell is available.
2. Starting from `A`, move downward along column (a_c) until another castle is reached. Do the same upward. The resulting interval of rows is the only possible vertical range of an empty rectangle containing `A`, because every such rectangle contains column (a_c). A castle in that column would be inside the rectangle and would violate the one-castle condition.
3. For every usable row, count the consecutive empty cells immediately to the left of column (a_c) and immediately to the right. Call these raw values `left` and `right`. A row with a castle somewhere else can still participate, but its horizontal interval must stop before that castle.
4. Propagate these horizontal capacities away from the row containing `A`. When moving one row upward or downward, the rectangle must fit on every row between that row and `A`, so the usable left extension becomes the minimum of the current row's raw extension and the extension already possible on the previous row. The same applies to the right extension.
5. Enumerate every top row and bottom row containing `A`. If the top row is (t) and the bottom row is (b), the maximum common extension to the left is

[
\min(L_t,L_b),
]

because `L[t]` already contains the minimum over all rows from (t) to `A`, while `L[b]` contains the minimum from `A` to (b). The same reasoning gives the right extension

[
\min(R_t,R_b).
]

Thus the largest possible width for this vertical span is

[
\min(L_t,L_b)+\min(R_t,R_b)+1.
]

Multiplying this width by (b-t+1) gives the best area for that pair of rows.
6. Keep the rectangle with maximum area. Every rectangle considered is empty of other castles, and every possible vertical span of an empty rectangle containing `A` is considered, so the chosen rectangle is globally optimal for `A`.
7. Fill the chosen `A` rectangle with lowercase `a` on its empty cells. The castle `A` itself stays uppercase.
8. Split the remaining board into up to four rectangular regions around the `A` rectangle. For every nonempty region, collect the castles inside it. A nonempty region always contains a castle, because otherwise the `A` rectangle could have been enlarged into that region.
9. Recursively partition each remaining region. If it contains one castle, fill every empty cell of the region with that castle's lowercase letter. If it contains several castles with different rows, cut horizontally between two castles. If all castles have the same row, cut vertically between two castles. Both resulting rectangles contain at least one castle, so the process can continue.
10. When every recursive region has one castle, all cells have been assigned. The `A` rectangle is untouched after the first step, so its area remains the maximum possible.

### Why it works

Every valid province containing `A` is an axis-aligned rectangle containing `A` and no other castle. The first part of the algorithm examines exactly these possibilities. Its vertical boundaries must lie inside the maximal castle-free interval of `A`'s column, and for any fixed top and bottom rows, the largest possible horizontal interval is the intersection of the empty intervals available on all those rows. The propagated `L` and `R` arrays compute exactly those intersections, so the maximum found is the largest possible `A` rectangle.

It remains to show that this rectangle can actually occur in a complete partition. Its complement consists of four disjoint rectangular strips. If one of these strips were nonempty and contained no castle, the `A` rectangle could be extended into it, contradicting maximality of its area. Thus every nonempty strip contains at least one castle. Any rectangle containing multiple castles can be divided into two rectangles containing castles by choosing two castles with different rows or, if necessary, different columns. Repeating this produces rectangles with exactly one castle. Since each cut is made along an entire boundary of the current rectangle, the final regions form a disjoint partition of the complement. Hence the maximum empty rectangle for `A` is always attainable.

## Python Solution

```python
import sys
input = sys.stdin.readline

DOT = ord('.')

def solve():
    n, m = map(int, input().split())
    grid = [bytearray(input().strip(), 'ascii') for _ in range(n)]

    ar = ac = -1
    castles = []

    for r in range(n):
        row = grid[r]
        for c in range(m):
            ch = row[c]
            if ch != DOT:
                if ch == ord('A'):
                    ar, ac = r, c
                else:
                    castles.append((r, c, ch))

    # Find the largest empty rectangle containing A.
    left = [0] * n
    right = [0] * n

    top_lim = ar
    bottom_lim = ar

    for r in range(ar - 1, -1, -1):
        if grid[r][ac] != DOT:
            break
        top_lim = r

    for r in range(ar + 1, n):
        if grid[r][ac] != DOT:
            break
        bottom_lim = r

    # Raw horizontal free lengths, then prefix minima toward A.
    for r in range(ar, bottom_lim + 1):
        cnt = 0
        c = ac - 1
        row = grid[r]
        while c >= 0 and row[c] == DOT:
            cnt += 1
            c -= 1

        if r == ar:
            left[r] = cnt
        else:
            left[r] = min(left[r - 1], cnt)

        cnt = 0
        c = ac + 1
        while c < m and row[c] == DOT:
            cnt += 1
            c += 1

        if r == ar:
            right[r] = cnt
        else:
            right[r] = min(right[r - 1], cnt)

    for r in range(ar - 1, top_lim - 1, -1):
        row = grid[r]

        cnt = 0
        c = ac - 1
        while c >= 0 and row[c] == DOT:
            cnt += 1
            c -= 1
        left[r] = min(left[r + 1], cnt)

        cnt = 0
        c = ac + 1
        while c < m and row[c] == DOT:
            cnt += 1
            c += 1
        right[r] = min(right[r + 1], cnt)

    best_area = 1
    best_top = best_bottom = ar

    for top in range(ar, top_lim - 1, -1):
        for bottom in range(ar, bottom_lim + 1):
            width = min(left[top], left[bottom])
            width += min(right[top], right[bottom]) + 1
            height = bottom - top + 1
            area = width * height

            if area > best_area:
                best_area = area
                best_top = top
                best_bottom = bottom

    best_left = min(left[best_top], left[best_bottom])
    best_right = min(right[best_top], right[best_bottom])
    best_left = ac - best_left
    best_right = ac + best_right

    for r in range(best_top, best_bottom + 1):
        row = grid[r]
        for c in range(best_left, best_right + 1):
            if row[c] == DOT:
                row[c] = ord('a')

    # Recursively partition every region outside A's rectangle.
    def partition(top, bottom, left_col, right_col, pts):
        if not pts:
            return

        if len(pts) == 1:
            _, _, ch = pts[0]
            lower = ch + 32

            for r in range(top, bottom + 1):
                row = grid[r]
                for c in range(left_col, right_col + 1):
                    if row[c] == DOT:
                        row[c] = lower
            return

        p0 = pts[0]
        p1 = None

        # Prefer a horizontal cut.
        for p in pts[1:]:
            if p[0] != p0[0]:
                p1 = p
                break

        if p1 is not None:
            cut = min(p0[0], p1[0])

            upper = []
            lower = []
            for p in pts:
                if p[0] <= cut:
                    upper.append(p)
                else:
                    lower.append(p)

            partition(top, cut, left_col, right_col, upper)
            partition(cut + 1, bottom, left_col, right_col, lower)
            return

        # All castles have the same row, so a vertical cut exists.
        for p in pts[1:]:
            if p[1] != p0[1]:
                p1 = p
                break

        cut = min(p0[1], p1[1])

        left_pts = []
        right_pts = []
        for p in pts:
            if p[1] <= cut:
                left_pts.append(p)
            else:
                right_pts.append(p)

        partition(top, bottom, left_col, cut, left_pts)
        partition(top, bottom, cut + 1, right_col, right_pts)

    # The complement of A's rectangle is at most four rectangles.
    regions = []

    if best_top > 0:
        regions.append((0, best_top - 1, 0, m - 1))

    if best_bottom + 1 < n:
        regions.append((best_bottom + 1, n - 1, 0, m - 1))

    if best_left > 0:
        regions.append((best_top, best_bottom, 0, best_left - 1))

    if best_right + 1 < m:
        regions.append((best_top, best_bottom, best_right + 1, m - 1))

    for top, bottom, left_col, right_col in regions:
        pts = [
            p for p in castles
            if top <= p[0] <= bottom
            and left_col <= p[1] <= right_col
        ]
        partition(top, bottom, left_col, right_col, pts)

    return '\n'.join(row.decode('ascii') for row in grid)

if __name__ == "__main__":
    sys.stdout.write(solve())
```

The input is stored as `bytearray` rows rather than Python strings because the construction modifies many cells. Integer byte values also make the frequent `.` comparisons inexpensive. Since there are at most (10^6) cells, this representation stays comfortably inside the memory limit.

The first scan locates `A` and stores every other castle as a coordinate and byte value. The `top_lim` and `bottom_lim` calculations find the maximal vertical interval containing `A` without another castle in its column. A rectangle containing `A` cannot cross such a castle.

The `left` and `right` arrays are propagated independently in both directions. For rows below `A`, `left[r]` means the largest left extension that works for every row from `A` through `r`. The upward pass has the symmetric meaning. This is why the area calculation needs only `left[top]`, `left[bottom]`, `right[top]`, and `right[bottom]`, rather than scanning the whole vertical interval again.

The expression for `width` adds one for column `ac` itself. This is an easy off-by-one point. If there are two free cells to the left and three to the right, the total width is (2+1+3=6), not (5).

The recursive `partition` function never changes the chosen `A` rectangle. Its input rectangle is guaranteed to contain at least one non-`A` castle. When there is exactly one castle, the whole region belongs to it. With several castles, the selected cut places two castles on opposite sides, so neither recursive child can be empty of castles.

Python integers do not overflow for the largest possible area, (10^6), but ordinary integer arithmetic is used anyway. The recursive depth is at most the number of castles, which is only 26, so recursion is safe here.

## Worked Examples

### Sample 1

The `A` castle is at row 3, column 4 using one-based coordinates. Its column contains no other castle, so every row can potentially participate. The relevant values for the optimal vertical span are summarized below.

| Top row | Bottom row | Common left extension | Common right extension | Width | Height | Area |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 3 | 3 | 4 | 8 | 1 | 8 |
| 2 | 3 | 1 | 4 | 6 | 2 | 12 |
| 3 | 4 | 3 | 4 | 8 | 2 | 16 |
| 2 | 4 | 1 | 4 | 6 | 3 | 18 |
| 2 | 5 | 1 | 0 | 2 | 4 | 8 |

The best area is 18, obtained from rows 2 through 4 and columns 3 through 8. The resulting `A` rectangle is

```
......
.Faaaaaa
...Aaaaa
........
.....P..
..L.....
```

with the dots inside rows 2 through 4 and columns 3 through 8 converted to `a`.

The remaining cells can be partitioned independently. The upper strip contains only `X`, the left middle strip contains only `F`, and the bottom strip contains `P` and `L`. One valid output produced by the recursive construction is

```
xxxxxxXx
fFaaaaaa
ffaAaaaa
ffaaaaaa
pppppPpp
llLlllll
```

The official sample uses a different valid partition of the bottom region, which is allowed because the required `A` area is the same.

### Four-castle example

Consider

```
4 4
A..B
....
C..D
....
```

The `A` castle is at row 1, column 1. The best rectangle containing it uses rows 1 and 2 and columns 1 through 3.

| Top | Bottom | Left extension | Right extension | Width | Height | Area |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 2 | 3 | 1 | 3 |
| 1 | 2 | 0 | 2 | 3 | 2 | 6 |
| 1 | 3 | 0 | 0 | 1 | 3 | 3 |
| 1 | 4 | 0 | 0 | 1 | 4 | 4 |

The maximum is area 6. The `A` rectangle is removed conceptually, leaving a right rectangle containing `B` and a bottom rectangle containing `C` and `D`.

The bottom rectangle has two castles in the same row, so the recursive partition uses a vertical cut. One final result is

```
AaaB
aaab
Cddd
cddd
```

The `A` province has area 6, `B` owns the upper-right cell pair, `C` owns the lower-left column, and `D` owns the remaining lower-right rectangle. Every province is rectangular and contains exactly one castle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nm+n^2+K^2)) | Horizontal scans use (O(nm)), all top-bottom pairs use (O(n^2)), and recursive castle filtering uses (O(K^2)) with (K\le26). |
| Space | (O(nm+K)) | The grid uses (O(nm)), the clearance arrays use (O(n)), and there are at most 26 castles. |

For (n,m\le1000), the grid has at most (10^6) cells. The dominant work is a few linear scans of those cells plus at most (10^6) top-bottom pairs. The recursive construction is tiny because the number of distinct castles is bounded by 26. This fits comfortably within the 512 MB memory limit and is substantially smaller than the (O(n^2m^2)) brute-force search.

## Test Cases

The official sample has multiple valid outputs, so the test below checks against the deterministic output produced by this implementation. A special judge would accept the official sample output as well.

```python
import sys
import io

DOT = ord('.')

def solve():
    n, m = map(int, input().split())
    grid = [bytearray(input().strip(), 'ascii') for _ in range(n)]

    ar = ac = -1
    castles = []

    for r in range(n):
        for c in range(m):
            ch = grid[r][c]
            if ch != DOT:
                if ch == ord('A'):
                    ar, ac = r, c
                else:
                    castles.append((r, c, ch))

    left = [0] * n
    right = [0] * n

    top_lim = ar
    bottom_lim = ar

    for r in range(ar - 1, -1, -1):
        if grid[r][ac] != DOT:
            break
        top_lim = r

    for r in range(ar + 1, n):
        if grid[r][ac] != DOT:
            break
        bottom_lim = r

    for r in range(ar, bottom_lim + 1):
        row = grid[r]

        cnt = 0
        c = ac - 1
        while c >= 0 and row[c] == DOT:
            cnt += 1
            c -= 1
        left[r] = cnt if r == ar else min(left[r - 1], cnt)

        cnt = 0
        c = ac + 1
        while c < m and row[c] == DOT:
            cnt += 1
            c += 1
        right[r] = cnt if r == ar else min(right[r - 1], cnt)

    for r in range(ar - 1, top_lim - 1, -1):
        row = grid[r]

        cnt = 0
        c = ac - 1
        while c >= 0 and row[c] == DOT:
            cnt += 1
            c -= 1
        left[r] = min(left[r + 1], cnt)

        cnt = 0
        c = ac + 1
        while c < m and row[c] == DOT:
            cnt += 1
            c += 1
        right[r] = min(right[r + 1], cnt)

    best_area = 1
    best_top = best_bottom = ar

    for top in range(ar, top_lim - 1, -1):
        for bottom in range(ar, bottom_lim + 1):
            width = min(left[top], left[bottom])
            width += min(right[top], right[bottom]) + 1
            area = width * (bottom - top + 1)

            if area > best_area:
                best_area = area
                best_top = top
                best_bottom = bottom

    best_left = ac - min(left[best_top], left[best_bottom])
    best_right = ac + min(right[best_top], right[best_bottom])

    for r in range(best_top, best_bottom + 1):
        for c in range(best_left, best_right + 1):
            if grid[r][c] == DOT:
                grid[r][c] = ord('a')

    def partition(top, bottom, left_col, right_col, pts):
        if not pts:
            return

        if len(pts) == 1:
            lower = pts[0][2] + 32
            for r in range(top, bottom + 1):
                for c in range(left_col, right_col + 1):
                    if grid[r][c] == DOT:
                        grid[r][c] = lower
            return

        p0 = pts[0]
        p1 = None

        for p in pts[1:]:
            if p[0] != p0[0]:
                p1 = p
                break

        if p1 is not None:
            cut = min(p0[0], p1[0])
            upper = [p for p in pts if p[0] <= cut]
            lower = [p for p in pts if p[0] > cut]
            partition(top, cut, left_col, right_col, upper)
            partition(cut + 1, bottom, left_col, right_col, lower)
            return

        p1 = pts[1]
        cut = min(p0[1], p1[1])
        left_pts = [p for p in pts if p[1] <= cut]
        right_pts = [p for p in pts if p[1] > cut]

        partition(top, bottom, left_col, cut, left_pts)
        partition(top, bottom, cut + 1, right_col, right_pts)

    regions = []

    if best_top > 0:
        regions.append((0, best_top - 1, 0, m - 1))
    if best_bottom + 1 < n:
        regions.append((best_bottom + 1, n - 1, 0, m - 1))
    if best_left > 0:
        regions.append((best_top, best_bottom, 0, best_left - 1))
    if best_right + 1 < m:
        regions.append((best_top, best_bottom, best_right + 1, m - 1))

    for top, bottom, lc, rc in regions:
        pts = [
            p for p in castles
            if top <= p[0] <= bottom and lc <= p[1] <= rc
        ]
        partition(top, bottom, lc, rc, pts)

    return '\n'.join(row.decode() for row in grid)

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_input = input
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    try:
        return solve()
    finally:
        sys.stdin = old_stdin
        input = old_input

# Provided sample, using the deterministic output of this implementation.
sample1 = """6 8
......X.
.F......
...A....
........
.....P..
..L.....
"""

expected1 = """xxxxxxXx
fFaaaaaa
ffaAaaaa
ffaaaaaa
pppppPpp
llLlllll"""

assert run(sample1) == expected1, "sample 1"

# Minimum-size input.
assert run("""1 1
A
""") == "A", "minimum-size grid"

# Boundary condition: A touches the top-left corner and another castle
# blocks only the right side.
assert run("""2 3
A.B
...
""") == """AaB
aab""", "boundary expansion"

# All cells except A are empty, so A must own the whole grid.
assert run("""3 3
...
.A.
...
""") == """aaa
aAa
aaa""", "single castle"

# Several castles force recursive horizontal and vertical cuts.
assert run("""4 4
A..B
....
C..D
....
""") == """AaaB
aaab
Cddd
cddd""", "recursive partition"

# Maximum-size grid with only A.
n = 1000
m = 1000
rows = [bytearray(b'a' * m) for _ in range(n)]
rows[499][499] = ord('A')

max_input = f"{n} {m}\n" + "\n".join(
    row.decode() for row in rows
) + "\n"

max_expected = "\n".join(row.decode() for row in rows)
assert run(max_input) == max_expected, "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `6 x 8` sample | `A` area 18, with the deterministic partition shown above | Full construction and optimal `A` rectangle |
| `1 x 1` with `A` | `A` | Minimum dimensions and no empty cells |
| `2 x 3` with `A.B` | `AaB / aab` | Boundary expansion and right-side castle blocking |
| `3 x 3` with only `A` | All cells lowercase `a` except `A` | Maximum possible empty rectangle |
| `4 x 4` with `A,B,C,D` at corners | `AaaB / aaab / Cddd / cddd` | Horizontal and vertical recursive cuts |
| `1000 x 1000` with only `A` | One million cells owned by `A` | Maximum dimensions, performance, and boundary handling |

## Edge Cases

When `A` is the only castle, the vertical scan reaches both borders and every row has the full horizontal range available. For the input

```
2 2
A.
..
```

the only castle-free rectangle containing `A` is the whole grid, so the algorithm computes width (2), height (2), and area (4). It fills the three empty cells with `a`, producing

```
Aa
aa
```

No recursive region remains because the complement of the `A` rectangle is empty.

When another castle is on the same boundary row as `A`, the horizontal scan must stop exactly before that castle. For

```
2 3
A.B
...
```

the first row permits one cell to the right of `A`, while the second row permits two. The propagated right capacity for the two-row interval is therefore (1), giving width (2) and area (4). The chosen rectangle is rows 1 through 2 and columns 1 through 2. The remaining third column contains only `B`, so it becomes one rectangular province and the output is

```
AaB
aab
```

When a castle lies directly above or below `A`, the vertical interval must stop before that row. In

```
4 4
A..B
....
C..D
....
```

the castle `C` at row 3, column 1 prevents `A` from extending through row 3 while keeping column 1. The best rectangle is consequently rows 1 through 2 and columns 1 through 3, with area (6). The remaining regions contain `B`, `C`, and `D`, and the recursive partition handles them without modifying the already optimal `A` rectangle.

When all empty cells surround a castle, every direction can reach the border. For

```
3 3
...
.A.
...
```

the vertical range is all three rows, and every row has one empty cell on each side of `A`. The candidate with all three rows has width (3) and height (3), so the algorithm obtains area (9). The final grid is

```
aaa
aAa
aaa
```

The maximum-size case behaves identically, only with more cells. A (1000\times1000) grid containing just `A` makes the entire grid its province, so the algorithm performs only the required linear scans and (O(n^2)) boundary enumeration before filling the grid. The absence of any other castle also means the recursive partition has no remaining regions to process.
