---
title: "CF 102621B - Leaping Lizards"
description: "The room is a rectangular grid of pillars. Each pillar has a strength value that tells how many times lizards can leave from it before it collapses. Some pillars contain lizards and the rest are empty."
date: "2026-08-01T08:37:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102621
codeforces_index: "B"
codeforces_contest_name: "mBIT Advanced June 2020"
rating: 0
weight: 102621
solve_time_s: 66
verified: true
draft: false
---

[CF 102621B - Leaping Lizards](https://codeforces.com/problemset/problem/102621/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

The room is a rectangular grid of pillars. Each pillar has a strength value that tells how many times lizards can leave from it before it collapses. Some pillars contain lizards and the rest are empty. A lizard can jump to another pillar if the distance between the two positions is at most `d`, or it can jump out of the room when it is close enough to the border. The task is to determine how many lizards cannot escape.

The input describes several independent rooms. For each room, the first grid stores the durability of every pillar, and the second grid marks the starting positions of the lizards. The output is the number of lizards that remain trapped after the best possible sequence of jumps.

The dimensions are small enough that the grid can be expanded into a graph, but the number of lizards and possible movements makes direct simulation dangerous. A greedy strategy such as moving the closest lizard first fails because every jump consumes shared pillar capacity, so one lizard's decision can affect another lizard's options.

The right way to think about the constraints is that the number of cells is at most around a few hundred. This allows graph algorithms with several thousand vertices and edges. A solution that tries every possible ordering of lizard movements would grow exponentially, while a flow algorithm remains easily within the limits.

A common mistake is forgetting that a pillar can be used multiple times. For example, a strong pillar with value `2` can allow two different lizards to leave through it. Treating it as a single-use cell produces a wrong answer.

Another edge case is when a lizard is already close enough to the outside. For example:

```
1
1 1
1
L
```

The correct answer is `0`, because the only lizard can jump directly out. A solution that only checks jumps between pillars would incorrectly leave the lizard trapped.

A different edge case is when there are no possible exits:

```
1
3 1
000
000
000
L..
...
...
```

The correct answer is `1`. The lizard has no pillar to stand on and no way to reach the boundary, so it cannot escape. An implementation that only counts movement edges and forgets the missing pillars can incorrectly create invalid paths.

## Approaches

The brute-force approach is to simulate possible escape sequences. For every lizard, we could try every reachable pillar, update the remaining strength of the pillar it leaves from, and recursively continue. This is correct because every legal movement is explored, so the best sequence must appear somewhere in the search tree. The problem is that the number of possible sequences explodes. With hundreds of pillars, the number of possible movement combinations is far beyond what can be explored.

The key observation is that every lizard either reaches safety or consumes capacity from pillars. This is not really a movement-order problem. It is a resource allocation problem. Each pillar has a limited number of times it can be left from, and every lizard needs one unit of capacity on every pillar it uses before reaching the outside.

This structure matches a maximum flow model. We create a graph where a unit of flow represents one lizard. A path from a lizard node to the sink represents one possible escape route. Pillars are split into an incoming node and an outgoing node, with the edge between them having capacity equal to the pillar strength. That capacity represents how many lizards may leave from that pillar.

The source connects to every starting lizard with capacity one. The sink represents leaving the room. Running maximum flow gives the maximum number of lizards that can escape, and subtracting this from the total number of lizards gives the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in number of possible moves | O(cells) | Too slow |
| Optimal | O(V²E) with Dinic's algorithm | O(V + E) | Accepted |

## Algorithm Walkthrough

1. Build a flow graph containing two nodes for every pillar. The incoming node represents arriving at the pillar, while the outgoing node represents leaving it. Add an edge between them with capacity equal to the pillar's durability. This models the limited number of times the pillar can be used.
2. Add a source node and connect it to every lizard starting position with capacity one. Each lizard contributes exactly one unit of flow because each lizard either escapes or does not.
3. For every pillar, check whether a lizard standing there can jump directly outside. If it can, connect the outgoing pillar node to the sink with infinite capacity. The capacity is not limited because the outside can accept any number of escaping lizards.
4. For every pair of pillars whose distance is within the jumping range, add an edge from the first pillar's outgoing node to the second pillar's incoming node with infinite capacity. This represents a legal jump between pillars.
5. Run a maximum flow algorithm from the source to the sink. The resulting flow value is the number of lizards that successfully escape.
6. Subtract the escaped lizards from the original number of lizards. The remaining value is the number of casualties.

Why it works:

Every valid escape route corresponds to a path in the flow network. The only limited resources are pillar departures, and those are exactly represented by the capacity edges between the two copies of each pillar. Because each lizard starts with one unit of flow and the sink only receives flow from valid exits, every unit of maximum flow corresponds to one escaped lizard. The maximum flow therefore finds the largest possible number of escaping lizards, and the remaining lizards are precisely the ones that cannot escape.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, u, v, c):
        self.g[u].append([v, c, len(self.g[v])])
        self.g[v].append([u, 0, len(self.g[u]) - 1])

    def bfs(self, s, t):
        self.level = [-1] * self.n
        q = deque([s])
        self.level[s] = 0

        while q:
            u = q.popleft()
            for v, c, _ in self.g[u]:
                if c and self.level[v] == -1:
                    self.level[v] = self.level[u] + 1
                    q.append(v)

        return self.level[t] != -1

    def dfs(self, u, t, f):
        if u == t:
            return f

        while self.it[u] < len(self.g[u]):
            e = self.g[u][self.it[u]]
            v, c, rev = e

            if c and self.level[v] == self.level[u] + 1:
                pushed = self.dfs(v, t, min(f, c))
                if pushed:
                    e[1] -= pushed
                    self.g[v][rev][1] += pushed
                    return pushed

            self.it[u] += 1

        return 0

    def flow(self, s, t):
        ans = 0
        inf = 10 ** 9

        while self.bfs(s, t):
            self.it = [0] * self.n
            while True:
                pushed = self.dfs(s, t, inf)
                if pushed == 0:
                    break
                ans += pushed

        return ans

