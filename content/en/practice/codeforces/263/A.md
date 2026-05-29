---
title: "CF 263A - Beautiful Matrix"
description: "We are given a fixed 5 × 5 matrix containing exactly one cell with value 1, while every other cell contains 0. The goal is to move the 1 into the center of the matrix, which is position (3, 3) using 1-based indexing."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 263
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 161 (Div. 2)"
rating: 800
weight: 263
solve_time_s: 125
verified: true
draft: false
---

[CF 263A - Beautiful Matrix](https://codeforces.com/problemset/problem/263/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 2m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed 5 × 5 matrix containing exactly one cell with value `1`, while every other cell contains `0`. The goal is to move the `1` into the center of the matrix, which is position `(3, 3)` using 1-based indexing.

A move allows swapping two adjacent rows or two adjacent columns. Swapping neighboring rows changes the row position of the `1` by exactly one. Swapping neighboring columns changes the column position of the `1` by exactly one.

The input is simply the matrix itself. The output is the minimum number of row and column swaps needed to move the `1` into the center cell.

The constraints are extremely small because the matrix size is always fixed at 5 × 5. Even inefficient solutions would run instantly. This changes the nature of the problem completely. We do not need advanced optimization, graph search, or simulation. The real task is recognizing the mathematical structure behind the moves.

A common mistake is mixing 0-based and 1-based indexing. The center is the third row and third column in the statement, but in Python arrays that becomes index `(2, 2)`.

Consider this input:

```
0 0 0 0 0
0 0 0 0 1
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```

The `1` is at row `2`, column `5` using 1-based indexing. The answer is:

```
3
```

because we need two column swaps to move from column `5` to column `3`, and one row swap to move from row `2` to row `3`.

Another easy mistake is trying to count diagonal movement as one operation. That is impossible because each move changes only a row or only a column.

For example:

```
1 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```

The correct answer is:

```
4
```

The `1` must move two rows downward and two columns rightward. Those are independent operations, so the total is `2 + 2 = 4`.

A different subtle bug happens when people stop searching after finding the row containing `1` but forget to record the column correctly. Since there is exactly one `1`, we must store both coordinates before computing the answer.

## Approaches

The brute-force idea is to simulate every possible sequence of swaps until the `1` reaches the center. We could model each matrix configuration as a state and run BFS over all reachable states. Since each move swaps neighboring rows or columns, BFS would eventually find the shortest path.

This works because every move has equal cost, so BFS guarantees the minimum number of operations.

The problem is that this completely ignores the structure of the matrix. Even though the state space is still manageable for a 5 × 5 grid, it is unnecessary work. We are not rearranging many values. Only one cell matters.

The key observation is that row swaps and column swaps are independent. Moving the `1` vertically never affects its column, and moving it horizontally never affects its row.

If the `1` is currently at `(r, c)`, then:

- Moving it to row `3` needs `|r - 3|` row swaps.
- Moving it to column `3` needs `|c - 3|` column swaps.

Since these actions do not interfere with each other, the minimum total number of moves is simply:

```
|r - 3| + |c - 3|
```

This transforms the problem from state exploration into direct distance computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(states) | O(states) | Unnecessary |
| Optimal | O(25) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the 5 × 5 matrix.
2. Scan every cell until the value `1` is found.
3. Record its row index `r` and column index `c`.
4. Compute the vertical distance from the center using `abs(r - 2)` if using 0-based indexing.
5. Compute the horizontal distance from the center using `abs(c - 2)`.
6. Add the two distances and print the result.

The reason this works is that every adjacent row swap changes the row position by exactly one, and every adjacent column swap changes the column position by exactly one. No move can reduce both distances simultaneously.

### Why it works

The algorithm relies on Manhattan distance. Each allowed operation changes exactly one coordinate by one unit. Reaching the center requires correcting the row difference and the column difference independently.

Suppose the `1` starts at `(r, c)`. Any valid sequence of moves must perform at least `|r - 2|` row changes and at least `|c - 2|` column changes in 0-based indexing. Since each move changes only one coordinate, the minimum total is their sum.

The algorithm computes exactly this quantity, so it cannot underestimate or overestimate the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

# solution

def solve():
    row = col = -1

    for i in range(5):
        arr = list(map(int, input().split()))

        for j in range(5):
            if arr[j] == 1:
                row = i
                col = j

    print(abs(row - 2) + abs(col - 2))

solve()
```

The program scans the matrix once and stores the coordinates of the only cell containing `1`.

The implementation uses 0-based indexing because Python lists are naturally 0-based. That means the center cell is `(2, 2)` rather than `(3, 3)`.

The expression:

```
abs(row - 2) + abs(col - 2)
```

computes the Manhattan distance from the current position to the center.

One subtle detail is that we should not stop after finding the row containing `1`. We must store both coordinates correctly. Another common mistake is accidentally using `(3, 3)` with 0-based indexing, which shifts the target one cell too far.

## Worked Examples

### Example 1

Input:

```
0 0 0 0 0
0 0 0 0 1
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```

| Step | row | col | Calculation |
| --- | --- | --- | --- |
| Found `1` | 1 | 4 | Using 0-based indexing |
| Vertical distance | 1 | 4 | `abs(1 - 2) = 1` |
| Horizontal distance | 1 | 4 | `abs(4 - 2) = 2` |
| Final answer | 1 | 4 | `1 + 2 = 3` |

The trace shows that vertical and horizontal movement are counted independently. One row swap and two column swaps are required.

### Example 2

Input:

```
0 0 0 0 0
0 0 0 0 0
0 0 1 0 0
0 0 0 0 0
0 0 0 0 0
```

| Step | row | col | Calculation |
| --- | --- | --- | --- |
| Found `1` | 2 | 2 | Already centered |
| Vertical distance | 2 | 2 | `abs(2 - 2) = 0` |
| Horizontal distance | 2 | 2 | `abs(2 - 2) = 0` |
| Final answer | 2 | 2 | `0 + 0 = 0` |

This demonstrates the minimum possible answer. If the `1` already occupies the center, no swaps are needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(25) | We scan every cell of the fixed 5 × 5 matrix once |
| Space | O(1) | Only a few integer variables are stored |

Since the matrix size never changes, the running time is effectively constant. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    row = col = -1

    for i in range(5):
        arr = list(map(int, input().split()))

        for j in range(5):
            if arr[j] == 1:
                row = i
                col = j

    print(abs(row - 2) + abs(col - 2))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run(
"""0 0 0 0 0
0 0 0 0 1
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
"""
) == "3\n", "sample 1"

# already centered
assert run(
"""0 0 0 0 0
0 0 0 0 0
0 0 1 0 0
0 0 0 0 0
0 0 0 0 0
"""
) == "0\n", "already centered"

# top-left corner
assert run(
"""1 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
"""
) == "4\n", "top-left corner"

# bottom-right corner
assert run(
"""0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 1
"""
) == "4\n", "bottom-right corner"

# same row as center, different column
assert run(
"""0 0 0 0 0
0 0 0 0 0
1 0 0 0 0
0 0 0 0 0
0 0 0 0 0
"""
) == "2\n", "horizontal movement only"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` already in center | `0` | Zero-move scenario |
| `1` in top-left corner | `4` | Maximum upward and leftward distance |
| `1` in bottom-right corner | `4` | Maximum downward and rightward distance |
| `1` in center row only | `2` | Horizontal movement handled independently |

## Edge Cases

Consider the case where the `1` is already centered:

```
0 0 0 0 0
0 0 0 0 0
0 0 1 0 0
0 0 0 0 0
0 0 0 0 0
```

The algorithm finds `row = 2` and `col = 2` in 0-based indexing. It computes:

```
abs(2 - 2) + abs(2 - 2) = 0
```

The output is correctly `0`. This checks that the algorithm does not force unnecessary moves.

Now consider a corner position:

```
1 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```

The coordinates are `(0, 0)`. The algorithm computes:

```
abs(0 - 2) + abs(0 - 2) = 2 + 2 = 4
```

The result is correct because the `1` must move two rows downward and two columns rightward.

Another tricky case is when the `1` shares either the correct row or the correct column with the center:

```
0 0 0 0 0
0 0 0 0 0
1 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```

The `1` is already in the center row, so only horizontal movement is needed. The algorithm computes:

```
abs(2 - 2) + abs(0 - 2) = 0 + 2 = 2
```

This confirms that row and column distances are handled independently.
