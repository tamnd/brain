---
title: "CF 222B - Cosmic Tables"
description: "We have a matrix of integers and three kinds of operations applied to it repeatedly. One operation swaps two rows. Another swaps two columns. The third asks for the value currently visible at a specific row and column."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 222
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 137 (Div. 2)"
rating: 1300
weight: 222
solve_time_s: 93
verified: true
draft: false
---

[CF 222B - Cosmic Tables](https://codeforces.com/problemset/problem/222/B)

**Rating:** 1300  
**Tags:** data structures, implementation  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a matrix of integers and three kinds of operations applied to it repeatedly.

One operation swaps two rows. Another swaps two columns. The third asks for the value currently visible at a specific row and column.

The tricky part is that the matrix itself can be as large as one million cells, and the number of queries can reach five hundred thousand. A solution that physically rearranges entire rows or columns every time will spend far too much time moving data around.

The input first gives the dimensions of the table and the number of operations. Then comes the initial matrix. After that, each query is one of the following:

`r x y` swaps row `x` with row `y`.

`c x y` swaps column `x` with column `y`.

`g x y` asks for the value currently located at row `x`, column `y`.

For every `g` query, we print the requested number.

The constraints strongly shape the solution. The matrix size is at most `1000 × 1000`, which is manageable in memory. The real pressure comes from the `500000` operations. Even an `O(n)` or `O(m)` cost per swap becomes dangerous here.

Suppose we physically swap rows. A single row swap touches `m` elements. With `m = 1000` and `500000` operations, that becomes roughly `5 × 10^8` assignments in the worst case. Python will not survive that within the time limit.

We need each operation to run in constant time.

The non-obvious part is that row indices and column indices stop matching the original matrix after swaps begin. A careless implementation often mixes up “current row position” with “original row stored in memory”.

Consider this example:

```
2 2 3
1 2
3 4
r 1 2
g 1 1
g 2 1
```

After swapping rows 1 and 2, the visible matrix becomes:

```
3 4
1 2
```

The correct output is:

```
3
1
```

A buggy implementation that forgets to remap rows will still read from the original matrix and print `1` then `3`.

Column swaps create the same issue from the other direction.

```
2 3 2
1 2 3
4 5 6
c 1 3
g 1 1
```

The visible first row becomes:

```
3 2 1
```

The answer is `3`, not `1`.

Another subtle case is repeated swaps of the same rows or columns.

```
2 2 3
1 2
3 4
r 1 2
r 1 2
g 1 1
```

The two swaps cancel each other. The answer must return to `1`. A solution that mutates data incorrectly can drift away from the real state over time.

## Approaches

The brute-force idea is straightforward. Store the matrix exactly as it appears. For a row swap, exchange the two entire row arrays. For a column swap, iterate through every row and exchange the two column values. For a query, directly read the requested cell.

This works because each operation directly simulates the table state.

The problem is cost. A row swap takes `O(m)`, because we move all entries in those rows. A column swap takes `O(n)`. In the worst case, with `500000` swaps and dimensions near `1000`, the total work reaches hundreds of millions of operations.

The key observation is that swaps do not actually change the values themselves. They only change which original row or column currently appears at a given visible position.

Instead of moving data, we can keep two mapping arrays:

`row_pos[i]` tells us which original row currently occupies visible row `i`.

`col_pos[j]` tells us which original column currently occupies visible column `j`.

Initially:

```
row_pos[i] = i
col_pos[j] = j
```

When we swap rows, we only swap entries inside `row_pos`.

When we swap columns, we only swap entries inside `col_pos`.

For a query `(x, y)`, the actual value comes from:

```
matrix[row_pos[x]][col_pos[y]]
```

Now every operation becomes constant time.

The brute-force solution works because it maintains the exact visible matrix directly. The optimized solution works because the matrix contents never move logically, only the interpretation of indices changes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k × max(n, m)) | O(nm) | Too slow |
| Optimal | O(k + nm) | O(nm + n + m) | Accepted |

## Algorithm Walkthrough

1. Read the matrix into memory.

We keep the original matrix unchanged throughout the program.
2. Create a row mapping array.

`rows[i]` stores which original row currently appears at visible row `i`.

Initially, every row maps to itself.
3. Create a column mapping array.

`cols[j]` stores which original column currently appears at visible column `j`.

Initially, every column maps to itself.
4. Process each query one by one.

Each query modifies mappings or asks for a value.
5. For a row swap query `r x y`, swap `rows[x]` and `rows[y]`.

This updates the visible ordering instantly without touching the matrix itself.
6. For a column swap query `c x y`, swap `cols[x]` and `cols[y]`.

Again, only the interpretation of column positions changes.
7. For a get query `g x y`, compute:

```
original_row = rows[x]
original_col = cols[y]
```

Then output:

```
matrix[original_row][original_col]
```
8. Continue until all queries are processed.

### Why it works

The invariant is:

`rows[i]` always equals the original row currently displayed at visible row `i`, and `cols[j]` always equals the original column currently displayed at visible column `j`.

Initially this is true because nothing has been swapped.

A row swap exchanges two visible positions, so swapping the corresponding entries in `rows` preserves the invariant exactly. The same argument holds for column swaps.

A query asks for the value currently visible at `(x, y)`. By the invariant, the actual stored value comes from original row `rows[x]` and original column `cols[y]`. Reading that cell from the unchanged matrix always returns the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())

    table = [list(map(int, input().split())) for _ in range(n)]

    rows = list(range(n))
    cols = list(range(m))

    ans = []

    for _ in range(k):
        t, x, y = input().split()
        x = int(x) - 1
        y = int(y) - 1

        if t == 'r':
            rows[x], rows[y] = rows[y], rows[x]

        elif t == 'c':
            cols[x], cols[y] = cols[y], cols[x]

        else:
            ans.append(str(table[rows[x]][cols[y]]))

    sys.stdout.write("\n".join(ans))

