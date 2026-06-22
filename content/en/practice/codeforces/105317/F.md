---
title: "CF 105317F - Maze Runner"
description: "We are given a very small grid, at most 10 by 10, where every cell contains a lowercase letter. From any cell we are allowed to move to any of its 8 neighbors, including diagonals, and we are allowed to revisit cells arbitrarily many times."
date: "2026-06-23T06:07:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105317
codeforces_index: "F"
codeforces_contest_name: "JPC 1.0"
rating: 0
weight: 105317
solve_time_s: 57
verified: true
draft: false
---

[CF 105317F - Maze Runner](https://codeforces.com/problemset/problem/105317/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a very small grid, at most 10 by 10, where every cell contains a lowercase letter. From any cell we are allowed to move to any of its 8 neighbors, including diagonals, and we are allowed to revisit cells arbitrarily many times. The only restriction on movement is that a step must actually change the cell, so staying in place is not allowed.

Each query gives a short string, and we need to decide whether there exists a walk on the grid such that the sequence of visited cell letters spells exactly that string.

A key detail is that the same cell may be reused any number of times, so the structure is not a simple path problem with visited constraints. Instead, this is about whether the grid contains a labeled walk matching a sequence.

The constraints strongly shape the solution. The grid has at most 100 cells, while each query string has length at most 13. There are up to 100000 queries. This combination means we can afford a fairly heavy per query dynamic program over the grid, as long as each query stays close to roughly a few thousand operations. Anything involving exponential search over paths without memoization would fail immediately, since branching over 8 directions for 13 steps produces up to 8^13 possibilities in the worst case.

One subtle point is that reuse of cells removes the usual “simple path” structure. A naive depth first search that does not memoize states can revisit the same configuration many times, especially on uniform grids where all letters match.

A second subtle point is that each query is independent. We cannot carry state across queries because strings differ and validity depends on exact character sequence alignment.

## Approaches

A direct interpretation suggests starting from every cell that matches the first character of the pattern, then performing a depth first search trying all 8 moves at each step while matching the next character. This is correct because it explicitly enumerates all possible walks.

However, this approach repeats the same subproblems many times. From a fixed cell and a fixed index in the string, the remaining question is always the same: can we continue matching the suffix of the string from here? Without memoization, the recursion explores exponentially many redundant paths, especially because revisiting cells is allowed and cycles create infinite recomputation.

The structure of the problem allows a cleaner reformulation. For each query string, define a state as a pair consisting of a grid position and an index in the string. From a state, transitions go to any adjacent cell whose letter matches the next character. Since the string length is at most 13 and the grid has at most 100 positions, the total number of states per query is at most 1300. Each state has at most 8 transitions, so a full exploration with memoization is linear in this state space.

The key observation is that cycles in the grid do not matter once we memoize states. Even if a walk revisits a cell, we do not need to recompute whether a suffix is possible from that state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force DFS without memoization | O(8^L) per query | O(L) recursion | Too slow |
| DP over (cell, index) states per query | O(nm · L · 8) per query | O(nm · L) per query | Accepted |

## Algorithm Walkthrough

We process each query independently using a dynamic programming or memoized DFS formulation over the grid.

1. We consider every cell as a potential starting point for the pattern. A start cell is valid only if its letter matches the first character of the string. This restriction removes unnecessary work immediately, since mismatched starts can never lead to a valid match.
2. We define a function over states `(r, c, i)` meaning we are currently at cell `(r, c)` and we have already matched the prefix `s[0..i]`, so the next character to match is `s[i+1]`. The goal is to determine whether we can reach index `len(s) - 1`.
3. From a state `(r, c, i)`, if `i` is already the last index of the string, we have successfully matched the whole pattern and return success.
4. Otherwise, we attempt to move to all 8 neighboring cells `(nr, nc)`. A transition is only valid if the character in `(nr, nc)` equals `s[i+1]`. For each valid neighbor, we recursively evaluate the state `(nr, nc, i+1)`.
5. To avoid recomputing the same state multiple times, we store results in a memo table indexed by `(r, c, i)`. Once a state is computed, it is reused whenever encountered again.
6. The answer for the query is “YES” if any starting position leads to a successful completion of the string, otherwise “NO”.

The crucial implementation detail is that memoization is per query, not global. Each string defines a different state space, so reuse across queries would mix unrelated computations.

### Why it works

The correctness comes from the fact that every valid walk in the grid corresponds exactly to a sequence of transitions in the state graph defined by `(cell, index)`. Every possible move in the grid is represented in the transition step, and every valid sequence of characters must correspond to some path in this state graph.

Memoization does not remove any valid paths because it only eliminates recomputation of identical states, not transitions. Since each state fully captures all information needed to continue, recomputing it cannot change the result.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

dx = [-1,-1,-1,0,0,1,1,1]
dy = [-1,0,1,-1,1,-1,0,1]

def solve_one(grid, s, n, m):
    L = len(s)
    memo = [[[-1] * L for _ in range(m)] for _ in range(n)]

    def dfs(x, y, i):
        if memo[x][y][i] != -1:
            return memo[x][y][i]

        if i == L - 1:
            memo[x][y][i] = 1
            return 1

        nx_char = s[i + 1]
        for k in range(8):
            nx = x + dx[k]
            ny = y + dy[k]
            if 0 <= nx < n and 0 <= ny < m:
                if grid[nx][ny] == nx_char:
                    if dfs(nx, ny, i + 1):
                        memo[x][y][i] = 1
                        return 1

        memo[x][y][i] = 0
        return 0

    for i in range(n):
        for j in range(m):
            if grid[i][j] == s[0]:
                if dfs(i, j, 0):
                    return True
    return False

def main():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    q = int(input())

    for _ in range(q):
        s = input().strip()
        print("YES" if solve_one(grid, s, n, m) else "NO")

if __name__ == "__main__":
    main()
```

The grid traversal is implemented through an 8-direction offset array, which makes neighbor generation constant time per step. The memo table is three dimensional, keyed by row, column, and position in the string. Each query rebuilds this table because previous results are irrelevant.

The DFS immediately filters transitions by character equality, which is the main pruning factor that keeps the solution fast in practice. Without this check, every neighbor would be explored regardless of feasibility, multiplying work by up to eight at every step.

## Worked Examples

Consider the grid:

```
ab
ju
```

and the query string `auabj`.

We trace how the DP explores possible states starting from cells matching `'a'`.

| Step | Position | Index | Next char | Action |
| --- | --- | --- | --- | --- |
| 1 | (0,0) | 0 | u | try neighbors |
| 2 | (0,1) | 1 | a | move right |
| 3 | (1,1) | 2 | b | move diagonally/valid neighbor |
| 4 | (0,0) | 3 | j | revisit allowed |

This trace shows that revisiting cells is naturally handled without special marking, since state identity includes the index in the string.

Now consider a failing pattern where a character cannot be matched at any step. Suppose the next required character does not exist in any neighbor of any reachable state at a given depth. The memoization ensures that once all paths from a state fail, that state is never reconsidered again, preventing repeated dead-end exploration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q · n · m · L · 8) | Each query explores at most all `(cell, index)` states once, each with up to 8 transitions |
| Space | O(n · m · L) | Memo table per query stores results for all state triples |

With `n, m ≤ 10` and `L ≤ 13`, each query costs on the order of a few thousand operations, which fits comfortably even for `q = 100000` in optimized implementations, especially in compiled languages.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = []

    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    q = int(input())

    dx = [-1,-1,-1,0,0,1,1,1]
    dy = [-1,0,1,-1,1,-1,0,1]

    sys.setrecursionlimit(10**7)

    def solve_one(grid, s):
        n, m = len(grid), len(grid[0])
        L = len(s)
        memo = [[[-1]*L for _ in range(m)] for _ in range(n)]

        def dfs(x,y,i):
            if memo[x][y][i] != -1:
                return memo[x][y][i]
            if i == L-1:
                memo[x][y][i] = 1
                return 1
            need = s[i+1]
            for k in range(8):
                nx, ny = x+dx[k], y+dy[k]
                if 0 <= nx < n and 0 <= ny < m:
                    if grid[nx][ny] == need:
                        if dfs(nx,ny,i+1):
                            memo[x][y][i] = 1
                            return 1
            memo[x][y][i] = 0
            return 0

        for i in range(n):
            for j in range(m):
                if grid[i][j] == s[0]:
                    if dfs(i,j,0):
                        return True
        return False

    for _ in range(q):
        s = input().strip()
        out.append("YES" if solve_one(grid, s) else "NO")

    return "\n".join(out)

# sample-style sanity checks (placeholders since exact sample formatting omitted)
assert run("""2 2
ab
ju
4
auabj
auau
jbjbjbjb
ajbuabu
""") == "YES\nYES\nYES\nYES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 grid single letter | YES/NO | minimal start/finish behavior |
| repeating same letter grid | YES for short repeats | revisiting cells correctness |
| impossible letter in middle | NO | pruning correctness |
| long repeated pattern | YES/NO depending | depth handling up to 13 |

## Edge Cases

A grid filled with the same character stresses the reuse and cycle behavior. For a pattern like `"aaaaaaaaaaaaa"`, every cell is a valid start and every move remains valid. The algorithm still terminates correctly because the memo table ensures that each `(cell, index)` pair is evaluated only once, even though the number of conceptual walks is enormous.

A single-cell grid demonstrates boundary handling. If the pattern length is greater than 1, no transitions are possible because movement always changes the cell, so the only valid answer is for length 1 strings matching the single character.

A pattern whose first character does not exist in the grid is filtered immediately before DFS begins. This prevents unnecessary state creation and ensures the algorithm does not enter the recursion at all in that case.
