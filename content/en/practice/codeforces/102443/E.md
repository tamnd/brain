---
title: "CF 102443E - Hide-and-Seek for Robots"
description: "We have an (mtimes n) grid. A robot occupies some cells, and every robot points in one of four cardinal directions. A robot looking down sees a widening triangular region: one cell immediately below it, then three cells two rows below, then five cells three rows below, and so on."
date: "2026-08-08T12:59:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102443
codeforces_index: "E"
codeforces_contest_name: "2019-2020 Russia Team Open, High School Programming Contest (VKOSHP 19)"
rating: 0
weight: 102443
solve_time_s: 485
verified: true
draft: false
---

[CF 102443E - Hide-and-Seek for Robots](https://codeforces.com/problemset/problem/102443/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an (m\times n) grid. A robot occupies some cells, and every robot points in one of four cardinal directions. A robot looking down sees a widening triangular region: one cell immediately below it, then three cells two rows below, then five cells three rows below, and so on. The other three directions are defined symmetrically.

We must rotate robots so that no pair of robots sees each other. Rotating a robot by (90^\circ) costs one operation, so changing (U) to (D), for example, costs two operations. The output must keep exactly the same robot positions and must achieve the minimum total number of rotations.

The useful geometric observation is that two robots can see each other only when they point in opposite directions and the displacement in that direction is strictly larger than the perpendicular displacement. For a vertical pair this means that an upper robot pointing down and a lower robot pointing up are dangerous when

[
|\Delta c|<|\Delta r|.
]

For a horizontal pair the analogous condition is

[
|\Delta r|<|\Delta c|.
]

Equality is safe. This strict inequality is an easy place to make an off-by-one error.

The grid has at most (4\cdot 10^6) cells. An (O(mn\min(m,n))) solution would already require billions of operations, so enumerating possible contours independently for every column and checking every row again is too slow. The target is (O(mn)), or at most a small constant number of such passes.

There are several edge cases that matter.

Consider

```
1 3
R.L
```

The two robots are in the same row and point toward each other, so they see each other. Turning either one by (90^\circ) is sufficient, and the correct minimum cost is (1). A careless implementation that treats a diagonal condition as inclusive, or that only checks adjacent cells, can miss this conflict.

Now consider

```
3 1
R
.
L
```

The two robots are in the same column, but both look horizontally, so neither can see the other. The correct minimum cost is (0). This catches solutions that assume every pair of opposite directions is automatically bad.

For the strict diagonal boundary, consider

```
2 2
D.
.U
```

The robots are diagonally adjacent. Their row and column differences are both (1), so neither view cone contains the other robot. The correct output can be identical to the input, with cost (0). Replacing the strict inequality by a non-strict one incorrectly forces a rotation.

Finally, an empty grid such as

```
2 2
..
..
```

already satisfies the condition and must be returned unchanged. There is no reason to invent robots or modify empty cells.

## Approaches

The direct approach is to consider every robot, try its four possible directions, and check whether the resulting configuration is valid. There are four choices per robot, so with (k) robots this is (4^k), which becomes useless even for a few dozen robots. A slightly less naive approach is to inspect every pair of robots while constructing a configuration, but the pair count alone is (O(k^2)), and there are exponentially many direction assignments.

The useful structure comes from looking at only the vertical directions first. Imagine drawing the view cones of all robots that point up. Their forbidden regions form a monotone contour. For every column there is a boundary row (d_i). Robots on one side of the contour must use the upward direction, while robots on the other side must use the downward direction. A robot exactly on the contour is flexible. The contour cannot jump by more than one row between neighboring columns, so

[
|d_i-d_{i+1}|\le 1.
]

This is precisely the kind of local condition that a one-dimensional dynamic program can handle. This contour characterization is the central observation behind the known (O(mn)) solution.

There is one more detail. A robot that does not want to use the primary vertical direction can safely be made horizontal, provided all such horizontal robots in the canonical construction use the same horizontal direction. Horizontal robots then cannot see each other, because they all point the same way. Robots using a vertical direction and robots using a horizontal direction cannot see each other mutually, since mutual visibility requires both robots to point along the displacement axis.

We can thus build a canonical configuration around a vertical contour. Above the contour, every robot chooses either (U) or one fixed horizontal direction. Below it, every robot chooses either (D) or that same fixed horizontal direction. On the contour, a robot may choose (U), (D), or the fixed horizontal direction.

There is a symmetric construction with a horizontal contour. We transpose the grid, regard (L/R) as the primary directions, and use one fixed vertical direction as the alternative. We try both choices for the fixed alternative direction in each orientation. This gives only four DP runs, which is still (O(mn)).

The contour formulation is not merely a way to construct some valid configuration. A standard uncrossing argument lets any optimal valid configuration be converted to one of these canonical forms without increasing its rotation cost. If the conflicting pairs are predominantly vertical, their boundary can be represented by the vertical contour. If the corresponding structure is horizontal, transpose the argument. Once the contour is fixed, every robot can be optimized independently, so the remaining problem is exactly the DP described below.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(4^k k^2)) | (O(k)) | Too slow |
| Pairwise checking with arbitrary orientations | Exponential | (O(k)) | Too slow |
| Contour DP | (O(mn)) | (O(mn)) | Accepted |

