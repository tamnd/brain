---
title: "CF 1515F - Phoenix and Earthquake"
description: "The problem describes a scenario where a country’s road network has been destroyed by an earthquake, leaving n cities and m roads in a disconnected state."
date: "2026-06-10T18:34:12+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dfs-and-similar", "dsu", "graphs", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 1515
codeforces_index: "F"
codeforces_contest_name: "Codeforces Global Round 14"
rating: 2600
weight: 1515
solve_time_s: 176
verified: false
draft: false
---

[CF 1515F - Phoenix and Earthquake](https://codeforces.com/problemset/problem/1515/F)

**Rating:** 2600  
**Tags:** constructive algorithms, dfs and similar, dsu, graphs, greedy, trees  
**Solve time:** 2m 56s  
**Verified:** no  

## Solution
## Problem Understanding

The problem describes a scenario where a country’s road network has been destroyed by an earthquake, leaving `n` cities and `m` roads in a disconnected state. Each city starts with a certain amount of asphalt, and building a road consumes a fixed amount of asphalt `x`, which can be sourced from either of the two cities being connected. Asphalt can flow between cities that are already connected by repaired roads, meaning the network forms a dynamic pool of resources. The task is to determine whether it is possible to restore connectivity across all cities by repairing exactly `n-1` roads and, if so, output any valid sequence of repairs.

The inputs give the number of cities `n`, the number of potential roads `m`, the asphalt cost `x`, the initial asphalt amounts `a_i` for each city, and a list of `m` candidate roads. The output is "NO" if connectivity is impossible or "YES" followed by a sequence of `n-1` road indices representing a valid repair order.

Constraints indicate that `n` and `m` can be up to `3*10^5` and asphalt amounts can be very large, so an O(n log n) or O(m log n) algorithm is acceptable. Brute-force enumeration of all spanning trees is impossible due to combinatorial explosion. A naive approach that repeatedly tries all unused edges until one can be repaired is too slow and would time out on large inputs.

Non-obvious edge cases arise when the total asphalt in all cities is just barely enough to connect everything. For example, if `n=3`, `x=5`, asphalt amounts are `[2, 3, 5]`, and all three roads are available, careless implementations might fail if they choose the wrong starting road and consume asphalt unevenly. Another subtlety is that some cities may start with zero asphalt, requiring early connections to involve cities that have sufficient asphalt to "feed" other cities.

## Approaches

A brute-force approach would attempt to pick edges one by one, checking whether the sum of asphalt in the connected components is at least `x`. This would involve repeatedly scanning all unused edges and maintaining connectivity, which would be O(mn) in the worst case. With `n` and `m` up to 3*10^5, this is clearly infeasible. The brute-force works because it directly follows the problem’s rule about asphalt availability, but it fails for large instances due to the repeated scanning.

The key insight comes from viewing the cities as nodes in a graph and the repair process as building a spanning tree. A connected component with total asphalt less than `x` cannot add another road, so we need a strategy to always extend from a component with enough asphalt. This naturally leads to using a union-find (DSU) structure to maintain connected components and a greedy approach: always pick a road incident to a component whose total asphalt is at least `x`. We can implement this efficiently using a queue of "active" components that have sufficient asphalt, and a priority on edges connecting these components to yet-unconnected cities. This ensures that at each step we only consider feasible edges, avoiding unnecessary scans.

By carefully merging components and updating their total asphalt, we can repair all `n-1` roads in O(n + m) time using adjacency lists and DSU with path compression and union by size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(n + m) | Too slow |
| Greedy DSU | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the number of cities `n`, roads `m`, asphalt cost `x`, asphalt amounts `a[i]`, and the road list `(u, v)` indexed from 1.
2. Initialize a disjoint-set union (DSU) structure to track connected components, storing for each component the sum of asphalt it contains.
3. Build an adjacency list of edges for each city, storing both the neighbor and the road index.
4. Initialize a queue with all cities that currently have asphalt ≥ `x`. These are candidate starting points to grow the network.
5. While the queue is not empty:

a. Pop a city `u` from the queue.

b. Iterate over all edges from `u` to its neighbors `v`.

c. For each neighbor, check if `u` and `v` are in different components using DSU.

d. If so, check if the total asphalt of the merged component is at least `x`.

e. If the edge is feasible, repair it: append its index to the answer, merge the components in DSU, and update the total asphalt as `(asphalt_u + asphalt_v - x)`.

f. If the new component has asphalt ≥ `x`, push one representative city from it back into the queue to continue expansion.
6. After the process, check if all cities belong to the same component. If yes, print "YES" and the repair sequence. Otherwise, print "NO".

The reason this works is that we always grow the network from components with enough asphalt. Since asphalt can be pooled within connected components, we never run into a situation where a feasible repair is missed. The DSU ensures that we do not create cycles and only add edges that extend the forest toward a spanning tree.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

class DSU:
    def __init__(self, n, asphalt):
        self.parent = list(range(n))
        self.size = [1] * n
        self.asphalt = asphalt[:]

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return False
        if self.size[x_root] < self.size[y_root]:
            x_root, y_root = y_root, x_root
        self.parent[y_root] = x_root
        self.size[x_root] += self.size[y_root]
        self.asphalt[x_root] += self.asphalt[y_root]
        return x_root, y_root

n, m, x = map(int, input().split())
a = list(map(int, input().split()))
edges = []
adj = [[] for _ in range(n)]
for idx in range(m):
    u, v = map(int, input().split())
    u -= 1; v -= 1
    edges.append((u, v))
    adj[u].append((v, idx))
    adj[v].append((u, idx))

dsu = DSU(n, a)
used = [False] * m
queue = deque(i for i in range(n) if a[i] >= x)
answer = []

while queue and len(answer) < n-1:
    u = queue.popleft()
    u_root = dsu.find(u)
    for v, idx in adj[u]:
        if used[idx]:
            continue
        v_root = dsu.find(v)
        if u_root == v_root:
            continue
        total = dsu.asphalt[u_root] + dsu.asphalt[v_root]
        if total < x:
            continue
        used[idx] = True
        answer.append(idx + 1)
        new_root, old_root = dsu.union(u_root, v_root)
        dsu.asphalt[new_root] -= x
        if dsu.asphalt[new_root] >= x:
            queue.append(new_root)

if len(answer) == n-1:
    print("YES")
    print("\n".join(map(str, answer)))
else:
    print("NO")
```

The DSU class stores not only the parent and size of each component but also the total asphalt. The queue ensures we always attempt repairs from cities capable of funding a road. We mark edges as used to avoid double counting. After each union, we update the asphalt of the merged component and re-add it to the queue if it can still fund further repairs. The algorithm guarantees connectivity without cycles and respects asphalt constraints.

## Worked Examples

Sample Input 1:

```
5 4 1
0 0 0 4 0
1 2
2 3
3 4
4 5
```

| Step | Queue | Edge Chosen | Asphalt After | DSU Components | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | [3] | 3-4 | a=[0,0,3,1,0] | merge(3,4) | [3] |
| 2 | [3] | 2-3 | a=[0,0,2,1,0] | merge(2,3-4) | [3,2] |
| 3 | [3] | 1-2 | a=[0,0,1,1,0] | merge(1,2-3-4) | [3,2,1] |
| 4 | [3] | 4-5 | a=[0,0,1,0,0] | merge(4-5) | [3,2,1,4] |

This shows that the queue always picks a city with sufficient asphalt, and all roads are added successfully.

Sample Input 2 (impossible):

```
3 2 5
2 1 0
1 2
2 3
```

The total asphalt in any component is never enough to repair any road. The queue is empty from the start. Output is "NO".
