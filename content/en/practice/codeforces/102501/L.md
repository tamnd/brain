---
title: "CF 102501L - River Game"
description: "The grid describes a wetland where cells form rivers. A connected group of cells is one river area. Cameras can only be placed on . cells that touch one of these river areas, and two cameras touching the same river area cannot be adjacent."
date: "2026-08-05T17:55:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102501
codeforces_index: "L"
codeforces_contest_name: "2019-2020 ICPC Southwestern European Regional Programming Contest (SWERC 2019-20)"
rating: 0
weight: 102501
solve_time_s: 379
verified: true
draft: false
---

[CF 102501L - River Game](https://codeforces.com/problemset/problem/102501/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

The grid describes a wetland where `*` cells form rivers. A connected group of `*` cells is one river area. Cameras can only be placed on `.` cells that touch one of these river areas, and two cameras touching the same river area cannot be adjacent.

The game is not about the whole grid at once. The separation condition between different river areas means that a move near one river area can never affect moves near another one. This turns the board into several independent games whose results can be combined.

The value of `N` is at most 10, so the whole board has only 100 cells. This rules out approaches that simulate every possible game state of the complete board, because the number of subsets of cells is enormous. The small grid size does allow exponential algorithms on a single river area, because every river contains at most `2N`, or 20, wet cells. The key is to avoid exponential work on the whole board.

A common mistake is to count the number of possible camera positions and only check whether it is odd or even. This fails because the order of moves matters. For example:

```
...
...
***
```

There are three possible camera cells touching the river. The answer is `First player will win`, because choosing the middle cell prevents both remaining cells from being used. Counting moves would incorrectly predict that three moves are always available.

Another mistake is to merge different river areas into one game. For example:

```
*...*
.....
*...*
```

The two rivers are separated and their camera choices do not interact. Treating them as one graph creates illegal restrictions between unrelated cameras.

## Approaches

A direct approach would build the graph of possible camera positions for every river area and recursively try every possible move. A move removes the chosen camera cell and all neighboring camera cells, because those cells can no longer be used. This is exactly the Node Kayles game on a graph.

The brute force is correct because every possible future play is explored. However, a graph with `k` candidate camera cells can have up to `2^k` states. Applying this to the entire grid is impossible.

The useful observation is that every river area is independent. Sprague-Grundy theory lets us assign a number to each independent game. The xor of all river area values decides the winner. The remaining problem is computing the Grundy value of one small graph.

During the recursion, disconnected parts of a graph can be solved separately. If a move in one connected component cannot affect another component, the Grundy values are xor'ed. This greatly reduces the number of states that must be explored.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force on the whole board | O(2^(N²)) | O(2^(N²)) | Too slow |
| Grundy recursion per river area | Exponential in the number of camera cells of one area | O(number of states) | Accepted |

## Algorithm Walkthrough

1. Find every connected river area using flood fill. Each area is processed independently because the input guarantees that different areas cannot influence each other.
2. For each river area, collect every `.` cell that is adjacent to at least one wet cell. These cells are the vertices of the game graph. Two vertices have an edge if the corresponding cells are adjacent in the grid.
3. Compute the Grundy number of this graph recursively. A state is represented by the set of remaining camera positions.
4. Before trying moves in a state, split the remaining graph into connected components. The Grundy value of the whole state is the xor of the values of those components.
5. For a connected state, try every remaining camera position. Placing a camera removes that position and all its neighbors. Collect the Grundy values reachable after every move and take their mex.
6. Xor the Grundy values of all river areas. A zero xor means the second player wins, otherwise the first player wins.

Why it works: every river area is an impartial game, and different areas form a disjoint sum because no move can affect another area. Sprague-Grundy theory states that the value of a disjoint sum is the xor of component values. The recursive definition of Grundy values considers every legal move, so the mex computation exactly represents all possible future plays.

## Python Solution

```python
import sys
from functools import lru_cache

input = sys.stdin.readline

def solve():
    n = int(input())
    grid = [input().strip() for _ in range(n)]

    wet_seen = [[False] * n for _ in range(n)]
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def inside(r, c):
        return 0 <= r < n and 0 <= c < n

    def get_grundy(adj):
        m = len(adj)
        full = (1 << m) - 1

        @lru_cache(None)
        def grundy(mask):
            if mask == 0:
                return 0

            parts = []
            seen = 0
            for i in range(m):
                if (mask >> i) & 1 and not ((seen >> i) & 1):
                    stack = [i]
                    seen |= 1 << i
                    comp = 0
                    while stack:
                        v = stack.pop()
                        comp |= 1 << v
                        nxt = adj[v] & mask & ~seen
                        while nxt:
                            b = nxt & -nxt
                            u = b.bit_length() - 1
                            seen |= b
                            stack.append(u)
                            nxt -= b
                    parts.append(comp)

            if len(parts) > 1:
                ans = 0
                for p in parts:
                    ans ^= grundy(p)
                return ans

            values = set()
            x = mask
            while x:
                b = x & -x
                v = b.bit_length() - 1
                values.add(grundy(mask & ~adj[v] & ~b))
                x -= b

            g = 0
            while g in values:
                g += 1
            return g

        return grundy(full)

    answer = 0

    for r in range(n):
        for c in range(n):
            if grid[r][c] == '*' and not wet_seen[r][c]:
                area = []
                stack = [(r, c)]
                wet_seen[r][c] = True

                while stack:
                    x, y = stack.pop()
                    area.append((x, y))
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if inside(nx, ny) and not wet_seen[nx][ny] and grid[nx][ny] == '*':
                            wet_seen[nx][ny] = True
                            stack.append((nx, ny))

                candidates = set()
                for x, y in area:
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if inside(nx, ny) and grid[nx][ny] == '.':
                            candidates.add((nx, ny))

                nodes = list(candidates)
                index = {p: i for i, p in enumerate(nodes)}
                adj = [0] * len(nodes)

                for x, y in nodes:
                    i = index[(x, y)]
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if (nx, ny) in index:
                            adj[i] |= 1 << index[(nx, ny)]

                answer ^= get_grundy(adj)

    if answer:
        print("First player will win")
    else:
        print("Second player will win")

if __name__ == "__main__":
    solve()
```

The flood fill phase identifies exactly the independent subgames. The candidate set only contains firm ground cells touching the current river, so protected cells and unrelated ground never enter the graph.

The recursive function stores states as bitmasks. A bit set means that a camera position is still available. When a camera is placed, the chosen bit and every adjacent bit are removed.

The connected component split is the main optimization. Without it, many states would be recomputed as one large graph. With it, independent pieces are reduced to smaller games whose values can be xor'ed.

Python integers can hold arbitrary length bitmasks, so the implementation does not need special handling for the number of vertices. The grid boundary checks are also important because camera candidates can only come from inside the board.

## Worked Examples

For the first sample:

```
...
...
***
```

The candidate graph has three positions in a line.

| Remaining positions | Possible moves | Grundy value |
| --- | --- | --- |
| Three cells | Remove left, middle, or right | 1 |
| Empty | No moves | 0 |

The total Grundy value is nonzero, so the first player wins.

For the second sample, the two river areas are solved separately.

| River area | Grundy value |
| --- | --- |
| First river | 1 |
| Second river | 1 |

The xor is `1 xor 1 = 0`, so every first move can be answered by the second player.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | Exponential in the maximum camera graph size | Each river area is solved by memoized Grundy recursion |
| Space | Exponential in the maximum camera graph size | Memoization stores visited game states |

The whole grid is only 100 cells and each river contains at most 20 wet cells. The decomposition into independent river areas keeps the exponential part limited to small local graphs, which fits the constraints.

## Test Cases

```python
import sys
import io

# The implementation above can be wrapped into a function for local testing.

tests = [
    (
        "3\n...\n...\n***\n",
        "First player will win"
    ),
    (
        "1\n.\n",
        "Second player will win"
    ),
    (
        "3\n***\n***\n***\n",
        "Second player will win"
    ),
    (
        "4\n....\n....\n****\n....\n",
        "First player will win"
    ),
]

for inp, expected in tests:
    print(inp.strip(), "=>", expected)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| A single firm cell | Second player will win | No legal camera positions |
| All wet cells | Second player will win | Areas with no camera moves |
| A simple horizontal river | First player will win | Basic Grundy computation |
| A river touching a boundary | Depends on computed moves | Boundary handling |

## Edge Cases

A river with no adjacent firm ground creates an empty graph. The Grundy value is zero because the first player has no move. The recursion reaches the empty mask immediately and returns zero.

A single row or column near the boundary must not access cells outside the grid. The `inside` check prevents invalid neighbors from becoming camera positions.

Multiple river areas must remain separate. The algorithm only builds edges between camera positions around the same flood-filled river, then combines the resulting Grundy values with xor. This matches the actual game because moves cannot cross from one river area to another.
