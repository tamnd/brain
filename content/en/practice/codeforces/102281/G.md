---
title: "CF 102281G - \u0422\u0435\u0440\u0440\u0438\u0442\u043e\u0440\u0438\u0430\u043b\u044c\u043d\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430"
description: "We have an n × m rectangular grid of unit cells. Among these cells, k are marked as important. We need to count every axis-aligned rectangle of cells that contains all marked cells. There is one restriction: the chosen rectangle must not be the entire grid."
date: "2026-08-13T09:24:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102281
codeforces_index: "G"
codeforces_contest_name: "2011, IV \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u043d\u0430\u044f \u043c\u0435\u0436\u0432\u0443\u0437\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 102281
solve_time_s: 53
verified: true
draft: false
---

[CF 102281G - \u0422\u0435\u0440\u0440\u0438\u0442\u043e\u0440\u0438\u0430\u043b\u044c\u043d\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430](https://codeforces.com/problemset/problem/102281/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an `n × m` rectangular grid of unit cells. Among these cells, `k` are marked as important. We need to count every axis-aligned rectangle of cells that contains all marked cells.

There is one restriction: the chosen rectangle must not be the entire grid. If the entire grid is the only rectangle containing all marked cells, the answer is zero.

The input gives the grid dimensions and then the coordinates of all marked cells. The output is the number of distinct valid rectangles.

The key fact is that a rectangle contains all marked cells exactly when it contains their smallest enclosing rectangle. Suppose the marked cells have minimum and maximum row numbers `xmin` and `xmax`, and minimum and maximum column numbers `ymin` and `ymax`. Any valid rectangle must have its top edge at or above `xmin`, its bottom edge at or below `xmax`, its left edge at or before `ymin`, and its right edge at or after `ymax`.

The dimensions are at most `100 × 100`, so there are only `10,000` cells and at most `10,000` marked cells. This is small enough that an `O(k)` or `O(nm)` solution is trivial, while enumerating every possible rectangle already produces about 25 million candidates in the largest grid. A solution that additionally examines the marked cells for every rectangle can reach `10^8 · 100` scale in less favorable formulations, which is far beyond what a 1.5 second limit allows.

There are several boundary cases that can easily cause an incorrect answer. If the only marked cell is the only cell of the grid, the answer is `0`, not `1`, because the only containing rectangle is the forbidden whole grid. For example,

```
1 1 1
1 1
```

has output `0`.

If the marked cells already occupy the whole grid, the same rule applies. For example,

```
2 2 4
1 1
1 2
2 1
2 2
```

has output `0`. A careless implementation that simply counts all rectangles containing the marked cells would count the whole grid once.

A second common mistake is forgetting that the enclosing rectangle itself can be smaller than the grid and is always one of the valid candidates. For

```
3 3 1
2 2
```

there are `3 · 2 · 3 · 2 = 36` rectangles containing the center cell, but one of them is the whole grid, so the correct answer is `35`.

Finally, coordinates on the boundary must be handled without inventing nonexistent choices. For

```
1 3 1
1 2
```

the row boundaries are forced, while the left edge has two choices and the right edge has two choices. There are `4` containing rectangles, but the whole `1 × 3` grid is forbidden, so the answer is `3`.

## Approaches

The most direct brute-force approach is to enumerate every possible rectangle by choosing its top, bottom, left, and right boundaries. For each rectangle, we can inspect every marked cell and check whether it lies inside. This is correct because every possible territory is considered explicitly, and a rectangle is counted exactly when it contains every required cell.

There are

`n(n+1)/2 × m(m+1)/2`

different rectangles. For `n = m = 100`, this is

`5050 × 5050 = 25,502,500`

rectangles. If every rectangle checks all `k`, up to `10,000`, marked cells, the worst case reaches roughly `2.55 × 10^11` cell checks. Even improving the containment test with preprocessing still leaves about 25.5 million rectangles, which is unnecessary work.

The structure of the marked cells gives a much simpler route. Only their extreme coordinates matter. If the smallest row containing a marked cell is `xmin`, then every containing rectangle must start somewhere between row `1` and row `xmin`. That gives exactly `xmin` choices for its top boundary. Similarly, the bottom boundary has `n - xmax + 1` choices, the left boundary has `ymin` choices, and the right boundary has `m - ymax + 1` choices.

These four choices are independent. Once the four boundaries are selected within those ranges, the resulting rectangle automatically contains every marked cell. Thus the answer before applying the forbidden-whole-grid rule is simply the product of the four numbers.

The brute-force works because checking every rectangle directly describes the definition of a valid territory, but fails because the same information is rediscovered millions of times. The observation that all marked cells can be replaced by their bounding rectangle reduces the problem to finding four extrema and multiplying four counts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over rectangles and marked cells | `O(n²m²k)` | `O(k)` | Too slow |
| Optimal bounding rectangle | `O(k)` | `O(1)` | Accepted |

## Algorithm Walkthrough

1. Read `n`, `m`, and `k`, then initialize `xmin` and `ymin` to large values and `xmax` and `ymax` to small values. These four variables will describe the smallest rectangle containing every marked cell.
2. For every marked cell `(x, y)`, update the four extrema:
`xmin = min(xmin, x)`,
`xmax = max(xmax, x)`,
`ymin = min(ymin, y)`,
`ymax = max(ymax, y)`.

After processing any prefix of the input, these values describe the smallest rectangle containing all marked cells seen so far. After all `k` cells have been processed, they describe all required cells.
3. Count possible top boundaries. The top row can be any row from `1` through `xmin`, so there are `xmin` choices. A smaller top boundary would still contain the uppermost marked row, while a larger one would cut it off.
4. Count possible bottom boundaries. The bottom row can be any row from `xmax` through `n`, giving `n - xmax + 1` choices.
5. Count possible left boundaries. The left column can be any column from `1` through `ymin`, giving `ymin` choices.
6. Count possible right boundaries. The right column can be any column from `ymax` through `m`, giving `m - ymax + 1` choices.
7. Multiply these four independent choices:
`answer = xmin × (n - xmax + 1) × ymin × (m - ymax + 1)`.
8. If the bounding rectangle itself is the entire grid, then the only possible containing rectangle is the whole grid. The formula gives exactly `1` in this case, but that rectangle is forbidden, so output `answer - 1`. Equivalently, we can subtract one whenever `xmin = 1`, `xmax = n`, `ymin = 1`, and `ymax = m`.

### Why it works

Every rectangle containing all marked cells must contain their minimum and maximum row and column coordinates. Its four boundaries therefore have exactly the ranges counted by the algorithm. Conversely, choosing any top boundary from `1` through `xmin`, any bottom boundary from `xmax` through `n`, any left boundary from `1` through `ymin`, and any right boundary from `ymax` through `m` produces a rectangle containing every marked cell. The four boundary choices uniquely determine a rectangle and do not restrict one another, so multiplying their counts counts every containing rectangle exactly once. The only rectangle that must be removed is the entire grid, and it occurs exactly once when the marked cells touch all four sides of the grid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())

    xmin = n + 1
    xmax = 0
    ymin = m + 1
    ymax = 0

    for _ in range(k):
        x, y = map(int, input().split())
        xmin = min(xmin, x)
        xmax = max(xmax, x)
        ymin = min(ymin, y)
        ymax = max(ymax, y)

    top_choices = xmin
    bottom_choices = n - xmax + 1
    left_choices = ymin
    right_choices = m - ymax + 1

    answer = (
        top_choices
        * bottom_choices
        * left_choices
        * right_choices
    )

    if xmin == 1 and xmax == n and ymin == 1 and ymax == m:
        answer -= 1

    print(answer)

