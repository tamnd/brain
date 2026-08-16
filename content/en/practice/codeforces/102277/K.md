---
title: "CF 102277K - Chocolates"
description: "Timothy has a rectangular box with a fixed width and height. Every chocolate bar must have integer dimensions, must fit inside that box without rotation, and each possible pair of dimensions may be used at most once. A bar with dimensions (a times b) costs (a b)."
date: "2026-08-16T19:45:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102277
codeforces_index: "K"
codeforces_contest_name: "UCF Locals 2018"
rating: 0
weight: 102277
solve_time_s: 294
verified: true
draft: false
---

[CF 102277K - Chocolates](https://codeforces.com/problemset/problem/102277/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

Timothy has a rectangular box with a fixed width and height. Every chocolate bar must have integer dimensions, must fit inside that box without rotation, and each possible pair of dimensions may be used at most once. A bar with dimensions (a \times b) costs (a b).

The orientation is part of the identity of a bar. A (5\times3) bar and a (3\times5) bar are different gifts, while two (5\times5) bars would be identical and only one may be used. Thus, if the box has dimensions (W\times H), the possible gifts are exactly the (WH) ordered pairs

[
1\le a\le W,\qquad 1\le b\le H.
]

The task is to choose as many different pairs as possible while keeping the sum of their areas, which is also their total cost, within Timothy's savings balance (B). The output is the maximum number of bars that can be made.

The official contest page gives a 3 second time limit and 256 MB memory limit. The difficulty comes from the fact that the rectangle can represent a very large number of possible dimension pairs, so enumerating all (WH) bars is not a viable strategy. We need to exploit the fact that the cost of a bar depends only on the product (ab).

The first non-obvious edge case is a square box. For a (2\times2) box, the four possible dimensions have costs (1,2,2,4). With budget (5), the correct answer is (3), because we can choose (1\times1), (1\times2), and (2\times1), whose total cost is (5). A careless implementation that treats (1\times2) and (2\times1) as the same bar would return (2).

A second edge case occurs when the budget is too small to buy anything. For a (3\times3) box and budget (0), the correct answer is (0). Every legal bar has positive area, so choosing the cheapest bar would already exceed the budget. An implementation that assumes at least one bar can always be selected would incorrectly return (1).

A third edge case is when the budget is large enough to buy every possible bar. For a (2\times2) box, the total cost of all four bars is (1+2+2+4=9). With budget (9), the answer is (4). There is no reason to stop after finding some affordable prefix, because every possible dimension pair can be taken.

## Approaches

The direct approach is to generate every possible pair ((a,b)), compute its cost (ab), sort all (WH) costs, and take the cheapest prefix whose sum fits in the budget. This is correct because every bar has the same value to us, namely one additional student receiving a gift, so among any fixed number of bars we should always choose the cheapest available ones.

The problem is the number of pairs. Generating the whole multiplication table already costs (O(WH)) operations and storing it requires (O(WH)) memory. If both dimensions are large, this is far beyond what a 3 second solution can afford. Even a version that avoids storing the table but scans every pair still performs (WH) multiplications.

The key observation is that we do not actually need to know the individual bars in sorted order. For a value (x), consider all bars whose area is at most (x). For a fixed width (a), the allowed heights satisfy

[
b\le \left\lfloor\frac{x}{a}\right\rfloor.
]

Because the box limits the height to (H), the number of such bars in row (a) is

[
t_a=\min\left(H,\left\lfloor\frac{x}{a}\right\rfloor\right).
]

This lets us compute both the number of bars with cost at most (x) and their total cost without enumerating every pair.

The remaining difficulty is summing over all possible (a). The values (\lfloor x/a\rfloor) stay constant over long intervals once (a) becomes large. We can process the small (a) values individually and the large values in groups having the same quotient. This is the standard floor-division grouping technique and gives (O(\sqrt{x})) work for one query.

There is an even cleaner way to use this function. Let (F(x)) be the total cost of every legal bar whose cost is at most (x). We can find the smallest (x) for which (F(x)>B). Then every bar cheaper than (x) can be bought, while (x) is the cost of the next distinct group of bars. The remaining money can buy some number of those (x)-cost bars. This avoids a second binary search over the number of bars.

The brute-force method works because sorting gives exactly the cheapest possible prefix. It fails because the multiplication table is too large. The observation that all bars with the same area form a threshold group lets us count and sum entire groups at once, reducing the problem to floor-division sums and one binary search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(WH\log(WH))) | (O(WH)) | Too slow |
| Threshold grouping | (O(\sqrt B\log B)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Let (W) and (H) be the box dimensions and (B) be the savings. Every legal chocolate bar corresponds to one ordered pair ((a,b)) with (1\le a\le W) and (1\le b\le H), and its cost is (ab).
2. Compute the total cost of every possible bar:

[
T=\frac{W(W+1)}2\cdot\frac{H(H+1)}2.
]

If (B\ge T), every possible bar can be purchased, so the answer is simply (WH).

1. Define `stats(x)` to return two values. The first is the number of legal bars with area at most (x). The second is the sum of their areas.

For a fixed width (a), the number of usable heights is

[
t=\min(H,\lfloor x/a\rfloor).
]

The number contributed by this width is (t), while its cost contribution is

a\frac{t(t+1)}2.
]

