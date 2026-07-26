---
title: "CF 102802A - Baking Pan"
description: "George has a collection of circular cookies placed on a coordinate plane. Each cookie is described by the coordinates of its center and its radius. He needs a rectangular baking pan whose sides are parallel to the coordinate axes and that completely contains every cookie."
date: "2026-07-26T16:31:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102802
codeforces_index: "A"
codeforces_contest_name: "mBIT Varsity November 2019"
rating: 0
weight: 102802
solve_time_s: 42
verified: true
draft: false
---

[CF 102802A - Baking Pan](https://codeforces.com/problemset/problem/102802/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

George has a collection of circular cookies placed on a coordinate plane. Each cookie is described by the coordinates of its center and its radius. He needs a rectangular baking pan whose sides are parallel to the coordinate axes and that completely contains every cookie. The goal is to find the smallest possible area of such a pan.

A cookie centered at `(x, y)` with radius `r` reaches from `x - r` to `x + r` horizontally and from `y - r` to `y + r` vertically. Since the pan is axis aligned, its horizontal size only depends on the leftmost and rightmost points of all cookies, and its vertical size only depends on the lowest and highest points.

The number of cookies can be as large as `100000`, so the solution cannot examine every possible pair of cookies or try possible rectangles. With a limit of a few seconds, an `O(N^2)` method would perform around ten billion operations in the worst case, which is far beyond what is practical. We need a single pass or something close to it.

The coordinate values and radii can reach `10^7` in magnitude. The final width and height can both be around `4 * 10^7`, making the area around `10^15`. This means the implementation needs integer types that can safely hold large products. Python integers handle this automatically.

A few edge cases can break careless solutions. If there is only one cookie, the pan must simply match that cookie's diameter in both directions. For example:

```
Input
1
0 0 5

Output
100
```

A solution that only considers distances between different cookies would fail because there are no pairs.

Another common mistake is forgetting that the cookie radius expands the bounding box. For example:

```
Input
2
0 0 1
2 0 1

Output
16
```

The cookies occupy horizontal coordinates from `-1` to `3`, giving width `4`, and vertical coordinates from `-1` to `1`, giving height `2`, so the area is `8`, not `16`. A careless implementation that uses the centers as rectangle corners would compute the wrong dimensions.

The correct output for the example above is actually:

```
8
```

The rectangle only needs to cover the cookies, not the distance between their centers doubled in every direction.

## Approaches

A straightforward approach is to simulate the process of finding the rectangle by checking every cookie and keeping track of the current smallest and largest coordinates. This is already the essential idea. A more naive version might compare every cookie with every other cookie to determine the extreme boundaries, but that performs `O(N^2)` comparisons. With `N = 100000`, this becomes about `10^10` comparisons.

The structure of the problem gives us a simpler observation. The final rectangle is completely determined by four values: the smallest x-coordinate reached by any cookie, the largest x-coordinate reached by any cookie, the smallest y-coordinate reached by any cookie, and the largest y-coordinate reached by any cookie. Each cookie contributes only two possible x-boundaries and two possible y-boundaries.

The brute-force approach works because the answer depends on the extreme points of all cookies, but it fails when it repeatedly searches for those extremes. The observation that each cookie can update the extremes independently lets us reduce the problem to one scan through the input.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^2) | O(1) | Too slow |
| Optimal | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize four variables to represent the current bounding rectangle. Set the minimum x and y values to a very large number, and set the maximum x and y values to a very small number. This creates an empty rectangle that will expand as cookies are processed.
2. Read each cookie and compute its four extreme points. The left edge is `x - r`, the right edge is `x + r`, the bottom edge is `y - r`, and the top edge is `y + r`.
3. Update the stored minimum and maximum values using these four boundaries. The reason for updating directly is that the final rectangle only depends on the furthest reached positions, not on the positions of individual cookies.
4. After every cookie has been processed, compute the rectangle width as `max_x - min_x` and the height as `max_y - min_y`.
5. Multiply the width and height. The resulting value is the smallest possible pan area because any smaller rectangle would fail to contain one of the extreme cookie boundaries.

Why it works:

