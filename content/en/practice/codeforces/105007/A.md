---
title: "CF 105007A - Finding Bo"
description: "The grid describes a dog park laid out as a rectangle of cells. Each cell is either empty, marked by a dot, or contains a single digit from 1 to 9 representing a dog’s height at that position."
date: "2026-06-28T03:04:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105007
codeforces_index: "A"
codeforces_contest_name: "UTPC Contest 03-01-24 Div. 2 (Beginner)"
rating: 0
weight: 105007
solve_time_s: 86
verified: false
draft: false
---

[CF 105007A - Finding Bo](https://codeforces.com/problemset/problem/105007/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** no  

## Solution
## Problem Understanding

The grid describes a dog park laid out as a rectangle of cells. Each cell is either empty, marked by a dot, or contains a single digit from 1 to 9 representing a dog’s height at that position. Among all dogs in the park, exactly one has the greatest height, and the task is to locate its position and report its row and column using 1-based indexing.

What makes the input slightly more than a plain list is that the data is spatial. We are not just extracting a maximum value, we are also tracking where it occurs inside a 2D structure. The output is therefore not the value itself, but the coordinates of the cell that contains the maximum digit.

The constraints are small, with both dimensions up to 100. That means at most 10,000 cells exist. Any solution that scans each cell a constant number of times is easily fast enough. Even a straightforward full scan of the grid is comfortably within limits, while anything that tries to be more clever than necessary would not gain any meaningful performance advantage.

A subtle mistake often comes from input parsing. Each row is a string of characters, not space-separated values. Treating it as a list of integers or splitting incorrectly can shift columns or merge rows, producing incorrect coordinates. Another common issue is forgetting that the answer must be 1-based, since programming languages typically index from 0.

Edge cases that matter here are mostly structural rather than algorithmic. A grid of size 1×1 is valid and must return (1, 1). A grid where all dogs have the same height except one maximum is guaranteed unique, but a careless implementation that updates the answer on “greater or equal” instead of strictly greater could incorrectly overwrite the first maximum encountered. A grid with many dots and a single digit also tests whether parsing skips non-dog cells correctly.

## Approaches

The most direct approach is to scan every cell in the grid, checking whether it contains a digit. If it does, we compare it against the best height seen so far and update our stored best value and coordinates when a larger value appears. This works because the grid is small and each cell is inspected exactly once.

A brute-force variant would conceptually try each cell as a candidate answer and then scan the entire grid again to verify whether it is the maximum. That would involve comparing every pair of cells, resulting in roughly O((NM)^2) operations in the worst case. With N and M up to 100, this is unnecessary overhead and risks being inefficient in a more constrained version of the problem.

The key observation is that the problem only requires a global maximum over a finite set of values with positional tracking. There is no dependency between cells, no ordering constraints, and no need for preprocessing. This reduces the task to a single pass accumulation problem: maintain the best seen so far while traversing the grid once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pairwise Checking | O((NM)^2) | O(1) | Too slow |
| Single Pass Scan | O(NM) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the dimensions N and M, then read the grid row by row as strings. This preserves spatial structure so that each character corresponds to exactly one cell in the grid.
2. Initialize a variable to store the maximum height found so far. Set it below the smallest possible digit so that any valid dog will replace it immediately.
3. Initialize two variables to store the coordinates of the best position found so far.
4. Iterate over each row index i from 0 to N−1.
5. Inside each row, iterate over each column index j from 0 to M−1.
6. If the current cell contains a digit rather than a dot, convert it to an integer and compare it with the current maximum. If it is larger, update the maximum and record (i, j) as the new best position.
7. After scanning all cells, output the stored coordinates using 1-based indexing.

The reason we only update when we see a strictly larger value is tied to the guarantee that the tallest dog is unique. This ensures we never need tie-breaking logic; the first occurrence of the maximum is the correct one and remains stable.

### Why it works

At every step of the scan, the algorithm maintains the invariant that the stored position corresponds to the tallest dog encountered in the portion of the grid processed so far. Since every cell is visited exactly once and comparisons are monotonic with respect to height, this invariant guarantees that once the full grid has been processed, the stored position must correspond to the global maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    best_val = -1
    best_i = 0
    best_j = 0

    for i in range(n):
        row = input().strip()
        for j in range(m):
            c = row[j]
            if c != '.':
                val = ord(c) - ord('0')
                if val > best_val:
                    best_val = val
                    best_i = i
                    best_j = j

    print(best_i + 1, best_j + 1)

if __name__ == "__main__":
    solve()
```

The solution relies on a single pass over the grid. The conversion `ord(c) - ord('0')` avoids slower integer parsing and is safe because the input guarantees single-digit numbers. The coordinates are stored in 0-based indexing during computation and converted to 1-based only at output time, preventing off-by-one errors during updates.

A common implementation mistake is updating coordinates before checking whether the value is strictly larger, or using `>=` instead of `>`. That would incorrectly overwrite earlier occurrences of the maximum, which is unnecessary and can complicate reasoning about correctness. Another subtle issue is forgetting to strip newline characters from each row, which can shift indexing or introduce invalid characters.

## Worked Examples

### Example 1

Consider a small grid:

```
3 4
.2.1
..9.
.3.5
```

| Cell (i, j) | Value | Best so far | Best position |
| --- | --- | --- | --- |
| (0,0) | . | - | (0,0) |
| (0,1) | 2 | 2 | (0,1) |
| (0,2) | . | 2 | (0,1) |
| (0,3) | 1 | 2 | (0,1) |
| (1,0) | . | 2 | (0,1) |
| (1,1) | . | 2 | (0,1) |
| (1,2) | 9 | 9 | (1,2) |
| (1,3) | . | 9 | (1,2) |
| (2,0) | . | 9 | (1,2) |
| (2,1) | 3 | 9 | (1,2) |
| (2,2) | . | 9 | (1,2) |
| (2,3) | 5 | 9 | (1,2) |

The scan ends with the maximum value 9 at position (1,2) in 0-based indexing, which becomes (2,3) in 1-based indexing.

This trace confirms that the algorithm does not depend on where the maximum appears; it only tracks the largest value seen.

### Example 2

A single-row edge case:

```
1 5
.7.2.9
```

| Cell (i, j) | Value | Best so far | Best position |
| --- | --- | --- | --- |
| (0,0) | . | - | (0,0) |
| (0,1) | 7 | 7 | (0,1) |
| (0,2) | . | 7 | (0,1) |
| (0,3) | 2 | 7 | (0,1) |
| (0,4) | . | 7 | (0,1) |
| (0,5) | 9 | 9 | (0,5) |

The maximum shifts exactly once when 9 is encountered, showing that the update rule correctly handles late-occurring maxima.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(NM) | Each cell is visited once and processed in constant time |
| Space | O(1) | Only a few variables are used regardless of grid size |

The grid size is at most 10,000 cells, so a single linear scan is trivial within the 1-second limit. Memory usage remains constant since no additional structures proportional to input size are stored.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# simple sample
assert run("""3 4
.2.1
..9.
.3.5
""") == "2 3"

# single cell
assert run("""1 1
7
""") == "1 1"

# max at first position
assert run("""2 3
9..
.12
""") == "1 1"

# max at last position
assert run("""2 3
123
..9
""") == "2 3"

# all dots except one
assert run("""3 3
...
.5.
...
""") == "2 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 grid | 1 1 | minimal boundary case |
| max first cell | 1 1 | no overwrite needed |
| max last cell | 2 3 | late update correctness |
| sparse grid | 2 2 | parsing non-digit cells |

## Edge Cases

A 1×1 grid is the simplest possible structure. The algorithm initializes the best value below any valid digit, so the single cell is immediately chosen and returned as (1, 1). There are no iterations that could overwrite this result incorrectly.

A grid where the maximum occurs at the first cell tests whether later comparisons incorrectly replace an already optimal answer. Because updates only occur on strictly greater values, once the first maximum is stored, it remains unchanged unless a larger value appears, which cannot happen in a correct input.

A grid filled mostly with dots ensures that non-numeric characters are safely ignored. The scan simply skips these cells, leaving the best value unchanged until a digit is encountered.
