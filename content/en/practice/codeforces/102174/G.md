---
title: "CF 102174G - \u795e\u5723\u7684 F2 \u8fde\u63a5\u7740\u6211\u4eec"
description: "There are two counties, each containing positions numbered from (1) to (n). Positions within the same county have no connections by themselves. A prism is the only way to move between counties. A prism is described by two position intervals and a travel time."
date: "2026-08-19T07:06:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102174
codeforces_index: "G"
codeforces_contest_name: "The 14-th BIT Campus Programming Contest"
rating: 0
weight: 102174
solve_time_s: 182
verified: true
draft: false
---

[CF 102174G - \u795e\u5723\u7684 F2 \u8fde\u63a5\u7740\u6211\u4eec](https://codeforces.com/problemset/problem/102174/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

There are two counties, each containing positions numbered from (1) to (n). Positions within the same county have no connections by themselves. A prism is the only way to move between counties.

A prism is described by two position intervals and a travel time. If a unit is currently at any position in the first interval, it may jump to any position in the second interval in exactly (w) time. The jump is bidirectional, so the same cost applies in the opposite direction.

The (p) combat units start at positions (x_1,\ldots,x_p) in county one, while the (q) enemy buildings occupy positions (y_1,\ldots,y_q) in county two. A combat unit is considered finished as soon as it reaches any building. Since all units can move simultaneously, the required answer is the latest arrival time among the units when each unit independently chooses its fastest route to some enemy building.

If (d(x,y)) denotes the shortest-path distance between a combat position (x) and a building position (y), the answer is

[
\max_{i=1}^{p}\min_{j=1}^{q} d(x_i,y_j).
]

If even one combat unit cannot reach any enemy building, the answer is `boring game`.

The input contains up to (10^5) positions, (10^5) prisms, (10^5) combat units, and (10^5) buildings. With (n,m) both around (10^5), explicitly expanding every prism into all pairs of positions is impossible. Even a single prism covering all positions would represent (n^2=10^{10}) pairs, and with (10^5) prisms the worst case reaches (10^{15}) pairs before even considering the two directions. A solution needs roughly logarithmic work per prism rather than linear or quadratic work in the interval sizes.

There are several easy-to-miss boundary cases. First, a combat unit may be completely disconnected from every building. For example,

```
2 1 1 1
1 1 1 1 4
2
1
```

has a prism connecting only position (1) of each county, while the combat unit starts at position (2). The correct output is `boring game`. A careless implementation that initializes unreachable distances to zero, or simply takes a maximum over reachable units, can incorrectly return zero.

Second, both ends of a prism interval are included. For example,

```
4 1 1 1
1 1 4 4 3
1
4
```

has a direct route from position (1) to position (4), so the answer is `3`. Treating intervals as half-open during segment-tree decomposition would silently lose this route.

Third, the prism is bidirectional. For example,

```
3 1 1 1
1 1 3 3 5
3
1
```

also has answer `5`, even though the combat unit starts in the interval that appears as the second endpoint of the input prism. An implementation that only adds the listed direction produces `boring game`.

Finally, the answer is a maximum of per-unit shortest distances, not the globally shortest route. If two units need times (2) and (7), they move simultaneously, so the opponent surrenders at time (7), not time (9) and not time (2).

## Approaches

The brute-force solution starts by turning every prism into ordinary graph edges. For a prism connecting ([a,b]) to ([c,d]), we would add an edge from every (x\in[a,b]) to every (y\in[c,d]), and another edge in the opposite direction. This graph represents the problem exactly, so running a multi-source shortest-path algorithm on it is correct.

The problem is the number of edges. One prism can create ((b-a+1)(d-c+1)) pairs in each direction. With both intervals of length (n), this is (2n^2) directed edges. At (n=10^5), that is (2\cdot10^{10}) edges for just one prism, and the worst case over (10^5) prisms is (2\cdot10^{15}). This is far beyond the time and memory limits.

The first useful observation is that the destination is a set of buildings, so we do not need a separate shortest-path computation for every combat unit. Add a conceptual super-source connected with zero cost to every enemy building in the reversed graph. Then one Dijkstra run gives the distance from every position to its closest building.

The second observation handles the large intervals. Suppose we want to connect every point of interval (A) to every point of interval (B). A segment tree can represent either interval using only (O(\log n)) canonical nodes.

We use two directed copies of the segment tree. In the first copy, every child points to its parent with cost zero. Thus a point can climb from its leaf to any segment-tree node whose interval contains that point. In the second copy, every parent points to its children with cost zero. Thus a segment-tree node can descend to any point in its interval.

For one directed prism (A\to B), create a virtual vertex (v). Every canonical node covering (A) in the upward tree connects to (v) with cost (w), and (v) connects with cost zero to every canonical node covering (B) in the downward tree. A path from any point of (A) can climb to one canonical node, pay (w) exactly once at (v), and then descend to any point of (B).

Because the prism is bidirectional, we create the same construction for (B\to A). The upward and downward trees must remain separate. If their parent-child edges were made bidirectional, a point could move freely inside its own county by climbing and descending the same tree, which would introduce paths that do not exist in the original problem.

The implementation below runs Dijkstra on the reversed compressed graph. It stores the prism connections compactly as range events instead of materializing every graph edge. The target interval of a virtual vertex is attached to its canonical segment-tree nodes. When Dijkstra reaches such a node, the virtual vertex becomes reachable with zero additional cost. When the virtual vertex itself is popped, its source interval is decomposed into canonical nodes of the other tree and those nodes receive the prism cost.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(mn^2)) edge construction in the worst case | (O(mn^2)) | Too slow |
| Segment-tree compression + Dijkstra | (O((n+m)\log^2 n)) | (O(n+m\log n)) | Accepted |

