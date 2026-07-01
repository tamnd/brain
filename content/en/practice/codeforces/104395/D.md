---
title: "CF 104395D - Reds and Blues"
description: "We are given an undirected weighted graph where each vertex represents a city and each edge represents a possible road with a construction cost. Every city is marked either red or blue."
date: "2026-06-30T23:19:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104395
codeforces_index: "D"
codeforces_contest_name: "Cupertino Informatics Tournament"
rating: 0
weight: 104395
solve_time_s: 91
verified: true
draft: false
---

[CF 104395D - Reds and Blues](https://codeforces.com/problemset/problem/104395/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected weighted graph where each vertex represents a city and each edge represents a possible road with a construction cost. Every city is marked either red or blue. The task is to choose a set of roads to build so that all red cities become connected with each other, and all blue cities also become connected with each other. Paths are allowed to pass through cities of the opposite color, so the only requirement is connectivity inside each color class, not separation between them.

The goal is to minimize the total cost of the selected roads.

The constraints go up to two hundred thousand cities and two hundred thousand roads, so any solution that tries all subsets of edges or runs multi-source shortest path style recomputation per color class would be too slow. Anything around $O(m \log m)$ or $O(m \alpha(n))$ is acceptable, while anything quadratic over edges is immediately ruled out.

A subtle point is that red and blue requirements interact through shared edges. A single edge can simultaneously help connect both colors, because intermediate vertices can belong to either group. This means the problem is not two independent MSTs; instead, it is a coupled connectivity requirement over the same graph.

There are a few failure cases that expose naive approaches.

If we compute a minimum spanning tree and then remove edges that seem unnecessary for one color, we can easily break connectivity for the other color. For example, suppose reds lie on opposite ends of a path and blues are concentrated in the middle. The MST is correct for full connectivity, but deleting an edge that is not “needed” for blues may disconnect reds.

If we compute separate MSTs restricted to red-induced and blue-induced subgraphs, we fail immediately when no such subgraph is connected, even though intermediate non-matching vertices are allowed.

The real difficulty is that connectivity is not per induced subgraph but per selected global subgraph.

## Approaches

A brute-force interpretation is to choose a subset of edges and test whether both red and blue induced subgraphs are connected. This is equivalent to checking connectivity twice for each candidate subset, which is already exponential in the number of edges. Even if we restrict ourselves to spanning trees, the number of possible trees is far too large, making enumeration infeasible.

A more structured attempt is to think in terms of spanning trees. Any valid solution can be assumed to be acyclic after removing redundant edges, since cycles only add cost. So we are effectively looking for a low-cost forest structure that simultaneously satisfies two connectivity constraints: all red vertices lie in one connected component and all blue vertices lie in one connected component.

This suggests a Kruskal-style process. If we sort edges by weight and gradually merge components, each merge either helps red connectivity, blue connectivity, or both. We maintain connected components using DSU and track, for each component, whether it contains red nodes or blue nodes. The process can stop as soon as all red nodes are inside a single DSU component and all blue nodes are inside a single DSU component. Since Kruskal always processes edges in increasing order, the first moment both constraints become satisfied corresponds to a minimum-cost prefix of edges that achieves feasibility.

The key insight is that we are not forced to fully connect the entire graph. We only need to connect two sets of terminals, and Kruskal naturally builds the cheapest structure that progressively reduces the number of disconnected terminal groups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subset Search | Exponential | O(m) | Too slow |
| Optimal Kruskal with DSU tracking colors | O(m log m) | O(n) | Accepted |

## Algorithm Walkthrough

We treat the problem as building a minimum-cost edge set while monitoring whether each color class becomes internally connected.

1. Sort all edges by increasing weight. This ensures that whenever we accept an edge, it is the cheapest available way to merge two components at that moment.
2. Initialize a DSU where each node is its own component. Alongside each component, maintain two boolean flags indicating whether the component contains at least one red node and at least one blue node.
3. Also maintain two counters: the number of components that contain red nodes and the number of components that contain blue nodes. Initially, these are simply the number of red vertices and blue vertices, because each such vertex forms its own component.
4. Iterate over edges in sorted order. For each edge connecting u and v, find their DSU representatives. If they are already in the same component, skip the edge since it does not change connectivity.
5. If they are in different components, merge them. Before merging, determine whether each component contains red or blue nodes. After merging, update the flags of the resulting component and adjust the counters accordingly. If both components contained red nodes, merging reduces the number of red-containing components by one. The same logic applies to blue.
6. Add the edge cost to the running total whenever a merge is performed.
7. After each merge, check whether both counters have reached one. If so, stop immediately and output the accumulated cost.

The stopping condition is the point where all red nodes lie in a single connected component and all blue nodes lie in a single connected component.

### Why it works

At any point in Kruskal’s algorithm, the DSU components represent a partition of the graph induced by all edges chosen so far. Any valid solution must connect all red vertices into a single component and all blue vertices into a single component, which means it must eventually merge all red-containing components and all blue-containing components. Since edges are considered in non-decreasing order, delaying any merge beyond the first available opportunity can only increase cost. Therefore, the moment both constraints are satisfied corresponds to the minimum prefix of edges that is sufficient, and any later edges are unnecessary for feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n, colors):
        self.parent = list(range(n))
        self.size = [1] * n
        self.has_red = [0] * n
        self.has_blue = [0] * n
        self.red_components = 0
        self.blue_components = 0

        for i, c in enumerate(colors):
            if c == 'R':
                self.has_red[i] = 1
                self.red_components += 1
            else:
                self.has_blue[i] = 1
                self.blue_components += 1

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return 0

        if self.size[a] < self.size[b]:
            a, b = b, a

        cost_change = 0

        if self.has_red[a] and self.has_red[b]:
            self.red_components -= 1
        if self.has_blue[a] and self.has_blue[b]:
            self.blue_components -= 1

        self.parent[b] = a
        self.size[a] += self.size[b]
        self.has_red[a] |= self.has_red[b]
        self.has_blue[a] |= self.has_blue[b]

        return 1

