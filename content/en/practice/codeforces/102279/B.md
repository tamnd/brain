---
title: "CF 102279B - Beggin' For A Node"
description: "We have a tree with up to 200,000 vertices, and one unknown vertex contains the hidden secret. The program can communicate with an interactor using two queries. A type 1 query asks for the distance from a chosen vertex to the hidden vertex."
date: "2026-08-16T19:10:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102279
codeforces_index: "B"
codeforces_contest_name: "HCW 19 Team Round (ICPC format)"
rating: 0
weight: 102279
solve_time_s: 129
verified: true
draft: false
---

[CF 102279B - Beggin' For A Node](https://codeforces.com/problemset/problem/102279/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a tree with up to 200,000 vertices, and one unknown vertex contains the hidden secret. The program can communicate with an interactor using two queries. A type 1 query asks for the distance from a chosen vertex to the hidden vertex. A type 2 query asks for the neighbor of the chosen vertex that lies on the path toward the hidden vertex. If the chosen vertex is already the hidden vertex, type 2 returns zero. The goal is to identify the hidden vertex using at most 36 queries. The problem is genuinely interactive, so the input contains only the tree, while the answers to queries arrive during execution.

The tree has 200,000 vertices, so scanning all vertices with a query is immediately impossible under a 36-query limit. Even though a linear preprocessing pass over the tree is completely reasonable, asking one query per vertex would require 200,000 queries in the worst case. The intended solution has to make the set of possible hidden vertices shrink geometrically after every query.

There are three edge cases that are especially easy to mishandle. The first is a one-vertex tree:

```
1
```

The only vertex is necessarily the answer, so the correct output is `1`. A careless implementation that assumes every type 2 answer is a valid neighbor would fail because the interactor returns zero when querying the hidden vertex itself.

The second case is a two-vertex tree:

```
2
1 2
```

If the hidden vertex is 2, querying vertex 1 with type 2 returns 2. The algorithm must then continue inside the one-vertex component containing 2 and query it again, receiving zero. Stopping after the first nonzero response would output the neighbor rather than the hidden vertex.

The third case is a star:

```
5
1 2
1 3
1 4
1 5
```

If the hidden vertex is 5, vertex 1 is a centroid. A type 2 query at 1 immediately identifies the only relevant component, namely the singleton containing 5. The algorithm must cut the centroid from the remaining tree rather than globally discard the returned neighbor or treat the response as the final answer.

The official editorial gives an LCA, DFS, and binary-search solution and also mentions centroid decomposition as an alternative. The approach below uses the centroid idea directly, which makes the query bound particularly transparent.

## Approaches

A straightforward strategy is to ask a type 1 query for every vertex until the returned distance is zero. This is correct because exactly one vertex has distance zero from the hidden vertex. The problem is the query limit. In the worst case the hidden vertex is the last vertex tested, requiring 200,000 queries, while the interactor permits only 36.

The brute-force approach works because a distance query gives complete information about whether the tested vertex is the answer. It fails because it spends one query to distinguish one candidate. We need a query whose answer can eliminate a large fraction of candidates at once.

The key observation is the definition of a tree centroid. Every tree has a vertex such that, after removing that vertex, every resulting connected component contains at most half of the original vertices. Suppose the current set of possible hidden vertices forms a connected component and we choose its centroid `c`.

A type 2 query at `c` gives exactly the first edge on the path from `c` to the hidden vertex. If the answer is zero, `c` itself is hidden and we are finished. Otherwise, suppose the answer is `v`. Since the hidden vertex lies somewhere beyond `v`, it must belong to the component containing `v` after `c` is removed. We can discard every other component completely.

The important part is that the remaining component has at most half as many vertices as the previous one. We repeat the same operation on that component. This is precisely the query pattern behind a centroid decomposition, and it reduces the number of possible vertices by a factor of roughly two after every query. A centroid-based solution for this problem is also described in external contest material as a natural way to solve the task.

For 200,000 vertices, 18 halvings are enough because `2^18 = 262144`. Thus the algorithm uses at most 18 type 2 queries, comfortably below the limit of 36.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) queries and O(n) local work | O(n) | Too slow |
| Centroid Search | O(n log n) local work and O(log n) queries | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the adjacency list of the tree. We will repeatedly examine connected components obtained by cutting previously chosen centroids, so the original tree itself never needs to be modified.
2. Maintain a Boolean `blocked` array. A blocked vertex represents a centroid that has already been removed from the current search space. The component containing the hidden vertex is always represented by one unblocked starting vertex.
3. Starting from the current vertex, traverse only unblocked vertices and collect the entire current component. During this traversal, store a parent for every visited vertex. An iterative traversal is preferable in Python because a tree can be a path of length 200,000, which would exceed the normal recursion limit.
4. Compute subtree sizes inside the collected component by processing the traversal order in reverse. For every vertex, the size of the component on its parent side is `total_size - subtree_size[v]`, while every child contributes its own subtree size.
5. Find a vertex `c` for which every resulting component has size at most `total_size / 2`. Such a vertex is a centroid. We can simply scan all vertices in the current component and test this condition using the subtree sizes.
6. Ask the interactor `? 2 c`. If the answer is zero, the centroid itself is the hidden vertex, so print `! c` and terminate.
7. If the answer is a vertex `v`, block `c` and make `v` the starting vertex for the next iteration. The edge from `c` toward `v` is now effectively cut. Because `v` lies on the path from `c` to the hidden vertex, the hidden vertex is guaranteed to be inside this new component.
8. Repeat until the type 2 query returns zero. Each iteration reduces the number of possible vertices by at least half, so at most 18 queries are needed for `n <= 200000`.

