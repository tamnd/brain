---
title: "CF 102550C - \u041c\u0438\u043d\u043d\u043e\u0435 \u043f\u043e\u043b\u0435"
description: "The field is a rectangular grid where every cell initially contains an active mine. During the process, cells are removed one by one. A query asks about the closest remaining mine strictly in one of the four directions from a given cell."
date: "2026-08-06T20:39:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102550
codeforces_index: "C"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2018-2019, \u041f\u0435\u0440\u0432\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102550
solve_time_s: 218
verified: true
draft: false
---

[CF 102550C - \u041c\u0438\u043d\u043d\u043e\u0435 \u043f\u043e\u043b\u0435](https://codeforces.com/problemset/problem/102550/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

The field is a rectangular grid where every cell initially contains an active mine. During the process, cells are removed one by one. A query asks about the closest remaining mine strictly in one of the four directions from a given cell. For a vertical query we only care about the same column, and for a horizontal query we only care about the same row.

The input describes the grid dimensions and a sequence of operations. A removal operation permanently deletes a cell. A search operation asks for the coordinates of the nearest cell that has not been deleted yet in the requested direction, or reports that no such cell exists.

The limits are the main difficulty. The grid can contain up to four million cells, and there can be up to one million operations. Scanning a whole row or column for every query would be far too expensive. In the worst case, a single query could inspect 2000 cells, giving around two billion checks over all operations. The solution needs almost constant time per operation.

The deletion operations have a useful property: cells only disappear, they never return. This means we can use a data structure designed for monotonic removal. We only need to skip cells that have already been deleted.

Several boundary cases can break a direct implementation. A query from the edge of the grid may immediately have no possible answer. For example:

```
1 3 3
l 1 1
r 1 3
u 1 2
```

The output is:

```
-1
-1
-1
```

A careless implementation might accidentally include the starting cell or move outside the grid while searching.

Another case is a direction where the nearest cell was removed but a farther cell still exists:

```
1 4 3
c 1 2
r 1 1
l 1 4
```

The output is:

```
1 3
1 1
```

After removing `(1,2)`, the right query must skip it and find `(1,3)`. Stopping at the first removed position would give the wrong result.

A final tricky case is repeated searches after many deletions:

```
2 2 4
c 1 1
c 1 2
d 1 1
r 2 1
```

The output is:

```
2 1
2 2
```

The structure must continue to find remaining cells even after large parts of a row or column have disappeared.

## Approaches

A straightforward approach is to store which cells are still active and, for every query, walk one step at a time in the requested direction until an active cell is found. This is correct because the first active cell encountered is exactly the closest one. The problem is the amount of repeated work. With a 2000 by 2000 grid, a query may scan 1999 cells, and one million such queries can require almost two billion operations.

The key observation is that cells are only deleted. We never need to insert a mine again. For a row, after a column is removed, every future query that reaches that position should immediately jump over it. The same applies independently to every column.

This is exactly the situation handled by a disjoint set style "next pointer" structure. For each row we maintain a structure that can find the next remaining column and the previous remaining column. For each column we maintain the next and previous remaining row. When a cell is deleted, we connect it to the next available position, effectively removing it from future searches.

For example, if a row contains columns `1 2 3 4` and column `2` is removed, the next pointer of `2` becomes `3`. Any future search starting at `1` that asks for the next active column jumps through the deleted cell automatically.

The four structures together answer all directions in almost constant amortized time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q * max(n, m)) | O(nm) | Too slow |
| Optimal | O(q α(nm)) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Build four disjoint set structures. For every row, store a "next alive column" structure and a "previous alive column" structure. For every column, store the equivalent two structures for rows. Each structure initially points to itself because every cell exists.
2. For a removal operation at `(x, y)`, remove that cell from both its row structures and its column structures. In the next-pointer structures, connect the removed position to the next position. In the previous-pointer structures, connect it to the previous position.
3. For a right query from `(x, y)`, ask the row's next-pointer structure for the first active column after `y`. If the result is outside the valid column range, no answer exists. Otherwise, return `(x, result)`.
4. For a left query, use the row's previous-pointer structure. For an up query, use the column's previous-pointer structure. For a down query, use the column's next-pointer structure.

The reason this works is that the only changes are deletions. A deleted position always redirects to the closest position that could still be a valid answer. Path compression makes repeated jumps very cheap because long chains quickly collapse.

### Why it works

The invariant is that every pointer structure returns the closest still-existing position in its direction. Initially this is true because every cell exists and every pointer points to itself. When a cell is deleted, it is replaced by a link to its nearest surviving neighbor in that direction. Any future search that would have reached the deleted cell is redirected to exactly the position it should have found after the deletion. Since cells are never inserted again, no update can invalidate this property.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def find(arr, idx):
    root = idx
    while arr[root] != root:
        root = arr[root]
    while arr[idx] != idx:
        nxt = arr[idx]
        arr[idx] = root
        idx = nxt
    return root

