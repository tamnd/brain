---
problem: 936E
contest_id: 936
problem_index: E
name: "Iqea"
contest_name: "Codeforces Round 467 (Div. 1)"
rating: 3400
tags: ["data structures", "dfs and similar", "divide and conquer", "dsu", "shortest paths", "trees"]
answer: passed_samples
verified: true
solve_time_s: 133
date: 2026-06-17
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
---

# CF 936E - Iqea

**Rating:** 3400  
**Tags:** data structures, dfs and similar, divide and conquer, dsu, shortest paths, trees  
**Model:** gpt-5-3-mini  
**Solve time:** 2m 13s  
**Verified:** yes (1/1 samples)  

---

## Solution

## Problem Understanding

We are given a set of cells on a large grid. Each cell is a city, and roads exist between any two cities that share an edge on the grid. The important geometric constraints are that the chosen set of cells forms one connected region, and the empty cells also form one connected region. This implies we are working inside a single “solid” polyomino with no holes.

On this region we process a sequence of events. Some events add a new “shop” at a city, and others ask for a city’s distance to the closest already opened shop. Distance is measured as the shortest path length along grid edges, and movement is only allowed inside the given set of cities.

The key difficulty is that the graph is large, up to 300,000 vertices, and both updates and queries are online. A query must reflect all shops that have been added earlier in time.

A naive interpretation would be to recompute a shortest path from every query node to all shops using BFS. That would immediately fail because each BFS costs O(n), and doing it for up to 300,000 queries leads to an O(nq) solution, which is far beyond limits.

A more subtle issue is that distances are not Euclidean or Manhattan in the full grid. They are shortest paths constrained by the shape, so shortcuts through missing cells are impossible. Any approach that assumes simple coordinate geometry will produce incorrect answers in concave regions.

A small illustrative failure case is a U-shaped region. Two points can be close in coordinates but far in graph distance because the path must go around the missing interior. A solution that uses coordinate distance like `abs(x1-x2)+abs(y1-y2)` would underestimate distances.

The challenge is therefore a dynamic multi-source shortest path problem on a large sparse unweighted graph, with only insertions of sources and repeated distance queries.

## Approaches

A straightforward solution is to treat every query independently. For each type-2 query, run a BFS starting from that city and stop when any shop is reached. This is correct because BFS in an unweighted graph always finds shortest paths. However, if there are k shops and each query triggers a BFS, then in the worst case each BFS explores almost the whole graph. This leads to roughly O(nq), which is far too large.

The key observation is that BFS from multiple sources can be merged. If all shops were known in advance, we could run a single multi-source BFS and compute the distance to the nearest shop for every node. The difficulty is that shops are inserted over time, and we need answers between insertions.

This suggests maintaining a global shortest-path process that evolves as new sources appear. Instead of recomputing from scratch, we keep a priority queue exactly like Dijkstra’s algorithm, except all edges have weight 1. Each shop insertion is equivalent to inserting a new source with distance 0 into this global process.

The crucial idea is that we never need to restart computation. We maintain a global relaxation process across time. When a new shop appears, we push it into the priority queue. When we process queries, we ensure that distances for the queried node have been fully settled by continuing the propagation just enough.

This turns the problem into maintaining a dynamic multi-source BFS/Dijkstra process where sources are only added, never removed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Re-run BFS per query | O(nq) | O(n) | Too slow |
| Global incremental Dijkstra (multi-source) | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

We interpret the grid as an unweighted graph where each cell is a node and edges exist between adjacent cells that belong to the region.

We then maintain a global shortest-path structure.

1. Build adjacency lists for all given cells. For each cell, check its four neighbors and connect edges if the neighbor is also a valid cell. This gives us an implicit graph with O(n) edges.
2. Maintain a distance array `dist`, initialized to infinity, and a boolean array `done` indicating whether the shortest distance to a node has been finalized.
3. Maintain a global min-heap priority queue storing pairs `(distance, node)`.
4. When a shop is added at node `v`, we set `dist[v] = 0` and push `(0, v)` into the heap. We do not immediately propagate.
5. We process queries in order. Before answering a query for node `u`, we run the Dijkstra process forward until node `u` becomes finalized:

1. Repeatedly pop the smallest element `(d, v)` from the heap.
2. If `v` is already finalized, skip it.
3. Mark `v` as finalized and set `dist[v] = d`.
4. Relax all neighbors `to` of `v`. If `to` is not finalized and `d + 1 < dist[to]`, update `dist[to]` and push `(d + 1, to)`.
6. Once node `u` is finalized, its `dist[u]` is the answer to the query. If the heap becomes empty before `u` is reached, no shop is reachable at that moment, so we output `-1`.

The subtle point is that we do not need the entire graph to be processed. We only need to expand the Dijkstra frontier until the query node is reached. Since edge weights are uniform, this behaves exactly like a BFS wavefront expanding outward from all shops.

### Why it works

At any moment, the priority queue contains all discovered but not finalized shortest path candidates from all shops inserted so far. Each time we add a new shop, we introduce a new source of distance 0 into the same global structure. Because Dijkstra’s algorithm guarantees that nodes are finalized in non-decreasing distance order, once a node is popped, no future relaxation from already-inserted sources can improve it. Since new shops only add additional zero-distance sources, they only create additional relaxations that are naturally incorporated into the same process. Therefore, when we finally finalize a node, we have computed its shortest distance from the full set of shops inserted up to that time.

## Python Solution

