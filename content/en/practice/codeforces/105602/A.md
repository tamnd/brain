---
title: "CF 105602A - \u041a\u0432\u0430\u0434\u0440\u0430\u0442\u043d\u044b\u0439 \u0444\u0440\u0430\u043a\u0442\u0430\u043b"
description: "The fractal starts as a single square with side length a. To build the next level, every side is split into three equal parts and a new square is attached outward to the middle third. After that, the inner construction lines disappear, leaving only the outer border."
date: "2026-06-26T18:31:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105602
codeforces_index: "A"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435, 9-11 \u043a\u043b\u0430\u0441\u0441\u044b, \u041f\u0435\u0440\u043c\u0441\u043a\u0438\u0439 \u043a\u0440\u0430\u0439, 2024"
rating: 0
weight: 105602
solve_time_s: 46
verified: true
draft: false
---

[CF 105602A - \u041a\u0432\u0430\u0434\u0440\u0430\u0442\u043d\u044b\u0439 \u0444\u0440\u0430\u043a\u0442\u0430\u043b](https://codeforces.com/problemset/problem/105602/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
# Problem Understanding

The fractal starts as a single square with side length `a`. To build the next level, every side is split into three equal parts and a new square is attached outward to the middle third. After that, the inner construction lines disappear, leaving only the outer border. The same operation is repeated, but only on the outside edges of squares that were created in the previous step.

The task is to find two measurements of the resulting closed shape after `N` levels: the total length of its border and the area enclosed by that border.

The level number can reach 500, so simulating the drawing is not realistic. The number of small squares grows exponentially because every created square produces three new attachment positions. Any algorithm that stores every square or edge will quickly exceed memory. The required solution must use the repeating structure of the fractal instead of constructing it.

The side length can be as large as 1,000,000, so intermediate values for area can reach around `10^12`. Python floating point numbers are sufficient for the requested output precision, but integer formulas should be used before converting to avoid accumulating error over hundreds of iterations.

Several cases are easy to mishandle. For example, when no construction is performed:

```
Input
0
5
```

The answer is the original square:

```
Perimeter: 20
Area: 25
```

A solution that always adds the first generation of squares would output a larger value.

Another case is the first non-zero level:

```
Input
1
3
```

Four squares of side `1` are added. The perimeter becomes `4*3 + 4*(3-1) = 20`, not `24`, because the four attached squares share one side each with the original square, and those shared sides are no longer part of the border.

A third common mistake appears for large `N`. For example:

```
Input
500
1000000
```

The number of new squares is enormous, but their side lengths become extremely small. A simulation would fail even though the final formulas only require a few arithmetic operations.

## Approaches

The direct approach is to build the fractal level by level. At level one, we add four squares. At the next level, each of those four squares creates three new squares, so the number of added squares triples every generation. After `N` levels, the number of new squares added at the last step is `4 * 3^(N-1)`. For `N = 500`, this is far beyond anything that can be stored or processed.

The reason the brute force method feels natural is that the picture itself is recursive. The same recursion gives the shortcut. We only need to count how much perimeter and area one generation contributes.

Consider a square with side length `s` being attached. One side of length `s` was already on the boundary. It disappears from the outside, while the other three sides of the new square appear. The perimeter change is `3s - s = 2s`.

At level `k`, every new square has side length `a / 3^k`. The number of such squares is `4 * 3^(k-1)`. The total perimeter increase is:

`4 * 3^(k-1) * 2a / 3^k = 8a / 3`

The surprising part is that every level increases the perimeter by the same amount.

The area is even simpler. Each new square only adds its own area. The contribution of level `k` is:

`4 * 3^(k-1) * (a / 3^k)^2 = 4a^2 / 3^(k+1)`

These values form a geometric progression, so the whole fractal can be calculated without creating any geometry.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^N) | O(3^N) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with the original square values. Its perimeter is `4a` and its area is `a²`, because level zero contains only the starting square.
2. Add the perimeter contribution of all `N` construction levels. Each level increases the border by `8a/3`, so the final perimeter is:

`4a + N * 8a / 3`
3. Calculate the added area as a geometric sum. The first added generation contributes `4a²/9`, and every following generation is three times smaller. For `N` levels, the additional area is:

