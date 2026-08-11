---
title: "CF 102399C - \u0418\u0432\u0430\u043d\u0443\u0448\u043a\u0430-\u0434\u0443\u0440\u0430\u0447\u043e\u043a \u0438 \u0442\u0435\u043e\u0440\u0438\u044f \u0432\u0435\u0440\u043e\u044f\u0442\u043d\u043e\u0441\u0442\u0435\u0439"
description: "We have an (n times m) rectangular grid whose cells are colored with two colors. Two cells are neighbors when they share a side. A coloring is valid if every cell has at most one neighbor with the same color."
date: "2026-08-11T15:52:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102399
codeforces_index: "C"
codeforces_contest_name: "2019 \u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432, \u043b\u0438\u0433\u0430 A"
rating: 0
weight: 102399
solve_time_s: 134
verified: true
draft: false
---

[CF 102399C - \u0418\u0432\u0430\u043d\u0443\u0448\u043a\u0430-\u0434\u0443\u0440\u0430\u0447\u043e\u043a \u0438 \u0442\u0435\u043e\u0440\u0438\u044f \u0432\u0435\u0440\u043e\u044f\u0442\u043d\u043e\u0441\u0442\u0435\u0439](https://codeforces.com/problemset/problem/102399/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an (n \times m) rectangular grid whose cells are colored with two colors. Two cells are neighbors when they share a side. A coloring is valid if every cell has at most one neighbor with the same color.

The task is to count all valid colorings of the grid and print the result modulo (10^9+7). The grid dimensions can each reach (100,000), so the number of cells can reach (10^{10}). Any method that explicitly processes every possible coloring is hopeless, and even a method whose state depends exponentially on the smaller dimension cannot handle a (10^5 \times 10^5) grid. We need to reduce the problem to a constant amount of work per dimension.

There are two small cases that expose mistakes in the reasoning. For a (1\times1) grid, both colors are valid, so the answer is (2). A method that assumes every cell has four neighbors, or blindly applies a recurrence starting from (n=2), can get this wrong. For a (1\times3) grid, the valid strings are all binary strings without three equal consecutive cells, giving (6) colorings. A careless approach that only forbids adjacent equal cells would count only the two alternating strings and miss colorings such as (001).

For a (2\times2) grid, the answer is (6). The four cells cannot all have the same color, and a coloring with three cells of one color and one of the other is also invalid because one of the majority-color cells gets two equal neighbors. This is a useful check because it distinguishes the actual condition, at most one equal neighbor, from the stronger and incorrect condition that all neighbors must have the opposite color.

## Approaches

The direct approach is to enumerate every one of the (2^{nm}) colorings. For each coloring, we can inspect every cell and count its equal-colored side neighbors. This is correct because every possible coloring is considered and checked against exactly the required condition. Its worst-case work is (O(nm,2^{nm})). With (n=m=100,000), there are (10^{10}) cells and (2^{10^{10}}) possible colorings, so even writing down the search space is impossible.

The useful observation is to stop thinking about colors directly and instead mark every pair of adjacent cells that has the same color. Because a cell may have at most one equal-colored neighbor, these marked edges form a matching: two marked edges can never share a cell.

Now consider the orientation of such an edge. Suppose two horizontally adjacent cells have the same color. Each endpoint has already used its only allowed equal-colored neighbor, so the cells immediately above them, when they exist, must have the opposite color. The same argument propagates the horizontal equal-colored pair through every row. Thus a single horizontal equal-colored edge forces the whole coloring to have horizontal equal-colored edges only. A vertical equal-colored edge cannot occur anywhere in such a coloring, because a vertical edge would propagate in the perpendicular direction and eventually conflict with the forced horizontal structure. The same argument works with horizontal and vertical exchanged. This structural observation is the key to the entire solution.

Consequently, every valid coloring belongs to at least one of two families. In the first family there are no vertical equal-colored edges, so every column alternates vertically. In the second family there are no horizontal equal-colored edges, so every row alternates horizontally. The only colorings belonging to both families are the two checkerboard colorings.

Consider the first family. Since every column alternates vertically, the entire grid is determined by its first row. The first row can be any binary string in which three consecutive cells are never equal. Once the first row is chosen, all remaining rows are forced by vertical alternation. If the first cell's color is fixed, let (f_k) be the number of valid strings of length (k). The first two values are (f_1=1) and (f_2=2). For (k\ge3), after fixing the first cell, the final block can extend the previous string by one cell or by two equal cells, giving

[
f_k=f_{k-1}+f_{k-2}.
]

The first cell itself has two possible colors, so this family contains (2f_m) grids.

By symmetry, the family with no horizontal equal-colored edges contains (2f_n) grids. Their intersection consists exactly of the two checkerboards. Inclusion-exclusion gives

2(f_n+f_m-1).
]

