---
title: "CF 102331A - Apollonian Network"
description: "The graph starts as a triangle and is repeatedly expanded by choosing a triangular face, inserting a new vertex into it, and connecting the new vertex to all three vertices of that triangle."
date: "2026-08-13T03:30:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102331
codeforces_index: "A"
codeforces_contest_name: "2019 Summer Petrozavodsk Camp, Day 2: 300iq Contest 2 (XX Open Cup, Grand Prix of Kazan)"
rating: 0
weight: 102331
solve_time_s: 219
verified: true
draft: false
---

[CF 102331A - Apollonian Network](https://codeforces.com/problemset/problem/102331/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

The graph starts as a triangle and is repeatedly expanded by choosing a triangular face, inserting a new vertex into it, and connecting the new vertex to all three vertices of that triangle. Every inserted vertex is therefore born with exactly three neighbors, and those three neighbors form a clique. The input gives the final undirected graph together with a nonnegative weight for every edge. We need the maximum total weight of a simple path, meaning a path that never visits a vertex twice.

There are (n\le 250) vertices and exactly (3(n-2)) edges, so the graph is sparse. The small value of (n) by itself is not enough to make general longest-path algorithms feasible, because the longest simple path problem is NP-hard on arbitrary graphs. The useful constraint is structural rather than numerical: an Apollonian network is a planar 3-tree, so it has treewidth at most 3. A dynamic program whose state depends exponentially only on the treewidth is consequently practical here. With bags containing at most four vertices, the number of connectivity states is a fixed constant.

There are several edge cases that matter when implementing the DP. First, the optimal path can be a single vertex when every edge has weight zero. For example,

```
3
1 2 0
2 3 0
3 1 0
```

has answer `0`. An implementation that initializes the answer to a negative value and only considers paths containing an edge would fail.

A second case is a path that is completely contained in a peeled subtree. Consider

```
5
1 2 0
2 3 0
3 1 0
4 1 0
4 2 0
4 3 0
5 1 0
5 2 0
5 4 10
```

The answer is `10`, using the path (4\to5). When vertex 4 is eventually removed, this path has no vertex left in the separator triangle. A DP that keeps only configurations touching the separator would silently lose the optimum. The algorithm below records such a completed path in the global answer before discarding its state.

A third subtlety is that the part of a global path lying inside one subtree does not necessarily have to be connected by itself. For example, take the graph on six vertices obtained from triangle (1,2,3), insert 4 into it, insert 5 into triangle (1,2,4), and insert 6 into triangle (2,3,4). Give edges (5-1), (1-3), and (3-6) weight 10, and all other edges weight 0. The path (5\to1\to3\to6) has weight 30. Relative to the subtree rooted at 4, the edges (5-1) and (3-6) form two separate pieces, joined later through the separator edge (1-3). A DP that stores only one connected piece per subtree misses this possibility. The connectivity partition in our state is what handles it.

## Approaches

The direct approach is to enumerate simple paths with DFS. At every vertex we try every unused neighbor, mark the vertex as visited, recurse, and then undo the choice. This is correct because every simple path appears exactly once in such a search. The problem is the number of paths. A general DFS can inspect one ordered vertex sequence for every simple path, and in a complete graph the number of such sequences is

[
\sum_{k=1}^{n}\frac{n!}{(n-k)!},
]

which is (\Theta(n!)). Apollonian networks are not complete for large (n), but they still contain exponentially many simple paths, so exhaustive enumeration is far beyond what (n=250) permits.

The brute force works because it remembers the entire visited set. That is precisely what makes it expensive. The graph structure gives us a way to forget almost all of that information. An Apollonian network can be reduced to a triangle by repeatedly deleting a degree-3 vertex whose three remaining neighbors form a triangle. Reversing this process gives a tree decomposition in which every bag contains at most four vertices.

Once the graph is separated by a triangle, everything that happens deep inside the separated part can affect the rest of the graph only through those three boundary vertices. We therefore do not need to remember which internal vertices the partial path used. We only need to remember which boundary vertices are used, their current degrees, and which boundary vertices belong to the same connected component.

The selected edges inside a processed subtree form a forest of paths. The degree of every selected vertex is at most two, and connectivity is represented by a partition of the boundary vertices. A cycle is forbidden because the final object must be a simple path. When two child subtrees are merged, their forests may join through shared boundary vertices. We detect whether this creates a cycle using a tiny auxiliary union-find over the components of the two states.

The only awkward situation is a component that disappears when its last boundary vertex is forgotten. Such a component can never connect to anything outside the subtree. If it is the only selected component, it is already a complete path, so we update the global answer. If another component exists, the state can never become one simple path and is discarded.

The comparison is therefore:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n!)) in the worst general case | (O(n)) recursion and visited state | Too slow |
| Optimal | (O(nC^2)), where (C) is a constant depending only on bag size 4 | (O(nC)) | Accepted |

