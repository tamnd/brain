---
title: "CF 157A - Game Outcome"
description: "We are given an n × n board where every cell contains an integer. For each cell, we compare two quantities. The first quantity is the sum of all numbers in that cell’s row. The second quantity is the sum of all numbers in that cell’s column."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 157
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 110 (Div. 2)"
rating: 800
weight: 157
solve_time_s: 139
verified: true
draft: false
---

[CF 157A - Game Outcome](https://codeforces.com/problemset/problem/157/A)

**Rating:** 800  
**Tags:** brute force  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an `n × n` board where every cell contains an integer. For each cell, we compare two quantities.

The first quantity is the sum of all numbers in that cell’s row. The second quantity is the sum of all numbers in that cell’s column. A cell is called winning if its column sum is strictly larger than its row sum.

The task is to count how many cells satisfy this condition.

The board size is very small. Since `n ≤ 30`, the entire grid contains at most `30 × 30 = 900` cells. Even an algorithm that performs extra work for every cell will still run comfortably within the limits. This means we do not need advanced optimization techniques, but we should still think carefully about repeated computations.

A direct implementation might recompute the entire row sum and column sum separately for every cell. Each recomputation costs `O(n)`, and there are `n²` cells, so the total complexity becomes `O(n³)`. With `n = 30`, this is still fast enough, since the total number of operations is only around `27,000`.

Still, the structure of the problem naturally suggests a cleaner approach. Row sums and column sums are reused many times. Once we compute them once, every cell can be checked in constant time.

There are a few edge cases that can silently break careless implementations.

Consider the smallest possible board:

```
1
1
```

The only row sum is `1`, and the only column sum is also `1`. Since the condition is strictly greater, the answer is `0`.

A common mistake is using `>=` instead of `>`.

Another subtle case is when every value is identical:

```
2
5 5
5 5
```

Every row sum equals every column sum, so no cell is winning. The correct output is:

```
0
```

A careless implementation might accidentally count equal sums as valid.

One more tricky situation is when only some rows and columns differ:

```
3
1 1 10
1 1 10
1 1 10
```

The row sums are all `12`. The column sums are `3`, `3`, and `30`.

Only the third column produces winning cells, so the correct answer is:

```
3
```

This catches implementations that confuse row indices with column indices while computing sums.

## Approaches

The most direct solution is brute force. For every cell `(i, j)`, we compute the sum of row `i` by iterating through all columns, and we compute the sum of column `j` by iterating through all rows. If the column sum is larger, we increment the answer.

This works because the definition of a winning cell depends only on those two sums. The implementation is straightforward and mirrors the problem statement exactly.

The issue is repeated work. The same row sum gets recomputed once for every cell in that row, and the same column sum gets recomputed once for every cell in that column.

For example, if `n = 30`, then each of the `900` cells performs about `60` additions, leading to roughly `54,000` additions overall. This is still completely acceptable here, but the repetition is unnecessary.

The key observation is that row sums and column sums never change. Once we compute them once, they can be reused for every relevant cell.

We can first build two arrays:

`row_sum[i]` stores the sum of row `i`.

`col_sum[j]` stores the sum of column `j`.

Then each cell check becomes trivial:

If `col_sum[j] > row_sum[i]`, the cell is winning.

This reduces the complexity from `O(n³)` to `O(n²)` while also making the logic cleaner.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Accepted |
| Optimal | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n` and the `n × n` grid.
2. Create an array `row_sum` of size `n` initialized with zeros.
3. Create an array `col_sum` of size `n` initialized with zeros.
4. Traverse the entire grid once.

For every cell `(i, j)`, add its value to `row_sum[i]` and to `col_sum[j]`.

This computes every row total and column total in a single pass.
5. Initialize `answer = 0`.
6. Traverse the grid again.

For every cell `(i, j)`, compare `col_sum[j]` and `row_sum[i]`.
7. If `col_sum[j] > row_sum[i]`, increment `answer`.

The problem asks for strictly greater, not greater-than-or-equal.
8. Print `answer`.

### Why it works

The algorithm relies on a simple invariant: after the first traversal, `row_sum[i]` equals the sum of every value in row `i`, and `col_sum[j]` equals the sum of every value in column `j`.

Since these values are computed exactly once from the original grid and never modified afterward, every later comparison uses the correct totals. Each cell is checked independently against the exact condition from the problem statement, so every winning cell is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
grid = [list(map(int, input().split())) for _ in range(n)]

row_sum = [0] * n
col_sum = [0] * n

for i in range(n):
    for j in range(n):
        row_sum[i] += grid[i][j]
        col_sum[j] += grid[i][j]

answer = 0

for i in range(n):
    for j in range(n):
        if col_sum[j] > row_sum[i]:
            answer += 1

print(answer)
```

The first part reads the board into a 2D list.

The next nested loop computes row sums and column sums simultaneously. Updating both arrays inside the same traversal avoids unnecessary passes over the grid.

The second nested loop checks every cell independently. The condition uses `>` because the statement requires the column sum to be strictly larger.

No special handling is needed for small boards like `n = 1`. The logic naturally works because the row sum and column sum are equal for the only cell.

Python integers are also completely safe here. Even in the largest case, the maximum row or column sum is only `30 × 100 = 3000`.

## Worked Examples

### Example 1

Input:

```
1
1
```

The computed sums are:

| Cell | Row Sum | Column Sum | Winning? |
| --- | --- | --- | --- |
| (0,0) | 1 | 1 | No |

Final answer:

```
0
```

This example confirms that equality does not count as winning.

### Example 2

Input:

```
4
5 7 8 4
9 5 3 2
1 6 6 4
9 5 7 3
```

First compute row sums and column sums.

Row sums:

| Row | Sum |
| --- | --- |
| 0 | 24 |
| 1 | 19 |
| 2 | 17 |
| 3 | 24 |

Column sums:

| Column | Sum |
| --- | --- |
| 0 | 24 |
| 1 | 23 |
| 2 | 24 |
| 3 | 13 |

Now evaluate every cell.

| Cell | Row Sum | Column Sum | Winning? |
| --- | --- | --- | --- |
| (0,0) | 24 | 24 | No |
| (0,1) | 24 | 23 | No |
| (0,2) | 24 | 24 | No |
| (0,3) | 24 | 13 | No |
| (1,0) | 19 | 24 | Yes |
| (1,1) | 19 | 23 | Yes |
| (1,2) | 19 | 24 | Yes |
| (1,3) | 19 | 13 | No |
| (2,0) | 17 | 24 | Yes |
| (2,1) | 17 | 23 | Yes |
| (2,2) | 17 | 24 | Yes |
| (2,3) | 17 | 13 | No |
| (3,0) | 24 | 24 | No |
| (3,1) | 24 | 23 | No |
| (3,2) | 24 | 24 | No |
| (3,3) | 24 | 13 | No |

The total number of winning cells is `6`.

This trace demonstrates that the same row and column totals are reused across many checks, which is exactly why precomputing them is effective.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | We traverse the grid twice |
| Space | O(n) | We store row sums and column sums |

With `n ≤ 30`, the algorithm is far below the time and memory limits. Even the brute-force solution would pass, but the precomputed version is cleaner and scales better conceptually.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())
    grid = [list(map(int, input().split())) for _ in range(n)]

    row_sum = [0] * n
    col_sum = [0] * n

    for i in range(n):
        for j in range(n):
            row_sum[i] += grid[i][j]
            col_sum[j] += grid[i][j]

    ans = 0

    for i in range(n):
        for j in range(n):
            if col_sum[j] > row_sum[i]:
                ans += 1

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
assert run("1\n1\n") == "0\n", "sample 1"