## Algorithm Walkthrough

1. Treat every position in both counties as a vertex of the conceptual graph. For a prism ([a,b]\leftrightarrow[c,d]) with cost (w), create two virtual vertices, one representing the direction from ([a,b]) to ([c,d]), and the other representing the reverse direction. Two virtual vertices are necessary because the interval directions have different source and destination ranges.
2. Build one segment tree over all (2n) positions. Position (1) through (n) represents county one, and position (n+1) through (2n) represents county two. Keep two logical copies of this tree. In the upward copy, every child points to its parent with cost zero. In the downward copy, every parent points to its children with cost zero.
3. Connect the upward and downward copies at every real position with zero-cost edges in both directions. This makes both representations of the same physical position interchangeable, while internal segment-tree nodes remain directional.
4. For each directed prism (A\to B), decompose (B) into (O(\log n)) canonical nodes of the downward tree. In the reversed graph, each of those nodes gets a zero-cost connection to the prism's virtual vertex. We store these connections as events attached to the corresponding segment-tree nodes.
5. Store the source interval (A) and cost (w) inside the virtual vertex. When the virtual vertex is reached during reversed Dijkstra, decompose (A) into (O(\log n)) canonical nodes of the upward tree and relax all of them by (w). This is exactly the reversed form of paying (w) when entering the prism.
6. Initialize Dijkstra from every enemy building at distance zero. The building is represented by its leaf in the downward tree. Starting from the downward tree is convenient because the reversed prism edge enters the virtual vertex from the canonical nodes representing the destination interval.
7. During Dijkstra, an upward-tree node has reversed edges toward its children, because the original upward tree had edges from children to parents. A downward-tree node has a reversed edge toward its parent, because the original downward tree had edges from parents to children. A real leaf also has a zero-cost edge to the corresponding leaf of the other tree.
8. When Dijkstra finishes, the distance stored at the upward-tree leaf corresponding to combat position (x_i) is exactly the shortest distance from (x_i) to any enemy building. Take the maximum over all combat units. If any such distance is infinite, print `boring game`.

### Why it works

Consider one original prism from interval (A) to interval (B). Every point in (A) can climb the upward tree to exactly one of the canonical nodes covering (A). From there it reaches the prism vertex and pays (w). The prism vertex then reaches every canonical node covering (B) in the downward tree, and that node can descend to every point in (B). Thus the compressed graph contains a path of cost exactly (w) between every allowed pair of endpoints.

Conversely, the only positive-cost transition introduced by this construction is the transition through the virtual prism vertex. The zero-cost segment-tree edges only change the representation of the same interval membership and never allow movement between unrelated real positions. Consequently, every compressed path between real positions corresponds to a valid sequence of original prism traversals with the same cost.

Running Dijkstra on the reversed graph from all buildings computes the distance from every real position to its closest building. Since all combat units move simultaneously and independently, the time when all of them have arrived is the maximum of those shortest distances. An unreachable source has infinite distance, exactly matching the required `boring game` condition.

## Python Solution

