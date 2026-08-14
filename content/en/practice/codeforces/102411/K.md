---
title: "CF 102411K - King's Children"
description: "We have an (n times m) grid. Some cells contain distinct uppercase letters, each letter representing one child's castle, while every other cell is empty. The task is to replace every empty cell by the lowercase letter of the child whose rectangular province contains that cell."
date: "2026-08-14T14:39:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102411
codeforces_index: "K"
codeforces_contest_name: "ICPC 2019-2020 North-Western Russia Regional Contest"
rating: 0
weight: 102411
solve_time_s: 476
verified: false
draft: false
---

[CF 102411K - King's Children](https://codeforces.com/problemset/problem/102411/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We have an (n \times m) grid. Some cells contain distinct uppercase letters, each letter representing one child's castle, while every other cell is empty. The task is to replace every empty cell by the lowercase letter of the child whose rectangular province contains that cell. Every province must be a rectangle containing exactly one castle, and the province containing `A` must have maximum possible area. The original uppercase castle cells remain unchanged in the output. The official constraints are (1 \le n,m \le 1000), and there are at most 26 castles because every uppercase letter is distinct.

The (1000 \times 1000) bound means there can be one million cells, so any solution should be close to linear or quadratic in one grid dimension, rather than enumerating all possible rectangles. With (n=m=1000), there are already (10^6) cells, while (n^2m^2) is (10^{12}). The small alphabet is the second useful constraint: there can be only 26 provinces, so after finding the optimal province for `A`, we can afford to do considerably more work per castle, although the solution below does not need to.

The first tricky case is when `A` is on a boundary. For example,

```
A..
...
..B
```

The largest province for `A` is not necessarily just the first row or first column. Here the rectangle consisting of the first two rows has area 6, so a valid optimal output is

```
Aaa
aaa
bbB
```

A solution that only tries to expand symmetrically around `A` can miss this rectangle.

Another subtle case is a different castle blocking only one direction. For

```
A.B
```

`A` can own the first two cells, but it cannot cross `B`. The correct output is

```
AaB
```

Treating every non-`A` cell as empty while searching for `A` would incorrectly give `A` the whole row.

A third issue is that several maximum rectangles can have the same area. For

```
A.
.B
```

`A` can take the first row or the first column, both with area 2. One valid result is

```
Aa
bB
```

A correct implementation must not depend on a particular tie being the unique optimum. Any maximum rectangle is sufficient.

## Approaches

A direct approach is to enumerate every rectangle containing `A`, check whether it contains another castle, and keep the largest valid one. Even with a two-dimensional prefix sum that makes the validity check (O(1)), the number of rectangles containing a fixed cell can reach

[
500\cdot501\cdot500\cdot501
=62,750,250,000
]

when the grid is (1000\times1000) and `A` is near the center. That many candidates cannot be considered within two seconds. Checking every cell inside every candidate would be much worse.

The useful observation is that a rectangle containing `A` is determined by its top row, bottom row, left boundary, and right boundary. Once the top and bottom rows are fixed, the best possible horizontal boundaries can be found independently from the rows. For each row between the chosen top and bottom, count how many empty cells can be taken immediately to the left and right of `A`. The rectangle can use only the minimum left extension and minimum right extension among all rows in the interval.

Suppose `A` is at column (c). Let (L_i) be the number of cells that can be taken to the left of `A` on row (i), and (R_i) the corresponding number on the right. After propagating minimum values away from the row containing `A`, (L_i) and (R_i) represent the extensions that are simultaneously available throughout the interval between row (i) and `A`.

For a top row (u) and bottom row (d), the maximum width is then

[
\min(L_u,L_d)+\min(R_u,R_d)+1.
]

The `+1` is the column containing `A`. Trying all pairs of top and bottom rows takes (O(n^2)), while computing the horizontal extensions takes (O(nm)). This is enough for the constraints.

Once the optimal `A` rectangle is fixed, the rest of the problem becomes a construction problem. The key is to partition the area outside that rectangle recursively. The complement of a rectangle inside a larger rectangle consists of at most four rectangular bands: above, below, left, and right.

Every nonempty one of those bands must contain another castle. If, for example, the band above `A` contained no castle, the `A` rectangle could be extended upward, contradicting its maximality. The same argument applies to all four sides.

Now consider any rectangular region containing several castles. If their row coordinates are not all equal, cut the region horizontally between the minimum and maximum castle rows. Both resulting rectangles contain at least one castle. If all castles lie on one row, their columns are different, so a vertical cut separates them. Repeating this operation eventually leaves rectangles containing exactly one castle. This gives a valid province partition without changing the already optimal `A` rectangle.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2m^2)) with prefix sums | (O(nm)) | Too slow |
| Optimal | (O(nm+n^2+K^2)), (K\le26) | (O(nm+K)) | Accepted |

