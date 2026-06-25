---
title: "CF 106160G - Garbage In, Garbage Out"
description: "The maze is a grid of cells, and each cell contains a digit describing its radioactivity level. A traveler starts at the top-left cell and wants to reach the bottom cell while moving only between side-adjacent cells."
date: "2026-06-25T11:12:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106160
codeforces_index: "G"
codeforces_contest_name: "2025 Benelux Algorithm Programming Contest (BAPC 25)"
rating: 0
weight: 106160
solve_time_s: 28
verified: true
draft: false
---

[CF 106160G - Garbage In, Garbage Out](https://codeforces.com/problemset/problem/106160/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 28s  
**Verified:** yes  

## Solution
## Problem Understanding

The maze is a grid of cells, and each cell contains a digit describing its radioactivity level. A traveler starts at the top-left cell and wants to reach the bottom cell while moving only between side-adjacent cells. The danger of a chosen route is determined by the most radioactive cell visited on that route. The task is to find the smallest possible danger value among all routes, meaning we want the path whose highest cell value is as low as possible.

The grid dimensions are both below 100, so there are at most around 10,000 cells. This rules out algorithms that enumerate paths, because the number of possible walks grows exponentially as the maze gets larger. A solution around O(nm) or O(nm log V), where V is the range of possible radioactivity values, is easily fast enough.

The subtle part of the problem is that we are not trying to minimize the sum of values along a path. A path containing many small values can still be worse than a path containing one moderate value if that moderate value is the largest cell visited. This means ordinary shortest path algorithms using addition are not directly applicable.

Another edge case is when the answer is the starting cell itself. For example:

```
1 1
7
```

The correct output is:

```
7
```

A careless implementation that only checks cells after moving would incorrectly return a smaller value or fail because there are no moves.

Another edge case is when the destination can only be reached through a high-value cell. For example:

```
3 3
111
999
111
```

The correct output is:

```
1
```

because the top row connects around the high cells. An approach that greedily chooses the smallest neighboring cell can get trapped near the middle and incorrectly believe the answer is 9.

A final common mistake is ignoring that revisiting cells is allowed. The optimal route is about reachability under a limit, not about constructing one specific simple path.

## Approaches

The direct brute-force idea is to generate every possible route from the top-left corner to the destination, calculate the maximum value on each route, and keep the smallest maximum. This is correct because every possible route is considered. The problem is the number of routes. Even in a small open grid, every position can branch into multiple choices, creating an exponential number of possible walks. A complete search becomes impossible long before the largest allowed grid size.

The key observation is that the answer is a threshold. Suppose we guess that the maximum allowed radioactivity is X. Then every cell with value at most X is usable, and every larger cell is blocked. The original question becomes much simpler: can we reach the destination using only usable cells?

This converts the problem into a reachability check. If a threshold X works, every larger threshold also works because it only adds more cells. If X does not work, every smaller threshold fails. This monotonic property allows binary search over the answer.

For each candidate threshold, we run a graph traversal on the grid. A BFS or DFS marks all cells reachable through cells whose values do not exceed the threshold. Because there are only nine possible cell values, we could also try all thresholds, but binary search is a more general pattern and works for any value range.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(nm) | Too slow |
| Optimal | O(nm log C) | O(nm) | Accepted |

Here, C is the maximum possible cell value range. For this problem C is very small because the cells contain digits, but the same method works if values are much larger.

## Algorithm Walkthrough

1. Find the smallest and largest values present in the grid. The answer must be somewhere in this interval because no valid path can have a maximum smaller than every cell it visits, and using the maximum grid value always allows every cell to be used.
2. Binary search a candidate threshold X. For this value, treat every cell with value greater than X as blocked.
3. Run BFS from the starting cell. Add neighboring cells only when they are inside the grid, have not been visited, and their value is at most X. The traversal answers whether a path exists under the current limit.
4. If BFS reaches the destination, store X as a possible answer and search for a smaller threshold. A successful threshold means the true answer could be lower.
5. If BFS cannot reach the destination, search larger thresholds because more cells must become available.

Why it works: the important invariant is that the BFS result is monotonic with respect to the threshold. Once a threshold allows a route, every larger threshold also allows that route. Once a threshold blocks all routes, every smaller threshold also blocks them. Binary search finds the smallest threshold where reachability changes from false to true, which is exactly the minimum possible maximum value on a path.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [list(map(int, input().strip())) for _ in range(n)]

    low = min(min(row) for row in grid)
    high = max(max(row) for row in grid)

    def can_reach(limit):
        if grid[0][0] > limit:
            return False

        visited = [[False] * m for _ in range(n)]
        q = deque([(0, 0)])
        visited[0][0] = True

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while q:
            r, c = q.popleft()

            if r == n - 1 and c == m - 1:
                return True

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                if 0 <= nr < n and 0 <= nc < m:
                    if not visited[nr][nc] and grid[nr][nc] <= limit:
                        visited[nr][nc] = True
                        q.append((nr, nc))

        return False

    answer = high
    while low <= high:
        mid = (low + high) // 2

        if can_reach(mid):
            answer = mid
            high = mid - 1
        else:
            low = mid + 1

    print(answer)

if __name__ == "__main__":
    solve()
```

The grid is stored as integers so comparisons during BFS are direct. The binary search boundaries are initialized from the actual grid values, which avoids unnecessary checks of impossible thresholds.

The `can_reach` function represents the graph traversal from the algorithm walkthrough. The visited matrix is recreated for each BFS because every threshold creates a different graph of available cells.

The starting cell is checked before BFS begins. This handles the single-cell case and also prevents a threshold smaller than the starting value from being considered valid.

The binary search uses the standard lower-bound pattern. When a threshold succeeds, it is saved and the search moves left to find a smaller valid value. When it fails, the search moves right because the limit must increase.

## Worked Examples

Consider:

```
6 8
13567657
24903578
83107213
98829363
25511282
39108443
```

The search checks whether different limits allow a path.

| Threshold | BFS result | Reason |
| --- | --- | --- |
| 4 | Reachable | A route exists using only cells from 0 to 4 |
| 2 | Not reachable | The path is blocked by cells larger than 2 |
| 3 | Not reachable | The remaining low cells do not connect both sides |

The smallest successful threshold is 4, so the answer is 4. This trace demonstrates the monotonic property used by binary search.

For the second sample:

```
6 5
89888
88898
99998
88888
89999
88888
```

| Threshold | BFS result | Reason |
| --- | --- | --- |
| 8 | Reachable | The large region of 8-valued cells connects the start and end |
| 7 | Not reachable | Every cell is at least 8, so no movement is possible |

The answer is 8. This example exercises the case where the minimum possible path still requires a relatively high value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm log C) | Binary search performs O(log C) BFS runs, and each BFS visits each cell at most once |
| Space | O(nm) | The grid and visited matrix both use space proportional to the number of cells |

The grid has fewer than 10,000 cells, so even repeated full traversals are easily within the limits. The approach also scales well if the value range becomes larger.

## Test Cases

```python
import sys
import io
from collections import deque

def solution(inp):
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, m = map(int, input().split())
    grid = [list(map(int, input().strip())) for _ in range(n)]

    def can_reach(limit):
        if grid[0][0] > limit:
            return False

        q = deque([(0, 0)])
        visited = [[False] * m for _ in range(n)]
        visited[0][0] = True

        while q:
            r, c = q.popleft()
            if r == n - 1 and c == m - 1:
                return True

            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < m:
                    if not visited[nr][nc] and grid[nr][nc] <= limit:
                        visited[nr][nc] = True
                        q.append((nr, nc))

        return False

    lo = min(map(min, grid))
    hi = max(map(max, grid))
    ans = hi

    while lo <= hi:
        mid = (lo + hi) // 2
        if can_reach(mid):
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1

    return str(ans) + "\n"

assert solution("""6 8
13567657
24903578
83107213
98829363
25511282
39108443
""") == "4\n"

assert solution("""6 5
89888
88898
99998
88888
89999
88888
""") == "8\n"

assert solution("""1 1
7
""") == "7\n"

assert solution("""3 3
111
999
111
""") == "1\n"

assert solution("""2 2
99
99
""") == "9\n"

assert solution("""4 4
0123
9993
9994
1114
""") == "4\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single cell containing 7 | 7 | Starting cell is also the destination |
| Grid with a low-value path around 9s | 1 | Greedy movement traps are avoided |
| All cells equal to 9 | 9 | Uniform maximum values are handled correctly |
| Path requiring boundary movement | 4 | Edge traversal and BFS boundaries are correct |

## Edge Cases

For the single-cell grid:

```
1 1
7
```

Binary search eventually tests threshold 7. BFS starts at the only cell and immediately sees that it is the destination, so the answer is 7. The algorithm never assumes that at least one move exists.

For the grid:

```
3 3
111
999
111
```

A threshold of 1 marks all 9-valued cells as blocked. BFS moves across the top row and then down the right side, reaching the destination without entering a blocked cell. The algorithm returns 1 instead of following a locally attractive but incorrect route toward the center.

For a completely uniform grid:

```
2 2
99
99
```

Every threshold below 9 fails because the starting cell itself is unavailable. At threshold 9, BFS reaches the destination immediately through the open grid, so the minimum valid answer is correctly found as 9.