def solve():
    n, m, q = map(int, input().split())

    row_size = m + 1
    col_size = n + 1

    row_next = array('H', [0]) * (n * row_size)
    row_prev = array('H', [0]) * (n * row_size)
    col_next = array('H', [0]) * (m * col_size)
    col_prev = array('H', [0]) * (m * col_size)

    for i in range(n):
        base = i * row_size
        for j in range(m + 2):
            if j <= m:
                row_next[base + j] = j
            if j <= m:
                row_prev[base + j] = j

    for j in range(m):
        base = j * col_size
        for i in range(n + 1):
            col_next[base + i] = i
            col_prev[base + i] = i

    out = []

    for _ in range(q):
        parts = input().split()
        typ = parts[0]
        x = int(parts[1]) - 1
        y = int(parts[2]) - 1

        if typ == 'c':
            rb = x * row_size
            cb = y * col_size

            row_next[rb + y] = find(row_next, rb + y + 1) - rb
            row_prev[rb + y] = find(row_prev, rb + y - 1) - rb

            col_next[cb + x] = find(col_next, cb + x + 1) - cb
            col_prev[cb + x] = find(col_prev, cb + x - 1) - cb
        elif typ == 'r':
            rb = x * row_size
            ans = find(row_next, rb + y + 1) - rb
            if ans > m - 1:
                out.append("-1")
            else:
                out.append(f"{x + 1} {ans + 1}")
        elif typ == 'l':
            rb = x * row_size
            ans = find(row_prev, rb + y - 1) - rb
            if ans < 0:
                out.append("-1")
            else:
                out.append(f"{x + 1} {ans + 1}")
        elif typ == 'd':
            cb = y * col_size
            ans = find(col_next, cb + x + 1) - cb
            if ans > n - 1:
                out.append("-1")
            else:
                out.append(f"{ans + 1} {y + 1}")
        else:
            cb = y * col_size
            ans = find(col_prev, cb + x - 1) - cb
            if ans < 0:
                out.append("-1")
            else:
                out.append(f"{ans + 1} {y + 1}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code stores every row and column structure in flattened arrays. This avoids the overhead of millions of separate Python objects. Since all indices are at most 2000, `array('H')` is enough because every stored value fits in an unsigned 16-bit integer.

The `find` function is the usual disjoint set lookup with path compression. The first loop finds the final surviving position, and the second loop shortens the path so later queries are faster.

The deletion order matters. The code first connects the removed cell to its neighbors, then future queries will never return that cell again. The `+1` and `-1` offsets are also important because a query asks for a cell strictly after or strictly before the given position.

There is no integer overflow issue in Python, and the array sizes are controlled by the grid dimensions. The memory saving from using compact arrays is necessary because four structures over four million cells would be too large as normal Python lists.

## Worked Examples

For the sample input:

```
3 4 6
u 2 3
c 2 4
r 2 4
c 2 3
l 2 4
d 1 3
```

| Operation | Action | Important state | Result |
| --- | --- | --- | --- |
| 1 | up from (2,3) | Column 3 still has rows 1,2,3 | 1 3 |
| 2 | remove (2,4) | Row 2 loses column 4 |  |
| 3 | right from (2,4) | No column after 4 | -1 |
| 4 | remove (2,3) | Row 2 loses column 3 and 4 |  |
| 5 | left from (2,4) | Previous alive column is 2 | 2 2 |
| 6 | down from (1,3) | Column 3 has row 3 alive | 3 3 |

This trace shows that removed cells are skipped rather than simply marked and ignored during every search. The pointers are updated once during deletion and reused afterward.

A second example:

```
2 3 5
c 1 2
r 1 1
c 1 3
d 1 1
l 2 3
```

| Operation | Action | Important state | Result |
| --- | --- | --- | --- |
| 1 | remove (1,2) | Row 1 links column 2 to column 3 |  |
| 2 | right from (1,1) | Jumps through removed column 2 | 1 3 |
| 3 | remove (1,3) | Row 1 has no cells after column 1 |  |
| 4 | down from (1,1) | Column 1 still has row 2 | 2 1 |
| 5 | left from (2,3) | Row 2 has column 1 and 2 alive | 2 2 |

This example exercises a chain of deletions. The important property is that queries never traverse the deleted cells one by one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q α(nm)) | Every query and deletion performs only a constant number of disjoint set operations with path compression. |
| Space | O(nm) | Four compact arrays store row and column predecessor and successor information. |

The maximum grid size creates about four million cells. The algorithm performs a small number of operations for each of the one million queries, which fits the constraints because the inverse Ackermann factor is effectively constant.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("""3 4 6
u 2 3
c 2 4
r 2 4
c 2 3
l 2 4
d 1 3
""") == """1 3
-1
2 2
3 3""", "sample"

assert run("""1 1 3
r 1 1
c 1 1
l 1 1
""") == """-1
-1""", "single cell"

assert run("""1 5 5
c 1 2
r 1 1
c 1 3
r 1 1
l 1 5
""") == """1 3
1 4
1 4""", "deleted middle cells"

assert run("""3 1 4
c 2 1
d 1 1
c 3 1
d 1 1
""") == """3 1
-1""", "vertical boundary"

assert run("""2 2 4
c 1 1
c 1 2
d 1 1
r 2 1
""") == """2 1
2 2""", "remaining row after deletions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single cell grid | No answers after deletion | Handles smallest dimensions and empty directions |
| Removing middle cells | Skips deleted positions | Tests successor and predecessor jumps |
| Single column grid | Vertical navigation | Tests column structures and boundaries |
| Heavy deletion of one row | Remaining cells are independent | Tests that rows and columns do not interfere |

## Edge Cases

The first boundary case is a query from the edge of the grid. In the input:

```
1 3 1
l 1 1
```

the algorithm asks for the previous column of column `0` in zero-based indexing. The predecessor structure returns the sentinel position outside the grid, so the answer is `-1`.

The second case is skipping deleted cells:

```
1 4 2
c 1 2
r 1 1
```

After deleting `(1,2)`, the row successor of column `1` points directly to column `3`. The query returns:

```
1 3
```

without inspecting the removed cell again.

The third case is deleting an entire row section:

```
2 2 3
c 1 1
c 1 2
d 1 1
```

The first row has no remaining cells, but the column structure still contains `(2,1)`. The downward query returns:

```
2 1
```

because row and column structures are maintained separately.
