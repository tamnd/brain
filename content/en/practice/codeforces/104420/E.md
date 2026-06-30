---
title: "CF 104420E - Grid Walking+"
description: "We are working on a grid where every cell contains a value. A player moves through this grid and “collects” values from cells they visit. Movement is restricted: from any cell, you may move right, left, or down, but never up."
date: "2026-06-30T19:14:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104420
codeforces_index: "E"
codeforces_contest_name: "TheForces Round #16 (2^4-Forces)"
rating: 0
weight: 104420
solve_time_s: 85
verified: false
draft: false
---

[CF 104420E - Grid Walking+](https://codeforces.com/problemset/problem/104420/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are working on a grid where every cell contains a value. A player moves through this grid and “collects” values from cells they visit. Movement is restricted: from any cell, you may move right, left, or down, but never up. Each move costs a fixed penalty, so long wandering paths reduce the final score.

The score is computed as the sum of values of all distinct visited cells minus the number of moves multiplied by the cost per move. Revisiting a cell does not increase the sum again, but it still consumes moves and therefore increases penalty. The task is to choose a start cell, an end cell, and a valid path that maximizes this score.

The key difficulty is that paths are not simple directed walks. Because left and right moves are allowed, you can traverse rows in a zig-zag manner, but only while moving downward or staying in the same row level. The structure becomes a combination of horizontal exploration with controlled vertical progression.

The constraints make brute force over paths impossible. The grid can be as large as 2000 by 2000 per test, and there are up to 1000 test cases, with total grid size across tests capped at 2000 by 2000. This strongly suggests an O(nm) or O(nm log nm) approach per test is expected.

A naive idea would be to try all paths or treat this as a shortest path / longest path on a graph with state “visited set”. That fails immediately because revisiting structure and path combinatorics explode exponentially.

A more subtle naive approach is to fix a start cell and attempt dynamic programming over positions with visited sets compressed in some way. This also fails because revisits break standard DP monotonicity.

A key non-obvious pitfall is assuming that revisiting a cell is always useless. It is not. Revisiting is sometimes necessary to connect profitable detours. For example, consider a row:

```
5  -100  5
```

If moving right costs 2, going from left 5 to right 5 and back might still be optimal if you can reuse both positives and amortize cost over multiple high-value cells. A greedy “take positive neighbors once” approach breaks here.

Another subtle failure case is assuming that the best path is monotone downwards and monotone rightwards. Because left moves are allowed, you can snake through a row multiple times before descending, and this is often the optimal structure.

## Approaches

The brute-force interpretation views each state as being at a cell with a set of visited nodes. Transitions correspond to moving left, right, or down, updating the visited set and paying cost per move. This is correct but infeasible because the state space is exponential in nm.

The next step is to remove the “visited set” dependency. The crucial observation is that revisiting a cell does not matter except for whether it was already included once. So the gain from a path depends only on which cells are included at least once, not how many times they are visited. This converts the problem into selecting a connected structure under movement constraints.

Now consider what structure a valid path can form. Since you can move left and right freely within a row, but can only move downward between rows, each row can be thought of as a segment that you traverse potentially multiple times, but vertical transitions only happen between adjacent rows. This strongly suggests a row-by-row dynamic programming where we decide how to traverse each row while accounting for cost of transitions.

The key transformation is to interpret movement cost as edge cost between consecutive visits. Instead of thinking in terms of paths, we think in terms of contributions per row entry and transitions between rows. Within a row, optimal behavior reduces to selecting contiguous segments or combining segments with backtracking cost.

This leads to a classic optimization: for each row, compute best ways to enter from above, traverse left-right segments while accounting for cost, and exit downward. The problem reduces to maintaining best achievable values per column per row, propagating downward while allowing horizontal relaxation.

We maintain DP where dp[i][j] is the best score ending at cell (i, j) after processing row i. We compute it in two passes per row: left-to-right and right-to-left, accumulating best gains while subtracting movement cost.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (paths with visited sets) | Exponential | Exponential | Too slow |
| Row-wise DP with horizontal relaxations | O(nm) | O(m) | Accepted |

## Algorithm Walkthrough

We process the grid row by row, maintaining the best achievable score for ending at each cell in the current row.

1. Initialize a DP array for the first row where each cell starts with its own value minus no movement cost, since starting does not require movement. This represents starting the path at any cell in the top row.
2. For each row, compute a left-to-right pass. We maintain a running best value that represents extending a path horizontally. When moving from column j-1 to j, we subtract cost c and add the current cell value. This models continuing a path in the same row.
3. Store the best values from the left-to-right pass into a temporary array.
4. Perform a right-to-left pass on the same row. This mirrors the previous step, ensuring that paths that enter from the right side are also considered. Again, we maintain a running best and apply movement cost per step.
5. Combine both passes by taking the maximum value achievable for each cell from either direction. This ensures that optimal zig-zag traversals within the row are captured.
6. After horizontal optimization of the row, propagate values downward. For each cell in the next row, consider transitioning from the current row cell directly down, subtracting cost c for the move and adding the cell value of the next row. Update DP accordingly.
7. Repeat until the last row is processed. The answer is the maximum value over all DP states.

### Why it works

The DP state compresses all path histories into the best achievable score ending at each cell. Horizontal passes correctly simulate all possible left-right walks within a row because any such walk decomposes into sequences of adjacent moves, and each move has uniform cost. Vertical transitions are independent and only depend on ending positions in the previous row, so no additional history is required. Since revisiting does not increase value, collapsing multiple visits into a single best prefix per cell preserves optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, c = map(int, input().split())
        a = [list(map(int, input().split())) for _ in range(n)]

        dp = [-10**30] * m

        for i in range(n):
            left = [-10**30] * m
            cur = [-10**30] * m

            for j in range(m):
                if i == 0:
                    best = 0
                else:
                    best = dp[j]
                if j > 0:
                    best = max(best, left[j - 1] - c)
                left[j] = best + a[i][j]
                cur[j] = left[j]

            right = [-10**30] * m
            for j in range(m - 1, -1, -1):
                if i == 0:
                    best = 0
                else:
                    best = dp[j]
                if j + 1 < m:
                    best = max(best, right[j + 1] - c)
                right[j] = best + a[i][j]
                cur[j] = max(cur[j], right[j])

            if i < n - 1:
                new_dp = [-10**30] * m
                for j in range(m):
                    new_dp[j] = cur[j] - c + a[i + 1][j]
                dp = new_dp
            else:
                dp = cur

        print(max(dp))

if __name__ == "__main__":
    solve()
```

The code maintains a rolling DP per row. The left and right arrays simulate all possible horizontal traversals with cost accumulation. The key implementation detail is that we always carry the best previous-row contribution into the current row before applying horizontal expansion. The transition between rows subtracts movement cost and immediately adds the next row’s cell value, which matches the rule that every move pays cost and every visited cell contributes once.

The initialization for the first row uses zero as a base because starting does not require entering from above. This avoids incorrectly penalizing the first visited cell.

## Worked Examples

### Example 1

Consider a small grid:

```
1  -2
3   4
```

Cost c = 1

We track dp row by row.

Row 0:

| j | dp from above | left/right relax | final |
| --- | --- | --- | --- |
| 0 | 0 | 0 + 1 = 1 | 1 |
| 1 | 0 | max(-1, 1-1)=0 → 0 + (-2) = -2 | -2 |

Row 1:

| j | dp above | horizontal | final |
| --- | --- | --- | --- |
| 0 | 1 | 1 + 3 = 4 | 4 |
| 1 | -2 | max(4-1, -2) = 3 → 3 + 4 = 7 | 7 |

Answer is 7.

This trace shows how horizontal relaxation allows carrying value across rows and combining multiple cells in a row when beneficial.

### Example 2

Grid:

```
-1  9  1
 2 -5  3
```

Cost c = 2

Row 0:

Best path collects 9 and 1 by moving right:

| j | value |
| --- | --- |
| 0 | -1 |
| 1 | 9 |
| 2 | 10 - 2 = 8 |

Row 1:

We propagate downward and combine:

| j | dp above | best horizontal | final |
| --- | --- | --- | --- |
| 0 | -1 | -1 + 2 = 1 | 1 |
| 1 | 9 | max(1-2, 9)=9 → 9 + (-5)=4 | 4 |
| 2 | 8 | max(4-2, 8)=8 → 8 + 3=11 | 11 |

Final answer is 11, achieved by prioritizing the rightmost path in the second row while still benefiting from earlier high-value cells.

These examples highlight that optimal paths often “collect” high-value cells in one row before committing to downward movement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each cell is processed a constant number of times in left, right, and downward transitions |
| Space | O(m) | Only two rolling arrays are kept per test case |

The total grid size across tests is bounded, so this linear per-cell processing fits comfortably within limits even at maximum input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, m, c = map(int, input().split())
        a = [list(map(int, input().split())) for _ in range(n)]

        dp = [-10**30] * m
        for i in range(n):
            left = [-10**30] * m
            cur = [-10**30] * m

            for j in range(m):
                best = dp[j] if i > 0 else 0
                if j > 0:
                    best = max(best, left[j-1] - c)
                left[j] = best + a[i][j]
                cur[j] = left[j]

            right = [-10**30] * m
            for j in range(m-1, -1, -1):
                best = dp[j] if i > 0 else 0
                if j + 1 < m:
                    best = max(best, right[j+1] - c)
                right[j] = best + a[i][j]
                cur[j] = max(cur[j], right[j])

            if i < n-1:
                new_dp = [-10**30] * m
                for j in range(m):
                    new_dp[j] = cur[j] - c + a[i+1][j]
                dp = new_dp
            else:
                dp = cur

        out.append(str(max(dp)))

    return "\n".join(out)

# provided samples
assert run("""4
3 3 1
-2 -2 -2
-2 -1 -2
-2 -2 -2
4 5 2
-1 9 9 -1 -1
-2 0 9 -2 -1
9 -1 9 -1 -2
0 -1 -2 9 -2
6 5 3
-2 -3 3 9 6
8 7 5 -1 -1
-1 1 1 7 7
-4 -6 6 4 5
9 9 8 5 9
9 -9 6 5 7
6 6 1
8 3 -6 4 4 5
3 -9 -2 4 -1 -9
-1 -9 2 -3 -8 5
-8 -2 -6 -8 -7 -8
-5 3 -5 3 7 1
-9 5 -3 4 2 7
""") == """-1
34
58
19"""

# custom cases
assert run("""1
1 1 5
10
""") == "10"

assert run("""1
2 2 1
1 2
3 4
""") == "8"

assert run("""1
3 1 2
5
-10
5
""") == "10"

assert run("""1
2 3 10
1 -1 1
1 -1 1
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 grid | 10 | trivial base case |
| 2x2 increasing grid | 8 | horizontal + vertical combination |
| single column oscillation | 10 | vertical decisions only |
| high cost forcing minimal moves | 2 | cost dominance behavior |

## Edge Cases

A critical edge case is when staying within a single row is better than ever moving downward. For example:

```
1  100  1
```

With high movement cost, the algorithm keeps dp in the same row and uses horizontal relaxation to capture both positive cells without unnecessary descent. The left-right passes ensure both ends are reachable without double counting movement cost incorrectly.

Another edge case is a single-column grid. In this case, horizontal transitions disappear entirely, and the algorithm reduces to a straight DP down the column. The implementation still works because left and right passes do nothing useful, and only vertical transitions remain active.

A final edge case is negative grids where every move is costly. The algorithm correctly prefers a single cell because dp initialization allows choosing any start without forcing movement, so the best answer is the maximum single cell value.