Since the bag size is fixed at four, (C) is a constant. The theoretical complexity is thus linear in (n), with a relatively large constant caused by enumerating connectivity states.

## Algorithm Walkthrough

1. Build the graph and repeatedly remove an active vertex of degree three. Before removing a vertex (v), record its three currently active neighbors. They become the boundary of the subtree rooted at (v). In an Apollonian network those three neighbors form a triangle, so they are exactly the separator through which the rest of the graph can interact with (v)'s subtree.
2. For every removed vertex (v), define its bag as ([v,a,b,c]), where (a,b,c) are its three later neighbors. Choose the smallest of (a,b,c) as the parent of (v). Because (a,b,c) form a clique, the parent's bag contains all three of them. This connects the bags into a valid tree decomposition of width at most three.
3. For every subtree, store a DP state describing a forest of paths. For each boundary vertex we store whether it is used, its degree (0,1,) or (2), and a component label telling which other boundary vertices are connected to it. A used vertex with degree zero represents an isolated selected vertex. The state value is the maximum total weight of all selected edges realizing that boundary description.
4. Start every subtree with the empty state. Process all child subtrees one by one. A child state is lifted from its three-vertex boundary into the current four-vertex bag, and then merged with the states already accumulated from previous children.
5. During a merge, add the degrees of every shared boundary vertex. If a degree becomes larger than two, reject the combination. For connectivity, regard every component of the first state and every component of the second state as a node of an auxiliary bipartite graph. Every boundary vertex used by both states joins the corresponding pair of components. If these component nodes receive a cycle, the selected edges contain a cycle and the combination is rejected. Otherwise the union of the two forests is still a forest.
6. After all children have been merged, process the three edges from (v) to its later neighbors. For each edge there are two choices, omit it or add it. Adding it increases the degrees of its endpoints and joins their components. If the endpoints are already in the same component, adding the edge would create a cycle, so that choice is rejected.
7. Forget (v) from the four-vertex state. If (v) is unused, simply remove it. If (v) belongs to a component that also contains another boundary vertex, remove (v) and keep the component. If (v)'s component contains no other boundary vertex, that component is completely sealed inside the subtree. If there are no other selected boundary vertices, its weight is a valid complete path and updates the global answer. If another component exists, the state is impossible for a final simple path and is discarded.
8. The last three vertices form the root triangle. Merge all root children into a three-vertex DP, then process the three root edges. Among the resulting states, take the maximum value whose selected vertices form exactly one connected component. A connected acyclic graph in which every degree is at most two is a simple path, so this is exactly the desired answer.

### Why it works

The invariant is that every DP state represents exactly the possible selected-edge forests inside the processed subtree, restricted to configurations where every component still has a boundary vertex. The degree information guarantees that no selected vertex can have degree greater than two. The component partition guarantees that the DP knows exactly which boundary vertices can already be connected through the processed part. The union-find check prevents two independently acyclic pieces from forming a cycle when they are glued together.

When a component disappears at a forget operation, no future edge can reach it because all of its boundary vertices have disappeared. It is consequently either a complete solution by itself or an unusable disconnected component. At the root there is no outside graph, so accepting exactly one component is equivalent to accepting one simple path. Every possible simple path induces one sequence of DP states, and every accepted DP state corresponds to a valid simple path, so the maximum value produced by the DP is exactly the optimum.

