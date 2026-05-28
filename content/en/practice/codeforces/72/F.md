---
title: "CF 72F - Oil"
description: "We have an n × m grid. Some entire rows are empty, some entire columns are empty, and every empty cell belongs to at least one of those empty rows or empty columns. All remaining cells contain oil."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 72
codeforces_index: "F"
codeforces_contest_name: "Unknown Language Round 2"
rating: 1900
weight: 72
solve_time_s: 103
verified: true
draft: false
---

[CF 72F - Oil](https://codeforces.com/problemset/problem/72/F)

**Rating:** 1900  
**Tags:** *special, greedy, math  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an `n × m` grid. Some entire rows are empty, some entire columns are empty, and every empty cell belongs to at least one of those empty rows or empty columns.

All remaining cells contain oil. If we drill a well in one oil cell, we can reach every oil cell connected through edge-adjacent oil cells. The task is to compute how many connected oil regions exist.

Another way to think about the grid is this:

A cell contains oil if and only if:

```
its row is not empty
and
its column is not empty
```

So after removing the forbidden rows and forbidden columns, the remaining oil cells form several rectangular blocks. We need to count how many connected components those blocks create.

The limits are very small, only up to `100 × 100`. Even a straightforward BFS or DFS over the entire grid is completely safe. A full traversal touches at most `10^4` cells, which is tiny for a 2 second limit.

The tricky part is not performance, it is understanding the structure correctly.

Consider this example:

```
n = 5, m = 5
empty rows: 3
empty cols: none
```

The grid splits into:

```
rows 1-2
row 3 removed
rows 4-5
```

So there are exactly 2 connected oil regions.

Now consider:

```
n = 5, m = 5
empty rows: 3
empty cols: 3
```

The removed row and removed column form a cross. The remaining oil cells split into 4 disconnected rectangles, so the answer is 4.

A careless implementation might incorrectly think the answer is:

```
(#non-empty row segments) + (#non-empty column segments)
```

but the correct structure is multiplicative, not additive.

Another easy mistake appears when every row or every column is empty.

Example:

```
2 3
2 1 2
0
```

All rows are removed, so there are no oil cells at all. The answer is `0`, not `1`.

Similarly:

```
3 3
0
0
```

No rows or columns are removed, so the entire grid is one connected component. The answer is `1`.

## Approaches

The most direct solution is to explicitly build the grid.

We mark each row that is empty and each column that is empty. Then a cell `(i, j)` contains oil exactly when:

```
row i is not empty
and
column j is not empty
```

Once we construct this boolean grid, the problem becomes a standard connected components problem on a 2D grid. We run BFS or DFS from every unvisited oil cell and count how many traversals we start.

This brute-force method is fully correct because connectivity is exactly the usual four-directional grid connectivity. Every DFS discovers one entire oil region.

Its complexity is:

```
O(n * m)
```

because each cell is processed a constant number of times.

With `n, m ≤ 100`, this already passes comfortably.

There is also a structural observation hiding underneath.

Suppose we remove several rows. The remaining rows split into contiguous row segments. The same happens for columns.

For example:

```
rows:    valid valid removed valid valid removed valid
segments:   [1]                [2]                [3]
```

Every connected oil component is exactly:

```
(one row segment) × (one column segment)
```

because inside such a rectangle all cells exist and are connected, while removed rows or columns prevent crossing between rectangles.

So the answer equals:

```
(number of non-empty row segments)
*
(number of non-empty column segments)
```

This avoids graph traversal entirely.

The brute-force solution works because the grid is small, but the key insight is that deleting full rows and columns partitions the grid into independent rectangles. Once we recognize that structure, the problem reduces to counting contiguous surviving intervals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS/BFS | O(nm) | O(nm) | Accepted |
| Optimal Segment Counting | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the sets of empty rows and empty columns.

We need constant-time checks for whether a row or column is removed, so sets or boolean arrays are ideal.
2. Count how many contiguous segments of non-empty rows exist.

We scan rows from `1` to `n`.

Whenever a row is non-empty and either:

```
it is the first row
or
the previous row is empty
```

we start a new row segment.

Consecutive non-empty rows belong to the same connected vertical block.
3. Count how many contiguous segments of non-empty columns exist.

This is identical to the row process.
4. Multiply the two counts.

Each row segment combines with each column segment to form one connected rectangle of oil cells.
5. Handle the degenerate case automatically.

If there are no surviving rows or no surviving columns, one of the counts becomes `0`, so the final answer is also `0`.

### Why it works

Removing rows creates horizontal barriers that cannot be crossed. Removing columns creates vertical barriers that cannot be crossed.

After all removals, every surviving oil cell belongs to exactly one pair:

```
(row segment, column segment)
```

Inside such a pair, all cells form a complete rectangle, so any two cells are connected through ordinary grid movement.

Two cells belonging to different row segments cannot connect because an empty row separates them. Two cells belonging to different column segments cannot connect because an empty column separates them.

So connected components are in one-to-one correspondence with:

```
row segments × column segments
```

and multiplying the counts gives the exact number of oil regions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    row_data = list(map(int, input().split()))
    t = row_data[0]
    empty_rows = set(row_data[1:])

    col_data = list(map(int, input().split()))
    s = col_data[0]
    empty_cols = set(col_data[1:])

    row_segments = 0

    for i in range(1, n + 1):
        if i not in empty_rows:
            if i == 1 or (i - 1) in empty_rows:
                row_segments += 1

    col_segments = 0

    for j in range(1, m + 1):
        if j not in empty_cols:
            if j == 1 or (j - 1) in empty_cols:
                col_segments += 1

    print(row_segments * col_segments)

solve()
```

The implementation mirrors the mathematical structure directly.

We first store empty rows and columns in sets. Membership checks like:

```
i in empty_rows
```

run in constant expected time.

The row scan counts beginnings of contiguous valid intervals. A new segment starts only when the current row survives but the previous row does not.

For example:

```
rows: valid valid empty valid
```

The first valid row starts one segment, and the row after the empty row starts another.

The column logic is identical.

The multiplication step works because every row interval intersects every column interval in one connected rectangle.

A subtle detail is handling completely empty grids. Suppose all rows are removed. Then no row satisfies the condition for starting a segment, so:

```
row_segments = 0
```

The final product becomes zero automatically. No special case is needed.

Another common source of off-by-one errors is indexing. The input uses 1-based row and column numbering, so the loops intentionally iterate from `1` through `n` and `m`.

## Worked Examples

### Example 1

Input:

```
2 3
1 2
1 2
```

Rows:

```
1 = valid
2 = empty
```

Columns:

```
1 = valid
2 = empty
3 = valid
```

### Row scan

| Row | Empty? | Starts new segment? | row_segments |
| --- | --- | --- | --- |
| 1 | No | Yes | 1 |
| 2 | Yes | No | 1 |

### Column scan

| Column | Empty? | Starts new segment? | col_segments |
| --- | --- | --- | --- |
| 1 | No | Yes | 1 |
| 2 | Yes | No | 1 |
| 3 | No | Yes | 2 |

Final answer:

```
1 × 2 = 2
```

The remaining oil cells form two disconnected rectangles:

```
(1,1)
(1,3)
```

They cannot connect because column 2 is entirely empty.

### Example 2

Input:

```
5 5
1 3
1 3
```

Rows:

```
1-2 valid
3 empty
4-5 valid
```

Columns:

```
1-2 valid
3 empty
4-5 valid
```

### Row scan

| Row | Empty? | Starts new segment? | row_segments |
| --- | --- | --- | --- |
| 1 | No | Yes | 1 |
| 2 | No | No | 1 |
| 3 | Yes | No | 1 |
| 4 | No | Yes | 2 |
| 5 | No | No | 2 |

### Column scan

| Column | Empty? | Starts new segment? | col_segments |
| --- | --- | --- | --- |
| 1 | No | Yes | 1 |
| 2 | No | No | 1 |
| 3 | Yes | No | 1 |
| 4 | No | Yes | 2 |
| 5 | No | No | 2 |

Final answer:

```
2 × 2 = 4
```

The empty row and empty column divide the board into four disconnected quadrants.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | One linear scan over rows and columns |
| Space | O(n + m) | Sets storing removed rows and columns |

The limits are extremely small, so even a full graph traversal would pass easily. This optimized solution is still useful because it captures the actual structure of the problem instead of treating it as a generic connectivity task.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    row_data = list(map(int, input().split()))
    empty_rows = set(row_data[1:])

    col_data = list(map(int, input().split()))
    empty_cols = set(col_data[1:])

    row_segments = 0

    for i in range(1, n + 1):
        if i not in empty_rows:
            if i == 1 or (i - 1) in empty_rows:
                row_segments += 1

    col_segments = 0

    for j in range(1, m + 1):
        if j not in empty_cols:
            if j == 1 or (j - 1) in empty_cols:
                col_segments += 1

    print(row_segments * col_segments)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run("2 3\n1 2\n1 2\n") == "2", "sample 1"

# minimum grid, all oil
assert run("1 1\n0\n0\n") == "1", "single oil cell"

# completely empty grid
assert run("2 2\n2 1 2\n0\n") == "0", "all rows removed"

# cross split into four components
assert run("5 5\n1 3\n1 3\n") == "4", "four quadrants"

# alternating empty columns
assert run("3 5\n0\n2 2 4\n") == "3", "three vertical strips"

# large contiguous surviving block
assert run("100 100\n1 50\n1 50\n") == "4", "large grid split once"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1×1` with no removals | `1` | Smallest non-empty grid |
| All rows removed | `0` | No oil cells exist |
| Single removed row and column | `4` | Multiplicative component structure |
| Alternating empty columns | `3` | Multiple column segments |
| `100×100` split once | `4` | Large boundary-sized input |

## Edge Cases

Consider the case where every row is empty:

```
2 3
2 1 2
0
```

During the row scan:

```
row 1 -> empty
row 2 -> empty
```

No row segment is created, so:

```
row_segments = 0
```

Columns still form one segment, but:

```
0 × 1 = 0
```

This is correct because no oil cells remain.

Now consider no removals at all:

```
3 3
0
0
```

All rows belong to one contiguous row segment, and all columns belong to one contiguous column segment.

So:

```
1 × 1 = 1
```

The entire grid is connected.

Finally, consider separated valid intervals:

```
7 1
2 3 6
0
```

Surviving rows are:

```
1-2, 4-5, 7
```

That creates three row segments.

There is one column segment because the only column survives.

So the answer becomes:

```
3 × 1 = 3
```

The algorithm detects each new segment exactly when a surviving row follows a removed row, which correctly handles isolated rows and multiple gaps.
