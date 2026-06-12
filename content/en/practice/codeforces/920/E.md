---
title: "CF 920E - Connected Components?"
description: "The graph in this problem is not given in the usual way. Instead of listing edges that exist, the input lists pairs of vertices that are explicitly disconnected. Every pair of vertices that does not appear in this list should be treated as having an edge between them."
date: "2026-06-13T02:50:10+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "dsu", "graphs"]
categories: ["algorithms"]
codeforces_contest: 920
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 37 (Rated for Div. 2)"
rating: 2100
weight: 920
solve_time_s: 176
verified: true
draft: false
---

[CF 920E - Connected Components?](https://codeforces.com/problemset/problem/920/E)

**Rating:** 2100  
**Tags:** data structures, dfs and similar, dsu, graphs  
**Solve time:** 2m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

The graph in this problem is not given in the usual way. Instead of listing edges that exist, the input lists pairs of vertices that are explicitly disconnected. Every pair of vertices that does not appear in this list should be treated as having an edge between them.

So the structure is effectively a dense graph where almost everything is connected, except for a set of forbidden connections. The task is to determine how this implicit graph splits into connected components and to report both how many such components exist and the size of each one.

A useful way to think about it is that every vertex starts as potentially connected to all others, and each forbidden pair removes exactly one edge from this complete graph. Connectivity is therefore determined by whether these missing edges are sufficient to separate vertices into groups.

The constraints are large enough that any solution that attempts to explicitly build the full graph is impossible. With up to 200000 vertices, a complete graph would have on the order of n² edges, which is far beyond memory and time limits. Even iterating over all pairs would be roughly 4 × 10¹⁰ operations, which is infeasible in a 2-second limit. This immediately rules out adjacency matrices and naive BFS/DFS over an explicitly constructed graph.

The subtle difficulty is that missing edges are sparse compared to the implicit full graph. The structure is closer to a complement graph problem than a standard graph traversal problem.

A few edge cases are easy to get wrong.

If there are no forbidden pairs, the graph is a complete graph and therefore has exactly one component of size n. A naive approach that assumes input edges are actual edges would incorrectly treat it as empty graph and produce n components of size 1.

If every possible pair were forbidden (which is impossible due to constraints but useful conceptually), the graph would have n isolated vertices. A solution that only tracks missing edges without handling isolation properly could fail here.

Another subtle case is when forbidden edges form a star-like pattern. For example, if all pairs involving vertex 1 are missing, vertex 1 becomes isolated, while the rest remain fully connected. A naive traversal that does not account for complement structure might incorrectly merge or split these groups.

## Approaches

The brute-force idea is to explicitly construct adjacency lists for the complement graph. For every pair of vertices, we check whether it is forbidden. If not, we add an edge. This immediately becomes impossible because iterating over all pairs is O(n²), and storing adjacency is also O(n²) in the worst case.

The key observation is that we never need to explicitly enumerate edges. Each vertex is initially connected to all others, so the only reason two vertices are not connected is if we have evidence from the forbidden list that they are disconnected. This suggests maintaining, for each vertex, the set of vertices it is not connected to.

When we perform a BFS or DFS from a vertex v, we want to move to all vertices that are still “available”, meaning all vertices except those explicitly forbidden and except those already visited. The challenge is to efficiently find these available vertices without scanning all n candidates.

This is where a set-based or ordered structure becomes essential. We maintain a set of unvisited vertices. When processing a vertex v, we iterate through the unvisited set, but skip those that are forbidden with v. The forbidden neighbors of v are stored in a hash set, so we can efficiently test membership. Every time we confirm a valid neighbor, we remove it from the unvisited set and continue.

The important efficiency trick is that each vertex is removed from the unvisited set exactly once. Even though we may check it multiple times, the total work across all BFS steps remains linear in n plus m.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (explicit graph) | O(n²) | O(n²) | Too slow |
| Optimal (set + BFS over complement) | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We build a representation of forbidden edges and then run a BFS over the implicit complement graph.

1. Store all forbidden pairs in a hash-based structure, grouping them by vertex. This allows constant-time checks of whether an edge is missing between two vertices. The goal is to quickly test adjacency in the complement graph.
2. Maintain a set of all unvisited vertices. This set represents the frontier of vertices not yet assigned to a component.
3. While the unvisited set is not empty, pick an arbitrary vertex v from it and start a BFS for a new component. The size of this BFS will determine the size of one connected component.
4. Initialize a queue with v and remove v from the unvisited set. This ensures we never process the same vertex twice.
5. While the queue is not empty, pop a vertex x. We want to find all vertices still unvisited that are connected to x in the complement graph. That means all vertices except x itself and except those explicitly forbidden with x.
6. Iterate through the unvisited set and identify vertices that are not in the forbidden list of x. Every such vertex is adjacent in the complement graph, so we add it to the queue and remove it from the unvisited set.
7. Continue until the queue is exhausted. At this point, we have discovered the full connected component of v.
8. Record the size of this component and repeat the process with another unvisited vertex.

The key reason this works efficiently is that every vertex is removed from the unvisited set exactly once, and every removal corresponds to a confirmed edge traversal in the complement graph.

### Why it works

At any moment, the unvisited set contains exactly the vertices that have not been assigned to any component yet. When processing a vertex x, every vertex still in the unvisited set is a potential neighbor in the complement graph. The only exceptions are those explicitly forbidden with x.

When we move a vertex y from unvisited to the queue, we are asserting that there is no forbidden edge (x, y), meaning an edge exists in the implicit graph. Since BFS explores all reachable vertices under this adjacency definition, every vertex reachable through allowed edges will eventually be discovered. Because we never revisit vertices, components remain disjoint, and every vertex is assigned exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict, deque

def solve():
    n, m = map(int, input().split())
    
    forbidden = defaultdict(set)
    for _ in range(m):
        x, y = map(int, input().split())
        forbidden[x].add(y)
        forbidden[y].add(x)
    
    unvisited = set(range(1, n + 1))
    components = []
    
    while unvisited:
        start = next(iter(unvisited))
        unvisited.remove(start)
        
        q = deque([start])
        size = 0
        
        while q:
            v = q.popleft()
            size += 1
            
            to_remove = []
            for u in unvisited:
                if u not in forbidden[v]:
                    q.append(u)
                    to_remove.append(u)
            
            for u in to_remove:
                unvisited.remove(u)
        
        components.append(size)
    
    components.sort()
    print(len(components))
    print(*components)

if __name__ == "__main__":
    solve()
```

The forbidden adjacency is stored as a dictionary of sets so membership checks are O(1). The unvisited set allows us to avoid revisiting vertices, and removing vertices lazily after iteration avoids modifying a set during iteration.

The BFS loop expands a component by scanning the current unvisited pool and selecting only valid neighbors. Although this looks like a nested loop, each vertex is removed from `unvisited` exactly once, so the total number of successful insertions into components is linear in n.

The sorting at the end is required because components must be printed in non-decreasing order.

## Worked Examples

### Example 1

Input:

```
5 5
1 2
3 4
3 2
4 2
2 5
```

We start with unvisited = {1,2,3,4,5}.

We pick 1 as the first start.

| Step | Current | Unvisited before | Forbidden check | Newly added | Component size |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | {1,2,3,4,5} | 2 not allowed? yes forbidden? no | 2,3,4,5 except forbidden | 4 |

Vertex 1 is connected to all except those explicitly forbidden. After BFS, we get one component of size 4.

Remaining unvisited = {2}.

Now start at 2.

| Step | Current | Unvisited before | Forbidden check | Newly added | Component size |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | {2} | none | none | 1 |

We end with components [4,1], sorted as [1,4].

This confirms that forbidden edges isolate a single vertex from the dense core.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) amortized | each vertex is removed once, each forbidden edge is stored once |
| Space | O(n + m) | storage for unvisited set and forbidden adjacency |

The structure avoids quadratic enumeration by never explicitly building edges. Even though inner loops scan sets, every vertex transition from unvisited to visited happens once, which keeps total work linear in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    from collections import defaultdict, deque

    n, m = map(int, input().split())
    forbidden = defaultdict(set)

    for _ in range(m):
        x, y = map(int, input().split())
        forbidden[x].add(y)
        forbidden[y].add(x)

    unvisited = set(range(1, n + 1))
    components = []

    while unvisited:
        start = next(iter(unvisited))
        unvisited.remove(start)
        q = deque([start])
        size = 0

        while q:
            v = q.popleft()
            size += 1
            to_remove = []
            for u in unvisited:
                if u not in forbidden[v]:
                    q.append(u)
                    to_remove.append(u)
            for u in to_remove:
                unvisited.remove(u)

        components.append(size)

    components.sort()
    out = str(len(components)) + "\n" + " ".join(map(str, components))
    return out

# provided sample
assert run("""5 5
1 2
3 4
3 2
4 2
2 5
""") == "2\n1 4"

# minimum size
assert run("""1 0
""") == "1\n1"

# fully connected (no forbidden edges)
assert run("""4 0
""") == "1\n4"

# star forbidden structure
assert run("""5 4
1 2
1 3
1 4
1 5
""") == "2\n1 4"

# split into pairs
assert run("""4 2
1 2
3 4
""") == "1\n4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 node | 1 component | minimum case |
| no forbidden edges | full connectivity | complete graph behavior |
| star forbidden | isolated vertex | asymmetric disconnection |
| pair splits | full connectivity via complement | indirect connectivity |

## Edge Cases

When there are no forbidden edges, the algorithm should immediately produce a single component containing all vertices. The unvisited set starts with all nodes, and the first BFS starting from any node will accept every other node because none are excluded by forbidden lists.

When a single vertex is forbidden with all others, that vertex becomes isolated while the remaining graph stays fully connected. The BFS starting from any non-isolated node will never include the isolated vertex because it is always excluded during adjacency checks.

When forbidden edges form disjoint constraints between pairs of vertices, the complement graph becomes fully connected. The BFS will merge everything into a single component because every vertex remains reachable through allowed edges.