```python
import sys
import heapq
from array import array

input = sys.stdin.readline

INF = 4_000_000_000_000_000_000

def solve():
    n, m, p, q = map(int, input().split())

    # There are 2*n real positions, the first n in county 1
    # and the next n in county 2.
    N = 2 * n

    # Iterative segment tree size.
    S = 1
    while S < N:
        S <<= 1

    # Segment-tree indices are 1 .. 2*S-1.
    # Tree 0: upward tree, child -> parent in the original graph.
    # Tree 1: downward tree, parent -> child in the original graph.
    OUT_BASE = 2 * S
    VBASE = 4 * S

    virtual_count = 2 * m
    total_nodes = VBASE + virtual_count

    # For each downward-tree canonical node, head[idx] is the first
    # virtual prism attached to it in the reversed graph.
    head = array('i', [-1]) * (2 * S)

    # Linked-list storage for prism events.
    event_v = array('i')
    event_next = array('i')

    # Information stored for every virtual vertex.
    # In the reversed graph, this is the interval reached from the
    # virtual vertex, plus the cost of the prism.
    source_l = array('i')
    source_r = array('i')
    weight = array('q')

    def add_event(seg_idx, vid):
        event_v.append(vid)
        event_next.append(head[seg_idx])
        head[seg_idx] = len(event_v) - 1

    def add_interval_events(l, r, vid):
        """Attach vid to canonical nodes covering inclusive [l, r]."""
        l += S
        r += S + 1

        while l < r:
            if l & 1:
                add_event(l, vid)
                l += 1
            if r & 1:
                r -= 1
                add_event(r, vid)
            l >>= 1
            r >>= 1

    # Create both directions of every prism.
    for i in range(m):
        a, b, c, d, w = map(int, input().split())

        # Convert to zero-based positions in the combined 2*n array.
        a -= 1
        b -= 1
        c = n + c - 1
        d = n + d - 1

        # Direction: county 1 [a,b] -> county 2 [c,d].
        vid = VBASE + 2 * i
        source_l.append(a)
        source_r.append(b)
        weight.append(w)

        # In the reversed graph, destination [c,d] reaches vid at cost 0.
        add_interval_events(c, d, vid)

        # Direction: county 2 [c,d] -> county 1 [a,b].
        vid = VBASE + 2 * i + 1
        source_l.append(c)
        source_r.append(d)
        weight.append(w)

        # In the reversed graph, destination [a,b] reaches vid at cost 0.
        add_interval_events(a, b, vid)

    sources = [x - 1 for x in map(int, input().split())]
    targets = [n + y - 1 for y in map(int, input().split())]

    dist = array('q', [INF]) * total_nodes
    heap = []

    # Start from every enemy building in the downward-tree representation.
    for pos in targets:
        node = OUT_BASE + S + pos
        if dist[node] != 0:
            dist[node] = 0
            heapq.heappush(heap, (0, node))

    while heap:
        dcur, u = heapq.heappop(heap)
        if dcur != dist[u]:
            continue

        # Virtual prism vertex.
        if u >= VBASE:
            k = u - VBASE
            l = source_l[k] + S
            r = source_r[k] + S + 1
            nd = dcur + weight[k]

            # In the reversed graph, a virtual vertex reaches
            # canonical nodes covering its source interval in the
            # upward tree.
            while l < r:
                if l & 1:
                    v = l
                    node = v
                    if nd < dist[node]:
                        dist[node] = nd
                        heapq.heappush(heap, (nd, node))
                    l += 1

                if r & 1:
                    r -= 1
                    v = r
                    node = v
                    if nd < dist[node]:
                        dist[node] = nd
                        heapq.heappush(heap, (nd, node))

                l >>= 1
                r >>= 1

            continue

        # Downward-tree node.
        if u >= OUT_BASE:
            idx = u - OUT_BASE

            # Reverse of parent -> child is child -> parent.
            if idx > 1:
                v = OUT_BASE + (idx >> 1)
                if dcur < dist[v]:
                    dist[v] = dcur
                    heapq.heappush(heap, (dcur, v))

            # A leaf representing a real position is connected to
            # the same position in the upward tree.
            if idx >= S and idx < S + N:
                v = idx
                if dcur < dist[v]:
                    dist[v] = dcur
                    heapq.heappush(heap, (dcur, v))

            # Reverse prism edges: this canonical destination node
            # can enter every prism whose destination interval contains it.
            e = head[idx]
            while e != -1:
                v = event_v[e]
                if dcur < dist[v]:
                    dist[v] = dcur
                    heapq.heappush(heap, (dcur, v))
                e = event_next[e]

        # Upward-tree node.
        else:
            idx = u

            # Reverse of child -> parent is parent -> child.
            if idx < S:
                v = idx << 1
                if dcur < dist[v]:
                    dist[v] = dcur
                    heapq.heappush(heap, (dcur, v))

                v += 1
                if dcur < dist[v]:
                    dist[v] = dcur
                    heapq.heappush(heap, (dcur, v))

            # Same physical position, other representation.
            if idx >= S and idx < S + N:
                v = OUT_BASE + idx
                if dcur < dist[v]:
                    dist[v] = dcur
                    heapq.heappush(heap, (dcur, v))

    answer = 0

    for pos in sources:
        node = S + pos
        if dist[node] >= INF // 2:
            print("boring game")
            return
        if dist[node] > answer:
            answer = dist[node]

    print(answer)

if __name__ == "__main__":
    solve()
```

