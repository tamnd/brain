---
title: "CF 105164C - Chocolate Packing"
description: "We are given two rectangular prisms. One is a large shipping container with dimensions $L times W times H$, and the other is a smaller identical chocolate box with dimensions $l times w times h$. The goal is to determine how many small boxes can be packed inside the large one."
date: "2026-06-27T10:43:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105164
codeforces_index: "C"
codeforces_contest_name: "2024 ICPC Gran Premio de Mexico 1ra Fecha"
rating: 0
weight: 105164
solve_time_s: 80
verified: false
draft: false
---

[CF 105164C - Chocolate Packing](https://codeforces.com/problemset/problem/105164/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two rectangular prisms. One is a large shipping container with dimensions $L \times W \times H$, and the other is a smaller identical chocolate box with dimensions $l \times w \times h$. The goal is to determine how many small boxes can be packed inside the large one.

The key restriction is that every chocolate box must share the same orientation relative to the shipping box. That means we are not packing arbitrarily rotated boxes per placement, but rather we choose a single fixed orientation of the small box and then pack them in a grid-aligned way along the three axes of the container. Each box must align edge-to-edge with the shipping box axes.

The problem reduces to choosing the best permutation of $(l, w, h)$ assigned to $(L, W, H)$, and then computing how many full intervals of each dimension fit.

The constraints are small: all dimensions are at most 1000. This immediately rules out any need for simulation or search over placements. Even checking all possible orientations is constant work since there are only six permutations of the box dimensions.

A naive but incorrect idea is to compute $(L // l) \cdot (W // w) \cdot (H // h)$ without considering that rotating the small box might improve the fit. For example, if $L = 6, W = 5, H = 4$ and the box is $2 \times 1 \times 3$, using the wrong orientation could underutilize space, while the optimal rotation yields a higher packing count.

Another subtle issue is assuming partial fits contribute, but fractional boxes are not allowed. Any leftover space smaller than a full box in any dimension is wasted.

## Approaches

The brute-force method tries every possible orientation of the chocolate box. Since there are three dimensions, there are exactly six permutations. For each permutation, we compute how many boxes fit along each axis using integer division, then multiply the results.

This works because once an orientation is fixed, the packing becomes a perfect 3D grid. The number of placements along each axis is independent of the others, so multiplication is valid.

The brute-force approach is already optimal in terms of complexity because the search space is constant size. There is no benefit in trying to simulate placements or consider partial packing strategies.

The key insight is that orientation is the only degree of freedom. Once orientation is fixed, the problem becomes a direct volume-aligned tiling problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over orientations | O(1) | O(1) | Accepted |
| Optimal (same idea) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the dimensions of the shipping box and the chocolate box. These define the two 3D rectangles we are working with.
2. Generate all six permutations of the chocolate box dimensions. Each permutation represents a distinct orientation of how the small box could be aligned inside the large one.
3. For each permutation, compute how many boxes fit along each axis using integer division: $L // x$, $W // y$, $H // z$. This ensures we only count full boxes that fit completely.
4. Multiply the three values to get the total number of boxes for that orientation. This works because boxes form a uniform 3D grid once orientation is fixed.
5. Track the maximum value across all orientations.
6. Output the maximum.

### Why it works

Once a fixed orientation is chosen, the packing problem decomposes into three independent 1D packing problems along each axis. Since boxes cannot overlap or rotate individually, the optimal packing for that orientation is always the full grid formed by greedy placement along each dimension. Any leftover space is strictly smaller than a full box dimension, so it cannot contribute additional boxes. Therefore, the best solution must come from one of the six axis-aligned permutations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    L, W, H = map(int, input().split())
    l, w, h = map(int, input().split())

    dims = (l, w, h)
    from itertools import permutations

    best = 0
    for x, y, z in permutations(dims):
        count = (L // x) * (W // y) * (H // z)
        if count > best:
            best = count

    print(best)

if __name__ == "__main__":
    main()
```

The code starts by reading both sets of dimensions. It then enumerates all six possible orientations using permutations of the small box dimensions. For each orientation, it computes how many boxes fit along each axis using integer division, ensuring only fully contained boxes are counted. The product gives the total number of boxes for that orientation. The maximum across all orientations is printed.

A subtle but important detail is using integer division at every axis independently before multiplication. Multiplying first or using floating division would introduce incorrect rounding behavior.

## Worked Examples

### Example 1

Input:

```
6 5 4
2 1 3
```

We evaluate all orientations of (2,1,3).

| Orientation (x,y,z) | L//x | W//y | H//z | Total |
| --- | --- | --- | --- | --- |
| (2,1,3) | 3 | 5 | 1 | 15 |
| (2,3,1) | 3 | 1 | 4 | 12 |
| (1,2,3) | 6 | 2 | 1 | 12 |
| (1,3,2) | 6 | 1 | 2 | 12 |
| (3,2,1) | 2 | 2 | 4 | 16 |
| (3,1,2) | 2 | 5 | 2 | 20 |

Maximum is 20.

This trace shows that orientation choice dominates the solution. The best packing is not obvious without checking all permutations, since different axis assignments interact multiplicatively.

### Example 2

Input:

```
1 1 13
3 3 3
```

| Orientation (x,y,z) | L//x | W//y | H//z | Total |
| --- | --- | --- | --- | --- |
| any permutation | 0 or 0 or 4 | ... | ... | 0 |

Every orientation fails because at least one dimension of the box exceeds the container dimension, producing zero fit.

This confirms that the algorithm correctly handles cases where no boxes can be placed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only six permutations are checked, each involving constant-time arithmetic |
| Space | O(1) | Only a fixed number of variables are stored |

The constraints allow direct enumeration of all orientations. Since the computation per orientation is constant, the solution is trivially within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    L, W, H = map(int, input().split())
    l, w, h = map(int, input().split())

    from itertools import permutations

    best = 0
    for x, y, z in permutations((l, w, h)):
        best = max(best, (L // x) * (W // y) * (H // z))

    return str(best).strip()

# provided samples
assert run("1 1 13\n3 3 3\n") == "0"
assert run("6 5 4\n2 1 3\n") == "20"

# minimum-size inputs
assert run("1 1 1\n1 1 1\n") == "1"

# all-fit single layer
assert run("10 10 10\n2 2 2\n") == "125"

# one dimension blocks everything
assert run("5 5 5\n6 1 1\n") == "0"

# asymmetric optimal rotation case
assert run("4 6 8\n3 2 1\n") == "32"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 / 1 1 1 | 1 | minimal exact fit |
| 10 10 10 / 2 2 2 | 125 | uniform grid packing |
| 5 5 5 / 6 1 1 | 0 | impossible placement |
| 4 6 8 / 3 2 1 | 32 | rotation matters |

## Edge Cases

One important edge case occurs when one dimension of the chocolate box exceeds a corresponding dimension of the shipping box. For example:

Input:

```
5 5 5
6 1 1
```

For any permutation, at least one axis produces zero via integer division, so the final result is zero. The algorithm naturally handles this because multiplication with zero propagates correctly.

Another case is when all dimensions are equal:

Input:

```
3 3 3
1 1 1
```

Every orientation yields $3 \cdot 3 \cdot 3 = 27$. The permutation loop computes identical values, and the maximum remains correct.

Finally, when dimensions are highly asymmetric, the optimal solution may require a non-obvious permutation. The exhaustive check over six orientations guarantees correctness regardless of skew.
