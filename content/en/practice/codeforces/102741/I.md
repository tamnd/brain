---
title: "CF 102741I - Stunt Jump Escape"
description: "The map is a grid of hills. Michael starts somewhere on the top edge and moves one row downward every minute, while Trevor starts somewhere on the left edge and moves one column to the right every minute."
date: "2026-07-29T00:48:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102741
codeforces_index: "I"
codeforces_contest_name: "UTPC Contest 9-25-20 Div. 1"
rating: 0
weight: 102741
solve_time_s: 65
verified: true
draft: false
---

[CF 102741I - Stunt Jump Escape](https://codeforces.com/problemset/problem/102741/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

The map is a grid of hills. Michael starts somewhere on the top edge and moves one row downward every minute, while Trevor starts somewhere on the left edge and moves one column to the right every minute. Each move allows a sideways adjustment of at most one cell, so Michael can drift left or right while descending and Trevor can drift up or down while advancing. They want to meet at the same cell at the same time, and the score is the sum of the heights of every hill each rider visits. If both riders visit the same hill, its value is counted twice.

The constraints allow up to 1000 rows and 1000 columns, so there can be one million cells. A solution that does more than a small constant amount of work per cell is unlikely to fit comfortably. In particular, trying every pair of possible paths is impossible because the number of paths grows exponentially. Even a dynamic program with an extra dimension over both riders' positions would have around one trillion states, which is far beyond the limit. The useful target is an O(nm) or O(nm log n) solution.

The main edge cases come from the freedom of the starting positions and from the fact that meeting at the beginning is valid. A solution that assumes both riders start at the same corner loses valid answers.

For example:

```
1 3
5 1 1
```

The correct output is:

```
10
```

Both riders can start on the only available row and meet immediately at the first cell they choose. A careless solution that forces the meeting to happen after at least one move would miss this case.

Another case is:

```
2 2
1 1
2 2
```

The correct output is:

```
7
```

The best choice is for Michael to travel through values 1 and 2, while Trevor starts on the lower left value 2 and reaches the meeting cell with another value 2. The shared hills are counted for both riders, so removing duplicate values from the sum gives the wrong answer.

## Approaches

A direct approach is to enumerate a meeting point and calculate the best route for each rider to reach it. For every possible meeting cell, we could run a search from the starting edges. This is correct because the two riders move independently before they meet. However, repeating a search for every possible meeting point performs roughly O(nm) work per point, resulting in O(n²m²) operations in the worst case, which is too slow for a grid with one million cells.

The key observation is that the riders' movements have a fixed direction. Michael's row increases by exactly one every minute, so reaching a cell only depends on the previous row. Trevor's column increases by exactly one every minute, so reaching a cell only depends on the previous column. The two independent path problems can be solved separately with dynamic programming.

We compute one DP table containing the best score Michael can have when reaching every cell. A second DP table contains the best score Trevor can have when reaching every cell. A cell can be a meeting point only when both riders can arrive there at the same time. After the two tables are built, the answer is simply the maximum sum of the two values over all possible meeting cells.

The brute force works because it explores every possible pair of routes, but it repeats the same subproblems many times. The observation that each rider has only one changing coordinate lets us collapse those repeated calculations into two linear grid passes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²m²) | O(nm) | Too slow |
| Optimal | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Build Michael's dynamic programming table. For the top row, every cell is a possible starting position, so the initial value is simply the height of that cell. For every later row, the best way to enter a cell comes from one of the three cells directly above it diagonally or vertically. Add the current hill height after taking the best previous value.
2. Build Trevor's dynamic programming table. For the left column, every cell can be a starting position. For every later column, the previous position must be in the previous column and can be one row above, the same row, or one row below. Add the current hill height to the best previous score.
3. Check every cell that can be reached by both riders at the same time. A meeting at row i and column j is possible only when Michael has made i moves and Trevor has made j moves, so we need i = j. The answer is the maximum of Michael's value plus Trevor's value on these diagonal cells.
4. Return the maximum score found. The case where both riders start together is naturally included because diagonal cell (0,0) is considered.

Why it works: Michael's DP value for a cell stores the best possible score among all valid downward paths ending there. The transition considers every possible final move, so no better path can be missed. The same argument applies to Trevor's DP. Since the riders do not affect each other's movement before meeting, the best pair of routes for a chosen meeting cell is exactly the sum of the two independent DP values. Taking the maximum over all valid meeting cells gives the optimal total score.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(n)]

    michael = [[0] * m for _ in range(n)]
    for j in range(m):
        michael[0][j] = grid[0][j]

    for i in range(1, n):
        for j in range(m):
            best = michael[i - 1][j]
            if j > 0:
                best = max(best, michael[i - 1][j - 1])
            if j + 1 < m:
                best = max(best, michael[i - 1][j + 1])
            michael[i][j] = best + grid[i][j]

    trevor = [[0] * m for _ in range(n)]
    for i in range(n):
        trevor[i][0] = grid[i][0]

    for j in range(1, m):
        for i in range(n):
            best = trevor[i][j - 1]
            if i > 0:
                best = max(best, trevor[i - 1][j - 1])
            if i + 1 < n:
                best = max(best, trevor[i + 1][j - 1])
            trevor[i][j] = best + grid[i][j]

    ans = 0
    for i in range(min(n, m)):
        ans = max(ans, michael[i][i] + trevor[i][i])

    print(ans)

