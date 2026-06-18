---
problem: 1302D
contest_id: 1302
problem_index: D
name: "Dijkstra"
contest_name: "AIM Tech Poorly Prepared Contest (unrated, funny, Div. 1 preferred)"
rating: 0
tags: []
answer: passed_samples
verified: true
solve_time_s: 118
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2dd221-335c-83ec-b708-83f1f83c1158
---

# CF 1302D - Dijkstra

**Rating:** ?  
**Tags:** -  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 58s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2dd221-335c-83ec-b708-83f1f83c1158  

---

## Solution

## Problem Understanding

We are given an undirected graph where each connection between two vertices has a non-negative weight. The task is to determine the minimum possible total weight needed to travel from vertex 1 to vertex n, or report that it is impossible if no sequence of edges connects them.

This is a classic shortest path query on a weighted graph with up to 200,000 vertices and 200,000 edges. Each edge cost can be as large as 10^9, so any solution must carefully manage cumulative sums using 64-bit integers.

The constraint size immediately rules out any approach that tries to recompute paths exhaustively. A naive breadth-first search is invalid because edge weights are not uniform. A Floyd-Warshall style all-pairs computation is impossible since it would require O(n^3) time. Even repeated relaxation without structure would degrade to O(nm), which is far too slow when both n and m are large.

One subtle edge case comes from disconnected graphs. For example, if the input is:

```
4 2
1 2 3
3 4 5
```

then there is no path from 1 to 4, and the correct output is -1. Any implementation that initializes distances incorrectly or assumes reachability would incorrectly return a large default value instead of recognizing this disconnection.

Another important case is multiple edges between the same pair of vertices. Since the graph is not simple, there may be several different costs between two nodes. A correct solution must always consider the cheapest effective transition, not overwrite blindly or assume uniqueness.

## Approaches

A direct but incorrect approach is to try exploring all possible paths from 1 to n, accumulating costs along each route and tracking the minimum. This quickly becomes exponential in the number of vertices, since every branching in the graph doubles the number of partial paths being considered. Even pruning revisits only slightly improves the situation, but the worst case still explodes because the same vertex can be reached through many different cost contexts.

A more structured attempt is to run a breadth-first search-like traversal while relaxing distances whenever a shorter path is found. This works only if all edges have equal weight, which is not the case here. With arbitrary weights, BFS may finalize a node too early and miss a cheaper path discovered later.

The key observation is that all edge weights are non-negative, so once we know the currently best tentative distance to a vertex, we can safely expand vertices in increasing order of distance. This is exactly the condition required for Dijkstra’s algorithm. Instead of exploring blindly, we always process the next vertex with the smallest known distance, guaranteeing that when it is processed, its shortest distance is final.

