---
title: "CF 102680G - Bike Race"
description: "The problem describes a connected undirected road network. Each intersection is a vertex and each road is an edge. The three racers want to choose a starting intersection and a finishing intersection."
date: "2026-08-03T03:58:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102680
codeforces_index: "G"
codeforces_contest_name: "Brookfield Computer Programming Challenge 1"
rating: 0
weight: 102680
solve_time_s: 198
verified: true
draft: false
---

[CF 102680G - Bike Race](https://codeforces.com/problemset/problem/102680/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a connected undirected road network. Each intersection is a vertex and each road is an edge. The three racers want to choose a starting intersection and a finishing intersection. Since every racer always chooses a shortest possible route between those two points, the race route is forced to be one of the shortest paths for the chosen pair. The goal is to choose the pair of intersections whose shortest path is as long as possible.

In graph terms, we need to find the maximum shortest-path distance between any two vertices. This value is the diameter of the graph. The answer counts roads traveled, not the number of intersections visited. A path containing five intersections has length four because it uses four roads.

The input contains several test cases. Each test case gives the number of intersections and roads, followed by the undirected road connections. The graph is guaranteed to be connected, so every intersection can reach every other intersection.

The limits are small enough to allow algorithms that are around quadratic or slightly above in the number of vertices. Since the total number of intersections across all test cases is at most 1000 and each individual graph has at most 500 intersections, running a breadth-first search from every vertex is practical. A solution that tried to enumerate all pairs of vertices and search paths independently would repeat a lot of work and becomes unnecessarily expensive.

There are several edge cases where an incorrect implementation can fail. A graph with one intersection and one self-loop has no movement needed between different points, so the answer is zero.

```
1
1 1
1 1
```

The correct output is:

```
0
```

A solution that initializes the answer to one or assumes every path contains at least one road would produce the wrong result.

A graph where the longest shortest path is not a simple-looking chain is another common mistake. For example:

```
1
4 4
1 2
2 3
3 4
1 4
```

The correct output is:

```
2
```

The direct road from 1 to 4 prevents the diameter from becoming three. A careless approach that searches for the longest possible walk instead of the longest shortest path would incorrectly choose the path 1-2-3-4.

Parallel roads and self-loops also need to be handled without special cases. They do not change the shortest distance between two intersections because every road has the same cost. A BFS implementation naturally ignores repeated edges and self-loops.

## Approaches

A direct brute-force solution would consider every pair of intersections. For each pair, it would run a shortest path algorithm to find their distance, then keep the largest value found. Since the graph is unweighted, BFS is enough for each shortest path query. With $n$ vertices, there are $O(n^2)$ pairs, and each BFS costs $O(n+m)$, giving a total complexity of $O(n^2(n+m))$. With $n=500$, this is already around 125 million vertex-edge processing units per test case, and it repeats work that can be avoided.

The key observation is that the shortest distances from one starting intersection to every other intersection can be computed at once. BFS explores the graph layer by layer, so after one BFS we know the distance from one vertex to all others. Since the graph is unweighted, there is no need for Dijkstra or repeated pairwise searches.

The optimal method is to run BFS once from every intersection. Each BFS gives all distances from that source, and the largest value among them is a candidate for the diameter. Taking the maximum candidate over all sources gives the answer because every possible pair appears when one of its endpoints is used as the BFS source.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²(n+m)) | O(n+m) | Too slow |
| Optimal | O(n(n+m)) | O(n+m) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for every intersection. Each road is added in both directions because movement is allowed either way.
2. Run BFS from every intersection. During a BFS, store the shortest distance from the chosen source to every other intersection.
3. After each BFS finishes, inspect the largest distance reached from that source and update the global maximum. This value represents the longest shortest route that starts from the current intersection.
4. After all intersections have been used as BFS sources, output the largest recorded distance. Every possible start and finish pair has been considered through one of these BFS runs.

Why it works:

The invariant behind the algorithm is that after a BFS from a vertex, every stored distance is the shortest possible number of roads from that vertex to the corresponding destination. BFS has this property because it visits vertices in increasing order of distance. Since every vertex is used as a source, every pair of intersections has its shortest distance computed at least once. The maximum among all these shortest distances is exactly the graph diameter.

## Python Solution

