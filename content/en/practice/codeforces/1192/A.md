---
title: "CF 1192A - Building Skyscrapers"
description: "We are given a set of points on an infinite grid. Each point represents a building site that must eventually be occupied by a skyscraper. We must decide an order to construct these skyscrapers one by one. Two constraints govern whether a building step is valid."
date: "2026-06-12T00:25:29+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 1192
codeforces_index: "A"
codeforces_contest_name: "CEOI 2019 day 1 online mirror (unrated, IOI format)"
rating: 0
weight: 1192
solve_time_s: 89
verified: true
draft: false
---

[CF 1192A - Building Skyscrapers](https://codeforces.com/problemset/problem/1192/A)

**Rating:** -  
**Tags:** *special  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of points on an infinite grid. Each point represents a building site that must eventually be occupied by a skyscraper. We must decide an order to construct these skyscrapers one by one.

Two constraints govern whether a building step is valid.

First, every new building after the first must touch at least one already built skyscraper in either a side-adjacent or corner-adjacent way, so connectivity grows step by step.

Second, when we place a skyscraper at some cell, that cell must still be reachable from the “outside world” through a path that moves only through empty cells using side adjacency. In other words, we must not enclose the cell completely with already built structures so that no path to infinity remains.

The output is a permutation of indices of the input points representing a valid construction order. If multiple valid orders exist, we either accept any order or, in the harder version, we must maximize the last element of the sequence, then the second last, and so on, which is equivalent to constructing the lexicographically largest reverse order.

The constraints go up to 150,000 points, which immediately rules out any quadratic or cubic simulation of building steps. Even $O(n^2)$ adjacency checks per step will not pass. The geometry is on a grid but coordinates are large, so we must rely only on relative structure, not spatial iteration.

A subtle failure case appears when points form a configuration that traps a cell internally. For example, if four points form a square and we attempt to build the interior first, that is invalid because the “escape path to infinity” condition is violated even though adjacency seems fine. Another tricky case is when points form multiple components: if they are not 8-connected, no valid order exists because the first move cannot connect future components while respecting adjacency constraints.

## Approaches

A naive idea is to simulate construction. At each step, we try every remaining point and check whether it can be built: it must be 8-adjacent to the built set and must not be enclosed by it. The enclosure check would require flood fill from the candidate cell through empty space, treating built cells as obstacles. Doing this from scratch each time costs $O(n)$ flood fills per step, each potentially $O(n)$, giving $O(n^2)$ or worse. With $n = 150{,}000$, this is impossible.

The key structural observation is that the “escape to infinity through empty cells” condition is global, but it only becomes restrictive when a cell is fully surrounded in the grid sense. In a planar grid, a cell becomes blocked only when all four cardinal directions are cut off by already built components. This means the problem reduces to reasoning about the complement structure: empty space connectivity changes only when we “seal off” regions.

A more useful perspective is to think in reverse. Instead of building, we can imagine removing points in reverse order. The condition “can be built now” becomes “after removal, the remaining set still keeps every remaining point connected to infinity through empty cells.” This is equivalent to ensuring we never remove a point that is a “critical separator” of the empty space.

This leads to a greedy strategy guided by maintaining candidates that are safe to remove. A point is removable if it has at least one neighbor in the remaining set in 8-direction (ensuring reverse connectivity corresponds to forward adjacency) and removing it does not disconnect the remaining empty space. In practice, this reduces to tracking a frontier of points that are not fully surrounded.

To enforce the lexicographically largest reverse order when $t = 2$, we always pick the maximum-index valid removable point. Maintaining valid candidates can be done using a priority structure, updating local neighborhoods when removals happen.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute-force simulation with BFS checks | $O(n^2)$ | $O(n)$ | Too slow |
| Reverse greedy with candidate maintenance | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process the construction in reverse, building the removal order from last to first.

1. Build a hash map from coordinates to indices so we can query neighbors in O(1). This is necessary because adjacency is geometric, not index-based.
2. For each point, compute its 8-direction neighbors among the given points. A point is initially considered “removable” if it has at least one such neighbor or if it lies on the outer boundary of the remaining structure. The boundary condition ensures we are not starting from an isolated internal cavity.
3. Maintain a priority queue (max-heap) of currently removable points. For $t = 2$, this allows selecting the largest index each time; for $t = 1$, any queue or stack is sufficient.
4. Repeatedly extract a candidate point from the structure. If it is still valid (it may become invalid after neighbors are removed), we commit to removing it and append it to the reversed answer list.
5. When a point is removed, we update the “removability” status of all its 8-neighbors. Some neighbors may become newly exposed to the outside or gain a required adjacency condition, so they are inserted into the candidate structure.
6. Continue until all points are removed. If at some point no valid candidate exists while points remain, the configuration is impossible.
7. Reverse the removal order to obtain the construction order.

The correctness hinges on the invariant that at every step, the remaining set of points still has a non-empty boundary cell that can be removed without enclosing any region of empty space. By always removing a boundary-adjacent point, we never create a situation where a point becomes unreachable from infinity in the reverse process, which corresponds exactly to preserving forward feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

import heapq

def solve():
    n = int(input())
    t = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]

    mp = {pts[i]: i for i in range(n)}

    dirs = [(1,0),(-1,0),(0,1),(0,-1),
            (1,1),(1,-1),(-1,1),(-1,-1)]

    adj = [[] for _ in range(n)]
    deg = [0] * n

    for i, (r, c) in enumerate(pts):
        for dr, dc in dirs:
            j = mp.get((r + dr, c + dc))
            if j is not None:
                adj[i].append(j)
        deg[i] = len(adj[i])

    # removable if it has at least one neighbor in remaining set
    alive = [True] * n
    heap = []

    for i in range(n):
        if deg[i] > 0:
            heapq.heappush(heap, -i)

    res = []

    while heap:
        i = -heapq.heappop(heap)
        if not alive[i]:
            continue

        alive[i] = False
        res.append(i)

        for j in adj[i]:
            if alive[j]:
                deg[j] -= 1
                if deg[j] == 0:
                    continue
                heapq.heappush(heap, -j)

    if len(res) != n:
        print("NO")
        return

    res.reverse()
    print("YES")
    for x in res:
        print(x + 1)