### Why it works

Maintain the invariant that the current unblocked component contains the hidden vertex. Initially the entire tree is the current component, so the invariant is true. When its centroid `c` is queried, a nonzero answer `v` is the neighbor of `c` on the unique path from `c` to the hidden vertex. Removing `c` therefore leaves the hidden vertex in exactly the component containing `v`. The algorithm keeps precisely that component, so the invariant remains true. If the query returns zero, the interactor has established that `c` is the hidden vertex, so the algorithm can safely output it.

The centroid property guarantees that the retained component contains at most half of the previous component. Starting from at most 200,000 vertices, after 18 such reductions fewer than one vertex can remain, so the hidden vertex must have been identified before exceeding the 36-query limit.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1_000_000)

def find_centroid(start, graph, blocked, parent, size):
    order = [start]
    parent[start] = 0

    for v in order:
        pv = parent[v]
        for to in graph[v]:
            if blocked[to] or to == pv:
                continue
            parent[to] = v
            order.append(to)

    total = len(order)

    for v in reversed(order):
        size[v] = 1
        pv = parent[v]
        for to in graph[v]:
            if blocked[to] or parent[to] != v:
                continue
            size[v] += size[to]

    for v in order:
        largest = total - size[v]

        for to in graph[v]:
            if blocked[to] or parent[to] != v:
                continue
            if size[to] > largest:
                largest = size[to]

        if largest * 2 <= total:
            return v

    return start

def ask(t, v):
    print("?", t, v, flush=True)
    ans = int(input())
    if ans == -1:
        sys.exit(0)
    return ans

def main():
    n = int(input())

    graph = [[] for _ in range(n + 1)]

    for _ in range(n - 1):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    blocked = [False] * (n + 1)
    parent = [0] * (n + 1)
    size = [0] * (n + 1)

    current = 1
    queries = 0

    while True:
        centroid = find_centroid(
            current,
            graph,
            blocked,
            parent,
            size
        )

        queries += 1
        if queries > 36:
            sys.exit(0)

        nxt = ask(2, centroid)

        if nxt == 0:
            print("!", centroid, flush=True)
            return

        blocked[centroid] = True
        current = nxt

if __name__ == "__main__":
    main()
