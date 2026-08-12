---
title: "CF 102361F - Forest Program"
description: "We have an undirected graph whose connected components are all cacti. We may choose any set of edges to remove. After the removals, every connected component must be a tree, which is equivalent to saying that the remaining graph must contain no cycle."
date: "2026-08-13T00:12:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102361
codeforces_index: "F"
codeforces_contest_name: "2019 China Collegiate Programming Contest Qinhuangdao Onsite"
rating: 0
weight: 102361
solve_time_s: 84
verified: true
draft: false
---

[CF 102361F - Forest Program](https://codeforces.com/problemset/problem/102361/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an undirected graph whose connected components are all cacti. We may choose any set of edges to remove. After the removals, every connected component must be a tree, which is equivalent to saying that the remaining graph must contain no cycle.

The useful way to look at a cactus is to separate its edges into two kinds. Some edges belong to a cycle, and every such edge belongs to exactly one cycle. The remaining edges are not part of any cycle. Because cycles in a cactus do not share edges, the decisions made for different cycles are independent.

Suppose one cycle contains (k) edges. Keeping all (k) edges would leave that cycle intact, so that single choice is forbidden. Every other subset of its edges is valid, giving

[
2^k-1
]

choices. An edge outside every cycle can either be removed or kept, giving two choices.

If the cycle lengths are (c_1,c_2,\ldots,c_t), and their total number of edges is

[
C=c_1+c_2+\cdots+c_t,
]

then the answer is

[
2^{m-C}\prod_{i=1}^{t}(2^{c_i}-1).
]

The remaining task is to find every cycle and its length efficiently.

The official problem has (n\le300000), (m\le500000), with a 1 second time limit and 1024 MB memory limit. An algorithm that repeatedly scans the whole graph for exponentially many edge subsets is completely infeasible. We need essentially linear work in the graph size, with perhaps logarithmic factors for modular exponentiation.

There are several edge cases that easily cause incorrect solutions.

For an edgeless graph,

```
1 0
```

the answer is `1`. There is exactly one possible removal set, the empty set. A solution that assumes every component contains a cycle may accidentally return zero.

For a tree with one edge,

```
2 1
1 2
```

the answer is `2`. We may keep the edge or remove it. Both resulting graphs are forests. A solution that only counts ways to break cycles may return `1`, forgetting that non-cycle edges are also independently removable.

Disconnected components must be handled separately. For

```
6 6
1 2
2 3
3 1
4 5
5 6
6 4
```

there are two independent triangles, so the answer is

[
(2^3-1)^2=7^2=49.
]

A DFS started only from vertex 1 would completely miss the second component and return `7`.

Finally, consider a cycle with a bridge attached:

```
4 4
1 2
2 3
3 1
3 4
```

The triangle contributes `7` choices and the bridge contributes `2`, so the answer is `14`. Treating every edge as though it belonged to the cycle, or ignoring non-cycle edges altogether, gives the wrong result.

## Approaches

The most direct approach is to enumerate every subset of the (m) edges. For each subset, keep the selected edges and test whether the resulting graph is acyclic. A standard DFS or DSU-based check can determine whether a cycle exists in (O(n+m)) time. Since there are (2^m) subsets, this takes

[
O(2^m(n+m))
]

time. At the maximum (m=500000), this means examining about (2^{500000}), roughly (10^{150515}), different subsets. The method is correct because it explicitly checks every possible removal scheme, but the search space is far beyond any practical limit.

The cactus structure gives us a much stronger observation. A remaining graph fails to be a forest exactly when some original cycle survives completely. Thus every original cycle only imposes one condition: at least one of its edges must be removed. For a cycle of length (k), all (2^k) subsets of its edges are possible except the one subset that removes nothing, giving (2^k-1).

Edges outside cycles impose no restriction at all. Removing such an edge cannot create a cycle, and keeping it cannot create a cycle because the edge was not part of one in the original graph. Consequently, every such edge contributes a factor of `2`.

The only graph problem left is identifying all cycle lengths. A DFS provides exactly what we need. In an undirected DFS tree, every non-tree edge connects a vertex to one of its ancestors. If the current vertex has depth (d_u) and the ancestor has depth (d_v), the tree path between them contains (d_u-d_v) edges, and the non-tree edge closes a cycle of length

[
d_u-d_v+1.
]

The cactus condition makes this especially clean. Each non-tree edge corresponds to one distinct simple cycle, so counting these back edges gives every cycle exactly once.

The brute-force method works because it checks every possible subset explicitly, but fails because the number of subsets is exponential. The cactus observation reduces the entire problem to detecting cycle lengths with one DFS and multiplying independent contributions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^m(n+m))) | (O(n+m)) | Too slow |
| DFS on cactus | (O(n+m)) | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Build the undirected graph while assigning an edge ID to every input edge. The implementation stores the graph with adjacency arrays so that an undirected edge can be distinguished from its reverse even when both endpoints have already been visited.
2. Start a DFS from every vertex whose depth has not been assigned. The graph is not necessarily connected, so one DFS from vertex `1` is insufficient.
3. Assign the starting vertex depth `0`. Whenever DFS discovers an unvisited vertex `v` from `u`, assign `depth[v] = depth[u] + 1` and remember the edge used to reach `v` as its parent edge.
4. When examining an already visited neighbor `v` of `u`, ignore the reverse of the parent edge. If `depth[v] < depth[u]`, then `v` is an ancestor of `u`, so this edge is a non-tree edge that closes a cycle.
5. Compute the cycle length as `depth[u] - depth[v] + 1`. The tree path from `v` to `u` has `depth[u] - depth[v]` edges, and the current edge adds one more.
6. Multiply the answer by (2^{k}-1), where (k) is the discovered cycle length. Also add (k) to `cycle_edges`, the number of edges that belong to cycles.
7. After the DFS finishes, exactly `m - cycle_edges` edges are outside all cycles. Each of these can independently be kept or removed, so multiply the answer by

