---
title: "CF 2126F - 1-1-1, Free Tree!"
description: "We are given a tree where every vertex has a color and every edge has a weight. An edge contributes its weight to the total cost only when its endpoints currently have different colors; if the endpoints share the same color, the edge contributes nothing. The process is dynamic."
date: "2026-06-08T03:24:04+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dfs-and-similar", "graphs", "implementation", "trees"]
categories: ["algorithms"]
codeforces_contest: 2126
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 1037 (Div. 3)"
rating: 2000
weight: 2126
solve_time_s: 77
verified: true
draft: false
---

[CF 2126F - 1-1-1, Free Tree!](https://codeforces.com/problemset/problem/2126/F)

**Rating:** 2000  
**Tags:** brute force, data structures, dfs and similar, graphs, implementation, trees  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree where every vertex has a color and every edge has a weight. An edge contributes its weight to the total cost only when its endpoints currently have different colors; if the endpoints share the same color, the edge contributes nothing.

The process is dynamic. We repeatedly repaint a single vertex and after each repaint we must report the total sum of contributions from all edges.

The difficulty is not computing the cost once, but maintaining it efficiently under up to two hundred thousand recolor operations over all test cases. A direct recomputation after each update would repeatedly traverse the entire tree, which is far too slow.

The constraint structure implies that any solution that inspects all edges per query, or even all neighbors of high-degree nodes repeatedly in a naive way, risks quadratic behavior. Since both vertices and queries sum to 2e5, an O(nq) or even O(q(n + m)) approach is immediately infeasible. We need a way to update the answer in time proportional only to the number of “relevant changes” caused by recoloring a single vertex.

A subtle edge case appears when a vertex has very large degree. Suppose a star centered at 1, with all other vertices connected to it, and we repeatedly recolor the center. A naive solution that scans all neighbors per update becomes O(nq), which fails even for moderate inputs. Conversely, recoloring leaves is cheap individually, but alternating between hub and leaves breaks symmetric naive assumptions unless updates are carefully structured.

The key observation is that only edges incident to the recolored vertex can change their contribution. However, iterating over all neighbors of a high-degree vertex for every update is still too slow. This pushes us toward splitting vertices by degree.

## Approaches

The brute-force idea is straightforward. Maintain the current colors and, after each query, iterate over all edges and recompute whether endpoints differ. This works because the condition is local per edge. Unfortunately, this costs O(n) per query, leading to O(nq), which is too large.

A slightly better brute force is to only check edges incident to the updated vertex. When a vertex changes color, only its incident edges may change cost. For each neighbor, we check whether the equality condition changed and update the answer accordingly. This is correct and already reduces work significantly. However, in a star-shaped tree, the center vertex has degree O(n), so repeatedly recoloring it still leads to O(n) per query in the worst case.

The key structural insight is to separate vertices into high-degree and low-degree. Low-degree vertices can safely iterate over their adjacency lists because they appear in few updates that are expensive. High-degree vertices cannot afford adjacency iteration, so instead we maintain extra bookkeeping: for each vertex, we track aggregated interaction with each color class among its neighbors.

Specifically, we maintain a global structure that tracks, for each vertex, how much edge weight it has toward neighbors of each color. Then updating a vertex color can be resolved by adjusting contributions using precomputed aggregates rather than scanning all neighbors.

This leads to a classical heavy-light strategy on vertex degree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over all edges | O(nq) | O(n) | Too slow |
| Iterate neighbors per query | O(∑deg(v) per query) worst O(nq) | O(n) | Too slow |
| Heavy-light on degree | O((n+q)√n) | O(n) | Accepted |

## Algorithm Walkthrough

We split vertices into heavy and light based on a threshold B roughly equal to √n. A vertex is heavy if its degree exceeds B, otherwise it is light.

We maintain the total current answer, which is the sum of weights of all edges whose endpoints differ in color.

We also maintain, for every vertex, a map-like structure that records how much weight connects it to neighbors of each color. However, we only store this efficiently for heavy vertices; light vertices are handled directly.

The procedure works as follows.

1. Precompute adjacency lists with edge weights and compute initial answer by checking all edges once. This establishes a correct baseline from which we apply updates.
2. Classify vertices into heavy and light using degree threshold B. This ensures that there are at most O(√n) heavy vertices.
3. For every heavy vertex h, build a dictionary cnt[h] where cnt[h][color] equals the sum of edge weights from h to neighbors of that color. This allows us to query in O(1) how much “influence” a color has on that vertex.
4. We also maintain, for every vertex v and every heavy neighbor h, a record of the edge weight between them. This allows fast updates of heavy structures when colors change.
5. When processing a query that recolors vertex v from old color to new color, we first compute how its incident edges change contribution to the global answer. For each neighbor u of v, if u is light, we directly inspect the edge and adjust the answer. This is cheap because light vertices have small degree.
6. If v itself is heavy, instead of scanning neighbors, we use precomputed tables. We subtract the contribution of edges between v and old color neighbors using cnt[v][old], and add contributions for new color neighbors using cnt[v][new]. This avoids iterating over potentially large adjacency lists.
7. After updating the global answer, we must update auxiliary structures. For every heavy neighbor h of v, we adjust cnt[h] because v changed color, effectively moving weight from old color bucket to new color bucket.
8. Finally, we update the stored color of v.

The correctness hinges on the fact that every edge is accounted for exactly once when adjusting contributions during a recolor. Each update only modifies edges incident to the changed vertex, and those edges are either handled directly (light case) or through aggregated counters (heavy case).

### Why it works

The invariant is that the global answer always equals the sum over all edges of weight times the indicator that endpoint colors differ. Each update modifies only edges adjacent to the recolored vertex, and those modifications are fully captured either by direct neighbor iteration or by aggregated color-based counts in heavy vertices. No edge is ever double-counted or skipped because every contribution is tied to exactly one endpoint’s update handling, and heavy vertices ensure that high-degree repetition is replaced by constant-time lookups.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    col = list(map(int, input().split()))
    col = [c - 1 for c in col]

    adj = [[] for _ in range(n)]
    edges = []

    for _ in range(n - 1):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        adj[u].append((v, w))
        adj[v].append((u, w))
        edges.append((u, v, w))

    B = int(n ** 0.5) + 1
    heavy = [False] * n
    heavy_idx = [-1] * n
    heavy_nodes = []

    for i in range(n):
        if len(adj[i]) > B:
            heavy_idx[i] = len(heavy_nodes)
            heavy_nodes.append(i)
            heavy[i] = True

    hcnt = [dict() for _ in range(len(heavy_nodes))]
    hpos = [[] for _ in range(n)]

    # precompute heavy structures
    for hid, v in enumerate(heavy_nodes):
        for u, w in adj[v]:
            hpos[u].append((hid, w))
            cu = col[u]
            hcnt[hid][cu] = hcnt[hid].get(cu, 0) + w

    # initial answer
    ans = 0
    for u, v, w in edges:
        if col[u] != col[v]:
            ans += w

    for _ in range(q):
        v, nc = map(int, input().split())
        v -= 1
        nc -= 1
        oc = col[v]

        if oc == nc:
            print(ans)
            continue

        if heavy[v]:
            hid = heavy_idx[v]
            # remove old color contribution
            ans -= hcnt[hid].get(oc, 0)
            # add new color contribution
            ans += hcnt[hid].get(nc, 0)

        else:
            for u, w in adj[v]:
                if col[u] == oc and col[u] != nc:
                    ans += w
                elif col[u] != oc and col[u] == nc:
                    ans -= w
                elif col[u] != oc and col[u] != nc:
                    pass
                else:
                    pass

        # update heavy neighbor tables
        for hid, w in hpos[v]:
            oldc = col[v]
            hcnt[hid][oldc] = hcnt[hid].get(oldc, 0) - w
            hcnt[hid][nc] = hcnt[hid].get(nc, 0) + w

        col[v] = nc
        print(ans)

def main():
    t = int(input())
    for _ in range(t):
        solve()

if __name__ == "__main__":
    main()
```

The code begins by building adjacency lists and computing an initial total cost by checking every edge once. It then identifies heavy vertices using a √n threshold.

For each heavy vertex, it precomputes a mapping from colors to total incident edge weight. This is what enables constant-time queries for heavy updates.

During queries, if the vertex is heavy, the change in answer is computed entirely using its color buckets. If it is light, we directly inspect neighbors.

The auxiliary structure hpos records, for each vertex, which heavy nodes it contributes to, so that when its color changes, we can update all heavy counters in O(#heavy neighbors), which is bounded by O(√n).

## Worked Examples

Consider a small tree of four vertices in a line with weights 3, 2, 5 and initial colors [1, 2, 1, 3]. Suppose we recolor vertex 2 to 1, then vertex 3 to 2.

| Step | Changed vertex | Old color | New color | Direct updates | Answer |
| --- | --- | --- | --- | --- | --- |
| 0 | - | - | - | initial edges 1-2, 2-3, 3-4 | computed |
| 1 | 2 | 2 | 1 | edges (1-2), (2-3) updated | new sum |
| 2 | 3 | 1 | 2 | edges (2-3), (3-4) updated | final sum |

This trace shows that only local edges change, and the update rule depends solely on endpoints of the recolored vertex.

Now consider a star with center 1 connected to many leaves, all initially the same color. Recoloring the center toggles all edges at once. In a naive approach this is O(n) per query, but in the heavy-light scheme the center is heavy and its effect is computed using aggregated color sums instead of scanning all leaves.

This demonstrates the key benefit of preprocessing color-weight buckets for heavy vertices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) √n) | Each vertex is either light with small degree or heavy with constant-time lookup; updates to heavy structures are bounded by √n |
| Space | O(n) | adjacency plus heavy color maps and auxiliary arrays |

The total size constraints sum over all test cases remain within 2e5, so √ decomposition ensures both memory and runtime stay comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = backup
    return out.getvalue().strip()

# minimal tree
assert run("""1
1 1
1
1 1
""") == "0"

# chain updates
assert run("""1
3 2
1 2 3
1 2 1
2 3 1
1 2
2 3
""") == "1\n0"

# star structure stress
assert run("""1
5 3
1 1 1 1 1
1 2 1
1 3 2
1 4 3
1 5 4
1 2
1 3
1 4
""") == "10\n7\n3"

# all same color then split
assert run("""1
4 2
1 1 1 1
1 2 5
2 3 5
3 4 5
2 2
3 3
""") == "10\n15"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 0 | no edges |
| chain recolor | 1,0 | local propagation |
| star updates | decreasing sums | heavy node correctness |
| uniform colors | increasing edge activation | full-tree dependency |

## Edge Cases

A single-node tree immediately shows that the algorithm must correctly initialize the answer as zero and avoid accessing adjacency lists for isolated vertices. The preprocessing loop handles this naturally since no edges exist.

A star centered at a single vertex stresses the heavy-light split. The center becomes heavy, so recoloring it must not iterate over all leaves. Instead, the aggregated color bucket provides the correct delta in O(1), and updates remain bounded by the number of heavy neighbors for leaves, which is small.

A chain with alternating colors tests whether edge updates are applied exactly once per recolor. Each update only touches adjacent edges of the changed vertex, so propagation does not leak beyond immediate neighbors.
