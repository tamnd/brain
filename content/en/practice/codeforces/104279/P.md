---
title: "CF 104279P - \u4e09\u7ef4\u6a21\u578b"
description: "We are given a collection of triangular faces, each triangle described only by three integer vertex IDs. These IDs do not represent geometry in any meaningful way beyond identity."
date: "2026-07-01T21:14:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104279
codeforces_index: "P"
codeforces_contest_name: "21st UESTC Programming Contest - Preliminary"
rating: 0
weight: 104279
solve_time_s: 52
verified: true
draft: false
---

[CF 104279P - \u4e09\u7ef4\u6a21\u578b](https://codeforces.com/problemset/problem/104279/P)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of triangular faces, each triangle described only by three integer vertex IDs. These IDs do not represent geometry in any meaningful way beyond identity. Two triangles are considered adjacent if they share an entire edge, meaning they have exactly two vertex IDs in common. A “3D model” in this problem is simply a connected component under this adjacency relation on triangles.

The task is to group all triangles into such connected components, where connectivity is defined through shared edges between triangles, and then report how many components exist and the size of each component.

The important abstraction shift is that we are not working with geometry at all. We are working with a graph where nodes are triangles, and edges exist when two triangles share a pair of vertices.

The constraints are tight: the total number of triangles across all test cases is at most 100000. This immediately rules out any quadratic comparison between triangles. A naive pairwise check would require comparing every pair of triangles, which in the worst case is about 10^10 operations, far beyond the limit. Any valid solution must ensure that each triangle is processed only a small constant number of times, ideally logarithmic or amortized constant per operation.

A subtle pitfall is thinking that adjacency depends on full vertex overlap or geometric coincidence. It does not. Only exact shared pairs matter. Another subtle issue is assuming that shared vertices imply connectivity. That is false: triangles must share an edge, not just a single vertex. For example, triangles (1,2,3) and (1,4,5) share a vertex but are not connected.

Finally, the graph is not necessarily planar or well-structured. A single edge can belong to many triangles, forming a dense local cluster. Any solution relying on geometric intuition will fail.

## Approaches

A direct approach is to compare every pair of triangles and check whether they share two vertices. This is correct because it directly implements the definition of connectivity. However, checking adjacency for all pairs leads to O(n^2) comparisons, and each comparison requires checking set intersections or sorting comparisons, making it even slower in practice. With n up to 100000, this is impossible.

The key insight is to invert the perspective. Instead of asking whether two triangles are connected, we ask which triangles can be connected through a shared edge. Every triangle contains exactly three edges, and each edge can be represented as an unordered pair of vertex IDs. If two triangles share an edge, they share the same unordered pair representation of that edge.

So instead of comparing triangles against each other, we map edges to the triangles that contain them. Every edge becomes a key, and all triangles sharing that key are connected through that edge. This allows us to build the connectivity graph implicitly.

Once we have this mapping, we can use a disjoint set union structure to merge triangles that share any edge. Each edge group connects all triangles containing it. After processing all edges, each DSU component corresponds exactly to one connected 3D model.

This reduces the problem from pairwise comparison of triangles to linear processing of triangle edges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Edge hashing + DSU | O(n α(n)) | O(n) | Accepted |

## Algorithm Walkthrough

We treat each triangle as a node in a disjoint set union structure. The goal is to merge nodes whenever they share an edge.

1. Initialize a DSU structure with n elements, one per triangle. Each triangle starts in its own component because initially no connections are known.
2. For each triangle, enumerate its three edges. Each edge is represented as a sorted pair (min(u, v), max(u, v)). Sorting is necessary because edges are undirected, and (u, v) must be treated the same as (v, u).
3. Maintain a hash map from edge to the first triangle index that has been seen with this edge. When we encounter an edge for the first time, we store its triangle index.
4. When we encounter the same edge again in another triangle, we union the current triangle with the previously stored triangle. This ensures that all triangles sharing this edge end up in the same DSU component.
5. After processing all triangles and edges, iterate over all triangles and find their DSU root. Count the size of each root component.
6. Collect all component sizes and sort them in increasing order for output.

The crucial idea is that every shared edge induces a transitive connection between all triangles containing it. By unioning through the first occurrence, we effectively build a star structure inside each edge-group, which is sufficient for connectivity.

### Why it works

Each triangle belongs to a component defined by reachability through shared edges. Every time two triangles share an edge, they are directly connected and must belong to the same component. DSU guarantees that once two nodes are unioned, they remain in the same set, preserving this connectivity relation.

Conversely, if two triangles are connected through a chain of shared edges, the DSU will merge them step by step along that chain. Therefore, each final DSU set corresponds exactly to a maximal set of triangles connected through edge-sharing, which matches the definition of a 3D model in the problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]