[
2^{m-\text{cycle_edges}}.
]

1. Compute all powers of two up to `n` modulo `998244353` before the DFS. A cycle cannot contain more than `n` edges, so every factor (2^k) can then be obtained in constant time.

### Why it works

Consider any removal scheme produced by the algorithm. For every original cycle, the factor (2^k-1) chooses a subset of its edges other than the empty removed subset, so at least one edge of that cycle is removed. Since every original cycle is broken, no original cycle remains intact.

Conversely, suppose a removal scheme leaves a cycle. Every remaining edge was present in the original graph, so that cycle was also a cycle of the original cactus. The scheme would then have removed no edge from that cycle, which is precisely the one forbidden choice excluded by its (2^k-1) factor. Hence every scheme counted by the formula leaves a forest.

The DFS counts each cactus cycle once. Every non-tree edge in an undirected DFS connects a vertex with an ancestor, and the corresponding tree path plus that edge forms a cycle. Because every edge of a cactus belongs to at most one simple cycle, two such discovered cycles cannot represent the same edge cycle. Thus the collected cycle lengths account for exactly all cycle edges, and every remaining edge is genuinely outside every cycle.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n, m = map(int, input().split())

    head = [-1] * n
    to = [0] * (2 * m)
    nxt = [0] * (2 * m)

    edge_ptr = 0

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1

        to[edge_ptr] = v
        nxt[edge_ptr] = head[u]
        head[u] = edge_ptr
        edge_ptr += 1

        to[edge_ptr] = u
        nxt[edge_ptr] = head[v]
        head[v] = edge_ptr
        edge_ptr += 1

    pow2 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow2[i] = (pow2[i - 1] * 2) % MOD

    depth = [-1] * n
    parent_edge = [-1] * n
    current_edge = [-1] * n

    answer = 1
    cycle_edges = 0

    for root in range(n):
        if depth[root] != -1:
            continue

        depth[root] = 0
        parent_edge[root] = -1
        current_edge[root] = head[root]

        stack = [root]

        while stack:
            u = stack[-1]
            e = current_edge[u]

            if e == -1:
                stack.pop()
                continue

            current_edge[u] = nxt[e]

            if parent_edge[u] != -1 and e == (parent_edge[u] ^ 1):
                continue

            v = to[e]

            if depth[v] == -1:
                depth[v] = depth[u] + 1
                parent_edge[v] = e
                current_edge[v] = head[v]
                stack.append(v)
            elif depth[v] < depth[u]:
                length = depth[u] - depth[v] + 1
                cycle_edges += length
                answer = answer * (pow2[length] - 1) % MOD

    answer = answer * pow2[m - cycle_edges] % MOD
    print(answer)

if __name__ == "__main__":
    solve()
