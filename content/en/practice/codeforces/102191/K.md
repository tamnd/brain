---
title: "CF 102191K - Cactus Portal"
description: "The graph is a weighted chain of simple cycles. Starting from vertex 1 and moving toward vertex n, every cycle behaves like a choice between two arcs connecting the same two articulation vertices. Apart from those cycles, the graph contains ordinary chain edges."
date: "2026-08-18T09:41:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102191
codeforces_index: "K"
codeforces_contest_name: "PSUT Coding Marathon 2019"
rating: 0
weight: 102191
solve_time_s: 1129
verified: false
draft: false
---

[CF 102191K - Cactus Portal](https://codeforces.com/problemset/problem/102191/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 18m 49s  
**Verified:** no  

## Solution
## Problem Understanding

The graph is a weighted chain of simple cycles. Starting from vertex 1 and moving toward vertex n, every cycle behaves like a choice between two arcs connecting the same two articulation vertices. Apart from those cycles, the graph contains ordinary chain edges. Because no two cycles share a vertex, these choices occur independently in sequence.

We need to make a round trip from 1 to n and back to 1. At some vertex u on the outward trip, we may start a portal timer. We then have at most k seconds of actual walking before reaching another vertex v and activating the portal. Once activated, moving between u and v costs zero. The portal can be used during the return trip, so after reaching n we can return to v normally and then teleport from v back to u.

Suppose the chosen simple path from 1 to n contains u before v. Let P be the distance from 1 to u along this path, D the distance from u to v, and Q the distance from v to n. The complete trip costs

[
P+D+Q+Q+0+P=2P+D+2Q.
]

The only restriction on the portal is D <= k.

The input contains n vertices and e weighted edges. With n as large as 300000 and a two second limit, an algorithm that examines every pair of vertices is far too slow. Even O(n sqrt n) would be questionable in Python, so the intended solution needs to stay essentially linear apart from logarithmic data structure operations. The edge weights are positive and at most 1000, while k can be as large as 10^8, so we must work with exact integer distances rather than bounded-state dynamic programming over k.

There are several easy cases that can fool an implementation.

The first is that v does not have to be n. For example,

```
2 1 4
1 2 2
```

has answer 2. We can start the portal at vertex 1, walk to vertex 2, activate it, return through the portal, and finish at vertex 1. More generally, on a longer chain we can reach n after activating the portal and use it only on the final return. An implementation that only considers pairs ending at n misses valid solutions.

The second is that the best pair can lie inside a cycle and can use either of its two arcs. Consider

```
5 5 4
1 2 1
2 3 4
3 4 4
4 2 7
4 5 1
```

The ordinary shortest path uses the edge 2-4 of weight 7, giving a round trip of 18. The other arc from 2 to 4 has two edges of weight 4. We can start at 2, walk to 3 in 4 seconds, continue from 3 to 4 and then to 5, return to 4 and 3, and finally use the portal from 3 to 2. The total is 16. A solution that replaces every cycle by only its shortest arc would miss this possibility.

The third is the timeout boundary. With

```
2 1 4
1 2 5
```

the answer is 10, not 5, because the only possible portal activation requires walking 5 seconds while k is only 4. Using `<= k` instead of `< k` is also essential. If k were 5, the answer would become 5.

## Approaches

A direct solution would choose the first endpoint u, choose the second endpoint v, find a simple path from 1 through u and v to n, and evaluate the corresponding round trip. There are O(n^2) pairs, and even though distances inside a cactus can be computed efficiently, explicitly checking every pair gives O(n^2) work. With n = 300000, that is about 9 * 10^10 pair checks, which is completely infeasible.

The useful observation is that the graph is not an arbitrary cactus. Its cycles form a chain. We can walk from 1 to n and regard the graph as a sequence of blocks, where each block is either one ordinary edge or one cycle. For every cycle, the path from its left articulation vertex to its right articulation vertex chooses exactly one of its two arcs.

For a fixed choice of path, suppose the portal endpoints are u and v. The cost is

[
2P+D+2Q.
]

The graph structure lets us separate this expression into a contribution belonging to u, a contribution belonging to v, and a distance constraint between them.

Assume u is in an earlier block and v is in a later block. When we reach the left articulation vertex of v's block, let d be the distance from u to that articulation along the chosen path. Then the activation distance is d+a, where a is the distance from that articulation to v inside the current block. The cost becomes

[
(2P+d)+(a+2Q+2b),
]

where b is the remaining distance from v to the right articulation of its block.

The first parenthesized term belongs entirely to the previous endpoint. As we move from one block to the next, every old candidate's distance to the current frontier increases by exactly the shortest length of the block we just crossed. That means every candidate can be represented by a fixed transformed coordinate, while the current frontier contributes the same additive offset to every candidate.

This turns the problem into prefix minimum queries. For every possible first endpoint state we store a coordinate called `base` and a value called `value`. For the current second endpoint we get a threshold on `base`, and need the minimum stored value whose coordinate is at most that threshold. A Fenwick tree storing prefix minima provides exactly that operation.

A cycle needs one additional detail. An interior vertex can belong to either of the two possible simple paths through that cycle, so it has two states, one for each arc. The two articulation vertices only need their shortest-path states for cross-block transitions. Pairs whose two endpoints lie inside the same block are handled separately by a sliding window over the edges of each arc.

The brute force works because every pair can be evaluated independently. It fails because there are quadratically many pairs. The observation that the graph is a sequence of independent edge and cycle blocks lets us sweep from left to right, keeping every previous endpoint in one prefix-minimum structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n + e) | Too slow |
| Optimal | O(n log n + e) | O(n + e) | Accepted |

