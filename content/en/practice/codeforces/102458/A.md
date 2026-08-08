---
title: "CF 102458A - Daniel and Perpendophobia"
description: "The geometric story becomes much simpler if we look only at coordinates. Suppose Daniel has already recorded a point (u, v). A mine (x, y) must be avoided whenever x = u or y = v, because the segment joining the two points is then vertical or horizontal."
date: "2026-08-09T02:37:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102458
codeforces_index: "A"
codeforces_contest_name: "Hanoi final contest"
rating: 0
weight: 102458
solve_time_s: 390
verified: true
draft: false
---

[CF 102458A - Daniel and Perpendophobia](https://codeforces.com/problemset/problem/102458/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

The geometric story becomes much simpler if we look only at coordinates. Suppose Daniel has already recorded a point `(u, v)`. A mine `(x, y)` must be avoided whenever `x = u` or `y = v`, because the segment joining the two points is then vertical or horizontal. In other words, every recorded point makes its entire vertical line and horizontal line unavailable for future mines.

The origin is recorded before Daniel visits anything, so every mine with `x = 0` or `y = 0` is immediately unusable. Whenever Daniel visits a mine `(x, y)`, the coordinate value `x` becomes unavailable forever, and the coordinate value `y` also becomes unavailable forever.

This gives the real combinatorial structure of the problem. If we decide to visit several mines, no two visited mines may have the same `x` coordinate, and no two may have the same `y` coordinate. Conversely, any collection of mines satisfying those two conditions can be visited in any order. After visiting one mine, only its own `x` and `y` values become forbidden, so another mine with both coordinates still unused remains legal.

Thus the task is to choose as many mines as possible such that all chosen `x` coordinates are distinct and all chosen `y` coordinates are distinct, after discarding mines lying on either axis.

There can be up to `80,000` mines, while coordinates can be as large as `10^9`. The large coordinate range means we cannot build an array indexed directly by coordinates. More importantly, `N = 80,000` rules out quadratic algorithms: even `O(N^2)` would require around `6.4 * 10^9` pair checks in the worst case. We need an algorithm close to linear or perhaps `O(N sqrt N)`.

There are several edge cases that are easy to mishandle. Consider

```
1
0 7
```

The answer is `0`, because the origin has already recorded `x = 0`, so this mine is forbidden immediately. A solution that only checks whether the current mine is unexplored would incorrectly count it.

Now consider

```
3
1 1
1 2
2 3
```

The answer is `2`. We can visit `(1, 1)` and then `(2, 3)`. We cannot visit both `(1, 1)` and `(1, 2)`, because after the first visit every mine with `x = 1` is forbidden. A careless solution that only checks whether the `y` coordinates differ could count all three.

Another subtle case is

```
4
0 1
1 2
2 3
3 0
```

The answer is `2`. The two mines touching an axis are unusable from the start, leaving `(1, 2)` and `(2, 3)`. They have different `x` and `y` coordinates, so both can be visited. Simply treating every input mine as an available edge would overcount.

## Approaches

A direct brute-force solution can simulate every possible sequence of visits. At each state it checks all mines and recursively chooses every mine that is currently legal. This is correct because every legal sequence is considered, so the largest number of visited mines must appear in the search.

The problem is the number of sequences. In a configuration where many mines can be chosen, the search can explore permutations of almost all `N` mines. The number of possible prefixes is on the order of

`1 + N + N(N-1) + ... + N!`,

which is `O(N!)`. Even if checking a candidate were constant time, `N!` is already hopeless. At `N = 20`, `20!` is about `2.43 * 10^18`, far beyond anything executable.

The brute-force works because a visit only changes which coordinate values are available. That observation lets us throw away the geometry completely. Give every distinct `x` coordinate one vertex on the left and every distinct `y` coordinate one vertex on the right. Each mine `(x, y)` becomes an edge connecting its `x` vertex to its `y` vertex.

Now choosing a mine means choosing its corresponding edge. Two mines can both be visited exactly when their edges do not share an endpoint. So a valid collection of mines is precisely a matching in this bipartite graph.

The maximum number of mines Daniel can explore is consequently the size of a maximum bipartite matching. Mines with `x = 0` or `y = 0` are omitted because those coordinates are already occupied by the recorded origin.

A simple augmenting-path matching algorithm would repeatedly search through the whole graph and can become quadratic. With up to `80,000` edges, the appropriate implementation is Hopcroft-Karp, which finds augmenting paths in batches and runs in `O(E sqrt V)` time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N!) | O(N) recursion plus state | Too slow |
| Optimal | O(N sqrt N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Read all mines and discard every mine with `x = 0` or `y = 0`. The origin has already recorded both coordinate values, so those mines can never be selected.
2. Compress the remaining distinct `x` coordinates and distinct `y` coordinates into consecutive integer IDs. The original coordinates can be as large as `10^9`, but only equality between coordinates matters, so their actual magnitudes are irrelevant.
3. Create a bipartite graph. For every remaining mine `(x, y)`, add an edge from the compressed vertex representing `x` to the vertex representing `y`. Each edge corresponds to exactly one mine.
4. Maintain `pair_left[x]`, the right vertex currently matched to a left vertex, and `pair_right[y]`, the left vertex currently matched to a right vertex. An unmatched vertex is represented by `-1`.
5. Run Hopcroft-Karp. First perform a BFS from every unmatched left vertex. The BFS builds layers through alternating unmatched and matched edges and records the shortest distance at which a free right vertex can be reached.
6. Run DFS from every currently unmatched left vertex, following only edges that respect the BFS layers. Whenever the DFS reaches an unmatched right vertex, an augmenting path has been found, so all edges along that path can be flipped and the matching size increases by one.
7. Repeat the BFS and DFS phases until no augmenting path exists. At that point the current matching is maximum, so its size is the answer.

Why it works is captured by the matching invariant. At every moment, the selected edges represent mines with pairwise distinct `x` and `y` coordinates, so they form a feasible exploration plan. Whenever Hopcroft-Karp finds an augmenting path, flipping its edges preserves the matching property while increasing its size by exactly one. When BFS can no longer find an augmenting path, the augmenting-path theorem says that no larger matching exists. Since matchings and feasible sets of mines are exactly the same objects here, the final matching size is exactly the maximum number of mines Daniel can explore.

## Python Solution

```python
import sys
input = sys.stdin.readline

def maximum_mines(data):
    it = iter(map(int, data.split()))
    n = next(it)

    mines = []
    xs = {}
    ys = {}

    for _ in range(n):
        x = next(it)
        y = next(it)

        # The origin has already forbidden x = 0 and y = 0.
        if x == 0 or y == 0:
            continue

        if x not in xs:
            xs[x] = len(xs)
        if y not in ys:
            ys[y] = len(ys)

        mines.append((xs[x], ys[y]))

    nx = len(xs)
    ny = len(ys)

    graph = [[] for _ in range(nx)]
    for x, y in mines:
        graph[x].append(y)

    pair_left = [-1] * nx
    pair_right = [-1] * ny
    dist = [-1] * nx

    from collections import deque

    def bfs():
        q = deque()
        found = False

        for u in range(nx):
            if pair_left[u] == -1:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = -1

        while q:
            u = q.popleft()

            for v in graph[u]:
                matched_u = pair_right[v]

                if matched_u == -1:
                    found = True
                elif dist[matched_u] == -1:
                    dist[matched_u] = dist[u] + 1
                    q.append(matched_u)

        return found

    sys.setrecursionlimit(max(1_000_000, nx * 2 + 10))

    def dfs(u):
        for v in graph[u]:
            matched_u = pair_right[v]

            if matched_u == -1 or (
                dist[matched_u] == dist[u] + 1 and dfs(matched_u)
            ):
                pair_left[u] = v
                pair_right[v] = u
                return True

        dist[u] = -1
        return False

    matching = 0

    while bfs():
        for u in range(nx):
            if pair_left[u] == -1 and dfs(u):
                matching += 1

    return str(matching)

def main():
    data = sys.stdin.buffer.read()
    sys.stdout.write(maximum_mines(data))

if __name__ == "__main__":
    main()
```

The first pass compresses coordinates while reading the mines. Using dictionaries is necessary because coordinates range up to `10^9`; the compressed IDs are at most `N - 1`.

The graph contains one edge per usable mine. There is no need to store the original coordinates after compression, because the only operation the algorithm needs is testing whether two coordinates are equal.

`pair_left` and `pair_right` describe the current matching from both directions. Having both arrays makes it possible to follow an alternating path efficiently. If a right vertex is already matched, `pair_right[v]` immediately tells us which left vertex must be visited next.

The BFS constructs the layers used by Hopcroft-Karp. An unmatched right vertex means that the current BFS has found a possible endpoint of an augmenting path. The DFS then searches only through the layered structure, avoiding arbitrary paths that cannot belong to a shortest augmenting path.

The recursive DFS is safe after increasing Python's recursion limit. A graph with `80,000` edges can produce a long alternating path, so relying on Python's default recursion limit would be unsafe.

There is no integer-overflow issue in Python, and the coordinates themselves are never used in arithmetic. The answer is at most `N`, so the matching counter is also small.

## Worked Examples

For the first sample,

```
5
100 400
200 200
200 300
300 400
400 100
```

The compressed graph has left vertices representing `100, 200, 300, 400` and right vertices representing `100, 200, 300, 400`.

| Step | Left vertex | Chosen right vertex | Matching |
| --- | --- | --- | --- |
| 1 | 100 | 400 | `(100,400)` |
| 2 | 200 | 200 | `(100,400), (200,200)` |
| 3 | 300 | 400 | cannot keep this, `400` is occupied |
| 3 | 300 | 400 via reassignment | rearrange if possible |
| 3 | 300 | no free right after current choices | try another augmenting path |
| 3 | 400 | 100 | `(100,400), (200,200), (400,100)` |

The maximum matching has size `3`. For example, the three mines `(100,400)`, `(200,200)`, and `(400,100)` can be visited. Trying to add `(300,400)` fails because its `y = 400` conflicts with the first mine.

The trace demonstrates why this is not simply a problem of counting distinct `x` and `y` coordinates. The edges determine which combinations are actually available, so a matching algorithm is needed.

For the second sample,

```
4
0 1
1 2
2 3
3 0
```

The two axis mines disappear immediately.

| Step | Mine | Action | Matching size |
| --- | --- | --- | --- |
| 1 | `(0,1)` | discard because `x = 0` | 0 |
| 2 | `(1,2)` | add to matching | 1 |
| 3 | `(2,3)` | add to matching | 2 |
| 4 | `(3,0)` | discard because `y = 0` | 2 |

The answer is `2`. The two surviving mines use different `x` coordinates and different `y` coordinates, so they form a valid matching and can both be explored.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N sqrt N) | The graph has at most `N` edges and `O(N)` vertices, and Hopcroft-Karp takes `O(E sqrt V)` |
| Space | O(N) | Coordinate maps, graph edges, matching arrays, distances, and the BFS queue are all linear |