```

The adjacency structure uses `head`, `to`, and `nxt` instead of a Python list of tuples for every edge. Each input edge creates two directed adjacency entries, and the two entries have consecutive indices. That is why the reverse of a parent edge is obtained with `parent_edge[u] ^ 1`.

The DFS is iterative rather than recursive. With up to `300000` vertices, Python's default recursion depth is not sufficient for a path-shaped cactus, and increasing the recursion limit still leaves recursion overhead. The explicit `stack` avoids both problems.

`depth[v] == -1` is the unvisited condition. Once a vertex has a depth, an edge leading to a shallower vertex is treated as a back edge. Edges leading to deeper vertices are ignored because they are the reverse direction of a DFS tree edge or an already processed non-tree edge.

The expression `depth[u] - depth[v] + 1` is the exact cycle length. The `+1` is easy to miss because the depth difference counts only the tree edges, while the current non-tree edge is the final edge closing the cycle.

`cycle_edges` stores the sum of cycle lengths, not the number of cycles. Since cactus cycles are edge-disjoint, this is exactly the number of edges that are forbidden from being treated as independent bridge-like edges.

The modular arithmetic is safe in Python because integers have arbitrary precision. The explicit modulus after every multiplication keeps intermediate values small and follows the required modulus of `998244353`.

The implementation also starts DFS from every unvisited vertex. This handles isolated vertices and disconnected cactus components without any special case.

## Worked Examples

### Sample 1

The graph is a single triangle.

```
3 3
1 2
2 3
3 1
```

The DFS may choose the tree edges `1-2` and `2-3`. When it reaches the edge `3-1`, vertex `1` is an ancestor of vertex `3`, so one cycle is found.

| Current vertex | Neighbor | Depth of current | Depth of neighbor | Action | Cycle length |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 0 | -1 | Discover 2 |  |
| 2 | 3 | 1 | -1 | Discover 3 |  |
| 3 | 1 | 2 | 0 | Back edge | 3 |
| 3 | 2 | 2 | 1 | Parent edge |  |
| 2 | 1 | 1 | 0 | Parent edge |  |

The cycle contribution is

[
2^3-1=7.
]

All three edges belong to this cycle, so `cycle_edges = 3` and there are no independent non-cycle edges. The final answer is `7`.

This demonstrates the central counting rule: every subset of the triangle's edges is valid except the subset that removes nothing.

### Sample 2

The graph contains two triangles sharing vertex `2`:

```
6 6
1 2
2 3
3 1
2 4
4 5
5 2
```

A DFS tree can contain the edges `1-2`, `2-3`, `2-4`, and `4-5`. The remaining two edges close two separate cycles.

| Current vertex | Neighbor | Depth of current | Depth of neighbor | Action | Cycle length |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 0 | Tree edge |  |
| 2 | 3 | 0 | -1 | Discover 3 |  |
| 3 | 1 | 1 | 1 | Back to ancestor | 3 |
| 2 | 4 | 0 | -1 | Discover 4 |  |
| 4 | 5 | 1 | -1 | Discover 5 |  |
| 5 | 2 | 2 | 0 | Back to ancestor | 3 |

There are two cycles of length `3`, so the cycle factor is

[
(2^3-1)(2^3-1)=7\cdot7=49.
]

All six edges belong to one of these cycles, so there are no independent edges. The answer is `49`.

The two triangles sharing a vertex do not interfere with each other's choices because they share no edge. This is exactly the independence supplied by the cactus property.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+m)) | Every vertex and adjacency entry is processed a constant number of times, and powers of two are precomputed in (O(n)). |
| Space | (O(n+m)) | The adjacency arrays, DFS state, power table, and explicit stack all use linear space. |

The limits allow up to `300000` vertices and `500000` edges. The algorithm processes the graph linearly, so it avoids the exponential dependence on the number of possible edge-removal schemes. The iterative DFS also avoids Python recursion-depth failures on long tree-like components.

## Test Cases

```python
import sys
import io

MOD = 998244353

