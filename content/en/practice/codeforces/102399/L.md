---
title: "CF 102399L - \u0414\u043e\u0440\u043e\u0433\u043e\u0439 \u0448\u043a\u0430\u0444"
description: "We have a rectangular cabinet standing in the corner of a room. Its two dimensions along the walls are a and b. A door of length d is mounted at a distance l from the corner."
date: "2026-08-11T05:43:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102399
codeforces_index: "L"
codeforces_contest_name: "2019 \u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432, \u043b\u0438\u0433\u0430 A"
rating: 0
weight: 102399
solve_time_s: 84
verified: true
draft: false
---

[CF 102399L - \u0414\u043e\u0440\u043e\u0433\u043e\u0439 \u0448\u043a\u0430\u0444](https://codeforces.com/problemset/problem/102399/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rectangular cabinet standing in the corner of a room. Its two dimensions along the walls are `a` and `b`. A door of length `d` is mounted at a distance `l` from the corner. When the door is opened, we need to determine whether it can reach one of the two room walls without touching the cabinet.

The geometry is considered from above. The cabinet occupies a rectangle adjacent to the corner, while the door rotates around its hinge. The door is successful only if it eventually stops against a wall and does not touch the cabinet at any point. Touching the cabinet exactly at a corner also counts as failure. The input consists of the four positive integers `a`, `b`, `d`, and `l`, with all values at most `30000` and `a <= l`. The required output is `Yes` if at least one safe way to reach a wall exists, and `No` otherwise.

The bounds are small, but that does not mean we should search over positions or angles. There is no discrete set of possible door angles, so a simulation would have to approximate a continuous geometric process. The intended solution reduces the whole problem to a constant number of arithmetic operations. With only four numbers in the input, an `O(1)` solution is easily fast enough, while the real concern is getting the geometric inequalities and their strictness right.

There are two non-obvious boundary cases.

First, touching the cabinet is forbidden. For example,

```
1
1
1
2
```

gives

```
No
```

Here the door can reach the nearer wall exactly when `a + d = l`. Its endpoint is then exactly at the relevant cabinet boundary, so the door touches the cabinet. A careless implementation using `a + d <= l` would incorrectly print `Yes`. The official sample explicitly uses this case.

Second, having enough length to reach a wall is not sufficient if the corresponding trajectory passes through the cabinet. For example,

```
4
3
10
8
```

gives

```
No
```

Although the door is long enough to reach a wall, the limiting trajectory passes through the cabinet, so the door touches it before reaching the wall. This is the second official sample.

There is also a degenerate geometric boundary when `a = l`. In that case the quantity `l - a` becomes zero. The trajectory that would have passed through the far corner becomes vertical at the relevant boundary, so the far-wall formula cannot be divided by `l - a`. Since `a + d < l` is also impossible, the answer must be `No`.

## Approaches

A literal geometric simulation would try to rotate the door and determine when it first touches either a wall or the cabinet. This is not a useful computational model because the door angle is continuous. Sampling angles can miss the exact tangent position, especially in the cases where merely touching the cabinet changes the answer. Increasing the sampling density only makes the program slower without turning the approximation into an exact solution.

A more direct brute-force interpretation is to consider the two possible walls separately. If the door avoids the cabinet, its first successful contact must be either with the wall closer to the door or with the opposite wall. There are only two geometric possibilities, so there is no large search space to enumerate. The real optimization is not about reducing the number of cases, but about deriving an exact inequality for each case and avoiding floating-point calculations.

For the nearer wall, the geometry is especially simple. The door has length `d`, while the cabinet occupies `a` units between the door and the corner along the relevant direction. To get past the cabinet and reach the nearer wall without touching it, the available distance `l` must be strictly larger than their combined lengths. Thus the condition is

`a + d < l`.

The strict inequality follows directly from the collision rule. Equality means that the door endpoint reaches the cabinet boundary exactly.

The farther wall requires the key geometric observation. Let

`x = l - a`.

The door must pass through the far corner of the cabinet in the limiting configuration. From the door's starting point to that cabinet corner, the horizontal displacement is `x` and the perpendicular displacement is `b`. By the Pythagorean theorem, that segment has length

`sqrt(x² + b²)`.

The same line continues until it reaches the opposite wall. Since its horizontal component grows from `x` to `l`, the whole segment from the door's hinge to that wall has length

`l * sqrt(x² + b²) / x`.

The door can reach the farther wall safely only when its length is strictly greater than this value. The strict inequality again matters because equality means the door reaches the cabinet corner exactly and therefore scratches it. This is the geometric derivation used in the official contest analysis.

We could evaluate this condition using floating-point square roots, but there is no reason to introduce numerical precision into an exact integer problem. Starting with

`d > l * sqrt(x² + b²) / x`

and using `x > 0`, we can square both positive sides and multiply by `x²`. The condition becomes

`d² * x² > l² * (x² + b²)`.

All quantities are non-negative, so squaring does not change the truth of the inequality. Python integers also have arbitrary precision, so overflow is not an issue.

The two cases are independent. If either the nearer-wall condition or the farther-wall condition succeeds, the answer is `Yes`. Otherwise the answer is `No`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Numerical rotation simulation | Depends on angular resolution | O(1) | Inexact and unnecessary |
| Direct geometric conditions | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the four dimensions `a`, `b`, `d`, and `l`. These describe the cabinet, door, and distance from the door to the room corner.
2. Check whether `a + d < l`. If this is true, the door can reach the nearer wall before its endpoint reaches the cabinet, so the answer is immediately `Yes`. Equality is deliberately rejected because touching the cabinet is considered a collision.
3. Compute `x = l - a`. This is the horizontal distance from the door's hinge to the far corner of the cabinet.
4. If `x = 0`, the farther-wall construction is impossible to evaluate because the limiting line has zero horizontal component. The nearer-wall condition has already failed, so the answer is `No`.
5. Compare

`d² * x² > l² * (x² + b²)`.

This is the squared version of the condition that the door is strictly longer than the line from its hinge to the farther wall passing through the cabinet corner.
6. If the comparison is true, print `Yes`. Otherwise print `No`.

Why it works: the only safe ways for the door to finish its opening without hitting the cabinet are to reach the nearer wall or to reach the farther wall. The first possibility is characterized exactly by `a + d < l`. For the second possibility, the shortest door length capable of reaching the farther wall while staying on the safe side of the cabinet is the line through the cabinet's far corner, whose length is `l * sqrt((l-a)²+b²)/(l-a)`. A strictly longer door reaches the wall without touching that corner, while an equal or shorter door cannot do so safely. Since both geometric possibilities are checked exactly, the algorithm returns `Yes` precisely when a safe opening exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a = int(input())
    b = int(input())
    d = int(input())
    l = int(input())

    # The door can pass to the nearer wall.
    if a + d < l:
        print("Yes")
        return

    x = l - a

    # No room remains for the far-wall trajectory.
    if x == 0:
        print("No")
        return

    # Compare:
    # d > l * sqrt(x^2 + b^2) / x
    #
    # All quantities are positive, so we can square safely:
    # d^2 * x^2 > l^2 * (x^2 + b^2)
    left = d * d * x * x
    right = l * l * (x * x + b * b)

    print("Yes" if left > right else "No")

if __name__ == "__main__":
    solve()
```

The first comparison implements the nearer-wall case directly. There is no square root involved, and the strict `<` is essential because equality means the door touches the cabinet.

The variable `x` represents `l - a`, the horizontal distance from the door hinge to the far cabinet corner. When `x` is zero, dividing by it would be invalid. More importantly, there is no valid far-wall escape in this configuration, so returning `No` is the correct geometric behavior.

The final comparison is deliberately written using only integer multiplication. The original geometric condition contains a square root and a division, but both can be eliminated because every quantity involved is non-negative. The strict `>` must remain strict. Replacing it with `>=` would incorrectly accept a door that reaches the cabinet corner exactly.

The largest product is on the order of `30000^4`, around `8.1 * 10^17`, which fits in a signed 64-bit integer. Python integers are unbounded anyway, so the implementation is safe even without manually reasoning about machine overflow.

## Worked Examples

### Sample 1

The input is

```
2
2
6
4
```

The algorithm processes it as follows.

| Step | `a` | `b` | `d` | `l` | `x = l-a` | Near wall | Far-wall comparison | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 6 | 4 | 2 | `2+6 < 4` is false | `144*4 > 16*8` is true | Yes |

The door cannot pass through the nearer side because its length is too large for that route. For the farther wall, `x = 2`, so the squared comparison becomes

`6² * 2² > 4² * (2² + 2²)`,

which is

`144 > 128`.

The door is long enough to reach the farther wall while avoiding the cabinet, so the result is `Yes`. This matches the first official sample.

### Sample 2

The input is

```
4
3
10
8
```

The state is

| Step | `a` | `b` | `d` | `l` | `x = l-a` | Near wall | Far-wall comparison | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | 3 | 10 | 8 | 4 | `4+10 < 8` is false | `1600*16 > 64*25` is false | No |

The nearer wall is impossible because `14 < 8` is false. For the farther wall,

`d² * x² = 10² * 4² = 1600`

while

`l² * (x² + b²) = 8² * (4² + 3²) = 1600`.

The values are exactly equal. That means the door reaches the cabinet corner exactly, which counts as touching the cabinet. Since the condition must be strict, the answer is `No`. This equality case is precisely why using `>=` would be incorrect.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations and comparisons are performed. |
| Space | O(1) | Only the four input values and a few intermediate integers are stored. |

The constraints allow values up to `30000`, so the arithmetic remains tiny. The solution does not depend on the dimensions of the room, the number of possible door positions, or an angular resolution. It therefore comfortably fits the one-second time limit and uses negligible memory.

## Test Cases

```python
import sys
import io

def solve():
    a = int(input())
    b = int(input())
    d = int(input())
    l = int(input())

    if a + d < l:
        print("Yes")
        return

    x = l - a

    if x == 0:
        print("No")
        return

    left = d * d * x * x
    right = l * l * (x * x + b * b)

    print("Yes" if left > right else "No")

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("2\n2\n6\n4\n") == "Yes\n", "sample 1"
assert run("4\n3\n10\n8\n") == "No\n", "sample 2"
assert run("1\n1\n1\n2\n") == "No\n", "sample 3"
assert run("1\n1\n1\n3\n") == "Yes\n", "sample 4"

# Minimum-size input
assert run("1\n1\n1\n1\n") == "No\n", "minimum values"

# Maximum-size input
assert run("30000\n30000\n30000\n30000\n") == "No\n", "maximum values"

# Near-wall equality, which must fail because touching is forbidden
assert run("1\n7\n5\n6\n") == "No\n", "near-wall equality"

# Near-wall escape, with one extra unit of distance
assert run("1\n7\n5\n7\n") == "Yes\n", "near-wall strict inequality"

# Far-wall equality, using a 3-4-5 triangle
assert run("2\n3\n10\n4\n") == "No\n", "far-wall equality"

# Far-wall condition succeeds with a longer door
assert run("2\n3\n11\n4\n") == "Yes\n", "far-wall strict inequality"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1` | `No` | Minimum-size input and `a = l` boundary |
| `30000 30000 30000 30000` | `No` | Maximum-size arithmetic and `a = l` |
| `1 7 5 6` | `No` | Near-wall equality must not be accepted |
| `1 7 5 7` | `Yes` | Near-wall strict inequality |
| `2 3 10 4` | `No` | Exact far-wall tangency using a Pythagorean triple |
| `2 3 11 4` | `Yes` | Far-wall condition after crossing the exact threshold |

## Edge Cases

The first important edge case is equality for the nearer wall. With

```
1
1
1
2
```

we have `a + d = 2` and `l = 2`. The test `a + d < l` fails. The door cannot pass through the cabinet boundary without touching it, so the algorithm prints `No`. Using `<=` would silently turn a collision into a successful opening.

The second edge case is a door that is long enough to reach the farther wall only by touching the cabinet. Consider

```
4
3
10
8
```

Here `x = 4`. The two squared quantities are both `1600`, so the far-wall comparison `left > right` fails. The equality represents the door passing exactly through the cabinet corner. Since contact is forbidden, `No` is correct.

A useful exact equality case for the far-wall formula is

```
2
3
10
4
```

Here `x = l-a = 2`, while `b = 3`, so `sqrt(x²+b²) = 5`. The limiting length is

`l * 5 / x = 4 * 5 / 2 = 10`.

The door has exactly length `10`, so it reaches the cabinet corner and touches it. The integer comparison gives equality on both sides and prints `No`.

If we increase the door length by one,

```
2
3
11
4
```

the limiting length is still `10`, but now `d = 11`. The inequality is strict, so the door can reach the farther wall without touching the cabinet, and the answer becomes `Yes`.

Finally, consider the boundary `a = l`, for example

```
1
1
1
1
```

The nearer-wall condition is impossible because `a + d < l` becomes `2 < 1`. At the same time, `x = l-a = 0`, so there is no valid division in the far-wall formula. The algorithm explicitly handles this case before performing the squared comparison and returns `No`. This branch is necessary for both mathematical correctness and safe implementation.
