---
title: "CF 106458F - \u0420\u0430\u0441\u0441\u0442\u043e\u044f\u043d\u0438\u0435 \u043c\u0435\u0436\u0434\u0443 \u0442\u043e\u0447\u043a\u0430\u043c\u0438"
description: "The task is to compute the straight-line distance between two points on a coordinate plane. The input describes the coordinates of two points, each represented by its x-coordinate and y-coordinate. The output is the length of the segment connecting these two points."
date: "2026-06-25T09:12:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106458
codeforces_index: "F"
codeforces_contest_name: "\u041a\u043e\u0433\u043d\u0438\u0442\u0438\u0432\u043d\u044b\u0435 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438 2023-2024. \u041f\u0435\u0440\u0432\u044b\u0439 \u043e\u0442\u0431\u043e\u0440"
rating: 0
weight: 106458
solve_time_s: 27
verified: true
draft: false
---

[CF 106458F - \u0420\u0430\u0441\u0441\u0442\u043e\u044f\u043d\u0438\u0435 \u043c\u0435\u0436\u0434\u0443 \u0442\u043e\u0447\u043a\u0430\u043c\u0438](https://codeforces.com/problemset/problem/106458/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 27s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to compute the straight-line distance between two points on a coordinate plane. The input describes the coordinates of two points, each represented by its x-coordinate and y-coordinate. The output is the length of the segment connecting these two points.

For points `(x1, y1)` and `(x2, y2)`, the horizontal difference is `x2 - x1` and the vertical difference is `y2 - y1`. These two differences form the legs of a right triangle, so the required distance is the hypotenuse:

$$\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}$$

The constraints are small, but they still determine the correct implementation details. There is no need for any search, sorting, or geometric data structure because the answer is obtained from a constant number of arithmetic operations. The main concern is numerical precision, since the result is usually not an integer.

The edge cases are simple but easy to mishandle if the formula is implemented incorrectly.

For two identical points:

```
0 0
0 0
```

the answer is:

```
0.0
```

A solution that only calculates one coordinate difference would also pass many tests but may fail on general inputs.

For points lying on a vertical line:

```
5 1
5 6
```

the answer is:

```
5.0
```

The x difference is zero, but the distance is still determined by the y difference.

For points lying diagonally:

```
0 0
3 4
```

the answer is:

```
5.0
```

A careless implementation that adds coordinate differences instead of using the Euclidean formula would output `7`, which is the Manhattan distance rather than the requested distance.

## Approaches

The brute-force approach would usually mean trying to search for some pattern or enumerate possibilities. For this problem, that instinct is unnecessary because there is only one possible distance between the two given points. Any enumeration would only repeat work that the geometry formula already solves directly.

The mathematical observation is that the coordinate differences give the sides of a right triangle. The Pythagorean theorem converts these two independent movements into the length of the diagonal segment. The problem reduces from a geometry task to evaluating a fixed formula.

The brute-force idea is not meaningful here, because even a single unnecessary loop adds complexity without providing new information. The direct calculation is constant time and is the intended solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) depending on unnecessary enumeration | O(1) | Too slow conceptually and unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the coordinates of the two points. We store the four values because the answer depends on the difference between corresponding coordinates.
2. Compute the horizontal displacement using `x2 - x1` and the vertical displacement using `y2 - y1`. The sign does not matter because both values will be squared.
3. Square both differences and add them. This gives the squared length of the segment.
4. Take the square root of the sum. The resulting value is the Euclidean distance between the points.

Why it works: the coordinate differences create a right triangle where the segment between the points is the hypotenuse. The Pythagorean theorem states that the square of the hypotenuse equals the sum of the squares of the two legs. Since the two legs are exactly the x and y differences, the computed value is always the required distance.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    x1, y1 = map(float, input().split())
    x2, y2 = map(float, input().split())

    dx = x2 - x1
    dy = y2 - y1

    ans = math.sqrt(dx * dx + dy * dy)

    print(ans)

if __name__ == "__main__":
    solve()
```

The program first reads both points. The coordinates are stored as floating point values because the final distance may contain a fractional part.

The variables `dx` and `dy` represent the two sides of the right triangle formed by the points. Squaring them removes any negative sign, so the order of the two points does not affect the answer.

The expression `math.sqrt(dx * dx + dy * dy)` directly follows the mathematical formula. Python floating point numbers are sufficient for the precision required by this problem.

## Worked Examples

### Example 1

Input:

```
0 0
3 4
```

| Step | x1 | y1 | x2 | y2 | dx | dy | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Read points | 0 | 0 | 3 | 4 | - | - | - |
| Calculate differences | 0 | 0 | 3 | 4 | 3 | 4 | - |
| Apply formula | 0 | 0 | 3 | 4 | 3 | 4 | sqrt(9 + 16) = 5 |

The example demonstrates the standard 3-4-5 triangle. The algorithm only needs the two coordinate differences to recover the distance.

### Example 2

Input:

```
5 1
5 6
```

| Step | x1 | y1 | x2 | y2 | dx | dy | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Read points | 5 | 1 | 5 | 6 | - | - | - |
| Calculate differences | 5 | 1 | 5 | 6 | 0 | 5 | - |
| Apply formula | 5 | 1 | 5 | 6 | 0 | 5 | sqrt(0 + 25) = 5 |

This trace checks the vertical-line case where one coordinate difference disappears completely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The solution performs a fixed number of arithmetic operations. |
| Space | O(1) | Only a few variables are stored. |

The algorithm does not depend on the size of the coordinates or any hidden iteration. It easily fits any reasonable time and memory limits.

## Test Cases

```python
import sys
import io
import math

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    import math
    x1, y1 = map(float, sys.stdin.readline().split())
    x2, y2 = map(float, sys.stdin.readline().split())

    ans = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    result = str(ans)

    sys.stdin = old_stdin
    return result

# provided-style samples
assert solution("0 0\n3 4\n") == "5.0", "sample 1"
assert solution("1 1\n1 1\n") == "0.0", "sample 2"

# custom cases
assert solution("5 1\n5 6\n") == "5.0", "vertical line"
assert solution("-1 -1\n2 3\n") == "5.0", "negative coordinates"
assert solution("1000000 1000000\n1000000 999999\n") == "1.0", "large boundary values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` and `3 4` | `5.0` | Basic diagonal distance |
| `1 1` and `1 1` | `0.0` | Same point handling |
| `5 1` and `5 6` | `5.0` | Zero horizontal difference |
| `-1 -1` and `2 3` | `5.0` | Negative coordinates |
| `1000000 1000000` and `1000000 999999` | `1.0` | Large coordinate values |

## Edge Cases

For identical points:

```
0 0
0 0
```

the algorithm computes `dx = 0` and `dy = 0`. The formula becomes `sqrt(0 + 0)`, producing `0.0`. There is no special handling required because the general formula already covers this case.

For a vertical segment:

```
5 1
5 6
```

the algorithm computes `dx = 0` and `dy = 5`. The squared distance is `25`, so the answer is `sqrt(25) = 5.0`. A solution that divides by one coordinate difference or assumes both coordinates change would fail here.

For a diagonal segment:

```
0 0
3 4
```

the algorithm computes `dx = 3` and `dy = 4`. The squared distance is `9 + 16 = 25`, giving an answer of `5.0`. This confirms that the solution uses Euclidean distance rather than simply adding coordinate changes.