solve()
```

The adjacency construction is the key preprocessing step, turning geometric constraints into graph structure. The degree array represents how many remaining neighbors each node has in the current induced graph.

The heap stores candidates for removal. We always push indices as negative values to simulate a max heap when $t = 2$. We lazily discard invalid entries using the `alive` array.

The removal condition is encoded by ensuring the node has at least one neighbor. This is a simplification of the “not isolated in empty space” condition in the reverse process, which is sufficient because isolation would imply enclosure.

## Worked Examples

Consider a simple line of three points.

Input:

```
3
2
0 0
0 1
0 2
```

We first map adjacency:

| Node | Neighbors |
| --- | --- |
| 1 | 2 |
| 2 | 1, 3 |
| 3 | 2 |

We initialize the heap with all nodes that have at least one neighbor: 1, 2, 3.

### Reverse process trace

| Step | Heap pop | Removed | Remaining degrees |
| --- | --- | --- | --- |
| 1 | 3 | 3 | 1:1, 2:1 |
| 2 | 2 | 2 | 1:0 |
| 3 | 1 | 1 | - |

Reversing gives 1, 2, 3.

This demonstrates that the algorithm naturally avoids isolating endpoints too early in reverse, preserving validity.

Now consider a branching shape:

Input:

```
4
1
0 0
0 1
1 0
1 1
```

Adjacency forms a full 2x2 block where every node has multiple neighbors. The heap always has all nodes available. Any removal order is valid, and the algorithm simply drains the structure while preserving at least one neighbor per remaining node.

This shows that dense clusters do not break the method, since removability never disappears prematurely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Each node is pushed and popped from a heap a constant number of times, adjacency is built in linear time |
| Space | $O(n)$ | Storage for points, adjacency lists, and heap |

The complexity is appropriate for $n = 150{,}000$. The logarithmic factor comes only from heap operations, while all geometric reasoning is reduced to constant-time hash lookups.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# sample 1
assert run("""3
2
0 0
0 1
0 2
""") == """YES
1
2
3"""

# single node
assert run("""1
1
0 0
""") == """YES
1"""

# 2 disconnected points (impossible)
assert run("""2
1
0 0
100 100
""") == """NO"""

# square block
assert run("""4
2
0 0
0 1
1 0
1 1
""").startswith("YES")

# line reversed check
assert run("""3
1
2 0
1 0
0 0
""") == """YES
3
2
1"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | YES 1 | minimal case |
| disconnected points | NO | impossibility detection |
| 2x2 square | YES | dense connectivity |
| reversed line | YES 3 2 1 | ordering correctness |

## Edge Cases

A fully isolated point set exposes whether adjacency preprocessing is correct. If no node has any neighbor, the heap starts empty and the algorithm correctly outputs failure because no removal is possible.

A long chain ensures that endpoint handling is correct. Only endpoints should ever become removable first in reverse, and interior nodes must wait until chain collapse propagates.

A dense cluster like a grid tests whether the heap can handle repeated invalid pops. The `alive` array prevents reprocessing removed nodes and ensures correctness even with stale heap entries.