def solve():
    T = int(input())
    for _ in range(T):
        n = int(input())
        dsu = DSU(n)
        edge_map = {}

        for i in range(n):
            a, b, c = map(int, input().split())

            e1 = (a, b) if a < b else (b, a)
            e2 = (a, c) if a < c else (c, a)
            e3 = (b, c) if b < c else (c, b)

            for e in (e1, e2, e3):
                if e in edge_map:
                    dsu.union(i, edge_map[e])
                else:
                    edge_map[e] = i

        comp = {}
        for i in range(n):
            r = dsu.find(i)
            comp[r] = comp.get(r, 0) + 1

        sizes = sorted(comp.values())
        print(len(sizes))
        print(*sizes)

if __name__ == "__main__":
    solve()
```

The DSU is used to maintain connected components of triangles. The union operation only happens when we detect a repeated edge, which ensures correctness without redundant merges.

Each triangle generates exactly three edges, and each edge is normalized by sorting its endpoints so that identical edges map to the same key. The hash map stores only one representative triangle per edge, which is enough because connectivity is transitive.

The final loop compresses DSU representatives and counts component sizes. Sorting is required by output specification.

## Worked Examples

### Example 1

Input:

```
4
1001 1002 1003
1001 1002 1004
1001 1003 1004
1002 1003 1004
```

We process triangles one by one.

| Triangle | Edge processed | Map state | DSU merges |
| --- | --- | --- | --- |
| 0 | (1001,1002), (1001,1003), (1002,1003) | edges stored → 0 | none |
| 1 | (1001,1002) triggers match | edge (1001,1002): 0 | union(1,0) |
| 1 | others stored | updated |  |
| 2 | (1001,1003) matches 0 | union(2,0) |  |
| 3 | all edges match existing | union with 0 |  |

All triangles merge into one component. Output is one component of size 4.

This confirms that a fully connected tetrahedral structure collapses into a single DSU set.

### Example 2

Input:

```
6
1 2 3
1 2 4
1 5 6
7 8 9
7 8 10
11 12 13
```

| Triangle | Key merges |
| --- | --- |
| 0,1 | share edge (1,2) → merge |
| 2 | isolated |
| 3,4 | share edge (7,8) → merge |
| 5 | isolated |

Final groups are sizes 2, 2, 1, 1.

This shows that connectivity is strictly edge-based, not vertex-based, and multiple independent clusters coexist.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n α(n)) | Each triangle contributes three edge operations, each causing at most one DSU union with near-constant amortized cost |
| Space | O(n) | DSU arrays plus hash map storing at most 3n edges |

The total number of triangles across all test cases is at most 100000, so linear or near-linear behavior is sufficient. The DSU-based solution stays comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict

    class DSU:
        def __init__(self, n):
            self.p = list(range(n))
            self.s = [1]*n
        def f(self,x):
            while self.p[x]!=x:
                self.p[x]=self.p[self.p[x]]
                x=self.p[x]
            return x
        def u(self,a,b):
            a,b=self.f(a),self.f(b)
            if a==b:return
            if self.s[a]<self.s[b]:a,b=b,a
            self.p[b]=a
            self.s[a]+=self.s[b]

    T = int(input())
    out = []
    for _ in range(T):
        n = int(input())
        dsu = DSU(n)
        mp = {}
        for i in range(n):
            a,b,c = map(int,input().split())
            for e in [(min(a,b),max(a,b)),(min(a,c),max(a,c)),(min(b,c),max(b,c))]:
                if e in mp:
                    dsu.u(i, mp[e])
                else:
                    mp[e]=i
        comp = {}
        for i in range(n):
            r = dsu.f(i)
            comp[r]=comp.get(r,0)+1
        sizes = sorted(comp.values())
        out.append(str(len(sizes)))
        out.append(" ".join(map(str,sizes)))
    return "\n".join(out)

# custom tests

assert run("""1
1
1 2 3
""") == "1\n1"

assert run("""1
2
1 2 3
4 5 6
""") == "2\n1 1"

assert run("""1
3
1 2 3
1 2 4
4 2 3
""") == "1\n3"

assert run("""1
4
1 2 3
1 2 4
5 6 7
5 6 8
""") == "2\n2 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 triangle | 1 component | minimum case |
| 2 disjoint triangles | 2 components | disconnected graph |
| shared edge chain | 1 component | transitive merging |
| two separate pairs | 2 components | multiple clusters |

## Edge Cases

A subtle case is when connectivity forms through a chain of shared edges rather than direct sharing. Consider:

```
1 2 3
1 2 4
4 2 3
```

Triangle 0 connects to 1 via edge (1,2). Triangle 1 connects to 2 via edge (2,4). Even though triangle 0 and 2 do not share an edge directly, they become connected through triangle 1. The DSU correctly merges them step by step, producing a single component.

Another edge case is when many triangles share the same edge. For example:

```
1 2 3
1 2 4
1 2 5
1 2 6
```

All triangles share edge (1,2), so they must all be in one component. The hash map stores the first triangle, and every subsequent triangle unions into it, building a single connected set.

A final edge case is complete isolation, where no edges repeat. In that case, every triangle remains its own DSU set, and the output is n components each of size 1.
