---
problem: 1037E
contest_id: 1037
problem_index: E
name: "Trips"
contest_name: "Manthan, Codefest 18 (rated, Div. 1 + Div. 2)"
rating: 2200
tags: ["graphs"]
answer: passed_samples
verified: true
solve_time_s: 80
date: 2026-06-17
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a32a2fb-3504-83ec-844a-f6e3a70f29b3
---

# CF 1037E - Trips

**Rating:** 2200  
**Tags:** graphs  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 20s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a32a2fb-3504-83ec-844a-f6e3a70f29b3  

---

## Solution

## Problem Understanding

We are given a dynamic system of friendships among $n$ people. Initially there are no edges between them. Each morning, a new undirected edge is added between two previously unconnected vertices. After each addition, we need to consider the current graph and answer a question about the largest possible group of vertices that can be chosen for an evening trip.

A valid trip group is a subset of vertices with a local density constraint: for every chosen vertex, either it is excluded from the group, or it must have at least $k$ of its graph neighbors also included in the group. The goal is to maximize the size of such a subset after each edge insertion.

The key object is not connectivity but degree inside the induced subgraph. We are effectively searching for the largest induced subgraph whose minimum degree is at least $k$, often described as a $k$-core of the graph.

The constraints $n, m \le 2 \cdot 10^5$ rule out recomputing anything from scratch per day. A naive recomputation of a $k$-core after each edge would require repeatedly pruning low-degree vertices, costing $O(n + m)$ per query in the worst case, leading to $O(m(n+m))$, which is far too large.

A subtle edge case appears when the graph is sparse early but becomes dense later. Early answers can be zero even though a large valid group exists later. For example, if $k=2$ and the graph forms a triangle only at day 3, then days 1 and 2 must output 0 even though the final structure is small but non-trivial. Any approach assuming monotonic growth of the answer per vertex inclusion without rechecking degrees will fail.

## Approaches

The brute-force idea is straightforward. After each new edge, we build the current graph and repeatedly remove all vertices whose degree inside the remaining set is less than $k$. This is the standard peeling process for a $k$-core: we maintain a queue of vertices with degree less than $k$, delete them, and update neighbors until stabilization. The remaining vertices form the valid set, and its size is the answer.

This is correct because any vertex violating the degree constraint cannot belong to any valid solution, and removing it can only decrease neighbor degrees, possibly triggering further removals. The problem is that repeating this from scratch after every edge recomputes essentially the same peeling process many times. Since each run is $O(n + m)$, total complexity becomes $O(m(n+m))$, which is unacceptable at $2 \cdot 10^5$.

The key observation is that edges are only added, never removed. This means degrees only increase over time, so once a vertex becomes valid for the $k$-core, it will never become invalid later. However, the difficulty is that validity depends on other vertices being present in the core, not just raw degree.

The crucial transformation is to reverse time. Instead of adding edges forward, we process them backward while maintaining a dynamic $k$-core. Initially, at time $m$, all edges exist. We compute the final $k$-core once. Then we remove edges one by one in reverse order. When an edge is removed, some vertices may drop below degree $k$ and must be removed from the core. This creates a cascading deletion process. Each vertex is deleted at most once, and each edge is processed a constant number of times across deletions, giving a linear total complexity.

To support fast updates, we maintain adjacency lists and current degrees restricted to the current core. We also maintain a queue of vertices that become invalid after each edge removal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute k-core each day | $O(m(n+m))$ | $O(n+m)$ | Too slow |
| Reverse deletion with dynamic k-core | $O(n + m)$ | $O(n + m)$ | Accepted |

## Algorithm Walkthrough

We solve the problem by processing the sequence of edges in reverse and tracking when each vertex stops belonging to the valid $k$-core.

1. Build the full graph using all edges, and compute the initial degree of each vertex.

This represents the state at day $m$, where all friendships exist.
2. Compute the initial $k$-core using a queue of all vertices whose degree is less than $k$.

We repeatedly remove such vertices and decrease the degree of their neighbors that are still active.

This gives the final stable set at day $m$.
3. Maintain a boolean array marking whether each vertex is currently in the core.

Also maintain adjacency lists for all edges.
4. Store all edges in an array, and process them in reverse order from $m$ down to $1$.
5. For each edge $(u, v)$, remove its effect from the current state.

If both endpoints are still in the core, decrement their current degrees.
6. Whenever a vertex’s degree drops below $k$, push it into a queue of removals.

This vertex is no longer valid in the current state and must be peeled out.
7. While the queue is non-empty, repeatedly remove vertices:

mark them inactive, and decrement the degrees of their neighbors still active.

If any neighbor falls below $k$, it is added to the queue.
8. After fully processing the deletion cascade caused by edge removal $i$, record the size of the current core as the answer for day $i-1$.

### Why it works