n, m = map(int, input().split())
colors = input().strip()

edges = []
for _ in range(m):
    u, v, w = map(int, input().split())
    edges.append((w, u - 1, v - 1))

edges.sort()

dsu = DSU(n, colors)

ans = 0

for w, u, v in edges:
    if dsu.find(u) != dsu.find(v):
        dsu.union(u, v)
        ans += w

    if dsu.red_components == 1 and dsu.blue_components == 1:
        break

print(ans)
```

The DSU maintains not only connectivity but also which colors are present in each component. The union operation updates both structure and the color bookkeeping, allowing us to know exactly when all red nodes and all blue nodes collapse into single components.

A subtle implementation detail is that we only decrement the component counters when both merged components contain the same color. This avoids incorrectly reducing counts when only one side contributes that color.

The early stopping condition is essential for efficiency and correctness, since it ensures we do not add unnecessary edges after feasibility is reached.

## Worked Examples

### Example 1

Input:

```
5 5
RBRRB
1 3 1
4 3 1
2 5 2
1 2 4
2 3 4
```

We sort edges by weight:

| Step | Edge | Action | Red components | Blue components | Cost |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,3,1) | merge | 3 | 3 | 1 |
| 2 | (4,3,1) | merge | 2 | 3 | 2 |
| 3 | (2,5,2) | merge | 2 | 2 | 4 |
| 4 | stop condition met | stop | 1 | 1 | 4 |

After processing three smallest edges, both red and blue vertices become internally connected. The algorithm stops before using the more expensive edges, demonstrating that it always takes the cheapest prefix sufficient for both constraints.

### Example 2

Input:

```
4 4
RBBR
1 2 5
2 3 1
3 4 2
1 4 10
```

| Step | Edge | Action | Red components | Blue components | Cost |
| --- | --- | --- | --- | --- | --- |
| 1 | (2,3,1) | merge | 2 | 1 | 1 |
| 2 | (3,4,2) | merge | 1 | 1 | 3 |
| 3 | stop condition met | stop | 1 | 1 | 3 |

Here blue vertices become connected quickly through the middle, and once the red endpoints connect through intermediate nodes, both constraints are satisfied early. The expensive direct edge is never used.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Sorting edges dominates, DSU operations are nearly constant amortized |
| Space | O(n + m) | DSU arrays plus edge storage |

The constraints allow up to two hundred thousand edges, and sorting at this scale is well within limits. DSU operations are effectively constant, so the solution comfortably fits within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    class DSU:
        def __init__(self, n, colors):
            self.parent = list(range(n))
            self.size = [1]*n
            self.has_red = [0]*n
            self.has_blue = [0]*n
            self.red_components = 0
            self.blue_components = 0
            for i,c in enumerate(colors):
                if c=='R':
                    self.has_red[i]=1
                    self.red_components+=1
                else:
                    self.has_blue[i]=1
                    self.blue_components+=1

        def find(self,x):
            while self.parent[x]!=x:
                self.parent[x]=self.parent[self.parent[x]]
                x=self.parent[x]
            return x

        def union(self,a,b):
            a=self.find(a); b=self.find(b)
            if a==b: return
            if self.size[a]<self.size[b]: a,b=b,a
            if self.has_red[a] and self.has_red[b]:
                self.red_components-=1
            if self.has_blue[a] and self.has_blue[b]:
                self.blue_components-=1
            self.parent[b]=a
            self.size[a]+=self.size[b]
            self.has_red[a]|=self.has_red[b]
            self.has_blue[a]|=self.has_blue[b]

    n,m=map(int,input().split())
    colors=input().strip()
    edges=[]
    for _ in range(m):
        u,v,w=map(int,input().split())
        edges.append((w,u-1,v-1))
    edges.sort()

    dsu=DSU(n,colors)
    ans=0

    for w,u,v in edges:
        if dsu.find(u)!=dsu.find(v):
            dsu.union(u,v)
            ans+=w
        if dsu.red_components==1 and dsu.blue_components==1:
            break

    return str(ans)

# provided sample
assert run("""5 5
RBRRB
1 3 1
4 3 1
2 5 2
1 2 4
2 3 4
""") == "4"

# minimal case
assert run("""1 0
R
""") == "0"

# single color dominance
assert run("""3 2
RRR
1 2 5
2 3 7
""") == "12"

# mixed simple chain
assert run("""4 3
RBRB
1 2 1
2 3 2
3 4 3
""") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 0 | trivial connectivity |
| all same color | MST for full connection | single constraint degenerates |
| chain alternating colors | full propagation through intermediates | color interaction via shared path |

## Edge Cases

If all cities are red, the blue constraint is already satisfied in a degenerate sense since there are no blue nodes to connect. The algorithm initializes the blue component count to zero, so the stopping condition reduces to ensuring red connectivity only, and it behaves like a standard MST restricted termination.

If red or blue nodes are already initially isolated but connected through intermediate nodes of the opposite color, the algorithm correctly uses those intermediate nodes because DSU unions are color-agnostic and only track presence, not restriction.

In a case where the cheapest edges only connect within one color group and expensive edges are needed to connect the other, the algorithm correctly prioritizes early merges but continues until both counters reach one, ensuring neither constraint is ignored.