## Algorithm Walkthrough

1. First consider a vertical contour. For every column (c), choose an integer boundary (d_c) between (0) and (m+1). If (d_c=0), the entire column is below the contour. If (d_c=m+1), the entire column is above it. Otherwise row (d_c) is the contour cell.
2. Require

[
|d_c-d_{c-1}|\le 1.
]

This is exactly the geometric condition saying that the contour can move only one row up or down when moving one column horizontally.

1. Fix one horizontal escape direction (H), either (L) or (R). For a robot above the contour, only (U) and (H) are considered. For a robot below the contour, only (D) and (H) are considered. On the contour, (U,D,H) are available.
2. Convert those choices into rotation costs. If the original direction is (x), the cost of choosing (y) is the circular distance between the four directions. Thus (U\to R) and (U\to L) both cost (1), while (U\to D) costs (2).
3. For a fixed column and a fixed boundary (d), compute its total cost. Let (A_r) be the cheapest cost for row (r) when it is above the contour, (B_r) the cheapest cost when it is below, and (C_r) the cheapest cost when the row itself is the contour. Then

\sum_{r<d} A_r
+
C_d
+
\sum_{r>d} B_r.
]

The two sums are obtained with prefix and suffix sums, so all (m+2) possible values of (d) for one column are computed in (O(m)).

1. Define (dp_c[d]) as the minimum cost after processing columns (0\ldots c), with (d) as the contour position in column (c). The only possible previous contour positions are (d-1,d,d+1), giving

\operatorname{cost}_c(d)
+
\min(dp_{c-1}[d-1],dp_{c-1}[d],dp_{c-1}[d+1]).
]

1. Store which of the three predecessor states was used. After the last column, choose the cheapest boundary position and walk backward through these parent choices to reconstruct the entire contour.
2. Use the reconstructed contour to choose the actual direction of every robot. Above the contour choose the cheaper of (U) and (H). Below it choose the cheaper of (D) and (H). On the contour choose the cheapest of (U,D,H).
3. Repeat the same procedure with (H=L) and (H=R). Then transpose the grid and perform the symmetric construction twice more, with the primary directions now corresponding to (L/R) and the escape direction corresponding to (U) or (D).
4. Keep the cheapest of the four resulting configurations. In every generated configuration, all robots using the escape direction point identically, so they cannot see each other. The primary (U/D) or (L/R) robots are separated by the contour, and a primary-direction robot and an escape-direction robot cannot mutually see each other because their directions are perpendicular.

### Why it works

The invariant of the DP is that after processing column (c), `dp[d]` is the minimum rotation cost among all canonical configurations whose contour ends at row (d). The transition considers exactly the three possible contour positions compatible with the one-cell slope restriction, so every legal contour is represented.

For a fixed contour, the direction chosen for one robot does not affect the cost of any other robot. All horizontal escape robots point in the same direction, while the primary vertical robots are separated into an upward region and a downward region. On the contour, the contour's one-cell slope restriction prevents two opposite primary directions from being vertically close enough to see each other. Thus every DP state corresponds to a valid configuration.

The symmetric argument applies after transposition. The contour lemma says that an optimal valid configuration can be uncrossed into one of these canonical forms without increasing its number of rotations. Since we enumerate both axes and both possible escape directions, the minimum among the four DP results is the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**9

# Directions are arranged clockwise.
ORDER = "URDL"
IDX = {ch: i for i, ch in enumerate(ORDER)}

def turn_cost(a, b):
    x = abs(IDX[a] - IDX[b])
    return min(x, 4 - x)