solve()
```

The matrix is stored once and never modified afterward. This is the central implementation idea. All changes happen through the `rows` and `cols` mapping arrays.

The mappings use zero-based indexing because Python lists are zero-based. Every query subtracts one from the input indices immediately. Forgetting this conversion is the most common off-by-one mistake in this problem.

For a row swap, the code swaps only two integers inside `rows`. The same applies to columns. No matrix elements move physically.

The query operation looks slightly asymmetric at first glance:

```
table[rows[x]][cols[y]]
```

This works because `rows[x]` already tells us which original row currently occupies visible row `x`. The matrix itself still uses original coordinates.

The output is accumulated in a list and printed once at the end. Printing line by line up to half a million times can become slower in Python.

## Worked Examples

### Sample 1

Input:

```
3 3 5
1 2 3
4 5 6
7 8 9
g 3 2
r 3 2
c 2 3
g 2 2
g 3 2
```

Initial state:

```
rows = [0, 1, 2]
cols = [0, 1, 2]
```

| Query | rows | cols | Output |
| --- | --- | --- | --- |
| g 3 2 | [0,1,2] | [0,1,2] | 8 |
| r 3 2 | [0,2,1] | [0,1,2] |  |
| c 2 3 | [0,2,1] | [0,2,1] |  |
| g 2 2 | [0,2,1] | [0,2,1] | 9 |
| g 3 2 | [0,2,1] | [0,2,1] | 6 |

The trace shows how the matrix never changes physically. Only the interpretation arrays evolve. After swapping rows 2 and 3, visible row 2 now points to original row 3. After swapping columns 2 and 3, visible column 2 points to original column 3.

### Custom Example

Input:

```
2 3 4
1 2 3
4 5 6
c 1 3
r 1 2
g 1 1
g 2 3
```

Initial state:

```
rows = [0, 1]
cols = [0, 1, 2]
```

| Query | rows | cols | Output |
| --- | --- | --- | --- |
| c 1 3 | [0,1] | [2,1,0] |  |
| r 1 2 | [1,0] | [2,1,0] |  |
| g 1 1 | [1,0] | [2,1,0] | 6 |
| g 2 3 | [1,0] | [2,1,0] | 1 |

After the column swap, visible column 1 corresponds to original column 3. After the row swap, visible row 1 corresponds to original row 2. The query `(1,1)` correctly accesses original cell `(2,3)`, which contains `6`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm + k) | Reading the matrix costs O(nm), each query costs O(1) |
| Space | O(nm + n + m) | Matrix storage plus row and column mappings |

The matrix contains at most one million integers, which comfortably fits within memory limits. Each query performs only a few array accesses or swaps, so even five hundred thousand operations run efficiently within the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n, m, k = map(int, input().split())

        table = [list(map(int, input().split())) for _ in range(n)]

        rows = list(range(n))
        cols = list(range(m))

        ans = []

        for _ in range(k):
            t, x, y = input().split()
            x = int(x) - 1
            y = int(y) - 1

            if t == 'r':
                rows[x], rows[y] = rows[y], rows[x]

            elif t == 'c':
                cols[x], cols[y] = cols[y], cols[x]

            else:
                ans.append(str(table[rows[x]][cols[y]]))

        return "\n".join(ans)

    return solve()

# provided sample
assert run(
"""3 3 5
1 2 3
4 5 6
7 8 9
g 3 2
r 3 2
c 2 3
g 2 2
g 3 2
"""
) == "8\n9\n6", "sample 1"

# minimum size
assert run(
"""1 1 1
42
g 1 1
"""
) == "42", "minimum matrix"

# repeated swaps cancel out
assert run(
"""2 2 3
1 2
3 4
r 1 2
r 1 2
g 1 1
"""
) == "1", "double row swap"

# column remapping correctness
assert run(
"""2 3 2
1 2 3
4 5 6
c 1 3
g 1 1
"""
) == "3", "column swap"

# combined row and column swaps
assert run(
"""2 3 4
1 2 3
4 5 6
c 1 3
r 1 2
g 1 1
g 2 3
"""
) == "6\n1", "combined mappings"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 matrix | 42 | Smallest valid input |
| Two identical row swaps | 1 | Swaps correctly reverse |
| Single column swap | 3 | Column remapping correctness |
| Combined row and column swaps | 6, 1 | Interaction of both mappings |

## Edge Cases

Consider repeated swaps of the same rows.

Input:

```
2 2 3
1 2
3 4
r 1 2
r 1 2
g 1 1
```

Execution:

After the first swap:

```
rows = [1, 0]
```

After the second swap:

```
rows = [0, 1]
```

The mapping returns to its original state. Query `(1,1)` accesses:

```
table[0][0] = 1
```

The algorithm handles this naturally because swaps only exchange mapping entries.

Now consider independent row and column remapping.

Input:

```
2 3 3
1 2 3
4 5 6
r 1 2
c 1 3
g 1 1
```

After the row swap:

```
rows = [1, 0]
```

After the column swap:

```
cols = [2, 1, 0]
```

The query `(1,1)` maps to:

```
table[1][2] = 6
```

The visible top-left cell truly becomes `6`, because visible row 1 is original row 2 and visible column 1 is original column 3.

Finally, consider the smallest possible matrix.

Input:

```
1 1 1
99
g 1 1
```

No swaps exist because there is only one row and one column. The mapping arrays remain:

```
rows = [0]
cols = [0]
```

The query reads:

```
table[0][0] = 99
```

This confirms the implementation handles boundary dimensions correctly without special cases.
