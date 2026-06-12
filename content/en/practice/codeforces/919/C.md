---
title: "CF 919C - Seat Arrangements"
description: "We are given a classroom represented as a grid. Each cell is either empty (.) or occupied (). We want to seat exactly k students in a straight line. The seats must be consecutive and must lie entirely within a single row or entirely within a single column."
date: "2026-06-13T02:43:10+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 919
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 460 (Div. 2)"
rating: 1300
weight: 919
solve_time_s: 832
verified: true
draft: false
---

[CF 919C - Seat Arrangements](https://codeforces.com/problemset/problem/919/C)

**Rating:** 1300  
**Tags:** brute force, implementation  
**Solve time:** 13m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a classroom represented as a grid. Each cell is either empty (`.`) or occupied (`*`).

We want to seat exactly `k` students in a straight line. The seats must be consecutive and must lie entirely within a single row or entirely within a single column. Every seat in that chosen segment must be empty.

The task is to count how many distinct valid segments exist.

A segment is identified by its set of occupied cells. For example, if a row contains four consecutive empty seats and `k = 2`, then the intervals `[1,2]`, `[2,3]`, and `[3,4]` are three different arrangements.

The grid dimensions can be as large as `2000 × 2000`. That means the grid may contain up to four million cells. Any solution that repeatedly scans the same cells or checks every possible segment independently will become too slow. A successful solution should process each cell only a constant number of times, leading to roughly `O(nm)` work.

There are several edge cases that deserve attention.

Consider `k = 1`:

```
2 2 1
..
..
```

Every empty cell is simultaneously a valid horizontal segment and a valid vertical segment. The correct answer is `4`, not `8`. If we count rows and columns independently, every empty cell gets counted twice.

Another important case occurs when a run of empty seats is longer than `k`.

```
1 5 3
.....
```

The valid segments are:

```
[1,2,3]
[2,3,4]
[3,4,5]
```

The answer is `3`. A careless implementation might count only one segment per run.

Blocked cells split runs into independent pieces.

```
1 5 2
..*..
```

The left run contributes one arrangement, the right run contributes one arrangement, for a total of `2`. Treating the entire row as one run would incorrectly produce `4`.

## Approaches

The most direct solution is brute force. For every cell, we could try to start a horizontal segment of length `k` and check whether all `k` cells are empty. We could do the same vertically.

This is correct because every possible segment is examined exactly once. The problem is the running time. There are `O(nm)` possible starting positions, and each check may inspect up to `k` cells. In the worst case this becomes `O(nmk)`. With all dimensions reaching `2000`, that can approach billions of operations.

The key observation is that we do not actually care about individual cells. What matters are maximal consecutive runs of empty seats.

Suppose a row contains a run of length `L`.

```
.....   (L = 5)
```

If we need `k = 3`, then every consecutive block of length `3` inside this run is valid. The number of such blocks is:

```
L - k + 1
```

provided `L ≥ k`.

Instead of checking every candidate segment separately, we scan the row once, identify each empty run, and immediately add its contribution. The same idea works for columns.

There is one special situation: `k = 1`.

For larger `k`, horizontal and vertical segments are different objects, so counting rows and columns independently is correct.

For `k = 1`, every valid arrangement consists of a single empty cell. Counting rows and columns separately would count each empty cell twice. In that case we simply count empty cells once and stop.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nmk) | O(1) | Too slow |
| Optimal | O(nm) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Read the grid.
2. If `k = 1`, count the number of cells containing `.` and output that value.

Every empty cell represents exactly one valid arrangement. Counting rows and columns separately would double count.
3. Scan every row from left to right.

Maintain the length of the current consecutive run of empty cells.
4. Whenever a `*` is encountered, the current run ends.

If the run length is `L ≥ k`, add `L - k + 1` to the answer, because that many length-`k` segments fit inside the run.
5. After finishing the row, process the final run in the same way.

A row may end with empty cells, so the last run needs separate handling.
6. Repeat the same process for every column.

Each column is treated as a one-dimensional sequence. Every vertical run contributes `L - k + 1` arrangements.
7. Output the accumulated answer.

### Why it works

Every valid horizontal arrangement belongs to exactly one maximal horizontal run of empty cells. If that run has length `L`, the possible starting positions of a length-`k` segment are:

```
1, 2, ..., L-k+1
```

which gives exactly `L-k+1` arrangements.

The algorithm counts precisely those arrangements for every horizontal run and every vertical run. No valid segment is missed because every segment lies inside some run. No segment is counted twice because a segment has exactly one maximal containing run. The special handling of `k = 1` removes the only case where horizontal and vertical counting would overlap.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    if k == 1:
        ans = sum(row.count('.') for row in grid)
        print(ans)
        return

    ans = 0

    # Rows
    for r in range(n):
        run = 0
        for c in range(m):
            if grid[r][c] == '.':
                run += 1
            else:
                if run >= k:
                    ans += run - k + 1
                run = 0

        if run >= k:
            ans += run - k + 1

    # Columns
    for c in range(m):
        run = 0
        for r in range(n):
            if grid[r][c] == '.':
                run += 1
            else:
                if run >= k:
                    ans += run - k + 1
                run = 0

        if run >= k:
            ans += run - k + 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The first branch handles the special case `k = 1`. Every empty cell is a valid arrangement, so counting empty cells directly is both simpler and avoids double counting.