```python
import sys
input = sys.stdin.readline

def bfs(start, graph):
    n = len(graph)
    dist = [-1] * n
    dist[start] = 0
    queue = [start]
    head = 0

    while head < len(queue):
        u = queue[head]
        head += 1
        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)

    return max(dist)

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, m = map(int, input().split())
        graph = [[] for _ in range(n)]

        for _ in range(m):
            a, b = map(int, input().split())
            a -= 1
            b -= 1
            graph[a].append(b)
            graph[b].append(a)

        diameter = 0
        for i in range(n):
            diameter = max(diameter, bfs(i, graph))

        ans.append(str(diameter))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The adjacency list stores the graph efficiently because each road is processed once in each direction. The BFS function uses a list as a queue together with an index instead of repeatedly removing the first element, avoiding the linear cost of operations like `pop(0)`.

The distance array starts with `-1`, which represents an intersection that has not been reached yet. When BFS finds an unvisited neighbor, it assigns the parent's distance plus one. Because BFS expands in layers, the first assigned distance is always the shortest one.

The outer loop runs BFS from every intersection. The largest distance returned by any BFS is the final diameter. The graph is guaranteed to be connected, so every BFS reaches all vertices and `max(dist)` is always valid.

Python integers do not overflow, and the maximum queue size is bounded by the number of intersections. The implementation also avoids recursion, which removes any risk of recursion depth issues.

## Worked Examples

For the first sample:

```
3 3
1 2
3 1
2 3
```

The graph is a triangle. Every pair of intersections has a direct road.

| BFS source | Distances | Maximum distance | Current answer |
| --- | --- | --- | --- |
| 1 | [0, 1, 1] | 1 | 1 |
| 2 | [1, 0, 1] | 1 | 1 |
| 3 | [1, 1, 0] | 1 | 1 |

The trace shows why the answer is not the number of intersections on the route. The longest shortest route uses one road, so the diameter is 1.

For the second sample:

```
5 4
1 2
3 2
3 4
5 4
```

The graph forms a chain.

| BFS source | Distances | Maximum distance | Current answer |
| --- | --- | --- | --- |
| 1 | [0, 1, 2, 3, 4] | 4 | 4 |
| 2 | [1, 0, 1, 2, 3] | 3 | 4 |
| 3 | [2, 1, 0, 1, 2] | 2 | 4 |
| 4 | [3, 2, 1, 0, 1] | 3 | 4 |
| 5 | [4, 3, 2, 1, 0] | 4 | 4 |

The endpoints of the chain give the maximum distance. Running BFS from all vertices confirms that no other pair can be farther apart.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n(n+m)) | A BFS is performed from each of the n intersections, and each BFS visits every vertex and road. |
| Space | O(n+m) | The adjacency list stores the graph and BFS stores distances and the queue. |

With at most 500 intersections per test case and a total of at most 1000 intersections across tests, the repeated BFS approach stays comfortably within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("""2
3 3
1 2
3 1
2 3
5 4
1 2
3 2
3 4
5 4
""") == "1\n4\n", "sample cases"

assert run("""1
1 1
1 1
""") == "0\n", "single intersection"

assert run("""1
4 4
1 2
2 3
3 4
1 4
""") == "2\n", "cycle shortcut"

assert run("""1
5 4
1 2
2 3
3 4
4 5
""") == "4\n", "long chain"

assert run("""1
4 6
1 2
1 3
1 4
2 3
2 4
3 4
""") == "1\n", "complete graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex with self-loop | 0 | Handles graphs with no travel needed |
| Cycle with shortcut edge | 2 | Confirms shortest paths are used instead of arbitrary long walks |
| Five-node chain | 4 | Tests the maximum distance structure |
| Complete graph | 1 | Checks dense graphs where every pair is adjacent |

## Edge Cases

A single intersection with only a self-loop is handled correctly because BFS starts with distance zero and never discovers a farther vertex. The maximum distance remains zero, matching the fact that no road must be traveled.

```
1
1 1
1 1
```

The BFS queue contains only the starting intersection. The self-loop points back to an already visited vertex, so the distance array stays `[0]`.

A graph containing shortcuts requires using shortest distances, not the longest possible route. In the example:

```
1
4 4
1 2
2 3
3 4
1 4
```

BFS from intersection 1 gives distances `[0,1,2,1]`. The route through 2 and 3 exists, but it is not a shortest route to 4 because the direct edge 1-4 is shorter. The algorithm records distance 2 as the maximum, which is correct.

Parallel roads and self-loops do not require additional handling. BFS only cares whether a neighbor has already been visited. Multiple identical edges still produce the same shortest distance, and self-loops cannot reduce a distance that is already known.