With `N <= 80,000`, the graph contains at most `80,000` edges and at most `160,000` compressed vertices. The solution avoids every quadratic scan over pairs of mines and uses only linear graph storage, so it fits the intended large subtask and the `512 MB` memory limit.

## Test Cases

```python
import sys
from collections import deque

def solve_string(data: str) -> str:
    it = iter(map(int, data.split()))
    n = next(it)

    mines = []
    xs = {}
    ys = {}

    for _ in range(n):
        x = next(it)
        y = next(it)

        if x == 0 or y == 0:
            continue

        if x not in xs:
            xs[x] = len(xs)
        if y not in ys:
            ys[y] = len(ys)

        mines.append((xs[x], ys[y]))

    nx = len(xs)
    ny = len(ys)

    graph = [[] for _ in range(nx)]
    for x, y in mines:
        graph[x].append(y)

    left = [-1] * nx
    right = [-1] * ny
    dist = [-1] * nx

    def bfs():
        q = deque()
        found = False

        for u in range(nx):
            if left[u] == -1:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = -1

        while q:
            u = q.popleft()

            for v in graph[u]:
                w = right[v]

                if w == -1:
                    found = True
                elif dist[w] == -1:
                    dist[w] = dist[u] + 1
                    q.append(w)

        return found

    sys.setrecursionlimit(max(1_000_000, nx * 2 + 10))

    def dfs(u):
        for v in graph[u]:
            w = right[v]

            if w == -1 or (
                dist[w] == dist[u] + 1 and dfs(w)
            ):
                left[u] = v
                right[v] = u
                return True

        dist[u] = -1
        return False

    ans = 0

    while bfs():
        for u in range(nx):
            if left[u] == -1 and dfs(u):
                ans += 1

    return str(ans)

def run(inp: str) -> str:
    return solve_string(inp)

# Provided sample 1
assert run(
    """5
100 400
200 200
200 300
300 400
400 100
"""
) == "3", "sample 1"

# Provided sample 2
assert run(
    """4
0 1
1 2
2 3
3 0
"""
) == "2", "sample 2"

# Minimum-size input
assert run(
    """1
7 9
"""
) == "1", "single usable mine"

# All mines share the same x coordinate
assert run(
    """5
1 1
1 2
1 3
1 4
1 5
"""
) == "1", "all equal x coordinates"

# Axis boundaries plus a valid pair
assert run(
    """5
0 10
10 0
1 2
2 3
3 4
"""
) == "3", "axis mines must be ignored"

# Alternating-path case
assert run(
    """4
1 1
1 2
2 1
3 3
"""
) == "3", "augmenting path must rearrange an earlier match"

# Maximum-size input: 80,000 distinct independent mines
large = ["80000"]
large.extend(f"{i} {i}" for i in range(1, 80001))
assert run("\n".join(large)) == "80000", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7 9` | `1` | Minimum input and the basic one-edge matching |
| Five mines with `x = 1` | `1` | Repeated coordinates cannot be visited twice |
| Mines on both axes plus `(1,2),(2,3),(3,4)` | `3` | Correct handling of the origin's forbidden coordinates |
| `(1,1),(1,2),(2,1),(3,3)` | `3` | An augmenting path can replace an earlier matching choice |
| `80,000` diagonal mines | `80,000` | Maximum input size and linear graph construction |

