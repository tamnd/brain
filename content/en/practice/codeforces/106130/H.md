---
title: "CF 106130H - \u6211\u4e0d\u5403\u6c34\u679c"
description: "We have an $n times n$ cake represented as a grid. A cell contains either no fruit (0) or a fruit (1). The piece that Xiao Z cuts must come from the top-left corner of the cake."
date: "2026-06-19T19:50:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106130
codeforces_index: "H"
codeforces_contest_name: "GDUT 2025 Monthly competition"
rating: 0
weight: 106130
solve_time_s: 53
verified: true
draft: false
---

[CF 106130H - \u6211\u4e0d\u5403\u6c34\u679c](https://codeforces.com/problemset/problem/106130/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an $n \times n$ cake represented as a grid. A cell contains either no fruit (`0`) or a fruit (`1`).

The piece that Xiao Z cuts must come from the top-left corner of the cake. Because cuts are only allowed along row and column boundaries, any such piece is a rectangle whose top-left corner is fixed at cell $(1,1)$. The rectangle is completely determined by choosing its bottom row and right column.

The task is to find the largest-area rectangle of the form

$$[1..r] \times [1..c]$$

such that every cell inside it is `0`.

The grid size is at most 1000, so there are up to one million cells. Reading the input already costs $O(n^2)$, which means an accepted solution should stay around that complexity. Any approach that examines all possible rectangles independently would be far too expensive.

Several edge cases are easy to miss.

If the top-left cell itself contains a fruit, then no valid rectangle exists because every candidate rectangle must include that cell.

Example:

```
1
1
```

The answer is:

```
0
```

A careless solution that assumes the rectangle always has positive area would fail here.

Another subtle case is when a fruit appears far to the right in an early row.

```
3
0 0 1
0 0 0
0 0 0
```

The largest valid rectangle is only width 2, even though later rows are completely empty. The answer is $3 \times 2 = 6$. Any method that considers rows independently without remembering restrictions imposed by previous rows would incorrectly return 9.

A third case is when the limiting row appears in the middle.

```
4
0 0 0 0
0 1 0 0
0 0 0 0
0 0 0 0
```

The second row blocks every rectangle wider than 1. The largest valid rectangle is the entire first column, area 4. The restriction created by one row affects all rows below it.

## Approaches

The most direct brute-force idea is to try every possible bottom row $r$ and right column $c$, then check whether every cell inside the rectangle $[1..r]\times[1..c]$ is zero.

There are $n^2$ possible rectangles. Checking one rectangle may require examining up to $n^2$ cells, giving $O(n^4)$ time. With $n=1000$, this is completely infeasible.

The key observation is that every valid rectangle is anchored at the top-left corner.

For each row, we only care about how far we can extend from column 1 before encountering the first fruit.

Let

$$width_i$$

be the number of consecutive zeros starting from column 1 in row $i$.

For example, if a row is

```
0 0 0 1 0
```

then `width = 3`.

Suppose we want a rectangle ending at row $r$. Its width cannot exceed the smallest allowed width among the first $r$ rows, because every row inside the rectangle must remain fruit-free.

So for every row $r$,

$$\text{max valid width}
=
\min(width_1,\ldots,width_r).$$

The best rectangle ending at row $r$ has area

$$r \times \min(width_1,\ldots,width_r).$$

We can process rows from top to bottom while maintaining the running minimum width. This reduces the problem to a single pass over the grid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^4)$ | $O(1)$ | Too slow |
| Optimal | $O(n^2)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

1. Read the grid.
2. For each row, compute `width`, the number of consecutive zeros starting from the first column.

Stop scanning the row as soon as the first `1` appears, because anything to its right can never belong to a valid top-left rectangle.
3. Maintain `min_width`, the minimum `width` seen so far among all processed rows.

This value represents the largest width that every row from 1 to the current row can support simultaneously.
4. After processing row `i`, compute

$$area = (i+1) \times min\_width$$

because the rectangle spans the first `i+1` rows and can be at most `min_width` columns wide.
5. Update the answer with the maximum area encountered.
6. Output the answer.

### Why it works

For a rectangle ending at row $r$, every row from 1 through $r$ must be fruit-free within the chosen width. Row $k$ allows at most `width_k` columns. A width larger than the minimum of these values would include a fruit in at least one row, making the rectangle invalid.

Conversely, choosing exactly the minimum width guarantees that every cell in the rectangle belongs to the zero-prefix of its row, so the entire rectangle is fruit-free.

Thus the largest valid rectangle ending at row $r$ has width

$$\min(width_1,\ldots,width_r),$$