## Algorithm Walkthrough

1. Find the position of `A` and record the positions of all other castles. We will optimize only `A`, because once its maximum possible rectangle is fixed, the remaining cells can be partitioned independently.
2. Find the consecutive rows around `A` that are usable by an `A` rectangle. Starting from the row containing `A`, move upward and downward while the cell in `A`'s column is either `A` itself or `.`. A different castle in that column blocks every rectangle from crossing its row.
3. For every usable row, compute the number of consecutive dots immediately to the left and right of `A`'s column. These are the raw horizontal extensions for that row. A castle anywhere on the corresponding side stops the extension.
4. Propagate minimum horizontal extensions away from the row containing `A`. Moving downward, replace each value by the minimum of its own raw extension and the value from the previous row. Do the symmetric operation upward. After this, (L_i) represents the largest left extension that is available on every row between `A` and row (i), and (R_i) has the analogous meaning on the right.
5. Enumerate every possible top row and bottom row containing `A`. For each pair, compute

[
width=\min(L_{top},L_{bottom})+\min(R_{top},R_{bottom})+1
]

and multiply it by the height. Keep the rectangle with maximum area.

The endpoint minima are sufficient because the propagated arrays already contain the minimum extension over the entire interval from `A` to that endpoint.
6. Paint the chosen rectangle with lowercase `a`, leaving the uppercase `A` unchanged. No other castle lies inside it, because every horizontal and vertical extension was stopped by castles.
7. Consider the four rectangular bands outside the `A` rectangle. For each nonempty band, collect the castles lying inside it and recursively partition that band.
8. For a recursive region containing one castle, give the entire region to that castle. It is already a rectangle containing exactly one castle, so no further cut is needed.
9. For a region containing several castles, check their row coordinates. If they are not all equal, choose a horizontal boundary between the smallest and largest castle rows. Otherwise choose a vertical boundary between the smallest and largest castle columns. Recursively solve the two resulting regions.
10. Print the completed grid. Every original castle remains uppercase, while every empty cell has been assigned a lowercase owner.

### Why it works

For the `A` province, consider any valid rectangle containing `A`. Its top and bottom rows are some pair (u,d). On every row between them, its left boundary cannot go farther left than the consecutive empty cells before the first castle, and similarly on the right. The propagated (L) and (R) values capture exactly those common limits, so the width computed for (u,d) is the largest possible width for that vertical interval. Since every possible top and bottom pair is examined, the selected rectangle has maximum possible area among all rectangles that can legally contain `A`.