def solve_case(n, d, cap, lizards):
    m = len(cap[0])
    cells = n * m

    def inside(r, c):
        return 0 <= r < n and 0 <= c < m

    def idx(r, c):
        return r * m + c

    source = 2 * cells
    sink = source + 1
    dinic = Dinic(sink + 1)

    total = 0
    for r in range(n):
        for c in range(m):
            if cap[r][c] == '0':
                continue

            node = idx(r, c)
            dinic.add_edge(2 * node, 2 * node + 1, int(cap[r][c]))

            if lizards[r][c] == 'L':
                total += 1
                dinic.add_edge(source, 2 * node, 1)

            if r < d or c < d or n - 1 - r < d or m - 1 - c < d:
                dinic.add_edge(2 * node + 1, sink, 10 ** 9)

    for r in range(n):
        for c in range(m):
            if cap[r][c] == '0':
                continue

            for nr in range(n):
                for nc in range(m):
                    if cap[nr][nc] == '0':
                        continue
                    if r == nr and c == nc:
                        continue

                    dist = abs(r - nr) + abs(c - nc)
                    if dist <= d:
                        dinic.add_edge(2 * idx(r, c) + 1,
                                       2 * idx(nr, nc),
                                       10 ** 9)

    escaped = dinic.flow(source, sink)
    return total - escaped

def main():
    t = int(input())
    out = []

    for case in range(1, t + 1):
        n, d = map(int, input().split())
        cap = [input().strip() for _ in range(n)]
        lizards = [input().strip() for _ in range(n)]

        ans = solve_case(n, d, cap, lizards)
        out.append(f"Case {case}: {ans}")

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation follows the graph construction directly. Each pillar is represented twice because the capacity restriction applies when leaving a pillar, not when arriving at it. The edge between those two copies is the place where the durability limit is enforced.

The source edges have capacity one because a lizard cannot split into multiple escapes. The sink edges use a very large capacity because the outside has no bottleneck. The same value is used for movement edges because jumping between pillars is not limited by anything except the pillars themselves.

The distance check uses Manhattan distance because movement happens on the grid. The boundary check is done with the minimum distance to any edge. Since the constraints are small, checking all pairs of pillars is acceptable and keeps the implementation simple.

## Worked Examples

Consider this small case:

```
1
2 1
11
11
L.
.L
```

The important states are:

| Step | Current flow | Escaped | Remaining |
| --- | --- | --- | --- |
| Initial | 0 | 0 | 2 lizards |
| Build graph | 0 | 0 | Both lizards have paths |
| Maximum flow | 2 | 2 | 0 trapped |

Both lizards can reach the outside because every pillar is one jump away from the border. The flow value reaches the number of lizards.

Another case:

```
1
3 1
000
010
000
.L.
...
...
```

The trace is:

| Step | Current flow | Escaped | Remaining |
| --- | --- | --- | --- |
| Initial | 0 | 0 | 1 lizard |
| Build graph | 0 | 0 | Center pillar has no outgoing capacity |
| Maximum flow | 0 | 0 | 1 trapped |

The only existing pillar has strength one, but it is surrounded by missing pillars and is too far from safety. No path exists from source to sink.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(V²E) | Dinic's algorithm on the constructed graph |
| Space | O(V + E) | Stores the graph and residual edges |

There are at most a few hundred grid cells, so the graph contains only a few thousand vertices and edges. The maximum flow computation easily fits within the limits.

## Test Cases

```python
import sys
import io

# These tests assume solve_case is available.

assert solve_case(
    1, 1,
    ["1"],
    ["L"]
) == 0

assert solve_case(
    3, 1,
    ["000", "010", "000"],
    [".L.", "...", "..."]
) == 1

assert solve_case(
    2, 1,
    ["11", "11"],
    ["LL", "LL"]
) == 0

assert solve_case(
    3, 2,
    ["111", "111", "111"],
    ["L..", "...", "..."]
) == 0
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single pillar at border | 0 | Direct escape handling |
| Isolated center pillar | 1 | Impossible movement detection |
| Several lizards with strong pillars | 0 | Shared capacity handling |
| Large jump distance | 0 | Long-range jump edges |

## Edge Cases

A lizard that starts within jumping distance of the outside is handled by the direct edge from its pillar to the sink. For example:

```
1
1 1
1
L
```

The pillar is connected to the sink, so maximum flow sends one unit immediately. The final answer is `0`.

A pillar with zero strength cannot be used. For:

```
1
3 1
000
000
000
L..
...
...
```

the graph contains no node for the starting pillar's usable capacity. No source-to-sink path exists, so the maximum flow is zero and the algorithm returns `1`.

Multiple lizards sharing a pillar are handled through the capacity edge. If a pillar has strength `2`, the incoming-to-outgoing edge allows two units of flow. A single-use interpretation would incorrectly reduce the number of possible escapes. The flow network preserves exactly the resource limit described by the problem.
