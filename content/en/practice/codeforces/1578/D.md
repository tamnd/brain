---
title: "CF 1578D - Dragon Curve"
description: "Every unit square with integer corners is crossed by exactly one segment of one of four infinite dragon curves. For a query square with opposite corners $(x,y)$ and $(x+1,y+1)$, we must determine two things."
date: "2026-06-10T10:35:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 1578
codeforces_index: "D"
codeforces_contest_name: "ICPC WF Moscow Invitational Contest - Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 3200
weight: 1578
solve_time_s: 130
verified: false
draft: false
---

[CF 1578D - Dragon Curve](https://codeforces.com/problemset/problem/1578/D)

**Rating:** 3200  
**Tags:** -  
**Solve time:** 2m 10s  
**Verified:** no  

## Solution
## Problem Understanding

Every unit square with integer corners is crossed by exactly one segment of one of four infinite dragon curves. For a query square with opposite corners $(x,y)$ and $(x+1,y+1)$, we must determine two things.

The first is which of the four curves contains the segment crossing that square.

The second is the index of that segment along the curve, where the first segment of each curve has index $1$.

The coordinates are as large as $10^9$, and there are up to $2 \cdot 10^5$ queries. Any approach that explicitly generates the curve is hopeless. Even generating a finite dragon curve large enough to reach coordinates of that magnitude would require exponentially many segments. We need a logarithmic solution per query.

The difficult part is that the dragon curve is self-similar. A square very far from the origin still belongs to a structure that recursively looks like a smaller dragon curve. The intended solution repeatedly maps a query square from one scale of the fractal to the next smaller scale until it reaches the origin. Each step divides coordinates roughly by two, so only about 31 iterations are needed for coordinates up to $10^9$.

A common mistake is to assume that after scaling down, the segment order is preserved. Sometimes it is, but sometimes the order inside the corresponding larger segment is reversed. For example, two adjacent squares that belong to the same large-scale segment may appear in opposite order after one recursive reduction. The solution must explicitly track these reversals.

Another subtle case is handling negative coordinates. The recursive coordinate transform relies on arithmetic shifts and carefully chosen formulas. Replacing them with naive division can break the mapping for squares in the negative quadrants.

## Approaches

A brute-force approach would generate the dragon curve segment by segment until the target square is reached. This is conceptually straightforward because every segment crosses exactly one square. Unfortunately, the number of segments grows exponentially with the order of the curve. Coordinates near $10^9$ correspond to recursion depths around 30, which already implies billions of segments. The approach is completely infeasible.

The key observation is self-similarity.

Consider two versions of the dragon curve. Call the original one order $n+1$, and another one obtained by rotating it by $45^\circ$ counterclockwise and scaling by $1/\sqrt2$, order $n$. Every segment of the smaller curve expands into exactly two segments of the larger curve. This gives a direct recursive relationship between squares in the plane and squares at the next smaller scale.

The plane can be partitioned into $2 \times 2$ blocks. Depending on parity, such a block is either "vertical" or "horizontal". From the block type, we can derive a deterministic transformation that maps the current square to the corresponding square in the smaller dragon curve. Repeating this operation keeps shrinking the coordinates.

While shrinking, we also maintain the position of the segment inside the recursively expanded segment. Each reduction doubles the represented segment length. Sometimes the local ordering is reversed, so we replace

$$pos \leftarrow (2^k-1)-pos.$$

When the square finally becomes one of the four squares adjacent to the origin, the curve number is immediately known, and the accumulated position becomes the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal Recursive Reduction | (O(\log(\max( | x | , |

## Algorithm Walkthrough

1. Start with the queried square coordinates $(x,y)$.
2. Maintain two values:

`bit`, the number of original segments represented by the current recursive segment.

`pos`, the position inside that segment, initially zero.
3. While the square is not one of the four squares adjacent to the origin, perform one recursive reduction.
4. Double `bit` because one segment of the smaller curve corresponds to two segments of the larger curve. After $k$ reductions, the represented segment length is $2^k$.
5. Check whether this reduction reverses the local ordering. The required condition is

```
(x ^ y ^ ((x ^ y) >> 1)) & 1
```

If it is true, replace

```
pos = bit - 1 - pos
```

This mirrors the position inside the current segment.
6. Determine whether the current $2 \times 2$ block is horizontal or vertical.

If

```
((x ^ y) >> 1) & 1
```

is true, use the horizontal transformation:

```
x, y =
    (x >> 1) + ((y + 1) >> 1),
    ((y + 1) >> 1) - (x >> 1) - 1
```

Otherwise use the vertical transformation:

```
x, y =
    ((x + 1) >> 1) + (y >> 1),
    (y >> 1) - ((x + 1) >> 1)
```

These formulas map the square to the corresponding square in the next smaller dragon curve.
7. Continue until $(x,y)$ belongs to the $2 \times 2$ neighborhood around the origin, namely

```
-1 <= x <= 0 and -1 <= y <= 0
```
8. Determine the curve number from the final coordinates:

```
curve = (x & 1 ^ y & 3) + 1
```
9. The segment index is `pos + 1` because the output is 1-based.

### Why it works

Each reduction maps the queried square from one scale of the dragon curve to the next smaller scale. The geometric structure of the dragon curve guarantees that every square corresponds to exactly one square in the reduced representation. The coordinate transform preserves that correspondence. At the same time, `bit` records how many original segments have been merged into the current recursive segment, and `pos` records which of those segments contains the query. Whenever the recursive construction reverses orientation, the mirror transformation updates `pos` accordingly. After enough reductions, the query reaches one of the four base segments adjacent to the origin. At that point both the curve identity and the exact segment position are uniquely determined.

## Python Solution

```python
import sys
input = sys.stdin.readline

def dragon_curve(x, y):
    bit = 1
    pos = 0

    while not (-1 <= x <= 0 and -1 <= y <= 0):
        bit <<= 1

        if (x ^ y ^ ((x ^ y) >> 1)) & 1:
            pos = bit - 1 - pos

        if ((x ^ y) >> 1) & 1:
            x, y = (
                (x >> 1) + ((y + 1) >> 1),
                ((y + 1) >> 1) - (x >> 1) - 1
            )
        else:
            x, y = (
                ((x + 1) >> 1) + (y >> 1),
                (y >> 1) - ((x + 1) >> 1)
            )

    curve = ((x & 1) ^ (y & 3)) + 1
    return curve, pos + 1

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        x, y = map(int, input().split())
        c, p = dragon_curve(x, y)
        ans.append(f"{c} {p}")

    sys.stdout.write("\n".join(ans))

solve()
```

The implementation follows the recursive reduction literally.

The loop is the heart of the solution. Each iteration shrinks coordinates roughly by a factor of two, so even the largest coordinates require only about thirty iterations.

The variable `bit` always equals the length of the current recursive segment measured in original segments. This is why it doubles before processing the current reduction.

The reversal update is easy to get wrong. The formula uses the new value of `bit`, not the old one. If the order flips inside a segment of length $L$, position $p$ becomes $L-1-p$.

The coordinate transforms must use arithmetic right shifts exactly as shown. Python's shifts work correctly for negative integers, matching the intended behavior.

## Worked Examples

### Example 1

Input square:

```
(0, 0)
```

| x | y | bit | pos |
| --- | --- | --- | --- |
| 0 | 0 | 1 | 0 |

The square is already adjacent to the origin, so the loop never runs.

Final values:

| curve | position |
| --- | --- |
| 1 | 1 |

Output:

```
1 1
```

This example shows the base case of the recursion.

### Example 2

Input square:

```
(-2, 0)
```

| Iteration | x | y | bit | pos |
| --- | --- | --- | --- | --- |
| Start | -2 | 0 | 1 | 0 |
| After reduction | -1 | -1 | 2 | 1 |

The loop stops because $(-1,-1)$ is adjacent to the origin.

Final values:

| curve | position |
| --- | --- |
| 2 | 2 |

Output:

```
2 2
```

This example demonstrates a position reversal. The final position becomes the second segment rather than the first.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\log(\max( | x |
| Space | $O(1)$ | Only a few integer variables are stored |

With coordinates bounded by $10^9$, each query performs at most about 31 recursive reductions. For $2 \cdot 10^5$ queries, the total work is only a few million simple integer operations, comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_io(inp: str) -> str:
    data = io.StringIO(inp)
    out = io.StringIO()

    input = data.readline

    def dragon_curve(x, y):
        bit = 1
        pos = 0

        while not (-1 <= x <= 0 and -1 <= y <= 0):
            bit <<= 1

            if (x ^ y ^ ((x ^ y) >> 1)) & 1:
                pos = bit - 1 - pos

            if ((x ^ y) >> 1) & 1:
                x, y = (
                    (x >> 1) + ((y + 1) >> 1),
                    ((y + 1) >> 1) - (x >> 1) - 1
                )
            else:
                x, y = (
                    ((x + 1) >> 1) + (y >> 1),
                    (y >> 1) - ((x + 1) >> 1)
                )

        return ((x & 1) ^ (y & 3)) + 1, pos + 1

    t = int(input())
    for _ in range(t):
        x, y = map(int, input().split())
        c, p = dragon_curve(x, y)
        out.write(f"{c} {p}\n")

    return out.getvalue()

# provided sample
assert solve_io(
"""5
0 0
-2 0
-7 -7
5 -9
9 9
"""
) == (
"""1 1
2 2
3 189
4 186
2 68
"""
)

# base squares around origin
assert solve_io(
"""4
0 0
-1 0
-1 -1
0 -1
"""
) == (
"""1 1
2 1
3 1
4 1
"""
)

# negative coordinate handling
assert solve_io(
"""1
-2 0
"""
) == (
"""2 2
"""
)

# large coordinate stress
solve_io(
"""1
1000000000 1000000000
"""
)

# mixed quadrants
solve_io(
"""4
10 -7
-10 7
-10 -7
7 10
"""
)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `(0,0)` | `1 1` | Base case |
| `(-1,0)` | `2 1` | Curve identification near origin |
| `(-1,-1)` | `3 1` | Third base curve |
| `(0,-1)` | `4 1` | Fourth base curve |
| `(-2,0)` | `2 2` | Position reversal logic |
| Large coordinates | Valid answer | Logarithmic depth |

## Edge Cases

Consider the square at `(0,0)`.

The loop condition immediately fails because the square already belongs to the base neighborhood. No recursive reduction is needed. The algorithm directly computes curve `1` and position `1`. A solution that always performs at least one reduction would incorrectly move away from the base configuration.

Consider the square at `(-2,0)`.

The first reduction doubles `bit` from `1` to `2`. The parity test indicates that the local ordering is reversed, so `pos` changes from `0` to `1`. After the coordinate transform the square becomes `(-1,-1)`, which is a base square. The final answer is `2 2`. Any implementation that ignores reversals would return position `1`, which is wrong.

Consider a large negative coordinate such as `(-10^9,-10^9)`.

The recursive formulas repeatedly apply arithmetic shifts to negative values. Python preserves sign during right shifts, matching the intended geometric reduction. Replacing `>> 1` with ordinary division and truncation toward zero would produce different intermediate coordinates and eventually the wrong curve. The algorithm avoids this problem by using the exact transforms derived from the fractal structure.
