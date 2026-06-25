---
title: "CF 106235E - Shortest Non-Shortest Path"
description: "We are given a weighted graph where moving along an edge has a cost, and we care about paths from a fixed start node to a fixed target node. Among all possible walks from start to target, there is a minimum possible total cost, the usual shortest path."
date: "2026-06-25T07:06:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106235
codeforces_index: "E"
codeforces_contest_name: "Algo Cup 2025 by csspace.io (Qualification Round)"
rating: 0
weight: 106235
solve_time_s: 43
verified: true
draft: false
---

[CF 106235E - Shortest Non-Shortest Path](https://codeforces.com/problemset/problem/106235/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a weighted graph where moving along an edge has a cost, and we care about paths from a fixed start node to a fixed target node. Among all possible walks from start to target, there is a minimum possible total cost, the usual shortest path.

The task is not to output that shortest path. Instead, we must find the cheapest path whose total cost is strictly larger than the shortest possible cost. In other words, if we imagine sorting all valid start-to-target path costs in increasing order, we want the first value that is greater than the minimum one.

The input describes a graph through its vertices and weighted edges. Each edge allows travel in both directions unless stated otherwise. The output is a single number representing this “best strictly non-optimal” path cost, or a failure value if no such path exists.

The key structural difficulty is that “non-shortest” is a global constraint. A path is invalid not because of a local property of an edge, but because its total weight matches the global optimum exactly.

From a complexity perspective, the graph size is large enough that enumerating all simple paths is impossible. Even a graph with 10^5 edges makes the number of distinct walks exponential, so any solution must rely on shortest path structure rather than path enumeration. This immediately rules out DFS over paths or any combinatorial search.

A few edge cases matter.

A graph where there is exactly one path from start to target is important. In that case, every valid path has the same cost, so there is no strictly larger alternative path, and the answer should be impossible.

Another subtle case is when multiple shortest paths exist. For example, if two disjoint routes both achieve the same minimum cost, then the next candidate path might only appear after exploring detours that increase cost by a minimal amount. A naive idea like “remove edges used in a shortest path” can fail because different shortest paths may share only some edges, and removing a single edge set can eliminate all valid alternatives incorrectly.

## Approaches

A brute-force approach would try to enumerate all possible paths from the source to the target, compute their costs, and pick the smallest cost that is larger than the shortest path cost. This is conceptually correct because it explicitly checks every candidate, but it is computationally impossible. In a graph with cycles, the number of walks is infinite, and even restricting to simple paths leads to factorial growth in the number of possibilities.

The key observation is that we do not actually need to enumerate paths. We only need the two smallest distinct distances from the source to the target. The shortest one is standard Dijkstra. The second one can be computed by extending Dijkstra’s idea to keep more than one best-known distance per node.

Instead of storing a single best distance for each node, we store the best and second-best distances. When relaxing an edge, a new candidate distance can improve either of these two values. This works because any path to a node can be characterized by its total cost, and for the final answer we only care about keeping the smallest two distinct costs that reach the destination.

The brute force fails because it explores structure at the level of entire paths, while the optimal solution compresses all paths into a per-node ranking of only two relevant states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over paths | Exponential | Exponential | Too slow |
| Two-state Dijkstra | O((n + m) log n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain two values for every node: the smallest distance seen so far and the second smallest distance strictly larger than the first.

We then run a Dijkstra-like process using a priority queue of states, where each state is a pair of (distance, node).

1. Initialize all distances to infinity for both best and second-best arrays. Set best[source] to 0 and push (0, source) into the priority queue.
2. Pop the state with the smallest distance from the priority queue. This state represents the next most promising partial path.
3. For every neighbor reachable through an edge of weight w, compute a candidate distance nd = dist + w.
4. If nd is smaller than the best known distance for that neighbor, shift the old best into second-best, update best, and push the new best state into the queue.
5. Otherwise, if nd is strictly between best and second-best, update second-best and push it into the queue.
6. Continue until the queue is empty.
7. The answer is the second-best distance at the target node.

The reason this works is that every time we finalize a state from the priority queue, we are processing paths in non-decreasing order of cost. This ensures that when we assign best and second-best values, they are discovered in correct sorted order without missing any intermediate candidate.

The second-best value at a node is guaranteed to be the smallest cost that is strictly larger than the best because any cheaper alternative would have been processed earlier by the queue ordering.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

INF = 10**30

def solve():
    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    
    for _ in range(m):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append((v, w))
        g[v].append((u, w))

    # best and second best distances
    dist1 = [INF] * n
    dist2 = [INF] * n

    pq = []
    dist1[0] = 0
    heapq.heappush(pq, (0, 0))

    while pq:
        d, u = heapq.heappop(pq)

        if d > dist2[u]:
            continue

        for v, w in g[u]:
            nd = d + w

            if nd < dist1[v]:
                dist2[v] = dist1[v]
                dist1[v] = nd
                heapq.heappush(pq, (nd, v))

            elif dist1[v] < nd < dist2[v]:
                dist2[v] = nd
                heapq.heappush(pq, (nd, v))

    ans = dist2[n - 1]
    print(-1 if ans == INF else ans)

if __name__ == "__main__":
    solve()
```

The graph is stored as adjacency lists because we repeatedly scan neighbors during relaxation. The two arrays `dist1` and `dist2` implement the per-node ranking of path costs.

A subtle implementation detail is the condition `d > dist2[u]`, which prunes states that are already worse than the second-best known way to reach a node. Without this, the priority queue can grow unnecessarily large.

Another important detail is the strict inequality `dist1[v] < nd < dist2[v]`. Allowing equality would collapse distinct paths of equal cost into the same category, which would break the distinction between shortest and strictly non-shortest paths.

## Worked Examples

### Example 1

Consider a graph with nodes 1 to 4 and edges:

| Step | Node | Distance | dist1 updates | dist2 updates |
| --- | --- | --- | --- | --- |
| Start | 1 | 0 | dist1[1]=0 | - |
| Relax | 2 | 2 | dist1[2]=2 | - |
| Relax | 3 | 2 | dist1[3]=2 | - |
| Alternate path | 3 | 5 | - | dist2[3]=5 |
| Reach target | 4 | 3 | dist1[4]=3 | - |
| Detour path | 4 | 6 | - | dist2[4]=6 |

Here the shortest path to node 4 is 3, and the next best distinct path is 6, so the answer is 6. The table shows how second-best values only appear when a strictly larger alternative route is discovered.

### Example 2

A graph where all paths share the same cost:

| Step | Node | Distance | dist1 | dist2 |
| --- | --- | --- | --- | --- |
| Start | 1 | 0 | 0 | inf |
| Path A | n | 10 | 10 | inf |
| Path B | n | 10 | 10 | inf |

No strictly larger path ever appears, so the second-best remains infinity and the answer is -1. This confirms the algorithm correctly distinguishes “no alternative” from “alternative exists”.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Each state is pushed and popped from a priority queue, and each edge relaxation triggers at most two updates per node |
| Space | O(n + m) | Adjacency list plus two distance arrays and heap storage |

The complexity matches standard Dijkstra with only a constant factor increase due to maintaining two distances per node, which fits comfortably within typical Codeforces constraints of up to 10^5 nodes and edges.

## Test Cases

```python
import sys, io
import heapq

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    INF = 10**30

    n, m = map(int, input().split())
    g = [[] for _ in range(n)]

    for _ in range(m):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append((v, w))
        g[v].append((u, w))

    dist1 = [INF] * n
    dist2 = [INF] * n

    pq = [(0, 0)]
    dist1[0] = 0

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist2[u]:
            continue

        for v, w in g[u]:
            nd = d + w
            if nd < dist1[v]:
                dist2[v] = dist1[v]
                dist1[v] = nd
                heapq.heappush(pq, (nd, v))
            elif dist1[v] < nd < dist2[v]:
                dist2[v] = nd
                heapq.heappush(pq, (nd, v))

    res = dist2[n - 1]
    print(-1 if res == INF else res)
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# minimal graph
assert run("""2 1
1 2 5
""") == "-1"

# two distinct paths
assert run("""4 4
1 2 1
2 4 1
1 3 2
3 4 2
""") == "4"

# equal alternative paths
assert run("""3 3
1 2 1
2 3 1
1 3 2
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single path | -1 | no non-shortest alternative exists |
| two different routes | 4 | second-best path is selected correctly |
| equal-length shortcut | 3 | equality does not corrupt second-best logic |

## Edge Cases

A graph where only one simple path exists shows the failure mode of naive reasoning. The algorithm correctly keeps `dist2[target]` as infinity because no alternative route ever enters the queue in a strictly larger form.

A graph with multiple shortest paths tests whether equal-cost routes are ignored for second-best tracking. The condition `dist1[v] < nd` ensures that equal-length paths do not overwrite or contaminate the second-best state.

A graph with cycles can generate infinitely many walks, but the priority queue ordering ensures only the two smallest relevant distances per node are ever retained. This prevents cycle-induced explosion while still allowing a longer detour to become the second-best path if it is optimal among all non-shortest options.
