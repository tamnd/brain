---
title: "CF 242C - King's Path"
description: "We are given a gigantic chessboard whose coordinates go up to $10^9$, so the board itself is far too large to store explicitly. Only some cells are usable. These usable cells are described as row segments: for a row $r$, every column from $a$ to $b$ is allowed."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "hashing", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 242
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 149 (Div. 2)"
rating: 1800
weight: 242
solve_time_s: 102
verified: true
draft: false
---

[CF 242C - King's Path](https://codeforces.com/problemset/problem/242/C)

**Rating:** 1800  
**Tags:** dfs and similar, graphs, hashing, shortest paths  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a gigantic chessboard whose coordinates go up to $10^9$, so the board itself is far too large to store explicitly. Only some cells are usable. These usable cells are described as row segments: for a row $r$, every column from $a$ to $b$ is allowed.

A king starts at one allowed cell and wants to reach another allowed cell. In one move, the king may move to any of the eight neighboring cells, including diagonals. The king is never allowed to stand on a forbidden cell.

The task is to compute the minimum number of king moves needed to reach the destination, or report that no path exists.

The most important constraint is not the board size, but the total number of allowed cells. Even though coordinates go up to $10^9$, the total length of all segments is at most $10^5$. That means there are at most $10^5$ usable cells in the entire graph.

This changes the problem completely. We do not care about the empty space of the board at all. We only care about the explicitly listed allowed cells.

A shortest path problem with at most $10^5$ vertices immediately suggests BFS. Since every king move has equal cost, BFS gives the minimum number of moves automatically.

There are several edge cases that easily break careless implementations.

Suppose the allowed segments overlap.

Input:

```
1 1 1 3
2
1 1 2
1 2 3
```

The actual allowed cells are $(1,1), (1,2), (1,3)$. If we store segments separately without merging logically through a set structure, we may accidentally duplicate cells and process them multiple times.

The correct answer is:

```
2
```

Another dangerous case is when coordinates are huge but the usable region is tiny.

Input:

```
1000000000 1000000000 999999999 999999999
2
1000000000 1000000000 1000000000
999999999 999999999 999999999
```

The answer is:

```
1
```

Any solution trying to allocate a $10^9 \times 10^9$ grid obviously fails immediately.

Disconnected components are another easy trap.

Input:

```
1 1 3 3
2
1 1 1
3 3 3
```

The answer is:

```
-1
```

A DFS that stops when it first reaches the target would not be wrong here, but DFS does not guarantee shortest paths in general. Since every move has equal weight, BFS is the correct traversal.

Diagonal movement is also easy to forget.

Input:

```
1 1 2 2
2
1 1 1
2 2 2
```

The correct answer is:

```
1
```

A four-direction BFS would incorrectly produce `-1`.

## Approaches

The most direct brute-force idea is to model the entire board as a grid graph and run BFS from the starting position. Each cell has up to eight neighbors, and BFS would correctly compute the minimum number of moves.

The problem is the board size. Coordinates reach $10^9$, so even storing one boolean per cell is impossible. A full-grid BFS would require astronomical memory and time.

The key observation is that the board is mostly irrelevant. The king may only stand on allowed cells, and the total number of allowed cells is at most $10^5$.

That means we can compress the graph implicitly. Instead of thinking about a gigantic board, we think about a graph whose vertices are exactly the allowed cells.

For each allowed cell $(x,y)$, the king may move to any of these neighboring positions:

$$(x + dx, y + dy)$$

where $dx, dy \in \{-1,0,1\}$ and not both zero.

If the neighboring cell is also allowed, we add an edge implicitly during BFS.

This gives us a graph with at most $10^5$ vertices and at most $8 \cdot 10^5$ neighbor checks. That is completely manageable.

Efficient lookup becomes the central implementation detail. We need to answer:

"Is cell $(nx, ny)$ allowed and unvisited?"

in approximately constant time.

A hash set is perfect for this. We store every allowed cell inside a set of coordinate pairs.

Then BFS becomes straightforward:

1. Start from the initial cell.
2. Pop cells from the queue in increasing distance order.
3. Try all eight king moves.
4. Push valid unvisited neighbors.

Because BFS explores by distance layers, the first time we reach the destination is guaranteed to be optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over entire board | Impossible | Impossible | Too slow |
| BFS over allowed cells with hashing | $O(K)$ | $O(K)$ | Accepted |

Here $K$ is the total number of allowed cells, and $K \le 10^5$.

## Algorithm Walkthrough

1. Read the start and target coordinates.
2. Read all allowed segments and expand them into individual allowed cells.

Since the total segment length is at most $10^5$, expanding them explicitly is safe.
3. Store every allowed cell inside a hash set.

This allows constant-time membership checks during BFS.
4. Initialize a queue for BFS and a distance map.

The queue stores cells to process. The distance map stores the minimum number of moves needed to reach each visited cell.
5. Push the starting cell into the queue with distance $0$.
6. While the queue is not empty, pop the front cell.
7. If the current cell is the target, return its distance immediately.

BFS processes states in increasing distance order, so the first visit to the target is optimal.
8. Try all eight king moves.

For every pair $(dx, dy)$ where $dx, dy \in \{-1,0,1\}$ and not both zero:

1. Compute the neighboring cell.
2. Check whether it exists in the allowed-cell set.
3. Check whether it has already been visited.
4. If valid, assign distance + 1 and push it into the queue.
9. If BFS finishes without reaching the target, print `-1`.

### Why it works

The algorithm models every allowed cell as a graph vertex. Two vertices are adjacent exactly when the king can move between them in one step.

All edges have equal weight $1$, so BFS explores vertices in nondecreasing order of shortest-path distance from the source.

The invariant during BFS is:

"Whenever a cell is popped from the queue, its recorded distance is the minimum possible number of moves from the start."

This holds because BFS always processes all vertices at distance $d$ before any vertex at distance $d+1$.

Since every legal king move is explored and forbidden cells are ignored, the BFS traversal exactly matches the legal movement rules of the problem.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    x0, y0, x1, y1 = map(int, input().split())

    n = int(input())

    allowed = set()

    for _ in range(n):
        r, a, b = map(int, input().split())

        for c in range(a, b + 1):
            allowed.add((r, c))

    q = deque()
    q.append((x0, y0))

    dist = {(x0, y0): 0}

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    while q:
        x, y = q.popleft()

        if (x, y) == (x1, y1):
            print(dist[(x, y)])
            return

        current_dist = dist[(x, y)]

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            nxt = (nx, ny)

            if nxt not in allowed:
                continue

            if nxt in dist:
                continue

            dist[nxt] = current_dist + 1
            q.append(nxt)

    print(-1)

solve()
```

The solution begins by expanding all segments into explicit coordinate pairs. This is safe because the total number of generated cells is bounded by $10^5$.

The `allowed` set is the core data structure. Every BFS transition needs to test whether a neighboring cell is valid. A hash set gives average $O(1)$ lookup time.

The `dist` dictionary serves two purposes simultaneously. It stores shortest distances and also acts as the visited structure. If a node already exists in `dist`, it has already been processed or queued before.

The BFS queue processes cells in increasing order of distance. As soon as the target cell is popped, we know its distance is minimal and can terminate immediately.

One subtle detail is that we do not remove visited cells from `allowed`. Either approach works, but keeping `allowed` immutable and using `dist` as the visitation check keeps the logic simpler.

Another easy mistake is forgetting diagonal movement. The king has eight possible moves, not four.

The coordinate values themselves may be as large as $10^9$, but Python tuples and hash sets handle them naturally. Since we only store reachable allowed cells, the coordinate magnitude never affects complexity.

## Worked Examples

### Sample 1

Input:

```
5 7 6 11
3
5 3 8
6 7 11
5 2 5
```

Allowed cells become:

Row 5: columns 2 through 8

Row 6: columns 7 through 11

The BFS progression looks like this:

| Step | Current Cell | Distance | Newly Added Cells |
| --- | --- | --- | --- |
| 1 | (5,7) | 0 | (5,6), (5,8), (6,7), (6,8) |
| 2 | (5,6) | 1 | (5,5) |
| 3 | (5,8) | 1 | (6,9) |
| 4 | (6,7) | 1 | none |
| 5 | (6,8) | 1 | none |
| 6 | (5,5) | 2 | (5,4) |
| 7 | (6,9) | 2 | (6,10) |
| 8 | (5,4) | 3 | (5,3) |
| 9 | (6,10) | 3 | (6,11) |
| 10 | (6,11) | 4 | target reached |

Output:

```
4
```

This trace demonstrates that BFS expands uniformly by move count. Even though many cells are reachable, the first time we encounter `(6,11)` is guaranteed to be optimal.

### Example 2

Input:

```
1 1 3 3
3
1 1 1
2 2 2
3 3 3
```

The king can move diagonally through the middle cell.

| Step | Current Cell | Distance | Newly Added Cells |
| --- | --- | --- | --- |
| 1 | (1,1) | 0 | (2,2) |
| 2 | (2,2) | 1 | (3,3) |
| 3 | (3,3) | 2 | target reached |

Output:

```
2
```

This example confirms that diagonal movement is handled correctly. A four-direction traversal would fail here.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(K)$ | Each allowed cell is inserted once and processed once |
| Space | $O(K)$ | The allowed set, queue, and distance map store at most $K$ cells |

Here $K$ is the total number of allowed cells, and the problem guarantees $K \le 10^5$.

The BFS performs at most eight neighbor checks per cell, so the total amount of work remains linear in the number of usable cells. This easily fits within the 2-second limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    x0, y0, x1, y1 = map(int, input().split())

    n = int(input())

    allowed = set()

    for _ in range(n):
        r, a, b = map(int, input().split())

        for c in range(a, b + 1):
            allowed.add((r, c))

    q = deque([(x0, y0)])
    dist = {(x0, y0): 0}

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    while q:
        x, y = q.popleft()

        if (x, y) == (x1, y1):
            return str(dist[(x, y)]) + "\n"

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            nxt = (nx, ny)

            if nxt not in allowed:
                continue

            if nxt in dist:
                continue

            dist[nxt] = dist[(x, y)] + 1
            q.append(nxt)

    return "-1\n"

# provided sample
assert run(
"""5 7 6 11
3
5 3 8
6 7 11
5 2 5
"""
) == "4\n", "sample 1"

# direct diagonal move
assert run(
"""1 1 2 2
2
1 1 1
2 2 2
"""
) == "1\n", "diagonal movement"

# disconnected cells
assert run(
"""1 1 3 3
2
1 1 1
3 3 3
"""
) == "-1\n", "unreachable target"

# overlapping segments
assert run(
"""1 1 1 3
2
1 1 2
1 2 3
"""
) == "2\n", "overlapping segments"

# larger chain
assert run(
"""1 1 1 5
1
1 1 5
"""
) == "4\n", "straight movement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 4 | General BFS traversal |
| Diagonal-only path | 1 | Correct handling of king moves |
| Disconnected cells | -1 | Proper unreachable detection |
| Overlapping segments | 2 | Deduplication through hash sets |
| Straight row movement | 4 | Distance accumulation correctness |

## Edge Cases

### Overlapping Segments

Input:

```
1 1 1 3
2
1 1 2
1 2 3
```

The segments overlap at `(1,2)`.

The algorithm inserts cells into a set:

```
(1,1), (1,2), (1,3)
```

The duplicate insertion of `(1,2)` changes nothing because sets automatically deduplicate elements.

BFS proceeds:

```
(1,1) -> (1,2) -> (1,3)
```

Output:

```
2
```

Without a set, a careless implementation might enqueue the same cell multiple times.

### Huge Coordinates

Input:

```
1000000000 1000000000 999999999 999999999
2
1000000000 1000000000 1000000000
999999999 999999999 999999999
```

The cells are diagonally adjacent.

The algorithm never allocates a grid. It only stores:

```
(1000000000, 1000000000)
(999999999, 999999999)
```

BFS checks the eight neighboring positions and immediately reaches the target.

Output:

```
1
```

The coordinate magnitude has no effect on memory usage.

### Disconnected Components

Input:

```
1 1 3 3
2
1 1 1
3 3 3
```

BFS starts from `(1,1)`.

All eight neighboring cells are forbidden, so the queue becomes empty immediately.

Since the target was never reached, the algorithm prints:

```
-1
```

This confirms that the BFS correctly distinguishes unreachable states.

### Diagonal-Only Connectivity

Input:

```
1 1 3 3
3
1 1 1
2 2 2
3 3 3
```

The only valid path is:

```
(1,1) -> (2,2) -> (3,3)
```

A four-direction traversal would incorrectly fail here.

The BFS explicitly tries all eight king directions, so both diagonal moves are discovered correctly.

Output:

```
2
```
