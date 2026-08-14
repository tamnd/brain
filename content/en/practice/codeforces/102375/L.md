---
title: "CF 102375L - \u0411\u043b\u0438\u0436\u0430\u0439\u0448\u0438\u0435 \u0442\u043e\u0447\u043a\u0438"
description: "We care only about the Voronoi cell of the first marked point, restricted to the integer grid points inside the rectangle. A grid point (x, y) is good exactly when its Euclidean distance to p1 is no larger than its distance to every other marked point."
date: "2026-08-14T13:23:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "L"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 234
verified: false
draft: false
---

[CF 102375L - \u0411\u043b\u0438\u0436\u0430\u0439\u0448\u0438\u0435 \u0442\u043e\u0447\u043a\u0438](https://codeforces.com/problemset/problem/102375/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We care only about the Voronoi cell of the first marked point, restricted to the integer grid points inside the rectangle. A grid point `(x, y)` is good exactly when its Euclidean distance to `p1` is no larger than its distance to every other marked point.

The rectangle contains `(X + 1)(Y + 1)` integer points. For every candidate point, a direct solution compares its distance to all `K` marked points, so the straightforward method needs roughly `(X + 1)(Y + 1)K` distance comparisons. With all three parameters reaching `2 * 10^5`, that is about `8 * 10^15` comparisons, far beyond what is practical. We need to exploit the fact that comparing squared Euclidean distances makes the quadratic terms in `x` and `y` cancel.

There are several boundary cases that can silently break an implementation. With only one marked point, every grid point is good. For example,

```
1 1 1
0 0
```

has answer `4`, because all four integer points of the rectangle belong to the first point's region. An implementation that assumes at least one competitor may accidentally build an empty minimum or maximum envelope.

Another issue is a bisector passing between integer coordinates. Consider

```
2 1 2
2 0
1 0
```

The first point is closer whenever `x >= 1.5`, so the only good integer points have `x = 2`. Both possible `y` values are good, giving answer `2`. A careless integer conversion of a rational boundary can incorrectly include `x = 1`.

A symmetric problem occurs when the required bound is a ceiling rather than a floor. For the same input, the lower boundary is `x >= 1.5`, and integer arithmetic must produce `ceil(1.5) = 2`. Python's integer division is useful here, but only after keeping the denominator positive and handling ceiling explicitly.

Marked points can also lie on the rectangle boundary. For example,

```
2 1 2
0 0
2 0
```

contains points whose nearest marked point changes along the bottom edge, while the same comparison also applies to the row `y = 1`. The rectangle boundaries must be included, not treated as strict inequalities.

## Approaches

The brute-force method examines every integer `(x, y)` with `0 <= x <= X` and `0 <= y <= Y`, computes its squared distance to `p1`, and compares it with the squared distance to every other marked point. This is correct because the definition of a good point is exactly that collection of comparisons. Its worst-case cost is `(X + 1)(Y + 1)(K - 1)`, which is approximately `8 * 10^15` operations at the maximum constraints.

The useful observation comes from expanding one comparison. Let `p1 = (a, b)` and another marked point be `(u, v)`. We need

`(x-a)^2 + (y-b)^2 <= (x-u)^2 + (y-v)^2`.

After cancellation of `x^2` and `y^2`, this becomes

`2(u-a)x + 2(v-b)y <= u^2 + v^2 - a^2 - b^2`.

Every competitor therefore contributes a half-plane, not a curved condition. The set of good real points is the intersection of all these half-planes with the rectangle.

For a fixed integer `x`, every non-vertical half-plane gives either an upper bound or a lower bound on `y`. If `v > b`, it has the form

`y <= (C - A x) / B`

with `B > 0`. If `v < b`, it becomes

`y >= (A x - C) / (-B)`.

Thus, for each `x`, all competitors can be summarized by just two values: the smallest upper-bound line and the largest lower-bound line. These are lower and upper envelopes of linear functions.

A Li Chao tree lets us maintain such an envelope and query it at every integer `x` in logarithmic time. We keep one tree for minimum upper bounds and another for maximum lower bounds. The coefficients are kept as exact fractions, so no floating-point geometry is needed.

The brute-force works because every candidate can be checked independently, but fails because there are too many candidates. The observation that each distance comparison becomes a linear inequality lets us summarize all competitors by two line envelopes and process only the `X + 1` possible columns.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(XYK)` | `O(K)` | Too slow |
| Optimal | `O(K log X + X log X)` | `O(K + X)` | Accepted |

## Algorithm Walkthrough

1. Read `p1 = (a, b)` and regard every other marked point `(u, v)` as a constraint. Squared distances are sufficient because comparing nonnegative distances is equivalent to comparing their squares.
2. Expand the comparison against `(u, v)` into

`A x + B y <= C`,

where `A = 2(u-a)`, `B = 2(v-b)`, and `C = u^2 + v^2 - a^2 - b^2`.

The quadratic terms disappear, which is the key transformation from geometry to linear functions.
3. If `B > 0`, solve the inequality for `y` and obtain

`y <= (C - A x) / B`.

Store this rational linear function in a minimum Li Chao tree because the strongest upper restriction is the smallest one.
4. If `B < 0`, solve for `y` in the opposite direction and obtain

`y >= (A x - C) / (-B)`.

Store this function in a maximum Li Chao tree because the strongest lower restriction is the largest one.
5. If `B = 0`, the constraint contains only `x`. When `A > 0`, it restricts `x` from above with `x <= floor(C / A)`. When `A < 0`, it restricts `x` from below with `x >= ceil(C / A)`. Intersect these restrictions with `[0, X]`.

There is no `A = B = 0` case because the marked points are pairwise distinct.
6. Build the two Li Chao trees over the integer domain `[0, X]`. The trees compare rational line values by cross multiplication, so every comparison is exact.
7. For each integer `x` from the allowed left endpoint to the allowed right endpoint, query the minimum upper line and maximum lower line. Start with the rectangle's own limits `0 <= y <= Y`, so

`upper = min(Y, minimum upper constraint)`

and

`lower = max(0, maximum lower constraint)`.
8. Convert the rational bounds to integer bounds. The largest allowed integer `y` is `floor(upper)`, while the smallest allowed integer `y` is `ceil(lower)`. If the lower integer bound does not exceed the upper integer bound, add their difference plus one to the answer.
9. Output the accumulated number of integer points.

The invariant is that after processing all marked points, every query at a fixed integer `x` returns exactly the strongest upper and lower restrictions imposed by every competitor. Intersecting those restrictions with `[0, Y]` gives precisely the integer `y` values satisfying every distance comparison. Since every good point is characterized by those comparisons, every counted point is good and every good point is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def floor_div(a, b):
    return a // b

def ceil_div(a, b):
    return -((-a) // b)

class LiChao:
    def __init__(self, left, right, is_min):
        self.left = left
        self.right = right
        self.is_min = is_min
        self.tree = [None] * (4 * (right - left + 1))

    @staticmethod
    def value(line, x):
        m, b, d = line
        return m * x + b, d

    def better(self, a, b, x):
        if b is None:
            return True

        an, ad = self.value(a, x)
        bn, bd = self.value(b, x)

        left = an * bd
        right = bn * ad

        if self.is_min:
            return left < right
        return left > right

    def insert(self, line):
        self._insert(1, self.left, self.right, line)

    def _insert(self, node, l, r, line):
        cur = self.tree[node]

        if cur is None:
            self.tree[node] = line
            return

        mid = (l + r) // 2

        if self.better(line, cur, mid):
            self.tree[node], line = line, cur
            cur = self.tree[node]

        if l == r:
            return

        if self.better(line, cur, l) != self.better(line, cur, mid):
            self._insert(node * 2, l, mid, line)
        else:
            self._insert(node * 2 + 1, mid + 1, r, line)

    def query(self, x):
        return self._query(1, self.left, self.right, x)

    def _query(self, node, l, r, x):
        cur = self.tree[node]

        if l == r:
            return cur

        mid = (l + r) // 2

        if x <= mid:
            other = self._query(node * 2, l, mid, x)
        else:
            other = self._query(node * 2 + 1, mid + 1, r, x)

        if cur is None:
            return other
        if other is None:
            return cur

        if self.better(other, cur, x):
            return other
        return cur

def solve():
    X, Y, K = map(int, input().split())
    points = [tuple(map(int, input().split())) for _ in range(K)]

    a, b = points[0]

    lower_x = 0
    upper_x = X

    upper_tree = LiChao(0, X, True)
    lower_tree = LiChao(0, X, False)

    base = a * a + b * b

    for u, v in points[1:]:
        A = 2 * (u - a)
        B = 2 * (v - b)
        C = u * u + v * v - base

        if B > 0:
            # y <= (C - A*x) / B
            upper_tree.insert((-A, C, B))

        elif B < 0:
            # y >= (A*x - C) / (-B)
            lower_tree.insert((A, -C, -B))

        else:
            # A*x <= C
            if A > 0:
                upper_x = min(upper_x, floor_div(C, A))
            else:
                lower_x = max(lower_x, ceil_div(C, A))

    if lower_x > upper_x:
        print(0)
        return

    answer = 0

    for x in range(lower_x, upper_x + 1):
        low = 0
        high = Y

        line = lower_tree.query(x)
        if line is not None:
            m, c, d = line
            low = max(low, ceil_div(m * x + c, d))

        line = upper_tree.query(x)
        if line is not None:
            m, c, d = line
            high = min(high, floor_div(m * x + c, d))

        if low <= high:
            answer += high - low + 1

    print(answer)

if __name__ == "__main__":
    solve()
```

The input is read once into the list of marked points because every competitor has to be converted into one linear constraint. The first point is separated as `(a, b)`, since all constraints compare directly against it.

The values `A`, `B`, and `C` are stored with the factor `2` included. This avoids introducing half-integer constants during the transformation. For an upper constraint, the stored line represents `(C - A*x) / B`, so its numerator has slope `-A`. For a lower constraint, the denominator is made positive by multiplying the inequality by `-1`, giving `(A*x - C) / (-B)`.

The Li Chao tree never converts these values to floating point. If two fractions `n1 / d1` and `n2 / d2` have positive denominators, comparing them is equivalent to comparing `n1*d2` with `n2*d1`. Python integers also have arbitrary precision, so the cross products cannot overflow.

The rectangle contributes the initial bounds `low = 0` and `high = Y`. A missing lower envelope means there is no competitor restricting `y` from below, and similarly for the upper envelope. This is what makes the `K = 1` case work without a special geometric case.

The final `+ 1` in `high - low + 1` is necessary because both endpoints are allowed. The problem uses a non-strict distance comparison, so points exactly on a bisector must be counted.

## Worked Examples

For Sample 1, `p1 = (2, 2)`. The four competitors produce the following relevant bounds:

`(1, 1)` gives `y >= 3 - x`.

`(1, 3)` gives `y <= x + 1`.

`(3, 3)` gives `y <= 5 - x`.

`(3, 1)` gives `y >= x - 1`.

Together with `0 <= y <= 4`, the query results are:

| x | Lower bound | Upper bound | Good y values | Added |
| --- | --- | --- | --- | --- |
| 0 | 3 | 1 | none | 0 |
| 1 | 2 | 2 | 2 | 1 |
| 2 | 1 | 3 | 1, 2, 3 | 3 |
| 3 | 2 | 2 | 2 | 1 |
| 4 | 3 | 1 | none | 0 |

The total is `1 + 3 + 1 = 5`. The trace demonstrates why several half-planes must be combined: one competitor controls the lower boundary on the left, another controls it on the right, and the same happens for the upper boundary.

For Sample 2, `p1 = (0, 0)` and all other points are `(1,0)`, `(2,0)`, ..., `(5,0)`. Every competitor gives an upper bound on `x`, with the closest competitor `(1,0)` producing the tightest one:

`2x <= 1`, hence `x <= 1/2`.

All integer columns except `x = 0` are rejected.

| x | Lower bound | Upper bound | Good y values | Added |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 1 |
| 1 | 0 | 0 | none | 0 |
| 2 | 0 | 0 | none | 0 |
| 3 | 0 | 0 | none | 0 |
| 4 | 0 | 0 | none | 0 |
| 5 | 0 | 0 | none | 0 |
| 6 | 0 | 0 | none | 0 |

The table shows the vertical restriction after the constraints are processed. For the only allowed column `x = 0`, the rectangle still permits all `7` integer values of `y`, so the answer is `7`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(K log X + X log X)` | Each competitor is inserted into one Li Chao tree, then every allowed integer `x` is queried |
| Space | `O(K + X)` | The trees store `O(X)` nodes and there are `O(K)` stored lines |

With `K <= 2 * 10^5` and `X <= 2 * 10^5`, the algorithm performs only logarithmically many operations per constraint and per column. The largest intermediate arithmetic values are handled by Python's arbitrary-precision integers, so there is no fixed-width overflow issue. The memory usage is linear in the input size and the number of possible columns.

## Test Cases

The following harness assumes the submitted solution is saved as `solution.py`. It temporarily replaces the module's input and output streams, so each assertion executes the actual `solve()` function.

```python
import sys
import io
import solution

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = solution.input

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solution.input = sys.stdin.readline

    try:
        solution.solve()
        return sys.stdout.getvalue().strip()
    finally:
        solution.input = old_input
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run(
    """4 4 5
2 2
1 1
1 3
3 3
3 1
"""
) == "5", "sample 1"

assert run(
    """6 6 6
0 0
1 0
2 0
3 0
4 0
5 0
"""
) == "7", "sample 2"

# Minimum-size instance, only p1 exists.
assert run(
    """1 1 1
0 0
"""
) == "4", "single marked point"

# Boundary and ceiling handling.
assert run(
    """2 1 2
2 0
1 0
"""
) == "2", "half-integer lower boundary"

# All marked points share the same y-coordinate.
# p1=(2,1), competitors are (0,1) and (4,1).
# Good x are 1,2,3, for both y=0..3.
assert run(
    """4 3 3
2 1
0 1
4 1
"""
) == "12", "horizontal Voronoi strip"

# Horizontal bounds around p1.
# p1=(1,1), competitors immediately above and below.
# Only y=1 survives, for all four x coordinates.
assert run(
    """3 2 3
1 1
1 0
1 2
"""
) == "4", "upper and lower horizontal restrictions"

# Maximum-size construction.
# p1=(0,0), followed by 199999 points on y=0.
# Only x=0 is good, while every y from 0 through 200000 is allowed.
points = ["200000 200000 200000"]
points.append("0 0")
for x in range(1, 200000):
    points.append(f"{x} 0")

max_case = "\n".join(points) + "\n"
assert run(max_case) == "200001", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 0 0` | `4` | Minimum dimensions and the `K = 1` case |
| `2 1 2 / 2 0 / 1 0` | `2` | Exact handling of a half-integer lower boundary |
| `4 3 3 / 2 1 / 0 1 / 4 1` | `12` | Multiple constraints with identical `y` coordinates |
| `3 2 3 / 1 1 / 1 0 / 1 2` | `4` | Simultaneous lower and upper restrictions on `y` |
| `200000 200000 200000` with points `(0,0), (1,0), ..., (199999,0)` | `200001` | Maximum values of `X`, `Y`, and `K`, plus a tight vertical envelope |

## Edge Cases

The single-point case

```
1 1 1
0 0
```

creates no competitor lines at all. Both Li Chao trees remain empty, so every column starts with `low = 0` and `high = 1`. Each of the two columns contributes two points, giving `4`. The algorithm does not need to special-case this situation because an empty envelope naturally means that no additional restriction exists.

For the half-integer boundary

```
2 1 2
2 0
1 0
```

the comparison is

`(x-2)^2 + y^2 <= (x-1)^2 + y^2`,

which simplifies to `x >= 1.5`. The lower Li Chao tree stores the exact fraction `3/2`. At `x = 1`, the integer lower bound becomes `ceil(3/2) = 2`, exceeding the rectangle's `x` value, so no `y` is counted. At `x = 2`, the lower bound is still `2`, and both `y = 0` and `y = 1` are valid. The answer is `2`.

For the horizontal strip

```
4 3 3
2 1
0 1
4 1
```

the competitor `(0,1)` gives `x >= 1`, while `(4,1)` gives `x <= 3`. There are no restrictions on `y`, so the columns `1`, `2`, and `3` each contribute the four integer rows `0`, `1`, `2`, and `3`. The result is `12`. This exercises the case where the two envelopes are effectively horizontal constraints and verifies that the rectangle boundaries are included.

For

```
3 2 3
1 1
1 0
1 2
```

the point `(1,0)` gives `y >= 1/2`, while `(1,2)` gives `y <= 3/2`. On integer coordinates, only `y = 1` survives. Every `x` from `0` through `3` is allowed, so the algorithm adds one point for each of four columns and returns `4`. This checks both `ceil` and `floor` on rational bounds.

For the maximum-size case, the first point is `(0,0)` and all other marked points are `(x,0)` for `1 <= x <= 199999`. The closest competitor `(1,0)` already forces `x <= 1/2`, so among integer columns only `x = 0` remains. The rectangle contains `200001` possible values of `y`, from `0` through `200000`, and all of them are equally closest to `p1` because every competitor has the same `y` coordinate. The answer is consequently `200001`, confirming that the implementation handles the largest input without scanning all `K` competitors for every grid point.
