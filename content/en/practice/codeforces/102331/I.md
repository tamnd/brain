---
title: "CF 102331I - Interactive Vertex"
description: "We are given a tree with up to (200,000) vertices. Somewhere in this tree there is one hidden special vertex (u). We know the entire tree, but not (u), and we must discover it through interactive queries. A query chooses a vertex (x) and a set of vertices (V)."
date: "2026-08-13T03:43:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102331
codeforces_index: "I"
codeforces_contest_name: "2019 Summer Petrozavodsk Camp, Day 2: 300iq Contest 2 (XX Open Cup, Grand Prix of Kazan)"
rating: 0
weight: 102331
solve_time_s: 180
verified: true
draft: false
---

[CF 102331I - Interactive Vertex](https://codeforces.com/problemset/problem/102331/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree with up to (200,000) vertices. Somewhere in this tree there is one hidden special vertex (u). We know the entire tree, but not (u), and we must discover it through interactive queries.

A query chooses a vertex (x) and a set of vertices (V). The interactor answers whether

[
\operatorname{dist}(u,x)\leq \operatorname{dist}(u,v)
]

for every (v\in V). In other words, the answer is 1 exactly when (x) is no farther from the hidden vertex than every vertex in the queried set. The tree and the hidden vertex remain fixed during the whole interaction. The official protocol allows at most (4\lceil\log_2 n\rceil) queries.

The input consists of (n), followed by the (n-1) tree edges. There is no ordinary offline output because the answer to each query comes from the interactor. Once the hidden vertex is determined, we print `! u`.

The size bound of (200,000) rules out anything quadratic in the tree size. Even (O(n^2)) would mean around (4\cdot10^{10}) operations in the worst case, far beyond a two second limit. More subtly, an (O(n\log n)) preprocessing algorithm is perfectly reasonable, while the number of interactive queries has its own much stricter logarithmic bound. The solution consequently has to combine linear or near-linear tree processing with a carefully balanced sequence of queries.

There are several easy boundary cases that can break a careless implementation. Consider the smallest possible tree,

```
2
1 2
```

with hidden vertex (u=2). A query centered at vertex 1 with vertex 2 in the queried set must answer 0, because (\operatorname{dist}(2,2)=0<1=\operatorname{dist}(2,1)). If the implementation assumes that a centroid always has at least two neighboring components, it can fail here.

A star is another useful edge case. For

```
5
1 2
1 3
1 4
1 5
```

if the hidden vertex is 1, querying (x=1) against all four neighbors returns 1. Every neighbor is at distance 1 from the hidden vertex, while (x) itself is at distance 0. A solution that only interprets the query as choosing one of the child components would miss the possibility that the centroid itself is the answer.

The opposite situation also matters. In the same star, if (u=2), querying the four neighbors of vertex 1 returns 0, because vertex 2 itself is among the queried vertices and has distance 0 from (u), while vertex 1 has distance 1. A careless solution might reverse the meaning of the answer and continue into the wrong components.

Finally, a path can have a centroid whose two sides have very different structures. For example,

```
7
1 2
2 3
3 4
4 5
5 6
6 7
```

has a balanced central region, but after removing a centroid, the two candidate components are themselves paths. The algorithm must recompute the centroid inside the surviving component rather than continue using the original rooting.

## Approaches

The simplest possible strategy is to test vertices one by one. For a candidate (x), query (x) against every other vertex. The answer is 1 exactly when (x=u), because if (x=u), its distance is zero and every other vertex is at nonnegative distance, while if (x\neq u), including (u) in the queried set makes the answer 0. This approach is correct, but it can require (n-1) queries. At the maximum (n=200,000), that is (199,999) queries, while the allowed limit is only (4\lceil\log_2 200000\rceil=72). The problem is therefore not computational work inside a query, but the amount of information we extract from each interaction.

The key observation is what happens when (x) is adjacent to every vertex in the queried set. Suppose (c) is some vertex and (v) is one of its neighbors. Removing (c) splits the tree into components, one containing each neighbor. If the hidden vertex (u) lies in the component containing (v), the path from (u) to (c) starts with the edge (v-c). Consequently,

[
\operatorname{dist}(u,v)=\operatorname{dist}(u,c)-1.
]

So a query with (x=c) and a collection of neighboring vertices (v_1,\ldots,v_k) returns 0 precisely when the hidden vertex lies in one of the corresponding components. If it lies outside all those components, every queried neighbor is one edge farther away through (c), so the answer is 1. This converts the unusual distance comparison into a direct membership test for a union of tree components. The same core observation is used by the standard solution.

The next question is how to choose (c). We use a centroid of the current candidate component. Removing a centroid leaves components containing at most half of the current vertices. This gives us a naturally shrinking search space.

If we simply binary searched the neighboring components by their count, we could still do badly when one component contains many more vertices than another. Instead, we perform a weighted binary search where every component is weighted by its number of vertices. At every split we choose the prefix whose total weight gives the most balanced two sides. The interactor then tells us which side contains (u). This is the weighted search described in the contest tutorial.

The centroid query itself costs one interaction. If it returns 1, the centroid is the answer. Otherwise, the hidden vertex lies in one of the components. Weighted binary search identifies that component. We mark the centroid as removed and repeat the same process inside the surviving component. Because every stage substantially decreases the number of possible vertices, the total number of queries stays logarithmic, within the required (4\lceil\log_2 n\rceil) bound.

The brute-force method spends queries on individual vertices. The optimal method instead uses the tree's separators to turn one query into a statement about an entire connected component.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n)) queries, (O(n^2)) if distances are recomputed naively | (O(n)) | Too many queries |
| Optimal | (O(n\log n)) tree processing, (O(\log n)) queries | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Start with the whole tree as the candidate component. Maintain a `blocked` array. A blocked vertex has already been used as a centroid and will never belong to a future candidate component.
2. Find a centroid (c) of the current unblocked component. We do this with an iterative tree traversal, because a path with (200,000) vertices would overflow Python's recursion stack if a recursive DFS were used.
3. Consider every unblocked neighbor (v) of (c). Removing (c) creates one candidate component for each such neighbor. Store the size of each component together with its neighbor. Since (c) is a centroid, every such component contains at most half of the current candidate vertices.
4. Query (c) against all of these neighboring vertices. If the answer is 1, (u=c). Indeed, if (u=c), then (\operatorname{dist}(u,c)=0), so the condition is true. If (u) lies in any component of a neighbor (v), then (v) is one edge closer to (u) than (c), making the condition false. This single query detects the centroid exactly.
5. If the answer was 0, sort the candidate components by their sizes. Maintain an interval of component indices. Choose a prefix that minimizes the larger of its total size and the remaining suffix size. Query the centroid against the neighbor vertices belonging to that prefix.
6. If the answer is 0, the hidden vertex belongs to the selected prefix, so discard the suffix. If the answer is 1, the hidden vertex belongs to the suffix, so discard the prefix. Repeat until only one component remains.
7. Mark the centroid as blocked and make the unique surviving component the new candidate component. Since the tree is connected, this component can be represented simply by its surviving neighbor and its known size.
8. When the candidate component has one vertex, that vertex is necessarily the hidden vertex. Print it and flush.

The central invariant is that after every query, the hidden vertex remains inside the current candidate component. The centroid query preserves this invariant by either terminating at the centroid or proving that the hidden vertex lies in one of the components. Every weighted binary query then chooses exactly one side that must contain the hidden vertex. Once the centroid is removed, the surviving side is an actual connected component of the original candidate tree, so the same reasoning applies recursively. The weighted split keeps shrinking the candidate set sufficiently quickly for the logarithmic query bound. The official solution follows this centroid plus weighted binary search structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    blocked = [False] * (n + 1)
    parent = [0] * (n + 1)
    size = [0] * (n + 1)

    def ask(x, vertices):
        print("?", len(vertices), x, *vertices, flush=True)
        return int(input())

    def find_centroid(start):
        order = [start]
        parent[start] = 0

        for v in order:
            pv = parent[v]
            for to in g[v]:
                if blocked[to] or to == pv:
                    continue
                parent[to] = v
                order.append(to)

        total = len(order)

        for v in order:
            size[v] = 1

        for v in reversed(order):
            p = parent[v]
            if p:
                size[p] += size[v]

        centroid = start
        for v in order:
            largest = total - size[v]

            for to in g[v]:
                if blocked[to]:
                    continue
                if parent[to] == v:
                    if size[to] > largest:
                        largest = size[to]

            if largest * 2 <= total:
                centroid = v
                break

        return centroid, total

    current = 1
    current_size = n

    while current_size > 1:
        centroid, total = find_centroid(current)

        parts = []

        for to in g[centroid]:
            if blocked[to]:
                continue

            if parent[to] == centroid:
                part_size = size[to]
            else:
                part_size = total - size[centroid]

            parts.append((part_size, to))

        parts.sort()

        # If the centroid itself is the hidden vertex, the answer is 1.
        all_neighbors = [v for _, v in parts]
        if ask(centroid, all_neighbors):
            print("!", centroid, flush=True)
            return

        left = 0
        right = len(parts) - 1

        while left < right:
            total_weight = 0
            for i in range(left, right + 1):
                total_weight += parts[i][0]

            best_mid = left
            best_balance = 10**30
            prefix = 0

            for i in range(left, right + 1):
                prefix += parts[i][0]
                balance = max(prefix, total_weight - prefix)

                if balance < best_balance:
                    best_balance = balance
                    best_mid = i

            chosen = [parts[i][1] for i in range(left, best_mid + 1)]

            if ask(centroid, chosen):
                left = best_mid + 1
            else:
                right = best_mid

        next_vertex = parts[left][1]
        next_size = parts[left][0]

        blocked[centroid] = True
        current = next_vertex
        current_size = next_size

    print("!", current, flush=True)

if __name__ == "__main__":
    solve()
```

The input phase builds the undirected tree exactly as usual. There are no multiple test cases because this interactive problem describes one tree per invocation. The official protocol likewise starts with a single (n) and its (n-1) edges.

The `ask` function is deliberately tiny. It prints exactly one query line, flushes once, and immediately reads the interactor's answer. The statement explicitly requires flushing after every query in Python.

`find_centroid` uses an iterative traversal. The first pass collects all vertices of the current unblocked component and records their parents. The reverse pass computes subtree sizes. For a vertex (v), the largest component created by removing it is either the part above (v), with size `total - size[v]`, or one of its child subtrees. The first vertex for which every such component has size at most half is a centroid.

When the centroid is not the root of the temporary traversal, one of its neighbors is its parent. For that neighbor, its component has size `total - size[centroid]`. For every child neighbor, the component size is simply `size[to]`. This is why the code needs the parent information from the centroid search.

The `parts` list stores `(component_size, neighbor)` pairs and sorts them by component size. Sorting is not needed for correctness of an individual query, but it is part of the weighted binary search strategy that gives the required query bound. The query vertices are the neighbors themselves, not arbitrary vertices deep inside their components. That is the critical distance property.

The loop `while left < right` is the weighted binary search. Its boundaries are indices into `parts`, not vertex numbers. After every answer, exactly one side of the interval is discarded. The final remaining neighbor identifies the only component that can contain (u).

Python integers have arbitrary precision, so there is no integer overflow issue in the component-size arithmetic. The implementation also avoids recursive DFS, which is a practical requirement for a tree shaped like a chain with (200,000) vertices.

## Worked Examples

### Sample 1

The tree is a star centered at vertex 1, and the interactor answers 1 to the first query.

| Step | Candidate size | Centroid | Queried neighbors | Answer | New state |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 1 | 2, 3, 4, 5 | 1 | answer = 1 |

The answer is immediately vertex 1. This demonstrates why the centroid itself must be checked before trying to select one of its components. The official sample uses exactly this one-query interaction.

### Sample 2

The tree is the same star, but the hidden vertex is 2. The official sample supplies four zero responses, although interactive solutions are allowed to ask different valid queries. Our weighted split may use a different sequence while still reaching vertex 2.

| Step | Candidate size | Centroid | Queried vertices | Answer | New state |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 1 | 2, 3, 4, 5 | 0 | (u) is in one leaf component |
| 2 | 4 | 1 | 2, 3 | 0 | (u) is in component 2 |
| 3 | 1 | 1 | 2 | 0 | component 2 survives |

The final surviving component is the singleton containing vertex 2, so the program prints `! 2`. The sample's transcript contains a different sequence of valid partitions, which is normal for an interactive problem because the exact query order is not uniquely prescribed. The official sample confirms the final answer is 2.

The important invariant in both examples is that a zero answer to a query against neighbors of the centroid means the hidden vertex lies in one of those neighbors' components. The algorithm never has to calculate a distance to the hidden vertex itself.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n)) | Each centroid stage scans its current component, and every vertex belongs to only (O(\log n)) centroid levels |
| Space | (O(n)) | The adjacency lists and auxiliary arrays each use linear space |
| Queries | (O(\log n)) | Centroid checks and weighted binary-search queries shrink the candidate space geometrically |

The maximum tree size is (200,000), so linear-size arrays and (O(n\log n)) preprocessing comfortably fit within the 512 MiB memory limit. The interactive part is the stricter requirement. The problem permits (4\lceil\log_2 n\rceil) queries, which is only 72 queries at the maximum (n). The centroid and weighted-search construction is designed specifically to stay within that logarithmic budget.

## Test Cases

An ordinary `run(input) == output` harness cannot test this problem faithfully because the output depends on responses generated by the interactor. The useful local test is instead a deterministic judge simulator: it chooses a hidden vertex, computes each query's answer from actual tree distances, and checks that the algorithm eventually identifies that vertex.

The following harness mirrors the algorithm offline. It also records the number of queries, so the logarithmic interaction bound can be tested directly.

```python
# Offline simulator for the interactive algorithm.
# It does not replace the interactive submission above.

def simulate(n, edges, hidden):
    g = [[] for _ in range(n + 1)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    blocked = [False] * (n + 1)
    parent = [0] * (n + 1)
    size = [0] * (n + 1)
    queries = 0

    def distances_from_hidden():
        dist = [-1] * (n + 1)
        dist[hidden] = 0
        q = [hidden]

        for v in q:
            for to in g[v]:
                if dist[to] == -1:
                    dist[to] = dist[v] + 1
                    q.append(to)

        return dist

    dist = distances_from_hidden()

    def ask(x, vertices):
        nonlocal queries
        queries += 1
        return all(dist[v] >= dist[x] for v in vertices)

    def find_centroid(start):
        order = [start]
        parent[start] = 0

        for v in order:
            pv = parent[v]
            for to in g[v]:
                if blocked[to] or to == pv:
                    continue
                parent[to] = v
                order.append(to)

        total = len(order)

        for v in order:
            size[v] = 1

        for v in reversed(order):
            p = parent[v]
            if p:
                size[p] += size[v]

        for v in order:
            largest = total - size[v]

            for to in g[v]:
                if blocked[to]:
                    continue
                if parent[to] == v:
                    largest = max(largest, size[to])

            if largest * 2 <= total:
                return v, total

        raise AssertionError("centroid not found")

    current = 1
    current_size = n

    while current_size > 1:
        centroid, total = find_centroid(current)

        parts = []

        for to in g[centroid]:
            if blocked[to]:
                continue

            if parent[to] == centroid:
                part_size = size[to]
            else:
                part_size = total - size[centroid]

            parts.append((part_size, to))

        parts.sort()

        if ask(centroid, [v for _, v in parts]):
            answer = centroid
            assert answer == hidden
            assert queries <= 4 * ((n - 1).bit_length())
            return answer, queries

        left = 0
        right = len(parts) - 1

        while left < right:
            total_weight = sum(parts[i][0] for i in range(left, right + 1))

            best_mid = left
            best_balance = 10**30
            prefix = 0

            for i in range(left, right + 1):
                prefix += parts[i][0]
                balance = max(prefix, total_weight - prefix)

                if balance < best_balance:
                    best_balance = balance
                    best_mid = i

            chosen = [parts[i][1] for i in range(left, best_mid + 1)]

            if ask(centroid, chosen):
                left = best_mid + 1
            else:
                right = best_mid

        current = parts[left][1]
        current_size = parts[left][0]
        blocked[centroid] = True

    assert current == hidden
    assert queries <= 4 * ((n - 1).bit_length())
    return current, queries

# Sample 1
edges = [(1, 2), (1, 3), (1, 4), (1, 5)]
assert simulate(5, edges, 1)[0] == 1

# Sample 2
assert simulate(5, edges, 2)[0] == 2

# Minimum-size tree, hidden at the endpoint.
edges = [(1, 2)]
assert simulate(2, edges, 2)[0] == 2

# Equal-size components around a centroid.
edges = [
    (1, 2), (1, 3), (1, 4),
    (1, 5), (1, 6), (1, 7)
]
assert simulate(7, edges, 6)[0] == 6

# Long path, hidden at the boundary.
edges = [(i, i + 1) for i in range(1, 15)]
assert simulate(15, edges, 15)[0] == 15

# Maximum-size star, all components initially have equal size.
n = 200000
edges = [(1, i) for i in range(2, n + 1)]
answer, queries = simulate(n, edges, n)
assert answer == n
assert queries <= 4 * ((n - 1).bit_length())
```

The maximum-size test is intentionally a star because it stresses the large number of equal-sized components and checks that the weighted binary search does not accidentally become linear in the degree. The simulator also checks the formal query budget, which is more useful for this interactive problem than comparing a fixed output string.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 star with hidden vertex 1 | 1 | Centroid itself is the answer |
| Sample 2 star with hidden vertex 2 | 2 | Component selection after a zero centroid query |
| (2)-vertex tree, hidden vertex 2 | 2 | Minimum-size boundary case |
| Seven-vertex star, hidden vertex 6 | 6 | Equal component sizes and weighted splitting |
| Fifteen-vertex path, hidden vertex 15 | 15 | Deeply unbalanced original rooting and boundary target |
| (200,000)-vertex star, hidden vertex (200,000) | (200,000) | Maximum size and query-count limit |

## Edge Cases

For the two-vertex tree

```
2
1 2
```

the only possible centroid is either vertex. Suppose the algorithm starts at vertex 1. Its only unblocked neighbor is 2, so the first query is equivalent to asking whether vertex 2 is at least as close to the hidden vertex as vertex 1. If (u=2), the answer is 0 and the surviving component is the singleton `{2}`. The next iteration is skipped because its size is already one, and the program prints `! 2`. There is no assumption about having multiple children.

For the star

```
5
1 2
1 3
1 4
1 5
```

with (u=1), vertex 1 is the centroid and the query uses neighbors 2, 3, 4, and 5. Their distances from (u) are all 1, while the distance from (u) to the centroid is 0, so the answer is 1. The algorithm immediately prints `! 1`. This is exactly the situation represented by the first official sample.

For the same star with (u=2), the centroid query returns 0 because the queried vertex 2 has distance 0 from the hidden vertex while the centroid has distance 1. The algorithm then treats the four leaf components as four weighted candidates, each of size 1. A balanced split can ask about two leaves, receive 0 because leaf 2 is among them, and then reduce the interval to the remaining relevant candidates. Eventually only component 2 remains, so the answer is `! 2`. The official sample uses four queries to reach the same answer.

For a long path such as

```
7
1 2
2 3
3 4
4 5
5 6
6 7
```

the centroid of the whole tree is vertex 4. If the hidden vertex is 7, the first centroid query returns 0. Only the component containing 5 can contain the target, and its size is 3. Vertex 4 is then blocked, and the algorithm finds the centroid of the remaining path 5-6-7, which is 6. The same distance comparison identifies the component containing 7. The search continues until 7 is isolated. The essential point is that the centroid is recomputed after every reduction, rather than treating the original tree's root as permanent.

The maximum-degree case is a large star. Every component after removing the center has size 1, so sorting leaves all weights equal. The weighted search then behaves like ordinary binary search over the leaves, requiring only logarithmically many interactions. This is precisely the kind of tree that exposes an implementation that accidentally scans leaves one by one.

A final implementation trap is recursive DFS. A path with (200,000) vertices can create recursion depth close to (200,000), which is unsafe in Python even if the algorithm itself is correct. The submitted implementation uses explicit lists as traversal stacks, so the depth of the input tree does not affect Python's call stack.