# all equal values
assert run(
    "2\n"
    "5 5\n"
    "5 5\n"
) == "0\n", "all sums equal"

# one dominant column
assert run(
    "3\n"
    "1 1 10\n"
    "1 1 10\n"
    "1 1 10\n"
) == "3\n", "third column wins everywhere"

# asymmetric case
assert run(
    "2\n"
    "1 100\n"
    "1 100\n"
) == "2\n", "second column only"

# larger mixed case
assert run(
    "4\n"
    "5 7 8 4\n"
    "9 5 3 2\n"
    "1 6 6 4\n"
    "9 5 7 3\n"
) == "6\n", "mixed values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 × 1` board | `0` | Minimum-size input |
| All values equal | `0` | Strict comparison handling |
| One dominant column | `3` | Correct column accumulation |
| `[[1,100],[1,100]]` | `2` | Row/column indexing correctness |
| Mixed `4 × 4` board | `6` | General correctness |

## Edge Cases

Consider the smallest possible board:

```
1
1
```

The algorithm computes:

`row_sum = [1]`

`col_sum = [1]`

For the only cell, the comparison becomes `1 > 1`, which is false. The algorithm correctly prints:

```
0
```

This confirms that equality is not counted.

Now consider a board where every number is identical:

```
2
5 5
5 5
```

The row sums become `[10, 10]`, and the column sums also become `[10, 10]`.

Every comparison is `10 > 10`, which is false. No cells are counted, so the answer is:

```
0
```

This case verifies that the implementation does not accidentally use `>=`.

Finally, consider a case with a dominant column:

```
3
1 1 10
1 1 10
1 1 10
```

The algorithm computes:

`row_sum = [12, 12, 12]`

`col_sum = [3, 3, 30]`

For every row, only the third column satisfies `30 > 12`.

Exactly three cells are counted, so the output is:

```
3
```

This confirms that row and column indices are handled correctly and that sums are reused consistently across all cells.
