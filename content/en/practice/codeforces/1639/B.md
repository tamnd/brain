---
title: "CF 1639B - Treasure Hunt"
description: "This task is an interactive graph exploration problem. We start from a known vertex of a connected undirected graph. Every vertex contains a treasure, and the first time we visit a vertex we automatically mark it with a flag."
date: "2026-06-10T04:23:58+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "interactive"]
categories: ["algorithms"]
codeforces_contest: 1639
codeforces_index: "B"
codeforces_contest_name: "Pinely Treasure Hunt Contest"
rating: 0
weight: 1639
solve_time_s: 74
verified: true
draft: false
---

[CF 1639B - Treasure Hunt](https://codeforces.com/problemset/problem/1639/B)

**Rating:** -  
**Tags:** graphs, interactive  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

This task is an interactive graph exploration problem. We start from a known vertex of a connected undirected graph. Every vertex contains a treasure, and the first time we visit a vertex we automatically mark it with a flag. From the current position we only see, for each neighboring vertex, its degree and whether it already contains a flag. We do not know the actual labels of the neighbors.

A further complication is that the order of neighbors is randomized independently every time we enter a vertex. Even if we return to the same place, the first neighbor in the list may correspond to a different edge than before. The graph itself never changes, but there is no stable numbering of outgoing edges.

The objective is not to reconstruct the graph. We only need to visit every vertex at least once while using a reasonably small number of moves.

The graph contains at most 300 vertices and every degree is at most 50. Such small limits mean that any strategy with a few tens of thousands of moves is acceptable. Since the contest materials contain the complete graphs in advance, contestants could tailor their strategies to each test. The intended idea, however, is much simpler: design a random walk that prefers unexplored territory.

The most dangerous pitfall is assuming that an edge can be remembered by its position in the neighbor list.

Consider a path

```
1 - 2 - 3
```

Suppose we are at vertex 2 and the interactor currently reports

```
degree 1, unflagged
degree 1, flagged
```

Later, after returning to vertex 2, the order might become

```
degree 1, flagged
degree 1, unflagged
```

Choosing "neighbor number 1" both times does not correspond to traversing the same edge.

Another mistake is trying to reconstruct vertices solely by degree patterns. Two different neighbors may have identical degrees and identical flag states.

For example

```
    2
    |
1 - 3 - 4
```

Vertices 1 and 4 both have degree 1. When standing at 3, they are indistinguishable. Any deterministic attempt to assign identities can easily become inconsistent.

The correct approach avoids identifying neighbors altogether.

## Approaches

The most straightforward strategy is a completely uniform random walk. Whenever we arrive at a vertex, we choose one of its neighbors uniformly at random.

This method is correct because a connected graph is eventually covered by a random walk with probability 1. Unfortunately, the expected cover time of some graphs is large. For example, lollipop graphs are famous examples where pure random walks require about $O(n^3)$ moves in expectation. Even with only 300 vertices, this can become unnecessarily expensive.

The key observation is that the interactor tells us which neighboring vertices have already been visited. Since our goal is to discover new vertices, we should always move to an unflagged neighbor whenever such a neighbor exists.

Suppose the current vertex has several neighbors and at least one of them has not been visited yet. Going to a flagged neighbor cannot immediately increase the number of discovered vertices, while going to an unflagged one certainly does. Thus prioritizing unvisited neighbors is always beneficial.

Eventually we reach regions where every adjacent vertex has already been seen. At that point we need some mechanism to escape and continue exploring. Choosing randomly among all neighbors works well. This creates a biased random walk that aggressively expands whenever possible and otherwise wanders until it reaches a frontier vertex again.

The strategy does not require reconstructing the graph or remembering edge identities. It uses only the information available at the current step.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force random walk | Expected O(n³) moves | O(1) | Accepted but inefficient |
| Prefer unvisited neighbors | Expected much smaller, roughly O(m) to O(n²) in practice | O(1) | Accepted |

## Algorithm Walkthrough

1. Start at the given vertex. It is immediately considered visited.
2. Whenever the interactor reports the current vertex, inspect all neighboring descriptions.
3. Collect the indices corresponding to neighbors whose flag equals 0. These represent vertices that have never been visited.
4. If this set is nonempty, choose one of those indices. Visiting such a vertex increases the number of discovered vertices by one.
5. If every neighbor already has a flag, choose a random neighbor among all available choices. This allows the walk to leave dead ends and eventually reach unexplored regions again.
6. Continue until the interactor outputs `"AC"`.

### Why it works

The graph is connected. Whenever an unvisited neighbor exists, the algorithm immediately discovers a new vertex. Once the local neighborhood has been exhausted, the process becomes a random walk over already discovered vertices.

A random walk on a connected graph reaches every vertex with probability 1. Consequently, it eventually reaches a vertex adjacent to an undiscovered vertex. At that moment the algorithm immediately expands into that vertex. Repeating this argument shows that every vertex is eventually visited.

## Python Solution

Since this is an interactive problem, the code communicates with the interactor after every move.

```python
import sys
import random

input = sys.stdin.readline

rng = random.Random()

t = int(input())

for _ in range(t):
    n, m, start, base_move_count = map(int, input().split())

    for _ in range(m):
        input()

    while True:
        parts = input().split()

        if parts[0] == "AC" or parts[0] == "F":
            break

        d = int(parts[1])

        unvisited = []
        all_neighbors = []

        ptr = 2
        for i in range(d):
            deg = int(parts[ptr])
            flag = int(parts[ptr + 1])
            ptr += 2

            all_neighbors.append(i + 1)
            if flag == 0:
                unvisited.append(i + 1)

        if unvisited:
            move = rng.choice(unvisited)
        else:
            move = rng.choice(all_neighbors)

        print(move)
        sys.stdout.flush()
```

The graph description is given before the interaction starts, but this strategy does not need it. Those lines are simply read and discarded.

For every reported vertex, the code scans the neighbor descriptions. The variable `unvisited` stores indices whose flag equals zero. If this list is nonempty, one of its elements is chosen uniformly at random. Otherwise a random neighbor among all neighbors is selected.

The neighbor indices are one-based because the interactor expects values from 1 to `d`. Forgetting this conversion is a common source of wrong answers.

Another subtle detail is flushing the output after every move. Without flushing, the interactor never receives the answer and the solution hangs.

## Worked Examples

Because the real interaction is randomized, it is easier to illustrate the strategy on fixed scenarios.

### Example 1

Consider

```
1 - 2 - 3
```

Suppose we start at vertex 1.

| Current vertex | Neighbor flags | Candidate set | Chosen move |
| --- | --- | --- | --- |
| 1 | [0] | [2] | 2 |
| 2 | [1,0] | [3] | 3 |
| 3 | [1] | [2] | 2 |

The first two moves always discover a new vertex. After reaching vertex 3, all treasures have already been collected.

This example demonstrates how the algorithm greedily expands whenever possible.

### Example 2

Consider a star graph.

```
    2
    |
3 - 1 - 4
    |
    5
```

Start from vertex 1.

| Current vertex | Neighbor flags | Candidate set | Chosen move |
| --- | --- | --- | --- |
| 1 | [0,0,0,0] | all four leaves | one leaf |
| Leaf | [1] | none | center |
| 1 | [1,0,0,0] | three unvisited leaves | one leaf |
| Leaf | [1] | none | center |
| 1 | [1,1,0,0] | two unvisited leaves | one leaf |

Every return to the center exposes remaining unvisited leaves, and the process continues until all leaves are explored.

This example shows why random moves are needed when reaching dead ends.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total number of moves) | Each move processes one vertex description |
| Space | O(50) | Degree never exceeds 50 |

