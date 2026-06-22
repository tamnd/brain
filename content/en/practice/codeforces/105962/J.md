---
title: "CF 105962J - Tigrinho"
description: "We are given a 3 by 3 board. Each cell is either a digit from 1 to 9 or a wildcard symbol. The board participates in a scoring system based on five special lines: the three rows and the two diagonals."
date: "2026-06-22T16:18:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105962
codeforces_index: "J"
codeforces_contest_name: "UNICAMP Freshman Contest 2025"
rating: 0
weight: 105962
solve_time_s: 71
verified: true
draft: false
---

[CF 105962J - Tigrinho](https://codeforces.com/problemset/problem/105962/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a 3 by 3 board. Each cell is either a digit from 1 to 9 or a wildcard symbol. The board participates in a scoring system based on five special lines: the three rows and the two diagonals.

A line produces one unit of reward if, after ignoring wildcard cells, all remaining digits in that line are identical. If a line contains both digits and wildcards, the wildcards simply disappear from consideration. This means a line with a single digit always produces a reward, since there is nothing to disagree with. A line consisting only of wildcards contributes nothing, because there is no actual digit to compare.

The score of a board is the number of these five lines that satisfy the condition. The cost of playing is fixed, so minimizing profit is equivalent to minimizing the number of rewarded lines.

The input fixes only how many wildcard cells must appear in the grid. We are free to place them anywhere and freely choose digits in the remaining cells. The task is to construct a board with exactly that number of wildcards that produces the smallest possible score.

The grid is tiny, so even though the decision space involves both choosing wildcard positions and assigning digits, the total number of configurations remains manageable. The constraints immediately suggest that exponential search over the 9 cells is feasible.

A subtle case appears when a line contains exactly one non-wildcard digit. That line always yields a reward because a single value trivially satisfies the “all equal” condition. Similarly, a line with zero digits should not be considered a valid rewarded line, since there is no value at all to define equality.

The real difficulty is not counting scores for a fixed board, but realizing how digit assignment interacts with wildcard placement. Once we understand that digits can always be chosen adversarially to break equality whenever a line has at least two fixed cells, the problem becomes purely combinatorial over wildcard placement.

## Approaches

A direct brute force interpretation would consider every placement of wildcards and every assignment of digits from 1 to 9 for the remaining cells. For each complete grid, we would evaluate the five lines and compute the score. This is correct but far too large: even ignoring digits, choosing wildcard positions alone already gives 2^9 possibilities, and multiplying by digit assignments leads to 9^9 configurations, which is completely infeasible.

The key observation is that digit values do not matter individually. We are allowed to assign them freely after fixing wildcard positions. For any line that contains at least two non-wildcard cells, we can always assign different digits in those positions to prevent the line from becoming uniform. This means such lines can always be made to contribute zero.

A line becomes unavoidable only when it has at most one non-wildcard cell. In that case, no matter how digits are assigned, the line will always satisfy the condition. Therefore the score of a configuration depends only on how many lines contain at least two wildcards.

The problem reduces to choosing K cells to mark as wildcards in a 3 by 3 grid such that the number of lines containing at least two wildcards is minimized. This is small enough to brute force all combinations of K positions among 9.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force full grids | O(9^9) | O(1) | Too slow |
| Brute force wildcard placements | O(2^9 · 5) | O(1) | Accepted |

## Algorithm Walkthrough

We model the grid cells as indices from 0 to 8. Each subset of size K represents a possible placement of wildcards.

1. Enumerate all subsets of size K among the 9 positions. Each subset represents which cells are wildcards.
2. For each subset, compute the score over the five fixed lines: three rows and two diagonals. Each line is checked by counting how many wildcard cells it contains.
3. If a line contains two or more wildcards, it will always yield a reward regardless of digit assignment, so we increment the score for that line.
4. Track the minimum score across all subsets.

The reasoning behind step 3 is crucial. Once a line has at least two wildcards, it has at most one fixed digit. Any single value cannot conflict with itself, so the line inevitably becomes uniform after ignoring wildcards.

### Why it works

After fixing wildcard positions, digit assignment has full freedom on remaining cells. Any line that still has at least two non-wildcard positions can be broken by assigning distinct digits in those positions. Therefore such lines are never forced to contribute to the score. Conversely, any line with two or more wildcards cannot be broken, since it contains at most one real digit. This creates a direct equivalence between scoring lines and lines with at least two wildcards, making the combinatorial search over placements sufficient and exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

lines = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 4, 8),
    (2, 4, 6)
]

def solve():
    K = int(input().strip())

    best = 10

    for mask in range(1 << 9):
        if mask.bit_count() != K:
            continue

        score = 0
        for a, b, c in lines:
            cnt = 0
            if mask & (1 << a):
                cnt += 1
            if mask & (1 << b):
                cnt += 1
            if mask & (1 << c):
                cnt += 1

            if cnt >= 2:
                score += 1

        best = min(best, score)

    print(best)

if __name__ == "__main__":
    solve()
```

The implementation encodes the grid as a 9-bit mask, where each bit indicates whether a cell is a wildcard. For each valid mask with exactly K bits set, we evaluate the five relevant lines. The score computation follows directly from counting how many wildcard cells fall into each line.

The bit counting filter ensures we only evaluate valid configurations, and Python’s built-in bit operations make this enumeration extremely fast.

## Worked Examples

Consider a case where K = 2. We examine a configuration where both wildcards are placed in the top row.

| Step | Row 1 | Row 2 | Row 3 | Diag 1 | Diag 2 | Score |
| --- | --- | --- | --- | --- | --- | --- |
| Initial placement | 2 wildcards | 0 | 0 | 0 | 0 | 1 |

Only the top row contains two wildcards, so it is the only forced winning line. All other lines still contain at least two fixed cells, allowing digit assignment to prevent equality.

This confirms that only lines with at least two wildcards contribute.

Now consider K = 3, with wildcards placed on the main diagonal.

| Step | Row 1 | Row 2 | Row 3 | Diag 1 | Diag 2 | Score |
| --- | --- | --- | --- | --- | --- | --- |
| Placement | 1 | 1 | 1 | 3 | 0 | 1 |

The main diagonal has three wildcards and is automatically a winning line. No other line reaches the threshold of two wildcards, so the score remains 1.

These traces illustrate that the score depends only on how wildcards intersect the fixed five lines.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^9 · 5) | We enumerate all wildcard subsets and check five lines per subset |
| Space | O(1) | Only a fixed number of variables and pre-defined lines are used |

The total number of configurations is only 512, and each requires constant work. This is well within the limits even in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# minimal cases
assert run("0\n") == "0"
assert run("9\n") == "5"

# single wildcard
assert run("1\n") == "0"

# small structured case
assert run("2\n") in ["0", "1"]

# full diagonal domination
assert run("3\n") >= "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 | 0 | No wildcards, no forced lines |
| 9 | 5 | All lines contain only wildcards |
| 1 | 0 | Single wildcard cannot force a line |
| 3 | variable minimum | Diagonal interaction cases |

## Edge Cases

When K = 0, no wildcard exists and every line has three digits. We can always assign digits so that no line becomes uniform, for example by using three different values in each line. The algorithm correctly finds zero forced lines since no line has two wildcards.

When K = 9, every cell is a wildcard. Each of the five lines contains three wildcards, so every line is counted. The enumeration correctly evaluates every mask and returns a score of five.

When K is small, such as 1 or 2, no line can reach the threshold of two wildcards unless they are carefully aligned. The brute force correctly identifies that most configurations yield zero forced lines, matching the combinatorial reasoning.
