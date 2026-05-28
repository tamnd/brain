---
title: "CF 227A - Where do I Turn?"
description: "The hero starts at point A, rides to point B, and then must continue toward point C. At point B, he is facing in the direction from A to B. We need to determine whether reaching C requires turning left, turning right, or continuing straight."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry"]
categories: ["algorithms"]
codeforces_contest: 227
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 140 (Div. 2)"
rating: 1300
weight: 227
solve_time_s: 155
verified: true
draft: false
---

[CF 227A - Where do I Turn?](https://codeforces.com/problemset/problem/227/A)

**Rating:** 1300  
**Tags:** geometry  
**Solve time:** 2m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

The hero starts at point `A`, rides to point `B`, and then must continue toward point `C`. At point `B`, he is facing in the direction from `A` to `B`. We need to determine whether reaching `C` requires turning left, turning right, or continuing straight.

The geometry constraints simplify the problem a lot. The roads are guaranteed to be either parallel, collinear, or perpendicular. That means the movement from `B` to `C` is either in the same direction as `A -> B`, in the exact opposite direction, or rotated by exactly 90 degrees. The statement additionally guarantees that either all three points are collinear or angle `ABC` is a right angle.

The coordinates can be as large as `10^9`, both positive and negative. That rules out any approach involving grids, simulation, or floating point geometry. We only need a few arithmetic operations on coordinates, so an `O(1)` solution is the natural target.

A common mistake is mixing up the orientation direction. The hero stands at `B` while facing away from `A`, so the relevant direction vector is:

```
AB = B - A
```

and not `BA = A - B`.

For example:

```
A = (0, 0)
B = (0, 1)
C = (1, 1)
```

The hero moves upward from `A` to `B`. To reach `C`, he must turn right. Using the reversed vector would incorrectly produce `LEFT`.

Another easy mistake appears in straight-line cases.

Example:

```
A = (0, 0)
B = (1, 0)
C = (2, 0)
```

The correct answer is:

```
TOWARDS
```

A careless implementation that only checks the sign of a cross product might misclassify this because the cross product is zero. We must explicitly handle the collinear case separately.

Negative coordinates can also expose sign errors.

Example:

```
A = (0, 0)
B = (-1, 0)
C = (-1, -1)
```

The hero moves left, then downward. That is a left turn, not a right turn. Visual intuition becomes harder with negative axes, which is why relying on the orientation formula is safer than mentally drawing cases.

## Approaches

The brute-force way to solve this problem is to explicitly model the hero's direction and compare it against all possible valid moves. Since the movement rules only allow straight, left, or right turns, we could construct the direction vector from `A` to `B`, rotate it manually in both directions, and compare each result with the vector from `B` to `C`.

For instance, if the hero moves with vector `(dx, dy)`, then:

```
Left rotation  = (-dy, dx)
Right rotation = (dy, -dx)
```

We could compare `BC` against these transformed vectors and decide the answer. This works correctly because the problem guarantees only these three possibilities.

The brute-force method is already constant time, so there is no performance issue here. Still, it relies on manually handling geometric transformations and special cases for collinearity.

A cleaner observation is that this is exactly the standard orientation test from computational geometry. Given two vectors:

```
u = AB
v = BC
```

their 2D cross product tells us the turn direction:

```
cross = ux * vy - uy * vx
```

If the cross product is positive, the rotation from `u` to `v` is counterclockwise, meaning a left turn.

If it is negative, the turn is clockwise, meaning a right turn.

If it is zero, the vectors are collinear, so the hero continues straight.

This reduces the whole problem to a single arithmetic formula.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with manual rotations | O(1) | O(1) | Accepted |
| Cross product orientation test | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the coordinates of points `A`, `B`, and `C`.
2. Construct the direction vector from `A` to `B`.

```
AB = (xb - xa, yb - ya)
```

This represents the direction the hero is currently facing.

1. Construct the direction vector from `B` to `C`.

```
BC = (xc - xb, yc - yb)
```

This represents the direction the hero wants to move next.

1. Compute the 2D cross product:

```
cross = AB.x * BC.y - AB.y * BC.x
```

The sign of this value determines the orientation between the two vectors.

1. If `cross > 0`, print `"LEFT"`.

A positive cross product means the rotation from `AB` to `BC` is counterclockwise.

1. If `cross < 0`, print `"RIGHT"`.

A negative cross product means the rotation is clockwise.

1. Otherwise, print `"TOWARDS"`.

A zero cross product means both vectors lie on the same line.

### Why it works

The cross product measures signed area and orientation in 2D geometry. For vectors `u` and `v`, the sign of:

```
u.x * v.y - u.y * v.x
```

tells whether rotating from `u` to `v` goes counterclockwise or clockwise.

The hero's current facing direction is exactly vector `AB`, and the desired next direction is `BC`. Because the problem guarantees only left turns, right turns, or straight movement, the cross product completely determines the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

xa, ya = map(int, input().split())
xb, yb = map(int, input().split())
xc, yc = map(int, input().split())

abx = xb - xa
aby = yb - ya

bcx = xc - xb
bcy = yc - yb

cross = abx * bcy - aby * bcx

if cross > 0:
    print("LEFT")
elif cross < 0:
    print("RIGHT")
else:
    print("TOWARDS")
```

The first part of the code reads the three points and converts them into direction vectors. Using vectors instead of absolute coordinates is the key geometric step because turns depend on relative movement, not position.

The cross product computation is the heart of the solution:

```
cross = abx * bcy - aby * bcx
```

The order matters. Swapping the vectors reverses the sign and flips left/right answers.

Python integers automatically handle very large values, so coordinates near `10^9` are safe. In languages like C++, using `long long` would be necessary because products can reach about `10^18`.

The final conditional directly maps orientation to the required output. Zero must be checked separately because collinear vectors are neither left nor right turns.

## Worked Examples

### Example 1

Input:

```
0 0
0 1
1 1
```

| Variable | Value |
| --- | --- |
| AB | (0, 1) |
| BC | (1, 0) |
| cross | -1 |
| Result | RIGHT |

The hero moves upward first, then turns toward the positive x-axis. That rotation is clockwise, so the answer is `"RIGHT"`.

### Example 2

Input:

```
0 0
1 0
2 0
```

| Variable | Value |
| --- | --- |
| AB | (1, 0) |
| BC | (1, 0) |
| cross | 0 |
| Result | TOWARDS |

Both vectors point in exactly the same direction. The cross product becomes zero, confirming that the hero continues straight ahead.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed |
| Space | O(1) | No extra data structures are used |

The solution easily fits within the limits because it performs constant-time integer arithmetic regardless of coordinate size.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    xa, ya = map(int, input().split())
    xb, yb = map(int, input().split())
    xc, yc = map(int, input().split())

    abx = xb - xa
    aby = yb - ya

    bcx = xc - xb
    bcy = yc - yb

    cross = abx * bcy - aby * bcx

    if cross > 0:
        print("LEFT")
    elif cross < 0:
        print("RIGHT")
    else:
        print("TOWARDS")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output.strip()

# provided sample
assert run(
"""0 0
0 1
1 1
"""
) == "RIGHT", "sample 1"

# straight line
assert run(
"""0 0
1 0
2 0
"""
) == "TOWARDS", "straight movement"

# left turn with negative coordinates
assert run(
"""0 0
-1 0
-1 -1
"""
) == "LEFT", "negative coordinate orientation"

# right turn
assert run(
"""0 0
1 0
1 -1
"""
) == "RIGHT", "clockwise turn"

# large coordinates
assert run(
"""1000000000 1000000000
999999999 1000000000
999999999 999999999
"""
) == "LEFT", "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `(0,0) -> (1,0) -> (2,0)` | `TOWARDS` | Collinear movement |
| `(0,0) -> (-1,0) -> (-1,-1)` | `LEFT` | Correct orientation with negative coordinates |
| `(0,0) -> (1,0) -> (1,-1)` | `RIGHT` | Clockwise rotation |
| Large `10^9` coordinates | `LEFT` | No overflow issues |

## Edge Cases

Consider the collinear case:

```
0 0
1 0
2 0
```

The vectors are:

```
AB = (1, 0)
BC = (1, 0)
```

The cross product becomes:

```
1 * 0 - 0 * 1 = 0
```

The algorithm prints `"TOWARDS"`. Without explicitly checking for zero, an implementation could incorrectly classify this as left or right.

Now consider reversed horizontal movement:

```
0 0
-1 0
-1 -1
```

The vectors are:

```
AB = (-1, 0)
BC = (0, -1)
```

The cross product is:

```
(-1) * (-1) - 0 * 0 = 1
```

Since the result is positive, the algorithm prints `"LEFT"`. This case catches sign mistakes caused by intuition about screen coordinates or reversed vector order.

Finally, consider very large coordinates:

```
1000000000 1000000000
999999999 1000000000
999999999 999999999
```

The vectors are:

```
AB = (-1, 0)
BC = (0, -1)
```

The cross product is still computed correctly using integer arithmetic. Python handles these values safely, and the algorithm outputs `"LEFT"` without any precision issues.
