---
title: "CF 2120A - Square of Rectangles"
description: "We are given three axis-aligned rectangles. Their dimensions are already ordered so that $$l3 le l2 le l1$$ and $$b3 le b2 le b1.$$ The rectangles cannot be rotated."
date: "2026-06-08T03:52:24+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "math"]
categories: ["algorithms"]
codeforces_contest: 2120
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1033 (Div. 2) and CodeNite 2025"
rating: 800
weight: 2120
solve_time_s: 116
verified: true
draft: false
---

[CF 2120A - Square of Rectangles](https://codeforces.com/problemset/problem/2120/A)

**Rating:** 800  
**Tags:** geometry, math  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three axis-aligned rectangles. Their dimensions are already ordered so that

$$l_3 \le l_2 \le l_1$$

and

$$b_3 \le b_2 \le b_1.$$

The rectangles cannot be rotated. We must determine whether all three rectangles can be placed without overlap so that together they exactly form one square.

The dimensions are tiny, at most 100. The number of test cases is at most 100. This means we do not need sophisticated optimization. Even checking a handful of geometric configurations for every test case is effectively constant time.

The main difficulty is not performance but identifying every possible way three non-rotatable rectangles can combine into a square.

A common mistake is to check only whether the total area is a perfect square. Equal area is necessary, but it is far from sufficient.

Consider:

```
1
3 3 3 3 2 1
```

The total area is

$$9+9+2=20,$$

which is not a square, so the answer is clearly NO.

More subtle examples exist where the area is a square but the arrangement is impossible.

For example:

```
1
8 5 3 5 3 3
```

The total area is

$$40+15+9=64=8^2.$$

A careless solution might answer YES immediately. The correct answer is NO because the side lengths do not allow the rectangles to tile an $8 \times 8$ square.

Another easy-to-miss case occurs when all three rectangles must be stacked in one direction.

```
1
5 3 5 1 5 1
```

All widths are equal. Putting them one above another produces a $5 \times 5$ square, so the answer is YES. Any solution that only searches for more complicated layouts would incorrectly reject this case.

## Approaches

A brute-force mindset is a good starting point. Since there are only three rectangles, one could try to enumerate all possible relative positions on a grid and check whether the union forms a square.

Such a search would be correct because every valid arrangement would eventually be tested. The problem is that geometric placement introduces many coordinates and overlap checks. Even though the actual constraints are small, this approach is unnecessarily complicated.

The key observation is that there are only three rectangles and rotations are forbidden. Any tiling of a square by three rectangles must have a very restricted structure.

Let the square side length be $S$. First, the total area must equal $S^2$. If the area is not a perfect square, the answer is immediately NO.

Now consider the outer boundary of the square. Since only three rectangles are used, one rectangle must touch an entire side of the square. That creates only two possible top-level layouts.

The first possibility is that all three rectangles span the full width of the square and are stacked vertically, or symmetrically all span the full height and are stacked horizontally.

The second possibility is that one rectangle occupies a complete strip along one side of the square. The remaining two rectangles must then exactly fill the leftover rectangle. Since there are only two rectangles left, they can only fill that space by being stacked or placed side-by-side.

Because the dimensions are already ordered and there are only three rectangles, checking these few configurations is enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Placement Search | Large geometric enumeration | O(1) | Unnecessarily complicated |
| Optimal Geometric Case Analysis | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the total area:

$$A=l_1b_1+l_2b_2+l_3b_3.$$

1. Let

$$S=\sqrt{A}.$$

If $S^2 \ne A$, forming a square is impossible, so answer NO.

1. Check whether all three rectangles can be stacked vertically.

This requires

$$l_1=l_2=l_3=S$$

and

$$b_1+b_2+b_3=S.$$

If true, answer YES.

1. Check whether all three rectangles can be stacked horizontally.

This requires

$$b_1=b_2=b_3=S$$

and

$$l_1+l_2+l_3=S.$$

If true, answer YES.

1. Try each rectangle as the rectangle that occupies a full-width strip of the square.

Suppose rectangle $i$ has dimensions $(l,b)$.

It must satisfy

$$l=S.$$

After placing it, the remaining height is

$$H=S-b.$$

The other two rectangles must exactly fill an $S \times H$ rectangle.

Since there are only two rectangles left, they must either:

$$h_1=h_2=H,\qquad w_1+w_2=S$$

or

$$w_1=w_2=S,\qquad h_1+h_2=H.$$

If either condition holds, answer YES.

1. Symmetrically, try each rectangle as a full-height strip.

This requires

$$b=S.$$

The remaining width is

$$W=S-l.$$

The other two rectangles must exactly fill a $W \times S$ rectangle using the same two-rectangle checks.

1. If none of the above configurations work, answer NO.

### Why it works

Any tiling of a square by three axis-aligned rectangles induces a partition of the square. One rectangle must touch an entire side of the square, otherwise every side would be split among multiple rectangles and at least four rectangles would be required.

Removing that rectangle leaves a rectangular region. Since only two rectangles remain, that remaining rectangle can only be partitioned by one straight cut, either horizontal or vertical.

The algorithm checks exactly these possibilities. Every valid square tiling belongs to one of them, and every accepted configuration clearly forms a square without overlap. Hence the algorithm is both complete and correct.

## Python Solution

```python
import sys
from math import isqrt

input = sys.stdin.readline

def can_form_square(rects):
    area = sum(l * b for l, b in rects)
    s = isqrt(area)

    if s * s != area:
        return False

    # all stacked vertically
    if all(l == s for l, b in rects) and sum(b for l, b in rects) == s:
        return True

    # all stacked horizontally
    if all(b == s for l, b in rects) and sum(l for l, b in rects) == s:
        return True

    for i in range(3):
        l, b = rects[i]
        others = [rects[j] for j in range(3) if j != i]

        # full-width strip
        if l == s:
            h = s - b
            (l1, b1), (l2, b2) = others

            if b1 == h and b2 == h and l1 + l2 == s:
                return True

            if l1 == s and l2 == s and b1 + b2 == h:
                return True

        # full-height strip
        if b == s:
            w = s - l
            (l1, b1), (l2, b2) = others

            if l1 == w and l2 == w and b1 + b2 == s:
                return True

            if b1 == s and b2 == s and l1 + l2 == w:
                return True

    return False

def solve():
    t = int(input())

    ans = []

    for _ in range(t):
        l1, b1, l2, b2, l3, b3 = map(int, input().split())

        rects = [(l1, b1), (l2, b2), (l3, b3)]

        ans.append("YES" if can_form_square(rects) else "NO")

    sys.stdout.write("\n".join(ans))

solve()
```

The first section computes the total area and verifies that it is a perfect square. Without this check, impossible instances could be accepted later.

The next two checks handle the simplest layouts where every rectangle spans the entire width or the entire height of the final square.

The loop then treats each rectangle as the potential outer strip. Once that strip is fixed, only two rectangles remain. Two rectangles can partition a rectangle in only two ways, a horizontal split or a vertical split. The corresponding dimension equalities are checked directly.

The implementation never relies on floating-point square roots. Using `isqrt` avoids precision issues entirely.

## Worked Examples

### Example 1

Input:

```
5 3 5 1 5 1
```

Total area:

$$15+5+5=25.$$

Square side:

$$S=5.$$

| Step | Condition | Result |
| --- | --- | --- |
| Area perfect square | $25=5^2$ | Yes |
| Vertical stack | widths = 5, heights sum = 3+1+1=5 | Yes |
| Answer |  | YES |

This demonstrates the pure stacking configuration. Every rectangle spans the entire width of the square.

### Example 2

Input:

```
8 5 3 5 3 3
```

| Step | Value |
| --- | --- |
| Area | 64 |
| Square side | 8 |

Checking layouts:

| Check | Result |
| --- | --- |
| Vertical stack | Fail |
| Horizontal stack | Fail |
| Rectangle 1 as strip | Remaining dimensions incompatible |
| Rectangle 2 as strip | Impossible |
| Rectangle 3 as strip | Impossible |

Final answer:

```
NO
```

This example shows that area alone is not enough. Even though $64=8^2$, the side lengths do not permit a valid tiling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of geometric checks are performed |
| Space | O(1) | Uses only a few variables |

Each test case requires evaluating a constant number of formulas. With at most 100 test cases, the running time is negligible compared to the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import isqrt

def run(inp: str) -> str:
    def can_form_square(rects):
        area = sum(l * b for l, b in rects)
        s = isqrt(area)

        if s * s != area:
            return False

        if all(l == s for l, b in rects) and sum(b for l, b in rects) == s:
            return True

        if all(b == s for l, b in rects) and sum(l for l, b in rects) == s:
            return True

        for i in range(3):
            l, b = rects[i]
            others = [rects[j] for j in range(3) if j != i]

            if l == s:
                h = s - b
                (l1, b1), (l2, b2) = others

                if b1 == h and b2 == h and l1 + l2 == s:
                    return True

                if l1 == s and l2 == s and b1 + b2 == h:
                    return True

            if b == s:
                w = s - l
                (l1, b1), (l2, b2) = others

                if l1 == w and l2 == w and b1 + b2 == s:
                    return True

                if b1 == s and b2 == s and l1 + l2 == w:
                    return True

        return False

    data = inp.strip().splitlines()
    t = int(data[0])
    out = []

    for i in range(1, t + 1):
        vals = list(map(int, data[i].split()))
        rects = [(vals[0], vals[1]), (vals[2], vals[3]), (vals[4], vals[5])]
        out.append("YES" if can_form_square(rects) else "NO")

    return "\n".join(out)

# provided sample
assert run(
"""5
100 100 10 10 1 1
5 3 5 1 5 1
2 3 1 2 1 1
8 5 3 5 3 3
3 3 3 3 2 1
"""
) == """NO
YES
YES
NO
NO"""

# minimum dimensions
assert run(
"""1
1 1 1 1 1 1
"""
) == "NO"

# all equal rectangles forming a square
assert run(
"""1
2 2 2 2 2 2
"""
) == "NO"

# vertical stacking
assert run(
"""1
4 2 4 1 4 1
"""
) == "YES"

# perfect-square area but impossible layout
assert run(
"""1
8 5 3 5 3 3
"""
) == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1, 1×1, 1×1 | NO | Smallest dimensions |
| 2×2, 2×2, 2×2 | NO | Perfectly equal rectangles do not automatically work |
| 4×2, 4×1, 4×1 | YES | Pure vertical stacking |
| 8×5, 3×5, 3×3 | NO | Perfect-square area but impossible geometry |

## Edge Cases

Consider:

```
1
5 3 5 1 5 1
```

The area is $25$, so $S=5$. All rectangles have width 5 and their heights sum to 5. The algorithm accepts during the vertical-stack check and returns YES. A solution that only searches for L-shaped layouts would incorrectly reject it.

Consider:

```
1
8 5 3 5 3 3
```

The area is $64$, giving $S=8$. Every geometric configuration checked by the algorithm fails. The answer is NO even though the area is a perfect square. This prevents the common mistake of using area as the only criterion.

Consider:

```
1
2 3 1 2 1 1
```

The area is

$$6+2+1=9,$$

so $S=3$. The $2 \times 3$ rectangle occupies a full-height strip. The remaining width is 1. The other rectangles are $1 \times 2$ and $1 \times 1$, which stack vertically to fill a $1 \times 3$ region. The algorithm detects this in the full-height-strip case and returns YES.

Consider:

```
1
100 100 10 10 1 1
```

The area is

$$10101,$$

which is not a perfect square. The algorithm rejects immediately before performing any geometric checks. This handles the largest dimensions safely and efficiently.