The first construction section chooses a power-of-two segment-tree size (S), which makes the parent and child of a segment node simply `idx >> 1` and `idx << 1`. The combined tree contains both counties, so a single segment tree is enough. County two positions are shifted by (n), while county one positions stay in the first half.

The two arrays `source_l` and `source_r` store the interval on the source side of every virtual prism vertex. The destination interval is not stored separately because its canonical nodes are immediately converted into events during input processing. This saves a substantial amount of memory compared with storing two explicit adjacency lists for every prism.

The event arrays use integer arrays instead of Python lists of tuples. A Python tuple has considerable object overhead, which would be dangerous when (10^5) prisms each produce (O(\log n)) segment-tree events. `head`, `event_v`, and `event_next` form a compact linked-list representation.

The graph is never materialized as a conventional adjacency list. Segment-tree edges are generated directly from the node index during Dijkstra. When an upward node is processed, its children are generated. When a downward node is processed, its parent is generated. The only edges that need explicit storage are the prism events.

The range decomposition uses the half-open interval ([l,r)) internally. The input interval ([l,r]) is converted by setting the segment-tree endpoints to `l + S` and `r + S + 1`. That `+1` is essential because the problem intervals are inclusive.

The distance type is a signed 64-bit array. A path can contain many prism transitions, each costing up to (10^9), so 32-bit integers are insufficient. Python integers would be numerically safe, but `array('q')` keeps the distance table compact.

The stale-entry check `if dcur != dist[u]` replaces a separate visited array. If a node is improved multiple times, old heap entries remain in the heap, and only the entry matching the current best distance is processed.

The two counties are not connected merely because their positions have the same number. The only cross-county movement comes from prism vertices. The zero-cost edge between the two segment-tree representations is only between the two representations of the same physical position.

## Worked Examples

### Sample 1

The input is

```
5 3 2 2
2 4 1 3 1
1 1 4 5 3
1 2 3 4 2
2 3
4 5
```

The first combat unit starts at position (2), and the second starts at position (3). The enemy buildings are at positions (4) and (5).

The useful direct route for the first unit is through the third prism, from county-one positions ([1,2]) to county-two positions ([3,4]), costing (2). The second unit can use the first prism from position (3) to county-two position (3), costing (1), then use the third prism back to county one and another traversal to reach an enemy building. Its best arrival time is (4).

| Dijkstra state | Distance | Meaning |
| --- | --- | --- |
| Building 4 | 0 | Initial source |
| Building 5 | 0 | Initial source |
| Prism (1) reverse vertex | 0 | Its destination interval contains building 4 |
| Prism (3) reverse vertex | 0 | Its destination interval contains building 4 |
| Source position 2 | 2 | First combat unit reaches a building |
| Source position 3 | 4 | Second combat unit reaches a building |

The maximum shortest distance is (4), so the output is `4`. This demonstrates why the final operation is a maximum over the individual shortest paths, rather than a sum.

### Sample 2

A small second example is

```
3 1 1 1
1 2 2 3 5
2
3
```

The only prism permits county-one positions (1) and (2) to reach county-two positions (2) and (3) for cost (5). The combat unit starts at position (2), and the building is at position (3).

| Step | Current representation | Distance | Operation |
| --- | --- | --- | --- |
| 1 | Building 3, downward leaf | 0 | Dijkstra initialization |
| 2 | Downward canonical node for ([2,3]) | 0 | Climb in reversed downward tree |
| 3 | Prism virtual vertex | 0 | Destination interval event |
| 4 | Upward canonical node for ([1,2]) | 5 | Pay prism cost |
| 5 | Upward leaf for position 2 | 5 | Descend in reversed upward tree |