The row scan treats each row as a one-dimensional array. The variable `run` stores the length of the current consecutive block of empty seats. Whenever a blocked seat appears, the run ends and contributes `run - k + 1` segments if its length is large enough.

The column scan is identical except that indices are traversed vertically.

A common source of bugs is forgetting to process the final run after finishing a row or column. A run may continue until the boundary, so the contribution must be added after the loop as well.

Another easy mistake is mishandling `k = 1`. Without the special branch, every empty cell would be counted once in the row scan and once in the column scan.

## Worked Examples

### Example 1

Input:

```
2 3 2
**.
...
```

#### Row scan

| Row | Runs of '.' | Contribution |
| --- | --- | --- |
| `**.` | 1 | 0 |
| `...` | 3 | 2 |

Current answer = 2.

#### Column scan

| Column | Pattern | Run Length | Contribution |
| --- | --- | --- | --- |
| 1 | `*.` | 1 | 0 |
| 2 | `*.` | 1 | 0 |
| 3 | `..` | 2 | 1 |

Final answer = 3.

This example shows both types of arrangements. The second row contributes two horizontal segments, while the third column contributes one vertical segment.

### Example 2

Input:

```
1 5 3
.....
```

#### Row scan

| Row | Run Length | Contribution |
| --- | --- | --- |
| `.....` | 5 | 3 |

Current answer = 3.

#### Column scan

| Column | Run Length | Contribution |
| --- | --- | --- |
| 1 | 1 | 0 |
| 2 | 1 | 0 |
| 3 | 1 | 0 |
| 4 | 1 | 0 |
| 5 | 1 | 0 |

Final answer = 3.

This trace demonstrates the formula `L - k + 1`. A run of length five contains exactly three length-three segments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each cell is visited once during row scanning and once during column scanning |
| Space | O(nm) | The input grid is stored in memory |

The grid contains at most four million cells. The algorithm performs only a constant amount of work per cell, which comfortably fits within the limits. The memory usage is dominated by storing the grid itself.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m, k = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    if k == 1:
        return str(sum(row.count('.') for row in grid))

    ans = 0

    for r in range(n):
        run = 0
        for c in range(m):
            if grid[r][c] == '.':
                run += 1
            else:
                if run >= k:
                    ans += run - k + 1
                run = 0
        if run >= k:
            ans += run - k + 1

    for c in range(m):
        run = 0
        for r in range(n):
            if grid[r][c] == '.':
                run += 1
            else:
                if run >= k:
                    ans += run - k + 1
                run = 0
        if run >= k:
            ans += run - k + 1

    return str(ans)

# provided sample
assert run("2 3 2\n**.\n...\n") == "3", "sample 1"

# minimum size
assert run("1 1 1\n.\n") == "1", "single empty cell"

# all blocked
assert run("2 2 1\n**\n**\n") == "0", "no valid arrangement"

# long run
assert run("1 5 3\n.....\n") == "3", "L-k+1 counting"

# split runs
assert run("1 5 2\n..*..\n") == "2", "blocked seat splits runs"

# k = 1 double-count trap
assert run("2 2 1\n..\n..\n") == "4", "must not count rows and columns separately"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` with `.` | `1` | Minimum grid size |
| `2 2 1` all `*` | `0` | No valid arrangements |
| `1 5 3` with all `.` | `3` | Formula `L-k+1` |
| `1 5 2` with `..*..` | `2` | Run splitting at obstacles |
| `2 2 1` all `.` | `4` | Correct handling of `k=1` |

## Edge Cases

### Case 1: `k = 1`

Input:

```
2 2 1
..
..
```

The algorithm immediately enters the special branch and counts empty cells. There are four empty cells, so the answer is `4`.

If we had performed both row and column scans, each cell would contribute once horizontally and once vertically, producing `8`, which is incorrect.

### Case 2: Long empty run

Input:

```
1 5 3
.....
```

The row scan finds a single run with length `5`.

The contribution is:

```
5 - 3 + 1 = 3
```

corresponding to starting positions 1, 2, and 3. The algorithm counts all valid segments without enumerating them individually.

### Case 3: Obstacle splits a run

Input:

```
1 5 2
..*..
```

The scan discovers two separate runs of length `2`.

The first run contributes:

```
2 - 2 + 1 = 1
```

The second run contributes another `1`.

Total answer:

```
1 + 1 = 2
```

The obstacle prevents segments from crossing the middle position, and the algorithm naturally enforces that by terminating the current run whenever a `*` is encountered.
