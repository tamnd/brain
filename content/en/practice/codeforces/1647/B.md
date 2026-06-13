---
title: "CF 1647B - Madoka and the Elegant Gift"
description: "We are given a binary grid. A black subrectangle is any axis-aligned rectangle consisting entirely of 1s. Among all black rectangles, a rectangle is called nice if it cannot be extended into a larger black rectangle that contains it."
date: "2026-06-10T04:05:42+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "graphs", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1647
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 777 (Div. 2)"
rating: 1200
weight: 1647
solve_time_s: 118
verified: true
draft: false
---

[CF 1647B - Madoka and the Elegant Gift](https://codeforces.com/problemset/problem/1647/B)

**Rating:** 1200  
**Tags:** brute force, constructive algorithms, graphs, implementation  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary grid. A black subrectangle is any axis-aligned rectangle consisting entirely of `1`s.

Among all black rectangles, a rectangle is called nice if it cannot be extended into a larger black rectangle that contains it. In other words, it is maximal with respect to containment.

The grid is called elegant when no two nice rectangles share any cell.

At first glance, this definition sounds complicated because it talks about all possible all-`1` rectangles and their containment relationships. The challenge is to determine whether such overlapping maximal rectangles can exist.

The grid dimensions are at most `100 × 100`, and the sums of all row counts and column counts across test cases are bounded by `777`. This is a very small input size. Even an `O(nm(n+m))` solution is easily acceptable. What is not acceptable is enumerating all possible rectangles, because a `100 × 100` grid contains roughly `25 million` rectangles, and checking each one would be far too expensive.

The main difficulty is recognizing what the definition of elegant really means in terms of the shape formed by the `1`s.

Several edge cases are easy to misinterpret.

Consider

```
11
11
```

The correct answer is `YES`.

All four cells form a single maximal black rectangle. A naive approach that only checks whether adjacent `1`s exist would incorrectly reject it.

Consider

```
10
01
```

The correct answer is `YES`.

The two `1`s touch only diagonally. They belong to separate maximal rectangles and do not intersect.

Consider

```
11
10
```

The correct answer is `NO`.

The three `1`s form an L-shape. One maximal rectangle is the top row, another maximal rectangle is the left column. They overlap at the upper-left cell, so the grid is not elegant.

A careless implementation that only counts connected components would incorrectly accept this case because all `1`s belong to a single component.

Another important example is

```
111
101
111
```

The correct answer is `NO`.

The hole in the center prevents the entire shape from being a rectangle. Multiple maximal black rectangles overlap around the corners, creating intersecting nice rectangles.

The solution comes from understanding exactly which shapes of `1`s are allowed.

## Approaches

The brute-force interpretation follows the definition directly.

We could enumerate every axis-aligned rectangle, check whether it consists entirely of `1`s, determine whether it is maximal, collect all nice rectangles, and then test every pair for intersection.

A grid of size `100 × 100` contains approximately

$$\frac{100\cdot101}{2}\cdot\frac{100\cdot101}{2} \approx 25\,000\,000$$

rectangles.

Even before checking their contents, this is already far beyond what can be processed within the time limit.

The key observation is that the actual definition collapses into a very simple geometric property.

Take any connected component of `1`s using four-directional adjacency.

If that component itself forms a filled rectangle, then there is exactly one maximal black rectangle inside it, namely the whole component. No overlap problem exists.

If the component does not form a filled rectangle, then inside its bounding box there must be at least one missing cell. Such a shape necessarily contains an L-turn, a corner where a horizontal run of `1`s and a vertical run of `1`s meet. Those two runs generate different maximal black rectangles sharing the corner cell. Hence two nice rectangles intersect.

This means:

A grid is elegant if and only if every connected component of `1`s forms a complete rectangle.

Once we discover this property, the problem becomes very small. For every connected component, compute its bounding box. If the component contains exactly every cell of that bounding box, the component is rectangular. Otherwise the answer is immediately `NO`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Extremely large, roughly O(n²m²) rectangles plus validation | Large | Too slow |
| Optimal | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Iterate through all cells of the grid.
2. Whenever an unvisited cell containing `1` is found, start a BFS or DFS to discover its entire connected component.
3. While traversing the component, record:

- The minimum row index.
- The maximum row index.
- The minimum column index.
- The maximum column index.
- The number of cells in the component.
4. After the traversal finishes, compute the area of the component's bounding rectangle.

```
area = (max_row - min_row + 1) × (max_col - min_col + 1)
```
5. Compare the component size with the bounding rectangle area.

If they are different, some cell inside the bounding rectangle is missing. The component is not a filled rectangle, so the grid cannot be elegant. Output `NO`.
6. Continue processing all components.
7. If every component passes the check, output `YES`.

Why is comparing the area enough? Because every cell of the component lies inside the bounding box. If the number of component cells equals the box area, then every position inside the box must belong to the component. The component is exactly a rectangle.

### Why it works

The crucial property is that a connected component of `1`s is safe precisely when it is a filled rectangle.

If a component is a filled rectangle, then the entire component is one maximal black rectangle. Any smaller black rectangle is contained inside it and is not nice. No pair of nice rectangles can intersect.

If a component is not a filled rectangle, then its bounding box contains at least one missing cell. Such a shape cannot be represented by a single maximal rectangle. At least two maximal black rectangles are required, and they overlap somewhere inside the component. Those overlapping maximal rectangles are nice rectangles, violating elegance.

Thus every connected component must be rectangular, and checking that condition is both necessary and sufficient.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n, m = map(int, input().split())
    g = [input().strip() for _ in range(n)]

    vis = [[False] * m for _ in range(n)]
    ok = True

    for r in range(n):
        for c in range(m):
            if g[r][c] != '1' or vis[r][c]:
                continue

            q = deque([(r, c)])
            vis[r][c] = True

            min_r = max_r = r
            min_c = max_c = c
            cnt = 0

            while q:
                x, y = q.popleft()
                cnt += 1

                min_r = min(min_r, x)
                max_r = max(max_r, x)
                min_c = min(min_c, y)
                max_c = max(max_c, y)

                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx = x + dx
                    ny = y + dy

                    if (
                        0 <= nx < n
                        and 0 <= ny < m
                        and not vis[nx][ny]
                        and g[nx][ny] == '1'
                    ):
                        vis[nx][ny] = True
                        q.append((nx, ny))

            area = (max_r - min_r + 1) * (max_c - min_c + 1)

            if area != cnt:
                ok = False
                break

        if not ok:
            break

    print("YES" if ok else "NO")
```

The outer loops search for unvisited `1` cells. Each such cell starts a new connected component.

The BFS serves two purposes simultaneously. It marks all cells belonging to the component, and it computes the component's bounding box. Tracking the minimum and maximum row and column indices avoids any extra passes over the grid.

The variable `cnt` stores the number of cells in the component. After the BFS ends, the rectangle determined by the bounding box is known. If the component is a perfect rectangle, its size must equal the rectangle's area. Any hole, indentation, or L-shape reduces the component size while leaving the bounding box unchanged, causing the comparison to fail.

The implementation uses four-directional adjacency because that is the natural notion of connectivity for grid components. Diagonal neighbors are intentionally ignored.

No special handling is required for single cells, single rows, or single columns. The area formula works correctly in all those cases.

## Worked Examples

### Example 1

Input:

```
3 3
100
011
011
```

There are two connected components.

| Component | Cells | Bounding Box | Area | Cell Count | Valid |
| --- | --- | --- | --- | --- | --- |
| 1 | {(0,0)} | rows 0..0, cols 0..0 | 1 | 1 | Yes |
| 2 | {(1,1),(1,2),(2,1),(2,2)} | rows 1..2, cols 1..2 | 4 | 4 | Yes |

Both components are perfect rectangles, so the answer is:

```
YES
```

This example shows that multiple disconnected rectangles are completely acceptable.

### Example 2

Input:

```
3 3
110
111
110
```

There is one connected component.

| Component | Bounding Box | Area | Cell Count | Valid |
| --- | --- | --- | --- | --- |
| Entire shape | rows 0..2, cols 0..1 | 6 | 5 | No |

The bounding rectangle contains six cells:

```
11
11
11
```

but one of them is missing from the component. Since `area != count`, the component is not rectangular.

The answer is:

```
NO
```

This example demonstrates the key failure condition. A connected shape with a missing cell inside its bounding box creates overlapping maximal rectangles.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Every cell is visited at most once during BFS |
| Space | O(nm) | Visited array and BFS queue |

The largest possible grid contains only `10,000` cells. An `O(nm)` traversal is extremely small for the given limits. Memory usage is also tiny, comfortably fitting within the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n, m = map(int, input().split())
        g = [input().strip() for _ in range(n)]

        vis = [[False] * m for _ in range(n)]
        ok = True

        for r in range(n):
            for c in range(m):
                if g[r][c] != '1' or vis[r][c]:
                    continue

                q = deque([(r, c)])
                vis[r][c] = True

                min_r = max_r = r
                min_c = max_c = c
                cnt = 0

                while q:
                    x, y = q.popleft()
                    cnt += 1

                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)

                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx = x + dx
                        ny = y + dy

                        if (
                            0 <= nx < n
                            and 0 <= ny < m
                            and not vis[nx][ny]
                            and g[nx][ny] == '1'
                        ):
                            vis[nx][ny] = True
                            q.append((nx, ny))

                area = (max_r - min_r + 1) * (max_c - min_c + 1)

                if area != cnt:
                    ok = False

        ans.append("YES" if ok else "NO")

    return "\n".join(ans) + "\n"

# provided sample
assert run(
"""5
3 3
100
011
011
3 3
110
111
110
1 5
01111
4 5
11111
01010
01000
01000
3 2
11
00
11
"""
) == """YES
NO
YES
NO
YES
"""

# minimum size
assert run(
"""1
1 1
1
"""
) == "YES\n"

# all zeros
assert run(
"""1
2 2
00
00
"""
) == "YES\n"

# L-shape
assert run(
"""1
2 2
11
10
"""
) == "NO\n"

# full rectangle
assert run(
"""1
3 4
1111
1111
1111
"""
) == "YES\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1×1` containing `1` | YES | Smallest non-empty rectangle |
| All zeros | YES | No components at all |
| `11 / 10` | NO | L-shaped component |
| Full `3×4` block of ones | YES | Large rectangular component |

## Edge Cases

Consider the L-shape:

```
1
2 2
11
10
```

The BFS discovers one component containing three cells. Its bounding box spans both rows and both columns, giving area `4`. Since `3 != 4`, the component is not rectangular and the algorithm outputs `NO`.

Consider diagonally touching cells:

```
1
2 2
10
01
```

The cells are not four-directionally connected, so two separate components are found. Each component has area `1` and size `1`. Both checks succeed, and the output is `YES`.

Consider a hollow structure:

```
1
3 3
111
101
111
```

The BFS finds one component with eight cells. The bounding box is the entire `3 × 3` grid, whose area is `9`. Since `8 != 9`, the component is rejected and the answer is `NO`.

Consider a single row:

```
1
1 5
01111
```

The component occupies columns `1..4`. The bounding box area is `4`, exactly matching the number of cells. The component is a rectangle of height one, and the algorithm correctly outputs `YES`.

These cases cover the situations where naive interpretations often fail, but the bounding-box test handles all of them naturally.