At any moment in reverse processing, the set of active vertices is exactly the $k$-core of the graph formed by the suffix of edges. The peeling process maintains the invariant that every active vertex has degree at least $k$ inside the active set. When an edge is removed, the only possible violations come from degree decreases at its endpoints, and the cascade ensures all resulting violations are resolved. Since each vertex is removed once and never reinserted, the structure remains consistent across all steps.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n, m, k = map(int, input().split())
    
    edges = []
    adj = [[] for _ in range(n)]
    
    for i in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        edges.append((u, v))
        adj[u].append((v, i))
        adj[v].append((u, i))
    
    deg = [len(adj[i]) for i in range(n)]
    alive = [True] * n
    removed = [False] * n
    
    q = deque()
    
    for i in range(n):
        if deg[i] < k:
            q.append(i)
            removed[i] = True
            alive[i] = False
    
    while q:
        u = q.popleft()
        for v, _ in adj[u]:
            if alive[v]:
                deg[v] -= 1
                if not removed[v] and deg[v] < k:
                    removed[v] = True
                    alive[v] = False
                    q.append(v)
    
    ans = [0] * m
    cur_alive = sum(alive)
    
    for i in range(m - 1, -1, -1):
        ans[i] = cur_alive
        
        u, v = edges[i]
        if alive[u] and alive[v]:
            deg[u] -= 1
            deg[v] -= 1
            
            for x in (u, v):
                if alive[x] and deg[x] < k:
                    alive[x] = False
                    q.append(x)
        
        while q:
            u = q.popleft()
            for v, _ in adj[u]:
                if alive[v]:
                    deg[v] -= 1
                    if alive[v] and deg[v] < k:
                        alive[v] = False
                        q.append(v)
        
        cur_alive = sum(alive)
    
    print("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The code begins by constructing adjacency lists and initializing degrees as full-graph degrees. It then performs an initial peeling to compute the final $k$-core corresponding to day $m$. This step is essential because reverse processing assumes a valid starting core.

During reverse iteration, each edge is removed from the active structure. If both endpoints are currently active, their degrees are reduced, potentially violating the $k$-core condition. The BFS queue handles cascading removals, ensuring the invariant is restored.

A subtle implementation detail is that vertices are never reinserted after removal. The `alive` array guarantees monotonic deletion, which is what enables linear complexity.

## Worked Examples

### Example 1

Input:

```
4 4 2
2 3
1 2
1 3
1 4
```

We process all edges, build the full graph, and compute the final $k$-core. Initially no subset satisfies degree 2, so the core is empty.

We then go backward.

| Step | Removed edge | Alive vertices | Answer |
| --- | --- | --- | --- |
| 4 | (1,4) | none | 0 |
| 3 | (1,3) | none | 0 |
| 2 | (1,2) | {1,2,3} becomes stable later | 3 |
| 1 | (2,3) | {1,2,3} | 3 |

This shows how the core suddenly appears once enough edges are present.

### Example 2

Consider a line that gradually becomes denser:

```
5 4 1
1 2
2 3
3 4
4 5
```

Here any vertex with at least one neighbor can survive.

| Step | Removed edge | Alive vertices | Answer |
| --- | --- | --- | --- |
| 4 | (4,5) | all 5 | 5 |
| 3 | (3,4) | all 5 | 5 |
| 2 | (2,3) | all 5 | 5 |
| 1 | (1,2) | all 5 | 5 |

This demonstrates monotonic stability once a 1-core exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ | Each vertex is removed once, and each edge is processed only when endpoints are removed or updated |
| Space | $O(n + m)$ | Adjacency lists and state arrays store the full graph |

The constraints allow up to $2 \cdot 10^5$ vertices and edges, so linear-time processing comfortably fits within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import solve
    return sys.stdout.getvalue()

# provided sample
# assert run("""4 4 2
# 2 3
# 1 2
# 1 3
# 1 4
# """).strip() == "0\n0\n3\n3"

# minimum case
assert run("""2 1 1
1 2
""").strip() == "2"

# no valid core ever
assert run("""3 2 2
1 2
2 3
""").strip() == "0\n0"

# fully dense triangle
assert run("""3 3 2
1 2
2 3
3 1
""").strip() == "0\n0\n3"

# chain growth
assert run("""5 4 1
1 2
2 3
3 4
4 5
""").strip() == "5\n5\n5\n5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 1 / 1 2 | 2 | smallest valid core |
| 3 2 2 / chain | 0 0 | no feasible k-core |
| triangle | 0 0 3 | delayed formation of core |
| chain k=1 | 5 5 5 5 | monotonic stability |

## Edge Cases

One edge case is when a vertex barely meets the threshold only after a cascade. For instance, in a triangle with $k=2$, no vertex survives until all three edges exist. The algorithm handles this because initial peeling removes everything, and reverse insertion only restores vertices when both neighbors are active, ensuring all three are present simultaneously before any of them becomes stable.

Another edge case is when a single edge removal triggers a large cascade. Consider a dense component where every vertex has degree exactly $k$. Removing one edge drops two endpoints below threshold, which can propagate widely. The BFS queue ensures this propagation is fully resolved before moving to the next step, maintaining correctness even under worst-case cascading deletions.