After fixing this rectangle, every nonempty side band contains a castle, because otherwise `A` could have been extended into that band. Any rectangular region containing multiple castles can always be split by a horizontal or vertical boundary so that both sides contain at least one castle. Recursion eventually produces rectangles containing exactly one castle, and the cuts are disjoint and cover the original region. Thus all cells are assigned to exactly one valid province, while the `A` province remains globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_grid(n, m, rows):
    grid = [list(row) for row in rows]

    castles = []
    ar = ac = -1

    for r in range(n):
        for c in range(m):
            ch = grid[r][c]
            if 'A' <= ch <= 'Z':
                if ch == 'A':
                    ar, ac = r, c
                else:
                    castles.append((r, c, ch))

    # Find the vertical interval that an A-rectangle can occupy.
    lo = ar
    while lo > 0 and grid[lo - 1][ac] == '.':
        lo -= 1

    hi = ar
    while hi + 1 < n and grid[hi + 1][ac] == '.':
        hi += 1

    raw_l = [0] * n
    raw_r = [0] * n

    # Horizontal empty runs around A for every usable row.
    for r in range(lo, hi + 1):
        c = ac - 1
        cnt = 0
        row = grid[r]

        while c >= 0 and row[c] == '.':
            cnt += 1
            c -= 1
        raw_l[r] = cnt

        c = ac + 1
        cnt = 0
        while c < m and row[c] == '.':
            cnt += 1
            c += 1
        raw_r[r] = cnt

    # Propagate minima from A downwards and upwards.
    left = [0] * n
    right = [0] * n

    left[ar] = raw_l[ar]
    right[ar] = raw_r[ar]

    for r in range(ar + 1, hi + 1):
        left[r] = min(raw_l[r], left[r - 1])
        right[r] = min(raw_r[r], right[r - 1])

    for r in range(ar - 1, lo - 1, -1):
        left[r] = min(raw_l[r], left[r + 1])
        right[r] = min(raw_r[r], right[r + 1])

    # Find the maximum-area rectangle containing A.
    best_area = 1
    best_top = best_bottom = ar

    for top in range(ar, lo - 1, -1):
        for bottom in range(ar, hi + 1):
            width = (
                min(left[top], left[bottom])
                + min(right[top], right[bottom])
                + 1
            )
            area = width * (bottom - top + 1)

            if area > best_area:
                best_area = area
                best_top = top
                best_bottom = bottom

    best_left = ac - min(left[best_top], left[best_bottom])
    best_right = ac + min(right[best_top], right[best_bottom])

    # Reserve A's optimal province.
    for r in range(best_top, best_bottom + 1):
        row = grid[r]
        for c in range(best_left, best_right + 1):
            if row[c] == '.':
                row[c] = 'a'

    def fill_region(r1, r2, c1, c2, pts):
        if not pts:
            return

        if len(pts) == 1:
            _, _, ch = pts[0]
            lower = ch.lower()

            for r in range(r1, r2 + 1):
                row = grid[r]
                for c in range(c1, c2 + 1):
                    if row[c] == '.':
                        row[c] = lower
            return

        min_r = min(p[0] for p in pts)
        max_r = max(p[0] for p in pts)

        if min_r != max_r:
            cut = (min_r + max_r) // 2

            top_pts = [p for p in pts if p[0] <= cut]
            bottom_pts = [p for p in pts if p[0] > cut]

            fill_region(r1, cut, c1, c2, top_pts)
            fill_region(cut + 1, r2, c1, c2, bottom_pts)
        else:
            min_c = min(p[1] for p in pts)
            max_c = max(p[1] for p in pts)
            cut = (min_c + max_c) // 2

            left_pts = [p for p in pts if p[1] <= cut]
            right_pts = [p for p in pts if p[1] > cut]

            fill_region(r1, r2, c1, cut, left_pts)
            fill_region(r1, r2, cut + 1, c2, right_pts)

    def process_region(r1, r2, c1, c2):
        if r1 > r2 or c1 > c2:
            return

        pts = [
            p for p in castles
            if r1 <= p[0] <= r2 and c1 <= p[1] <= c2
        ]
        fill_region(r1, r2, c1, c2, pts)

    # The complement of A's rectangle consists of at most four rectangles.
    process_region(0, best_top - 1, 0, m - 1)
    process_region(best_bottom + 1, n - 1, 0, m - 1)
    process_region(best_top, best_bottom, 0, best_left - 1)
    process_region(best_top, best_bottom, best_right + 1, m - 1)

    return [''.join(row) for row in grid]