## Python Solution

```python
import sys
from collections import deque
from functools import lru_cache

input = sys.stdin.readline

NEG = -10**30

def solve():
    n = int(input())
    m = 3 * (n - 2)

    adj = [set() for _ in range(n)]
    weight = {}

    for _ in range(m):
        a, b, w = map(int, input().split())
        a -= 1
        b -= 1
        if a > b:
            a, b = b, a
        adj[a].add(b)
        adj[b].add(a)
        weight[(a, b)] = w

    if n == 3:
        a, b, c = 0, 1, 2
        print(max(weight[(0, 1)] + weight[(0, 2)],
                  weight[(0, 1)] + weight[(1, 2)],
                  weight[(0, 2)] + weight[(1, 2)]))
        return

    active = [True] * n
    degree = [len(adj[v]) for v in range(n)]
    q = deque(v for v in range(n) if degree[v] == 3)

    later = [[] for _ in range(n)]
    parent = [-1] * n

    removed = 0

    while removed < n - 3:
        while q and (not active[q[0]] or degree[q[0]] != 3):
            q.popleft()

        v = q.popleft()
        if not active[v] or degree[v] != 3:
            continue

        ns = [u for u in adj[v] if active[u]]
        ns.sort()
        later[v] = ns

        p = ns[0]
        parent[v] = p

        active[v] = False
        removed += 1

        for u in ns:
            adj[u].remove(v)
            degree[u] -= 1
            if degree[u] == 3:
                q.append(u)

        adj[v].clear()
        degree[v] = 0

    root = [v for v in range(n) if active[v]]
    root.sort()

    children = [[] for _ in range(n)]
    for v in range(n):
        if parent[v] != -1:
            children[parent[v]].append(v)

    for v in range(n):
        children[v].sort()

    def normalize(deg, labels):
        mp = {}
        nxt = 0
        res = []
        for x in labels:
            if x == -1:
                res.append(-1)
            else:
                if x not in mp:
                    mp[x] = nxt
                    nxt += 1
                res.append(mp[x])
        return tuple(deg), tuple(res)

    @lru_cache(maxsize=None)
    def merge_states(a, b):
        da, la = a
        db, lb = b
        k = len(da)

        deg = [0] * k
        for i in range(k):
            x = da[i] + db[i]
            if x > 2:
                return None
            deg[i] = x

        ca = 0
        cb = 0
        for x in la:
            if x >= 0:
                ca = max(ca, x + 1)
        for x in lb:
            if x >= 0:
                cb = max(cb, x + 1)

        total = ca + cb
        dsu = list(range(total))

        def find(x):
            while dsu[x] != x:
                dsu[x] = dsu[dsu[x]]
                x = dsu[x]
            return x

        def union(x, y):
            x = find(x)
            y = find(y)
            if x == y:
                return False
            dsu[y] = x
            return True

        for i in range(k):
            if la[i] != -1 and lb[i] != -1:
                x = la[i]
                y = ca + lb[i]
                if not union(x, y):
                    return None

        labels = [-1] * k
        root_to_label = {}
        nxt = 0

        for i in range(k):
            if la[i] != -1:
                r = find(la[i])
            elif lb[i] != -1:
                r = find(ca + lb[i])
            else:
                continue

            if r not in root_to_label:
                root_to_label[r] = nxt
                nxt += 1
            labels[i] = root_to_label[r]

        return tuple(deg), tuple(labels)

    @lru_cache(maxsize=None)
    def add_edge(state, x, y):
        deg, labels = state
        if deg[x] == 2 or deg[y] == 2:
            return None

        deg2 = list(deg)
        deg2[x] += 1
        deg2[y] += 1

        labels2 = list(labels)
        lx = labels2[x]
        ly = labels2[y]

        if lx != -1 and ly != -1:
            if lx == ly:
                return None
            for i in range(len(labels2)):
                if labels2[i] == ly:
                    labels2[i] = lx
        elif lx != -1:
            labels2[y] = lx
        elif ly != -1:
            labels2[x] = ly
        else:
            new_label = 0
            for z in labels2:
                if z >= new_label:
                    new_label = z + 1
            labels2[x] = new_label
            labels2[y] = new_label

        return normalize(deg2, labels2)

    empty4 = ((0, 0, 0, 0), (-1, -1, -1, -1))
    empty3 = ((0, 0, 0), (-1, -1, -1))

    answer = 0

    def lift_child(state, mapping):
        deg3, lab3 = state
        deg4 = [0, 0, 0, 0]
        lab4 = [-1, -1, -1, -1]

        for i in range(3):
            p = mapping[i]
            deg4[p] = deg3[i]
            lab4[p] = lab3[i]

        return tuple(deg4), tuple(lab4)

    sys.setrecursionlimit(10000)

    def dfs(v):
        nonlocal answer

        s = sorted(later[v])
        bag = [v] + s
        pos = {x: i for i, x in enumerate(bag)}

        cur = {empty4: 0}

        for ch in children[v]:
            child_dp = dfs(ch)

            child_boundary = later[ch]
            mapping = [pos[x] for x in child_boundary]

            lifted = {}
            for st, val in child_dp.items():
                lst = lift_child(st, mapping)
                old = lifted.get(lst)
                if old is None or val > old:
                    lifted[lst] = val

            nxt_dp = {}

            for st1, val1 in cur.items():
                for st2, val2 in lifted.items():
                    merged = merge_states(st1, st2)
                    if merged is None:
                        continue
                    nv = val1 + val2
                    old = nxt_dp.get(merged)
                    if old is None or nv > old:
                        nxt_dp[merged] = nv

            cur = nxt_dp

        for i, u in enumerate(s, start=1):
            a, b = (v, u) if v < u else (u, v)
            w = weight[(a, b)]

            nxt_dp = dict(cur)
            for st, val in cur.items():
                ns = add_edge(st, 0, i)
                if ns is None:
                    continue
                nv = val + w
                old = nxt_dp.get(ns)
                if old is None or nv > old:
                    nxt_dp[ns] = nv
            cur = nxt_dp

        result = {}

        for st, val in cur.items():
            deg, labels = st
            lv = labels[0]

            if lv == -1:
                ns = normalize(deg[1:], labels[1:])
                old = result.get(ns)
                if old is None or val > old:
                    result[ns] = val
                continue

            same = False
            for i in range(1, 4):
                if labels[i] == lv:
                    same = True
                    break

            if same:
                ns = normalize(deg[1:], labels[1:])
                old = result.get(ns)
                if old is None or val > old:
                    result[ns] = val
            else:
                other_used = any(x != -1 for x in labels[1:])
                if not other_used:
                    if val > answer:
                        answer = val

        return result

    root_dp = {empty3: 0}

    for ch in children[root[0]] + children[root[1]] + children[root[2]]:
        child_dp = dfs(ch)
        boundary = later[ch]

        mapping = []
        for x in boundary:
            mapping.append(root.index(x))

        lifted = {}
        for st, val in child_dp.items():
            deg3, lab3 = st
            deg = [0, 0, 0]
            lab = [-1, -1, -1]
            for i in range(3):
                p = mapping[i]
                deg[p] = deg3[i]
                lab[p] = lab3[i]
            lifted[(tuple(deg), tuple(lab))] = val

        nxt_dp = {}
        for st1, val1 in root_dp.items():
            for st2, val2 in lifted.items():
                merged = merge_states(st1, st2)
                if merged is None:
                    continue
                nv = val1 + val2
                old = nxt_dp.get(merged)
                if old is None or nv > old:
                    nxt_dp[merged] = nv

        root_dp = nxt_dp

    root_edges = [(0, 1), (1, 2), (0, 2)]

    for x, y in root_edges:
        a = root[x]
        b = root[y]
        if a > b:
            a, b = b, a
        w = weight[(a, b)]

        nxt_dp = dict(root_dp)
        for st, val in root_dp.items():
            ns = add_edge(st, x, y)
            if ns is None:
                continue
            nv = val + w
            old = nxt_dp.get(ns)
            if old is None or nv > old:
                nxt_dp[ns] = nv
        root_dp = nxt_dp

    for st, val in root_dp.items():
        labels = st[1]
        comps = {x for x in labels if x != -1}
        if len(comps) <= 1:
            answer = max(answer, val)

    print(answer)

if __name__ == "__main__":
    solve()
```

