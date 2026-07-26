---
title: "CF 102822H - Hide and Seek"
description: "We are given three Manhattan distances. One player is at an unknown integer coordinate (x1, y1), the other is at (x2, y2), and the origin is the third reference point."
date: "2026-07-26T15:55:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102822
codeforces_index: "H"
codeforces_contest_name: "2020 China Collegiate Programming Contest - Mianyang Site"
rating: 0
weight: 102822
solve_time_s: 51
verified: true
draft: false
---

[CF 102822H - Hide and Seek](https://codeforces.com/problemset/problem/102822/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three Manhattan distances. One player is at an unknown integer coordinate `(x1, y1)`, the other is at `(x2, y2)`, and the origin is the third reference point. The first distance tells us how far the first player is from `(0,0)`, the second tells us the same for the second player, and the third tells us the distance between the two players. The task is to count how many ordered pairs of integer positions satisfy all three measurements. Swapping the two players creates a different situation.

The input contains up to `100000` independent test cases, and each distance can be as large as `10^9`. A direct enumeration of possible coordinates is impossible because even one Manhattan circle can contain billions of integer points. The solution has to process every test case in constant time.

The main trap cases are caused by parity. After transforming the coordinates, not every point in the transformed plane corresponds to an integer point in the original plane. Another common mistake is forgetting that the two players are ordered.

For example, if the input is:

```
1
1 1 1
```

the answer is `0`. Two points at Manhattan distance `1` from the origin cannot also be at Manhattan distance `1` from each other in this way while respecting the required parity of transformed coordinates. A solution that counts all transformed square boundary points without checking parity overcounts.

Another edge case is both players being at the origin:

```
1
0 0 0
```

The answer is `1`, because both coordinates must be `(0,0)`. A formula based only on the size of the squares may accidentally count nonexistent directions.

The third important case is when the two measured distances from the origin are different but the players are swapped. For:

```
1
2 4 2
```

the answer counts the situation with the first player on the distance-2 layer and the second player on the distance-4 layer separately from the reversed arrangement. Treating the pair as unordered loses valid answers.

## Approaches

A brute force solution would generate every integer point with Manhattan distance `d01` from the origin, generate every point with Manhattan distance `d02`, and test every pair. The number of points on a Manhattan circle of radius `r` is proportional to `r`, so the worst case is about `10^9` points per layer. Pairing them gives far beyond feasible limits.

The key observation is that Manhattan distance becomes much simpler after rotating the coordinate system. Define:

```
u = x + y
v = x - y
```

For two points, the Manhattan distance becomes:

```
max(|u1-u2|, |v1-v2|)
```

and the distance from the origin becomes:

```
max(|u|, |v|)
```

So the problem changes from diamonds in the original plane into axis-aligned squares in the `(u,v)` plane.

A point `(u,v)` represents integer `(x,y)` only when `u` and `v` have the same parity. Instead of enumerating the square border, we count pairs inside squares and use inclusion-exclusion to recover borders.

Let `G(a,b,r)` be the number of pairs of transformed points where the first point is inside the square of radius `a`, the second is inside the square of radius `b`, and their Chebyshev distance is at most `r`. Then the number of pairs exactly on the two required layers is:

```
G(a,b,r) - G(a-1,b,r) - G(a,b-1,r) + G(a-1,b-1,r)
```

Finally, the answer for exact distance `c` is the number with distance at most `c` minus the number with distance at most `c-1`.

To compute `G`, we split transformed points by parity. A point can have `(u,v)` both even or both odd. For each choice of parity of the first point and the second point, the two coordinates become independent one-dimensional counting problems.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(d01 * d02) | O(1) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Convert the Manhattan problem into a Chebyshev problem using `u=x+y` and `v=x-y`.

The transformation changes diamonds into squares, which lets us reason about axis-aligned ranges.

1. Implement a function that counts pairs of transformed points inside two squares with distance at most `r`.

A square of radius `a` contains all points where both transformed coordinates are between `-a` and `a`. We count these square regions first because borders are harder to handle directly.

1. Split the counting by parity.

For every possible parity of the first point and second point, count valid `u` coordinates and valid `v` coordinates independently. The product of those two counts gives the number of two-dimensional pairs for that parity combination.

1. Use one-dimensional prefix counting.

For one coordinate, after dividing by two, we need to count pairs of indices whose difference lies in an interval. This can be done by computing the prefix count of pairs with difference at most a value.

1. Convert square counts into layer counts using inclusion-exclusion.

Subtract the inner squares from the outer squares so only points at exactly the required Manhattan distances remain.

1. Compute the exact distance answer.

The required distance is exactly `d12`, so calculate the number with distance at most `d12` and subtract the number with distance at most `d12-1`.

Why it works:

The coordinate transformation preserves the distances needed by the problem. Every valid original point maps to exactly one transformed point with matching coordinate parity, and every transformed point with equal coordinate parity maps back to exactly one integer point. The square inclusion-exclusion removes every point that is not on the requested distance layer exactly once. The final subtraction removes all pairs whose distance is smaller than the required third distance, leaving exactly the pairs with the desired distance.

## Python Solution

```python
import sys
input = sys.stdin.readline

def ceil_div(a, b):
    return -((-a) // b)

def sum_range(l, r):
    if l > r:
        return 0
    return (l + r) * (r - l + 1) // 2

def prefix_diff(n1, n2, s):
    # number of pairs (i, j), 0 <= i < n1, 0 <= j < n2, i-j <= s
    ans = 0

    l = 0
    r = min(n1 - 1, s)
    if l <= r:
        ans += (r - l + 1) * n2

    l = max(0, s + 1)
    r = min(n1 - 1, s + n2 - 1)
    if l <= r:
        ans += (r - l + 1) * (n2 + s) - sum_range(l, r)

    return ans

def count_difference(l1, r1, l2, r2, lo, hi):
    if l1 > r1 or l2 > r2:
        return 0
    n1 = r1 - l1 + 1
    n2 = r2 - l2 + 1
    shift = l1 - l2
    return prefix_diff(n1, n2, hi - shift) - prefix_diff(n1, n2, lo - 1 - shift)

def coordinate_count(a, b, r, p, q):
    if a < 0 or b < 0:
        return 0

    l1 = ceil_div(-a - p, 2)
    r1 = (a - p) // 2
    l2 = ceil_div(-b - q, 2)
    r2 = (b - q) // 2

    if l1 > r1 or l2 > r2:
        return 0

    diff = p - q
    lo = ceil_div(-r - diff, 2)
    hi = (r - diff) // 2

    return count_difference(l1, r1, l2, r2, lo, hi)

def square_count(a, b, r):
    if a < 0 or b < 0:
        return 0

    ans = 0
    for p in (0, 1):
        for q in (0, 1):
            c = coordinate_count(a, b, r, p, q)
            ans += c * c
    return ans

def inside_layers(a, b, r):
    return (
        square_count(a, b, r)
        - square_count(a - 1, b, r)
        - square_count(a, b - 1, r)
        + square_count(a - 1, b - 1, r)
    )

def solve_case(a, b, c):
    if c < 0:
        return 0
    return inside_layers(a, b, c) - inside_layers(a, b, c - 1)

t = int(input())
out = []
for case in range(1, t + 1):
    a, b, c = map(int, input().split())
    out.append(f"Case #{case}: {solve_case(a, b, c)}")

print("\n".join(out))
```

The `ceil_div` helper is needed because Python's integer division rounds downward, while the mathematical ceiling division is required when converting coordinate ranges.

The `prefix_diff` function is the core one-dimensional counting routine. It splits the possible first indices into three regions: indices where every second coordinate works, indices where only part of the interval works, and indices where no second coordinate works.

`coordinate_count` converts a transformed coordinate range into an index range by fixing a parity. The distance condition becomes a range on the difference of the two indices.

`square_count` combines the four parity combinations. The multiplication by itself is valid because the `u` and `v` dimensions are independent after the transformation.

`inside_layers` applies inclusion-exclusion to remove the inner square layers. Finally, `solve_case` changes a "distance at most" count into an exact distance count.

## Worked Examples

For the first sample:

```
2 4 2
```

The important values during the calculation are:

| Step | First radius | Second radius | Distance limit | Result |
| --- | --- | --- | --- | --- |
| Count at most 2 | 2 | 4 | 2 | 32 |
| Count at most 1 | 2 | 4 | 1 | 0 |
| Final answer |  |  |  | 32 |

The example demonstrates that exact distance counting is obtained by subtracting the smaller distance region. Every valid pair appears in the first count and disappears only when its distance is below the target.

For the fourth sample:

```
1 1 1
```

| Step | First radius | Second radius | Distance limit | Result |
| --- | --- | --- | --- | --- |
| Count at most 1 | 1 | 1 | 1 | 0 |
| Count at most 0 | 1 | 1 | 0 | 0 |
| Final answer |  |  |  | 0 |

This case confirms that parity restrictions remove transformed points that do not correspond to integer coordinates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Each test case performs a fixed number of arithmetic operations and parity checks |
| Space | O(1) | Only scalar variables are stored |

The input size is large because there can be `100000` test cases, so the solution avoids loops depending on the distances. All operations are constant time and fit comfortably within the limits.

## Test Cases

```
# These tests are intended to be run with the submitted solution.

def brute(a, b, c):
    ans = 0
    for x1 in range(-10, 11):
        for y1 in range(-10, 11):
            if abs(x1) + abs(y1) != a:
                continue
            for x2 in range(-10, 11):
                for y2 in range(-10, 11):
                    if abs(x2) + abs(y2) == b and abs(x1-x2)+abs(y1-y2) == c:
                        ans += 1
    return ans

assert solve_case(0, 0, 0) == 1
assert solve_case(1, 1, 1) == 0
assert solve_case(2, 4, 2) == 32
assert solve_case(1, 3, 2) == 20
assert solve_case(3, 4, 5) == 48
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 0` | `1` | Both players at the origin |
| `1 1 1` | `0` | Parity restrictions |
| `2 4 2` | `32` | Different radii and ordered positions |
| `1 3 2` | `20` | Small non-trivial layers |
| `3 4 5` | `48` | Larger transformed square interaction |

## Edge Cases

For:

```
1
0 0 0
```

both transformed squares have radius zero. Inclusion-exclusion leaves only the single transformed point `(0,0)`, which corresponds to the original point `(0,0)`.

For:

```
1
1 1 1
```

the transformed square has several points, but only points where `u` and `v` share parity are valid. The parity split in `square_count` discards invalid transformed points before counting.

For:

```
1
2 4 2
```

the two players belong to different Manhattan layers. The inclusion-exclusion keeps only the border of each square, and the final distance subtraction keeps only pairs whose Chebyshev distance is exactly two.

For cases with extremely large distances such as:

```
1
1000000000 1000000000 1000000000
```

the algorithm never iterates through the coordinate range. All calculations are done with integer arithmetic, so the large bounds only affect the size of the intermediate values. Python integers handle these values safely.