def solve():
    n, m = map(int, input().split())
    rows = [input().strip() for _ in range(n)]
    print('\n'.join(solve_grid(n, m, rows)))

if __name__ == "__main__":
    solve()
```

The first part locates `A` and all other castles. The castle list is kept separately from the mutable grid, which makes the later recursive partitioning independent of the lowercase cells that have already been written.

The vertical interval is found before computing horizontal extensions. A different castle in `A`'s column is a hard barrier, so rows beyond it can never participate in an `A` province.

The raw left and right runs inspect only cells immediately adjacent to `A`'s column. The propagation step is what changes these raw values into interval-wide limits. Without that propagation, using only the two endpoint rows would incorrectly ignore a blocking castle in the middle of the interval.

The maximum-area search uses strict `>` when comparing areas. Equal-area rectangles are both valid, so retaining the first one avoids unnecessary tie handling.

The recursive partition never modifies the `A` rectangle. Each side region is disjoint from it, and each recursive cut divides one rectangle into two smaller rectangles. When only one castle remains in a region, the entire region can be painted with that child's lowercase letter.

There is no integer overflow issue in Python. The largest area is only (10^6), although Python integers would handle substantially larger values as well.

## Worked Examples

The official sample has `A` at row 2, column 3 using zero-based coordinates. The useful horizontal extensions after vertical propagation are as follows.

| Row | Raw left | Raw right | Propagated left | Propagated right |
| --- | --- | --- | --- | --- |
| 0 | 3 | 2 | 1 | 2 |
| 1 | 1 | 4 | 1 | 4 |
| 2 | 3 | 4 | 3 | 4 |
| 3 | 3 | 4 | 3 | 4 |
| 4 | 3 | 1 | 3 | 1 |
| 5 | 0 | 4 | 0 | 1 |

For the interval from row 1 through row 3, the width is

[
\min(1,3)+\min(4,4)+1=6,
]

so the area is (6\cdot3=18). The chosen rectangle is rows 1 through 3 and columns 2 through 7.

| Top | Bottom | Width | Height | Area | Best |
| --- | --- | --- | --- | --- | --- |
| 2 | 2 | 8 | 1 | 8 | rows 2..2 |
| 1 | 2 | 6 | 2 | 12 | rows 1..2 |
| 1 | 3 | 6 | 3 | 18 | rows 1..3 |
| 0 | 3 | 4 | 4 | 16 | rows 1..3 |
| 1 | 4 | 5 | 4 | 20 | rows 1..4 |

The final row in the table shows why the propagated values matter: although row 4 itself has three cells available to the left, its right side is blocked by `P`, so extending the rectangle downward reduces the width. The actual best interval is determined by considering all pairs, not just by taking the widest individual rows.

For a second example, consider

```
2 2
A.
.B
```

The row containing `A` has one free cell to its right. The second row has no free cell to the right because `B` occupies that position.

| Top | Bottom | Width | Height | Area | Best |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 1 | 2 | rows 0..0 |
| 0 | 1 | 1 | 2 | 2 | rows 0..0 |

The two choices have equal area, so the strict comparison keeps the first rectangle. `A` owns the first row. The remaining second row is a rectangle containing only `B`, so it becomes `bB`. The final output is

```
Aa
bB
```

This example demonstrates both the tie case and the recursive construction. The optimal area for `A` is 2 regardless of which maximum rectangle is selected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nm+n^2+K^2)) | Horizontal runs scan the grid once, top and bottom rows give (O(n^2)) candidates, and recursive point filtering costs at most (O(K^2)) |
| Space | (O(nm+K)) | The mutable grid dominates memory, while the extension arrays and castle list are linear |

With (n,m\le1000), (nm) is at most one million and (n^2) is also at most one million. The number of castles satisfies (K\le26), so the recursive construction is tiny compared with the grid operations. The solution stays comfortably within the 512 MB memory limit and avoids the (10^{12})-scale rectangle enumeration that makes brute force impractical.

## Test Cases

The test harness below assumes the solution is saved as `solution.py` and imports its `solve_grid` function.

```python
from solution import solve_grid