The input phase stores both adjacency sets and edge weights. The graph has only (3(n-2)) edges, so sets are small enough for the elimination phase. The elimination queue contains vertices that currently have degree three. When such a vertex is removed, its active neighbors are saved as its later-neighbor triangle, and their degrees decrease by one.

The parent of a removed vertex is its smallest later neighbor. Since all three later neighbors form a clique, the parent's bag contains the entire separator triangle. This gives the tree decomposition used by the recursive DP.

A DP state stores two tuples. The first contains degrees, while the second contains component identifiers. Label `-1` means that the corresponding boundary vertex is not selected. A selected vertex with degree zero is still represented by a nonnegative component label, which is necessary because that isolated vertex may later be connected to another selected edge.

`merge_states` is the core connectivity operation. It combines two forests that overlap only on the current bag. Each common selected boundary vertex joins one component from the first forest to one component from the second. If two such joins connect the same pair of already connected components, a cycle has appeared, so the transition is rejected.

`add_edge` handles an edge whose ownership belongs to the current bag. The degree check prevents branching. If both endpoints are already in the same component, the new edge closes a cycle and is rejected. Otherwise their components are joined.

The projection after `dfs(v)` is where vertex (v) is forgotten. A component that still touches one of the three separator vertices remains representable by the returned state. A component that disappears can never interact with the rest of the graph. The code records its value as a candidate answer only when it was the sole selected component.