This is the standard characterization used for the problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nm,2^{nm})) | (O(nm)) | Too slow |
| Fibonacci recurrence | (O(\max(n,m))) | (O(\max(n,m))) | Accepted |

## Algorithm Walkthrough

1. Read (n) and (m), and let (L=\max(n,m)). We only need Fibonacci-like values up to the larger dimension.
2. Define (f_1=1) and (f_2=2). For every (i) from (3) through (L), compute
[
f_i=f_{i-1}+f_{i-2}\pmod{10^9+7}.
]
This counts binary strings of length (i) with a fixed first color and with no three consecutive equal colors.
3. The colorings with no vertical equal-colored edges are counted by (2f_m). The factor (2) chooses the color of the first cell, after which vertical alternation determines the rest of each column.
4. By rotating the argument by (90^\circ), the colorings with no horizontal equal-colored edges are counted by (2f_n).
5. The two families overlap in exactly the two checkerboard colorings. Subtract these two duplicated colorings once, obtaining
[
2f_n+2f_m-2.
]
6. Print
[
2(f_n+f_m-1)\pmod{10^9+7}.
]

The invariant behind the counting is that every valid coloring with an equal-colored adjacent pair has only one possible orientation for such pairs. Once that orientation is chosen, the perpendicular direction must alternate, and the remaining freedom is exactly a one-dimensional binary string with no three equal consecutive colors. The two possible orientations are disjoint except for the two checkerboards, so the inclusion-exclusion formula counts every valid coloring exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n, m = map(int, input().split())
    limit = max(n, m)

    if limit == 1:
        f1 = 1
    else:
        f1, f2 = 1, 2

        for _ in range(3, limit + 1):
            f1, f2 = f2, (f1 + f2) % MOD

    if n == 1:
        fn = 1
    elif n == 2:
        fn = 2
    else:
        a, b = 1, 2
        for _ in range(3, n + 1):
            a, b = b, (a + b) % MOD
        fn = b

    if m == 1:
        fm = 1
    elif m == 2:
        fm = 2
    else:
        a, b = 1, 2
        for _ in range(3, m + 1):
            a, b = b, (a + b) % MOD
        fm = b

    print((2 * (fn + fm - 1)) % MOD)

if __name__ == "__main__":
    solve()
```

The recurrence can be computed only once up to (\max(n,m)), which is simpler and avoids doing two separate loops. The implementation above keeps the boundary cases explicit, but a compact array-based implementation is also possible.

The values (f_1=1) and (f_2=2) are not the usual Fibonacci initialization (1,1). They have a direct combinatorial meaning here. With a fixed first color, there is one string of length one, while there are two strings of length two: the second cell may have either color.

Python integers do not overflow, but every recurrence value is reduced modulo (10^9+7) anyway. The subtraction of (1) happens before the final multiplication, and adding the modulus is unnecessary in Python because the final `% MOD` handles a negative intermediate value correctly.

A more efficient implementation can store all values in an array and directly read (f_n) and (f_m). The rolling version uses only constant auxiliary memory and is sufficient when the two dimensions are processed separately.

## Worked Examples

For the provided sample (n=2,m=3), the recurrence gives (f_1=1), (f_2=2), and (f_3=3).

| Step | Dimension | (f_{i-2}) | (f_{i-1}) | (f_i) |
| --- | --- | --- | --- | --- |
| Initial | 1 |  | 1 |  |
| Initial | 2 | 1 | 2 |  |
| Recurrence | 3 | 1 | 2 | 3 |

The two families contain (2f_2=4) and (2f_3=6) colorings. Both contain the two checkerboards, so the union has (4+6-2=8) colorings.

For a second example, take (n=1,m=3). The recurrence values are again (f_1=1,f_2=2,f_3=3).

| Step | Dimension | (f_{i-2}) | (f_{i-1}) | (f_i) |
| --- | --- | --- | --- | --- |
| Initial | 1 |  | 1 |  |
| Initial | 2 | 1 | 2 |  |
| Recurrence | 3 | 1 | 2 | 3 |

The formula gives

[
2(f_1+f_3-1)=2(1+3-1)=6.
]

Those six strings are exactly the binary strings of length three excluding (000) and (111). This confirms that the two-dimensional argument also handles the degenerate one-row grid correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\max(n,m))) | We compute the recurrence only up to the larger dimension. |
| Space | (O(1)) | Only the last two recurrence values are needed. |

The largest dimension is only (100,000), so the algorithm performs roughly (100,000) simple recurrence steps. This is easily compatible with the stated constraints, while any exponential dependence on the number of cells is completely infeasible.

## Test Cases

```python
import sys
import io