## Algorithm Walkthrough

1. Decompose the graph while walking from vertex 1 toward vertex n. Every ordinary degree-2 section is an edge block. Whenever a degree-3 vertex is reached, the two edges that are not the incoming chain edge are the two directions around a cycle. Traverse both directions until they meet at the next degree-3 articulation vertex. This gives the two arcs of the cycle.

In this graph family, cycle articulation vertices have degree 3, ordinary chain vertices and cycle interior vertices have degree 2, and vertices 1 and n have degree 1. That makes the decomposition possible without a general-purpose block-cut tree.
2. For every block, compute its shortest left-to-right length. For an ordinary edge this is simply its weight. For a cycle with arc lengths L1 and L2, the shortest block length is min(L1,L2). Let these lengths be S0, S1, ..., S(m-1).
3. Compute the shortest possible 1-to-n distance

[
T=\sum_i S_i.
]

Without a useful portal, the answer is 2T. We initialize the answer with this value.
4. Give each vertex inside a block one or two path states. A state is represented by `(a, b)`, where a is the distance from the block's left articulation to the vertex along the selected arc, and b is the distance from the vertex to the block's right articulation along the same arc.

For an ordinary edge of length S, the two articulation states are `(0,S)` and `(S,0)`. For a cycle, we again include `(0,S)` and `(S,0)` for the articulation vertices, where S is the shortest cycle length. Every interior vertex gets one state from each of the two arcs.
5. Let F be the shortest distance from vertex 1 to the left articulation of the current block. After crossing the current block by its shortest route, the new frontier distance is `F + S`.

For a state `(a,b)` used as the first portal endpoint, its prefix distance from 1 is `F+a`. Once we leave its block through the chosen arc, its distance to the current frontier is `b` plus all shortest intermediate blocks.
6. When a first endpoint state is moved from its own block to the next frontier, define

[
base=b-(F+S).
]

At a later block whose frontier distance is F', the actual distance from this endpoint to the frontier is

[
base+F'.
]

Its associated cost contribution is

