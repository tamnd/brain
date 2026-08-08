---
title: "CF 102503F - Ulam Spiral"
description: "The grid contains positive integers arranged in a square spiral around 1. The coordinates are centered at 1, with the first coordinate increasing upward and the second increasing to the right. Thus 2 is at (0,1), 3 at (1,1), 4 at (1,0), and so on."
date: "2026-08-09T05:40:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102503
codeforces_index: "F"
codeforces_contest_name: "National Olympiad in Informatics - Philippines (NOI.PH) Online Eliminations 2020"
rating: 0
weight: 102503
solve_time_s: 515
verified: true
draft: false
---

[CF 102503F - Ulam Spiral](https://codeforces.com/problemset/problem/102503/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

The grid contains positive integers arranged in a square spiral around `1`. The coordinates are centered at `1`, with the first coordinate increasing upward and the second increasing to the right. Thus `2` is at `(0,1)`, `3` at `(1,1)`, `4` at `(1,0)`, and so on.

For each test case, we are given two ulam numbers `i` and `j`. We locate both numbers in the infinite spiral, take the smallest axis-aligned rectangle containing their two cells, and sum the values of every ulam inside that rectangle. The required answer is this sum modulo `10^9 + 7`. The official statement confirms that there can be up to `20,000` test cases and that each number can be as large as `10^18`.

The bound of `10^18` immediately rules out constructing the spiral up to either input value. A number around `10^18` lies roughly `5 * 10^8` cells away from the center, so even a single large rectangle can contain on the order of `10^18` cells. A solution that visits cells individually is not remotely feasible. With `20,000` test cases, the intended solution needs essentially constant or logarithmic work per case.

There are several boundary cases that are easy to mishandle. When the two inputs are equal, the rectangle is one cell. For example, input `1 1` has answer `1`, not `0` or the size of a surrounding ring. A careless implementation that assumes two distinct coordinates can get this wrong.

Another common mistake is counting a spiral corner twice when summing its four sides. For example, `13` and `25` are both on the same vertical side of the ring of radius `2`. Their rectangle contains `25, 10, 11, 12, 13`, whose sum is `71`. If every ring side is treated as fully inclusive, the corner values can be added twice.

The direction of the coordinate system also matters. For example, `7` and `9` lie on the same row, at coordinates `(-1,-1)` and `(-1,1)`. The rectangle contains exactly `7,8,9`, so the answer for `7 9` is `24`. Reversing the meaning of the first coordinate changes which side of the spiral is being considered and silently produces incorrect coordinates.

Finally, large values must not be converted through floating-point square roots. For an input such as `10^18`, a floating-point approximation can land on the wrong spiral ring near a perfect square. Python integers and `math.isqrt` avoid this entire class of errors.

## Approaches

The direct approach is straightforward. First locate `i` and `j` in the spiral. Then determine the minimum and maximum row and column among the two positions. Finally, enumerate every cell in that rectangle, evaluate its ulam number, and add it to the answer.

This brute force is correct because the requested rectangle is finite, and every cell is visited exactly once. The problem is its size. With values near `10^18`, the two points can be separated by roughly `10^9` cells in each coordinate direction, giving a rectangle containing roughly `10^18` cells. The worst-case operation count is therefore on the order of `10^18` cell evaluations for just one test case.

The useful observation is that the spiral is highly structured. Every cell belongs to exactly one square ring, where the ring index is

[
k=\max(|a|,|b|).
]

Ring `k` contains the values from the previous square plus one through `(2k+1)^2`. More importantly, each of its four sides is an arithmetic progression whose value is a quadratic polynomial in `k` plus a linear function of the position along that side.

For example, the bottom side of ring `k`, where `a=-k`, has

[
value = 4k^2+3k+1+b.
]

The other three sides have similarly simple formulas. This changes the problem completely. Instead of visiting every cell, we sum the intersection of the requested rectangle with every ring side symbolically. For a fixed side, the coordinates that belong to the rectangle are bounded by expressions of the form `constant`, `k`, or `-k`. Between consecutive points where these expressions cross, the endpoints are fixed affine functions of `k`. The contribution of one ring is then a polynomial of degree at most three in `k`, which can be summed with standard formulas for powers of integers.

The brute-force method works because it explicitly visits the cells. It fails because there can be quadrillions of them. The observation that every ring side is an affine sequence around a quadratic base lets us replace all those visits by a constant number of polynomial summations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(A)` per case, where `A` is rectangle area | `O(1)` | Too slow |
| Optimal | `O(1)` per case | `O(1)` | Accepted |

## Algorithm Walkthrough

1. Convert each input ulam number into its spiral coordinates.

For a number `n`, let `k` be the smallest nonnegative integer satisfying

[
n\le(2k+1)^2.
]

This is its ring. The largest value on the ring is `(2k+1)^2`, located at `(-k,k)`. Walking around the ring from there gives the coordinate formulas used later.

If

[
d=(2k+1)^2-n,
]

then the four parts of the ring are obtained from `d`:

[
\begin{aligned}
d<2k &: (a,b)=(-k,k-d),\
2k\le d<4k &: (a,b)=(-k+d-2k,-k),\
4k\le d<6k &: (a,b)=(k,-k+d-4k),\
6k\le d &: (a,b)=(k-(d-6k),k).
\end{aligned}
]

The center `n=1` is naturally handled by `k=0`.
2. Take the coordinate-wise bounding rectangle of the two positions.

If the two positions are `(a1,b1)` and `(a2,b2)`, define

[
L_a=\min(a_1,a_2),\quad R_a=\max(a_1,a_2),
]

and

[
L_b=\min(b_1,b_2),\quad R_b=\max(b_1,b_2).
]

The required rectangle is exactly

[
L_a\le a\le R_a,\qquad L_b\le b\le R_b.
]
3. Express the value on each ring side as a polynomial.

We assign every corner to exactly one side to avoid double counting. The resulting side ranges and value formulas are

[
\begin{array}{c|c|c}
Side & Coordinate range & Value\
\hline
Bottom & a=-k,\ -k\le b\le k & 4k^2+3k+1+b\
Left & b=-k,\ -k+1\le a\le k & 4k^2+k+1-a\
Top & a=k,\ -k+1\le b\le k & 4k^2-k+1-b\
Right & b=k,\ -k+1\le a\le k-1 & 4k^2-3k+1+a
\end{array}
]

The asymmetric endpoint rules are deliberate. The bottom side owns both bottom corners, the left side owns the top-left corner, the top side owns the top-right corner, and the right side owns no corners.
4. For each side, determine which rings can intersect the requested rectangle.

For example, on the bottom side we have `a=-k`. The rectangle requires

[
L_a\le-k\le R_a,
]

so

[
-R_a\le k\le-L_a.
]

Similar inequalities give the valid `k` range for the other three sides.
5. For a fixed valid ring, intersect the side's coordinate interval with the rectangle's coordinate interval.

Every endpoint is an affine function of `k`. For example, on the bottom side,

[
-k\le b\le k
]

must be intersected with

[
L_b\le b\le R_b.
]

Thus the actual endpoints are

[
l(k)=\max(L_b,-k),
\qquad
r(k)=\min(R_b,k).
]

On other sides, the same idea applies, with intervals such as `[-k+1,k]` or `[-k+1,k-1]`.
6. Split the range of `k` whenever two affine endpoint expressions cross.

Each endpoint is one of four affine functions: the rectangle's fixed lower bound, the side's lower bound, the rectangle's fixed upper bound, or the side's upper bound. Two affine functions can change order only once. We therefore collect all integer crossing points, split the `k` range there, and process each resulting interval separately.

Inside one such interval, we know exactly which affine expression is the lower endpoint and which is the upper endpoint. Their forms are

[
l(k)=pk+q,\qquad r(k)=sk+t.
]
7. Sum one side of one `k` interval as a polynomial.

Suppose the value formula on the side is

[
Ak^2+Bk+C+Dx.
]

The number of selected cells is

[
r-l+1,
]

which is linear in `k`. The sum of their coordinates is

[
\frac{r(r+1)-l(l-1)}2,
]

which is quadratic in `k`.

Consequently, the total contribution of the side is a polynomial of degree at most three in `k`. We evaluate the sums of `1`, `k`, `k^2`, and `k^3` over the interval using closed formulas.
8. Add the contributions of the four sides modulo `10^9+7`.

There are only four sides, and each side produces only a constant number of `k` intervals. The entire test case therefore takes constant time.

### Why it works

The invariant is that every cell of the spiral belongs to exactly one of the four owned side ranges of exactly one ring. The coordinate conversion puts each input ulam on its unique ring and side, while the bounding rectangle contains exactly the cells whose coordinates lie between the two extrema.

For each owned side, the intersection with the rectangle is represented exactly by its lower and upper affine endpoint functions. Splitting at every crossing makes those functions fixed choices throughout each processed interval. The polynomial calculation then sums every selected cell on those rings exactly once. Since the four side ownership ranges partition every ring without overlap, their contributions equal precisely the sum of the requested rectangle.

## Python Solution

```python
import sys
from math import isqrt

input = sys.stdin.readline

MOD = 10**9 + 7
INV2 = pow(2, MOD - 2, MOD)
INV6 = pow(6, MOD - 2, MOD)

def coord(n):
    # Smallest k such that n <= (2k + 1)^2.
    k = (isqrt(n - 1) + 1) // 2

    m = (2 * k + 1) ** 2
    d = m - n

    if d < 2 * k:
        # Bottom: a = -k
        return -k, k - d

    if d < 4 * k:
        # Left: b = -k
        d -= 2 * k
        return -k + d, -k

    if d < 6 * k:
        # Top: a = k
        d -= 4 * k
        return k, -k + d

    # Right: b = k
    d -= 6 * k
    return k - d, k

def powers_sum(l, r):
    if l > r:
        return (0, 0, 0, 0)

    n = r - l + 1

    def pref1(x):
        return x * (x + 1) * INV2 % MOD

    def pref2(x):
        return x * (x + 1) * (2 * x + 1) % MOD * INV6 % MOD

    def pref3(x):
        y = x * (x + 1) % MOD * INV2 % MOD
        return y * y % MOD

    return (
        n % MOD,
        (pref1(r) - pref1(l - 1)) % MOD,
        (pref2(r) - pref2(l - 1)) % MOD,
        (pref3(r) - pref3(l - 1)) % MOD,
    )

def add_side(ans, kl, kr, fixed_l, fixed_r,
             lp, lq, rp, rq, A, B, C, D):
    """
    Sum one spiral side.

    The side coordinate interval is
        [lp*k + lq, rp*k + rq]
    and the rectangle coordinate interval is
        [fixed_l, fixed_r].

    Value on the side is
        A*k^2 + B*k + C + D*x.
    """
    kl = max(kl, 0)
    if kl > kr:
        return ans

    # Four affine expressions determine the two endpoints:
    # fixed_l, geometric_l, fixed_r, geometric_r.
    expr = [
        (0, fixed_l),
        (lp, lq),
        (0, fixed_r),
        (rp, rq),
    ]

    cuts = {kl, kr + 1}

    # Within each interval between crossings, the ordering of
    # all endpoint expressions is fixed.
    for i in range(4):
        p1, q1 = expr[i]
        for j in range(i + 1, 4):
            p2, q2 = expr[j]
            den = p1 - p2
            num = q2 - q1

            if den != 0 and num % den == 0:
                x = num // den
                if kl <= x <= kr:
                    cuts.add(x)
                    if x + 1 <= kr:
                        cuts.add(x + 1)

    cuts = sorted(cuts)

    for idx in range(len(cuts) - 1):
        l = cuts[idx]
        r = cuts[idx + 1] - 1

        if l > r:
            continue

        mid = (l + r) // 2

        gl = lp * mid + lq
        gr = rp * mid + rq

        # Choose which affine expression realizes max(fixed_l, geometric_l).
        if fixed_l >= gl:
            Lp, Lq = 0, fixed_l
        else:
            Lp, Lq = lp, lq

        # Choose which affine expression realizes min(fixed_r, geometric_r).
        if fixed_r <= gr:
            Rp, Rq = 0, fixed_r
        else:
            Rp, Rq = rp, rq

        # If the interval is empty at the midpoint, it is empty
        # throughout this segment because all orderings are fixed.
        if Lp * mid + Lq > Rp * mid + Rq:
            continue

        # count = r(k) - l(k) + 1
        count0 = Rq - Lq + 1
        count1 = Rp - Lp

        # Base value polynomial is C + B*k + A*k^2.
        base = [C, B, A]

        # Multiply base by count.
        poly = [0, 0, 0, 0]
        count = [count0, count1]

        for i in range(3):
            for j in range(2):
                poly[i + j] += base[i] * count[j]

        # Sum of coordinates:
        # (r(r+1) - l(l-1)) / 2.
        # For x = p*k + q:
        # x(x+1) = p^2*k^2 + p*(2q+1)*k + q(q+1).
        r2 = Rp * Rp
        r1 = Rp * (2 * Rq + 1)
        r0 = Rq * (Rq + 1)

        l2 = Lp * Lp
        l1 = Lp * (2 * Lq - 1)
        l0 = Lq * (Lq - 1)

        poly[2] += D * (r2 - l2) * INV2
        poly[1] += D * (r1 - l1) * INV2
        poly[0] += D * (r0 - l0) * INV2

        s0, s1, s2, s3 = powers_sum(l, r)

        ans += poly[0] * s0
        ans += poly[1] * s1
        ans += poly[2] * s2
        ans += poly[3] * s3
        ans %= MOD

    return ans

def solve_case(i, j):
    a1, b1 = coord(i)
    a2, b2 = coord(j)

    la = min(a1, a2)
    ra = max(a1, a2)
    lb = min(b1, b2)
    rb = max(b1, b2)

    ans = 0

    # Bottom:
    # a = -k, b in [-k, k]
    # value = 4k^2 + 3k + 1 + b
    ans = add_side(
        ans,
        -ra, -la,
        lb, rb,
        -1, 0, 1, 0,
        4, 3, 1, 1
    )

    # Left:
    # b = -k, a in [-k+1, k]
    # value = 4k^2 + k + 1 - a
    ans = add_side(
        ans,
        -rb, -lb,
        la, ra,
        -1, 1, 1, 0,
        4, 1, 1, -1
    )

    # Top:
    # a = k, b in [-k+1, k]
    # value = 4k^2 - k + 1 - b
    ans = add_side(
        ans,
        la, ra,
        lb, rb,
        -1, 1, 1, 0,
        4, -1, 1, -1
    )

    # Right:
    # b = k, a in [-k+1, k-1]
    # value = 4k^2 - 3k + 1 + a
    ans = add_side(
        ans,
        lb, rb,
        la, ra,
        -1, 1, 1, -1,
        4, -3, 1, 1
    )

    return ans % MOD

def main():
    t = int(input())
    out = []

    for _ in range(t):
        i, j = map(int, input().split())
        out.append(str(solve_case(i, j)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The `coord` function first finds the ring containing the requested number. The expression `(isqrt(n - 1) + 1) // 2` gives the correct ring without floating-point arithmetic. The variable `d` measures how far the number is from the maximum value at the bottom-right corner, which directly identifies its side and coordinate.

The `powers_sum` function provides the four quantities needed for a cubic polynomial: the sums of `1`, `k`, `k^2`, and `k^3`. All divisions are performed modulo `10^9+7` using modular inverses.

The central routine is `add_side`. Its four affine endpoint expressions are enough to describe every possible intersection between one spiral side and the rectangle. It inserts every integer crossing into the partition, so inside each resulting interval the same endpoint expressions remain active. The midpoint is only used to identify those active expressions, not to approximate the answer.

The polynomial in `add_side` deserves particular attention. The value of one cell is quadratic in `k`, while the number of cells on the selected part of a side is linear in `k`. Their product is cubic. The coordinate sum contributes another quadratic term. Thus the whole interval is reducible to the four power sums returned by `powers_sum`.

The side ranges deliberately use different endpoints. The bottom side includes both bottom corners, the left side starts one position after the bottom-left corner, the top side starts one position after the top-left corner, and the right side excludes both remaining corners. This makes the four ranges disjoint and prevents double counting.

Python integers have arbitrary precision, so the intermediate products are safe even though the original values are as large as `10^18` and the rectangle sum is much larger.

## Worked Examples

### Sample 1, `2 12`

The coordinates are

[
2=(0,1),\qquad 12=(1,2).
]

The bounding rectangle is therefore

[
0\le a\le1,\qquad1\le b\le2.
]

The cells inside it are `2, 11, 3, 12`.

| Step | `k` | Selected coordinates | Values added | Running sum |
| --- | --- | --- | --- | --- |
| Bottom side | `1` | `(0,1)` | `2` | `2` |
| Right/top intersection | `2` | `(0,2)` | `11` | `13` |
| Top side | `1` | `(1,1)` | `3` | `16` |
| Right side | `2` | `(1,2)` | `12` | `28` |

The answer is `28`, matching the sample. The trace shows that the rectangle can intersect several different rings, but the algorithm never iterates over all rings between them. Each applicable range is summed as a polynomial.

### Sample 1, `9 7`

The coordinates are

[
9=(-1,1),\qquad7=(-1,-1).
]

Both values lie on the same row, so the bounding rectangle is

[
a=-1,\qquad -1\le b\le1.
]

| Step | `k` | Selected coordinates | Values added | Running sum |
| --- | --- | --- | --- | --- |
| Bottom side | `1` | `(-1,-1)` | `7` | `7` |
| Bottom side | `1` | `(-1,0)` | `8` | `15` |
| Bottom side | `1` | `(-1,1)` | `9` | `24` |

The answer is `24`. This case exercises a narrow rectangle whose entire content lies on one spiral side.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(1)` per test case | Four sides, each split into only a constant number of affine-order intervals |
| Space | `O(1)` | Only a constant number of coordinates, polynomial coefficients, and interval boundaries are stored |

With at most `20,000` test cases and inputs up to `10^18`, the solution performs only a small constant amount of arithmetic per case. It never constructs the spiral, never iterates over the rectangle, and never iterates over all rings between the two input values, so it fits comfortably within the `3` second and `512 MB` limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

# The production solution above can be placed in this function/module.
# For a standalone test file, assume solve_case is already defined.

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    try:
        t = int(input())
        ans = []
        for _ in range(t):
            i, j = map(int, input().split())
            ans.append(str(solve_case(i, j)))
        return "\n".join(ans)
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run("""\
3
2 12
9 7
7 9
""") == """\
28
24
24
""", "sample 1"

# Minimum input, same cell
assert run("""\
1
1 1
""") == """\
1
""", "single center cell"

# Adjacent cells
assert run("""\
1
1 2
""") == """\
3
""", "adjacent cells"

# Same row, exercises side traversal
assert run("""\
1
7 9
""") == """\
24
""", "same-row boundary case"

# Same column, includes two corners of one ring
assert run("""\
1
13 25
""") == """\
71
""", "same-column ring case"

# Maximum input value, equal endpoints
assert run("""\
1
1000000000000000000 1000000000000000000
""") == """\
49
""", "maximum value and modular reduction"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1` | `1` | Minimum input and degenerate one-cell rectangle |
| `1 / 1 2` | `3` | Adjacent cells and the first spiral step |
| `1 / 7 9` | `24` | Same-row rectangle and bottom-side traversal |
| `1 / 13 25` | `71` | Same-column traversal and ring-corner ownership |
| `1 / 10^18 10^18` | `49` | Maximum input, exact ring calculation, and modulo arithmetic |

## Edge Cases

The equal-input case is handled before any geometric complication can arise. For `1 1`, both coordinates are `(0,0)`, so the rectangle is one cell. The bottom-side calculation includes ring `k=0`, whose formula gives `1`, while the other three owned side ranges are empty. The output is exactly `1`.

The same-row case `7 9` has coordinates `(-1,-1)` and `(-1,1)`. The only relevant ring is `k=1`, and the bottom side contributes the interval `b=-1..1`. Its formula gives `7,8,9`, producing `24`. No other side adds these cells, so there is no duplication.

The corner case `13 25` has coordinates `(2,2)` and `(-2,2)`. The rectangle is the single column `b=2`, with rows from `-2` through `2`. The values are `25,10,11,12,13`, summing to `71`. The bottom side owns `25`, the right side owns `10,11,12`, and the top side owns `13`. The endpoint conventions are exactly what prevent the corners from being counted twice.

The maximum-value case uses `10^18` for both inputs. Since the two coordinates are identical, only one cell is required. The algorithm locates the number using integer square-root arithmetic and returns its value modulo `10^9+7`. Because

[
10^{18}=(10^9)^2\equiv(-7)^2\equiv49\pmod{10^9+7},
]

the expected output is `49`. This also demonstrates why no floating-point computation is needed anywhere in the solution.