The graph itself contains at most 300 vertices and maximum degree 50. Processing one interaction step is constant time. The amount of memory used is negligible compared with the 256 MB limit.

## Test Cases

Interactive problems cannot be tested with ordinary input-output pairs because the judge reacts to our moves. Still, we can test the local decision logic.

```
def choose(flags):
    unvisited = [i + 1 for i, x in enumerate(flags) if x == 0]
    if unvisited:
        return unvisited
    return list(range(1, len(flags) + 1))

# one unvisited neighbor
assert choose([1, 0, 1]) == [2]

# all neighbors already visited
assert choose([1, 1, 1]) == [1, 2, 3]

# all neighbors unvisited
assert choose([0, 0, 0]) == [1, 2, 3]

# degree one vertex
assert choose([1]) == [1]

# mixed configuration
assert choose([0, 1, 0, 1]) == [1, 3]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| [1,0,1] | [2] | Preference for unexplored neighbors |
| [1,1,1] | [1,2,3] | Random walk fallback |
| [0,0,0] | [1,2,3] | Multiple candidate choices |
| [1] | [1] | Degree one vertices |
| [0,1,0,1] | [1,3] | Correct filtering |

## Edge Cases

Consider a path of two vertices.

```
1 - 2
```

Starting from vertex 1, the only neighbor is unvisited, so the algorithm immediately moves to vertex 2 and finishes. Degree one vertices cause no special difficulties.

Another interesting case is a cycle

```
1 - 2 - 3 - 4 - 1
```

Suppose we have already visited vertices 1, 2, and 3. At vertex 2, both neighbors are flagged, so the algorithm performs a random move. Eventually it reaches vertex 3, which still has an unvisited neighbor 4. The moment such a frontier vertex is reached, the algorithm expands again.

Finally, consider symmetric vertices with identical degrees. For example,

```
    2
    |
1 - 3 - 4
```

Vertices 1 and 4 both have degree one. The algorithm never tries to distinguish them. It only uses their flag states, so the changing order of neighbors cannot invalidate any stored information. This avoids the main difficulty of the problem.