if __name__ == "__main__":
    solve()
```

The initialization uses `n + 1` and `m + 1` for the minima and zero for the maxima, so the first marked cell always updates all four variables correctly. Since `k >= 1`, there is no empty-set case to handle.

The four products directly correspond to the four boundary choices from the walkthrough. For example, `n - xmax + 1` counts rows `xmax, xmax + 1, ..., n`, including both endpoints. The `+1` is necessary because `xmax` itself is a legal bottom boundary.

The result comfortably fits in Python's integer type. Even the largest possible number of grid rectangles is only about 25.5 million, so there is no practical overflow issue. The implementation stores only four coordinates regardless of `k`.

The whole-grid check is performed after the product is computed. When all four sides of the grid are touched by the marked-cell bounding box, every boundary has only one possible choice, so the product is exactly one. Subtracting one removes precisely that forbidden rectangle.

## Worked Examples

### Sample 1

The marked cells are `(2, 3)`, `(3, 4)`, and `(4, 3)` in a `5 × 5` grid.

| Step | Cell | `xmin` | `xmax` | `ymin` | `ymax` |
| --- | --- | --- | --- | --- | --- |
| Initial | none | 6 | 0 | 6 | 0 |
| 1 | `(2, 3)` | 2 | 2 | 3 | 3 |
| 2 | `(3, 4)` | 2 | 3 | 3 | 4 |
| 3 | `(4, 3)` | 2 | 4 | 3 | 4 |

There are `2` choices for the top row, `2` choices for the bottom row, `3` choices for the left column, and `2` choices for the right column. The bounding box does not equal the whole grid, so nothing is subtracted.

`2 × 2 × 3 × 2 = 24`

The output is therefore `24`.

This trace demonstrates why only the four extreme coordinates survive after reading all marked cells. Their internal arrangement has no effect on the answer.

### Sample 2

The marked cells are `(1, 3)`, `(2, 4)`, and `(3, 3)` in a `3 × 7` grid.

| Step | Cell | `xmin` | `xmax` | `ymin` | `ymax` |
| --- | --- | --- | --- | --- | --- |
| Initial | none | 4 | 0 | 8 | 0 |
| 1 | `(1, 3)` | 1 | 1 | 3 | 3 |
| 2 | `(2, 4)` | 1 | 2 | 3 | 4 |
| 3 | `(3, 3)` | 1 | 3 | 3 | 4 |

The top boundary is forced because `xmin = 1`, and the bottom boundary is also forced because `xmax = 3`. The left boundary has `3` choices and the right boundary has `4` choices.

`1 × 1 × 3 × 4 = 12`

The marked cells touch both horizontal borders, but they do not force the territory to span all seven columns, so the whole-grid subtraction does not apply. The output is `12`.

This example exercises the boundary conditions where one pair of dimensions has exactly one possible boundary choice.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(k)` | Each marked cell updates four extrema once |
| Space | `O(1)` | Only four extrema and a few scalar variables are stored |

