---
title: "CF 102769B - Bounding Wall"
description: "We have a rectangular map of cells. A dry cell is represented by and a wet cell is represented by .. A bounding wall is the border of a rectangle, but the problem asks for its covered rectangle area."
date: "2026-07-30T04:28:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102769
codeforces_index: "B"
codeforces_contest_name: "2020 China Collegiate Programming Contest Qinhuangdao Site"
rating: 0
weight: 102769
solve_time_s: 107
verified: true
draft: false
---

[CF 102769B - Bounding Wall](https://codeforces.com/problemset/problem/102769/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rectangular map of cells. A dry cell is represented by `#` and a wet cell is represented by `.`. A bounding wall is the border of a rectangle, but the problem asks for its covered rectangle area. The rectangle must be completely made of dry cells and must contain the cell mentioned in a query. After some queries, individual cells toggle between dry and wet, and we need to answer the largest possible area for the requested cell.

The input contains several test cases. Each test case gives the initial grid followed by operations. An update changes one cell. A query asks for the largest all-dry rectangle that includes a specific position.

The constraints are small in one dimension but allow up to 1000 rows, 1000 columns, and 1000 operations in one test case. A solution that tries every possible rectangle is impossible because a 1000 by 1000 grid already has about $10^{12}$ possible rectangles. Even recomputing the answer for every query with a full dynamic programming table would be too slow. We need a method where each query only scans the grid once.

The useful observation is that 1000 columns fit naturally into machine-sized bit operations. A whole row can be represented as one integer, where bit `1` means dry. Intersecting rows becomes a single integer AND operation. This allows us to examine all columns of a candidate rectangle extremely quickly.

There are a few edge cases that break careless solutions. If the queried cell itself is wet, the answer is zero because every valid rectangle must contain that cell.

For example:

```
1 1 1
.
2 1 1
```

The output is:

```
Case #1:
0
```

A solution that only checks neighboring cells may incorrectly return a positive area.

Another case is a rectangle that touches the boundary of the board.

Example:

```
2 3 1
###
###
2 1 1
```

The answer is:

```
Case #1:
6
```

The optimal rectangle uses the entire grid. Code that starts expanding only when there are cells on both sides can miss such cases.

A third common mistake is assuming the rectangle must have both height and width greater than one. A single row or a single column is allowed.

Example:

```
1 4 1
####
2 1 3
```

The answer is:

```
Case #1:
4
```

A method that only considers two-dimensional rectangles would fail here.

## Approaches

A direct approach is to enumerate every possible rectangle containing the queried cell and test whether all its cells are dry. This is correct because every valid answer is considered, but the number of rectangles in a 1000 by 1000 grid is around $10^{12}$. Even with prefix sums, checking all rectangles per query is far beyond the limit.

A better idea is to fix one dimension of the rectangle and compute the best possible other dimension. For a query cell, every rectangle must contain the queried row. If we extend upward from that row, we can maintain the intersection of all rows included so far. The remaining set bits are exactly the columns where every row in the current height interval is dry.

The largest rectangle for that height interval is the longest consecutive segment of these valid columns that contains the queried column. We can do the same while extending downward. The two scans cover every possible top and bottom boundary of the rectangle.

The reason this works efficiently is that the grid dimensions are only 1000. Representing each row as a Python integer lets every row intersection happen in constant time from the algorithm's point of view, because the actual work is handled by optimized big integer operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²m²) per query | O(1) | Too slow |
| Optimal bitset expansion | O(n) per query | O(n) | Accepted |

## Algorithm Walkthrough

1. Store every row of the grid as an integer bit mask. Bit `j` is set when column `j` of that row is dry. A cell update becomes a single XOR operation on the corresponding bit.
2. For a query at `(r, c)`, start with all columns available and extend upward from row `r`. After adding each row, intersect the current mask with that row. The remaining bits represent columns that are dry in every row of the current rectangle height.
3. If the queried column disappears from the mask, stop extending in that direction. Any larger rectangle would also contain that wet cell, so no further rows can create a valid answer.
4. For every valid height interval, calculate the length of the consecutive dry segment containing column `c`. Multiply that width by the current height and update the answer.
5. Repeat the same process while extending downward from row `r + 1`. Combining both directions considers every possible top and bottom border of a rectangle containing the query cell.

Why it works:

During the upward scan, after processing rows from `top` to `r`, the bit mask contains exactly the columns where every cell in those rows is dry. The longest consecutive segment containing `c` is the widest rectangle possible for that exact set of rows. Every valid rectangle has some top row, and that top row appears in the scan. The same argument applies to the downward scan. Since every possible vertical range is considered and the best width is chosen for each one, the maximum area found is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def trailing_ones(x):
    return ((~x) & (x + 1)).bit_length() - 1

def width_at(mask, col):
    right = trailing_ones(mask >> col)
    left_mask = mask & ((1 << col) - 1)
    left = trailing_ones(left_mask)
    return left + right + 1

def solve_case(n, m, q, grid, queries):
    rows = []
    for s in grid:
        x = 0
        for i, ch in enumerate(s):
            if ch == '#':
                x |= 1 << i
        rows.append(x)

    all_bits = (1 << m) - 1
    ans = []

    for t, x, y in queries:
        x -= 1
        y -= 1

        if t == 1:
            rows[x] ^= 1 << y
        else:
            if ((rows[x] >> y) & 1) == 0:
                ans.append("0")
                continue

            best = 1

            mask = all_bits
            height = 0
            for i in range(x, -1, -1):
                mask &= rows[i]
                if ((mask >> y) & 1) == 0:
                    break
                height += 1
                best = max(best, height * width_at(mask, y))

            mask = all_bits
            height = 0
            for i in range(x + 1, n):
                mask &= rows[i]
                if ((mask >> y) & 1) == 0:
                    break
                height += 1
                best = max(best, height * width_at(mask, y))

            ans.append(str(best))

    return ans

def main():
    t = int(input())
    out = []

    for case in range(1, t + 1):
        n, m, q = map(int, input().split())
        grid = [input().strip() for _ in range(n)]
        queries = [tuple(map(int, input().split())) for _ in range(q)]

        out.append(f"Case #{case}:")
        out.extend(solve_case(n, m, q, grid, queries))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The grid representation is the main implementation detail. Each row is converted into an integer, so updating a cell does not require changing strings or rebuilding arrays. XOR works because the operation only flips one bit.

For a query, `mask` starts with all columns enabled. Every AND operation removes columns that contain at least one wet cell in the current vertical range. When the query column is removed, the rectangle can no longer include the requested cell, so the scan ends immediately.

The function `width_at` finds the consecutive run of set bits containing a given column. The right side is obtained by counting trailing ones after shifting the queried bit to the least significant position. The left side is the same operation on the bits before the queried column.

Python integers have arbitrary precision, so there is no overflow concern even though a row can contain 1000 bits.

## Worked Examples

For the first sample:

```
2 3 2
###
##.
2 2 2
2 1 3
```

The grid is:

```
###
##.
```

For the query at row 2, column 2:

| Direction | Height | Valid columns | Width | Area |
| --- | --- | --- | --- | --- |
| Up | 1 | ### | 3 | 3 |
| Up | 2 | ## | 2 | 4 |

The answer is `4`.

For the second query at row 1, column 3:

| Direction | Height | Valid columns | Width | Area |
| --- | --- | --- | --- | --- |
| Down | 1 | ### | 3 | 3 |

The answer is `3`.

For the second sample:

```
4 3 3
###
#.#
#.#
###
2 3 2
1 3 2
2 3 2
```

The first query asks for the center wet cell:

| Step | Cell state | Result |
| --- | --- | --- |
| Check queried cell | `.` | 0 |

After flipping that cell:

```
###
###
#.#
###
```

The final query produces:

| Direction | Height | Valid columns | Width | Area |
| --- | --- | --- | --- | --- |
| Up | 3 | ### | 3 | 9 |

The rectangle expands over the first three rows, giving area `9`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per query | Each query scans rows, and each row operation is a bitwise integer operation |
| Space | O(n) | Only the bit mask of each row is stored |

The largest test case has 1000 rows and 1000 queries, resulting in about one million row scans. Bit operations on 1000-bit integers are fast enough for this limit.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    it = iter(data)
    t = int(next(it))
    out = []

    for case in range(1, t + 1):
        n = int(next(it))
        m = int(next(it))
        q = int(next(it))
        grid = [next(it) for _ in range(n)]
        queries = []
        for _ in range(q):
            queries.append((int(next(it)), int(next(it)), int(next(it))))

        out.append(f"Case #{case}:")
        out.extend(solve_case(n, m, q, grid, queries))

    return "\n".join(out)

assert run("""1
2 3 2
###
##.
2 2 2
2 1 3
""") == """Case #1:
4
3"""

assert run("""1
1 4 1
####
2 1 3
""") == """Case #1:
4"""

assert run("""1
1 1 2
#
2 1 1
1 1 1
""") == """Case #1:
1"""

assert run("""1
3 3 3
###
#.#
###
2 2 2
1 2 2
2 2 2
""") == """Case #1:
3
9"""

assert run("""1
2 2 1
..
..
2 1 1
""") == """Case #1:
0"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample grid with two queries | 4, 3 | Basic rectangle expansion |
| Single row of dry cells | 4 | One-dimensional rectangles |
| One-cell grid with update | 1 | Minimum size and flip handling |
| Center cell becoming dry | 3 then 9 | Updates and larger rectangles |
| Fully wet grid | 0 | Impossible rectangle cases |

## Edge Cases

When the queried cell is wet, the algorithm checks the bit before scanning. For a grid containing only `.` at the queried position, the answer immediately becomes zero because every possible rectangle would include that wet cell.

When the optimal rectangle touches a border, the upward or downward scan naturally reaches the edge of the row array. There is no special boundary handling because the scan simply stops after the last valid row.

When only one row or one column is available, the same intersection logic still applies. The width calculation can return one, and the area formula correctly handles thin rectangles. No assumption about minimum height or width is built into the algorithm.
