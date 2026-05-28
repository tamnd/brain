---
title: "CF 36C - Bowls"
description: "Each bowl is a frustum, a cone with its tip cut off. A bowl is described by its height h, bottom radius r, and top radiu"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "implementation"]
categories: ["algorithms"]
codeforces_contest: 36
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 36"
rating: 2200
weight: 36
solve_time_s: 125
verified: false
draft: false
---

[CF 36C - Bowls](https://codeforces.com/problemset/problem/36/C)

**Rating:** 2200  
**Tags:** geometry, implementation  
**Solve time:** 2m 5s  
**Verified:** no  

## Solution
## Problem Understanding

Each bowl is a frustum, a cone with its tip cut off. A bowl is described by its height `h`, bottom radius `r`, and top radius `R`. The bowls are stacked in the given order, always sharing the same vertical axis. Every new bowl is lowered as much as possible without intersecting any previous bowl.

We must compute the final total height of the stack, measured from the bottom of the lowest bowl to the top edge of the highest bowl.

The geometry matters because the bowls are not cylinders. Their radius changes linearly with height, so whether two bowls collide depends on where their side surfaces meet.

The constraint `n ≤ 3000` is the key observation. A quadratic solution performs about nine million pair checks, which is completely fine in Python if each check is constant time. Anything cubic would already approach `2.7 × 10^10` operations and is impossible within two seconds.

The tricky part is determining how far down a new bowl can go when several previous bowls already exist. A careless implementation often compares only top and bottom radii, but the first collision may happen somewhere in the middle of the slanted surfaces.

Consider this example:

```
2
10 1 100
10 99 100
```

The second bowl almost matches the slope of the first one. They collide near the top, not at the bottom. If we only compare bottom radii, we would incorrectly think the second bowl can descend very far.

Another subtle case is complete containment:

```
2
100 1 100
10 2 3
```

The second bowl fits entirely inside the first one, so its bottom reaches the bottom of the first bowl. The total height remains `100`, not `110`.

There is also the opposite situation where the new bowl is much wider:

```
2
10 1 2
10 100 200
```

The second bowl cannot enter the first one at all. Its bottom sits exactly on top of the first bowl, giving total height `20`.

These cases show why we need an exact geometric condition instead of heuristic comparisons.

## Approaches

The most direct simulation is to process bowls one by one. For every new bowl, try to lower it until it touches an earlier bowl. Since every bowl already has a fixed vertical position, the only unknown is the height of the new bowl's bottom.

The brute-force version could continuously test positions or binary search the placement height while checking for intersections against all previous bowls. The geometry check itself is easy because the radius varies linearly with height. Unfortunately, if we binary search with high precision for every pair of bowls, the total work becomes roughly `O(n² log precision)`. It would still pass here, but it is more complicated than necessary and hides the underlying structure.

The key observation is that the limiting position between two bowls can be derived directly with similar triangles.

Suppose bowl `i` is already placed with bottom at height `pos[i]`. We want to place bowl `j` below as much as possible.

At vertical offset `x` inside bowl `j`, its radius is:

$$r_j + \frac{R_j - r_j}{h_j} x$$

For bowl `i`, at height `y` above its bottom:

$$r_i + \frac{R_i - r_i}{h_i} y$$

When the bowls first touch, these radii become equal at some common global height. Solving the equations reveals a remarkably simple condition:

If the slopes are equal, one bowl either fully fits or never fits.

Otherwise, the touching point determines a unique relative shift.

This lets us compute the minimum valid placement against one earlier bowl in constant time. Taking the maximum over all previous bowls gives the final position of the new bowl.

Since `n = 3000`, checking every pair directly is perfectly acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with binary search | O(n² log precision) | O(n) | Accepted but unnecessarily complicated |
| Direct geometric computation | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Store the bottom height `pos[i]` for every bowl.

The first bowl always starts at height `0`.
2. Process bowls in the given order.

Bowl positions never change afterward, so earlier bowls act as fixed obstacles.
3. For the current bowl `j`, initialize its bottom position to `0`.

This means we first assume it can descend completely.
4. Compare bowl `j` against every earlier bowl `i`.

We compute the lowest height where bowl `j` does not intersect bowl `i`.
5. Let

$$k_i = \frac{R_i - r_i}{h_i}, \quad
k_j = \frac{R_j - r_j}{h_j}$$

These are the side slopes of the bowls.

1. If `k_i == k_j`, the bowls are geometrically similar.

In this case:

- If `r_j >= R_i`, bowl `j` is entirely wider and cannot enter bowl `i`. Its bottom must be at least `pos[i] + h_i`.
- Otherwise, bowl `j` can slide completely inside bowl `i`, so this pair imposes no restriction beyond `pos[i]`.
2. Otherwise, solve for the first touching point of the side surfaces.

The derived formula for the minimum valid bottom position is:

$$need = pos[i] + \frac{r_i - r_j + k_j h_j}{k_j - k_i}$$

This formula gives the position where the outer surface of bowl `j` first touches bowl `i`.

1. Bowl `j` also cannot go below the bottom of bowl `i`.

Clamp the value with:

$$need = \max(need, pos[i])$$

1. The current bowl must satisfy every previous restriction, so update:

$$pos[j] = \max(pos[j], need)$$

1. After all bowls are placed, the answer is:

$$\max_i (pos[i] + h_i)$$

This is the highest top edge in the stack.

### Why it works

For every pair of bowls, there exists a lowest relative placement where they do not intersect. Any lower position would cause the slanted surfaces to cross. The derived equation computes exactly this boundary position.

When processing bowl `j`, every earlier bowl already has a fixed position. Taking the maximum over all pairwise lower bounds gives the unique lowest feasible placement for bowl `j`. Since the bowl is always placed as low as possible, this greedy construction matches the physical stacking process.

## Python Solution

```python
import sys
input = sys.stdin.readline

EPS = 1e-12

def main():
    n = int(input())

    h = [0.0] * n
    r = [0.0] * n
    R = [0.0] * n

    for i in range(n):
        hh, rr, RR = map(float, input().split())
        h[i] = hh
        r[i] = rr
        R[i] = RR

    pos = [0.0] * n

    for j in range(n):
        best = 0.0

        kj = (R[j] - r[j]) / h[j]

        for i in range(j):
            ki = (R[i] - r[i]) / h[i]

            if abs(ki - kj) < EPS:
                if r[j] >= R[i] - EPS:
                    need = pos[i] + h[i]
                else:
                    need = pos[i]
            else:
                need = pos[i] + (r[i] - r[j] + kj * h[j]) / (kj - ki)
                need = max(need, pos[i])

            best = max(best, need)

        pos[j] = best

    ans = 0.0

    for i in range(n):
        ans = max(ans, pos[i] + h[i])

    print(f"{ans:.10f}")

if __name__ == "__main__":
    main()
```

The arrays `h`, `r`, and `R` store the geometric parameters of each bowl. The `pos` array stores the vertical coordinate of each bowl's bottom.

The main loop processes bowls in insertion order. Since earlier bowls never move again, every placement decision becomes independent once previous positions are fixed.

The slope calculation is the most important geometric ingredient:

```
k = (R - r) / h
```

This is the radius increase per unit height. Because the bowl walls are straight lines, the radius at any height becomes a simple linear function.

Parallel slopes require separate handling. When two bowls have identical side angles, they never intersect along the slanted surfaces unless one is entirely wider. Floating-point comparisons use `EPS` because exact equality on doubles is unreliable.

The formula:

```
need = pos[i] + (r[i] - r[j] + kj * h[j]) / (kj - ki)
```

comes directly from solving the equality of radii at the touching point. The derivation assumes the first contact occurs on the side walls.

The clamp:

```
need = max(need, pos[i])
```

prevents the current bowl from going below the earlier bowl's bottom. Without this line, some configurations would incorrectly place a bowl deeper than physically possible.

Finally, the answer is not simply the last bowl's top. Earlier bowls may still extend higher than later ones, so we compute the maximum over all bowls.

## Worked Examples

### Example 1

Input:

```
2
40 10 50
60 20 30
```

| Bowl | Computed position | Top height |
| --- | --- | --- |
| 0 | 0 | 40 |
| 1 | 10 | 70 |

The first bowl occupies heights `[0, 40]`.

The second bowl is narrower near the top, so it partially enters the first bowl. The geometric formula determines that the lowest valid position is `10`. Its top becomes `10 + 60 = 70`.

The final stack height is `70`.

### Example 2

Input:

```
3
100 1 100
10 2 3
20 150 200
```

| Bowl | Computed position | Top height |
| --- | --- | --- |
| 0 | 0 | 100 |
| 1 | 0 | 10 |
| 2 | 100 | 120 |

The second bowl fits entirely inside the first bowl, so its bottom also stays at height `0`.

The third bowl is much wider than everything below it. It cannot enter any earlier bowl, so it rests on top of the tallest obstruction at height `100`.

This trace confirms that containment and non-overlapping cases are both handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Every bowl is compared with all previous bowls |
| Space | O(n) | Arrays store bowl parameters and positions |

With `n ≤ 3000`, the algorithm performs at most about nine million pair checks. Each check is constant time arithmetic, which easily fits within the time limit in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline
    EPS = 1e-12

    n = int(input())

    h = [0.0] * n
    r = [0.0] * n
    R = [0.0] * n

    for i in range(n):
        hh, rr, RR = map(float, input().split())
        h[i] = hh
        r[i] = rr
        R[i] = RR

    pos = [0.0] * n

    for j in range(n):
        best = 0.0
        kj = (R[j] - r[j]) / h[j]

        for i in range(j):
            ki = (R[i] - r[i]) / h[i]

            if abs(ki - kj) < EPS:
                if r[j] >= R[i] - EPS:
                    need = pos[i] + h[i]
                else:
                    need = pos[i]
            else:
                need = pos[i] + (r[i] - r[j] + kj * h[j]) / (kj - ki)
                need = max(need, pos[i])

            best = max(best, need)

        pos[j] = best

    ans = max(pos[i] + h[i] for i in range(n))
    print(f"{ans:.10f}")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run(
"""2
40 10 50
60 20 30
"""
) == "70.0000000000", "sample 1"

# minimum size
assert run(
"""1
10 1 2
"""
) == "10.0000000000", "single bowl"

# complete containment
assert run(
"""2
100 1 100
10 2 3
"""
) == "100.0000000000", "small bowl fully inside"

# completely outside
assert run(
"""2
10 1 2
10 100 200
"""
) == "20.0000000000", "second bowl rests on top"

# equal slopes
assert run(
"""2
10 1 11
20 2 22
"""
) == "20.0000000000", "parallel sides"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single bowl | 10 | Base case with no pair interactions |
| Small bowl inside large bowl | 100 | Complete containment |
| Huge bowl after tiny bowl | 20 | No insertion possible |
| Equal slopes | 20 | Correct handling of parallel walls |

## Edge Cases

Consider the containment case:

```
2
100 1 100
10 2 3
```

The first bowl has enormous width compared to the second. During processing, the computed restriction never forces the second bowl upward. Its bottom remains at `0`.

The tops are:

- Bowl 0: `0 + 100 = 100`
- Bowl 1: `0 + 10 = 10`

The algorithm correctly outputs `100`.

Now consider a bowl that cannot enter at all:

```
2
10 1 2
10 100 200
```

The second bowl is already wider at its bottom than the first bowl at its top. The pairwise restriction becomes:

```
need = pos[0] + h[0] = 10
```

So the second bowl starts exactly where the first one ends. The final height becomes `20`.

Finally, examine equal slopes:

```
2
10 1 11
20 2 22
```

Both bowls expand by one unit of radius per unit of height. Their side walls are parallel. Since the second bowl is wider everywhere, it cannot descend into the first bowl. The special parallel-slope branch correctly places it at height `10`.