## Edge Cases

A mine on an axis is handled before the graph is built. For

```
1
0 7
```

the mine is discarded because its `x` coordinate is already present in the origin. No graph edge remains, so Hopcroft-Karp returns `0`. The same reasoning applies to a mine such as `(8,0)`.

When many mines have the same coordinate, they all become edges incident to one graph vertex. For

```
5
1 1
1 2
1 3
1 4
1 5
```

there is only one left vertex and five right vertices. A matching can contain only one edge because every edge shares that left endpoint. The algorithm returns `1`, exactly matching the fact that visiting any one of these mines permanently forbids the other four.

The origin itself is not an input mine, but its coordinates still matter. In

```
4
0 1
1 2
2 3
3 0
```

the first and last mines are removed because they share a coordinate with the recorded origin. The remaining two edges are disjoint, giving a matching of size `2`. This prevents the common mistake of building a matching over all input edges without accounting for the initial state.

The augmenting-path case

```
4
1 1
1 2
2 1
3 3
```

has an especially useful structure. A naive greedy algorithm might first choose `(1,1)`, which blocks both `(1,2)` and `(2,1)`. A maximum matching instead chooses `(1,2)` and `(2,1)`, then `(3,3)`, reaching `3`. Hopcroft-Karp can discover this through an augmenting path that changes an earlier choice. This is why an arbitrary greedy matching is not sufficient.

Finally, the coordinate limit of `10^9` does not create a special case in the implementation. Coordinates are stored as dictionary keys and immediately compressed to small integer IDs. The algorithm never allocates an array of size proportional to the coordinate value, so a mine such as `(1000000000, 999999999)` costs exactly the same amount of graph storage as a mine such as `(1,2)`.