MOD = 10**9 + 7

def solve_data(data: str) -> str:
    n, m = map(int, data.split())

    limit = max(n, m)
    f = [0] * (limit + 1)

    f[1] = 1
    if limit >= 2:
        f[2] = 2

    for i in range(3, limit + 1):
        f[i] = (f[i - 1] + f[i - 2]) % MOD

    answer = 2 * (f[n] + f[m] - 1) % MOD
    return str(answer)

def run(inp: str) -> str:
    return solve_data(inp).strip()

# Provided sample
assert run("2 3\n") == "8", "sample 1"

# Minimum-size grid
assert run("1 1\n") == "2", "single cell has two colors"

# One-dimensional boundary case
assert run("1 3\n") == "6", "binary strings of length 3 without 000 or 111"

# Equal dimensions, catches symmetric counting mistakes
assert run("2 2\n") == "6", "2x2 grid"

# Large boundary case
def expected(n: int, m: int) -> str:
    limit = max(n, m)
    a, b = 1, 2

    if limit == 1:
        fn = fm = 1
    else:
        values = [0, 1, 2]
        for i in range(3, limit + 1):
            values.append((values[-1] + values[-2]) % MOD)
        fn = values[n]
        fm = values[m]

    return str(2 * (fn + fm - 1) % MOD)

assert run("100000 100000\n") == expected(100000, 100000), \
    "maximum equal dimensions"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `2` | Minimum grid and dimension-one initialization |
| `1 3` | `6` | One-dimensional boundary and no-three-equal recurrence |
| `2 2` | `6` | Symmetry and overlap of the two orientation families |
| `100000 100000` | Computed modulo (10^9+7) | Maximum dimensions and modular recurrence |

## Edge Cases

For `1 1`, the recurrence has only (f_1=1). The formula gives

[
2(1+1-1)=2.
]

There is only one cell, so either of the two colors produces a valid coloring. The absence of neighbors is handled naturally by the formula.

For `1 3`, the grid is just a binary string. A valid string cannot contain three equal consecutive cells because the middle cell would have two equal neighbors. The six valid strings are exactly the strings counted by (2f_3=6). The formula gives the same result:

[
2(f_1+f_3-1)=2(1+3-1)=6.
]

For `2 2`, (f_2=2), so

[
2(f_2+f_2-1)=2(2+2-1)=6.
]

The six valid colorings include the two checkerboards and the four colorings having one pair of equal adjacent cells. This case confirms that the two orientation families must overlap by exactly two colorings rather than being simply added.

For `2 3`, the recurrence gives (f_2=2) and (f_3=3). The horizontal-edge family contributes (2f_2=4), the vertical-edge family contributes (2f_3=6), and the two checkerboards occur in both families. The final count is (4+6-2=8), matching the sample.

For `100000 100000`, no special mathematical case is needed. The recurrence is evaluated modulo (10^9+7) at every step, so the values remain small, and the answer is obtained from the two identical values (f_{100000}). The running time remains linear in (100,000), not in the (10^{10}) cells of the grid.