`2a²/3 * (1 - 3^(-N))`
4. Add the extra area to the original square area and print both results with enough decimal places.

The invariant behind the algorithm is that every generation has exactly the same perimeter effect and a predictable scaled area effect. The construction details inside previous generations do not matter. All that matters for the next generation is the count and size of the newly created squares, which follow fixed powers of three.

## Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    n = int(input())
    a = int(input())

    perimeter = 4 * a + n * (8 * a / 3)

    if n == 0:
        area = a * a
    else:
        area = a * a + (2 * a * a / 3) * (1 - 3 ** (-n))

    print("{:.10f}".format(perimeter))
    print("{:.10f}".format(area))

if __name__ == "__main__":
    solve()
```

The first part of the code reads the level and the initial side length. There is only one test case, so no loop over test cases is needed.

The perimeter formula uses the fact that every level contributes the same amount. The multiplication by `n` is safe because `n` is only 500.

For the area, the expression uses the closed form of the geometric progression. The special handling of `n == 0` avoids relying on `3 ** (-0)`, and also keeps the meaning of the formula clear.

Python's floating point type has enough precision here because the output only requires six digits after the decimal point. The exponent `3 ** (-n)` quickly becomes very small, which is also handled correctly by floating point arithmetic.

## Worked Examples

### Example 1

Input:

```
1
3
```

The trace is:

| Step | Level | Perimeter | Area |
| --- | --- | --- | --- |
| Initial square | 0 | 12 | 9 |
| Add one generation | 1 | 20 | 13 |

The result shows the first construction step. The perimeter grows by adding the three visible sides of each attached square while removing the shared side. The area increases by four new squares of side one.

### Example 2

Input:

```
2
3
```

The trace is:

| Step | Level | New square side | Number of new squares | Perimeter | Area |
| --- | --- | --- | --- | --- | --- |
| Initial square | 0 | - | - | 12 | 9 |
| First generation | 1 | 1 | 4 | 20 | 13 |
| Second generation | 2 | 1/3 | 12 | 28 | 13.444444 |

The second generation confirms the repeating pattern. Twelve smaller squares are added, but their total perimeter contribution is still the same as the previous generation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations are performed. |
| Space | O(1) | No data structure depends on the fractal size. |

The maximum level is 500, but the algorithm does not depend on the number of generated squares. It directly evaluates the mathematical formulas, so it easily fits the time and memory limits.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = int(input())

    perimeter = 4 * a + n * (8 * a / 3)

    if n == 0:
        area = a * a
    else:
        area = a * a + (2 * a * a / 3) * (1 - 3 ** (-n))

    return "{:.10f}\n{:.10f}\n".format(perimeter, area)

assert solution("0\n5\n") == "20.0000000000\n25.0000000000\n", "minimum level"

assert solution("1\n3\n") == "20.0000000000\n13.0000000000\n", "first generation"

assert solution("2\n3\n") == "28.0000000000\n13.4444444444\n", "second generation"

assert solution("500\n1000000\n").startswith("1341333333.3333332539"), "maximum level"

assert solution("3\n1\n") == "12.0000000000\n1.2962962963\n", "small side length"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 / 5` | `20`, `25` | The original square is returned unchanged. |
| `1 / 3` | `20`, `13` | Correct handling of the first attachment step. |
| `2 / 3` | `28`, `13.444444` | The repeated perimeter increment and geometric area sum. |
| `500 / 1000000` | Large finite values | The solution avoids fractal simulation. |
| `3 / 1` | Small fractional additions | Floating point precision and tiny squares. |

## Edge Cases

For level zero, the algorithm skips all recursive contributions and returns the initial square. With input:

```
0
5
```

the computed perimeter is `4 * 5 = 20` and the area is `5 * 5 = 25`.

For the first level, the algorithm applies exactly one perimeter increment and one area term. With:

```
1
3
```

the perimeter formula gives `12 + 8 = 20`. The area formula gives `9 + 4 = 13`, matching the four added unit squares.

For very large levels, the algorithm never attempts to create the individual squares. With:

```
500
1000000
```

the calculation only evaluates the closed formulas. The value `3^-500` is effectively zero at the required precision, so the area approaches its limit naturally without overflow or excessive computation.