This ordering is efficiently maintained using a min-heap priority queue. Each time we improve the distance to a node, we push it into the heap. Each extraction gives us the next most promising vertex to expand.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Path Enumeration | Exponential | O(n) | Too slow |
| Dijkstra with Min Heap | O((n + m) log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list representation of the graph. Each vertex stores all outgoing edges as pairs of (neighbor, cost). This structure allows fast iteration over neighbors during relaxation.
2. Initialize a distance array where every vertex is set to infinity, except vertex 1 which is set to 0. This encodes the fact that we start at node 1 with zero cost.
3. Create a min-heap priority queue and insert the pair (0, 1). The heap is used to always expand the currently closest known vertex.
4. While the heap is not empty, extract the vertex u with the smallest known distance d. This vertex represents the most promising frontier point.
5. If the extracted distance d is larger than the stored distance for u, skip it. This prevents processing outdated heap entries that were pushed before a better path was discovered.
6. For every neighbor v of u with edge weight w, check whether reaching v through u improves its current best known distance. If d + w is smaller than dist[v], update dist[v] and push (dist[v], v) into the heap. This step propagates improvements outward from confirmed shortest paths.
7. After the heap is exhausted, check dist[n]. If it is still infinity, output -1; otherwise output dist[n].

### Why it works

The algorithm relies on the property that once a node is removed from the priority queue with the smallest distance among all candidates, that distance is final. Any alternative path to that node would have to go through another node with equal or greater tentative distance, which cannot produce a smaller result without contradicting the ordering enforced by the heap. This guarantees that every node is settled in increasing order of true shortest distance, ensuring correctness of all relaxations.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

INF = 10**30

n, m = map(int, input().split())
g = [[] for _ in range(n + 1)]

for _ in range(m):
    a, b, c = map(int, input().split())
    g[a].append((b, c))
    g[b].append((a, c))

dist = [INF] * (n + 1)
dist[1] = 0

pq = [(0, 1)]

while pq:
    d, u = heapq.heappop(pq)

    if d != dist[u]:
        continue

    for v, w in g[u]:
        nd = d + w
        if nd < dist[v]:
            dist[v] = nd
            heapq.heappush(pq, (nd, v))

print(-1 if dist[n] == INF else dist[n])
```

The adjacency list construction ensures that each edge is stored exactly twice, once for each direction, since the graph is undirected. The distance array uses a large sentinel value to represent unreached vertices, and Python’s arbitrary precision integers safely handles large path sums without overflow issues.

The heap always stores candidate states, and the check `d != dist[u]` discards stale entries efficiently. Without this check, the algorithm would still be correct but slower due to redundant expansions.

## Worked Examples

### Example 1

Input:

```
3 3
1 2 5
2 3 1
1 3 7
```

We track the algorithm state.

| Step | Node popped | dist array (1,2,3) | Action |
| --- | --- | --- | --- |
| 1 | (0,1) | (0,∞,∞) | relax 2→5, 3→7 |
| 2 | (5,2) | (0,5,7) | relax 3→6 |
| 3 | (6,3) | (0,5,6) | done |

The heap processes node 2 before node 3 because 5 < 7, allowing a shorter route to 3 to be discovered. This confirms that greedy expansion is necessary.

Output is 6.

### Example 2

Input:

```
4 3
1 2 4
2 3 5
1 4 20
```

| Step | Node popped | dist array (1,2,3,4) | Action |
| --- | --- | --- | --- |
| 1 | (0,1) | (0,4,∞,20) | relax neighbors |
| 2 | (4,2) | (0,4,9,20) | relax 3 |
| 3 | (9,3) | (0,4,9,20) | no change |
| 4 | (20,4) | (0,4,9,20) | done |

This shows how indirect paths are discovered progressively, and direct but expensive edges are naturally ignored.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | each edge may trigger a heap update, each update costs log n |
| Space | O(n + m) | adjacency list plus distance array and heap storage |

With up to 200,000 nodes and edges, this complexity comfortably fits within the time limit because the logarithmic factor remains small and each operation is linear in practice.

## Test Cases

```python
import sys, io
import heapq

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    INF = 10**30

    n, m = map(int, input().split())
    g = [[] for _ in range(n + 1)]

    for _ in range(m):
        a, b, c = map(int, input().split())
        g[a].append((b, c))
        g[b].append((a, c))

    dist = [INF] * (n + 1)
    dist[1] = 0

    pq = [(0, 1)]

    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    return str(-1 if dist[n] == INF else dist[n])

# provided sample
assert run("""3 3
1 2 5
2 3 1
1 3 7
""") == "6"

# custom: disconnected graph
assert run("""4 2
1 2 3
3 4 5
""") == "-1"

# custom: multiple edges
assert run("""3 3
1 2 10
1 2 2
2 3 3
""") == "5"

# custom: direct vs indirect
assert run("""4 4
1 4 100
1 2 1
2 3 1
3 4 1
""") == "3"

# custom: single node
assert run("""1 0
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| disconnected graph | -1 | unreachable handling |
| multiple edges | 5 | correct edge minimization |
| indirect path better than direct | 3 | Dijkstra correctness |
| single node | 0 | base case correctness |

## Edge Cases

A disconnected graph such as `1-2` and `3-4` tests whether unreachable nodes are detected correctly. The distance to node n remains infinity, and the algorithm returns -1 without attempting invalid paths.

Multiple edges between the same nodes ensure that relaxation logic does not assume uniqueness. In the test case with edges `1-2 (10)` and `1-2 (2)`, the heap processes both, but only the smaller weight updates the distance, and the algorithm correctly propagates value 2.

A graph where a direct edge is worse than an indirect path highlights the importance of ordering by distance. The direct edge to node 4 is 100, but the chain 1→2→3→4 produces 3. The heap ensures nodes are expanded in increasing cost, allowing the shorter multi-step route to be discovered first and correctly overwrite the initial direct guess.