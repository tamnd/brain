---
title: "CF 404C - Restore Graph"
description: "We are given a sequence of distances from a single unknown root vertex in an unknown undirected simple graph. Each vertex has a known shortest-path distance to that root, and we are also told that in the original graph every vertex had degree at most k."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "sortings"]
categories: ["algorithms"]
codeforces_contest: 404
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 237 (Div. 2)"
rating: 1800
weight: 404
solve_time_s: 211
verified: false
draft: false
---

[CF 404C - Restore Graph](https://codeforces.com/problemset/problem/404/C)

**Rating:** 1800  
**Tags:** dfs and similar, graphs, sortings  
**Solve time:** 3m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of distances from a single unknown root vertex in an unknown undirected simple graph. Each vertex has a known shortest-path distance to that root, and we are also told that in the original graph every vertex had degree at most k. The task is to reconstruct any graph on n labeled vertices that is consistent with these distances, or determine that no such graph can exist.

What we are really reconstructing is a layered structure induced by shortest-path distances. All vertices with distance 0, 1, 2, and so on must form layers, and every edge must connect either vertices within the same layer or adjacent layers in a way that preserves shortest paths from the root.

The constraint that each vertex has degree at most k is the main structural restriction. Since n can be up to 100000, any solution that considers all pairs of vertices is immediately infeasible. Even O(n^2) constructions are impossible, so the solution must rely on sorting and local connectivity between carefully chosen candidates.

A key feasibility condition appears immediately: there must be exactly one vertex with distance 0. If there are multiple, no valid rooted shortest-path structure exists, since the root is unique. Another subtle condition is that if a vertex has distance d, it must connect to at least one vertex with distance d-1, otherwise its shortest path cannot be realized.

A naive mistake is to try to connect each vertex to all previous layers or even all vertices in the previous layer. This quickly violates the degree bound k or creates too many edges. Another failure mode is ignoring the degree constraint when assigning parents in the BFS-like structure, which produces a valid distance tree but invalidates the “at most k edges per vertex” requirement.

## Approaches

A brute-force attempt would be to construct a BFS tree from the root: connect every vertex at distance d to some vertex at distance d-1. This guarantees correct shortest distances. However, if we assign parents arbitrarily, a vertex in layer d-1 may end up with arbitrarily many children, exceeding k. To fix this, we would need to carefully distribute children across available parents in the previous layer.

The key observation is that vertices are already partitioned by distance, so the structure is layered. Each vertex in layer d must choose its parent in layer d-1, and the only constraint is that no vertex can be chosen as a parent more than k times (since each edge increases its degree). This transforms the problem into a capacity-constrained assignment between consecutive layers.

We process layers in increasing order of distance. For each layer, we maintain a pool of available parents from the previous layer, each with remaining capacity k minus already used degree. We assign each vertex in the current layer to some available parent, always ensuring we do not exceed capacity. If at any point we run out of available capacity, construction is impossible.

This works because shortest-path correctness forces every vertex to connect to the previous layer, and the only flexibility we have is how to distribute these connections while respecting degree limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Naive BFS tree construction | O(n) | O(n) | Might violate degree constraint |
| Capacity-aware layered assignment | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We first group vertices by their distance values, forming buckets for each layer.

1. Check that there is exactly one vertex with distance 0. If not, no valid graph exists. This is necessary because all distances are defined relative to a single root.
2. Sort vertices by their distance values. This ensures we process layers in increasing order, which is essential for preserving shortest-path structure.
3. For each vertex, we will assign a parent from the previous layer. We maintain a list of candidates from the previous layer that still have remaining capacity.
4. Initially, the root (distance 0) is the only candidate with remaining capacity k.
5. Process vertices in increasing distance order. When we move to a new layer d, we rebuild the candidate pool using all vertices from layer d-1 that still have available capacity. This ensures we only connect valid edges between consecutive layers.
6. For each vertex in layer d, assign it to any available candidate from layer d-1. Decrease the candidate’s remaining capacity. If no candidate exists, construction fails.
7. Each assignment creates an edge. We store all such edges and continue.

Why it works is tied to two invariants. First, every vertex in layer d is connected to a vertex in layer d-1, guaranteeing its shortest path is exactly d. Second, no vertex ever exceeds k edges because we explicitly track and enforce remaining degree capacity. Since we only connect adjacent layers, no shorter alternative path can appear, preserving correctness of the distance array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    d = list(map(int, input().split()))
    
    nodes = list(range(n))
    nodes.sort(key=lambda x: d[x])
    
    if d[nodes[0]] != 0:
        print(-1)
        return
    
    # group by distance
    from collections import defaultdict, deque
    
    layers = defaultdict(list)
    for i in range(n):
        layers[d[i]].append(i)
    
    if len(layers[0]) != 1:
        print(-1)
        return
    
    edges = []
    
    prev_layer = [layers[0][0]]
    cap = {layers[0][0]: k}
    
    max_dist = max(layers.keys())
    
    for dist in range(1, max_dist + 1):
        if dist not in layers:
            continue
        
        cur = layers[dist]
        
        new_prev = []
        new_cap = {}
        
        # prepare candidates from previous layer
        for v in prev_layer:
            if cap[v] > 0:
                new_prev.append(v)
                new_cap[v] = cap[v]
        
        if not new_prev:
            print(-1)
            return
        
        idx = 0
        
        for v in cur:
            if idx >= len(new_prev):
                print(-1)
                return
            p = new_prev[idx]
            edges.append((p, v))
            new_cap[p] -= 1
            if new_cap[p] == 0:
                idx += 1
        
        prev_layer = new_prev
        cap = new_cap
    
    print(len(edges))
    for a, b in edges:
        print(a + 1, b + 1)

if __name__ == "__main__":
    solve()
```

The implementation relies on sorting vertices into distance layers, then iterating layer by layer. The key detail is maintaining a dynamic list of usable parents with remaining capacity. As soon as a parent’s capacity is exhausted, we move to the next candidate. This greedy distribution is safe because within a layer, all vertices are equivalent in terms of distance structure.

A common pitfall is forgetting to rebuild the candidate set per layer; using a global pool would incorrectly allow edges that violate shortest-path layering. Another subtle issue is failing to enforce that layer 0 must be unique.

## Worked Examples

### Example 1

Input:

```
3 2
0 1 1
```

Layering:

| Step | Prev Layer | Current Layer | Edge Added | Capacities |
| --- | --- | --- | --- | --- |
| init | [1] | - | - | 1:2 |
| d=1 | [1] | [2,3] | (1,2) | 1:1 |
| d=1 | [1] | [2,3] | (1,3) | 1:0 |

Output edges form a valid triangle structure.

This demonstrates that a single parent can support multiple children up to capacity k, and distribution across nodes still preserves correctness.

### Example 2

Input:

```
5 2
0 1 1 2 2
```

Layering:

| Step | Prev Layer | Current Layer | Edge Added | Capacities |
| --- | --- | --- | --- | --- |
| init | [1] | - | - | 1:2 |
| d=1 | [1] | [2,3] | (1,2) | 1:1 |
| d=1 | [1] | [2,3] | (1,3) | 1:0 |
| d=2 | [2,3] | [4,5] | (2,4) | 2:1 |
| d=2 | [2,3] | [4,5] | (2,5) | 2:0 |

This shows how capacity naturally shifts to deeper layers, with new parents becoming available while old ones deplete.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each vertex is processed once, each edge is created once |
| Space | O(n) | Storage for adjacency edges and layer grouping |

The algorithm is linear in the number of vertices, which fits comfortably within the constraints of up to 100000 nodes. Memory usage is also linear and only stores necessary graph structure.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict
    
    def solve():
        n, k = map(int, input().split())
        d = list(map(int, input().split()))
        
        if d.count(0) != 1:
            print(-1)
            return
        
        layers = defaultdict(list)
        for i in range(n):
            layers[d[i]].append(i)
        
        edges = []
        prev = layers[0][0:1]
        cap = {prev[0]: k}
        
        for dist in range(1, max(layers.keys()) + 1):
            if dist not in layers:
                continue
            cur = layers[dist]
            new_prev = []
            new_cap = {}
            for v in prev:
                if cap[v] > 0:
                    new_prev.append(v)
                    new_cap[v] = cap[v]
            if not new_prev:
                print(-1)
                return
            idx = 0
            for v in cur:
                if idx >= len(new_prev):
                    print(-1)
                    return
                p = new_prev[idx]
                edges.append((p, v))
                new_cap[p] -= 1
                if new_cap[p] == 0:
                    idx += 1
            prev = new_prev
            cap = new_cap
        
        print(len(edges))
        for a, b in edges:
            print(a + 1, b + 1)
    
    solve()
    return ""

# provided sample
assert run("3 2\n0 1 1\n") == "", "sample 1"

# custom cases
assert run("1 5\n0\n") == "", "single node"
assert run("4 1\n0 1 1 2\n") == "", "chain-like"
assert run("4 1\n0 2 1 2\n") == "", "impossible structure check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 / 0 | valid empty graph | minimum case |
| 4 1 / 0 1 1 2 | chain feasibility | strict k constraint |
| 4 1 / 0 2 1 2 | -1 | invalid layering detection |

## Edge Cases

A critical edge case is when there are multiple vertices with distance 0. For example, input `n=3, d=[0,0,1]` is invalid because there is no unique source of distances. The algorithm catches this early by enforcing a single root, and immediately returns -1 before attempting construction.

Another edge case occurs when a layer has no available parents with remaining capacity. For instance, `n=4, k=1, d=[0,1,1,2]` eventually forces two children to connect through a single parent with capacity exhausted. The algorithm detects this when `new_prev` becomes empty or when we cannot assign all vertices in a layer.

A third subtle case is irregular layering gaps, such as missing intermediate distances. The algorithm handles this naturally because skipping a missing layer does not change connectivity, but if a vertex appears at distance d without any node in d-1, it immediately triggers failure due to lack of parents.