def solve_data(inp: str) -> str:
    data = inp.split()
    it = iter(data)

    n = int(next(it))
    m = int(next(it))

    head = [-1] * n
    to = [0] * (2 * m)
    nxt = [0] * (2 * m)

    ptr = 0

    for _ in range(m):
        u = int(next(it)) - 1
        v = int(next(it)) - 1

        to[ptr] = v
        nxt[ptr] = head[u]
        head[u] = ptr
        ptr += 1

        to[ptr] = u
        nxt[ptr] = head[v]
        head[v] = ptr
        ptr += 1

    pow2 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow2[i] = pow2[i - 1] * 2 % MOD

    depth = [-1] * n
    parent_edge = [-1] * n
    current_edge = [-1] * n

    answer = 1
    cycle_edges = 0

    for root in range(n):
        if depth[root] != -1:
            continue

        depth[root] = 0
        current_edge[root] = head[root]
        stack = [root]

        while stack:
            u = stack[-1]
            e = current_edge[u]

            if e == -1:
                stack.pop()
                continue

            current_edge[u] = nxt[e]

            if parent_edge[u] != -1 and e == (parent_edge[u] ^ 1):
                continue

            v = to[e]

            if depth[v] == -1:
                depth[v] = depth[u] + 1
                parent_edge[v] = e
                current_edge[v] = head[v]
                stack.append(v)
            elif depth[v] < depth[u]:
                length = depth[u] - depth[v] + 1
                cycle_edges += length
                answer = answer * (pow2[length] - 1) % MOD

    answer = answer * pow2[m - cycle_edges] % MOD
    return str(answer)

# Provided samples
assert solve_data(
    """3 3
1 2
2 3
3 1
"""
) == "7", "sample 1"

assert solve_data(
    """6 6
1 2
2 3
3 1
2 4
4 5
5 2
"""
) == "49", "sample 2"

# Minimum-size graph: one isolated vertex.
assert solve_data(
    """1 0
"""
) == "1", "minimum graph"

# A tree with four edges. Every edge is independent, so there are 2^4 schemes.
assert solve_data(
    """5 4
1 2
1 3
1 4
1 5
"""
) == "16", "tree with independent edges"

# One triangle plus one bridge.
assert solve_data(
    """4 4
1 2
2 3
3 1
3 4
"""
) == "14", "cycle plus bridge"

# Two disconnected triangles.
assert solve_data(
    """6 6
1 2
2 3
3 1
4 5
5 6
6 4
"""
) == "49", "disconnected cycles"

# Large boundary case: 300000 vertices, 149999 triangles sharing vertex 1.
# This gives 300000 vertices and 449997 edges.
n = 300000
lines = [f"{n} 449997"]
for i in range(149999):
    a = 2 + 2 * i
    b = a + 1
    lines.append(f"1 {a}")
    lines.append(f"{a} {b}")
    lines.append(f"{b} 1")

large_input = "\n".join(lines) + "\n"
expected = str(pow(7, 149999, MOD))

assert solve_data(large_input) == expected, "large cactus boundary case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | `1` | Isolated vertex and zero edges |
| Five-vertex star | `16` | Every edge is outside a cycle and can be independently removed |
| Triangle plus one bridge | `14` | Correct separation of cycle edges and non-cycle edges |
| Two disconnected triangles | `49` | Multiple connected components and independent cycle factors |
| 300000-vertex cactus with 149999 triangles | (7^{149999}\bmod998244353) | Large vertex count, many cycles, iterative DFS, and performance |

## Edge Cases

For an isolated vertex, the input is

```
1 0
```

The DFS starts at vertex `1`, assigns it depth `0`, and immediately finishes because its adjacency list is empty. No cycle is found, so `cycle_edges = 0`. The final factor is (2^0=1), giving output `1`. This correctly counts the empty removal set.

For a tree such as

```
5 4
1 2
1 3
1 4
1 5
```

every DFS edge is a tree edge, and no edge ever connects a vertex to an ancestor. Thus no cycle factor is multiplied into the answer. All four edges are outside cycles, so the final factor is (2^4=16). The algorithm correctly allows every combination of removing or keeping those edges.

For a triangle with a bridge,

```
4 4
1 2
2 3
3 1
3 4
```

DFS detects the back edge closing the triangle and obtains cycle length `3`. It adds `3` to `cycle_edges`, leaving `4-3=1` independent edge. The answer becomes

[
(2^3-1)2=7\cdot2=14.
]

The bridge can be removed even though it is not necessary for breaking the cycle, which is why its factor must remain in the formula.

For disconnected triangles,

```
6 6
1 2
2 3
3 1
4 5
5 6
6 4
```

the first DFS finds a length-three cycle, then the outer loop reaches vertex `4` and starts another DFS because it is still unvisited. The second DFS finds the second length-three cycle. The resulting product is (7\cdot7=49). This demonstrates why the outer loop over all vertices is necessary.

For a large cactus containing many short cycles, the explicit stack prevents recursion depth problems. In the test with 149999 triangles, every cycle contributes the factor `7`, so the answer is (7^{149999}) modulo `998244353`. The DFS still processes each of the roughly 450000 edges only a constant number of times, preserving the linear complexity.