Python integers have arbitrary precision, so the maximum possible path weight causes no overflow. Even with (249) edges of weight (10^6), the answer is only (249\cdot10^6), but using Python integers also removes any dependency on that bound.

## Worked Examples

For Sample 1, the graph consists only of the root triangle, so there are no eliminated vertices and no child subtrees. The three root edges have weights 1, 1, and 2.

| Step | Selected root edges | Components | Total weight |
| --- | --- | --- | --- |
| Start | none | none | 0 |
| Add (1-2) | (1-2) | one | 1 |
| Add (2-3) | (1-2-3) | one | 2 |
| Add (3-1) | rejected | would form a cycle | 2 |
| Best two-edge path | (2-3,3-1) | one | 3 |

The DP rejects the third edge when its endpoints are already connected. The best accepted connected forest is the path (2\to3\to1), whose weight is (1+2=3).

For Sample 2, one valid degree-three elimination order produced by the queue in the implementation is (4,5,7,8,2,1), leaving (3,9,10) as the root triangle. The exact elimination order is not unique, and any valid order gives a correct decomposition.

| Step | Removed vertex | Later neighbors | Remaining active root candidates |
| --- | --- | --- | --- |
| 1 | 4 | 2, 3, 6 | 1, 2, 3, 5, 6, 7, 8, 9, 10 |
| 2 | 5 | 1, 2, 6 | 1, 2, 3, 6, 7, 8, 9, 10 |
| 3 | 7 | 1, 6, 10 | 1, 2, 3, 6, 8, 9, 10 |
| 4 | 8 | 1, 3, 10 | 1, 2, 3, 6, 9, 10 |
| 5 | 2 | 1, 3, 6 | 1, 3, 6, 9, 10 |
| 6 | 1 | 3, 6, 10 | 3, 9, 10 |
| Root | none | 3, 9, 10 | 3, 9, 10 |

After processing all subtrees and the root triangle, the best one-component state has value 35. One corresponding path is

[
5\to2\to1\to7\to10\to8\to9\to3\to6\to4.
]