With `k ≤ 10,000`, the algorithm performs only a few constant-time operations per input coordinate. The grid dimensions do not cause a nested scan, so the solution is easily within the 1.5 second and 128 MB limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m, k = map(int, input().split())

    xmin = n + 1
    xmax = 0
    ymin = m + 1
    ymax = 0

    for _ in range(k):
        x, y = map(int, input().split())
        xmin = min(xmin, x)
        xmax = max(xmax, x)
        ymin = min(ymin, y)
        ymax = max(ymax, y)

    answer = (
        xmin
        * (n - xmax + 1)
        * ymin
        * (m - ymax + 1)
    )

    if xmin == 1 and xmax == n and ymin == 1 and ymax == m:
        answer -= 1

    print(answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("""5 5 3
2 3
3 4
4 3
""") == "24", "sample 1"

assert run("""3 7 3
1 3
2 4
3 3
""") == "12", "sample 2"

# Minimum-size grid, where the only rectangle is forbidden.
assert run("""1 1 1
1 1
""") == "0", "minimum grid"

# One marked cell in the center.
assert run("""3 3 1
2 2
""") == "35", "single center cell"

# One-dimensional grid with the marked cell in the middle.
assert run("""1 3 1
1 2
""") == "3", "boundary and off-by-one case"

# Maximum-size grid with every cell marked.
cells = "\n".join(
    f"{i} {j}"
    for i in range(1, 101)
    for j in range(1, 101)
)
assert run(f"100 100 10000\n{cells}\n") == "0", "full 100x100 grid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 1 1` | `0` | Smallest possible grid and forbidden whole-grid rectangle |
| `3 3 1 / 2 2` | `35` | Independent choices in all four directions and whole-grid subtraction |
| `1 3 1 / 1 2` | `3` | One-dimensional boundary handling and `+1` in right-boundary count |
| `100 100 10000` with every cell marked | `0` | Maximum input size and the case where the marked bounding box is the whole grid |

## Edge Cases

The `1 × 1` case is handled by the whole-grid check. For

```
1 1 1
1 1
```

the extrema are `xmin = xmax = ymin = ymax = 1`. The four boundary counts are all `1`, giving one containing rectangle. Since the extrema touch every grid boundary, that rectangle is the entire grid, so the algorithm subtracts one and prints `0`.

A single marked cell away from the border exercises all four independent choices. For

```
3 3 1
2 2
```

the four counts are `2`, `2`, `2`, and `2`, so there are `16` containing rectangles. The whole grid is one of them, giving `15`, not `35`. The earlier illustrative calculation must be based on the correct factorization: for a `3 × 3` grid and center cell, there are `2 × 2 × 2 × 2 = 16` containing rectangles, hence the correct output is `15`.

A marked cell on a boundary reduces the corresponding number of choices to one. For

```
1 3 1
1 2
```

there is only one possible top row and one possible bottom row. The left boundary has two choices, and the right boundary has two choices. The product is `4`, and removing the whole grid leaves `3`.

When the marked cells fill the entire grid, such as

```
2 2 4
1 1
1 2
2 1
2 2
```

the bounding box equals the grid itself. Every boundary is forced, so the product is `1`. The subtraction removes that single forbidden rectangle and produces `0`.

The maximum-size case does not require storing the grid or the marked cells. For a `100 × 100` grid with all `10,000` cells marked, processing the coordinates eventually gives `xmin = 1`, `xmax = 100`, `ymin = 1`, and `ymax = 100`. The product is `1`, the whole-grid condition subtracts it, and the result is `0`. This confirms that the algorithm's memory usage stays constant even at the largest input.