1. Handle all widths for which (t=H) together. This happens when

[
a\le \left\lfloor\frac{x}{H}\right\rfloor.
]

If this range contains (m) widths, it contributes (mH) bars and

[
\frac{m(m+1)}2\frac{H(H+1)}2
]

total cost.

Grouping this first range matters because it may contain a huge number of widths, while every one of them has exactly the same number of valid heights.

1. For the remaining small widths, iterate directly up to (\lfloor\sqrt{x}\rfloor). There are only (O(\sqrt{x})) such values.
2. Once (a>\sqrt{x}), the quotient (\lfloor x/a\rfloor) is small. For a current (a), let (q=\lfloor x/a\rfloor). The same quotient remains valid through

[
r=\left\lfloor\frac{x}{q}\right\rfloor.
]

So all widths from (a) through (r) can be processed together. Their contribution to the count is the interval length multiplied by (q), and their cost contribution is

[
\left(\sum_{i=a}^{r}i\right)\frac{q(q+1)}2.
]

1. We now know how to compute (F(x)), the total cost of all bars with area at most (x). Since (F(x)) is nondecreasing, binary search for the smallest (x) such that

[
F(x)>B.
]

The search upper bound can be taken as (\min(WH,B+1)). If not all bars are affordable, the first area that exceeds the budget cannot need to be larger than (B+1).

1. Let this first value be (x). Compute the number and total cost of all bars with area at most (x-1). Every one of these bars can be purchased.
2. Let `remaining = B - cost`. Every remaining candidate in the next cost group costs exactly (x), so we can purchase

[
\left\lfloor\frac{\text{remaining}}x\right\rfloor
]

more bars.

1. Add this number to the count of bars with cost below (x). The result is the maximum possible number of gifts.

### Why it works

The invariant is that, for any threshold (x), `stats(x)` describes exactly the complete set of legal bars whose cost is at most (x). Since every bar has the same benefit, an optimal solution always consists of the cheapest available bars. Let (x) be the smallest cost threshold whose complete group would make the budget insufficient. All bars with cost below (x) must be taken in an optimal solution, because replacing any one of them with a more expensive bar cannot improve the number of gifts. After taking them, every remaining candidate costs exactly (x), so taking as many of them as the remaining budget permits is optimal. The threshold grouping only changes how these bars are counted, not which bars are represented.

## Python Solution

