---
title: "CF 90B - African Crossword"
description: "We are given a small grid of lowercase letters. A cell survives only if its letter is unique both inside its row and inside its column. If the same character appears somewhere else in the same row, that cell is removed."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 90
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 74 (Div. 2 Only)"
rating: 1100
weight: 90
solve_time_s: 104
verified: true
draft: false
---

[CF 90B - African Crossword](https://codeforces.com/problemset/problem/90/B)

**Rating:** 1100  
**Tags:** implementation, strings  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small grid of lowercase letters. A cell survives only if its letter is unique both inside its row and inside its column. If the same character appears somewhere else in the same row, that cell is removed. The same happens if the character appears somewhere else in the same column.

After removing all invalid cells simultaneously, we read the remaining letters row by row, from top to bottom and left to right, and concatenate them into the final answer.

The grid dimensions are at most 100 × 100, so the total number of cells is at most 10,000. Even algorithms that inspect an entire row and column for every cell are still fast enough here, because 10,000 × 200 operations is only about two million comparisons. That means we do not need advanced data structures or preprocessing tricks.

The main challenge is not performance, it is implementing the filtering condition correctly.

A common mistake is checking only rows or only columns. A cell survives only if both conditions hold simultaneously.

Consider this example:

```
2 2
aa
bc
```

The two `a` cells are invalid because they repeat inside the first row.

The correct output is:

```
bc
```

Another easy mistake is removing letters one by one instead of simultaneously. The problem says all repeated letters are crossed out at the same time, so removing one cell cannot make another cell suddenly become unique.

For example:

```
3 1
a
a
a
```

All three cells are invalid because the column contains repeated `a`.

The correct output is an empty string logically, but the statement guarantees at least one surviving character in valid test cases.

One more subtle case is when a letter is unique in its row but repeated in its column.

```
2 2
ab
cb
```

The two `b` cells must be removed because they share a column.

The correct output is:

```
ac
```

A careless implementation that checks only rows would incorrectly keep both `b` cells.

## Approaches

The brute-force idea follows the definition directly. For every cell, scan the entire row to see whether the same letter appears somewhere else. Then scan the entire column for the same condition. If neither scan finds another equal character, append the cell to the answer.

This works because the grid is small. Suppose the grid is 100 × 100. For each of the 10,000 cells, we scan up to 100 row positions and 100 column positions. That gives roughly two million comparisons, which is completely fine within the time limit.

The brute-force approach already passes comfortably, so there is no need for sophisticated optimization. Still, we can organize the logic more cleanly by counting frequencies first.

The key observation is that a cell survives exactly when its character appears once in its row and once in its column. Instead of repeatedly rescanning rows and columns, we can precompute character frequencies for every row and every column.

For each row, count how many times each letter appears. Do the same for each column. Then a cell `(i, j)` survives if:

```
row_count[i][grid[i][j]] == 1
and
col_count[j][grid[i][j]] == 1
```

This turns repeated scanning into constant-time checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n × m × (n + m)) | O(1) | Accepted |
| Optimal | O(n × m) | O(n × 26 + m × 26) | Accepted |

## Algorithm Walkthrough

1. Read the grid into a list of strings.

We need random access to every cell because each character must be checked against its row and column frequencies.
2. Build frequency tables for rows.

For every row, count how many times each lowercase letter appears. Since letters are only `'a'` to `'z'`, an array of size 26 is enough.
3. Build frequency tables for columns.

For every column, count how many times each lowercase letter appears in that column.
4. Traverse every cell `(i, j)` in row-major order.

This traversal order matches the required output order, so surviving characters can be appended directly to the answer string.
5. For the current character `c`, check whether it appears exactly once in its row and exactly once in its column.

If both counts equal 1, keep the character. Otherwise discard it.
6. Print the concatenated surviving characters.

### Why it works

The algorithm directly encodes the condition from the problem statement. A character survives only when no other equal character exists in its row and no other equal character exists in its column.

The row frequency table tells us exactly how many equal letters appear in that row. The column frequency table does the same for the column. If both counts are 1, the current cell is unique in both directions and must remain. If either count is larger than 1, some matching character exists and the cell must be crossed out.

Because every cell is checked independently against the original frequencies, all removals happen simultaneously, exactly as required.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    row_count = [[0] * 26 for _ in range(n)]
    col_count = [[0] * 26 for _ in range(m)]

    # Count frequencies in rows
    for i in range(n):
        for j in range(m):
            idx = ord(grid[i][j]) - ord('a')
            row_count[i][idx] += 1

    # Count frequencies in columns
    for j in range(m):
        for i in range(n):
            idx = ord(grid[i][j]) - ord('a')
            col_count[j][idx] += 1

    ans = []

    # Collect surviving characters
    for i in range(n):
        for j in range(m):
            idx = ord(grid[i][j]) - ord('a')

            if row_count[i][idx] == 1 and col_count[j][idx] == 1:
                ans.append(grid[i][j])

    print("".join(ans))

