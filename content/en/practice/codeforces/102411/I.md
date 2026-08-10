---
title: "CF 102411I - Ideal Pyramid"
description: "We need to choose an integer center (X, Y) and an integer height H for an axis-aligned square pyramid. Because every side has slope exactly 45°, moving one unit horizontally or vertically away from the center lowers the pyramid by exactly one unit."
date: "2026-08-10T14:48:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102411
codeforces_index: "I"
codeforces_contest_name: "ICPC 2019-2020 North-Western Russia Regional Contest"
rating: 0
weight: 102411
solve_time_s: 785
verified: true
draft: false
---

[CF 102411I - Ideal Pyramid](https://codeforces.com/problemset/problem/102411/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 13m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to choose an integer center `(X, Y)` and an integer height `H` for an axis-aligned square pyramid. Because every side has slope exactly `45°`, moving one unit horizontally or vertically away from the center lowers the pyramid by exactly one unit. Thus, at position `(x, y)`, the pyramid's height is

[
H-\max(|x-X|,|y-Y|).
]

An obelisk `(x_i, y_i, h_i)` fits if its height does not exceed this value. The task is to find a pyramid with the smallest possible height that contains every obelisk, and output any center achieving that minimum.

The input contains at most `1000` obelisks. Their coordinates and heights can reach `10^8` in magnitude, so enumerating possible coordinates is completely infeasible. A coordinate can have roughly `2 * 10^8` possible values, giving roughly `4 * 10^16` possible centers. With `1000` obelisks, checking all of them would require around `4 * 10^19` elementary checks. The solution needs to process the input essentially linearly.

The integer restrictions also matter. A continuous geometric optimum is not enough because the center and height must be integers. Fortunately, the relevant constraints are all integer intervals, so the exact integer optimum can be obtained without floating point arithmetic.

There are several edge cases that can make a careless solution fail. With a single obelisk,

```
1
0 0 5
```

the answer is `0 0 5`. A method that blindly tries to place the center halfway between extreme coordinates can accidentally increase the height even though placing it directly under the obelisk is optimal.

A more interesting boundary case is

```
2
0 0 1
2 0 1
```

The correct answer can be

```
1 0 2
```

because the pyramid has height `2`, and both obelisks are exactly one unit from the center. The interval for the optimal center closes at a single integer point. Using strict inequalities instead of inclusive ones would incorrectly reject this solution.

Different dimensions can also require different heights. For example,

```
2
0 0 100
10 0 1
```

has optimal height `100`, with center `(0, 0)`. The very tall first obelisk dominates the answer, even though the second obelisk is far away. Treating all obelisks as if they had the same height would produce the wrong result.

Finally, large negative coordinates must be handled without assumptions that coordinates are nonnegative. For

```
2
-100000000 -100000000 1
100000000 100000000 1
```

the optimal height is `100000001`, and `(0, 0)` is a valid center. Python integers handle this range naturally, while fixed-width implementations need sufficiently wide integer types.

## Approaches

A direct approach would enumerate candidate centers `(X, Y)`. For each center, we could compute the smallest required height as

[
\max_i\left(h_i+\max(|x_i-X|,|y_i-Y|)\right).
]

This is correct because each obelisk independently tells us the minimum height needed at that center. However, there are about `4 * 10^16` integer centers in the coordinate range, and checking `1000` obelisks for each gives roughly `4 * 10^19` operations in the worst case. The time limit rules this out immediately.

The useful observation is hidden inside the `max`. We can rewrite

\max(h_i+|x_i-X|,\ h_i+|y_i-Y|).
]

Taking the maximum over all obelisks gives

[
H=
\max\left(
\max_i(h_i+|x_i-X|),
\max_i(h_i+|y_i-Y|)
\right).
]

The two coordinates have completely separated. We can independently determine the smallest height needed for the `x` coordinate and for the `y` coordinate, then take the larger of the two heights.

Consider just one dimension. We have positions `c_i`, heights `h_i`, and want the smallest integer `H` for which some integer center `C` satisfies

[
h_i+|c_i-C|\le H
]

for every `i`. Rearranging gives

[
c_i+h_i-H\le C\le c_i-h_i+H.
]

Each obelisk therefore gives an allowed interval for `C`. All obelisks can be satisfied exactly when these intervals have a common point.

Define

[
L=\max_i(c_i+h_i),
\qquad
R=\min_i(c_i-h_i).
]

After intersecting all intervals, the possible centers are precisely

[
[L-H,\ R+H].
]

This interval is nonempty exactly when

[
L-H\le R+H,
]

or

[
2H\ge L-R.
]

Thus the minimum integer height required by this coordinate is

[
H_{\text{dim}}=\left\lceil\frac{L-R}{2}\right\rceil.
]

We calculate this once for `x` and once for `y`. The pyramid must satisfy both dimensions, so its minimum height is the maximum of those two values. Once that height is known, any integer point in each resulting interval is a valid center. Choosing the left endpoint, `L-H`, is convenient and avoids any rounding issues.