```python
import sys
from math import isqrt

input = sys.stdin.readline

def solve_case(W, H, B):
    total_bars = W * H
    total_cost = (W * (W + 1) // 2) * (H * (H + 1) // 2)

    if B >= total_cost:
        return total_bars

    if B <= 0:
        return 0

    def stats(x):
        if x <= 0:
            return 0, 0

        # For a <= m, every height 1..H is affordable.
        m = min(W, x // H)

        count = m * H
        cost = (
            m * (m + 1) // 2
            * (H * (H + 1) // 2)
        )

        left = m + 1
        if left > W or left > x:
            return count, cost

        root = isqrt(x)

        # Small widths are processed individually.
        right = min(W, root)

        for a in range(left, right + 1):
            t = min(H, x // a)
            if t <= 0:
                break

            count += t
            cost += a * t * (t + 1) // 2

        left = max(left, root + 1)

        # For a > sqrt(x), floor(x / a) is constant on intervals.
        while left <= W and left <= x:
            q = x // left
            if q <= 0:
                break

            right = min(W, x // q)
            t = min(H, q)

            length = right - left + 1
            count += length * t

            sum_a = (left + right) * length // 2
            cost += sum_a * t * (t + 1) // 2

            left = right + 1

        return count, cost

    # If not all bars fit, the first area whose complete group
    # makes the total exceed B is at most B + 1.
    lo = 1
    hi = min(total_bars if total_bars < B + 1 else B + 1,
             W * H)

    while lo < hi:
        mid = (lo + hi) // 2
        _, cost = stats(mid)

        if cost > B:
            hi = mid
        else:
            lo = mid + 1

    x = lo

    count_before, cost_before = stats(x - 1)
    remaining = B - cost_before

    return count_before + remaining // x

def solve(data):
    values = list(map(int, data.split()))
    if not values:
        return ""

    W, H, B = values[:3]
    return str(solve_case(W, H, B))

def main():
    data = sys.stdin.buffer.read()
    sys.stdout.write(solve(data) + "\n")

if __name__ == "__main__":
    main()
```

The first part of `solve_case` handles the case where the entire multiplication table is affordable. The product of the triangular sums gives the exact total area of all possible ordered dimension pairs.

`stats(x)` is the central routine. The expression `m = min(W, x // H)` identifies widths for which every height up to `H` fits under the threshold. Computing their contribution with arithmetic-series formulas prevents a potentially enormous loop.

The direct loop covers widths up to `sqrt(x)`. After that point, `x // a` is small and changes only at relatively sparse positions. The expression `right = min(W, x // q)` finds the maximal interval on which the quotient remains `q`. The sum of all widths in that interval is computed with the standard arithmetic-series formula.

The binary search uses the total cost rather than the number of bars. This is the subtle part of the implementation. If `x` is the first value for which the cost of all bars with area at most `x` exceeds the budget, then `x` must correspond to an actual bar cost. Otherwise `F(x)` would equal `F(x-1)`, contradicting minimality. Consequently, every unselected bar at the boundary costs exactly `x`, so integer division by `x` gives exactly how many can still be afforded.

Python integers have arbitrary precision, so products such as `W * (W + 1) * H * (H + 1)` do not overflow. The formulas use integer division only after multiplication, avoiding floating-point rounding. The search is inclusive on both sides, and evaluating `stats(x - 1)` is what separates the cheaper bars from the boundary group.

## Worked Examples

Because the supplied Codeforces page exposes the statement title and contest metadata but not the statement's sample I/O in its text representation, the following traces use two concrete instances of the same problem. The original UCF problem is the source of the formulation.

### Example 1

Consider a (2\times2) box with budget (5).

The four possible bars have areas (1,2,2,4). The cheapest three cost (1+2+2=5), so the answer is (3).

| Threshold (x) | Bars with cost (\le x) | Count | Total cost |
| --- | --- | --- | --- |
| 1 | (1\times1) | 1 | 1 |
| 2 | (1\times1,1\times2,2\times1) | 3 | 5 |
| 3 | same three bars | 3 | 5 |
| 4 | all four bars | 4 | 9 |

The binary search finds (x=4), because the cost through (3) is (5), while the cost through (4) is (9). The algorithm takes all three bars cheaper than (4), leaving zero budget for the final bar.

### Example 2

Consider a (3\times3) box with budget (10).

The areas are

[
1,2,3,2,4,6,3,6,9.
]

After sorting, they are

[
1,2,2,3,3,4,6,6,9.
]

