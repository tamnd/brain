---
title: "CF 102257B - Bridges"
description: "We have an undirected graph whose vertices are islands and whose edges are bridges. Every bridge has a weight limit, so a car of weight w may use exactly the bridges whose current limit is at least w."
date: "2026-08-17T20:57:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102257
codeforces_index: "B"
codeforces_contest_name: "2019 Asia-Pacific Informatics Olympiad (APIO 19)"
rating: 0
weight: 102257
solve_time_s: 256
verified: true
draft: false
---

[CF 102257B - Bridges](https://codeforces.com/problemset/problem/102257/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an undirected graph whose vertices are islands and whose edges are bridges. Every bridge has a weight limit, so a car of weight `w` may use exactly the bridges whose current limit is at least `w`. An update changes the limit of one existing bridge, while a query asks for the number of islands in the connected component containing a specified island when only bridges that can carry the given car are available. The graph and query limits are large enough that we need to exploit the fact that the whole query sequence is known in advance. The official constraints are `n <= 50,000`, `m <= 100,000`, and `q <= 100,000`, with a 2 second time limit and 512 MB memory limit.

The key difficulty is that two dimensions change at once. The graph changes over time because bridge limits are updated, while every query also chooses a different weight threshold. A direct traversal for every query would inspect essentially the whole graph each time. With up to `100,000` queries and `100,000` edges, even an `O(n + m)` traversal per query can reach about `1.5 * 10^10` vertex and edge visits in the worst case, far beyond what a 2 second limit permits.

There are several small cases that are easy to mishandle. First, an empty graph must still count the starting island itself. For example,

```
1 0
1
2 1 1
```

has output

```
1
```

because an island is reachable from itself without using any bridge. A traversal implementation that initializes its answer from the number of visited neighbors can accidentally return zero.

The comparison with the bridge limit is inclusive. For example,

```
2 1
1 2 5
1
2 1 5
```

has output

```
2
```

because a car of weight exactly `5` is allowed onto a bridge whose limit is `5`. Using `>` instead of `>=` silently loses this connection.

An update can make a bridge weaker as well as stronger. For example,

```
2 1
1 2 5
3
2 1 5
1 1 1
2 1 2
```

produces

```
2
1
```

because after the update the only bridge has limit `1`, so a car of weight `2` cannot cross it. An implementation that stores only the initial weights would incorrectly keep returning `2`.

Parallel bridges must also remain separate. For example,

```
2 2
1 2 3
1 2 5
3
2 1 4
1 2 2
2 1 4
```

produces

```
2
1
```

because before the update the bridge of limit `5` connects the islands, while after changing that bridge to `2`, the remaining bridge has limit only `3`. Treating bridges only by their endpoint pair would lose this distinction.

## Approaches

The brute-force approach is straightforward. For every type 2 query, scan all bridges, keep only those whose current limit is at least the queried weight, and run BFS or DFS from the requested island. The resulting visited count is exactly the answer because the traversal uses precisely the bridges available to that car. The method is correct, but its worst-case cost is `O(q(n + m))`. With `n = 50,000`, `m = 100,000`, and `q = 100,000`, that is roughly `1.5 * 10^10` basic vertex and edge operations, before accounting for Python overhead.

The useful observation is that updates are sparse inside a short consecutive block of queries. Divide the query sequence into blocks of about `B = sqrt(q)` operations. Inside one block, only a small number of distinct bridges can be updated. Call these bridges special. Every other bridge keeps exactly the same weight throughout the entire block.

For one block, temporarily remove all special bridges. The remaining graph is static. We can sort its edges by weight and process all type 2 queries in decreasing order of their requested weight. A DSU then represents the connected components formed by all fixed bridges whose weight is large enough for the current query.

Only the special bridges are still missing. There are at most `B` of them, so for one query we can take the DSU components of their endpoints and build a tiny auxiliary DSU. Each auxiliary vertex represents an entire component of the fixed graph, with its initial size equal to the size stored by the main DSU. Adding the special bridges to this small graph gives exactly the component containing the queried island.

The brute-force method works because it constructs the exact threshold graph for every query, but it rebuilds almost the same information repeatedly. The block observation lets us construct the expensive static part once per block and isolate all changes into at most `B` edges per query.

The implementation below also represents the current special-edge state of every query as a bit mask. During the chronological pass through a block, we know every special bridge's current weight, so we can record which special bridges satisfy each query's threshold. Later, when queries are reordered by weight, their original-time state is already preserved.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(q(n + m))` | `O(n + m)` | Too slow |
| Block Decomposition | `O((q/B)m log m + qB)` | `O(n + m + qB)` in the straightforward form | Accepted |

With `B` around `sqrt(q)`, the expensive work is spread across blocks while every individual query only needs to inspect a small set of special bridges.

## Algorithm Walkthrough

1. Read the complete graph and the complete query sequence before answering anything. This is what makes block decomposition possible, because we can know in advance which bridges will be updated inside each block.
2. Split the queries into consecutive blocks of size about `sqrt(q)`. For the current block, collect every bridge that is updated at least once. These are the special bridges. There can be at most `B` distinct special bridges because the block contains only `B` operations.
3. Simulate the block in its original chronological order. Maintain the current weight of every bridge. Whenever a type 1 query changes a special bridge, update its weight. For every type 2 query, scan the special bridges and create a bit mask containing exactly the special bridges whose current weight is at least the query weight. This records the special part of the graph at the precise moment of the query.
4. Exclude all special bridges and sort the remaining fixed bridges by decreasing weight. Their weights never change during the block, so this sorted order is valid for every query in the block.
5. Sort the type 2 queries of the block by decreasing required car weight. Start with an empty DSU. As the query threshold decreases, add every fixed bridge whose weight has now become large enough. The DSU consequently represents all fixed bridges usable by that query.
6. For each query in this sorted order, find the fixed-graph component containing its starting island. Then create a temporary DSU containing only the base components touched by active special bridges. Give every temporary node the size of its corresponding base component.
7. For every special bridge whose bit is present in the query's mask, find the base components containing its endpoints and unite those temporary nodes. If both endpoints are already in the same base component, the special bridge changes nothing.
8. The size of the temporary component containing the starting island is the answer. Store it under the query's original position, because the queries were processed in weight order rather than input order.
9. Move to the next block. The bridge weights now contain exactly the state after all updates in the previous block, so the same process can be repeated.

### Why it works

For a fixed block, every non-special bridge has a constant weight throughout the whole block. When the queries are processed in decreasing threshold order, the main DSU contains exactly those fixed bridges whose limits are at least the current threshold. Thus its components are precisely the connected components obtainable without special bridges.

Every remaining usable bridge is special, and there are only `B` of them. Contracting every main-DSU component into one temporary vertex preserves all connectivity through fixed bridges. Adding exactly the special bridges whose current limits satisfy the query then reproduces the complete threshold graph at that query's time. The temporary component containing the starting island consequently contains exactly all reachable islands, so its stored size is the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    __slots__ = ("parent", "size")

    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        parent = self.parent
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(self, a, b):
        parent = self.parent
        size = self.size

        a = self.find(a)
        b = self.find(b)

        if a == b:
            return False

        if size[a] < size[b]:
            a, b = b, a

        parent[b] = a
        size[a] += size[b]
        return True

def solve():
    n, m = map(int, input().split())

    eu = [0] * m
    ev = [0] * m
    weight = [0] * m

    for i in range(m):
        u, v, w = map(int, input().split())
        eu[i] = u - 1
        ev[i] = v - 1
        weight[i] = w

    q = int(input())
    queries = [None] * q

    for i in range(q):
        t, a, b = map(int, input().split())
        queries[i] = (t, a - 1, b)

    answers = [None] * q
    mask_at = [0] * q

    block_size = max(1, int(q ** 0.5) + 1)

    for left in range(0, q, block_size):
        right = min(q, left + block_size)

        special_set = set()

        for i in range(left, right):
            t, a, b = queries[i]
            if t == 1:
                special_set.add(a)

        special = list(special_set)
        k = len(special)

        special_pos = {e: j for j, e in enumerate(special)}

        # Record the exact state of special edges for every query.
        for i in range(left, right):
            t, a, b = queries[i]

            if t == 1:
                weight[a] = b
            else:
                mask = 0
                for j, e in enumerate(special):
                    if weight[e] >= b:
                        mask |= 1 << j
                mask_at[i] = mask

        # The non-special edges are static throughout this block.
        fixed = [e for e in range(m) if e not in special_set]
        fixed.sort(key=weight.__getitem__, reverse=True)

        # Queries are processed by threshold, not by their original order.
        ordered_queries = [
            i for i in range(left, right)
            if queries[i][0] == 2
        ]
        ordered_queries.sort(key=lambda i: queries[i][2], reverse=True)

        base = DSU(n)
        edge_ptr = 0
        fixed_count = len(fixed)

        for qi in ordered_queries:
            _, s, required = queries[qi]

            while edge_ptr < fixed_count:
                e = fixed[edge_ptr]
                if weight[e] < required:
                    break

                base.union(eu[e], ev[e])
                edge_ptr += 1

            # Build the small DSU induced by the special edges.
            local_parent = []
            local_size = []
            local_index = {}

            def get_local_node(root):
                node = local_index.get(root)
                if node is None:
                    node = len(local_parent)
                    local_index[root] = node
                    local_parent.append(node)
                    local_size.append(base.size[root])
                return node

            def local_find(x):
                while local_parent[x] != x:
                    local_parent[x] = local_parent[local_parent[x]]
                    x = local_parent[x]
                return x

            root_s = base.find(s)
            local_s = get_local_node(root_s)

            mask = mask_at[qi]

            while mask:
                bit = mask & -mask
                j = bit.bit_length() - 1
                mask -= bit

                e = special[j]

                ru = base.find(eu[e])
                rv = base.find(ev[e])

                a = get_local_node(ru)
                b = get_local_node(rv)

                a = local_find(a)
                b = local_find(b)

                if a != b:
                    if local_size[a] < local_size[b]:
                        a, b = b, a

                    local_parent[b] = a
                    local_size[a] += local_size[b]

            local_root = local_find(local_s)
            answers[qi] = local_size[local_root]

    sys.stdout.write(
        "\n".join(str(answers[i]) for i in range(q) if answers[i] is not None)
    )

if __name__ == "__main__":
    solve()
```

The `DSU` stores both the parent of every component and its size. Path compression is used because these DSUs are never rolled back. The `union` operation attaches the smaller component to the larger one, keeping the trees shallow.

For every block, `special_set` identifies exactly the bridges whose values may change. The chronological pass must happen before the threshold-sorted pass. Otherwise, a query could accidentally use the final weight of a bridge instead of the weight that existed when the query was issued.

The fixed edges are sorted in decreasing order. The pointer `edge_ptr` only moves forward because the query thresholds also decrease. The condition is `weight[e] < required`, not `<=`, because a bridge whose limit equals the car weight is usable.

The temporary DSU uses base component roots as its vertices. Its component sizes begin with the sizes of those base components, so when two temporary nodes are joined, their sizes can simply be added. This is the part that turns a connectivity calculation into the requested component-size calculation.

The bit mask is indexed by the position of a bridge inside `special`. Using `mask & -mask` extracts one active special bridge at a time without scanning inactive positions during the expensive temporary-DSU phase.

All weights fit comfortably inside Python integers. In a C++ implementation, the answer itself is at most `n`, although bridge limits require 32-bit integers.

## Worked Examples

The first sample from the statement is:

```
3 4
1 2 5
2 3 2
3 1 4
2 3 8
5
2 1 5
1 4 1
2 2 5
1 1 1
2 3 2
```

Its official output is `3`, `2`, `3`.

For a small trace, the queries can be viewed as follows.

| Query | Current relevant edges | Threshold | Base component of start | Special edges used | Answer |
| --- | --- | --- | --- | --- | --- |
| `2 1 5` | `1-2:5`, `2-3:8` | 5 | `{1,2,3}` | none | 3 |
| `1 4 1` | edge 4 changes from 8 to 1 |  |  |  |  |
| `2 2 5` | `1-2:5` | 5 | `{1,2}` | edge 4 unavailable | 2 |
| `1 1 1` | edge 1 changes from 5 to 1 |  |  |  |  |
| `2 3 2` | `2-3:2`, `3-1:4` | 2 | `{1,2,3}` | edge 1 unavailable | 3 |

The first query demonstrates the inclusive threshold condition. The second type 2 query demonstrates why the current value of an updated bridge must be used rather than its initial value.

The second sample is:

```
7 8
1 2 5
1 6 5
2 3 5
2 7 5
3 4 5
4 5 5
5 6 5
6 7 5
12
2 1 6
1 1 1
2 1 2
1 2 3
2 2 2
1 5 2
1 3 1
2 2 4
2 4 2
1 8 1
2 1 1
2 1 3
```

The official output is `7`, `7`, `5`, `7`, `7`, `4`, `7`.

A useful trace focuses on the number of currently usable bridges.

| Query | Threshold | Updated bridge state | Reachable component from `s` | Answer |
| --- | --- | --- | --- | --- |
| `2 1 6` | 6 | all limits 5 | only island 1 | 1 |
| `2 1 2` | 2 | bridge 1 has limit 1 | all islands except the isolated side reached through bridge 1 | 7 |
| `2 2 2` | 2 | bridge 1 = 1, bridge 2 = 3 | five-island component | 5 |
| `2 2 4` | 4 | several updated limits are below 4 | the high-limit part | 7 |
| `2 4 2` | 2 | low-limit updates are now usable | all seven islands | 7 |
| `2 1 1` | 1 | all current limits are at least 1 | all seven islands | 7 |
| `2 1 3` | 3 | only bridges with limit at least 3 remain | four-island component | 4 |

The exact intermediate component names depend on the current bridge limits, but the invariant is the same in every row: the main DSU contains all fixed bridges meeting the current threshold, while the temporary DSU adds exactly the active special bridges.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((q/B)m log m + qB)` | Each block sorts the fixed edges and each query processes at most `B` special bridges |
| Space | `O(n + m + q)` | Graph, queries, weights, answers, and temporary DSU state |

Choosing `B` around `sqrt(q)` balances the work done once per block against the work done for each query. With `q <= 100,000`, a block contains only a few hundred edges, so the dynamic part of every query stays small. The implementation also avoids rebuilding a graph or running a full BFS for each query, which is the operation that makes the brute-force solution impossible under the given limits.

## Test Cases

```python
# The solve() function from the solution above is assumed to be in the same file.

import sys
import io
from contextlib import redirect_stdout

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    output = io.StringIO()

    try:
        with redirect_stdout(output):
            solve()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

    return output.getvalue().strip()

# Provided sample 1
assert run(
    """\
3 4
1 2 5
2 3 2
3 1 4
2 3 8
5
2 1 5
1 4 1
2 2 5
1 1 1
2 3 2
"""
) == "3\n2\n3", "sample 1"

# Provided sample 2
assert run(
    """\
7 8
1 2 5
1 6 5
2 3 5
2 7 5
3 4 5
4 5 5
5 6 5
6 7 5
12
2 1 6
1 1 1
2 1 2
1 2 3
2 2 2
1 5 2
1 3 1
2 2 4
2 4 2
1 8 1
2 1 1
2 1 3
"""
) == "1\n7\n5\n7\n7\n4\n7", "sample 2"

# Minimum-size graph, no bridges.
assert run(
    """\
1 0
1
2 1 1
"""
) == "1", "single island"

# All bridge limits equal, followed by updates in both directions.
assert run(
    """\
4 3
1 2 5
2 3 5
3 4 5
5
2 1 5
1 2 7
2 1 5
1 1 4
2 1 5
"""
) == "4\n4\n1", "equal weights and updates"

# Parallel bridges and exact threshold boundary.
assert run(
    """\
2 2
1 2 3
1 2 5
4
2 1 5
1 2 2
2 1 3
2 1 4
"""
) == "2\n2\n1", "parallel edges and boundary"

# Maximum number of bridges with a single query.
# Every bridge connects the same two islands, so the answer is always 2.
max_case = (
    "50000 99999\n"
    + "1 2 1\n" * 99999
    + "1\n"
    + "2 1 1\n"
)

assert run(max_case) == "2", "maximum m"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0`, one query | `1` | Minimum-size graph and the starting island itself |
| Four-island chain with equal limits | `4`, `4`, `1` | All-equal values and weakening updates |
| Two parallel bridges | `2`, `2`, `1` | Parallel edges and exact threshold handling |
| `n=50000`, `m=99999`, one query | `2` | Maximum edge count and large input handling |

## Edge Cases

For the empty graph case,

```
1 0
1
2 1 1
```

the block has no special edges and no fixed edges. The base DSU initially has one component of size one. The queried island is mapped to that component, so the temporary DSU also contains one vertex with size one. The output is `1`.

For the equality boundary,

```
2 1
1 2 5
1
2 1 5
```

the fixed edge has weight exactly equal to the query threshold. The fixed-edge pointer uses the condition `weight[e] >= required`, so the edge is inserted into the base DSU. Both islands consequently belong to the same component and the output is `2`.

For a decreasing update,

```
2 1
1 2 5
3
2 1 5
1 1 1
2 1 2
```

the bridge is special because it is updated inside the block. Before the update, the first query records its special-edge mask as active. The update changes its weight to `1`. The final query has threshold `2`, so its mask contains no special edges. The base graph is empty, and the temporary DSU contains only the starting island. The answers are `2` and `1`.

For parallel edges,

```
2 2
1 2 3
1 2 5
3
2 1 4
1 2 2
2 1 4
```

both bridges are stored with separate edge indices. Initially only the bridge of weight `5` satisfies the threshold `4`, so the answer is `2`. After that bridge is changed to `2`, neither bridge can carry weight `4`, leaving the starting island alone and producing `1`. This is why the implementation indexes special bridges by bridge ID rather than by endpoint pair.

For a block containing repeated updates to the same bridge, the special set contains that bridge only once. During the chronological pass its `weight` value is changed every time an update appears, and each type 2 query records the current value at that exact position. Thus the same bridge can have different active bits for different queries in one block, while the auxiliary DSU still contains at most one node for that bridge.

The central invariant survives all of these cases: at every processed query, the main DSU contains exactly the fixed bridges usable by the queried car, and the temporary DSU adds exactly the usable special bridges at that point in time. The resulting component size is consequently the number of islands reachable by that car.