def solve_family(g, up, down, side):
    """
    Solve the contour problem on g.

    Above the contour:
        choose up or side.

    Below the contour:
        choose down or side.

    On the contour:
        choose up, down, or side.

    Returns:
        (minimum_cost, contour)
    """
    h = len(g)
    w = len(g[0])
    states = h + 2

    # parent[c * states + d]:
    # 0 -> previous d-1
    # 1 -> previous d
    # 2 -> previous d+1
    parent = bytearray(w * states)

    prev = [INF] * states

    for c in range(w):
        # Prefix costs for rows above the contour.
        pref = [0] * (h + 1)

        # Suffix costs for rows below the contour.
        suff = [0] * (h + 1)

        col = g

        for r in range(h):
            ch = col[r][c]

            a = min(turn_cost(ch, up), turn_cost(ch, side))
            pref[r + 1] = pref[r] + a

        for r in range(h - 1, -1, -1):
            ch = col[r][c]

            b = min(turn_cost(ch, down), turn_cost(ch, side))
            suff[r] = suff[r + 1] + b

        # Cost of every possible contour position.
        cost = [0] * states

        # d = 0, everything is below.
        cost[0] = suff[0]

        # d = h + 1, everything is above.
        cost[h + 1] = pref[h]

        for d in range(1, h + 1):
            ch = col[d - 1][c]

            boundary = min(
                turn_cost(ch, up),
                turn_cost(ch, down),
                turn_cost(ch, side),
            )

            cost[d] = pref[d - 1] + boundary + suff[d]

        if c == 0:
            prev = cost
            continue

        cur = [INF] * states
        base = c * states

        for d in range(states):
            best = prev[d]
            code = 1

            if d > 0 and prev[d - 1] < best:
                best = prev[d - 1]
                code = 0

            if d + 1 < states and prev[d + 1] < best:
                best = prev[d + 1]
                code = 2

            cur[d] = best + cost[d]
            parent[base + d] = code

        prev = cur

    best_d = min(range(states), key=prev.__getitem__)
    best_cost = prev[best_d]

    contour = [0] * w
    d = best_d

    for c in range(w - 1, -1, -1):
        contour[c] = d

        if c == 0:
            break

        code = parent[c * states + d]

        if code == 0:
            d -= 1
        elif code == 2:
            d += 1

    return best_cost, contour

def build_family(g, up, down, side, contour):
    h = len(g)
    w = len(g[0])

    ans = [list(row) for row in g]

    for c in range(w):
        d = contour[c]

        for r in range(h):
            ch = g[r][c]

            if ch == '.':
                continue

            if d == 0:
                choices = (down, side)
            elif d == h + 1:
                choices = (up, side)
            elif r < d - 1:
                choices = (up, side)
            elif r > d - 1:
                choices = (down, side)
            else:
                choices = (up, down, side)

            best = choices[0]
            best_cost = turn_cost(ch, best)

            for cand in choices[1:]:
                cur = turn_cost(ch, cand)
                if cur < best_cost:
                    best_cost = cur
                    best = cand

            ans[r][c] = best

    return [''.join(row) for row in ans]

def transpose_problem(g):
    """
    Transform the problem so that original horizontal directions
    become vertical directions.

    Original:
        L -> transformed U
        R -> transformed D
        U -> transformed L
        D -> transformed R
    """
    h = len(g)
    w = len(g[0])

    mp = {
        'L': 'U',
        'R': 'D',
        'U': 'L',
        'D': 'R',
        '.': '.',
    }

    t = []
    for c in range(w):
        row = []
        for r in range(h):
            row.append(mp[g[r][c]])
        t.append(''.join(row))

    return t

def untranspose_answer(t):
    """
    Inverse of transpose_problem.
    """
    h = len(t)
    w = len(t[0])

    mp = {
        'U': 'L',
        'D': 'R',
        'L': 'U',
        'R': 'D',
        '.': '.',
    }

    ans = [['.'] * h for _ in range(w)]

    for r in range(h):
        for c in range(w):
            ans[c][r] = mp[t[r][c]]

    return [''.join(row) for row in ans]

def solve_grid(g):
    best_cost = INF
    best_answer = None

    # Vertical contour.
    for side in ('L', 'R'):
        cost, contour = solve_family(g, 'U', 'D', side)

        if cost < best_cost:
            best_cost = cost
            best_answer = build_family(
                g, 'U', 'D', side, contour
            )

    # Horizontal contour, obtained by transposing.
    tg = transpose_problem(g)

    for side in ('L', 'R'):
        cost, contour = solve_family(tg, 'U', 'D', side)

        if cost < best_cost:
            transformed = build_family(
                tg, 'U', 'D', side, contour
            )
            best_cost = cost
            best_answer = untranspose_answer(transformed)

    return best_answer