| Threshold (x) | Count | Total cost |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 3 | 5 |
| 3 | 5 | 11 |
| 4 | 6 | 15 |

The first threshold whose complete group exceeds the budget is (x=3). All five bars with area at most (2) cost (5), leaving (5). Each of the next bars costs (3), so only one more can be bought. The answer is (4).

The trace demonstrates why we search for the first threshold whose cumulative cost exceeds the budget rather than simply looking for the largest threshold whose cumulative cost fits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\sqrt B\log B)) | Each threshold query uses floor-division grouping in (O(\sqrt B)), and binary search makes (O(\log B)) queries. |
| Space | (O(1)) | Only scalar variables are maintained. |

The algorithm never constructs the (W\times H) multiplication table. The threshold queries operate on arithmetic intervals, so the memory usage remains constant even when the number of possible chocolate bars is very large. The 3 second and 256 MB limits of the original contest make this asymptotic reduction necessary.

## Test Cases

The original statement is available as the UCF Local Contest 2018 problem set, where the problem appears under the name Chocolate Gifts. The following tests exercise the minimum dimensions, a large dimension range, equal-cost orientations, complete affordability, and the boundary where one additional bar becomes too expensive.

```
# helper: run solution on input string, return output string
import io

def run(inp: str) -> str:
    return solve(inp).strip()

# Minimum-size input
assert run("1 1 1\n") == "1", "minimum box and exact budget"

# Nothing is affordable
assert run("3 3 0\n") == "0", "zero budget"

# 2x2 costs are 1, 2, 2, 4
assert run("2 2 5\n") == "3", "equal-cost orientations"

# All bars are affordable
assert run("2 2 9\n") == "4", "entire multiplication table fits"

# Boundary case: 3x3 sorted costs are 1,2,2,3,3,4,6,6,9
assert run("3 3 10\n") == "4", "cannot afford the fifth cheapest bar"

# One-dimensional box, useful for checking arithmetic progression
assert run("1 5 15\n") == "5", "all bars in a 1x5 box"

# Large dimensions with tiny budget
assert run("1000000 1000000 1\n") == "1", "large dimensions, smallest possible budget"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `1` | Minimum-size instance and exact affordability |
| `3 3 0` | `0` | Boundary case where no positive-cost bar fits |
| `2 2 5` | `3` | Distinct orientations with equal cost |
| `2 2 9` | `4` | Complete affordability |
| `3 3 10` | `4` | Boundary between two cumulative cost groups |
| `1 5 15` | `5` | Arithmetic-series behavior for a one-dimensional box |
| `1000000 1000000 1` | `1` | Very large dimensions with a tiny budget |

## Edge Cases

For a square box, orientation still matters. On input `2 2 5`, the algorithm computes the costs (1,2,2,4). At threshold (2), `stats(2)` returns count (3) and cost (5). The next threshold is (4), whose cumulative cost is (9), so the answer remains (3). Both (1\times2) and (2\times1) are counted because they correspond to different widths in the outer sum.

For an empty budget, input `3 3 0` immediately returns `0`. The implementation checks `B <= 0` before starting the threshold search, so it never attempts to divide by a zero boundary cost or assume that a positive-cost bar can be selected.

When every possible bar fits, the input `2 2 9` is handled before the binary search. The total cost is

[
\frac{2\cdot3}{2}\frac{2\cdot3}{2}=9,
]

which equals the budget, so all (2\cdot2=4) bars are affordable. This early exit also prevents unnecessary threshold calculations when the answer is simply the total number of possible dimension pairs.

For the one-dimensional case `1 5 15`, the possible costs are (1,2,3,4,5), whose sum is (15). The complete-affordability check returns (5). This case is useful because the quotient-grouping code must still work when one dimension is exactly one and there is no two-dimensional structure to exploit.

For the large case `1000000 1000000 1`, the cheapest possible bar is (1\times1), costing exactly (1). The answer is consequently (1). The search never needs to enumerate the million-by-million grid. The threshold immediately lies near the smallest costs, and the grouped formulas represent the rest of the rectangle implicitly.