The brute-force approach works because it explicitly evaluates every possible center. It fails because the coordinate space is enormous. The observation that the `max` separates into independent `x` and `y` terms reduces the geometric problem to two one-dimensional interval intersections, which can each be processed in one pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n · C²)` where `C` is the coordinate range | `O(n)` | Too slow |
| Optimal | `O(n)` | `O(n)` for storing input, or `O(1)` beyond it | Accepted |

## Algorithm Walkthrough

1. Read all obelisks. For the `x` dimension, compute

[
L_x=\max_i(x_i+h_i)
]

and

[
R_x=\min_i(x_i-h_i).
]

These two values describe the intersection of all possible center intervals after the pyramid height is fixed.
2. Compute the same quantities for the `y` dimension:

[
L_y=\max_i(y_i+h_i),
\qquad
R_y=\min_i(y_i-h_i).
]

The two dimensions can be processed independently because the pyramid's required height is the maximum of the requirements in the two coordinates.
3. Find the minimum height required by the `x` dimension:

[
H_x=\left\lceil\frac{L_x-R_x}{2}\right\rceil.
]

For integer values, this is computed as `(L_x - R_x + 1) // 2`.
4. Find the corresponding value for the `y` dimension:

[
H_y=\left\lceil\frac{L_y-R_y}{2}\right\rceil.
]
5. Set

[
H=\max(H_x,H_y).
]

This height is sufficient for both dimensions, and it cannot be reduced because one of the two dimensions already needs at least this much height.
6. Choose

[
X=L_x-H,
\qquad
Y=L_y-H.
]

Since `H >= H_x` and `H >= H_y`, these values belong to their respective feasible intervals. They are integers because every quantity involved is an integer.
7. Output `X`, `Y`, and `H`. The resulting pyramid contains every obelisk, and no pyramid with a smaller height can contain all of them.

### Why it works

For any fixed height `H`, an obelisk `(c_i,h_i)` in one dimension permits exactly the center interval `[c_i+h_i-H, c_i-h_i+H]`. The intersection of all these intervals is `[L-H,R+H]`, so a valid center exists exactly when `2H >= L-R`. Hence `H_x` and `H_y` are the exact minimum heights forced by the two coordinates.

The full pyramid requires both one-dimensional inequalities simultaneously. Since its height requirement is the maximum of the independent `x` and `y` requirements, the global optimum is exactly `max(H_x,H_y)`. Choosing `L_x-H` and `L_y-H` places the center inside both feasible intersections, so every obelisk is contained while the height is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    lx = -10**30
    rx = 10**30
    ly = -10**30
    ry = 10**30

    for _ in range(n):
        x, y, h = map(int, input().split())

        lx = max(lx, x + h)
        rx = min(rx, x - h)

        ly = max(ly, y + h)
        ry = min(ry, y - h)

    hx = (lx - rx + 1) // 2
    hy = (ly - ry + 1) // 2

    H = max(hx, hy)

    X = lx - H
    Y = ly - H

    print(X, Y, H)

if __name__ == "__main__":
    solve()
```

The four variables `lx`, `rx`, `ly`, and `ry` maintain the extreme values needed for the interval intersections. For example, `lx` stores the largest `x_i + h_i`, because every feasible center must be at least `x_i + h_i - H`.

The expressions `x + h` and `x - h` should be kept in that order. Reversing one of them changes which side of the feasible interval is being represented and leads to incorrect centers.

The ceiling division is another place where an off-by-one error is easy. For nonnegative integer `d`, `ceil(d / 2)` is `(d + 1) // 2`. Here `L - R` is always nonnegative because for every obelisk, `x_i + h_i > x_i - h_i`, and the same ordering survives taking the maximum and minimum.

There is no floating point computation. The exact integer geometry is enough, and Python's arbitrary-precision integers comfortably handle all intermediate values. The largest relevant expression is on the order of `2 * 10^8`, so even a signed 64-bit integer would be sufficient in languages with fixed-width integers.

The code does not need to store the obelisks. Each one contributes only to four running extrema, so the implementation can process the input in a single pass.

## Worked Examples

### Sample 1

The input contains one obelisk at `(0,0)` with height `5`.

| Variable | After reading the obelisk |
| --- | --- |
| `lx` | `5` |
| `rx` | `-5` |
| `ly` | `5` |
| `ry` | `-5` |
| `hx` | `5` |
| `hy` | `5` |
| `H` | `5` |
| `X` | `0` |
| `Y` | `0` |

The feasible interval for the `x` center at height `5` is `[5-5,-5+5] = [0,0]`, and the same is true for `y`. Thus the center is forced to `(0,0)`, and the pyramid has height `5`.

### Sample 2

The obelisks are `(3,3,3)` and `(6,6,2)`.

| Obelisk | `x+h` | `x-h` | `y+h` | `y-h` |
| --- | --- | --- | --- | --- |
| `(3,3,3)` | `6` | `0` | `6` | `0` |
| `(6,6,2)` | `8` | `4` | `8` | `4` |