```

The adjacency list stores the original tree. No edges are physically deleted because doing so would require updating several adjacency lists. Instead, `blocked[v]` makes a previously selected centroid invisible to all future component traversals.

`find_centroid` first traverses the current connected component. The `order` list contains its vertices in parent-before-child order. Processing this list backwards gives every subtree size without recursion. This is particularly useful for Python because a path-shaped tree can contain 200,000 nested vertices.

For a vertex `v`, `size[v]` is its subtree size with respect to the temporary root `start`. Removing `v` creates one possible component on the parent side with size `total - size[v]`, plus one component for every child with size `size[child]`. The vertex is a centroid exactly when the largest of these values is at most half of `total`.

The `ask` function prints the query and immediately flushes standard output. Flushing is mandatory in an interactive problem because the interactor cannot answer a query that remains buffered. If the interactor returns `-1`, the protocol says the program must terminate.

Only type 2 queries are needed. A nonzero answer is not itself the hidden vertex. It is the first vertex after the current centroid on the path to the hidden vertex, so it tells us which half-sized component to retain.

The query counter is technically unnecessary for correctness because the centroid argument already proves that at most 18 queries are made for the maximum input size. Keeping it in the implementation makes accidental protocol violations fail safely.

There is no recursion in the component traversal or centroid computation. This avoids Python stack overflow on a path-shaped tree. Python integers also have no overflow issue for the subtree sizes, although all relevant sizes are only at most 200,000 anyway.

## Worked Examples

The statement provides one interaction transcript. Its tree is

```
7
2 1
2 4
3 5
6 2
1 3
2 7
```

and the transcript reveals that the hidden vertex is 3.

The centroid of the full seven-vertex tree is vertex 2. Removing 2 leaves components of sizes 1, 1, 1, and 3, so every component has size at most 3.

| Current component | Size | Centroid | Type 2 answer | Next component | Size after cut |
| --- | --- | --- | --- | --- | --- |
| `{1,2,3,4,5,6,7}` | 7 | 2 | 1 | `{1,3,5}` | 3 |
| `{1,3,5}` | 3 | 3 | 0 | Finished | 1 |

The first query is effectively `? 2 2`, and the interactor returns 1 because the path from 2 to the hidden vertex 3 begins with the edge `2 -> 1`. After blocking 2, the only relevant component is `{1,3,5}`. Its centroid is 3. Querying 3 returns zero, so the answer is 3. This demonstrates the central invariant: after every nonzero answer, the hidden vertex remains in the selected component.

For a second example, consider a star whose center is vertex 1, with the hidden vertex at 5.

```
6
1 2
1 3
1 4
1 5
1 6
```

The center is itself a centroid because removing it leaves five components of size one.

| Current component | Size | Centroid | Type 2 answer | Next component | Size after cut |
| --- | --- | --- | --- | --- | --- |
| `{1,2,3,4,5,6}` | 6 | 1 | 5 | `{5}` | 1 |
| `{5}` | 1 | 5 | 0 | Finished | 1 |

The first query identifies the branch containing the hidden vertex immediately. The second query is made on that singleton component and returns zero. This example shows why the nonzero type 2 response should be interpreted as a direction, not as the final answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each centroid-search iteration scans its current component, whose size decreases geometrically |
| Space | O(n) | The adjacency list and auxiliary arrays each require linear space |
| Queries | O(log n) | Every query reduces the candidate component to at most half its previous size |

For `n = 200000`, there can be at most 18 centroid queries because `2^18 = 262144`. The local tree processing performs a geometric sequence of scans, bounded by `O(n log n)`, which is easily compatible with the 2 second and 256 MB limits in a compiled implementation and is also practical in Python with iterative traversal.

## Test Cases

Because this is an interactive problem, the published sample is an interaction transcript rather than an ordinary deterministic input/output pair. A normal `run(input)` helper cannot reproduce the interactor. The following test harness uses a fixed hidden vertex and simulates type 2 answers. The offline solver mirrors the submitted centroid algorithm, while the simulator roots the tree at the hidden vertex so that the parent of a queried vertex is exactly the interactor's type 2 response.

```python
import io
import sys

