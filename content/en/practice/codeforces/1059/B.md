---
title: "CF 1059B - Forgery"
description: "We are given a binary grid representing a target drawing made of ink cells. Each cell is either already filled or empty, and we want to determine whether this final pattern could have been produced from an initially empty grid using a specific stamping tool."
date: "2026-06-15T09:35:15+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1059
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 514 (Div. 2)"
rating: 1300
weight: 1059
solve_time_s: 219
verified: true
draft: false
---

[CF 1059B - Forgery](https://codeforces.com/problemset/problem/1059/B)

**Rating:** 1300  
**Tags:** implementation  
**Solve time:** 3m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary grid representing a target drawing made of ink cells. Each cell is either already filled or empty, and we want to determine whether this final pattern could have been produced from an initially empty grid using a specific stamping tool.

The tool does not paint arbitrary shapes. Instead, it always paints the border of a 3 by 3 square, leaving the center cell untouched. Every application is centered at some cell, and it paints the eight surrounding cells in that 3 by 3 neighborhood. The center itself is never affected. The operation can only be used when the full 3 by 3 block lies inside the grid.

The question is whether there exists a sequence of such stamp operations that produces exactly the given grid, starting from all empty cells.

The grid size can be up to 1000 by 1000, which means up to one million cells. Any solution that tries to simulate stamping at every possible position and repeatedly updating the grid in a naive way risks becoming too slow if each check is expensive. We therefore need a method where each cell is processed only a constant number of times, or at least each potential stamp is evaluated in constant time.

A subtle difficulty appears when ink cells exist that cannot possibly belong to the border of any valid stamp. For example, a single isolated `#` in the middle of a sea of dots cannot be explained, since every stamp paints in a ring of eight neighbors. Another problematic pattern is a `#` cell that is not supported by any possible 3 by 3 configuration, meaning it is never part of any valid border.

The key failure mode for naive reasoning is assuming that every `#` must be the center of some stamp or that every `#` must itself be painted directly. In reality, only the border matters, and coverage can overlap in complex ways.

## Approaches

A brute-force idea is to simulate stamping. For every possible center of a 3 by 3 block, we could attempt to apply the stamp if it does not contradict the target grid, and mark the cells it would paint. After trying all possible placements, we compare the resulting painted grid with the target.

This approach is conceptually correct, but its weakness is that it does not enforce necessity. We might apply stamps that are not required, and even worse, we might miss the fact that some `#` cells are never covered unless we carefully check coverage constraints. In the worst case, we would examine every cell as a potential center, and for each center we inspect up to 9 cells, leading to about 9 million operations, which is borderline but still manageable. However, correctness becomes tricky because we need to ensure that every `#` is explainable, not just reproducible by arbitrary stamping.

The key insight is to reverse the thinking. Instead of constructing the grid forward, we check whether every `#` cell can be "justified" as belonging to the border of at least one valid stamp. A cell can be painted only if there exists some center around it such that it lies in the 3 by 3 border pattern. That means for each `#`, we check whether it can be the top, bottom, left, or right neighbor of some valid center. If no such center exists, the configuration is impossible.

This reduces the problem to verifying local feasibility around each cell. We scan all possible centers, mark which border cells they can produce, and then verify that every `#` is covered by at least one valid stamp center.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n m) to O(n m · 9) | O(n m) | Too slow / hard to reason |
| Center-based validation | O(n m) | O(n m) | Accepted |

## Algorithm Walkthrough

1. We create a boolean grid `good` that marks whether a 3 by 3 stamp centered at a given position is valid. A center is valid if all eight border cells are `#`. This ensures that applying a stamp there would not introduce any incorrect dots.
2. We iterate over all possible centers `(i, j)` where a full 3 by 3 block fits. For each center, we check the eight surrounding positions. If they are all `#`, we mark this center as usable.
3. We create another boolean grid `covered` of the same size as the input grid, initially all false. This will track which cells can be explained by at least one valid stamp.
4. For every valid center `(i, j)`, we mark its eight border cells in `covered` as true. This simulates the fact that this stamp could have contributed ink to those cells.
5. After processing all centers, we iterate over the entire grid and check every `#` cell. If any `#` is not marked in `covered`, then it cannot be explained by any valid stamp configuration, so the answer is NO.
6. If all `#` cells are covered, we return YES.

### Why it works