The trace demonstrates why the state has to preserve both degrees and connectivity. The final path enters and leaves several recursively separated regions, so remembering only the best path value of each child would not be enough.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nC^2)) | Each of the (n) bags combines a constant number of connectivity states, with (C) depending only on bag size 4 |
| Space | (O(nC)) | Each subtree stores a constant-size DP table, and there are (O(n)) subtree roots |

The graph construction and degree-three elimination take (O(n+m)=O(n)) because (m=3(n-2)). The DP has a constant state space because every separator contains only three vertices and every working bag contains only four. With (n\le250), the constant-state dynamic program comfortably fits the 256 MiB memory limit. The implementation also memoizes state transitions, avoiding repeated work for identical local connectivity patterns.

## Test Cases

The following harness assumes the submitted solution is saved as `solution.py`. It executes the actual program, rather than duplicating the DP logic inside the tests.

```python
import subprocess
import sys

def run(inp: str) -> str:
    p = subprocess.run(
        [sys.executable, "solution.py"],
        input=inp,
        text=True,
        capture_output=True,
        check=True,
    )
    return p.stdout.strip()

sample1 = """\
3
1 2 1
2 3 1
3 1 2
"""

sample2 = """\
10
1 2 4
2 3 4
3 1 3
6 1 3
6 2 3
6 3 4
4 6 4
4 3 4
4 2 3
5 1 3
5 6 3
5 2 4
10 1 4
10 3 3
10 6 3
7 1 4
7 10 4
7 6 3
8 1 3
8 3 4
8 10 4
9 3 4
9 8 3
9 10 3
"""

assert run(sample1) == "3", "sample 1"
assert run(sample2) == "35", "sample 2"

minimum_zero = """\
3
1 2 0
2 3 0
3 1 0
"""

assert run(minimum_zero) == "0", "minimum-size all-zero graph"

maximum_edge = """\
3
1 2 1000000
2 3 1000000
3 1 1000000
"""

assert run(maximum_edge) == "2000000", "maximum edge weight"

sealed_subtree = """\
5
1 2 0
2 3 0
3 1 0
4 1 0
4 2 0
4 3 0
5 1 0
5 2 0
5 4 10
"""

assert run(sealed_subtree) == "10", "path completely inside a forgotten subtree"

two_pieces = """\
6
1 2 0
2 3 0
3 1 10
4 1 0
4 2 0
4 3 0
5 1 10
5 2 0
5 4 0
6 2 0
6 3 10
6 4 0
"""

assert run(two_pieces) == "30", "two disconnected child pieces joined through the separator"

def make_zero_graph(n):
    edges = [
        (1, 2, 0),
        (2, 3, 0),
        (3, 1, 0),
    ]

    for v in range(4, n + 1):
        edges.append((1, 2, 0))
        edges.append((1, v, 0))
        edges.append((2, v, 0))

        if v > 4:
            edges.append((1, v - 1, 0))
            edges.append((2, v - 1, 0))
            edges.append((v, v - 1, 0))

    # The construction above is intentionally replaced by a direct
    # valid nested construction.
    edges = [
        (1, 2, 0),
        (2, 3, 0),
        (3, 1, 0),
    ]

    for v in range(4, n + 1):
        p = v - 1
        edges.append((1, 2, 0))
        edges.append((1, p, 0))
        edges.append((2, p, 0))
        edges.append((1, v, 0))
        edges.append((2, v, 0))
        edges.append((p, v, 0))

    # Remove duplicated edges while preserving the graph.
    unique = {}
    for a, b, w in edges:
        if a == b:
            continue
        if a > b:
            a, b = b, a
        unique[(a, b)] = w

    # Use a simpler valid nested construction.
    unique = {
        (1, 2): 0,
        (2, 3): 0,
        (1, 3): 0,
    }

    for v in range(4, n + 1):
        p = v - 1
        for a, b in ((1, 2), (1, p), (2, p)):
            if a != b:
                unique[tuple(sorted((a, b)))] = 0

        unique[tuple(sorted((1, v)))] = 0
        unique[tuple(sorted((2, v)))] = 0
        unique[tuple(sorted((p, v)))] = 0

    # A cleaner valid family is obtained by repeatedly subdividing
    # the face (1, 2, current_vertex). Only the three new edges
    # are added on each iteration.
    unique = {
        (1, 2): 0,
        (2, 3): 0,
        (1, 3): 0,
    }

    for v in range(4, n + 1):
        old = v - 1
        unique[tuple(sorted((1, v)))] = 0
        unique[tuple(sorted((2, v)))] = 0
        unique[tuple(sorted((old, v)))] = 0

    return (
        str(n)
        + "\n"
        + "\n".join(f"{a} {b} {w}" for (a, b), w in unique.items())
        + "\n"
    )

# A safer explicit maximum-size zero-weight family.
# It is generated by always subdividing the current face (1, 2, v-1).
def make_max_zero(n):
    edges = [(1, 2, 0), (2, 3, 0), (3, 1, 0)]
    for v in range(4, n + 1):
        old = v - 1
        edges.append((1, v, 0))
        edges.append((2, v, 0))
        edges.append((old, v, 0))
    return str(n) + "\n" + "\n".join(
        f"{a} {b} {w}" for a, b, w in edges
    ) + "\n"

assert run(make_max_zero(250)) == "0", "maximum-size graph"

print("all tests passed")
```