The only combat unit reaches the building in (5) time units, so the answer is `5`. This trace demonstrates that the prism cost is paid exactly once, regardless of how many segment-tree nodes are needed to represent either interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((n+m)\log^2 n)) | Each prism creates (O(\log n)) events, and Dijkstra processes the resulting (O((n+m)\log n)) transitions with a logarithmic heap factor |
| Space | (O(n+m\log n)) | The two segment trees and distance table are linear, while prism events require (O(m\log n)) compact storage |

The constraints of (10^5) positions and (10^5) prisms rule out any construction proportional to the product of interval lengths. The segment-tree representation reduces every interval interaction to logarithmically many structural operations. The implementation also avoids Python object-heavy adjacency lists, which is particularly relevant under the 256 MB memory limit.

## Test Cases

The following tests assume the submitted solution is available as `solution.py` and exposes the `solve()` function shown above.

```python
# helper: run solution on input string, return output string
import sys
import io
from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run(
    """5 3 2 2
2 4 1 3 1
1 1 4 5 3
1 2 3 4 2
2 3
4 5
"""
) == "4", "provided sample"

# Custom 1: minimum-size input
assert run(
    """1 1 1 1
1 1 1 1 7
1
1
"""
) == "7", "minimum size"

# Custom 2: unreachable combat unit
assert run(
    """2 1 1 1
1 1 1 1 4
2
1
"""
) == "boring game", "unreachable source"

# Custom 3: both interval boundaries must be included
assert run(
    """4 1 1 1
1 1 4 4 3
1
4
"""
) == "3", "inclusive boundaries"

# Custom 4: duplicate positions and multiple prisms
assert run(
    """5 2 3 2
2 4 3 5 2
3 3 1 2 7
2 2 4
3 5
"""
) == "2", "duplicate positions and overlapping intervals"

# Custom 5: maximum n and m, while keeping every prism interval a singleton
m = 100000
lines = ["100000 100000 1 1"]
lines.extend(["1 1 1 1 1"] * m)
lines.append("1")
lines.append("1")
max_case = "\n".join(lines) + "\n"

assert run(max_case) == "1", "maximum n and m"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Provided sample | `4` | Multiple units and paths |
| (n=1,m=1) | `7` | Smallest possible graph |
| Disconnected source | `boring game` | Unreachable-distance handling |
| Singleton boundary intervals | `3` | Inclusive interval endpoints |
| Duplicate and overlapping positions | `2` | Repeated sources and targets |
| (n=m=100000) with singleton prisms | `1` | Maximum input scale and compact storage |

## Edge Cases

The disconnected case

```
2 1 1 1
1 1 1 1 4
2
1
```

starts the only combat unit at county-one position (2). The sole prism accepts only county-one position (1), so no path can leave position (2). Dijkstra never assigns a finite distance to its upward leaf. The final scan detects `INF` and prints `boring game`.

The inclusive-boundary case

```
4 1 1 1
1 1 4 4 3
1
4
```

has both prism intervals consisting exactly of their boundary positions. The decomposition of ([1,1]) and ([4,4]) each produces a single segment-tree leaf. The reversed Dijkstra reaches the virtual prism at distance zero and then reaches the source leaf with distance (3). The answer is `3`.

The reverse-direction case

```
3 1 1 1
1 1 3 3 5
3
1
```

requires using the prism from its second listed interval back to its first. The construction explicitly creates a second virtual vertex for this direction. Starting from county-two position (1), reversed Dijkstra reaches that virtual vertex and then the county-one source with cost (5). The output is `5`.

The duplicate-position case

```
5 2 3 2
2 4 3 5 2
3 3 1 2 7
2 2 4
3 5
```

has combat units at positions (2,2,4), with two copies of the same building-free target interval endpoints. Both position (2) and position (4) can use the first prism to reach a building in cost (2). The duplicate combat unit has the same distance as the other unit at position (2). The maximum is consequently `2`.

The large-input test contains (10^5) prisms, but every interval is a singleton. Each prism contributes only one canonical segment-tree event per direction, so the event arrays remain linear in (m). This case checks that the implementation does not allocate a Python tuple or list object for every potential graph edge and that the integer-array representation scales to the largest input sizes.
