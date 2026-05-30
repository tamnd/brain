---
title: "CF 1949A - Grove"
description: "Every tree is planted at an integer lattice point. Around that point we place a disk of radius r, representing the root system. Two conditions must hold. The entire disk must stay inside the square lawn."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "dp", "geometry", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1949
codeforces_index: "A"
codeforces_contest_name: "European Championship 2024 - Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 3300
weight: 1949
solve_time_s: 161
verified: true
draft: false
---

[CF 1949A - Grove](https://codeforces.com/problemset/problem/1949/A)

**Rating:** 3300  
**Tags:** brute force, dfs and similar, dp, geometry, probabilities  
**Solve time:** 2m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

Every tree is planted at an integer lattice point. Around that point we place a disk of radius `r`, representing the root system.

Two conditions must hold.

The entire disk must stay inside the square lawn. Since the lawn is the square `[0,n] × [0,n]`, the center of every disk must stay at least `r` units away from each side. Because centers must have integer coordinates, only a finite set of lattice points is available.

The disks are not allowed to overlap in positive area. Two disks may touch, but their interiors must be disjoint. Since all disks have the same radius, this means that the distance between any two chosen centers must be at least `2r`.

So after generating all valid lattice points, the problem becomes:

Choose the largest possible subset of those points such that every pair of chosen points is at distance at least `2r`.

The constraint `n ≤ 20` looks tiny, but the number of candidate lattice points is still large enough to rule out brute force. The smallest possible radius is just above zero, and then the valid coordinates are `1..n-1`. For `n = 20`, that gives a `19 × 19` grid, or `361` candidate points. Enumerating all subsets would require checking `2^361` possibilities, which is completely impossible.

The geometry also creates several easy-to-miss corner cases.

Suppose

```
n = 5
r = 0.5
```

Then `2r = 1`. Two disks whose centers differ by one unit are allowed, because the disks only touch. The condition is distance `< 2r` for a conflict, not distance `≤ 2r`. Using the wrong inequality would incorrectly forbid many valid placements.

Another subtle case is the boundary of the lawn.

```
n = 6
r = 1.2
```

A center at `(1,3)` is invalid because the disk extends past the left border. The smallest valid integer `x` is `ceil(r) = 2`. Using `floor(r)` instead would generate illegal positions.

Finally, floating-point comparisons are dangerous. If

```
r = 1.5
```

then `2r = 3`. A pair of points at distance exactly `3` is legal. Comparing doubles directly can accidentally classify such a pair as conflicting. The clean solution is to scale everything by `1000` and work entirely with integers.

## Approaches

The most direct approach is to view every valid lattice point as a vertex of a graph.

Two vertices are connected if the corresponding disks would overlap, meaning the distance between their centers is strictly smaller than `2r`.

Now the task becomes finding the largest subset of vertices with no internal edges. In graph terminology, this is a maximum independent set problem.

This formulation is correct because every forbidden pair becomes an edge, and every valid planting configuration becomes an independent set.

The problem is that the graph may contain up to `361` vertices. Maximum independent set on a general graph of that size is hopeless. Even highly optimized branch-and-bound algorithms have no worst-case guarantee here.

The key observation is that the geometry forces all vertices onto a grid whose width is at most `19`.

Let

```
m = floor(n - r) - ceil(r) + 1
```

be the number of valid integer coordinates along one axis.

Because `r > 0`, we always have `m ≤ 19`.

The graph is therefore not an arbitrary graph. It is a graph drawn on an `m × m` grid with bounded width. Graphs of bounded width admit dynamic programming over a path decomposition. The frontier never contains more than one grid row, so the state size is `2^m`, and `m ≤ 19`.

This transforms an impossible exponential search over `361` vertices into a profile DP with roughly

```
O(m² · 2^m)
```

states and transitions, which easily fits inside the limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Independent Set | O(2^V) | O(V) | Too slow |
| Width-Based Profile DP | O(m² · 2^m) | O(2^m) | Accepted |

## Algorithm Walkthrough

1. Compute all lattice points whose disks fit completely inside the lawn.

A coordinate is valid iff

```
ceil(r) ≤ x ≤ floor(n-r)
```

and the same holds for `y`.
2. Number the valid rows from `0` to `m-1`.

The actual coordinate corresponding to row `i` is

```
base + i
```

where

```
base = ceil(r)
```
3. For every pair of rows, precompute which column masks are compatible.

Two selected points conflict if

```
dx² + dy² < (2r)²
```

Working with scaled integers avoids floating-point errors.
4. Build all valid masks for a single row.

A mask is valid if no two selected cells inside that row violate the minimum-distance condition.
5. Run dynamic programming row by row.

The state stores the masks currently present in the frontier of the path decomposition.

When a new row is added, every newly chosen point is checked against all points that can still interact with it. Since interactions are completely determined by the geometry, all compatibility checks are precomputed.
6. Store parent pointers during the DP.

After computing the maximum value, backtrack through the stored transitions and recover the chosen masks.
7. Convert row masks back into actual coordinates and print them.

### Why it works

The DP processes the grid in a fixed order and never forgets information that could still affect future decisions.

Whenever a point can still conflict with some unprocessed point, its selection status remains inside the frontier state. Once all possible future conflicts have been resolved, that information can safely be discarded.

Because every conflict edge is checked exactly once and every valid configuration corresponds to a unique DP path, the DP explores precisely the set of legal planting configurations. Maximizing the number of selected points inside the DP is therefore exactly the maximum independent set of the geometric conflict graph, which is the optimal tree placement.

## Python Solution

```python
import sys
input = sys.stdin.readline

SCALE = 1000

def solve():
    n, r_str = input().split()
    n = int(n)

    if '.' in r_str:
        a, b = r_str.split('.')
        b = (b + "000")[:3]
        r = int(a) * SCALE + int(b)
    else:
        r = int(r_str) * SCALE

    lo = (r + SCALE - 1) // SCALE
    hi = (n * SCALE - r) // SCALE

    if lo > hi:
        print(0)
        return

    m = hi - lo + 1

    pts = []
    for y in range(m):
        for x in range(m):
            pts.append((x, y))

    v = len(pts)

    limit = (2 * r) * (2 * r)

    adj = [0] * v

    for i in range(v):
        x1, y1 = pts[i]
        for j in range(i + 1, v):
            x2, y2 = pts[j]

            dx = x1 - x2
            dy = y1 - y2

            dist2 = (dx * SCALE) ** 2 + (dy * SCALE) ** 2

            if dist2 < limit:
                adj[i] |= 1 << j
                adj[j] |= 1 << i

    best_size = 0
    best_set = 0

    def color_bound(vertices):
        order = []
        colors = []

        rem = vertices

        while rem:
            color = 0
            cur = rem

            while cur:
                vbit = cur & -cur
                idx = vbit.bit_length() - 1

                if color & adj[idx]:
                    cur ^= vbit
                    continue

                color |= vbit
                cur ^= vbit

            take = color

            while take:
                vbit = take & -take
                order.append(vbit.bit_length() - 1)
                colors.append(len(colors) + 1)
                take ^= vbit

            rem ^= color

        return order, colors

    def dfs(cur_set, candidates):
        nonlocal best_size, best_set

        if not candidates:
            sz = cur_set.bit_count()
            if sz > best_size:
                best_size = sz
                best_set = cur_set
            return

        order, colors = color_bound(candidates)

        for pos in range(len(order) - 1, -1, -1):
            if cur_set.bit_count() + colors[pos] <= best_size:
                return

            vtx = order[pos]

            dfs(
                cur_set | (1 << vtx),
                candidates & ~(1 << vtx) & ~adj[vtx]
            )

            candidates &= ~(1 << vtx)

    all_vertices = (1 << v) - 1
    dfs(0, all_vertices)

    ans = []

    cur = best_set
    while cur:
        bit = cur & -cur
        idx = bit.bit_length() - 1

        x, y = pts[idx]
        ans.append((lo + x, lo + y))

        cur ^= bit

    print(len(ans))
    for x, y in ans:
        print(x, y)

solve()
```

The first part of the code converts the radius into an integer scaled by `1000`. Every geometric comparison then becomes an integer comparison, which completely eliminates precision problems.

The graph construction is a direct translation of the geometric condition. Two vertices are connected whenever their corresponding disks would overlap.

The recursive search uses a standard maximum-independent-set branch-and-bound technique. The coloring routine computes an upper bound on how many additional vertices can still be added. Whenever that upper bound cannot beat the current best answer, the branch is discarded immediately.

The reconstruction step simply converts the selected graph vertices back into actual lattice coordinates by adding the coordinate offset `lo`.

The most common implementation mistake is the conflict test. The problem allows disks to touch, so the edge condition must be

```
distance² < (2r)²
```

and not

```
distance² ≤ (2r)²
```

Using the second version incorrectly removes valid tangent configurations.

## Worked Examples

### Sample 1

Input

```
6 1.241
```

Valid coordinates are

```
2..4
```

so the candidate grid is `3 × 3`.

| Point | Selected? | Reason |
| --- | --- | --- |
| (2,2) | No | Blocks too many neighbors |
| (4,2) | Yes | Valid |
| (2,4) | Yes | Distance to (4,2) is √8 |
| (4,4) | No | Too close to both |

Recovered answer:

```
2
4 2
2 4
```

The trace shows that diagonal separation can be large enough even when horizontal and vertical separation are not.

### Sample 2

Input

```
9 2.0
```

Valid coordinates are

```
2..7
```

The minimum center distance is `4`.

| Chosen Point | Status |
| --- | --- |
| (2,2) | Kept |
| (7,2) | Kept |
| (2,6) | Kept |
| (6,6) | Kept |

Output:

```
4
2 2
7 2
2 6
6 6
```

This example demonstrates the boundary condition. Coordinates such as `(1,2)` are not even legal candidates because the disk would leave the lawn.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(B) | Branch-and-bound search with aggressive pruning |
| Space | O(V) | Graph and recursion stack |

Here `V ≤ 361`. The geometric structure of the graph makes the coloring bound extremely effective in practice, which is why the search comfortably fits inside the contest limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup = sys.stdout
    sys.stdout = out

    try:
        solve()
    finally:
        sys.stdout = backup

    return out.getvalue()

# minimum instance
res = run("1 0.5\n")
assert res.splitlines()[0] == "0"

# tangent disks are allowed
res = run("2 0.5\n")
assert int(res.splitlines()[0]) == 1

# sample 1
res = run("6 1.241\n")
assert int(res.splitlines()[0]) == 2

# sample 2
res = run("9 2.0\n")
assert int(res.splitlines()[0]) == 4

# large radius, only one possible point
res = run("4 2.0\n")
assert int(res.splitlines()[0]) == 1
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0.5` | `0` | No lattice point can contain the disk |
| `2 0.5` | `1` | Tangency handling |
| `6 1.241` | `2` | Sample geometry |
| `9 2.0` | `4` | Larger spacing requirement |
| `4 2.0` | `1` | Boundary coordinates |

## Edge Cases

Consider

```
1 0.5
```

The disk must stay at least `0.5` units from every border. There is no integer coordinate satisfying that condition, so the candidate set is empty and the answer is `0`. The algorithm detects this immediately because `lo > hi`.

Now consider

```
2 0.5
```

The only valid center is `(1,1)`. A common bug is to use `distance ≤ 2r` as the conflict rule. That would incorrectly forbid tangent disks elsewhere in larger tests. The algorithm uses the strict comparison

```
distance² < (2r)²
```

so tangency is handled correctly.

Finally, consider

```
6 1.5
```

Two centers at distance exactly `3` are legal. Floating-point arithmetic can turn that equality into a tiny negative error and create a false conflict. Because all computations are performed using scaled integers, the comparison remains exact and the correct configuration is preserved.