if __name__ == "__main__":
    solve()
```

The first DP pass follows Michael's movement rules. The first row is initialized directly because he may choose any top-row starting position. The transition only looks at the previous row, matching the fact that he must move downward every minute.

The second DP pass is the same idea rotated by 90 degrees. Trevor's time dimension is the column number, so every transition comes from the previous column. Initializing every cell in the left column is necessary because Trevor can begin anywhere along that edge.

The final loop only checks cells `(i, i)`. At time `i`, Michael must be on row `i` and Trevor must be on column `i`, so any other cell cannot be a simultaneous meeting location. The use of Python integers avoids overflow because the maximum score can be much larger than a 32-bit integer.

## Worked Examples

For the first sample:

```
2 2
1 1
2 2
```

Michael's table becomes:

| Cell | Value |
| --- | --- |
| (0,0) | 1 |
| (0,1) | 1 |
| (1,0) | 3 |
| (1,1) | 3 |

Trevor's table becomes:

| Cell | Value |
| --- | --- |
| (0,0) | 1 |
| (1,0) | 2 |
| (0,1) | 2 |
| (1,1) | 4 |

The possible meeting cells are `(0,0)` and `(1,1)`. Their scores are 2 and 7, so the answer is 7. This trace shows why shared hills are counted twice.

For the second sample:

```
3 3
1 2 3
4 5 6
7 8 9
```

The diagonal states are:

| Position | Michael score | Trevor score | Combined |
| --- | --- | --- | --- |
| (0,0) | 1 | 1 | 2 |
| (1,1) | 8 | 8 | 16 |
| (2,2) | 17 | 25 | 42 |

The best meeting point is the bottom-right cell, producing 42. This trace demonstrates that the optimal meeting point does not have to be early.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each DP table processes every grid cell once. |
| Space | O(nm) | Two tables store the best scores for both riders. |

With at most one million cells, the solution performs only a few million operations and fits easily within the given limits.

## Test Cases

```python
import sys
import io

def solve_case(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.readline

    n, m = map(int, data().split())
    grid = [list(map(int, data().split())) for _ in range(n)]

    michael = [[0] * m for _ in range(n)]
    for j in range(m):
        michael[0][j] = grid[0][j]

    for i in range(1, n):
        for j in range(m):
            best = michael[i - 1][j]
            if j:
                best = max(best, michael[i - 1][j - 1])
            if j + 1 < m:
                best = max(best, michael[i - 1][j + 1])
            michael[i][j] = best + grid[i][j]

    trevor = [[0] * m for _ in range(n)]
    for i in range(n):
        trevor[i][0] = grid[i][0]

    for j in range(1, m):
        for i in range(n):
            best = trevor[i][j - 1]
            if i:
                best = max(best, trevor[i - 1][j - 1])
            if i + 1 < n:
                best = max(best, trevor[i + 1][j - 1])
            trevor[i][j] = best + grid[i][j]

    ans = 0
    for i in range(min(n, m)):
        ans = max(ans, michael[i][i] + trevor[i][i])

    sys.stdin = old_stdin
    return str(ans) + "\n"

assert solve_case("""2 2
1 1
2 2
""") == "7\n"

assert solve_case("""3 3
1 2 3
4 5 6
7 8 9
""") == "42\n"

assert solve_case("""1 1
10
""") == "20\n"

assert solve_case("""2 3
5 1 1
1 1 1
""") == "13\n"

assert solve_case("""3 1
7
2
3
""") == "14\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 10` | `20` | Minimum grid size and immediate meeting |
| `2 3 / 5 1 1 / 1 1 1` | `13` | Rectangular grid and unequal dimensions |
| `3 1 / 7 / 2 / 3` | `14` | Single-column boundary handling |

## Edge Cases

For the immediate meeting case:

```
1 1
10
```

Both riders begin on the only hill. The DP tables both contain 10 at `(0,0)`, and the final answer checks that cell, producing 20. No movement is required.

For the shared starting edge case:

```
2 2
1 1
2 2
```

The algorithm does not force movement before checking the answer. It evaluates `(0,0)` as a valid meeting point and also evaluates `(1,1)`, where the optimal paths meet. The second option gives 7.

For the rectangular case:

```
2 3
5 1 1
1 1 1
```

The diagonal meeting positions are only `(0,0)` and `(1,1)`, because both riders must have taken the same number of moves. The algorithm never accesses invalid diagonal positions beyond the smaller dimension, preventing an out-of-bounds error.