def run(inp: str) -> str:
    lines = inp.strip().splitlines()
    n, m = map(int, lines[0].split())
    rows = lines[1:]
    return "\n".join(solve_grid(n, m, rows))

# Provided sample
assert run(
    """6 8
......X.
.F......
...A....
........
.....P..
..L.....
"""
) == """xxxxxxXx
fFaaaaaa
ffaAaaaa
ffaaaaaa
pppppPpp
llLlllll""", "sample 1"

# Constructed sample 2: two maximum rectangles of equal area for A.
assert run(
    """2 2
A.
.B
"""
) == """Aa
bB""", "sample 2, tie between maximum A rectangles"

# Minimum-size input.
assert run(
    """1 1
A
"""
) == """A""", "minimum grid"

# Boundary condition and a castle blocking A's expansion.
assert run(
    """1 3
A.B
"""
) == """AaB""", "boundary and horizontal blocker"

# A at the corner, with the optimal rectangle using two rows.
assert run(
    """3 3
A..
...
..B
"""
) == """Aaa
aaa
bbB""", "corner A and maximum rectangle"

# Maximum-size legal grid with no other castles.
# The requested all-equal-castle case is illegal because all letters
# must be distinct, so this stresses the analogous all-empty interior.
n = m = 1000
rows = ["A" + "." * 999] + ["." * 1000 for _ in range(999)]
inp = f"{n} {m}\n" + "\n".join(rows)

expected = "\n".join(
    ["A" + "a" * 999] + ["a" * 1000 for _ in range(999)]
)

assert run(inp) == expected, "maximum-size grid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Official (6\times8) sample | `A` gets rows 1..3 and columns 2..7 | General construction and optimal `A` rectangle |
| `A.` / `.B` | `Aa` / `bB` | Equal-area choices and recursive partitioning |
| `A` | `A` | Minimum dimensions |
| `A.B` | `AaB` | Boundary handling and castle blocking horizontal expansion |
| `A..` / `...` / `..B` | `Aaa` / `aaa` / `bbB` | Corner position and a two-row optimal rectangle |
| (1000\times1000), only `A` | Entire grid owned by `A` | Maximum dimensions and the case with no competing castles |

## Edge Cases

When `A` occupies the only cell,

```
A
```

the vertical interval has one row, both horizontal extensions are zero, and the only candidate rectangle has area 1. There are no other regions to partition, so the output remains `A`.

When another castle blocks a direction, as in

```
A.B
```

the raw right extension of `A` is 1 because the dot at column 1 is free and `B` at column 2 stops the scan. The best rectangle has width 2. The remaining one-cell region contains `B`, so the result is `AaB`. The castle is never treated as an empty cell during the search.

When several maximum rectangles have the same area,

```
A.
.B
```

the first candidate is the one-cell-high rectangle covering the first row, with area 2. Extending downward produces a one-column-wide rectangle of area 2 as well. Since the comparison is strict, the first maximum is retained. The complement is the second row, which is assigned to `B`, producing `Aa` and `bB`. Either maximum choice would satisfy the optimization requirement.

When `A` is on a corner but can expand through several rows, as in

```
A..
...
..B
```

the propagated right extension is 2 on the first two rows, while `B` limits the third row. The candidate covering rows 0 and 1 has width 3 and height 2, giving area 6. No rectangle containing `A` can include the third row while keeping that width. The selected `A` rectangle is thus the first two rows, and the remaining bottom row contains only `B`, giving `Aaa`, `aaa`, `bbB`.

The maximum-size case with only `A` is also useful because every cell is eligible for the favorite child. The horizontal extension reaches the right boundary on every row, the vertical interval reaches the bottom boundary, and the maximum rectangle is the entire (1000\times1000) grid. Since there are no other castles, the recursive partition has nothing to process after reserving `A`'s rectangle.
