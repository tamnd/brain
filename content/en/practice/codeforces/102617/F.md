---
title: "CF 102617F - Baking Pan"
description: "The problem describes a set of circular cookies that must fit inside a rectangular baking pan. Each cookie has a center on a coordinate plane and a radius."
date: "2026-08-01T07:11:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102617
codeforces_index: "F"
codeforces_contest_name: "mBIT Rookie November 2019"
rating: 0
weight: 102617
solve_time_s: 57
verified: true
draft: false
---

[CF 102617F - Baking Pan](https://codeforces.com/problemset/problem/102617/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a set of circular cookies that must fit inside a rectangular baking pan. Each cookie has a center on a coordinate plane and a radius. The pan must have sides parallel to the coordinate axes, and we need the smallest possible area of a rectangle that contains every cookie completely.

A cookie with center `(x, y)` and radius `r` reaches `r` units left, right, up, and down from its center. That means the smallest rectangle containing one cookie has horizontal range `[x - r, x + r]` and vertical range `[y - r, y + r]`. The answer is the area of the rectangle covering all these individual ranges.

The input size can reach `100000` cookies, so the algorithm must process each cookie a constant number of times. A quadratic approach that compares every pair of cookies would perform about `10^10` operations in the largest case, which is far beyond what a normal contest time limit allows. The constraints point toward a linear scan.

The main edge cases come from forgetting that the pan must contain the entire cookie, not only its center. A single cookie can already determine the answer. For example:

```
1
0 0 5
```

The correct output is:

```
100
```

The pan must have width `10` and height `10`. An approach that only tracks the center would incorrectly return area `0`.

Another common mistake is handling negative coordinates incorrectly. Consider:

```
2
-10 -5 2
4 3 1
```

The horizontal limits are `[-12, -8]` and `[3, 5]`, so the total width is `17`. The vertical limits are `[-7, -3]` and `[2, 4]`, so the height is `11`. The correct output is:

```
187
```

A careless implementation using only positive values or applying absolute values to coordinates can lose the true minimum and maximum positions.

A final boundary case is when all cookies overlap:

```
3
0 0 1
0 0 1
0 0 1
```

The correct output is:

```
4
```

The pan does not need to grow for repeated cookies. Only the extreme borders matter.

## Approaches

The brute-force idea would be to try possible rectangles and check whether every cookie fits inside each one. This is correct because eventually the optimal rectangle would be considered, but there is no useful way to enumerate all possible rectangles. The number of possible coordinates grows with the input values, making this approach impossible even for a moderate number of cookies.

A more natural brute-force interpretation is to find the leftmost, rightmost, lowest, and highest cookie boundaries by repeatedly comparing every cookie against every other cookie. That approach works because the answer depends only on the extreme values. However, if there are `n` cookies and we repeatedly search for the extremes, the work becomes `O(n^2)`, which means about `10^10` comparisons for `n = 100000`.

The key observation is that the final rectangle is completely determined by four numbers. The left side is the smallest value of `x - r`, the right side is the largest value of `x + r`, the bottom side is the smallest value of `y - r`, and the top side is the largest value of `y + r`. Each cookie can update these four values independently.

The brute-force method works because it eventually finds these four boundaries, but it repeats the same comparisons many times. The observation that every cookie contributes only four candidate borders lets us replace repeated searching with a single pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize four variables representing the current pan boundaries. The left and bottom boundaries start at positive infinity because we are searching for smaller values. The right and top boundaries start at negative infinity because we are searching for larger values.
2. Read each cookie and calculate its four extreme coordinates: `x - r`, `x + r`, `y - r`, and `y + r`. These are the only values that can affect the final pan.
3. Update the current boundaries using these four values. The smallest left edge and bottom edge become the new lower limits, while the largest right edge and top edge become the new upper limits.
4. After all cookies are processed, calculate the width as `right - left` and the height as `top - bottom`. Their product is the smallest possible pan area.

Why it works: after processing any prefix of the cookies, the stored four boundaries exactly describe the smallest rectangle containing all cookies seen so far. When a new cookie is added, the only possible change is that it extends one of these four sides. Since every cookie is processed and all possible extensions are considered, the final boundaries contain every cookie and cannot be reduced further.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    left = float('inf')
    right = -float('inf')
    bottom = float('inf')
    top = -float('inf')
    
    for _ in range(n):
        x, y, r = map(int, input().split())
        
        left = min(left, x - r)
        right = max(right, x + r)
        bottom = min(bottom, y - r)
        top = max(top, y + r)
    
    width = right - left
    height = top - bottom
    
    print(width * height)

if __name__ == "__main__":
    solve()
```

The code keeps only the four borders of the current answer. The values `x - r` and `x + r` describe the left and right points of a cookie, while `y - r` and `y + r` describe the bottom and top points.

Using `float('inf')` and negative infinity avoids needing special handling for the first cookie. Every input value is then processed through the same update logic.

Python integers have arbitrary precision, so the final multiplication does not require special overflow handling. The width and height calculations must be done after all updates, because the area depends on the complete set of cookies rather than any individual cookie.

## Worked Examples

Consider:

```
4
1 1 5
2 -4 3
-5 2 6
-8 -1 4
```

The trace is:

| Cookie | Left | Right | Bottom | Top |
| --- | --- | --- | --- | --- |
| Start | inf | -inf | inf | -inf |
| (1, 1, 5) | -4 | 6 | -4 | 6 |
| (2, -4, 3) | -4 | 6 | -7 | 6 |
| (-5, 2, 6) | -11 | 6 | -7 | 8 |
| (-8, -1, 4) | -12 | 6 | -7 | 8 |

The final width is `18` and the final height is `15`, giving area `270`. This example demonstrates how different cookies can determine different sides of the pan.

A single cookie case:

```
1
0 0 5
```

| Cookie | Left | Right | Bottom | Top |
| --- | --- | --- | --- | --- |
| Start | inf | -inf | inf | -inf |
| (0, 0, 5) | -5 | 5 | -5 | 5 |

The width and height are both `10`, so the answer is `100`. This confirms that the algorithm handles the smallest possible input without any special case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each cookie updates four boundaries once. |
| Space | O(1) | Only four boundary variables are stored. |

The algorithm scales directly with the number of cookies. For `100000` cookies, it performs only a few hundred thousand arithmetic operations, which easily fits typical contest limits.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    data = inp.strip().split()
    if not data:
        return ""
    
    it = iter(data)
    n = int(next(it))
    
    left = float('inf')
    right = -float('inf')
    bottom = float('inf')
    top = -float('inf')
    
    for _ in range(n):
        x = int(next(it))
        y = int(next(it))
        r = int(next(it))
        left = min(left, x - r)
        right = max(right, x + r)
        bottom = min(bottom, y - r)
        top = max(top, y + r)
    
    return str((right - left) * (top - bottom))

assert solution("""4
1 1 5
2 -4 3
-5 2 6
-8 -1 4
""") == "270", "sample"

assert solution("""1
0 0 5
""") == "100", "single cookie"

assert solution("""3
0 0 1
0 0 1
0 0 1
""") == "4", "all equal cookies"

assert solution("""2
-10 -5 2
4 3 1
""") == "187", "negative coordinates"

assert solution("""2
10000000 10000000 10000000
-10000000 -10000000 10000000
""") == "1600000000000000", "large coordinates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One cookie with radius 5 | 100 | The rectangle must include the whole cookie. |
| Three identical cookies | 4 | Repeated cookies do not change the borders. |
| Cookies with negative coordinates | 187 | Correct handling of minimum and maximum values. |
| Very large coordinates and radii | 1600000000000000 | Large arithmetic values and overflow safety. |

## Edge Cases

For the single-cookie case:

```
1
0 0 5
```

the algorithm starts with empty boundaries. The only cookie changes all four sides to `-5` and `5`. The resulting rectangle has area `100`, which is the smallest possible pan.

For negative coordinates:

```
2
-10 -5 2
4 3 1
```

the first cookie contributes left edge `-12` and bottom edge `-7`. The second cookie contributes right edge `5` and top edge `4`. The final rectangle is `17` units wide and `11` units tall, so the answer is `187`. The algorithm does not treat negative positions specially, because comparisons naturally handle them.

For overlapping cookies:

```
3
0 0 1
0 0 1
0 0 1
```

every cookie produces the same borders. The minimum and maximum operations leave the rectangle unchanged after the first cookie, giving the correct answer of `4`. This shows why the solution depends on extremes rather than the number of cookies.