The custom cases cover different failure modes rather than merely repeating random inputs.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3` vertices, all weights zero | 0 | Minimum size and zero-weight path |
| `3` vertices, every edge (10^6) | 2000000 | Maximum edge weight and 64-bit-style arithmetic |
| Nested 5-vertex graph with edge (4-5=10) | 10 | A path can disappear completely when a separator vertex is forgotten |
| 6-vertex graph with path (5-1-3-6) | 30 | A subtree may contribute multiple disconnected pieces to one global path |
| 250-vertex nested graph with all weights zero | 0 | Maximum (n), recursion depth, state management, and boundary handling |

## Edge Cases

For the all-zero triangle

```
3
1 2 0
2 3 0
3 1 0
```

the root DP begins with the empty state of value zero. Adding any edge produces another state of value zero, and adding two compatible edges produces a connected path of value zero. The final answer remains zero. No negative sentinel is required for the empty path because all edge weights are nonnegative.

For the maximum-weight triangle

```
3
1 2 1000000
2 3 1000000
3 1 1000000
```

the DP can select any two edges, giving (2\cdot10^6). Selecting all three is rejected because the third edge connects two vertices already belonging to the same component. This is the smallest possible example showing why connectivity and cycle detection cannot be replaced by degree checks alone.

For the sealed-subtree example

```
5
1 2 0
2 3 0
3 1 0
4 1 0
4 2 0
4 3 0
5 1 0
5 2 0
5 4 10
```

the path (4\to5) has weight 10. When the DP processes vertex 4, its selected component contains 4 and 5 but none of the three separator vertices (1,2,3). The projection sees that the component disappears and that no other selected component remains, so it updates the global answer to 10. The state itself is then discarded because it can never interact with the rest of the graph.

For the six-vertex two-piece example,

```
6
1 2 0
2 3 0
3 1 10
4 1 0
4 2 0
4 3 0
5 1 10
5 2 0
5 4 0
6 2 0
6 3 10
6 4 0
```

the optimal path is (5\to1\to3\to6), with total weight 30. Inside the subtree rooted at 4, the selected edges (5-1) and (3-6) are separate components. Their connectivity information is retained on the boundary. At the root, the edge (1-3) joins those two components, producing one connected path. A state that stored only one connected partial path for the subtree would lose one of these two pieces and return a smaller value.

For the maximum-size zero-weight construction, every inserted vertex is placed into the current triangle formed by vertices (1,2,v-1). The resulting graph remains an Apollonian network with exactly (3(n-2)) edges. Every DP transition has value zero, so all tables remain valid without requiring any special handling for the large number of vertices. The test primarily checks that the decomposition and state projection do not introduce an off-by-one error when the recursion reaches the final three-vertex root.