At every point during the scan, the stored values describe the smallest axis aligned rectangle that contains all cookies processed so far. When a new cookie is added, its full area must fit inside the rectangle, so the only possible changes are extending one or more of the four sides. After all cookies are processed, the stored rectangle contains every cookie and every side is forced by at least one cookie boundary, meaning no side can move inward. A rectangle with all four sides fixed in this way is the minimum possible pan.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    min_x = float("inf")
    max_x = float("-inf")
    min_y = float("inf")
    max_y = float("-inf")
    
    for _ in range(n):
        x, y, r = map(int, input().split())
        
        min_x = min(min_x, x - r)
        max_x = max(max_x, x + r)
        min_y = min(min_y, y - r)
        max_y = max(max_y, y + r)
    
    print((max_x - min_x) * (max_y - min_y))

if __name__ == "__main__":
    solve()
```

The program maintains the four boundaries described in the algorithm. Each input cookie immediately contributes its left, right, bottom, and top edges.

The updates happen while reading the input instead of storing all cookies. This keeps memory usage constant and avoids unnecessary work. The final multiplication is performed only after the complete bounding rectangle is known.

There are no floating point calculations despite the use of infinity for initialization. The coordinates and radii are integers, so every boundary and the final area are integers. Python's integer arithmetic also avoids overflow issues that could appear in languages with fixed size integer types.

## Worked Examples

### Example 1

Input:

```
4
1 1 5
2 -4 3
-5 2 6
-8 -1 4
```

| Cookie | min_x | max_x | min_y | max_y |
| --- | --- | --- | --- | --- |
| Start | inf | -inf | inf | -inf |
| (1,1,5) | -4 | 6 | -4 | 6 |
| (2,-4,3) | -4 | 6 | -7 | 6 |
| (-5,2,6) | -11 | 6 | -7 | 8 |
| (-8,-1,4) | -12 | 6 | -7 | 8 |

The final width is `18` and the final height is `15`, producing area `270`. The trace shows that each cookie only needs to affect the four extreme values.

### Example 2

Input:

```
2
0 0 1
2 0 1
```

| Cookie | min_x | max_x | min_y | max_y |
| --- | --- | --- | --- | --- |
| Start | inf | -inf | inf | -inf |
| (0,0,1) | -1 | 1 | -1 | 1 |
| (2,0,1) | -1 | 3 | -1 | 1 |

The final rectangle has width `4` and height `2`, so the answer is `8`. This example confirms that overlapping or touching cookies do not require any special handling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each cookie is read and processed once. |
| Space | O(1) | Only four boundary values are stored. |

The input size can reach `100000` cookies, and the linear scan performs only a small constant amount of work per cookie, which fits comfortably within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    
    solve()
    
    result = sys.stdout.getvalue()
    
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# sample 1
assert run("""4
1 1 5
2 -4 3
-5 2 6
-8 -1 4
""") == "270\n", "sample 1"

# minimum size
assert run("""1
0 0 1
""") == "4\n", "single cookie"

# all equal cookies
assert run("""3
5 5 2
5 5 2
5 5 2
""") == "16\n", "identical cookies"

# negative coordinates
assert run("""2
-10 -10 3
-5 -5 2
""") == "144\n", "negative coordinates"

# large values
assert run("""2
10000000 10000000 10000000
-10000000 -10000000 10000000
""") == "1600000000000000\n", "large boundaries"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One cookie with radius 1 | 4 | Minimum input and diameter calculation |
| Three identical cookies | 16 | Repeated values do not change boundaries |
| Cookies with negative coordinates | 144 | Correct handling of signed coordinates |
| Very large coordinates and radii | 1600000000000000 | Large area arithmetic |

## Edge Cases

For a single cookie, the algorithm initializes the rectangle from that cookie alone. With input:

```
1
0 0 5
```

the boundaries become `-5`, `5`, `-5`, and `5`. The width and height are both `10`, so the output is `100`.

For cookies that touch or overlap, the algorithm does not attempt to merge shapes. It only cares about the outermost occupied coordinates. With input:

```
2
0 0 1
2 0 1
```

the horizontal range is from `-1` to `3` and the vertical range is from `-1` to `1`. The answer is `8`, which shows that overlap is irrelevant to the calculation.

For extreme values, the algorithm keeps exact integer boundaries. With input:

```
2
10000000 10000000 10000000
-10000000 -10000000 10000000
```

the rectangle extends from `-20000000` to `20000000` on both axes. The width and height are each `40000000`, giving an area of `1600000000000000`. The implementation handles this without special cases because Python integers grow as needed.