and checking all rows considers every possible bottom boundary. The maximum area among them is the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    min_width = n
    ans = 0

    for i in range(n):
        row = list(map(int, input().split()))

        width = 0
        while width < n and row[width] == 0:
            width += 1

        min_width = min(min_width, width)
        ans = max(ans, (i + 1) * min_width)

    print(ans)

solve()
```

The first task for each row is finding how many consecutive zeros appear from the left edge. Once the first fruit is reached, extending farther right is impossible for any valid top-left rectangle, so nothing beyond that position affects the answer.

`min_width` stores the tightest width restriction among all rows processed so far. When a new row is added, the rectangle can only be as wide as the smallest prefix width seen anywhere above it.

The area calculation uses `(i + 1)` because rows are processed with zero-based indexing in the loop, while the rectangle height is the actual number of rows included.

No special handling is required when the top-left cell contains a fruit. In that case the first row has `width = 0`, causing `min_width` to become zero and all computed areas to remain zero.

## Worked Examples

### Example 1

Input:

```
3
0 0 0
0 0 1
1 1 1
```

Row prefix widths are:

```
3, 2, 0
```

| Row | width | min_width | Area | Best |
| --- | --- | --- | --- | --- |
| 1 | 3 | 3 | 3 | 3 |
| 2 | 2 | 2 | 4 | 4 |
| 3 | 0 | 0 | 0 | 4 |

The answer is:

```
4
```

The best rectangle uses the first two rows and first two columns.

### Example 2

Input:

```
3
1 0 0
1 0 1
1 1 1
```

Row prefix widths are:

```
0, 0, 0
```

| Row | width | min_width | Area | Best |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 | 0 |
| 3 | 0 | 0 | 0 | 0 |

The answer is:

```
0
```

Since the top-left cell already contains a fruit, no valid rectangle exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Each grid cell is read once, and each row is scanned only until its first fruit |
| Space | $O(1)$ extra | Only a few variables are maintained besides the current row |

The input itself contains $n^2$ values, so $O(n^2)$ time is essentially optimal. With $n \le 1000$, processing one million cells is easily manageable.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())

    min_width = n
    ans = 0

    for i in range(n):
        row = list(map(int, input().split()))

        width = 0
        while width < n and row[width] == 0:
            width += 1

        min_width = min(min_width, width)
        ans = max(ans, (i + 1) * min_width)

    return str(ans)

# sample-like cases
assert run("3\n0 0 0\n0 0 1\n1 1 1\n") == "4"
assert run("3\n1 0 0\n1 0 1\n1 1 1\n") == "0"

# minimum size, empty cell
assert run("1\n0\n") == "1"

# minimum size, fruit
assert run("1\n1\n") == "0"

# all zeros
assert run("3\n0 0 0\n0 0 0\n0 0 0\n") == "9"

# limiting row in the middle
assert run("4\n0 0 0 0\n0 1 0 0\n0 0 0 0\n0 0 0 0\n") == "4"

# width shrinks gradually
assert run("4\n0 0 0 0\n0 0 0 1\n0 0 1 1\n0 1 1 1\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `1` | Smallest valid instance |
| `1 / 1` | `0` | Top-left fruit |
| All zeros | `9` | Entire grid can be taken |
| Restriction in second row | `4` | Running minimum width logic |
| Gradually shrinking widths | `6` | Maximum may occur before the last row |

## Edge Cases

### Top-left cell contains a fruit

Input:

```
2
1 0
0 0
```

The first row has `width = 0`. Immediately `min_width` becomes 0.

| Row | width | min_width | Area |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 0 |
| 2 | 2 | 0 | 0 |

The algorithm outputs 0, which is correct because every valid rectangle must contain the fruit at $(1,1)$.

### Early row limits all later rows

Input:

```
3
0 1 0
0 0 0
0 0 0
```

Widths are:

```
1, 3, 3
```

Processing gives:

| Row | width | min_width | Area |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 3 | 1 | 2 |
| 3 | 3 | 1 | 3 |

The answer is 3. Even though the last two rows allow width 3, the fruit in the first row permanently restricts every valid top-left rectangle to width 1.

### Best rectangle does not end at the last row

Input:

```
4
0 0 0
0 0 0
0 0 0
0 1 1
```

Widths are:

```
3, 3, 3, 1
```

| Row | width | min_width | Area |
| --- | --- | --- | --- |
| 1 | 3 | 3 | 3 |
| 2 | 3 | 3 | 6 |
| 3 | 3 | 3 | 9 |
| 4 | 1 | 1 | 4 |

The maximum area is 9 at row 3. The algorithm checks every possible bottom row, so it correctly finds a rectangle that ends before the final row.