def solve_offline(inp: str, hidden: int):
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    graph = [[] for _ in range(n + 1)]

    for _ in range(n - 1):
        u = next(it)
        v = next(it)
        graph[u].append(v)
        graph[v].append(u)

    # Simulate the interactor's type-2 answers.
    parent_hidden = [0] * (n + 1)
    order = [hidden]

    for v in order:
        for to in graph[v]:
            if to == parent_hidden[v]:
                continue
            parent_hidden[to] = v
            order.append(to)

    blocked = [False] * (n + 1)
    parent = [0] * (n + 1)
    size = [0] * (n + 1)

    def find_centroid(start):
        order = [start]
        parent[start] = 0

        for v in order:
            for to in graph[v]:
                if blocked[to] or to == parent[v]:
                    continue
                parent[to] = v
                order.append(to)

        total = len(order)

        for v in reversed(order):
            size[v] = 1
            for to in graph[v]:
                if blocked[to] or parent[to] != v:
                    continue
                size[v] += size[to]

        for v in order:
            largest = total - size[v]

            for to in graph[v]:
                if blocked[to] or parent[to] != v:
                    continue
                largest = max(largest, size[to])

            if largest * 2 <= total:
                return v

        return start

    current = 1
    queries = 0

    while True:
        centroid = find_centroid(current)
        queries += 1

        if centroid == hidden:
            return centroid, queries

        nxt = parent_hidden[centroid]
        blocked[centroid] = True
        current = nxt

# Provided sample tree. The interaction transcript establishes hidden = 3.
sample = """\
7
2 1
2 4
3 5
6 2
1 3
2 7
"""
assert solve_offline(sample, 3) == (3, 2), "sample"

# Minimum-size tree.
case_min = """\
1
"""
assert solve_offline(case_min, 1) == (1, 1), "minimum tree"

# Two vertices, hidden at the second vertex.
case_two = """\
2
1 2
"""
assert solve_offline(case_two, 2) == (2, 2), "two-vertex boundary"

# Star, testing a highly branching tree and an immediate singleton component.
case_star = """\
5
1 2
1 3
1 4
1 5
"""
assert solve_offline(case_star, 5) == (5, 2), "star"

# Maximum-size path, hidden at the final vertex.
n = 200000
case_max = str(n) + "\n" + "\n".join(
    f"{i} {i + 1}" for i in range(1, n)
) + "\n"

answer, queries = solve_offline(case_max, n)
assert answer == n, "maximum-size path answer"
assert queries <= 18, "centroid query bound"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `7` with the six sample edges, hidden `3` | `3` | Provided interaction example and normal centroid reduction |
| `1` | `1` | Minimum input and zero-response query |
| `2` with edge `1 2`, hidden `2` | `2` | Singleton component after the first cut |
| Five-vertex star centered at `1`, hidden `5` | `5` | Highly branching tree and directional type 2 response |
| Path with 200,000 vertices, hidden `200000` | `200000` | Maximum size, deep tree, iterative traversal, and query bound |

The maximum-size test deliberately uses a path because it is the worst shape for recursive tree algorithms. The submitted solution never recurses through the path, and the centroid process reduces it to roughly half its remaining length at every query.

## Edge Cases

For a one-vertex tree,

```
1
```

the only possible current component is `{1}`, whose centroid is 1. The type 2 query `? 2 1` returns zero because vertex 1 is the hidden vertex. The program immediately prints `! 1`. There is no attempt to interpret zero as a neighbor, so the boundary case is handled correctly.

For the two-vertex tree

```
2
1 2
```

with hidden vertex 2, the initial centroid is 1. The type 2 query at 1 returns 2. Vertex 1 is then blocked, leaving the singleton component `{2}`. Its centroid is 2, and the next type 2 query returns zero. The algorithm prints 2 after exactly two queries. This is the smallest example showing why a nonzero type 2 response means "continue in this direction" rather than "answer this vertex".

For the five-vertex star

```
5
1 2
1 3
1 4
1 5
```

with hidden vertex 5, vertex 1 is a centroid. Querying it returns 5, so all other leaves can immediately be discarded. The next component contains only vertex 5, whose query returns zero. The algorithm uses two queries and never needs distance information.

For the maximum-size path, the first centroid lies near the middle. If the hidden vertex is at one endpoint, the type 2 answer selects the half containing that endpoint. The next centroid again lies near the middle of that half, and the same process continues. A path of 200,000 vertices therefore requires at most 18 queries despite having a depth of 199,999. The iterative traversal is what prevents the path's depth from causing Python recursion failure.

The central edge case across all of these examples is the moment when the remaining component has one vertex. The centroid is necessarily that vertex, and type 2 returns zero. The implementation checks this response before blocking the centroid, so it never accidentally removes the correct answer from the search space.
