---
title: "CF 165A - Supercentral Point"
description: "We are given a set of points on a 2D Cartesian plane. A point is called supercentral if there exists at least one other point directly to its left, one directly to its right, one directly above it, and one directly below it."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 165
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 112 (Div. 2)"
rating: 1000
weight: 165
solve_time_s: 112
verified: false
draft: false
---

[CF 165A - Supercentral Point](https://codeforces.com/problemset/problem/165/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of points on a 2D Cartesian plane. A point is called supercentral if there exists at least one other point directly to its left, one directly to its right, one directly above it, and one directly below it.

The key detail is that these neighbors must share either the same x-coordinate or the same y-coordinate. A point on the left or right must stay on the same horizontal line, while a point above or below must stay on the same vertical line.

For every point, we must check whether all four directions are represented somewhere in the set. The answer is simply the number of points that satisfy this condition.

The constraints are very small. The number of points is at most 200, which means even an algorithm with roughly 40,000 pair comparisons is completely safe. A quadratic solution is fast enough within the 2 second limit.

The main danger in this problem is misunderstanding what qualifies as a neighbor. The point does not need to be the closest point in that direction. Any point satisfying the directional condition is enough.

Consider this example:

```
5
0 0
2 0
5 0
0 2
0 -2
```

Point `(0,0)` has a right neighbor because both `(2,0)` and `(5,0)` are to its right on the same horizontal line. We only care that at least one exists.

Another common mistake is forgetting that all four directions are required simultaneously.

Example:

```
4
0 0
1 0
-1 0
0 1
```

The correct answer is:

```
0
```

Point `(0,0)` has left, right, and upper neighbors, but no lower neighbor, so it is not supercentral.

A careless implementation might also accidentally count diagonal points.

Example:

```
5
0 0
1 1
-1 1
1 -1
-1 -1
```

The correct answer is:

```
0
```

None of these points share the same x-coordinate or y-coordinate with `(0,0)`, so none of them qualify as directional neighbors.

## Approaches

The most direct idea is to process each point independently and search through all other points to see whether the four required directions exist.

Suppose we are currently examining point `(x,y)`. We iterate over every other point `(nx,ny)` and check four conditions:

- `nx < x and ny == y` means we found a left neighbor.
- `nx > x and ny == y` means we found a right neighbor.
- `nx == x and ny < y` means we found a lower neighbor.
- `nx == x and ny > y` means we found an upper neighbor.

Once all four conditions become true, the point is supercentral.

This brute-force strategy is already fast enough because `n ≤ 200`. In the worst case, we compare every pair of points once, giving about `200 × 200 = 40,000` comparisons. That is tiny.

There is no need for advanced data structures or geometry tricks because the constraints are intentionally small. The problem is mainly about implementing the directional checks correctly.

The useful observation is that the property of being supercentral depends only on the existence of points in four directions. We do not care about distances or nearest neighbors. That means a simple scan over all points is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n²) | O(1) | Accepted |

In this problem, the brute-force approach is already optimal enough for the given limits.

## Algorithm Walkthrough

1. Read all points into a list.
2. Initialize a counter `answer = 0`.
3. For each point `(x,y)` in the list, create four boolean variables:

`left`, `right`, `up`, and `down`.
4. Scan through every other point `(nx,ny)`.
5. If `ny == y` and `nx < x`, mark `left = True`.
6. If `ny == y` and `nx > x`, mark `right = True`.
7. If `nx == x` and `ny < y`, mark `down = True`.
8. If `nx == x` and `ny > y`, mark `up = True`.
9. After checking all points, if all four booleans are true, increment the answer.
10. Print the final answer.

Why it works:

For every point, the algorithm explicitly checks whether at least one point exists in each required direction. The conditions exactly match the definition of supercentral points. Since every other point is examined, no valid neighbor can be missed. A point is counted only when all four directional requirements are satisfied simultaneously.

## Python Solution

```python
import sys
input = sys.stdin.readline

# solution

def solve():
    n = int(input())
    points = [tuple(map(int, input().split())) for _ in range(n)]

    answer = 0

    for x, y in points:
        left = False
        right = False
        up = False
        down = False

        for nx, ny in points:
            if ny == y:
                if nx < x:
                    left = True
                elif nx > x:
                    right = True

            if nx == x:
                if ny < y:
                    down = True
                elif ny > y:
                    up = True

        if left and right and up and down:
            answer += 1

    print(answer)

solve()
```

The solution follows the algorithm directly.

The outer loop selects the current point we want to test. The inner loop searches for neighbors in the four directions.

The implementation separates horizontal and vertical checks because the definitions are different. Horizontal neighbors require equal `y` values, while vertical neighbors require equal `x` values.

Using boolean flags is the cleanest approach because we only care whether a neighbor exists, not how many exist.

