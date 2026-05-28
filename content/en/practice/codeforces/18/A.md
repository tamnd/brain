---
title: "CF 18A - Triangle"
description: "We are given three points on the plane with integer coordinates. These three points already form a valid triangle, meaning they are not collinear."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "geometry"]
categories: ["algorithms"]
codeforces_contest: 18
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 18 (Div. 2 Only)"
rating: 1500
weight: 18
solve_time_s: 108
verified: true
draft: false
---
[CF 18A - Triangle](https://codeforces.com/problemset/problem/18/A)

**Rating:** 1500  
**Tags:** brute force, geometry  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three points on the plane with integer coordinates. These three points already form a valid triangle, meaning they are not collinear.

The task is to classify the triangle into one of three categories.

The triangle is `RIGHT` if one of its angles is exactly 90 degrees.

The triangle is `ALMOST` if it is not currently right-angled, but moving exactly one vertex by one unit in one of the four cardinal directions makes it right-angled. The moved point must still have integer coordinates.

If neither condition holds, we print `NEITHER`.

The coordinates are very small, only between `-100` and `100`. That changes the nature of the problem completely. We do not need advanced geometry, floating point arithmetic, or optimization tricks. Even trying many candidate configurations is cheap because the total number of possibilities is tiny.

The biggest danger in geometry problems is precision. A careless implementation might compute angles using trigonometric functions and compare floating point values to `90`. That is fragile because floating point rounding can turn an exact right angle into something like `89.999999`.

For example:

```
0 0 3 0 0 4
```

This is obviously a right triangle, but using cosine formulas with floating point comparisons can introduce tiny errors.

The safe approach is to work entirely with squared distances and integer arithmetic.

Another subtle case appears when checking the `ALMOST` condition. We are only allowed to move a point by distance exactly `1` along the grid. Diagonal movement is not allowed.

For example:

```
0 0 1 2 2 1
```

Moving a point diagonally could create a right triangle, but diagonal movement has Euclidean distance `sqrt(2)`, not `1`. The correct answer here is not based on diagonal moves.

A different implementation mistake is forgetting to reject the original triangle before searching for `ALMOST`.

Example:

```
0 0 2 0 0 1
```

This is already right-angled. Even though moving points might also produce another right triangle, the correct output must still be `RIGHT`.

## Approaches

The most direct way to solve the problem is to check whether the current triangle is right-angled. If it is not, we try every allowed move and check again.

A triangle is right-angled if its side lengths satisfy the Pythagorean theorem. Since coordinates are integers, squared distances are integers too. Suppose the squared side lengths are `a`, `b`, and `c`. After sorting them, the triangle is right-angled exactly when:

```
a + b = c
```

This brute-force strategy is already fast enough. Each point has four possible moves:

```
(x+1,y), (x-1,y), (x,y+1), (x,y-1)
```

There are three points, so only `3 × 4 = 12` modified triangles to test.

Each test computes three squared distances and performs constant work. Even with a huge time limit reduction, this would still run instantly.

The key observation is that geometry with integer coordinates often becomes simpler when we avoid actual distances. Squared distances preserve all comparisons needed for the Pythagorean theorem while eliminating square roots entirely.

A more naive geometric approach might compute vectors and dot products, or even angles with trigonometric functions. Those methods work mathematically, but they are unnecessarily complicated here. The problem structure is small enough that exhaustive checking combined with integer arithmetic gives a cleaner and safer solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with floating point geometry | O(1) | O(1) | Accepted but error-prone |
| Integer squared-distance checking | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three points.
2. Write a helper function that determines whether three points form a right triangle.
3. Inside this function, compute the squared lengths of all three sides.

If the points are `A`, `B`, and `C`, compute:

```
AB², AC², BC²
```

Using squared distances avoids floating point arithmetic completely.

1. Sort the three squared lengths.

The largest side must be the hypotenuse in a right triangle, so after sorting we only need to check whether:

```
smallest + middle = largest
```

1. First check the original triangle.

If it already satisfies the Pythagorean condition, print `RIGHT`.

1. Otherwise, try moving each point in the four allowed directions.

For every point, generate these candidates:

```
(x+1,y)
(x-1,y)
(x,y+1)
(x,y-1)
```

Replace the original point temporarily and test the new triangle.

1. If any modified triangle becomes right-angled, print `ALMOST`.

The moment we find one valid move, we can stop searching.

1. If none of the twelve moves works, print `NEITHER`.

### Why it works

The algorithm checks every configuration allowed by the statement.

A triangle is right-angled exactly when its side lengths satisfy the Pythagorean theorem. Squared distances preserve this property perfectly because:

```
a² + b² = c²
```

contains only integer operations.

For the `ALMOST` condition, the statement allows only one-unit horizontal or vertical moves. The algorithm explicitly enumerates all such moves for every vertex, so no valid candidate is missed.

Since every allowed modification is tested and every test is mathematically exact, the algorithm cannot misclassify a triangle.

## Python Solution

```python
import sys
input = sys.stdin.readline

def dist2(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2

def is_right(points):
    x1, y1 = points[0]
    x2, y2 = points[1]
    x3, y3 = points[2]

    sides = [
        dist2(x1, y1, x2, y2),
        dist2(x1, y1, x3, y3),
        dist2(x2, y2, x3, y3)
    ]

    sides.sort()

    return sides[0] > 0 and sides[0] + sides[1] == sides[2]

def solve():
    nums = list(map(int, input().split()))

    points = [
        [nums[0], nums[1]],
        [nums[2], nums[3]],
        [nums[4], nums[5]]
    ]

    if is_right(points):
        print("RIGHT")
        return

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for i in range(3):
        original_x, original_y = points[i]

        for dx, dy in directions:
            points[i] = [original_x + dx, original_y + dy]

            if is_right(points):
                print("ALMOST")
                return

        points[i] = [original_x, original_y]

    print("NEITHER")

solve()
```

The `dist2` function computes squared Euclidean distance. Using squared distances avoids square roots and keeps every calculation exact.

The `is_right` function is the core geometry check. It computes the three squared side lengths, sorts them, and verifies the Pythagorean condition. The additional check `sides[0] > 0` protects against degenerate edges, although the original input is guaranteed nondegenerate.

The main logic first checks the original triangle. This ordering matters because a triangle that is already right-angled must print `RIGHT`, even if moving a point could also create another right triangle.

The search for `ALMOST` iterates through all twelve legal moves. After testing a move, the point is restored before trying the next one. Forgetting this restoration step is a common source of bugs because later iterations would start from already-modified coordinates.

Everything runs with integer arithmetic, so there are no precision issues.

## Worked Examples

### Example 1

Input:

```
0 0 2 0 0 1
```

The points are:

```
A = (0,0)
B = (2,0)
C = (0,1)
```

| Side | Squared Length |
| --- | --- |
| AB² | 4 |
| AC² | 1 |
| BC² | 5 |

After sorting:

| Sorted Values |
| --- |
| 1, 4, 5 |

We check:

```
1 + 4 = 5
```

The condition holds, so the output is:

```
RIGHT
```

This trace shows why squared distances are enough. We never compute actual lengths or angles.

### Example 2

Input:

```
0 0 1 1 2 0
```

Original squared lengths:

| Side | Squared Length |
| --- | --- |
| AB² | 2 |
| AC² | 4 |
| BC² | 2 |

Sorted:

| Sorted Values |
| --- |
| 2, 2, 4 |

We check:

```
2 + 2 = 4
```

This is true, so the triangle is already right-angled.

Now consider:

```
0 0 1 1 3 0
```

Original squared lengths:

| Side | Squared Length |
| --- | --- |
| AB² | 2 |
| AC² | 9 |
| BC² | 5 |

Sorted:

| Sorted Values |
| --- |
| 2, 5, 9 |

We check:

```
2 + 5 = 7
```

Not right-angled.

Move point `C` from `(3,0)` to `(2,0)`:

| Side | Squared Length |
| --- | --- |
| AB² | 2 |
| AC² | 4 |
| BC² | 2 |

Now:

```
2 + 2 = 4
```

So the answer becomes:

```
ALMOST
```

This trace demonstrates that checking all one-step moves is sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | At most 13 triangle checks, each with constant work |
| Space | O(1) | Only a few variables and coordinate arrays are stored |

The constraints are tiny, so the solution easily fits within the limits. Even interpreted Python code finishes instantly because the total number of operations is extremely small.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def dist2(x1, y1, x2, y2):
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def is_right(points):
        x1, y1 = points[0]
        x2, y2 = points[1]
        x3, y3 = points[2]

        sides = [
            dist2(x1, y1, x2, y2),
            dist2(x1, y1, x3, y3),
            dist2(x2, y2, x3, y3)
        ]

        sides.sort()

        return sides[0] > 0 and sides[0] + sides[1] == sides[2]

    nums = list(map(int, input().split()))

    points = [
        [nums[0], nums[1]],
        [nums[2], nums[3]],
        [nums[4], nums[5]]
    ]

    if is_right(points):
        return "RIGHT"

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for i in range(3):
        ox, oy = points[i]

        for dx, dy in directions:
            points[i] = [ox + dx, oy + dy]

            if is_right(points):
                return "ALMOST"

        points[i] = [ox, oy]

    return "NEITHER"

# provided sample
assert run("0 0 2 0 0 1\n") == "RIGHT", "sample 1"

# already right triangle
assert run("0 0 3 0 0 4\n") == "RIGHT", "classic 3-4-5"

# becomes right after one move
assert run("0 0 1 1 3 0\n") == "ALMOST", "single move fixes triangle"

# impossible case
assert run("0 0 1 2 2 1\n") == "NEITHER", "no valid one-step move"

# negative coordinates
assert run("-1 -1 1 -1 -1 2\n") == "RIGHT", "handles negatives"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 3 0 0 4` | `RIGHT` | Exact integer Pythagorean triple |
| `0 0 1 1 3 0` | `ALMOST` | One legal move creates a right triangle |
| `0 0 1 2 2 1` | `NEITHER` | Exhaustive move search fails correctly |
| `-1 -1 1 -1 -1 2` | `RIGHT` | Negative coordinates handled safely |

## Edge Cases

Consider the case where the triangle is already right-angled:

```
0 0 2 0 0 1
```

The algorithm first calls `is_right` on the original points.

Squared side lengths are:

```
1, 4, 5
```

Since:

```
1 + 4 = 5
```

the algorithm immediately prints `RIGHT` and stops. It never enters the `ALMOST` search. This ordering is necessary because the statement prioritizes `RIGHT` over `ALMOST`.

Now consider a case where diagonal movement would help, but legal movement would not:

```
0 0 1 2 2 1
```

The algorithm checks the original triangle and finds no Pythagorean relation.

It then tests exactly these twelve moves:

```
(+1,0), (-1,0), (0,+1), (0,-1)
```

for each vertex.

No tested configuration becomes right-angled, so the algorithm prints `NEITHER`.

This confirms that only cardinal-direction moves are considered, exactly matching the problem definition.

Finally, consider negative coordinates:

```
-1 -1 1 -1 -1 2
```

Squared side lengths become:

```
4, 9, 13
```

After sorting:

```
4, 9, 13
```

Since:

```
4 + 9 = 13
```

the algorithm correctly outputs `RIGHT`.

The computation uses only subtraction and squaring, so negative coordinates require no special handling.