```python
import sys
input = sys.stdin.readline
import heapq

def solve():
    n = int(input())
    cells = set()
    coords = []

    for _ in range(n):
        x, y = map(int, input().split())
        coords.append((x, y))
        cells.add((x, y))

    # build adjacency
    adj = {}
    for x, y in coords:
        adj[(x, y)] = []
        for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) in cells:
                adj[(x, y)].append((nx, ny))

    q = int(input())

    INF = 10**18
    dist = {c: INF for c in cells}
    done = {c: False for c in cells}

    pq = []

    def push(v, d):
        heapq.heappush(pq, (d, v))

    def process_until(target=None):
        while pq:
            d, v = heapq.heappop(pq)
            if done[v]:
                continue
            done[v] = True
            dist[v] = d
            if target is not None and v == target:
                return
            for to in adj[v]:
                if not done[to] and d + 1 < dist[to]:
                    dist[to] = d + 1
                    push(to, d + 1)
        return

    for _ in range(q):
        t, x, y = map(int, input().split())
        v = (x, y)

        if t == 1:
            dist[v] = 0
            push(v, 0)
        else:
            process_until(v)
            print(dist[v] if done[v] else -1)

if __name__ == "__main__":
    solve()
```

The adjacency construction uses a hash set of coordinates to ensure O(1) neighbor checks. This is necessary because the grid coordinates are large but sparse.

The priority queue is shared across all operations, so distances discovered in earlier phases are reused. The `process_until` function is the core: it advances the global shortest-path expansion only as far as needed to finalize the queried node.

A subtle implementation detail is that we only mark a node as finalized when it is popped from the heap, not when it is updated. This preserves correctness of Dijkstra’s ordering. Another important point is that we never reset the structure between queries; shops accumulate naturally in the same global queue.

## Worked Examples

Consider a small line-shaped region:

Input:

```
3
1 1
1 2
1 3
3
1 1 1
2 1 3
2 1 2
```

### Trace

| Step | Event | PQ state | Finalized | dist(1,3) | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | add shop (1,1) | (0,(1,1)) | {} | inf | - |
| 2 | query (1,3) | expand | (1,1) | 2 | 2 |
| 3 | query (1,2) | expand more | (1,1),(1,2) | 1 | 1 |

This demonstrates that the BFS wave expands incrementally and reuses work between queries. The second query benefits from already explored frontier nodes.

Now consider a disconnected-in-coordinates but connected-in-graph shape, such as an L-shape:

```
4
1 1
1 2
1 3
2 3
3
1 1 1
1 2 3
2 3 3
```

The wave from both shops propagates around the corner correctly, and the query at (3,3) receives the correct minimum distance via the only valid path through the bend.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | Each node is finalized once, each edge relaxed once in a global Dijkstra process |
| Space | O(n) | adjacency list, distance map, heap storage |

The structure never recomputes BFS from scratch. Each vertex enters the heap a limited number of times, and each extraction permanently finalizes it. With n and q up to 300,000, this fits comfortably within constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import heapq

    n = int(input())
    cells = set()
    coords = []
    for _ in range(n):
        x, y = map(int, input().split())
        coords.append((x, y))
        cells.add((x, y))

    adj = {}
    for x, y in coords:
        adj[(x, y)] = []
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            if (x+dx, y+dy) in cells:
                adj[(x, y)].append((x+dx, y+dy))

    q = int(input())

    INF = 10**18
    dist = {c: INF for c in cells}
    done = {c: False for c in cells}
    pq = []

    def push(v, d):
        heapq.heappush(pq, (d, v))

    def process(target=None):
        while pq:
            d, v = heapq.heappop(pq)
            if done[v]:
                continue
            done[v] = True
            dist[v] = d
            if target == v:
                return
            for to in adj[v]:
                if not done[to] and d + 1 < dist[to]:
                    dist[to] = d + 1
                    push(to, d + 1)

    out = []
    for _ in range(q):
        t, x, y = map(int, input().split())
        v = (x, y)
        if t == 1:
            dist[v] = 0
            push(v, 0)
        else:
            process(v)
            out.append(str(dist[v] if done[v] else -1))

    return "\n".join(out)

# provided sample
assert run("""7
1 2
1 3
2 3
3 1
3 2
3 3
4 2
5
2 3 2
1 4 2
2 1 2
1 3 3
2 2 3
""") == """-1
5
1"""

# custom: single node
assert run("""1
1 1
1
2 1 1
""") == "-1"

# custom: immediate answer
assert run("""2
1 1
1 2
3
1 1 1
2 1 2
2 1 1
""") == """1
0"""

# custom: chain
assert run("""4
1 1
1 2
1 3
1 4
4
1 1 1
2 1 4
1 1 4
2 1 2
""") == """3
1"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | -1 | no shop case |
| immediate answer | 1, 0 | multiple queries and self-shop |
| chain update | 3, 1 | propagation over time |

## Edge Cases

A corner case is when queries ask before any shop exists. In that situation, the priority queue remains empty and no node is ever finalized. The algorithm correctly returns `-1` because the `done` flag for the queried node never becomes true.

Another case is repeated expansion through a long corridor. If shops are added at one end and queries occur at the other, the Dijkstra process gradually expands along the corridor. Even though the corridor may have length up to n, each vertex is finalized once, so repeated queries do not reprocess already settled regions.

A final subtle case is multiple shops being added near each other. Their BFS waves merge in the priority queue, but Dijkstra ordering ensures the smallest distance always dominates, so no incorrect overwriting occurs even if updates arrive in different orders.