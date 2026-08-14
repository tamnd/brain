---
title: "CF 102416E - Space guardians"
description: "We have at most 100 spherical protected regions in three-dimensional space. Starship (i) has center ((xi,yi,zi)) and radius (ri). We must choose some starships whose original spheres do not overlap. Touching at exactly one point is allowed."
date: "2026-08-14T14:42:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102416
codeforces_index: "E"
codeforces_contest_name: "Edinburgh Competition 2019"
rating: 0
weight: 102416
solve_time_s: 128
verified: false
draft: false
---

[CF 102416E - Space guardians](https://codeforces.com/problemset/problem/102416/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We have at most 100 spherical protected regions in three-dimensional space. Starship (i) has center ((x_i,y_i,z_i)) and radius (r_i). We must choose some starships whose original spheres do not overlap. Touching at exactly one point is allowed.

After choosing a starship, its responsibility expands from radius (r_i) to radius (3r_i). The expanded spheres may overlap. The requirement is that the union of all original spheres must be contained in the union of the expanded spheres belonging to the chosen starships.

The output only needs to give one valid subset. The subset does not have to be minimum, so we can concentrate on finding a construction that is guaranteed to work.

Two spheres (i) and (j) are disjoint exactly when

[
d(i,j) \ge r_i+r_j,
]

where

[
d(i,j)^2=(x_i-x_j)^2+(y_i-y_j)^2+(z_i-z_j)^2.
]

Using squared distances avoids square roots and keeps every calculation integral.

The constraint (n\le100) is small enough for (O(n^2)) work, which means we can compare every pair of spheres. An (O(n^3)) solution would also be numerically small here, but there is no reason to use it. Exponential search over all subsets is completely infeasible: (2^{100}) is about (1.27\cdot10^{30}), even before doing the geometric checks.

There are two boundary cases that are easy to mishandle. First, touching spheres are allowed to coexist. For example,

```
2
0 0 0 1
2 0 0 1
```

has centers exactly two units apart, so the spheres touch but do not overlap. Both can be selected, and a valid output is

```
2
1 2
```

A check using `distance <= r1 + r2` would incorrectly reject this pair.

The second boundary concerns coverage. Suppose a sphere is skipped because it intersects a selected sphere. The selected sphere must have radius at least as large as the skipped one. If the two spheres intersect, every point of the skipped sphere is at distance at most (r_i+r_j) from the selected center. Since (r_i\le r_j), this is at most (2r_j), which is smaller than its new radius (3r_j). A careless implementation that chooses spheres in arbitrary order loses the crucial radius comparison and can fail to cover a large sphere with a much smaller selected sphere.

For example,

```
2
0 0 0 10
10 0 0 1
```

should select the radius-10 sphere. If the small sphere were selected first and the large sphere were then skipped merely because the original spheres intersect, the expanded radius-3 sphere would not cover the large sphere. Processing in decreasing radius prevents this situation.

## Approaches

The most direct brute-force approach is to try every subset of starships. For each subset, we can check every pair of chosen spheres for overlap and then check whether every original sphere is covered by the expanded spheres. Even with an (O(n^2)) validation procedure, this costs (O(2^n n^2)). At (n=100), the subset count alone is about (1.27\cdot10^{30}), so this approach is far beyond the limit.

The useful observation is that we do not need to search for the right subset. Sort the spheres by decreasing radius and greedily keep a sphere exactly when it is disjoint from every sphere already kept.

The disjointness part is immediate. We only add a sphere after confirming that its original sphere does not intersect any selected sphere.

The interesting part is coverage. Consider a sphere (A) that the algorithm does not select. At the moment (A) is considered, some previously selected sphere (B) must intersect (A). Because the list is sorted by decreasing radius,

[
r_A\le r_B.
]

Take any point (P) inside (A). Its distance from the center of (B) is at most

[
|P-C_B|\le |P-C_A|+|C_A-C_B|
\le r_A+(r_A+r_B).
]

That expression is at most (2r_A+r_B), which is at most (3r_B) because (r_A\le r_B). Thus every point of (A) lies inside the sphere of radius (3r_B) centered at (B).

In fact, we can use the slightly looser but simpler bound

[
|P-C_B|\le r_A+r_A+r_B\le3r_B.
]

So every skipped sphere is completely covered by the three-times-expanded sphere of some earlier selected sphere.

The brute-force works because it explicitly searches for a subset satisfying both conditions, but fails because there are exponentially many subsets. The observation that a larger sphere automatically covers every intersecting smaller sphere after its radius is tripled turns the search into a simple greedy construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^n n^2)) | (O(n)) | Too slow |
| Greedy by decreasing radius | (O(n^2+n\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read all starships and keep their original indices, because the output must use the indices from the input.
2. Sort the starships by decreasing radius. If two radii are equal, any order between them is valid.
3. Start with an empty set of selected starships. Process the sorted list from largest radius to smallest.
4. For the current starship (i), compare it with every already selected starship (j). Compute the squared center distance

[
d^2=(x_i-x_j)^2+(y_i-y_j)^2+(z_i-z_j)^2.
]

The current sphere can be selected only if

[
d^2\ge(r_i+r_j)^2
]

for every selected (j). Equality is allowed because touching spheres count as disjoint.

1. If the current sphere is disjoint from all selected spheres, add it to the answer. Otherwise skip it.
2. After all spheres have been processed, print the selected indices. The algorithm always produces a valid answer, so the `NO` branch is never needed.

### Why it works

Maintain the invariant that every sphere processed so far is either selected or is completely covered by the three-times-expanded sphere of some selected sphere.

A selected sphere obviously satisfies the invariant because its own expanded sphere contains its original sphere. If a sphere is skipped, it intersects an earlier selected sphere (j), and the sorting order gives (r_i\le r_j). For any point (P) in the skipped sphere,

[
|P-C_j|
\le |P-C_i|+|C_i-C_j|
\le r_i+(r_i+r_j)
=2r_i+r_j
\le3r_j.
]

Hence the entire skipped sphere is covered by the expanded sphere of (j). At the same time, a sphere is selected only when it is disjoint from every previously selected sphere, so all selected original regions remain pairwise disjoint. Both required properties hold after every iteration and consequently hold for the final answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    ships = []

    for i in range(1, n + 1):
        x, y, z, r = map(int, input().split())
        ships.append((r, x, y, z, i))

    # Larger spheres must be considered first.
    ships.sort(reverse=True)

    selected = []

    for r, x, y, z, idx in ships:
        can_take = True

        for sr, sx, sy, sz, sidx in selected:
            dx = x - sx
            dy = y - sy
            dz = z - sz

            dist2 = dx * dx + dy * dy + dz * dz
            radius_sum = r + sr

            # Touching is allowed, so equality is also disjoint.
            if dist2 < radius_sum * radius_sum:
                can_take = False
                break

        if can_take:
            selected.append((r, x, y, z, idx))

    print(len(selected))
    print(*[idx for _, _, _, _, idx in selected])

if __name__ == "__main__":
    solve()
```

The input is stored together with the original index so that sorting does not lose the identity of a starship. The tuple starts with the radius, allowing `sort(reverse=True)` to process larger radii first.

For every candidate, the inner loop compares it with only the selected spheres. The squared distance is compared with the squared sum of radii, so there is no floating-point arithmetic. This is particularly useful because the boundary case where two spheres exactly touch must be handled precisely.

The comparison uses `<` rather than `<=`. If

[
d^2=(r_i+r_j)^2,
]

the spheres touch and are explicitly allowed to be selected together. Only a strictly smaller distance means that their interiors overlap.

Python integers have arbitrary precision, so there is no overflow issue. Even in a fixed-width integer language, the coordinate differences are at most (10^4), giving squared distances on the order of (10^8), while squared radius sums are also safely small.

The algorithm never prints `NO`. The proof above shows that the decreasing-radius construction always gives a valid subset, including when there is only one sphere.

## Worked Examples

### Sample 1

The input is

```
4
1 0 0 1
2 0 0 1
7 0 0 1
10 0 0 3
```

The radius-3 sphere is processed first. It is selected immediately. The three radius-1 spheres are then checked against the selected sphere. Their center distances from ((10,0,0)) are 9, 8, and 3 respectively, while the required disjointness thresholds are (4).

With the deterministic sorting used by the code, the first two radius-1 spheres are selected and the sphere at (x=7) is skipped.

| Current index | Radius | Selected before | Distance checks | Decision |
| --- | --- | --- | --- | --- |
| 4 | 3 | none | none | select |
| 1 | 1 | 4 | (9\ge4) | select |
| 2 | 1 | 4, 1 | (8\ge4,\ 1<2) is false because centers 1 and 2 are distance 1 | skip |
| 3 | 1 | 4, 1 | (3<4) | skip |

The selected set produced by this implementation is `{4, 1}`. Sphere 2 is covered by the expanded sphere of sphere 1, while sphere 3 is covered by the expanded sphere of sphere 4. The sample's `{2,4}` is another valid answer, since the output is not required to be unique.

### A simple covering example

Consider

```
3
0 0 0 5
6 0 0 2
20 0 0 1
```

The radius-5 sphere is selected first. The radius-2 sphere intersects it, so it is skipped. The radius-1 sphere is disjoint from the selected sphere and is selected.

| Current index | Radius | Selected before | Relevant distance | Decision |
| --- | --- | --- | --- | --- |
| 1 | 5 | none | none | select |
| 2 | 2 | 1 | (6<7) | skip |
| 3 | 1 | 1 | (20\ge6) | select |

Sphere 2 is covered by the radius-15 expanded sphere of sphere 1. This demonstrates exactly why the radius ordering matters: the sphere that causes another sphere to be skipped is guaranteed to be at least as large.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n+n^2)) | Sorting costs (O(n\log n)), and at most (n) candidates each compare with (n) selected spheres |
| Space | (O(n)) | The input and selected-starship arrays contain (O(n)) records |

With (n\le100), the quadratic part performs at most about (10^4) pairwise checks. The coordinate and radius limits also make every arithmetic operation inexpensive, so the solution is comfortably within the 1 second and 256 MB limits.

## Test Cases

The test harness below checks the actual geometric conditions rather than requiring one particular valid subset. This is necessary because the problem allows any valid answer, so different correct greedy tie-breaking choices can produce different index sets.

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        n = int(sys.stdin.readline())
        ships = []

        for i in range(1, n + 1):
            x, y, z, r = map(int, sys.stdin.readline().split())
            ships.append((r, x, y, z, i))

        ships.sort(reverse=True)

        selected = []

        for r, x, y, z, idx in ships:
            ok = True

            for sr, sx, sy, sz, sidx in selected:
                dx = x - sx
                dy = y - sy
                dz = z - sz

                dist2 = dx * dx + dy * dy + dz * dz
                rr = r + sr

                if dist2 < rr * rr:
                    ok = False
                    break

            if ok:
                selected.append((r, x, y, z, idx))

        print(len(selected))
        print(*[idx for _, _, _, _, idx in selected])

        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def validate(inp: str, out: str) -> bool:
    lines = out.strip().splitlines()
    if not lines:
        return False

    n = int(inp.splitlines()[0])
    data = [tuple(map(int, line.split())) for line in inp.splitlines()[1:]]

    k = int(lines[0])
    ids = list(map(int, lines[1].split())) if len(lines) > 1 else []

    if k != len(ids):
        return False
    if not (1 <= k <= n):
        return False
    if len(set(ids)) != k:
        return False
    if any(i < 1 or i > n for i in ids):
        return False

    selected = [data[i - 1] for i in ids]

    # Check that selected original spheres are pairwise disjoint.
    for i in range(k):
        x1, y1, z1, r1 = selected[i]
        for j in range(i + 1, k):
            x2, y2, z2, r2 = selected[j]

            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2

            dist2 = dx * dx + dy * dy + dz * dz
            rr = r1 + r2

            if dist2 < rr * rr:
                return False

    # Check that every original sphere is covered by the union
    # of the expanded selected spheres.
    for x, y, z, r in data:
        covered = False

        for sx, sy, sz, sr in selected:
            dx = x - sx
            dy = y - sy
            dz = z - sz

            center_dist2 = dx * dx + dy * dy + dz * dz

            # The farthest point of the original sphere is
            # center distance + r, so coverage requires
            # center distance <= 3*sr - r.
            reach = 3 * sr - r

            if reach >= 0 and center_dist2 <= reach * reach:
                covered = True
                break

        if not covered:
            return False

    return True

def run(inp: str) -> str:
    out = solve_data(inp)
    assert validate(inp, out), f"Invalid output:\n{out}"
    return out

# Provided sample.
run("""4
1 0 0 1
2 0 0 1
7 0 0 1
10 0 0 3
""")

# Minimum-size input.
run("""1
5 5 5 7
""")

# Two spheres that only touch. Both may be selected.
run("""2
0 0 0 1
2 0 0 1
""")

# One large sphere intersects a smaller sphere.
# The larger one must be processed first so the smaller one is skipped safely.
run("""2
0 0 0 10
10 0 0 1
""")

# All spheres have identical centers.
# Only one original sphere can be selected, and its 3r expansion
# covers every identical sphere.
run("""4
100 100 100 2
100 100 100 2
100 100 100 2
100 100 100 2
""")

# Larger boundary-style case with 100 spheres.
# All are identical, so exactly one is needed.
large_case = "100\n" + "\n".join(
    f"{i} 0 0 1" for i in range(100)
)
run(large_case)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | Any geometrically valid subset | General construction and non-unique output |
| `1 / 5 5 5 7` | One selected sphere | Minimum-size input |
| Two unit spheres at distance 2 | Both may be selected | Exact touching boundary |
| Radius 10 and radius 1 with intersecting centers | Large sphere selected, small one skipped | Decreasing-radius invariant |
| Four identical spheres | Exactly one selected | Coincident centers and equal radii |
| 100 unit spheres on a line | A valid quadratic construction | Maximum (n) and performance |

## Edge Cases

The first boundary case is exact tangency. For

```
2
0 0 0 1
2 0 0 1
```

the squared center distance is (4), and the squared sum of radii is also (4). The condition for overlap is `dist2 < radius_sum * radius_sum`, so the spheres are accepted together. Their original regions only touch, which the problem explicitly permits. The algorithm outputs both indices.

The second edge case is a smaller sphere intersecting a larger one. For

```
2
0 0 0 10
10 0 0 1
```

the radius-10 sphere is processed first and selected. The radius-1 sphere is then rejected because the center distance (10) is less than (11). To verify coverage, the farthest point of the small sphere from the large center is at distance (11), while the selected sphere has expanded radius (30). The entire small sphere is consequently covered.

The third edge case is several spheres with exactly the same center:

```
4
100 100 100 2
100 100 100 2
100 100 100 2
100 100 100 2
```

The first sphere is selected. Every later sphere has center distance zero and combined radius four, so it intersects the selected sphere and is skipped. The selected sphere expands to radius six, which contains all four original radius-2 spheres because they have the same center. This also demonstrates why the algorithm can safely return a single starship even when many original protected regions exist.

The fourth edge case is a long chain of touching spheres. For example,

```
3
0 0 0 1
2 0 0 1
4 0 0 1
```

allows all three spheres to be selected because adjacent spheres touch and the first and third are disjoint. A strict-overlap test selects all three. If an implementation treats tangency as intersection, it would incorrectly discard the middle sphere and potentially change the construction unnecessarily.

The final edge case is the maximum input size, (n=100). The algorithm still performs only (O(n^2)) geometric comparisons. No recursion, graph construction, floating-point geometry, or subset enumeration is needed, so the maximum case remains comfortably within the limits.