def main():
    m, n = map(int, input().split())
    g = [input().strip() for _ in range(m)]

    ans = solve_grid(g)

    sys.stdout.write('\n'.join(ans))

if __name__ == "__main__":
    main()
```

The direction order `URDL` makes rotation distance a circular distance. For example, `U` to `D` is two turns, while `U` to either `L` or `R` is one turn.

The `solve_family` function is the core DP. The states are the (m+2) possible contour positions. The two extra states represent contours completely above or completely below the grid, so there is no special case involving an artificial row in the actual grid.

For each column, `pref` stores the accumulated cost of putting rows above the contour into the `up-or-side` category. `suff` does the same for rows below the contour. Consequently, every possible contour position is evaluated in constant time after the two linear scans.

The transition examines exactly three predecessors. The byte array `parent` is enough because each state needs to remember only whether the previous contour was one row above, equal, or one row below. Using a `bytearray` instead of a Python list of integers keeps the (O(mn)) reconstruction memory small.

The reconstruction uses exactly the same choices as the DP. A robot above the contour chooses between the primary direction and the fixed escape direction. A robot below does the analogous thing with the opposite primary direction. A robot on the contour has the additional choice of the other primary direction.

The second pair of runs is the same algorithm after transposing the grid. The direction mapping is necessary because an original `L` becomes transformed `U`, an original `R` becomes transformed `D`, an original `U` becomes transformed `L`, and an original `D` becomes transformed `R`.

No integer-overflow issue exists in Python. The maximum useful cost is at most twice the number of robots, so a large finite `INF` is sufficient.

## Worked Examples

### Sample 1

The input is

```
2 3
RDL
.U.
```

One optimal contour can be viewed vertically. Consider using `L` as the fixed horizontal escape direction. The contour can stay at row (1) in every column.

| Column | Boundary | Above cost | Boundary cost | Below cost | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | `R -> U` = 1 | 0 | 1 |
| 2 | 1 | 0 | `D -> D` = 0 | `U -> L` = 1 | 1 |
| 3 | 1 | 0 | `L -> L` = 0 | 0 | 0 |

The total is (2). One possible optimum is the sample output:

```
UDL
.R.
```

The first robot turns from `R` to `U`, and the second-row robot turns from `U` to `R` in the sample output. Both changes cost one.

The important point is that leaving the first `R` and third `L` unchanged would make those two robots see each other horizontally. The contour DP pays for exactly the necessary separation.

### Sample 2

The input is

```
2 2
..
..
```

There are no robots, so every contour has zero cost.

| Column | Boundary | DP cost |
| --- | --- | --- |
| 1 | 0 | 0 |
| 2 | 0 | 0 |

The reconstructed grid remains empty:

```
..
..
```

This confirms that the artificial contour states do not create robots or modify empty cells.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(mn)) | Four contour DP runs are only a constant factor, and each run scans every cell a constant number of times |
| Space | (O(mn)) | The parent array stores three-way predecessor choices for every contour state |

The grid contains at most (4\cdot10^6) cells. The algorithm performs only a constant number of linear passes over those cells, rather than enumerating robot pairs or direction assignments. The (O(mn)) memory is within the 512 MB limit, although Python's compact `bytearray` parent representation is particularly useful here.

## Test Cases

The output is not unique, so tests should verify the returned configuration rather than compare it character by character. For small cases we can brute-force every pair to check validity and calculate the exact rotation cost.

```python
# helper: run solution on input string, return output string
import sys
import io
from itertools import product

# Assume the editorial solution above has been placed in a module
# named solution, or copy solve_grid into this test file.

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    m, n = map(int, sys.stdin.readline().split())
    g = [sys.stdin.readline().strip() for _ in range(m)]

    ans = solve_grid(g)

    sys.stdin = old_stdin
    return '\n'.join(ans)

ORDER = "URDL"
IDX = {c: i for i, c in enumerate(ORDER)}

def dist(a, b):
    x = abs(IDX[a] - IDX[b])
    return min(x, 4 - x)

def sees(r1, c1, d, r2, c2):
    dr = r2 - r1
    dc = c2 - c1

    if d == 'U':
        return dr < 0 and abs(dc) < -dr
    if d == 'D':
        return dr > 0 and abs(dc) < dr
    if d == 'L':
        return dc < 0 and abs(dr) < -dc
    return dc > 0 and abs(dr) < dc