solve()
```

The first section reads the grid and prepares frequency arrays. Using arrays of length 26 is simpler and faster than dictionaries because the alphabet is fixed.

The row counting loop records how many times each character appears inside each row. The column counting loop does the same for columns. Splitting these passes keeps the logic straightforward and avoids mixing two independent concepts.

The final traversal follows row-major order because the output must preserve the original reading order. This detail is easy to overlook. Sorting the surviving characters or storing them in another structure would produce incorrect answers.

The condition:

```
row_count[i][idx] == 1 and col_count[j][idx] == 1
```

is the exact translation of the problem rule. Both checks are required. Using `or` here would incorrectly keep cells that are unique in only one direction.

The implementation has no boundary issues because every loop stays within the grid dimensions, and character indices always remain between 0 and 25.

## Worked Examples

### Example 1

Input:

```
3 3
cba
bcd
cbc
```

Row frequencies:

| Row | Frequencies |
| --- | --- |
| `cba` | c:1 b:1 a:1 |
| `bcd` | b:1 c:1 d:1 |
| `cbc` | c:2 b:1 |

Column frequencies:

| Column | Characters | Frequencies |
| --- | --- | --- |
| 0 | c b c | c:2 b:1 |
| 1 | b c b | b:2 c:1 |
| 2 | a d c | a:1 d:1 c:1 |

Cell checks:

| Cell | Character | Row Unique | Column Unique | Keep |
| --- | --- | --- | --- | --- |
| (0,0) | c | Yes | No | No |
| (0,1) | b | Yes | No | No |
| (0,2) | a | Yes | Yes | Yes |
| (1,0) | b | Yes | Yes | Yes |
| (1,1) | c | Yes | Yes | Yes |
| (1,2) | d | Yes | Yes | Yes |
| (2,0) | c | No | No | No |
| (2,1) | b | Yes | No | No |
| (2,2) | c | No | Yes | No |

Final answer:

```
abcd
```

This trace shows that uniqueness must hold in both dimensions simultaneously.

### Example 2

Input:

```
2 2
ab
cb
```

Row frequencies:

| Row | Frequencies |
| --- | --- |
| `ab` | a:1 b:1 |
| `cb` | c:1 b:1 |

Column frequencies:

| Column | Characters | Frequencies |
| --- | --- | --- |
| 0 | a c | a:1 c:1 |
| 1 | b b | b:2 |

Cell checks:

| Cell | Character | Row Unique | Column Unique | Keep |
| --- | --- | --- | --- | --- |
| (0,0) | a | Yes | Yes | Yes |
| (0,1) | b | Yes | No | No |
| (1,0) | c | Yes | Yes | Yes |
| (1,1) | b | Yes | No | No |

Final answer:

```
ac
```

This example demonstrates why checking only rows is insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n × m) | Each cell is processed a constant number of times |
| Space | O(n × 26 + m × 26) | Frequency tables for rows and columns |

With at most 10,000 cells, the solution easily fits within the limits. The memory usage is tiny because only frequency arrays for lowercase letters are stored.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        n, m = map(int, input().split())
        grid = [input().strip() for _ in range(n)]

        row_count = [[0] * 26 for _ in range(n)]
        col_count = [[0] * 26 for _ in range(m)]

        for i in range(n):
            for j in range(m):
                idx = ord(grid[i][j]) - ord('a')
                row_count[i][idx] += 1

        for j in range(m):
            for i in range(n):
                idx = ord(grid[i][j]) - ord('a')
                col_count[j][idx] += 1

        ans = []

        for i in range(n):
            for j in range(m):
                idx = ord(grid[i][j]) - ord('a')

                if row_count[i][idx] == 1 and col_count[j][idx] == 1:
                    ans.append(grid[i][j])

        return "".join(ans)

    return solve()

# provided sample
assert run(
"""3 3
cba
bcd
cbc
"""
) == "abcd", "sample 1"

# minimum size
assert run(
"""1 1
a
"""
) == "a", "single cell"

# repeated row
assert run(
"""1 4
abca
"""
) == "bc", "row duplicates"

# repeated column
assert run(
"""4 1
a
b
a
c
"""
) == "bc", "column duplicates"

# all unique
assert run(
"""2 3
abc
def
"""
) == "abcdef", "all survive"

# mixed duplicates
assert run(
"""2 2
ab
cb
"""
) == "ac", "column duplicate removal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1×1` grid | `a` | Minimum valid input |
| `abca` | `bc` | Row duplicate handling |
| Single repeated column | `bc` | Column duplicate handling |
| All unique grid | `abcdef` | Every cell survives |
| Mixed duplicate case | `ac` | Both row and column conditions together |

## Edge Cases

Consider a row with repeated letters:

```
1 4
abca
```

The row frequencies are:

```
a:2, b:1, c:1
```

All column frequencies are 1 because there is only one row.

The algorithm removes both `a` cells because their row count is greater than 1. The surviving letters are `b` and `c`, so the output becomes:

```
bc
```

This confirms that duplicates inside the same row invalidate every matching occurrence.

Now consider a column duplicate case:

```
4 1
a
b
a
c
```

The column frequencies are:

```
a:2, b:1, c:1
```

Every row contains only one character, so row frequencies are all 1.

The algorithm removes both `a` cells because their column count is greater than 1. The output becomes:

```
bc
```

This verifies that column repetition alone is enough to remove a cell.

Finally, consider a case where duplicates exist in both directions:

```
3 3
aaa
aba
aaa
```

The center `b` is unique in its row and column, while every `a` repeats many times.

The algorithm keeps only the center cell, producing:

```
b
```

This demonstrates that the checks are independent and correctly isolate the surviving cells.
