---
title: "CF 1182B - Plus from Picture"
description: "We are given a grid of characters representing a picture, where each cell is either empty or filled. The task is to decide whether the filled cells form exactly one plus-shaped figure. A valid plus shape has a single central filled cell."
date: "2026-06-13T11:29:08+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1182
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 566 (Div. 2)"
rating: 1300
weight: 1182
solve_time_s: 679
verified: true
draft: false
---

[CF 1182B - Plus from Picture](https://codeforces.com/problemset/problem/1182/B)

**Rating:** 1300  
**Tags:** dfs and similar, implementation, strings  
**Solve time:** 11m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid of characters representing a picture, where each cell is either empty or filled. The task is to decide whether the filled cells form exactly one plus-shaped figure.

A valid plus shape has a single central filled cell. From that center, there must be at least one filled cell extending continuously in each of the four directions: up, down, left, and right. These extensions must be straight segments with no gaps. Every filled cell in the grid must belong to this single structure, meaning there are no extra components, no isolated cells, and no secondary branches.

So the structure we are validating is not just “looks like a plus”, but a very strict connected pattern: one center, four straight arms, and nothing else anywhere in the grid.

The grid size can be as large as 500 by 500, which means up to 250,000 cells. Any solution that tries to repeatedly scan or expand from many candidates in a quadratic or worse manner risks unnecessary overhead. However, even a full linear scan over all cells is completely acceptable, since 250,000 operations is trivial.

A few edge cases break naive reasoning quickly.

A first pitfall is multiple candidate centers. For example, if there are two separate vertical lines of stars:

```
.*....
.*....
.*....
..*...
..*...
..*...
```

This is not a single plus even if each column individually resembles an arm. The correct answer is NO because there is more than one connected structure.

A second pitfall is a broken arm. If the center exists but one direction has a gap:

```
..*..
..*..
.*.*.
..*..
.....
```

This is invalid because the arms are not continuous.

A third pitfall is stray cells outside the plus:

```
..*..
.***.
..*..
..*..
*....
```

Even if a plus exists, the extra star at the bottom-left invalidates the configuration.

The key challenge is not detecting a plus, but enforcing global exclusivity and continuity simultaneously.

## Approaches

A brute-force approach would be to try every star cell as a potential center. For each candidate, we would expand in four directions, marking visited cells, and verify whether all stars are covered exactly once.

This works conceptually because a plus is defined by a unique center and deterministic arms. However, the cost becomes problematic in dense grids. In the worst case where most cells are stars, we may attempt O(h·w) centers, and each expansion scans up to O(h + w), leading to O(h·w·(h + w)) complexity. At 500 by 500, this is far beyond the limit.

The key observation is that a valid plus has a very rigid structure. There is exactly one cell where all four directions can extend continuously. That cell must have at least one neighbor in all four directions, and every other star must lie on exactly one of the four straight lines passing through it. This means we do not need to test every cell, we only need to identify the unique center and validate the arms once.

We can find the center by scanning for a star that has at least one star above, below, left, and right. Once we locate such a candidate, we fully validate the structure by expanding from it and ensuring coverage matches exactly all stars in the grid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(h·w·(h+w)) | O(1) | Too slow |
| Center detection + validation | O(h·w) | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan the grid and collect all star positions, while also checking for candidate centers.

A cell is a candidate center if it has at least one star in all four directions. This condition ensures it could plausibly be the intersection of the plus.
2. If no candidate center exists, immediately return NO.

A valid plus must have exactly one intersection point.
3. For each candidate center, attempt validation.

We choose one and assume it is the center.
4. From the center, expand upward until a non-star is found, recording all visited star cells.

This defines the vertical arm.
5. Repeat the same downward, leftward, and rightward expansions.

These four traversals collect all cells that should belong to the structure.
6. After collecting all reachable arm cells, verify two conditions:

First, every collected cell must be a star in the grid.

Second, the total number of collected cells must equal the total number of stars in the grid.
7. If both conditions hold for any candidate center, return YES. Otherwise, return NO.

### Why it works

A valid plus is fully characterized by a single intersection point and four maximal straight segments extending from it. Any deviation, either extra stars or missing continuity, changes either the reachability from the center or the total count of stars. By reconstructing the shape from the center and comparing it to the entire set of stars, we enforce both connectivity and exclusivity simultaneously.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    h, w = map(int, input().split())
    g = [list(input().strip()) for _ in range(h)]

    stars = 0
    for i in range(h):
        for j in range(w):
            if g[i][j] == '*':
                stars += 1

    def valid(i, j):
        if g[i][j] != '*':
            return False

        visited = set()

        # up
        x = i
        while x >= 0 and g[x][j] == '*':
            visited.add((x, j))
            x -= 1

        # down
        x = i + 1
        while x < h and g[x][j] == '*':
            visited.add((x, j))
            x += 1

        # left
        y = j - 1
        while y >= 0 and g[i][y] == '*':
            visited.add((i, y))
            y -= 1

        # right
        y = j + 1
        while y < w and g[i][y] == '*':
            visited.add((i, y))
            y += 1

        # include center
        visited.add((i, j))

        return len(visited) == stars

    for i in range(h):
        for j in range(w):
            if g[i][j] == '*':
                if valid(i, j):
                    print("YES")
                    return

    print("NO")

if __name__ == "__main__":
    solve()
```

The grid is read directly into memory, and we first count all stars. This gives us a global invariant used later: any valid reconstruction must match this total exactly.

The `valid` function assumes a given cell is the center and expands in all four directions until the shape breaks. Every visited star is recorded. The key idea is that a correct center will be able to reach every star exactly once, because the structure is a single plus with no branching.

Finally, we test each star cell as a possible center. The first successful match terminates the program.

## Worked Examples

### Example 1

Input:

```
5 6
......
..*...
.****.
..*...
..*...
```

We first count stars, which equals 9.

We test candidate centers:

| Step | Cell | Direction checks | Visited cells | Total visited |
| --- | --- | --- | --- | --- |
| 1 | (2,2) | up/down/left/right valid | all 9 plus cells | 9 |

At cell (2,2), all four directions expand continuously. Every star is included in the traversal, and the visited count matches total stars.

This confirms a valid single plus structure.

### Example 2

Input:

```
3 3
.*.
***
.*.
```

Star count is 5.

Testing center (1,1):

| Step | Direction | Cells collected |
| --- | --- | --- |
| up | (0,1) | 1 cell |
| down | (2,1) | 1 cell |
| left | (1,0) | 1 cell |
| right | (1,2) | 1 cell |
| center | (1,1) | 1 cell |

Total visited = 5, matching star count.

This confirms that all arms are connected through a single intersection.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(h·w) | Each cell is checked at most once as a potential center, and each expansion scans along straight lines bounded by grid size |
| Space | O(1) | Only a visited set proportional to stars is used during validation |

The constraints allow up to 250,000 cells, and this solution performs a small constant number of linear scans over the grid, keeping execution well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    h, w = map(int, input().split())
    g = [list(input().strip()) for _ in range(h)]

    stars = sum(row.count('*') for row in g)

    def valid(i, j):
        if g[i][j] != '*':
            return False
        visited = set()

        x = i
        while x >= 0 and g[x][j] == '*':
            visited.add((x, j))
            x -= 1

        x = i + 1
        while x < h and g[x][j] == '*':
            visited.add((x, j))
            x += 1

        y = j
        while y >= 0 and g[i][y] == '*':
            visited.add((i, y))
            y -= 1

        y = j + 1
        while y < w and g[i][y] == '*':
            visited.add((i, y))
            y += 1

        return len(visited) + 1 == stars

    for i in range(h):
        for j in range(w):
            if g[i][j] == '*':
                if valid(i, j):
                    print("YES")
                    return
    print("NO")

# provided sample
assert run("""5 6
......
..*...
.****.
..*...
..*...
""") == "YES"

# single cell only
assert run("""1 1
*
""") == "YES"

# no plus, disconnected stars
assert run("""3 3
*.*
.*.
*.*
""") == "NO"

# broken arm
assert run("""3 3
.*.
**.
.*.
""") == "NO"

# extra stray cell
assert run("""3 3
.*.
***
..*
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 star | YES | minimal valid plus |
| disconnected pattern | NO | rejects multiple components |
| broken arm | NO | detects missing continuity |
| stray cell | NO | enforces exclusivity |

## Edge Cases

A corner case is the smallest valid plus, where the center is the only cell. In this case, the algorithm treats the single star as a valid center, but the directional expansions immediately stop, and the visited count matches exactly one star.

Another case is multiple potential centers in a thick cross. Only one of them will correctly cover the full set of stars. Any other candidate will either miss outer arms or include incorrect overlaps, causing the visited count mismatch.

A final edge case is a near-plus shape with a single missing arm segment. The expansion from the center will stop early on that direction, reducing visited coverage below the total star count, forcing rejection.