[
2(F+a)+(base+F').
]

Rearranging gives

[
\left(2(F+a)+base\right)+F'.
]

The second term is common to every candidate at the current frontier. We therefore store `2(F+a)+base` in a Fenwick tree indexed by `base`.
7. For a current second endpoint state `(a,b)`, the distance from an earlier first endpoint to it is `base + F + a`. The portal is usable exactly when

[
base \le k-F-a.
]

We query the Fenwick tree for the minimum stored value over all coordinates satisfying this inequality. If that minimum is M, the complete round trip has cost

[
M+F+a+2(b+Q),
]

where Q is the shortest distance from the current block's right articulation to n.
8. Process all second-endpoint states of the current block before inserting the current block's states into the Fenwick tree. This ordering is what prevents an endpoint from being used as if it were strictly earlier when both endpoints actually belong to the same block.
9. Handle pairs inside the same block separately. For an ordinary edge, the only possible positive segment has length equal to that edge.

For a cycle, process each of its two arcs independently. Along one arc, the distance between two vertices is the sum of a consecutive interval of edge weights. Because all weights are positive, a two-pointer window finds the maximum interval whose total is at most k. If that maximum usable segment has length D and the chosen arc has length L, the full path through this block has length `F + L + Q`, so the resulting round trip is

[
2(F+L+Q)-D.
]
10. Coordinate-compress every `base` value before the sweep. The Fenwick tree stores minimum values rather than sums, so an update replaces a position only when the new value is smaller.

### Why it works

Every valid simple 1-to-n route chooses exactly one arc in every cycle. If the two portal endpoints lie in different blocks, the route between them consists of the remaining part of the first endpoint's chosen arc, the shortest route through all completely crossed blocks, and the beginning of the second endpoint's chosen arc. The transformed `base` value captures precisely the part of this distance that remains fixed while the sweep advances. The Fenwick query considers exactly those earlier states whose total activation distance is at most k, and among them chooses the minimum possible round-trip contribution.

If both endpoints lie in the same block, they must lie on the same selected arc of that block. The sliding window examines every consecutive vertex interval on each arc and keeps the longest interval whose length is at most k. Since the portal saves exactly that interval's length from the ordinary round trip, the formula `2(F+L+Q)-D` evaluates every same-block possibility.

Thus every valid portal placement is considered either by a cross-block Fenwick query or by a same-block sliding window, while every generated candidate corresponds to a valid simple path. Taking the minimum together with the no-portal baseline gives the optimum.

## Python Solution

```python
import sys
from bisect import bisect_left, bisect_right
from array import array

input = sys.stdin.readline

def solve():
    n, e, k = map(int, input().split())
    n0 = n - 1

    # Edge data. Using arrays keeps the graph representation compact.
    eu = array('i')
    ev = array('i')
    ew = array('i')

    # Each adjacency entry is an edge id.
    adj = [[] for _ in range(n)]

    for eid in range(e):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        eu.append(u)
        ev.append(v)
        ew.append(w)
        adj[u].append(eid)
        adj[v].append(eid)

    def other(eid, x):
        u = eu[eid]
        v = ev[eid]
        return v if u == x else u

    # Walk one direction around a cycle starting with first_eid.
    # The cycle is guaranteed to meet the chain again at a degree-3 vertex.
    def walk_cycle(start, first_eid):
        arc = []
        cur = start
        pe = first_eid

        while True:
            arc.append(pe)

            if eu[pe] == cur:
                nxt = ev[pe]
            else:
                nxt = eu[pe]

            if nxt != start and len(adj[nxt]) == 3:
                return arc, nxt

            # Every non-terminal vertex inside a cycle has degree 2.
            e0 = adj[nxt][0]
            e1 = adj[nxt][1]
            ne = e1 if e0 == pe else e0

            cur = nxt
            pe = ne

    # Blocks are:
    # (0, edge_id, edge_length)
    # (1, arc1_edge_ids, arc2_edge_ids, arc1_length, arc2_length)
    blocks = []

    cur = 0
    prev_eid = -1

    while cur != n0:
        deg = len(adj[cur])

        if deg == 2:
            e0 = adj[cur][0]
            e1 = adj[cur][1]
            eid = e1 if e0 == prev_eid else e0

            nxt = other(eid, cur)
            blocks.append((0, eid, ew[eid]))

            prev_eid = eid
            cur = nxt
            continue

        # At a degree-3 vertex, prev_eid is the incoming chain edge.
        starts = []
        for eid in adj[cur]:
            if eid != prev_eid:
                starts.append(eid)

        arc1, end1 = walk_cycle(cur, starts[0])
        arc2, end2 = walk_cycle(cur, starts[1])

        # Both arcs must reach the same right articulation vertex.
        end = end1

        len1 = 0
        for eid in arc1:
            len1 += ew[eid]

        len2 = 0
        for eid in arc2:
            len2 += ew[eid]

        blocks.append((1, arc1, arc2, len1, len2))

        # Leave the cycle through its unique non-cycle edge.
        cycle_edges = set(arc1)
        cycle_edges.update(arc2)

        out_eid = -1
        for eid in adj[end]:
            if eid not in cycle_edges:
                out_eid = eid
                break

        # The chain edge after the cycle is a separate block.
        nxt = other(out_eid, end)
        blocks.append((0, out_eid, ew[out_eid]))

        prev_eid = out_eid
        cur = nxt

    m = len(blocks)

    # Shortest left-to-right length of every block.
    shortest = [0] * m
    total = 0

    for i, block in enumerate(blocks):
        if block[0] == 0:
            s = block[2]
        else:
            s = block[3]
            if block[4] < s:
                s = block[4]

        shortest[i] = s
        total += s

    # Yield all path states (a, b) for a block.
    # a = distance from left articulation to endpoint
    # b = distance from endpoint to right articulation
    def states(block, s):
        if block[0] == 0:
            yield 0, s
            yield s, 0
            return

        arc1, arc2, len1, len2 = block[1], block[2], block[3], block[4]

        # Articulation states use the shortest way through the cycle.
        yield 0, s
        yield s, 0

        cur_dist = 0
        for j in range(len(arc1) - 1):
            cur_dist += ew[arc1[j]]
            yield cur_dist, len1 - cur_dist

        cur_dist = 0
        for j in range(len(arc2) - 1):
            cur_dist += ew[arc2[j]]
            yield cur_dist, len2 - cur_dist

    # Collect all transformed coordinates for coordinate compression.
    bases = []
    F = 0

    for i, block in enumerate(blocks):
        s = shortest[i]
        after = F + s

        for a, b in states(block, s):
            bases.append(b - after)

        F = after

    bases.sort()

    INF = 10**30
    size = len(bases)
    bit = [INF] * (size + 1)

    def update(pos, value):
        while pos <= size:
            if value < bit[pos]:
                bit[pos] = value
            pos += pos & -pos

    def query(pos):
        result = INF
        while pos > 0:
            value = bit[pos]
            if value < result:
                result = value
            pos -= pos & -pos
        return result

    answer = 2 * total
    F = 0

    for i, block in enumerate(blocks):
        s = shortest[i]
        after = F + s
        Q = total - after

        # First handle both endpoints inside this block.
        if block[0] == 0:
            w = block[2]
            if w <= k:
                candidate = 2 * (F + w + Q) - w
                if candidate < answer:
                    answer = candidate
        else:
            arc1 = block[1]
            arc2 = block[2]
            len1 = block[3]
            len2 = block[4]

            for arc, length in ((arc1, len1), (arc2, len2)):
                left = 0
                window = 0
                best = 0

                for right in range(len(arc)):
                    window += ew[arc[right]]

                    while window > k:
                        window -= ew[arc[left]]
                        left += 1

                    if window > best:
                        best = window

                if best > 0:
                    candidate = 2 * (F + length + Q) - best
                    if candidate < answer:
                        answer = candidate

        # Query all previous blocks as possible first endpoints.
        for a, b in states(block, s):
            threshold = k - F - a
            pos = bisect_right(bases, threshold)

            if pos == 0:
                continue

            best = query(pos)
            if best == INF:
                continue

            candidate = best + F + a + 2 * (b + Q)
            if candidate < answer:
                answer = candidate

        # Only after all queries do current states become previous states.
        for a, b in states(block, s):
            base = b - after
            pos = bisect_left(bases, base) + 1
            value = 2 * (F + a) + base
            update(pos, value)

        F = after

    print(answer)

if __name__ == "__main__":
    solve()
```

The graph representation stores every undirected edge once in three compact arrays and keeps only edge IDs in the adjacency lists. This avoids storing two complete endpoint-weight tuples for every adjacency entry.

The first traversal constructs the block chain directly from the degree pattern. At a degree-2 vertex there is only one edge that does not lead back to the previous vertex, so that edge is the next chain block. At a degree-3 vertex, the incoming chain edge is known, leaving exactly two cycle edges. Traversing those two edges independently recovers the two cycle arcs.

The `states` generator is the central representation of a possible portal endpoint. An interior cycle vertex occurs once on each arc, so it receives two states. The articulation vertices receive only their shortest-block states for cross-block transitions. Same-block transitions are handled separately, which is why the longer articulation states are unnecessary there.

The transformed coordinate `base = b - after` is the key to the Fenwick sweep. At a later block with frontier distance F, the actual distance from that endpoint to the frontier is `base + F`. The timeout condition consequently becomes a simple prefix condition on `base`.

The Fenwick tree stores minima. Its update operation performs a standard point update, while its query returns the minimum value over every compressed coordinate up to a specified threshold. The use of `bisect_right` is deliberate because a portal distance exactly equal to k is legal.

All distances can reach roughly 3 * 10^8, and intermediate expressions are also comfortably within Python integers. No special overflow handling is needed.

## Worked Examples

### Sample 1

The graph decomposes into the following blocks when moving from 1 to 12:

| Block | Structure | Shortest length |
| --- | --- | --- |
| 1 | Edge 1-2 | 2 |
| 2 | Cycle 2 to 4, arcs 2-5-4 and 2-3-4 | 6 |
| 3 | Edge 4-6 | 2 |
| 4 | Edge 6-10 | 3 |
| 5 | Cycle 10 to 9, arcs 10-9 and 10-11-7-8-9 | 2 |
| 6 | Edge 9-12 | 4 |

The shortest 1-to-12 path therefore has length

[
2+6+2+3+2+4=19,
]

so without a portal the cost is 38.

The optimal first endpoint is vertex 5. On the first cycle it uses the arc 2-5-4, so its distance from 1 is 2+3=5. From vertex 5 to the left articulation of the final block, vertex 9, the distance is 3+2+3+2=10. The final edge from 9 to 12 contributes another 4 seconds, giving a portal activation distance of 14.

| Variable | Value |
| --- | --- |
| First endpoint u | 5 |
| Distance 1 to u | 5 |
| Distance u to frontier 9 | 10 |
| Distance 9 to v = 12 | 4 |
| Activation distance | 14 |
| Total | 5 + 14 + 5 = 24 |

The Fenwick query accepts this candidate because 14 <= k = 14. The resulting answer is 24, matching the sample.

### Custom cycle example

Consider

```
5 5 4
1 2 1
2 3 4
3 4 4
4 2 7
4 5 1
```

The cycle between 2 and 4 has two arcs of lengths 8 and 7. The ordinary shortest path chooses the edge 2-4 of length 7, so the shortest 1-to-5 distance is 9 and the baseline round trip is 18.

The direct cycle edge has weight 7, so it cannot be used for portal activation because k is 4. On the other arc, however, each edge has weight 4. We can choose u = 2 and v = 3.

| Variable | Value |
| --- | --- |
| First endpoint u | 2 |
| Prefix to u | 1 |
| Chosen arc | 2-3-4 |
| u to v | 4 |
| v to n | 4 + 1 = 5 |
| Total | 2(1) + 4 + 2(5) = 16 |

The same-block sliding window finds a maximum usable segment of length 4 on the long arc. The answer becomes 16, improving on the no-portal value of 18.

This example demonstrates why a cycle cannot simply be replaced by its shortest arc. A longer arc may contain the only pair of vertices whose distance is within the portal timeout.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + e) + n log n) | The block traversal is linear, every state is generated a constant number of times, and every Fenwick operation costs O(log n). |
| Space | O(n + e) | The graph, block representation, compressed coordinates, and Fenwick tree are all linear in the input size. |