The `elif` statements avoid unnecessary checks once we already know whether a point lies on one side. Since all coordinates are distinct, a point cannot simultaneously be both left and right of the current point.

There are no overflow concerns because coordinates are small integers. The only subtle part is remembering that diagonal points do not count unless one coordinate matches exactly.

## Worked Examples

### Sample 1

Input:

```
8
1 1
4 2
3 1
1 2
0 2
0 1
1 0
1 3
```

### Trace for point `(1,1)`

| Compared Point | Left | Right | Up | Down |
| --- | --- | --- | --- | --- |
| (4,2) | False | False | False | False |
| (3,1) | False | True | False | False |
| (1,2) | False | True | True | False |
| (0,2) | False | True | True | False |
| (0,1) | True | True | True | False |
| (1,0) | True | True | True | True |
| (1,3) | True | True | True | True |

All four directions exist, so `(1,1)` is supercentral.

### Trace for point `(1,2)`

| Compared Point | Left | Right | Up | Down |
| --- | --- | --- | --- | --- |
| (1,1) | False | False | False | True |
| (4,2) | False | True | False | True |
| (3,1) | False | True | False | True |
| (0,2) | True | True | False | True |
| (0,1) | True | True | False | True |
| (1,0) | True | True | False | True |
| (1,3) | True | True | True | True |

This point is also supercentral.

The final answer is:

```
2
```

These traces show that neighbors do not need to be adjacent. Any valid point in the required direction is enough.

### Second Example

Input:

```
5
0 0
1 0
-1 0
0 1
0 -1
```

### Trace for point `(0,0)`

| Compared Point | Left | Right | Up | Down |
| --- | --- | --- | --- | --- |
| (1,0) | False | True | False | False |
| (-1,0) | True | True | False | False |
| (0,1) | True | True | True | False |
| (0,-1) | True | True | True | True |

The point satisfies all four conditions, so the answer is:

```
1
```

This example demonstrates the simplest possible supercentral configuration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Every point is compared with every other point |
| Space | O(1) | Only a few boolean variables are used beyond the input list |

With at most 200 points, the quadratic scan performs only about 40,000 comparisons. This easily fits within the time limit. Memory usage is minimal.

## Test Cases

```python
# helper: run solution on input string, return output string

import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    points = [tuple(map(int, input().split())) for _ in range(n)]

    answer = 0

    for x, y in points:
        left = right = up = down = False

        for nx, ny in points:
            if ny == y:
                if nx < x:
                    left = True
                elif nx > x:
                    right = True

            if nx == x:
                if ny < y:
                    down = True
                elif ny > y:
                    up = True

        if left and right and up and down:
            answer += 1

    print(answer)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
assert run(
"""8
1 1
4 2
3 1
1 2
0 2
0 1
1 0
1 3
"""
) == "2", "sample 1"

# minimum size
assert run(
"""1
0 0
"""
) == "0", "single point cannot be supercentral"

# simple cross
assert run(
"""5
0 0
1 0
-1 0
0 1
0 -1
"""
) == "1", "center point is supercentral"

# diagonal points only
assert run(
"""5
0 0
1 1
-1 1
1 -1
-1 -1
"""
) == "0", "diagonal points do not count"

# multiple horizontal points but missing vertical
assert run(
"""4
0 0
1 0
2 0
-1 0
"""
) == "0", "missing upper and lower neighbors"

print("All tests passed!")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single point | 0 | Minimum-size input |
| Cross centered at origin | 1 | Basic valid supercentral point |
| Diagonal-only configuration | 0 | Diagonal neighbors must not count |
| Horizontal line only | 0 | All four directions are required |

## Edge Cases

Consider a point that has neighbors in only three directions.

Input:

```
4
0 0
1 0
-1 0
0 1
```

During the scan for `(0,0)`, the algorithm sets:

- `left = True`
- `right = True`
- `up = True`

But `down` remains false because no point has the same x-coordinate and a smaller y-coordinate. Since all four booleans are required, the point is not counted. The final answer is `0`.

Now consider diagonal points.

Input:

```
5
0 0
1 1
-1 1
1 -1
-1 -1
```

When checking `(0,0)`, every other point fails both equality checks:

- `ny == y` is never true.
- `nx == x` is never true.

All four direction flags remain false, so the algorithm correctly outputs `0`.

Finally, consider multiple neighbors on the same side.

Input:

```
6
0 0
1 0
2 0
3 0
0 1
0 -1
```

The algorithm marks `right = True` as soon as it encounters `(1,0)`. The additional points `(2,0)` and `(3,0)` do not change anything. Since there is still no left neighbor, the point is not counted. The final answer is `0`.

This confirms that the algorithm only checks existence, exactly matching the problem definition.