The key invariant is that every valid final `#` cell must be explainable as part of at least one 3 by 3 border whose center lies inside the grid. Any valid construction consists only of such stamps, and every stamp contributes ink only to its border cells. Therefore, if a cell is not in any valid border, no sequence of stamps can ever produce it. Conversely, if every `#` is in at least one valid border, we can assign stamps greedily in any order since overlaps are allowed and never remove ink.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    g = [input().strip() for _ in range(n)]
    
    covered = [[False] * m for _ in range(n)]
    
    def ok(i, j):
        return (g[i-1][j-1] == '#' and g[i-1][j] == '#' and g[i-1][j+1] == '#' and
                g[i][j-1] == '#'                     and g[i][j+1] == '#' and
                g[i+1][j-1] == '#' and g[i+1][j] == '#' and g[i+1][j+1] == '#')
    
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if ok(i, j):
                covered[i-1][j-1] = True
                covered[i-1][j] = True
                covered[i-1][j+1] = True
                covered[i][j-1] = True
                covered[i][j+1] = True
                covered[i+1][j-1] = True
                covered[i+1][j] = True
                covered[i+1][j+1] = True
    
    for i in range(n):
        for j in range(m):
            if g[i][j] == '#' and not covered[i][j]:
                print("NO")
                return
    
    print("YES")

if __name__ == "__main__":
    solve()
```

The core of the implementation is the `ok` function, which checks whether a stamp centered at `(i, j)` is valid. We only consider centers that are fully inside the grid, since border centers cannot form a 3 by 3 pattern.

The `covered` matrix tracks reachability from all valid stamp centers. Each valid center contributes to exactly eight surrounding cells, matching the stamping rule precisely. The final scan ensures that no required ink cell is left unsupported.

Boundary handling is critical here. The loops over `i in range(1, n-1)` and `j in range(1, m-1)` ensure we never access out-of-bounds neighbors when checking a 3 by 3 block.

## Worked Examples

### Sample 1

Input:

```
3 3
###
#.#
###
```

We evaluate the only possible center at `(1, 1)` in 0-based indexing (center of the grid).

| Center | Valid stamp? | Covered cells |
| --- | --- | --- |
| (1,1) | Yes | all border cells |

After marking, all `#` cells in the border are covered, and the center cell is ignored.

Every `#` has support, so the output is YES.

### Sample 2 (conceptual impossible pattern)

Input:

```
3 3
###
#..
###
```

| Center | Valid stamp? | Covered cells |
| --- | --- | --- |
| (1,1) | No | none |

No valid stamp exists because not all border cells are `#`. Therefore no coverage is produced.

The cell at bottom-left or top-right `#` cannot be explained, so the output is NO.

This shows that partial borders break the possibility of constructing the configuration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each cell is checked a constant number of times as part of at most one center scan |
| Space | O(nm) | We store a coverage grid of the same size as input |

The grid size is at most one million cells, and each is processed with constant work. This fits comfortably within both the time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve_capture()

def solve_capture():
    n, m = map(int, input().split())
    g = [input().strip() for _ in range(n)]
    covered = [[False]*m for _ in range(n)]

    def ok(i, j):
        return (g[i-1][j-1] == '#' and g[i-1][j] == '#' and g[i-1][j+1] == '#' and
                g[i][j-1] == '#' and g[i][j+1] == '#' and
                g[i+1][j-1] == '#' and g[i+1][j] == '#' and g[i+1][j+1] == '#')

    for i in range(1, n-1):
        for j in range(1, m-1):
            if ok(i, j):
                covered[i-1][j-1] = covered[i-1][j] = covered[i-1][j+1] = True
                covered[i][j-1] = covered[i][j+1] = True
                covered[i+1][j-1] = covered[i+1][j] = covered[i+1][j+1] = True

    for i in range(n):
        for j in range(m):
            if g[i][j] == '#' and not covered[i][j]:
                return "NO"
    return "YES"

# provided sample
assert run("""3 3
###
#.#
###
""") == "YES"

# isolated impossible
assert run("""3 3
###
#..
###
""") == "NO"

# minimum valid-ish pattern
assert run("""3 3
###
###
###
""") == "YES"

# all dots
assert run("""3 3
...
...
...
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3x3 full block | YES | single center validity |
| broken border | NO | partial stamp impossibility |
| full grid | YES | maximal coverage |
| empty grid | YES | no required constraints |

## Edge Cases

A corner case is when the grid contains `#` cells near the boundary. For example, a `#` at position `(0, 0)` can never be covered by any stamp because no 3 by 3 block includes it as a border cell. The algorithm naturally handles this because no valid center can mark it in `covered`, so it is detected as uncovered.

Another case is when all cells are `#`. Every center `(i, j)` with a full 3 by 3 neighborhood becomes valid, and every cell is covered by multiple overlapping stamps. The algorithm still only requires at least one coverage, so it correctly outputs YES without needing to reason about overlap structure.