The structural restriction on the graph gives e = O(n), because each cycle contributes only one more edge than its number of vertices and the cycles are vertex-disjoint. With at most about 2n endpoint states, the Fenwick tree handles only O(n) updates and queries. This keeps the solution within the intended asymptotic limits for n = 300000.

## Test Cases

```python
import sys
import io

from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    try:
        solve()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

    return out.getvalue().strip()

# Provided sample
sample1 = """\
12 13 14
1 2 2
4 3 5
10 9 2
9 8 7
2 5 3
6 4 2
2 3 2
10 11 5
11 7 6
9 12 4
5 4 3
8 7 1
10 6 3
"""
assert run(sample1) == "24", "sample 1"

# Minimum-size graph, portal can be activated exactly at the timeout.
assert run("""\
2 1 5
1 2 5
""") == "5", "minimum size and k equality"

# Boundary case, the only edge is longer than k, so no portal can activate.
assert run("""\
2 1 4
1 2 5
""") == "10", "portal timeout boundary"

# Maximum-size path, all edge weights are equal.
# The whole path has length 299999 and can be used as the portal segment.
n = 300000
lines = [f"{n} {n - 1} 100000000"]
for i in range(1, n):
    lines.append(f"{i} {i + 1} 1")
large_case = "\n".join(lines) + "\n"

assert run(large_case) == "299999", "maximum-size all-equal chain"

# A longer cycle arc contains the only usable portal segment.
assert run("""\
5 5 4
1 2 1
2 3 4
3 4 4
4 2 7
4 5 1
""") == "16", "cycle arc and same-block portal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 24 | Cross-block portal placement and the sample's optimal cycle choices |
| `2 1 5 / 1 2 5` | 5 | Minimum graph and inclusive `distance <= k` boundary |
| `2 1 4 / 1 2 5` | 10 | Correct rejection when activation distance exceeds k |
| 300000-vertex unit chain | 299999 | Maximum input size, all-equal weights, and long cross-block window |
| Five-vertex graph with a cycle | 16 | Same-block handling and a portal endpoint inside a non-shortest cycle arc |

## Edge Cases

For the minimum graph

```
2 1 5
1 2 5
```

there is only one block. Its shortest length is 5, so the no-portal baseline is 10. The same-block calculation finds a segment of length 5 because the sliding window accepts equality with k. The resulting value is `2 * 5 - 5 = 5`.

For

```
2 1 4
1 2 5
```

the same sliding window immediately sees that the only edge has weight 5 > 4. Its usable segment length is zero, so no portal candidate improves the baseline. The algorithm returns 10.

For the chain

```
4 3 4
1 2 2
2 3 2
3 4 2
```

the shortest 1-to-4 distance is 6, giving a baseline of 12. The first endpoint can be vertex 1 and the second endpoint can be vertex 3. Their distance is 4, so the portal activates exactly at the timeout boundary. The resulting cost is

[
2\cdot0+4+2\cdot2=8.
]

The Fenwick sweep discovers this pair across multiple blocks. This is also the case that catches an implementation that incorrectly requires the second endpoint to be n.

For the cycle case

```
5 5 4
1 2 1
2 3 4
3 4 4
4 2 7
4 5 1
```

the shortest route through the cycle uses 2-4 with length 7, but that edge is too long for the portal. The other arc consists of two edges of length 4. The same-block sliding window finds the segment 2-3 with length 4. Its prefix is 1 and its suffix from 3 to 5 is 5, giving

[
2\cdot1+4+2\cdot5=16.
]

The answer is consequently 16, even though the ordinary shortest round trip is 18. This confirms that the algorithm must retain both arcs of every cycle instead of keeping only the shortest one.
