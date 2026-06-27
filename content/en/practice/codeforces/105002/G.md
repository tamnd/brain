---
title: "CF 105002G - \u0411\u0430\u043b\u0434\u0430"
description: "We are given a grid of size n by m, where each cell contains either a letter or a dot indicating an empty cell. On this grid, we want to determine whether a given word s already appears as a valid “snake” path."
date: "2026-06-28T03:20:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105002
codeforces_index: "G"
codeforces_contest_name: "vkoshp.letovo 2022"
rating: 0
weight: 105002
solve_time_s: 63
verified: true
draft: false
---

[CF 105002G - \u0411\u0430\u043b\u0434\u0430](https://codeforces.com/problemset/problem/105002/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid of size n by m, where each cell contains either a letter or a dot indicating an empty cell. On this grid, we want to determine whether a given word s already appears as a valid “snake” path.

A valid appearance means we can choose a starting cell and then move step by step in the four cardinal directions so that each step goes to an adjacent cell, we never reuse a cell, and the sequence of visited cells spells out s exactly in order. Only cells that already contain letters are usable, and the letter in each visited cell must match the corresponding character of s.

The word s has the additional property that all its characters are distinct. This restriction is crucial because it limits the length of any successful path to at most 26, and it prevents revisiting the same letter position in the word, though it does not directly prevent revisiting grid cells unless we enforce the path rule.

The grid itself can be large in total size up to 10^6 cells, so any solution that tries to search all paths in a naive DFS manner over the grid structure risks exploring an exponential number of paths and will not finish in time.

A subtle point that often breaks naive solutions is the interaction between branching and path validity. Even though the word is short, a single character may appear in many positions in the grid, and naive backtracking from each occurrence can repeatedly explore overlapping regions. Another common failure mode is forgetting the “no reuse of cells” constraint, which can accidentally allow invalid cycles if not tracked properly.

For example, if the grid is a large open area filled with the same letter distribution that matches transitions of s, a naive DFS may revisit the same region through different paths and explode combinatorially even though the word length is small.

The task is therefore not to search arbitrarily in the grid, but to efficiently check whether there exists a valid chain of positions, one per character of s, such that consecutive positions are adjacent in the grid.

## Approaches

The most direct idea is to start from every occurrence of the first character and perform a DFS or BFS that tries to build the word step by step. From each current cell, we explore its four neighbors and continue if the next character matches.

This is correct logically, because it enumerates all possible paths that spell the word. However, its complexity depends on the number of branching choices at each step. In a dense grid, each step may branch up to four directions, and multiple starting positions can multiply the search space. Even though the word length is at most 26, the search tree can still expand to a very large number of partial paths, especially when many grid cells match intermediate characters.

The key observation that simplifies the problem is that the word length is very small, while the grid is large. Instead of thinking in terms of arbitrary path exploration, we can think in terms of layer-by-layer propagation. Each character position in the word forms a layer, and we only need to know which grid cells can represent that position in some valid partial path.

We start with all cells that match the first character. Then, for each next character, we compute all grid cells that are adjacent to at least one reachable cell from the previous layer and contain the required character. Since each cell transition is local and checked only once per layer, this process remains linear in the number of grid cells per layer.

This transforms the problem into a controlled dynamic propagation across at most 26 layers, avoiding exponential branching entirely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| DFS from every start | Exponential in worst case | O(k) recursion | Too slow |
| Layered propagation DP | O(nm · | s | ) |

## Algorithm Walkthrough

1. Read the grid and locate all cells that match the first character of the word. These form the initial set of reachable positions, since any valid path must start from one of them.
2. Maintain a boolean grid or visitation marker that tracks which cells are reachable at the current character index. This prevents duplicate processing of the same cell within one layer.
3. For each next character in the word, build a new set of reachable positions by scanning all currently reachable cells and checking their four neighbors. If a neighbor contains the required next character, it becomes reachable in the next layer.
4. Replace the current reachable set with the newly constructed set and proceed to the next character.
5. If at any stage the reachable set becomes empty, the word cannot be formed as a valid path and we stop early.
6. After processing all characters, if at least one cell is reachable at the final character, the word exists on the board.

### Why it works

The algorithm maintains the invariant that after processing the i-th character of the word, the set of active cells exactly corresponds to all endpoints of valid paths that spell the prefix s[0..i]. Each transition step only extends valid paths by one adjacency move that matches the next character. Since every valid path must be built incrementally through adjacent steps, and we never discard any valid extension, no solution is lost. At the same time, every recorded state corresponds to a real path segment, so no invalid path is ever introduced.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    s = input().strip()
    k = len(s)

    # current reachable cells
    cur = set()

    # initialize with positions of first character
    for i in range(n):
        row = grid[i]
        for j in range(m):
            if row[j] == s[0]:
                cur.add((i, j))

    if not cur:
        print("NO")
        return

    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for idx in range(1, k):
        nxt_char = s[idx]
        nxt = set()

        for x, y in cur:
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < m:
                    if grid[nx][ny] == nxt_char:
                        nxt.add((nx, ny))

        cur = nxt
        if not cur:
            print("NO")
            return

    print("YES")

if __name__ == "__main__":
    solve()
```

The implementation directly follows the layered propagation idea. The initial scan collects all valid starting points. Each iteration advances one character forward by expanding only through valid grid adjacencies. The use of a set ensures that each cell is processed at most once per layer, preventing redundant propagation when multiple paths reach the same position.

The key implementation detail is that we never attempt to track full paths. We only track reachable endpoints per prefix length, which is sufficient because the word itself uniquely determines the sequence of required characters.

## Worked Examples

### Example 1

Input grid:

```
ALGAE
RPA.T
C.R.H
T.TYO
I...S
C....
PARTY
```

Word: PARTY

We start by collecting all cells containing P. Suppose only one such cell exists at (1,1).

| Step | Character | Reachable cells |
| --- | --- | --- |
| 0 | P | {(1,1)} |
| 1 | A | {(1,2)} |
| 2 | R | {(1,3)} |
| 3 | T | {(0,3)} |
| 4 | Y | {(3,3)} |

At the final step we still have reachable positions, so the answer is YES.

This trace shows that propagation correctly follows a single continuous chain without needing to explicitly reconstruct the path.

### Example 2

Input grid:

```
.P.YT.
.YTPHO
.T.YOP
NONNHY
PYTOHN
..P.YO
```

Word: PYTHON

| Step | Character | Reachable cells |
| --- | --- | --- |
| 0 | P | multiple positions |
| 1 | Y | reduced set |
| 2 | T | further reduced |
| 3 | H | possibly empty |
| 4 | O | empty |

At some intermediate step, no valid extension exists, so the process terminates early with NO. This demonstrates how pruning prevents unnecessary exploration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm · | s |
| Space | O(nm) | Set of reachable states can in worst case cover the grid |

The grid size dominates, but the word length is bounded by 26, so the total operations remain comfortably within limits for 10^6 cells.

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

# sample 1
assert run("""6 5
ALGAE
RPA.T
C.R.H
T.TYO
I...S
C....
PARTY
""") == "YES"

# sample 2
assert run("""6 6
.P.YT.
.YTPHO
.T.YOP
NONNHY
PYTOHN
..P.YO
PYTHON
""") == "NO"

# single cell
assert run("""1 1
A
A
""") == "YES"

# impossible start
assert run("""2 2
AB
CD
EF
""") == "NO"

# linear path
assert run("""1 6
ABCDEF
ABCDEF
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single cell match | YES | minimal boundary |
| no starting letter | NO | early rejection |
| straight line match | YES | simplest chain |
| sample grids | YES/NO | correctness on full cases |

## Edge Cases

A critical edge case occurs when the first character appears many times across the grid but none of those occurrences can actually connect to the second character. The algorithm handles this naturally because the initial set may be large, but the first propagation step immediately filters it down based on adjacency, collapsing the frontier in one iteration.

Another case is when characters appear in clusters forming loops. Even if many paths cycle locally, the set-based propagation prevents repeated expansion within the same layer, so loops do not inflate the state space.

Finally, when the word is of length 1, the algorithm correctly returns YES if and only if that character exists anywhere in the grid, since the initial set itself is already the final answer.