def validate(inp, out):
    data = inp.strip().splitlines()
    m, n = map(int, data[0].split())
    original = data[1:]

    answer = out.splitlines()

    assert len(answer) == m
    assert all(len(row) == n for row in answer)

    robots = []

    for r in range(m):
        for c in range(n):
            assert (original[r][c] == '.') == (answer[r][c] == '.')

            if answer[r][c] != '.':
                robots.append((r, c, answer[r][c]))

    for i in range(len(robots)):
        r1, c1, d1 = robots[i]

        for j in range(i + 1, len(robots)):
            r2, c2, d2 = robots[j]

            assert not (
                sees(r1, c1, d1, r2, c2)
                and sees(r2, c2, d2, r1, c1)
            )

    cost = 0

    for r in range(m):
        for c in range(n):
            if original[r][c] != '.':
                cost += dist(original[r][c], answer[r][c])

    return cost

# Provided sample 1.
sample1 = """\
2 3
RDL
.U.
"""

out = run(sample1)
assert validate(sample1, out) == 2, "sample 1"

# Provided sample 2.
sample2 = """\
2 2
..
..
"""

out = run(sample2)
assert validate(sample2, out) == 0, "sample 2"

# Minimum-size input.
case3 = """\
1 1
U
"""

out = run(case3)
assert validate(case3, out) == 0, "single robot needs no rotation"

# All robots already point in the same direction.
case4 = """\
3 4
RRRR
RRRR
RRRR
"""

out = run(case4)
assert validate(case4, out) == 0, "all equal directions"

# Opposite horizontal directions in one row.
case5 = """\
1 3
R.L
"""

out = run(case5)
assert validate(case5, out) == 1, "horizontal mutual visibility"

# Opposite horizontal directions in one column.
case6 = """\
3 1
R
.
L
"""

out = run(case6)
assert validate(case6, out) == 0, "same column is safe"

# Equal row/column displacement is not visible.
case7 = """\
2 2
D.
.U
"""

out = run(case7)
assert validate(case7, out) == 0, "diagonal equality is safe"

# Maximum-size input shape, chosen so the expected cost is obvious.
m = 2000
n = 2000
large = str(m) + " " + str(n) + "\n" + "\n".join(["U" * n] * m) + "\n"

out = run(large)
assert all(row == "U" * n for row in out.splitlines()), \
    "maximum-size all-U case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 3 / RDL / .U.` | Any valid configuration with cost 2 | Provided sample and contour reconstruction |
| `2 2 / .. / ..` | Empty grid | Empty input |
| `1 1 / U` | `U` | Minimum-size input |
| `3 4` with every cell `R` | Same grid | All-equal directions |
| `1 3 / R.L` | Any valid configuration with cost 1 | Horizontal mutual visibility |
| `3 1 / R / . / L` | Same grid | Opposite horizontal directions in one column |
| `2 2 / D. / .U` | Same grid | Strict diagonal boundary |
| `2000 x 2000` all `U` | Same grid | Maximum-size input and performance |

## Edge Cases

The first edge case is an empty grid. For

```
2 2
..
..
```

every column can use contour state (0), (1), (2), or (3), and every column cost is zero. The DP consequently returns zero and the reconstruction leaves every cell as `.`.

The second edge case is a single robot. For

```
1 1
L
```

we can choose the contour directly through that cell, so the robot can retain `L` at zero cost. The DP's boundary transition includes the original direction through the minimum over its allowed directions, so it does not force an unnecessary rotation.

The third edge case is the strict diagonal boundary:

```
2 2
D.
.U
```

The two robots are at displacement ((1,1)). A downward cone contains only the same-column cell in its first row, so the diagonal cell is not visible. The same is true for the upward cone. The algorithm never introduces a constraint at equality because the contour argument uses a strict cone, matching the original geometry.

The fourth edge case is opposite horizontal directions in one column:

```
3 1
R
.
L
```

These robots cannot see each other because their horizontal displacement is zero. A vertical contour representation might be less convenient for preserving both directions, but after transposing the grid they lie on the same horizontal-contour boundary. The symmetric DP handles both `L` and `R` without forcing a rotation, giving cost zero.

The final subtle case is when many robots lie on the contour. Consecutive contour rows can differ by at most one, so two boundary robots have vertical displacement no larger than their horizontal displacement. That is exactly the opposite of the strict condition required for a vertical mutual view. This is why robots on the contour can use the two primary directions without creating a hidden vertical conflict.

A practical implementation note: the four constant-factor DP runs are the part most worth optimizing in Python. The `bytearray` parent storage and avoiding nested Python objects for DP state are deliberate choices for the 2000×2000 limit.