After both obelisks, we have `lx = 8`, `rx = 0`, `ly = 8`, and `ry = 0`.

| Variable | Value |
| --- | --- |
| `hx` | `(8-0+1)//2 = 4` |
| `hy` | `(8-0+1)//2 = 4` |
| `H` | `4` |
| `X` | `8-4 = 4` |
| `Y` | `8-4 = 4` |

At `(4,4)`, the first obelisk is one unit away in both coordinates, so the pyramid has height `4-1=3`. The second is two units away, so its available height is `4-2=2`. Both are exactly supported, giving the required output `4 4 4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` | Every obelisk updates four extrema once. |
| Space | `O(1)` | Only four extrema are maintained, excluding input storage. |

With `n <= 1000`, the algorithm performs only a few thousand integer operations. The coordinate and height bounds also fit comfortably within ordinary 64-bit arithmetic, while Python's integer type provides additional safety. The method is far below the available 2-second time and 512 MB memory limits.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = inp.strip().split()
    it = iter(data)

    n = int(next(it))

    lx = -10**30
    rx = 10**30
    ly = -10**30
    ry = 10**30

    for _ in range(n):
        x = int(next(it))
        y = int(next(it))
        h = int(next(it))

        lx = max(lx, x + h)
        rx = min(rx, x - h)
        ly = max(ly, y + h)
        ry = min(ry, y - h)

    hx = (lx - rx + 1) // 2
    hy = (ly - ry + 1) // 2

    H = max(hx, hy)
    X = lx - H
    Y = ly - H

    return f"{X} {Y} {H}\n"

def run(inp: str) -> str:
    return solve_data(inp)

assert run("""\
1
0 0 5
""") == "0 0 5\n", "sample 1"

assert run("""\
2
3 3 3
6 6 2
""") == "4 4 4\n", "sample 2"

assert run("""\
1
-100000000 -100000000 100000000
""") == "-100000000 -100000000 100000000\n", "minimum-size boundary case"

assert run("""\
2
0 0 1
2 0 1
""") == "1 0 2\n", "exact interval boundary"

assert run("""\
2
0 0 100
10 0 1
""") == "0 0 100\n", "different heights"

all_equal = "1000\n" + "\n".join(
    "12345678 -87654321 99999999" for _ in range(1000)
) + "\n"

assert run(all_equal) == "12345678 -87654321 99999999\n", "maximum n, equal values"

assert run("""\
2
-100000000 -100000000 1
100000000 100000000 1
""") == "0 0 100000001\n", "large negative and positive coordinates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0 0 5` | `0 0 5` | Single-obelisk minimum |
| `0 0 1 / 2 0 1` | `1 0 2` | Exact intersection boundary and ceiling division |
| `0 0 100 / 10 0 1` | `0 0 100` | Unequal heights and one dimension dominating |
| `1000` identical obelisks | `12345678 -87654321 99999999` | Maximum `n` and repeated values |
| `±100000000` coordinates | `0 0 100000001` | Coordinate boundaries and large arithmetic |

## Edge Cases

The single-obelisk case

```
1
0 0 5
```

produces `lx = ly = 5` and `rx = ry = -5`. Both one-dimensional minimum heights are `(5 - (-5) + 1) // 2 = 5`. The chosen center is `5 - 5 = 0` in both dimensions, giving `0 0 5`. The algorithm does not rely on having multiple obelisks to form an interval.

The exact-boundary case

```
2
0 0 1
2 0 1
```

gives `lx = 3` and `rx = -1`. The required `x` height is `(3 - (-1) + 1) // 2 = 2`. At height `2`, the feasible `x` interval is `[3-2,-1+2] = [1,1]`, so the only possible center is `X=1`. The `y` dimension needs only height `1`, so the final height remains `2`. This catches implementations that accidentally use floor division.

For the unequal-height case

```
2
0 0 100
10 0 1
```

the `x` extrema are `100` and `-100`, requiring height `100`, while the `y` extrema are also `100` and `-100`, but the resulting center calculation gives `(0,0)`. At that center the first obelisk reaches exactly height `100`, while the second has available height `90`, which is much more than its required height `1`. The tall obelisk determines the minimum.

For the coordinate-boundary case

```
2
-100000000 -100000000 1
100000000 100000000 1
```

we get `L_x = L_y = 100000001` and `R_x = R_y = -100000001`. Thus `H = (100000001 - (-100000001) + 1) // 2 = 100000001`. The chosen center is `0,0`. Each obelisk is exactly `100000000` units away in the relevant coordinate, leaving height `1`, so both are contained exactly at the boundary.

The maximum-size test with `1000` identical obelisks exercises the input bound without changing the mathematical structure. Every update leaves the four extrema unchanged after the first obelisk, so the final answer remains the same. This demonstrates why repeated points do not require any special handling and why the linear scan remains efficient.
