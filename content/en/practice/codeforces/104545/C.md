---
title: "CF 104545C - Coffee Break"
description: "We are given a small binary grid representing a table of snacks, where each cell is either a 1 (a cheese ball) or a 0 (a coxinha)."
date: "2026-06-30T08:56:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104545
codeforces_index: "C"
codeforces_contest_name: "VIII MaratonUSP Freshman Contest"
rating: 0
weight: 104545
solve_time_s: 54
verified: true
draft: false
---

[CF 104545C - Coffee Break](https://codeforces.com/problemset/problem/104545/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small binary grid representing a table of snacks, where each cell is either a 1 (a cheese ball) or a 0 (a coxinha). The task is to choose exactly one axis-aligned rectangular subgrid and collect all snacks inside it, with the restriction that the rectangle must not contain any coxinhas at all. In other words, every chosen cell inside the rectangle must be a 1.

The objective is to maximize the number of collected cheese balls, which is equivalent to maximizing the area of a subrectangle consisting entirely of 1s.

The constraint n × m ≤ 400 is the key structural clue. Even in the worst case this is a very small grid, which allows solutions that are quadratic or slightly worse per cell without risk of exceeding time limits. However, it also hints that the intended solution is not brute-force over all rectangles, since that would still involve checking many submatrices repeatedly, leading to unnecessary overhead and awkward implementation.

A naive approach that enumerates every possible rectangle and verifies whether it is all ones can fail silently in performance or implementation complexity. For example, even on a 20 × 20 grid, there are about 10^8 rectangles, and checking each one costs additional work.

A more subtle failure case for naive implementations comes from incorrect validation of rectangles. Suppose we pick a rectangle and check only its corners or a partial scan:

Input:

```
3 3
1 1 1
1 0 1
1 1 1
```

A careless checker might validate a rectangle spanning the entire grid by only checking borders and conclude it is valid, incorrectly returning 9. The correct answer is 4, coming from any 2×2 sub-square of ones that avoids the center zero.

This shows that correctness depends on global structure inside the rectangle, not just boundary values.

## Approaches

The brute-force idea is straightforward: enumerate all possible subrectangles defined by top row, bottom row, left column, and right column, and for each one scan every cell to check if it contains a zero. If it does not, compute its area and update the answer.

This works because it directly enforces the definition of the problem. However, its cost grows too quickly. There are O(n^2 m^2) rectangles, and each verification costs O(nm) in the worst case, leading to a theoretical O(n^3 m^3) bound. Even with n × m ≤ 400, this is far too slow in practice.

The key observation is that we do not actually need to recompute validity of every rectangle from scratch. Instead, we can reuse structure across rows. If we fix the bottom row, we can compress the grid into a histogram where each column stores how many consecutive 1s end at that row. Any all-ones rectangle ending at that row becomes a contiguous segment in this histogram. The problem then becomes the classic largest rectangle in a histogram, solved efficiently with a monotonic stack.

This transforms a 2D rectangle search into a sequence of 1D problems, each solvable in linear time per row.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((nm)^2 · nm) | O(1) | Too slow |
| Histogram DP + Stack | O(nm) | O(m) | Accepted |

## Algorithm Walkthrough

We process the grid row by row, maintaining an array that represents histogram heights of consecutive ones.

1. Initialize an array `height` of size m with zeros. This array represents, for each column, how many consecutive ones we have seen ending at the current row.
2. For each row, update the histogram by scanning columns. If the current cell is 1, increment `height[j]` by 1, otherwise reset it to 0. This step converts the 2D constraint into a 1D representation of vertical runs.
3. For the updated `height` array, compute the largest rectangle in a histogram. This is done using a monotonic increasing stack of indices. When we encounter a height smaller than the stack top, we repeatedly pop and compute areas using the popped height as the limiting height and the current index as the right boundary.
4. Keep track of the maximum area seen across all rows.
5. After processing all rows, output the maximum recorded area.

The crucial reasoning step is that every valid all-ones rectangle has a unique bottom row. By treating each row as a potential bottom boundary, we ensure that every rectangle is considered exactly once in the histogram phase.

### Why it works

At any row r, `height[c]` encodes the maximum possible height of a rectangle ending at r and extending upward in column c without interruption. Any all-ones rectangle with bottom row r corresponds to a contiguous segment of columns where all heights are at least the rectangle height. The histogram formulation captures exactly these constraints, so the largest rectangle in the histogram is exactly the best rectangle ending at row r. Since every rectangle has some bottom row, scanning all rows covers all possibilities.

## Python Solution

```python
import sys
input = sys.stdin.readline

def largest_histogram(heights):
    stack = []
    best = 0
    heights.append(0)
    
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            left = stack[-1] if stack else -1
            width = i - left - 1
            best = max(best, height * width)
        stack.append(i)
    
    heights.pop()
    return best

def solve():
    n, m = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(n)]
    
    height = [0] * m
    answer = 0
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                height[j] += 1
            else:
                height[j] = 0
        
        answer = max(answer, largest_histogram(height))
    
    print(answer)

if __name__ == "__main__":
    solve()
```

The implementation maintains a rolling histogram `height` that accumulates consecutive ones vertically. The helper function computes the best rectangle in linear time per row using a stack that enforces increasing heights. The sentinel zero appended to the histogram ensures that all remaining stack elements are flushed at the end of computation.

The only subtle implementation detail is resetting a column height to zero immediately upon encountering a zero cell, since any rectangle including that cell would become invalid.

## Worked Examples

### Example 1

Input:

```
2 2
1 1
1 1
```

Histogram evolution and computation:

| Row | Height array | Best histogram area |
| --- | --- | --- |
| 1 | [1, 1] | 2 |
| 2 | [2, 2] | 4 |

The second row produces a histogram where both columns reach height 2, forming a 2×2 rectangle.

This confirms that vertical accumulation correctly captures rectangles spanning multiple rows.

### Example 2

Input:

```
3 3
1 0 1
0 1 1
0 1 1
```

| Row | Height array | Best histogram area |
| --- | --- | --- |
| 1 | [1, 0, 1] | 1 |
| 2 | [0, 1, 2] | 2 |
| 3 | [0, 2, 3] | 4 |

At the last row, columns 2 and 3 form a growing staircase of heights, and the histogram identifies a 2×2 all-ones rectangle.

This demonstrates how the method naturally accumulates vertical continuity and converts it into horizontal width expansion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each row is processed in O(m), and histogram computation is linear due to monotonic stack operations |
| Space | O(m) | Only the height array and stack are stored |

Given n × m ≤ 400, this solution runs extremely fast, well within limits even with overhead from Python.

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

# provided samples
assert run("2 2\n1 1\n1 1\n") == "4"
assert run("3 3\n1 0 1\n0 1 1\n0 1 1\n") == "4"

# single cell
assert run("1 1\n1\n") == "1"

# all zeros
assert run("2 3\n0 0 0\n0 0 0\n") == "0"

# all ones larger rectangle
assert run("2 3\n1 1 1\n1 1 1\n") == "6"

# mixed pattern
assert run("3 4\n1 1 0 1\n1 1 1 1\n1 0 1 0\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 grid | 1 | minimal case |
| all zeros | 0 | no valid rectangle |
| full ones | 6 | full rectangle correctness |
| mixed grid | 4 | handling interruptions |

## Edge Cases

A fully zero grid tests whether the algorithm properly resets histogram heights instead of accumulating stale values. When every row is zero, the height array remains zero and the histogram always returns zero, producing the correct answer.

A single row grid reduces the problem to a pure histogram. The algorithm correctly computes the longest contiguous segment of ones, since all heights are either 0 or 1.

A fully one-filled grid tests maximum accumulation. Each row increases all histogram values, and the final row produces a histogram where the entire width is usable with maximal height, yielding n × m as expected.
